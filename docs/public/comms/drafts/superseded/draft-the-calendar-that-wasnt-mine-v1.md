# The Calendar That Wasn't Mine

*January 28*

[alt text: Two mailboxes side by side with letters spilling between them, some clearly meant for one ending up in the other]
Caption: "The walls existed. The isolation didn't."

Tuesday afternoon. I'm testing the alpha release with a fresh account — username "alfamux," our second real user slot. I connect my Google Calendar, expecting to see my own schedule.

The calendar shows meetings I've never heard of. A dentist appointment in a city I don't live in. A standup for a team I'm not on.

These are someone else's calendar events. Showing up in my account. On a system I built to be multi-user.

## The leak

Multi-tenancy is supposed to mean isolation. User A's data stays with User A. User B's data stays with User B. The walls between accounts are supposed to be absolute.

[PM PLACEHOLDER: The moment you realized what you were seeing - someone else's actual calendar]

The walls weren't there. Or rather — they were there for some things and not others. User accounts existed. Login worked correctly. The database had `owner_id` columns on most tables. It looked multi-tenant. It felt multi-tenant.

But the calendar integration stored OAuth tokens globally. When I connected my calendar, the system saved my Google credentials. When the next user came along, the system retrieved... my credentials. Because they were the only credentials there. No user scoping. No isolation. Just a global token bucket.

One user's calendar. Showing in another user's account. The leak was complete.

## The archaeology

This wasn't a new bug. This was an old assumption, finally visible.

Back in October 2025, we'd added multi-user support. The commit looked comprehensive — user accounts, authentication, `owner_id` foreign keys on the main tables. The PR passed review. The tests passed. Multi-user: done.

[PM PLACEHOLDER: The October commit - what you remember about that work, whether it felt complete at the time]

Except the integration layer never got updated. Calendar tokens, Slack credentials, GitHub connections — all the external service authentication still used global storage. The October commit updated the core, but the edges remained single-tenant.

Eight months of development on top of that foundation. Features built, bugs fixed, patterns established — all assuming the multi-user support was complete. It wasn't. The calendar leak proved it.

## The scope of the problem

Once we knew what to look for, we found it everywhere.

Calendar tokens: global. Slack tokens: global. GitHub tokens: global. Notion tokens: global. Every external integration stored credentials without user context.

[PM PLACEHOLDER: The audit process - systematically checking each integration]

And it wasn't just tokens. The projects table had a unique constraint on `name` — globally unique, not per-user unique. Two users couldn't both have a project called "Q1 Planning." The constraint would reject the second one. Data isolation failure of a different kind.

The API key storage used a global prefix. The config services didn't require user context. The OAuth callbacks didn't verify which user initiated the flow.

We'd built multi-user authentication on top of single-user infrastructure. The login was isolated. Everything behind it wasn't.

## The fix that couldn't be incremental

My Lead Developer proposed a phased approach: update each integration one at a time, make `user_id` optional at first, gradually require it everywhere. Safe. Incremental. Low risk.

My Chief Architect said: make `user_id` required from the start.

[PM PLACEHOLDER: The conversation with the Architect - whether the advice surprised you]

The reasoning: optional parameters create hiding places. If `user_id` is optional, code paths that don't provide it will continue to work. They shouldn't work — they're the exact paths that leak data — but they will. The migration "completes" with gaps still hidden.

Required parameters create a forcing function. Every code path that lacks user context fails immediately. The failures tell you exactly where to look. No hiding. No gradual drift. No "we'll get to that later."

We made `user_id` required from Phase 1.

## Nine phases

The fix touched everything.

Phase 1: Repositories require `owner_id`. No more optional user context. Every database operation scoped to a specific user.

Phase 2: OAuth investigation. Map every token storage and retrieval path. Find every place credentials flow without user context.

Phase 3: RequestContext enforcement. Every authenticated request carries user identity. Middleware validates it. No anonymous operations on protected resources.

[PM PLACEHOLDER: The day of execution - how it felt to have so many things break at once]

Phase 4: Repository isolation tests. Eighteen new tests verifying that User A cannot access User B's data through any repository method.

Phase 5: OAuth state redesign. The OAuth callback now embeds `user_id` in the state parameter. When Google redirects back, we know which user initiated the flow.

Phase 6: Credential storage separation. `IntegrationConfigService` for app-level credentials. `UserTokenService` for user-specific tokens. Clear separation, clear ownership.

Phase 7: Config service signatures. Every method that touches user data requires `user_id` as a parameter. No more inferring. No more globals.

Phase 8: Singleton manager refactor. The conversation managers, the onboarding managers — all the stateful services now explicitly track which user they're serving.

Phase 9: Workspace activation. The `workspace_id` concept that had been designed but dormant, finally wired in as the future path for team isolation.

94 new tests. ADR-058 documenting every decision. One day of execution.

## What the forcing function revealed

The Architect was right. Making `user_id` required immediately surfaced gaps we wouldn't have found otherwise.

A webhook handler that processed Slack events without checking which user's Slack connection triggered them. An OAuth callback that stored tokens before verifying the user session. A config lookup that fell back to global defaults when user-specific values weren't found.

[PM PLACEHOLDER: Specific gaps the forcing function revealed - things that would have been easy to miss]

Each failure was a discovery. Each discovery was a fix. By the end of the day, the system was genuinely isolated — not "mostly isolated" or "isolated except for edge cases." Every code path either handled user context explicitly or had been deliberately designed for system-level operations.

## The October lesson

The October 2025 commit wasn't wrong. Adding user accounts, authentication, and `owner_id` columns was necessary work. The mistake was assuming it was complete.

Multi-tenancy isn't a feature you add. It's a property that must hold everywhere. One leaky integration undermines the entire model. One global token bucket means the walls don't exist.

[PM PLACEHOLDER: How you think about "complete" differently now - the difference between adding a feature and ensuring a property]

The October commit added the structure. The January fix ensured the property. Eight months between them — eight months where the system looked multi-tenant but wasn't.

## The calendar now

I tested again after the fix. Fresh account, fresh calendar connection. The events that appeared were mine. Only mine. The dentist appointment in the wrong city was gone. The standup for the team I'm not on was gone.

[PM PLACEHOLDER: The feeling of seeing your own calendar after seeing someone else's]

The walls exist now. 94 tests verify they hold. ADR-058 documents why they're built this way. The forcing function ensured we found every gap.

One day of aggressive fixing. Eight months of hidden assumptions surfaced. User A's calendar stays with User A.

That's what multi-tenancy actually means.

---

*Next on Building Piper Morgan: The Forcing Function, where one piece of architectural advice from this fix revealed a principle worth applying everywhere.*

*Have you discovered that "multi-user support" wasn't as complete as you thought? What finally revealed the gaps?*
