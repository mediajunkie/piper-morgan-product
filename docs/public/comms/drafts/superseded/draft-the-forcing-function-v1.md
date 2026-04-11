# The Forcing Function

*January 30*

[alt text: A puzzle piece that only fits in one orientation, with several wrong-orientation attempts visible]
Caption: "If it fits wrong, you find out immediately."

We were planning a multi-tenancy fix. Nine phases of work across dozens of files. The question was sequencing: where to start?

The original plan made `owner_id` optional first—update the function signatures to accept user context, then gradually require it everywhere. Incremental. Low risk. Each phase builds on the last.

My Chief Architect said: make it required from the beginning.

## The counterintuitive advice

Making `owner_id` optional first seems safer. You can update call sites one at a time. Nothing breaks while you're in the middle of the migration. Each commit is a small, safe step forward.

Making `owner_id` required immediately seems risky. Suddenly every call site without user context fails. The codebase breaks until you fix everything. More pressure, more urgency, more things going wrong at once.

[PM PLACEHOLDER: Initial reaction to the advice - did it feel risky?]

But here's what the Architect understood: when you make a constraint optional, you create hiding places. Code paths that don't pass `owner_id` continue to work. They shouldn't work—they're missing required context—but they do. The migration "completes" with gaps you don't know about.

When you make the constraint required immediately, every gap reveals itself. The code breaks in exactly the places that need fixing. No hiding. No gradual drift. No "we'll get to that later."

## The forcing function principle

A forcing function is a constraint that makes the right behavior unavoidable. It doesn't suggest. It doesn't recommend. It requires.

Making `owner_id` required created a forcing function. Every code path now had to handle user context or fail immediately. We couldn't accidentally ship multi-tenancy that worked for some paths but not others. The constraint forced completeness.

[PM PLACEHOLDER: Forcing functions in your own work - constraints that made correctness unavoidable]

The alternative—optional parameters, gradual migration, incremental adoption—creates what looks like progress without the underlying guarantee. You update twenty call sites, feel good about the progress, miss the twenty-first because it happens to work without the parameter.

Forcing functions trade comfort for confidence. The migration is more uncomfortable—more things break, more urgency to fix them. But when it's done, it's actually done. No hidden gaps. No "mostly migrated."

## How we applied it

Phase 1 of the multi-tenancy fix: make `owner_id` required in the repository layer. Immediately, every service that called the repository without user context failed.

This felt aggressive. The test suite lit up with failures. Code that had been running fine for months suddenly didn't work.

But each failure was a discovery. Here's a service that doesn't have user context. Here's a code path that assumed global state. Here's an edge case we didn't know existed.

[PM PLACEHOLDER: Specific discoveries from the forcing function - gaps you wouldn't have found otherwise?]

We fixed them one by one. Not because we were methodically searching—because the failures told us exactly where to look. The forcing function converted "audit every call site" into "fix what breaks."

By the end of Phase 1, the repository layer was genuinely multi-tenant. Not "mostly multi-tenant." Not "multi-tenant except for edge cases we haven't found yet." Every call site either provided user context or had been deliberately designed to work without it.

## Where it applies

The principle extends beyond database migrations.

API versioning: don't support both old and new formats indefinitely. Pick a deprecation date and enforce it. The forcing function reveals which clients haven't migrated.

Feature flags: don't leave flags in "percentage rollout" forever. Move to 100% or remove the feature. The forcing function reveals whether the feature actually works.

Code reviews: don't allow "we'll clean this up later" comments. Either clean it up now or explicitly defer with a tracked issue. The forcing function reveals whether cleanup ever happens.

[PM PLACEHOLDER: Other domains where forcing functions apply - hiring? team processes?]

The pattern is consistent: gradual migration creates hiding places; hard cutoffs reveal gaps. Discomfort during the transition is the price of confidence after.

## The tradeoff

Forcing functions aren't free. They create pressure. They surface problems faster than you might be ready to solve them. They can overwhelm a team if the scope is too large.

The Architect's advice came with context: we were doing a nine-phase migration with explicit scope. The forcing function applied to each phase, not to the entire migration at once. Phase 1 required `owner_id` in repositories. Phase 2 required it in services. Each phase had a bounded forcing function.

[PM PLACEHOLDER: When forcing functions would be too aggressive - scope too large, team too small?]

Forcing functions work best when the scope is clear and the team can handle the pressure. They work worst when they create chaos without providing clarity.

## What we learned

The multi-tenancy migration completed in one day. 94 new tests. Every code path explicitly handling user context. No hidden gaps, no edge cases waiting to fail in production.

Without the forcing function, we might have spent that day feeling productive while missing call sites. We might have shipped "multi-tenancy" that worked for most users but leaked data between accounts for edge cases. We might have discovered the gaps months later, in production, with real user data.

[PM PLACEHOLDER: How the day felt with forcing function pressure vs. how it might have felt without]

The Architect's advice cost us comfort. It bought us confidence. That's the forcing function tradeoff: harder migration, better result.

Make the constraint required from the beginning. Let the failures tell you where to look. Trust the discomfort—it's revealing the gaps you need to find anyway.

---

*Next on Building Piper Morgan: [PM to decide - could tease the Sprint Gate pattern if ready, or another piece from the pipeline]*

*Where have you used forcing functions—hard constraints that revealed gaps you wouldn't have found with gradual migration? When did the discomfort pay off?*
