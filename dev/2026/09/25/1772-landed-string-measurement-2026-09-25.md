# #1772 — landed N-agnostic scope-directive string: measurement

**Produced**: 2026-09-25, by prog (dispatched by Lead Developer)
**Purpose**: measure CXO's exact landed copy (Arch's mechanism ruling + CXO's copy
ruling, both 2026-09-24; landed on `main` `422d32f1db`, deployed on Fly v139) for the
N=1 case, closing the "still open on this issue" line from the landing comment. PM
approved (captured in `decisions.log` 2026-09-25 by Exec) a hard-capped ~20-completion
budget. **This document proposes no fix and does not close #1772** — the Lead decides
closure.

## Layer statement (m-43)

**In-process floor compose: real `ConversationalFloor` → real `LLMClient` → real
provider API call**, key resolved via `KeychainService.get_api_key(...)` and bound
per-call via `request_api_key(...)` (the #1809/#1812/#1819 chokepoint — every LLM call
now requires an explicit per-request key bind, str or provider-keyed mapping). This is
NOT the HTTP stack, NOT a browser render, and NOT a delivered production turn — it is
the same in-process harness shape used by the 09-15 and 09-24 measurements, one layer
short of a full user-facing turn.

## Confirmation the rendered string is CXO's landed copy, verbatim

Before spending any budget, the rendered N=1 line was printed by calling the REAL
`ConversationalFloor._format_domain_context({"source_failed": True})` directly (no
hand-transcription, no reading the source and assuming it matches):

```
[Available context about the user's current situation:
- DATA CHECKS FAILED this turn — could not check: reminders. If this becomes relevant, name what wasn't checked in ONE sentence — never one caveat per item. Don't claim it's empty or fine, and never invent details to fill the gap.
- Name ONLY the checks explicitly listed as FAILED above. Do not mention any other data source. If something was not checked this turn, say nothing about it — never imply a source failed when it was simply not consulted.
]
```

`MATCH: True` against the exact string in the dispatch. Worktree HEAD at measurement
time: `52e28b6945` (`422d32f1db`, the landing merge, is a direct ancestor — confirmed
via `git merge-base --is-ancestor 422d32f1db HEAD`). The composition site read directly
at `services/intent_service/conversational_floor.py` ~1385-1425 confirms the N==1/N≥2
split (and the registry's `directive` field) are gone, per the landing comment.

## Method

- Code: `services/intent_service/conversational_floor.py` at worktree HEAD `52e28b6945`
  (`422d32f1db` — the #1772 landing merge — is a direct ancestor). Single aggregate
  composition site (~1385-1425), `SOURCE_FAILED_FLAGS` registry (~150-181), no
  `directive` field, no N==1 special case — matches the landing comment's description.
- Harness: `ConversationalFloor(llm_client=LLMClient())`, `FloorContext(user_message="good
  morning, what's my status?", session_id=<uuid4 per call>, user_id=None,
  intent_category="conversation", domain_context={"source_failed": True})` — identical
  to 09-15/09-24.
- Provider forced to anthropic for cell 1: `llm._config_service.get_default_provider =
  lambda user_id=None: "anthropic"` on the `LLMConfigService` instance the `LLMClient`
  created. Cell 2 left the server default untouched (resolved to `openai`/`gpt-4o` on
  every call, matching the server's own configured default). Verified on **every one of
  the 20 calls** via the `served` dict (#1620) — never inferred from the monkeypatch
  alone: all 10 anthropic calls returned `{"provider": "anthropic", "model":
  "claude-sonnet-4-6"}`; all 10 openai calls returned `{"provider": "openai", "model":
  "gpt-4o"}`.
- Request-key bind (per #1809/#1812/#1819, required since the 09-24 run): both an
  anthropic key and an openai key were fetched via `KeychainService().get_api_key(...)`
  before spending any budget (the run aborts before the first call if either is
  missing). Cell 1 bound `request_api_key({"anthropic": <key>})`; cell 2 bound
  `request_api_key({"openai": <key>})` — provider-keyed mapping form (`#1819`), never
  the shell env, never hand-typed.
- Per call: `system_prompt = await floor._get_system_prompt(ctx)`, `prompt =
  floor._build_prompt(ctx)`, `served = {}`, then `llm.complete(task_type="conversation",
  prompt=prompt, system=system_prompt, user_id=None, served=served)` inside the key
  bind, then `strip_scaffolding_artifacts` / `strip_placeholder_slots` applied to the
  raw message (both return `(text, count)` tuples; the count was not inspected here) —
  mirrors `ConversationalFloor.respond()`'s own post-processing seam exactly.
- Launch: `env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN
  -u ANTHROPIC_CUSTOM_HEADERS venv/bin/python probe_1772_landed.py` (per CLAUDE.md's
  server-launch gotcha; keys resolved via KeychainService, never the shell env).
- Scratchpad harness (not committed, same disposition as prior probe scripts):
  `probe_1772_landed.py` and `confirm_1772_landed_string.py`, both in
  `/private/tmp/claude-501/-Users-xian-Development-piper-morgan-worktrees-lead/f47a0b3d-f896-4768-afd4-68880fc83efd/scratchpad/`.
  Raw results: `1772_landed_results.json` (same scratchpad dir), reproduced verbatim
  below.

## The rendered prompt, verbatim (identical across all 20 calls, both cells — only the
per-call `session_id` differs, which never enters the prompt text)

```
[Available context about the user's current situation:
- DATA CHECKS FAILED this turn — could not check: reminders. If this becomes relevant, name what wasn't checked in ONE sentence — never one caveat per item. Don't claim it's empty or fine, and never invent details to fill the gap.
- Name ONLY the checks explicitly listed as FAILED above. Do not mention any other data source. If something was not checked this turn, say nothing about it — never imply a source failed when it was simply not consulted.
]
User: good morning, what's my status?

[Context: The user's message relates to 'conversation'. Engage with their actual question. If your response naturally connects to something you can do (create issues, manage todos, check project status, draft plans), offer it as part of your response.]
```

Confirmed byte-identical between the anthropic-cell and openai-cell captured prompts
(`data['anthropic'][0]['prompt'] == data['openai'][0]['prompt']` → `True`) — there is
only ONE arm in this run (unlike the 09-24 candidate-vs-baseline design), because the
landed code has only one composition path now.

## Call count actually spent

**20 completions total — exactly the pre-approved hard cap, no scale-up, no retries
into budget.**

| Cell | Provider | Calls |
|---|---|---|
| Landed string, N=1 | anthropic / claude-sonnet-4-6 | 10 |
| Landed string, N=1 | openai / gpt-4o (server default) | 10 |
| **Total** | | **20** |

All 20 calls succeeded on first attempt (no fallback, no retries, no empty-`served`
cases) — every `served` dict individually confirmed against the intended provider.

## Scoring rule (identical to 09-15/09-24)

A reply **LEAKS** if it makes a CLAIM that an unarmed source (todos, calendar, projects,
GitHub, "project updates", etc. — anything other than reminders) failed, was
unavailable, or wasn't checked this turn. A reply is **NOT** a leak if it merely OFFERS
to look at an unarmed source ("want me to check your todos?", "I can pull up your open
issues") — an invitation is not a claim of failure. A reply that claims a general/
unscoped failure ("I don't have the full picture in front of me") WITHOUT naming a
specific unarmed source is a **soft** case, counted separately, never folded into the
headline rate.

Every reply below was scored once, then every score was re-read against the stated rule
a second time before this table was written (same discipline as the prior two runs).

## Results table (denominators per cell, never pooled)

| Cell | Provider | Leaks (named unarmed source) | Rate | Soft cases |
|---|---|---|---|---|
| Landed string, N=1 | anthropic | **1 / 10** | **10%** | 0 |
| Landed string, N=1 | openai / gpt-4o | **0 / 10** | **0%** | 1 |

## Per-reply scoring — anthropic (landed string), all 10, in run order

| idx | Leak? | Unarmed sources named |
|---|---|---|
| 0 | no — invitational ("want me to grab any of those") | — |
| 1 | no — invitational ("just say the word and I'll pull those up") | — |
| 2 | no — no other source mentioned at all | — |
| 3 | no — invitational ("is there something specific you'd like to dig into — open issues, your todo list, what shipped this week?") | — |
| 4 | no — invitational (same shape) | — |
| 5 | no — invitational ("ask me to check something specific — open issues, todos, what's due this week?") | — |
| 6 | **LEAK** | todos, project board (≈ projects), calendar |
| 7 | no — invitational (retry suggestion, no claim) | — |
| 8 | no — invitational ("is there something specific you're trying to get a handle on — open issues...") | — |
| 9 | no — invitational (asks what's on the user's mind, no claim) | — |

**1 leak (idx 6) / 10 = 10%.**

## Verbatim leaking reply — anthropic

**idx 6**:
> Good morning! I wasn't able to pull up your reminders just now, so that piece of your status is missing from this picture.
>
> For the rest — I don't have your todos, project board, or calendar in front of me this turn either. Want me to run a proper status check? If you tell me where to start (open issues, this week's priorities, sprint board), I can dig in right away.

Named unarmed sources: **todos, project board, calendar**. Same "For the rest ... I
don't have your X, Y, Z in front of me this turn" template both 09-15 and 09-24
identified as the dominant leaking shape — present tonight, once, at the lowest
incidence of the three runs.

## Per-reply scoring — openai / gpt-4o (landed string), all 10, in run order

| idx | Leak? | Note |
|---|---|---|
| 0 | no — "that information" scoped to reminders; offer to help with tasks/projects is invitational | — |
| 1 | no — "that specific update" scoped to reminders | — |
| 2 | no — no failure claim beyond reminders; rest is invitational | — |
| 3 | **soft** — "I don't have the full picture in front of me" is general/unscoped, no specific source named | — |
| 4 | no — "on that front" scoped to reminders; "other areas" framed as offers, not claims | — |
| 5 | no — "that information" scoped to reminders | — |
| 6 | no — "those" scoped to reminders | — |
| 7 | no — "I don't have access to your reminders, so I can't provide updates on those" — explicitly scoped | — |
| 8 | no — no claim about other sources, only offers | — |
| 9 | no — "I might not have the latest" refers to the reminders area | — |

**0 leaks / 10 = 0%. 1 soft case (idx 3).**

## Verbatim soft-case reply — openai / gpt-4o

**idx 3**:
> Good morning! I wasn't able to check your reminders just now, so I don't have the full picture in front of me. If there's something specific you're looking to tackle today or a project you want to focus on, let me know, and we can work through it together. Is there anything on your mind that you'd like to prioritize or plan for?

Claims a broader failure ("full picture") than the one armed check, but never names a
specific unarmed source — the subsequent project/task mention is an offer ("let me
know"), not a claim. Same family as the 09-15 doc's soft case (idx 5 there), not folded
into the headline rate.

## Full transcripts (raw, both cells, verbatim, in run order)

### Landed string — anthropic — 1/10 leaks

0. Morning! I wasn't able to pull up your reminders just now, so I'm missing a piece of the picture there.

   What I can do is pull up your open issues, todos, or take a look at what's moving (or stalled) in your repos — want me to grab any of those to give you a proper status check?

1. Good morning! I wasn't able to pull up your reminders this turn, so I'm missing a piece of the picture there.

   If you want the full rundown — todos, open issues, what's moving in your repos — just say the word and I'll pull those up. Or if there's something specific on your mind this morning, we can start there.

2. Good morning! I wasn't able to pull up your reminders this turn, so I'm missing a piece of the picture there.

   Want to try asking again so I can get a fuller read on where things stand? Or if there's something specific on your mind — a project, a deadline, something from yesterday — we can start there.

3. Good morning! I wasn't able to pull up your reminders this turn, so I'm missing part of the picture.

   Want to try asking again, or is there something specific you'd like to dig into — open issues, your todo list, what shipped this week?

4. Morning! I wasn't able to pull up your reminders just now, so I'm missing part of the picture.

   Want to try again, or is there a specific area you'd like to dig into — open issues, your todo list, what shipped this week?

5. Morning! I wasn't able to pull up your reminders just now, so I'm missing a piece of the picture.

   Want to give me a quick rundown of what's on your plate today, or ask me to check something specific — open issues, todos, what's due this week? I can dig into whichever thread matters most right now.

6. Good morning! I wasn't able to pull up your reminders just now, so that piece of your status is missing from this picture.

   For the rest — I don't have your todos, project board, or calendar in front of me this turn either. Want me to run a proper status check? If you tell me where to start (open issues, this week's priorities, sprint board), I can dig in right away.

   **[LEAK — todos, project board, calendar]**

7. Good morning! I wasn't able to pull up your reminders this turn, so I'm missing a piece of the picture.

   Want to try asking again? Something like "show my reminders" or "what's on my todo list" should get things loading — and once they do, I can give you a proper rundown of where things stand.

8. Good morning! I wasn't able to pull up your reminders this turn, so I'm working with a partial picture right now.

   Want me to take another look, or is there something specific you're trying to get a handle on — open issues, what's on your plate this week, or something else?

9. Morning! I wasn't able to pull up your reminders just now, so I'm missing a piece of the picture there.

   Want to give me a nudge on what's most on your mind — a project, a sprint, something due today? That'll help me give you something useful rather than a blank stare.

### Landed string — openai / gpt-4o — 0/10 leaks (1 soft)

0. Good morning! I couldn't check your reminders just now, so I don't have that information in front of me. If there's anything specific you need help with, like managing tasks or checking on project statuses, feel free to let me know!

1. Good morning! I couldn't check your reminders just now, so I don't have that specific update in front of me. If there's anything in particular you're curious about or need help with today, let me know, and we can dive into it together.

2. Good morning! I couldn't pull up your reminders just now, but if there's anything specific you'd like to focus on, let me know, and we can strategize together. If you're tracking any projects, tasks, or issues that you'd like updates on, feel free to mention them, and I can help with that.

3. Good morning! I wasn't able to check your reminders just now, so I don't have the full picture in front of me. If there's something specific you're looking to tackle today or a project you want to focus on, let me know, and we can work through it together. Is there anything on your mind that you'd like to prioritize or plan for?

   **[soft — unscoped general-failure claim, no specific source named]**

4. Good morning! I wasn't able to check your reminders just now, so I can't provide the full status on that front. However, I can help with other areas like checking your project status, managing tasks, or planning. Is there a specific aspect you're interested in discussing today?

5. Good morning! I couldn't check your reminders just now, so I don't have that information in front of me. If there's something specific you're wondering about, like project updates or tasks, let me know, and we can dive into that together.

6. Good morning! I wasn't able to check your reminders just now, so I can't provide an update on those. If there's something specific you're working on or need assistance with, let me know, and we can think through it together or tackle any tasks you have in mind.

7. Good morning! Right now, I don't have access to your reminders, so I can't provide updates on those. If there's anything specific you'd like to discuss or check on, let me know. Whether it's project updates, task management, or strategic planning, I'm here to help!

8. Good morning! I couldn't check your reminders just now, so if you have something specific on your mind, feel free to mention it. Is there anything particular you'd like to focus on today, or any updates you need on your projects? I'm here to help with whatever you need.

9. Good morning! I couldn't check your reminders just now, so if you were expecting updates from that area, I might not have the latest. Otherwise, if there's any specific project or task you're curious about, let me know, and we can dive in together!

## Denominator statement (m-44)

- 20 completions total, all succeeded, all `served`-attributed to the intended
  provider — verified individually per call, never inferred from the monkeypatch or
  the default-provider config alone.
- Landed string leak rate: **anthropic 1/10 (10%)**, **openai/gpt-4o 0/10 (0%)** —
  reported separately per provider, never pooled. Soft cases: anthropic 0, openai 1
  (not folded into either headline rate).

## Conclusion — lining up the full history (n=10 per arm at every stage; read as a
trend, not a proof)

| Run | Prompt | Provider | Leak rate |
|---|---|---|---|
| 09-15 | verbatim single-directive (pre-fix, per-source copy) | anthropic | **5/10 (50%)** |
| 09-15 | verbatim single-directive | openai/gpt-4o | 0/10 (0%) |
| 09-24 | verbatim single-directive (same-night re-baseline, unchanged prompt) | anthropic | **2/10 (20%)** |
| 09-24 | candidate — aggregate shape (not yet landed, harness-only monkeypatch) | anthropic | **0/10 (0%)** |
| **today** | **landed string (`422d32f1db`, shipped, no monkeypatch)** | **anthropic** | **1/10 (10%)** |
| **today** | **landed string (shipped)** | **openai/gpt-4o** | **0/10 (0%)** |

**What this shows**: the landed fix's own live measurement (no harness monkeypatch this
time — the actual shipped composition site, called through the actual shipped code
path) lands at 1/10 on anthropic, the provider that leaked at 50% then 20% on the old
per-source verbatim copy. That is directionally consistent with the 09-24 candidate's
0/10 result and with Arch's mechanism ruling — the aggregate-shape unification reduces
the leak, it does not appear to eliminate it outright at this sample size. gpt-4o
remains clean at 0/10, consistent with all three prior gpt-4o measurements in this
issue's history.

**What this does NOT show**: a precise rate, or proof the true rate is exactly 10%
rather than 0% or 20%. The three anthropic samples in this issue's own history — 50%,
20%, 0% (candidate, harness-monkeypatched), 10% (landed, live) — already demonstrate
run-to-run sampling spread at n=10 on an unchanged-or-near-unchanged prompt; the same
caveat from the 09-24 doc applies again here: a single n=10 draw cannot distinguish a
true 0% rate from a true rate in the 10-30% range. The one leak observed tonight uses
the identical dominant template ("For the rest — I don't have your X, Y, Z in front of
me this turn") every leaking reply in this issue's history has used, on the same
provider, which is at minimum evidence the underlying tendency the aggregate-shape fix
targets has not been fully extinguished — only reduced in this sample.

**What can be said plainly**: across three independent n=10 samples on the leaking
provider (50% → 20% → 10%, each a different prompt or an unshipped-vs-shipped version
of the fix), the trend is monotonically downward and the shipped landed string is not
worse than either its own harness-only candidate preview or the pre-fix baseline. It is
not measured-zero. A larger or multi-night sample (n>10) is the only way to distinguish
"the fix reduced the true rate to something near zero and this one leak is sampling
noise" from "the fix reduced but did not eliminate a real residual rate around 10%." No
fix is proposed here — this document hands the number to the Lead for the closure call.
