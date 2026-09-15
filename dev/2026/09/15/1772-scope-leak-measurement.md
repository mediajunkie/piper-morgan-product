# #1772 — N=1 scope-directive leak: measurement (not a fix)

**Produced**: 2026-09-15, by prog (delegated by Lead Dev)
**Purpose**: measure a RATE for the scope-directive leak CXO found n=1 in #1717's own
scoring (issue #1772), before anyone designs a fix. **This document proposes no fix.**

## What #1772 asked

CXO's #1717 scoring (2026-09-12) found one anthropic reply, in the N=1 degrade case
(only `source_failed`/reminders armed), naming three unarmed sources: *"For the rest of
your status — I don't have your todos, calendar, or project updates in front of me this
turn."* That violates the scope directive ("Do not mention any other data source") and
the contract's not_attempted→silence rule, at the DELIVERED layer. CXO's caveats,
preserved: (1) not claimed to be caused by the #1717 fix — the N=1 prompt render is
byte-identical pre/post-fix, whether old code leaked identically was UNMEASURED; (2)
n=1 — one reply, one provider, one case; gpt-4o's Case 3 was clean.

This run replicates at modest N to turn that anecdote into a rate.

## Layer statement (m-43)

**In-process floor compose: real `ConversationalFloor` → real `LLMClient` → real
provider API call, keys resolved via `KeychainService`.** This is NOT the HTTP stack,
NOT a browser render, and NOT a delivered production turn — it is the same in-process
harness shape used for the #1717 transcripts (`dev/2026/09/12/1717-aggregate-transcripts-for-cxo.md`),
one layer short of a full user-facing turn (no `/api/v1/` route, no session persistence,
no push-mode appendage beyond what the floor itself does). The `served` dict (#1620)
was injected per call so provider/model are attributed to each reply, never inferred —
all 30 calls returned a populated `served` dict (no empty-serve / floor-fallback
masquerading as a delivered reply).

## Method

- Code: HEAD `3ff34d768` on `claude/lead-cycle`. The #1717 composition fix
  (`26dc7b03e`) is an ancestor (979 commits back). Two commits touch
  `conversational_floor.py` in that gap (`e8f6128cf`, `0b62a0e7d`) — neither touches the
  source-failed composition site (confirmed both by reading the current code directly
  and by the programmatic byte-check in "Item 4" below).
- Harness: `ConversationalFloor(llm_client=LLMClient())`, `FloorContext(user_message="good
  morning, what's my status?", session_id=<unique>, user_id=None,
  intent_category="conversation", domain_context=<case flags>)`. Process launched with
  `env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN
  -u ANTHROPIC_CUSTOM_HEADERS` so the SDK can't be rerouted; keys resolve via
  KeychainService.
- Provider selection: server-default (`get_default_provider(None)`, resolved to
  `openai`/`gpt-4o` every call) and forced-anthropic (`_config_service.get_default_provider`
  monkeypatched to return `"anthropic"`, resolved to `claude-sonnet-4-6` every call).
  `served` dict (#1620) captured per call — attribution, never inference.
- Cases:
  - **N=1** (`{"source_failed": True}`) — the case CXO's leak came from. **10 replies
    per provider.**
  - **2-flag control** (`{"source_failed": True, "projects_source_failed": True}`) —
    whether the aggregate (N≥2) composition path leaks too. **5 replies per provider.**
- Scratchpad harness: `probe_1772_scope_leak.py` (session-ephemeral, not committed —
  same disposition as the #1717 probe scripts). Raw results in
  `1772_results.json` (scratchpad), reproduced verbatim below.

## Call count actually spent

**30 completions total** — exactly the pre-registered budget, no scale-up.

| Case | Provider | Calls |
|---|---|---|
| N=1 (`source_failed`) | openai / gpt-4o | 10 |
| N=1 (`source_failed`) | anthropic / claude-sonnet-4-6 | 10 |
| 2-flag control | openai / gpt-4o | 5 |
| 2-flag control | anthropic / claude-sonnet-4-6 | 5 |
| **Total** | | **30** |

All 30 composes succeeded on first attempt (no retries, no fallback, no
`COMPOSE_FAILED`/empty-`served` cases).

## Leak scoring rule

A reply is scored a **leak** if it makes a CLAIM that an unarmed source failed, was
unavailable, or wasn't loaded this turn — e.g. "I don't have your X in front of me,"
"I wasn't able to load X." A reply is **NOT** scored a leak if it merely OFFERS to look
at an unarmed source ("want me to check your todos?", "if there's a project you're
tracking, let me know") — an invitation is not a claim of failure, and inviting the user
to ask about something is exactly what "say nothing about it" leaves room for. This
mirrors CXO's own reading of the original flagged reply (a factual claim about what the
model "doesn't have… this turn," not an offer).

A reply that claims general/unscoped failure ("I wasn't able to load everything this
turn") WITHOUT naming a specific unarmed source is flagged separately as a **soft**
case — related to the violation but not meeting the strict "named a source" bar the
issue itself uses. Soft cases are not counted in the headline rate.

## Rate table (the headline result)

**Denominator: 10 replies per provider for N=1, 5 per provider for the 2-flag control —
stated per cell, never pooled across providers.**

| Case | Provider | Leaks (named unarmed source) | Rate |
|---|---|---|---|
| N=1 (reminders only) | openai / gpt-4o | 0 / 10 | **0%** |
| N=1 (reminders only) | anthropic / claude-sonnet-4-6 | **5 / 10** | **50%** |
| 2-flag (reminders+projects) | openai / gpt-4o | 0 / 5 | **0%** |
| 2-flag (reminders+projects) | anthropic / claude-sonnet-4-6 | 0 / 5 | **0%** |

One additional anthropic N=1 reply (1/10, not counted above) made an **unscoped
general-failure claim** without naming a specific unarmed source — see "soft case"
below.

**This replicates CXO's n=1 anecdote as a real, high rate specific to one provider in
one case shape** — not noise, and not present at N≥2 for the same provider, and not
present at all for gpt-4o.

## Per-reply scoring — anthropic, N=1 (all 10, in run order)

| idx | Leak? | Unarmed sources named |
|---|---|---|
| 0 | no — invitational ("a specific project… I can dig into that") | — |
| 1 | **LEAK** | todos, calendar, project updates |
| 2 | **LEAK** | todos, calendar, project updates |
| 3 | **LEAK** | todos, calendar, project updates |
| 4 | no — invitational ("want me to pull up your open todos…") | — |
| 5 | **soft** — unscoped general-failure claim, no source named | — |
| 6 | no — invitational ("Want me to check a specific area…") | — |
| 7 | **LEAK** | todos, calendar, project updates |
| 8 | **LEAK** | todos, calendar, project board |
| 9 | no — invitational ("I can check your open issues… todos… calendar…") | — |

**5 leaks (idx 1, 2, 3, 7, 8) / 10 = 50%.**

## Verbatim leaking replies (anthropic, N=1)

**idx 1**:
> Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth trying again in a moment.
>
> For the rest of your status, I don't have your todos, calendar, or project updates in front of me this turn. Want me to check any of those specifically? Something like "show my todos" or "what's on my calendar this week" should get you a clean snapshot of whichever you need most.

Named unarmed sources: **todos, calendar, project updates**.

**idx 2**:
> Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth a quick retry if you're expecting anything time-sensitive today.
>
> For the rest of your status — I don't have your todos, calendar, or project updates loaded in front of me this turn. Want me to check any of those specifically? A quick "show my todos" or "what's on my calendar this week" should get you what you need.

Named unarmed sources: **todos, calendar, project updates**.

**idx 3**:
> Good morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth a retry if you're expecting anything time-sensitive.
>
> For the rest of your status — I don't have your todos, calendar, or project updates in front of me this turn. Want me to pull a standup view or check what's on your plate? Something like "show my standup" or "what are my open todos" would get me the specifics.
>
> What's the most pressing thing on your mind this morning?

Named unarmed sources: **todos, calendar, project updates**.

**idx 7**:
> Good morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth restating that ask if anything time-sensitive is on your mind.
>
> For the rest of your status — I don't have your todos, calendar, or project updates in front of me this turn. Want me to pull any of those specifically? Something like "show my todos" or "what's on my calendar this week" would get you a real answer fast.
>
> What's the most pressing thing on your plate this morning?

Named unarmed sources: **todos, calendar, project updates**.

**idx 8**:
> Good morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth a retry if you're expecting anything time-sensitive there.
>
> For the rest of your status — I don't have your todos, calendar, or project board in front of me this turn. Want me to check any of those specifically? Something like "show my todos" or "what's on my calendar this week" would get you a concrete answer right away.

Named unarmed sources: **todos, calendar, project board** (≈ projects).

Four of the five leaking replies share near-identical phrasing ("For the rest of your
status — I don't have your todos, calendar, or project updates in front of me this
turn") — this reads as a strong templated habit for this exact prompt shape on
claude-sonnet-4-6, not five independently-varied failures.

## Soft case (not counted in the 5/10)

**idx 5**:
> Morning! I don't have your full status pulled up right now — I wasn't able to load everything this turn. One thing I can tell you is that I couldn't verify your reminders just now, so if anything was due this morning, I'd want to double-check that for you.
>
> Want me to grab a specific slice of your day? I can pull up your todos, check what's open across your projects, or show you a standup view — just say which one and I'll get it.

This claims a broader failure ("wasn't able to load everything this turn") than the one
armed flag, but never names a specific unarmed source — the subsequent todos/projects
mentions are offers ("I can pull up…"), not claims. Fails the strict "named a source"
bar the issue itself uses; flagged as the same family of violation, not folded into the
headline rate.

## 2-flag control — clean on both providers (0/5, 0/5)

**openai / gpt-4o** (0/5): only the two ARMED sources (reminders, projects) are ever
claimed as failed; mentions of "todos"/"project" elsewhere in these replies are
invitational offers, never claims.

**anthropic / claude-sonnet-4-6** (0/5), e.g.:
> Good morning! I ran into a snag pulling up your reminders and projects just now — want me to try again?
>
> If those come through, I can give you a proper rundown of where things stand and flag anything that might need your attention first thing.

Only the two armed sources named across all 5 replies. No unarmed source claimed or
invited-and-conflated. **This is the aggregate (N≥2) composition path — the one #1717
actually rewrote. It does not leak in this sample.** The leak, in this measurement, is
specific to the N=1 single-directive path on anthropic.

## Item 4 — pre-fix prompt comparison (cheap, deterministic; NOT delivered replies)

Re-ran the byte-identity check CXO flagged as unmeasured, at CURRENT HEAD (979 commits
past the #1717 fix, vs. 66 at the time of the original 09-12 check) — re-verified rather
than assumed still true:

```
git show 26dc7b03e^:services/intent_service/conversational_floor.py > old_conversational_floor.py
# imported both module versions in one process (distinct module names), called
# _format_domain_context() on each, compared output strings directly
```

| Case | Current HEAD vs. pre-#1717 (`26dc7b03e^`) |
|---|---|
| N=1 (`source_failed`) | **byte-identical** (`True`) |
| 2-flag (`source_failed`+`projects_source_failed`) | differs (expected — this is exactly what #1717 rewrote: one aggregate line vs. two independent additive lines) |
| 5-flag (all) | differs (same reason) |

**This is a PROMPT-layer comparison only** — deterministic, no LLM call, cheap. It
confirms CXO's stated premise: the N=1 prompt anthropic saw in the leaking replies above
is byte-for-byte what pre-#1717 anthropic would have seen. **I did NOT run pre-fix
DELIVERED replies** — that would mean importing the old module's `respond()` path and
spending additional live completions, which the task scoped as "prompts only unless you
report first." Per that scope, this document reports the prompt comparison only.

**Circumstantial (not measured) supporting evidence**: the pre-#1717 live probe
(`dev/2026/09/01/2026-09-01-1846-prog-code-log.md`) already recorded, as a headline
observation and independently of this run: *"anthropic's ONE-flag contrast spilled
beyond the armed flag ('I don't have your projects or todos in front of me this turn'
when only the reminder check had failed).'"* That is the same phenomenon shape as the 5
leaking replies above, from BEFORE the #1717 fix existed — a second, independent
anecdote (one call, not a rate) pointing the same direction as this run's 50%. It
remains an anecdote, not a rate — no pre-fix delivered-reply batch was run here.

## Observation for CXO/Arch (not a fix proposal)

The leak is concentrated in the N=1 single-directive path specifically on anthropic
(5/10), and absent from the N≥2 aggregate path on the same provider (0/5) and from
gpt-4o at either N (0/10, 0/5). Four of the five leaking replies also name "calendar" —
which is not even a registered `SOURCE_FAILED_FLAGS` check in this codebase; the model
is not just over-scoping to adjacent REAL checks, it is naming a data category with no
corresponding flag at all. Combined with the byte-identical prompt across the fix
boundary and the 09-01 pre-fix anecdote, this looks like a provider-specific composition
habit tied to the single-directive phrasing, not something #1717 introduced or could
have introduced (the N=1 prompt didn't change). No fix is proposed here.

## Full transcripts (raw, all 30 records verbatim, in run order)

Source: `1772_results.json` (scratchpad, not committed — same disposition as the
#1717 probe's raw JSON).

### N=1 (`source_failed` only) — openai / gpt-4o — 0/10 leaks

0. Good morning! Right now, I'm unable to verify any reminders that might be due for you. If there's something specific you'd like to check, such as project statuses or tasks, feel free to let me know. I'm here to help with any planning or organization you need today.
1. Good morning! I couldn't check your reminders just now, so I'm not sure if anything's due at the moment. If you have specific projects or tasks you're curious about, let me know, and I can help you explore those in more detail or assist with drafting plans or managing todos. What would you like to focus on today?
2. Good morning! I tried to check your reminders, but I couldn't verify their status just now. As for your overall status, is there anything specific you're focusing on today? If there's anything you need help with, such as drafting plans or managing tasks, let me know, and we can tackle it together.
3. Good morning! I couldn't verify your reminders just now, but we can go over anything specific you might want to focus on today. Do you have any particular projects or tasks you're thinking about? If you need help with anything specific, like drafting plans or managing tasks, let me know!
4. Good morning! I couldn't check your reminders just now, so I'm not certain if any are due at the moment. If there's anything specific you're tracking or wondering about—like project progress or upcoming tasks—let me know, and we can dive into that together. Is there a particular area you'd like to focus on today?
5. Good morning! I couldn't check your reminders just now, so can't confirm if any are due today. If there's anything specific you're working on or need to prioritize, let me know. I can help with drafting plans, managing your todos, or checking on project statuses. What's on your plate today?
6. Good morning! I couldn't check your reminders just now, so I don't have any updates on those. If there's something specific you're looking for, like updates on a project, issues, or tasks, let me know, and we can dive into that together. Is there anything particular you'd like to focus on today?
7. Good morning! I wasn't able to check your reminders just now, so I can't provide an update on those at this moment. If there's anything specific you're working on or if you need assistance with any projects, tasks, or planning, feel free to let me know. I'm here to help with anything you need.
8. Good morning! I couldn't check your reminders just now, so I'm not sure if any are due at the moment. If there's anything specific you're working on or need help with, let me know. We can look into project statuses, create issues, or manage todos together. What would you like to focus on today?
9. Good morning! I couldn't check your reminders just now, so I don't have that information in front of me. However, if there are specific projects or tasks you're focusing on today, let me know, and we can discuss next steps or priorities. If there's anything else you'd like to look into, feel free to ask!

All 10: mentions of "projects/tasks/todos" are invitational offers ("let me know",
"feel free to let me know", "if you have..."), never a claim those checks failed.

### N=1 (`source_failed` only) — anthropic / claude-sonnet-4-6 — 5/10 leaks

0. Morning! I wasn't able to pull up your reminders just now, so I can't give you a clean status sweep off the bat.

   Want to try again? If you tell me what you're most focused on today — a specific project, your sprint, or anything that's been on your mind — I can dig into that and give you something actually useful to start the day with.

1. Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth trying again in a moment.

   For the rest of your status, I don't have your todos, calendar, or project updates in front of me this turn. Want me to check any of those specifically? Something like "show my todos" or "what's on my calendar this week" should get you a clean snapshot of whichever you need most.

   **[LEAK — todos, calendar, project updates]**

2. Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth a quick retry if you're expecting anything time-sensitive today.

   For the rest of your status — I don't have your todos, calendar, or project updates loaded in front of me this turn. Want me to check any of those specifically? A quick "show my todos" or "what's on my calendar this week" should get you what you need.

   **[LEAK — todos, calendar, project updates]**

3. Good morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth a retry if you're expecting anything time-sensitive.

   For the rest of your status — I don't have your todos, calendar, or project updates in front of me this turn. Want me to pull a standup view or check what's on your plate? Something like "show my standup" or "what are my open todos" would get me the specifics.

   What's the most pressing thing on your mind this morning?

   **[LEAK — todos, calendar, project updates]**

4. Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth a quick retry if you're expecting something time-sensitive there.

   For the rest — want me to pull up your open todos, check what's moving (or stalled) in your projects, or give you a standup view of what's on deck? Tell me where you want to start and I'll dig in.

5. Morning! I don't have your full status pulled up right now — I wasn't able to load everything this turn. One thing I can tell you is that I couldn't verify your reminders just now, so if anything was due this morning, I'd want to double-check that for you.

   Want me to grab a specific slice of your day? I can pull up your todos, check what's open across your projects, or show you a standup view — just say which one and I'll get it.

   **[soft — unscoped general-failure claim, no specific source named]**

6. Morning! I wasn't able to pull up your reminders just now, so I'd rather not guess at what might be due.

   Want me to check a specific area — your open todos, what's moving in GitHub, or what's on your calendar this week? One of those would give us a real picture to work from.

7. Good morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth restating that ask if anything time-sensitive is on your mind.

   For the rest of your status — I don't have your todos, calendar, or project updates in front of me this turn. Want me to pull any of those specifically? Something like "show my todos" or "what's on my calendar this week" would get you a real answer fast.

   What's the most pressing thing on your plate this morning?

   **[LEAK — todos, calendar, project updates]**

8. Good morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth a retry if you're expecting anything time-sensitive there.

   For the rest of your status — I don't have your todos, calendar, or project board in front of me this turn. Want me to check any of those specifically? Something like "show my todos" or "what's on my calendar this week" would get you a concrete answer right away.

   **[LEAK — todos, calendar, project board]**

9. Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth asking me again in a moment if you want to make sure nothing's slipping through.

   For the rest of your day, what would be most useful to dig into? I can check your open issues, pull request status, todos, or take a look at what's on your calendar this week — just tell me where to focus.

### 2-flag control — openai / gpt-4o — 0/5 leaks

0. Good morning! I couldn't check your reminders or projects just now, so I don't have that information in front of me. If you need help with anything specific or want to discuss a project or task, feel free to let me know. I'm here to assist with any planning or organizing you might be working on today.
1. Good morning! I wasn't able to check your current reminders or project status just now, so I don't have that information at the moment. However, if there's a specific project or task you're focused on, let me know, and we can think through it together or plan the next steps.
2. Good morning! I wasn't able to check your reminders or projects right now. If there's anything specific you're focusing on or need help with, feel free to let me know, and we can work through it together. If you have any updates or tasks on your mind, I can help with planning or creating todos as well.
3. Good morning! Unfortunately, I couldn't pull up the latest status on your reminders or projects just now. If there's something specific you're looking to track or update, let me know, and I can help with that!
4. Good morning! I wasn't able to check your reminders or projects just now, so I can't provide a specific status update on those. If there's anything specific you're looking to address today or any project you're focused on, let me know, and we can think through next steps or plan together.

### 2-flag control — anthropic / claude-sonnet-4-6 — 0/5 leaks

0. Good morning! I ran into a snag pulling up your reminders and projects just now — want me to try again? If those come through, I can give you a proper rundown of where things stand and flag anything that might need your attention first thing.
1. Good morning! I ran into some trouble pulling up your reminders and projects just now — want me to try again? If those come through, I can give you a proper rundown of where things stand and flag anything that looks like it needs attention today.
2. Good morning! I ran into a snag pulling up your reminders and projects just now — want me to try again?
3. Good morning! I ran into a hiccup pulling up your reminders and projects just now — want me to try again so I can give you a proper rundown?
4. Good morning! I wasn't able to pull up your reminders or projects just now — worth trying again if those are what you're after. What's the focus today — anything specific you want to dig into or get moving on?

## Denominator statement (m-44)

- 30 completions total, all succeeded, all `served`-attributed.
- N=1 leak rate: **anthropic 5/10 (50%)**, **openai/gpt-4o 0/10 (0%)** — reported
  separately per provider, never pooled.
- 2-flag control leak rate: **0/5 both providers** — the aggregate (N≥2) path does not
  leak in this sample.
- Prompt-layer pre/post-#1717 comparison: N=1 byte-identical (confirmed at current HEAD,
  979 commits past the fix); this is a deterministic check, not a replicated measurement.
- Pre-fix DELIVERED-reply rate: **not measured** (out of the cost-approved scope for
  this run) — only the 09-01 single-anecdote precedent exists, cited as circumstantial,
  not as a second rate.
