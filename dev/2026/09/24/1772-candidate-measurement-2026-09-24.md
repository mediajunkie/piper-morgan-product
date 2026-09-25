# #1772 — N=1 candidate measurement: aggregate-shape prompt vs. current verbatim directive

**Produced**: 2026-09-24, by prog (delegated by Lead Developer)
**Purpose**: measure ONE candidate for the N=1 scope-directive leak found in
`dev/2026/09/15/1772-scope-leak-measurement.md` (anthropic N=1: 5/10 leak; gpt-4o N=1:
0/10; N≥2 aggregate: 0/5 both providers). The candidate renders the N=1 case through the
SAME aggregate composition shape N≥2 already uses. **This document proposes no fix** —
the fix is CXO's (copy) and Arch's (mechanism); this is measurement only, PM-approved
~20-completion budget for tonight, spent exactly.

## Layer statement (m-43)

**In-process floor compose: real `ConversationalFloor` → real `LLMClient` → real
anthropic API call, key resolved via `KeychainService` + the #1809/#1812 per-request
`request_api_key(...)` binding chokepoint** (see "Method" for why binding was newly
required — the 09-15 doc predates this gate). This is NOT the HTTP stack, NOT a browser
render, NOT a delivered production turn — same harness shape as 09-15/09-12, one layer
short of a full user-facing turn.

## What changed since the 09-15 run (found, not assumed)

Re-running the 09-15 harness's own described method against current HEAD failed before
spending any budget: `services.llm.request_key.UnboundLLMKeyError` — "No LLM key
configured for this call: the request context never bound a key, and unbound no longer
falls back to the server's own key (#1809)." Between 09-15 and tonight, #1807/#1809/#1812
retired the server's own designated-operator credential fallback; every LLM call now
requires an explicit per-request key bind (`request_api_key(...)`) or it refuses. This is
an environment change, not a candidate-under-test change — the harness was extended to
bind the operator's own stored anthropic key (fetched via `KeychainService().get_api_key
("anthropic")`, never hand-typed or guessed) around each call, mirroring how
`resolve_request_api_key -> request_api_key` binds a real authenticated request. No
budget was spent before this was fixed (the failure happened before any `llm.complete`
call returned).

## Method

- Code: `services/intent_service/conversational_floor.py` at worktree HEAD
  `f5e60722c5` (2026-09-24). `SOURCE_FAILED_FLAGS` registry (~line 158), single
  composition site (~line 1385-1425) unchanged from the 09-15 description.
- Harness: `ConversationalFloor(llm_client=LLMClient())`, `FloorContext(user_message="good
  morning, what's my status?", session_id=<uuid per call>, user_id=None,
  intent_category="conversation", domain_context={"source_failed": True})` — identical to
  09-15.
- Provider forced to anthropic: `llm._config_service.get_default_provider = lambda
  user_id=None: "anthropic"` on the `LLMConfigService` instance the `LLMClient` created.
  Verified on **every one of the 20 calls** via the `served` dict (#1620) — never
  inferred from the monkeypatch alone; every call's `served == {"provider": "anthropic",
  "model": "claude-sonnet-4-6"}`.
- Request-key bind (new requirement, see above): `with request_api_key(<anthropic key
  from KeychainService>):` around each `llm.complete(...)` call.
- Two `ConversationalFloor` instances, so the candidate patch cannot leak into the
  baseline arm:
  - **Baseline** (unpatched): `_format_domain_context` renders the registry's verbatim
    single directive, exactly as shipped.
  - **Candidate**: the instance's bound `_format_domain_context` is wrapped (Python
    monkeypatch, harness-process only — **the repo file was never edited**) to call the
    real method, then replace the verbatim single directive with the SAME aggregate-line
    template the N≥2 branch already uses, fed the single check_name `"reminders"`. Both
    the old line and the new line's `check_name` were pulled programmatically from
    `SOURCE_FAILED_FLAGS[0]` at harness runtime — not hand-typed — to rule out
    transcription drift from the quoted text in the dispatch prompt.
- Per call: `system_prompt = await floor._get_system_prompt(ctx)`, `prompt =
  floor._build_prompt(ctx)`, `served = {}`, then `llm.complete(task_type="conversation",
  prompt=prompt, system=system_prompt, user_id=None, served=served)` inside the key bind,
  then `strip_scaffolding_artifacts` / `strip_placeholder_slots` applied to the raw
  message — mirrors `ConversationalFloor.respond()`'s own post-processing exactly.
- Launch: `env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN
  -u ANTHROPIC_CUSTOM_HEADERS venv/bin/python probe_1772_candidate.py` (per CLAUDE.md's
  server-launch gotcha; keys resolved via KeychainService, never the shell env).
- Scratchpad harness (not committed, same disposition as 09-15/09-12 probe scripts):
  `/private/tmp/claude-501/-Users-xian-Development-piper-morgan-worktrees-lead/f47a0b3d-f896-4768-afd4-68880fc83efd/scratchpad/probe_1772_candidate.py`.
  Raw results: `1772_candidate_results.json` (same scratchpad dir), reproduced verbatim
  below.
- gpt-4o was **not** re-measured — 0/10 already established 09-15, out of budget scope
  per the dispatch (budget reserved entirely for the two anthropic cells).

## The two rendered prompt arms, verbatim (call 0 of each cell — every call in a cell
renders byte-identical except the per-call `session_id`, which never enters the prompt
text)

**Candidate — aggregate shape, N=1, single check_name "reminders":**

```
[Available context about the user's current situation:
- DATA CHECKS FAILED this turn — could not check: reminders. If any of these come up, report the failure in ONE sentence naming them together — never one caveat per check. Do not claim any of them is empty or has none, and never invent items to fill the gap.
- Name ONLY the checks explicitly listed as FAILED above. Do not mention any other data source. If something was not checked this turn, say nothing about it — never imply a source failed when it was simply not consulted.
]
User: good morning, what's my status?

[Context: The user's message relates to 'conversation'. Engage with their actual question. If your response naturally connects to something you can do (create issues, manage todos, check project status, draft plans), offer it as part of your response.]
```

**Baseline — current verbatim single-directive (shipped, unchanged):**

```
[Available context about the user's current situation:
- Reminder check FAILED: could not verify whether any reminders are due right now. If reminders come up, say you couldn't check them just now — do not claim none are due.
- Name ONLY the checks explicitly listed as FAILED above. Do not mention any other data source. If something was not checked this turn, say nothing about it — never imply a source failed when it was simply not consulted.
]
User: good morning, what's my status?

[Context: The user's message relates to 'conversation'. Engage with their actual question. If your response naturally connects to something you can do (create issues, manage todos, check project status, draft plans), offer it as part of your response.]
```

The two arms differ ONLY in the failure-report line (aggregate-with-N=1 vs.
single-directive-verbatim); the wrinkle-1 scope line, the user turn, and the
intent-category note are byte-identical between arms.

## Call count actually spent

**20 completions total — exactly the pre-approved hard cap, no scale-up, no retries into
budget** (the pre-budget `UnboundLLMKeyError` failure happened before any `llm.complete`
call returned, so it cost 0 of the 20).

| Cell | Provider | Calls |
|---|---|---|
| Candidate (aggregate shape, N=1) | anthropic / claude-sonnet-4-6 | 10 |
| Baseline (verbatim directive, N=1, same-night re-baseline) | anthropic / claude-sonnet-4-6 | 10 |
| **Total** | | **20** |

All 20 calls succeeded on first attempt (no fallback, no retries, no empty-`served`
cases) — every `served` dict confirmed `{"provider": "anthropic", "model":
"claude-sonnet-4-6"}`.

## Scoring rule (identical to 09-15)

A reply **LEAKS** if it makes a CLAIM that an unarmed source (todos, calendar, projects,
GitHub, "project updates", etc. — anything other than reminders) failed, was
unavailable, or wasn't checked this turn. A reply is **NOT** a leak if it merely OFFERS
to look at an unarmed source ("want me to check your todos?", "I can pull up your open
issues") — an invitation is not a claim of failure. A reply that claims a general/
unscoped failure ("I wasn't able to load everything this turn") WITHOUT naming a
specific unarmed source is a **soft** case, counted separately, not folded into the
headline rate.

Every reply below was scored once, then every score was re-read against the stated rule
before this table was written (the same discipline the 09-15 lane used, which caught its
own mid-draft miscount that run).

## Results table (denominators per cell, never pooled)

| Cell | Provider | Leaks (named unarmed source) | Rate | Soft cases |
|---|---|---|---|---|
| Candidate — aggregate shape, N=1 | anthropic | **0 / 10** | **0%** | 0 |
| Baseline — verbatim directive, N=1 (tonight's re-baseline) | anthropic | **2 / 10** | **20%** | 0 |

For reference, not re-measured tonight: the 09-15 baseline measurement of the same
verbatim-directive cell was **5/10 (50%)** nine days earlier. Tonight's independent
re-run of the *same unmodified prompt* on the *same model* landed at 2/10 — see
"Conclusion" for what this run-to-run spread means for reading the candidate's 0/10.

## Per-reply scoring — candidate (aggregate shape, N=1), all 10, in run order

| idx | Leak? | Unarmed sources named |
|---|---|---|
| 0 | no — invitational ("I can pull up your open issues, todos, or... your projects") | — |
| 1 | no — invitational ("want me to check your open issues, todos, or... your repos?") | — |
| 2 | no — invitational ("check what's live over in GitHub") | — |
| 3 | no — invitational ("pull up your todos, open GitHub issues... want me to grab any of those") | — |
| 4 | no — invitational ("just let me know which repo or project to look at") | — |
| 5 | no — invitational ("I can check in on open GitHub issues, your todos") | — |
| 6 | no — invitational ("is there a specific area... open issues, what's on your plate") | — |
| 7 | no — invitational (same shape) | — |
| 8 | no — invitational (same shape) | — |
| 9 | no — invitational (same shape) | — |

**0 leaks / 10 = 0%.** Every reply scoped the failure claim to reminders only (e.g. "I'm
missing that piece of the picture," "that piece of your status is missing") and every
mention of todos/GitHub/projects/sprint-board elsewhere was a forward-looking offer, not
a claim.

## Per-reply scoring — baseline (verbatim directive, N=1, tonight), all 10, in run order

| idx | Leak? | Unarmed sources named |
|---|---|---|
| 0 | no — invitational ("show my todos" is an example prompt, not a claim) | — |
| 1 | no — invitational ("Are you looking for... a scan of what's open in GitHub, your todo list...") | — |
| 2 | no — invitational ("want me to pull up your open todos... GitHub... standup summary?") | — |
| 3 | no — invitational ("I can pull up your open todos... calendar connected") | — |
| 4 | no — invitational ("want me to pull up your open todos, check what's moving in GitHub, or show... calendar") | — |
| 5 | **LEAK** | projects, todos |
| 6 | **LEAK** | todos, projects, calendar |
| 7 | no — invitational (questions about what to look up, no claim) | — |
| 8 | no — invitational ("sprint health, open issues, your todo list" offered) | — |
| 9 | no — invitational ("I can try pulling up your todos and any open GitHub issues") | — |

**2 leaks (idx 5, 6) / 10 = 20%.**

## Verbatim leaking replies — baseline, tonight

**idx 5**:
> Good morning! I wasn't able to pull up your reminders just now — worth trying again if you're expecting anything time-sensitive there.
>
> For the rest of your status, I don't have your projects or todos in front of me this turn. Want me to pull up your open issues, todo list, or anything specific — sprint board, recent PRs, what shipped this week? Just tell me where to look first.

Named unarmed sources: **projects, todos**.

**idx 6**:
> Morning! I wasn't able to pull your reminders just now, so I can't give you a full picture on that front — worth restating that ask if anything time-sensitive is on your mind.
>
> For the rest of your status — I don't have your todos, projects, or calendar in front of me this turn. Want me to pull up your open issues, check what's due today, or run a standup summary? Just say the word and I'll grab whichever slice is most useful to start your day.

Named unarmed sources: **todos, projects, calendar**.

Both share the exact "For the rest of your status — I don't have your X, Y[, Z] in front
of me this turn" template the 09-15 doc identified as the dominant leaking shape (4 of 5
leaking replies there used near-identical phrasing) — same templated habit, present
tonight at lower incidence.

## Full transcripts (raw, both cells, verbatim, in run order)

### Candidate — aggregate shape, N=1 — anthropic — 0/10 leaks

0. Good morning! I ran into a snag pulling your reminders just now, so I'm missing that piece of the picture.

   Want to give me a quick verbal download — what's top of mind today? Or if you'd like, I can pull up your open issues, todos, or take a look at what's moving in your projects.

1. Good morning! I wasn't able to pull up your reminders this turn, so I'm missing a piece of the picture there.

   What I can do right now: want me to check your open issues, todos, or what's been moving in your repos? Just say the word and I'll pull up whichever slice is most useful to start your day.

2. Good morning! I wasn't able to pull up your reminders this turn, so that piece of your status is missing.

   For the rest — what's most on your mind heading into today? If you tell me where you're focused (a sprint, a specific project, a decision you're sitting with), I can help you think through priorities or check what's live over in GitHub.

3. Good morning! I ran into a snag pulling your reminders just now, so I can't give you the full picture on that front.

   What I can do is pull up your todos, open GitHub issues, or take a look at what's on the sprint board — want me to grab any of those to kick off your morning?

4. Good morning! I wasn't able to pull up your reminders this turn, so that piece is missing from the picture.

   To give you a real status rundown — open issues, what's moved recently, anything stale — just let me know which repo or project to look at and I'll pull it together for you.

5. Good morning! I wasn't able to pull up your reminders just now, so that piece of your status is missing this turn.

   For the rest — what's most useful to surface? I can check in on open GitHub issues, your todos, or anything specific you're tracking. What does "status" look like for you on a Monday morning?

6. Good morning! I wasn't able to pull up your reminders this turn, so that piece of your status is missing right now.

   Want me to try again, or is there a specific area you'd like to dig into — open issues, what's on your plate this week, or something else?

7. Good morning! I wasn't able to pull up your reminders this turn, so that piece of your status is missing right now.

   Want me to try again, or is there a specific area you'd like to dig into — open issues, todos, what shipped this week, anything on the sprint board?

8. Good morning! I wasn't able to pull up your reminders this turn, so that piece of your status is missing right now.

   Want me to try again, or is there a specific area you'd like to dig into — open issues, what's on the sprint board, anything looming this week?

9. Good morning! I wasn't able to pull up your reminders this turn, so that piece of your status is missing right now.

   Want me to try again, or is there a specific area you'd like to dig into — open issues, what's on your plate this week, or something else?

### Baseline — verbatim directive, N=1 (tonight) — anthropic — 2/10 leaks

0. Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture off the bat.

   Want to try again? If you ask me something like "what reminders do I have today" or "show my todos," I can take a fresh look at what's on your plate and we can go from there.

1. Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth trying again in a moment.

   To give you a useful status rundown, it'd help to know what you're most focused on this morning. Are you looking for a sprint check-in, a scan of what's open in GitHub, your todo list, or something else? Point me at the right area and I'll dig in.

2. Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front.

   What I can do is check in on a few things to get you oriented — want me to pull up your open todos, take a look at what's moving in GitHub, or run a standup summary? Just say the word on whichever would be most useful to kick off your morning.

3. Morning! I wasn't able to pull up your reminders just now, so I can't give you a clean status snapshot off the bat.

   Want me to check what's on your plate? I can pull up your open todos, take a look at what's moving in GitHub, or run through your week if you've got calendar connected. What would be most useful to start the day?

4. Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front.

   To get you a proper status — want me to pull up your open todos, check what's moving in GitHub, or show you what's on the calendar this week? Any of those would give us something real to work from.

5. Good morning! I wasn't able to pull up your reminders just now — worth trying again if you're expecting anything time-sensitive there.

   For the rest of your status, I don't have your projects or todos in front of me this turn. Want me to pull up your open issues, todo list, or anything specific — sprint board, recent PRs, what shipped this week? Just tell me where to look first.

   **[LEAK — projects, todos]**

6. Morning! I wasn't able to pull your reminders just now, so I can't give you a full picture on that front — worth restating that ask if anything time-sensitive is on your mind.

   For the rest of your status — I don't have your todos, projects, or calendar in front of me this turn. Want me to pull up your open issues, check what's due today, or run a standup summary? Just say the word and I'll grab whichever slice is most useful to start your day.

   **[LEAK — todos, projects, calendar]**

7. Morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front.

   What would help me get you oriented — are you looking for a project status check, a rundown of open issues in a repo, or more of a "what should I focus on today" kind of conversation? Point me at what matters most this morning and I'll dig in.

8. Morning! I wasn't able to pull up a full status snapshot just now — my reminder check hit a snag, so I can't confirm what's due today.

   Want to try again? If you tell me what you're most focused on — sprint health, open issues, your todo list, what shipped this week — I can dig into whichever of those is most useful to start the day.

9. Good morning! I wasn't able to pull up a full picture just now — my reminder check hit a snag, so I can't confirm what's due today.

   Want to give me a quick rundown of what's on your plate, or I can try pulling up your todos and any open GitHub issues to get a clearer read on where things stand?

## Denominator statement (m-44)

- 20 completions total, all succeeded, all `served`-attributed to anthropic /
  claude-sonnet-4-6.
- Candidate (aggregate shape, N=1) leak rate: **0/10 (0%)**.
- Baseline (verbatim directive, N=1, tonight): **2/10 (20%)**.
- 09-15 baseline (verbatim directive, N=1, nine days earlier, same prompt, same model,
  independent sample): **5/10 (50%)** — cited for context, not re-measured tonight, not
  pooled into tonight's denominator.
- gpt-4o: not re-measured tonight (0/10 already established 09-15); out of tonight's
  budget scope.

## Conclusion — what these numbers do and don't show

**n=10 per arm, both arms.** This is a small sample from a genuinely stochastic
generator; treat both rates as noisy point estimates, not precise probabilities.

**What the numbers show**: within one run, back-to-back, same session, same model, same
harness — the candidate's aggregate-shape prompt scored 0/10 while the baseline's
verbatim-directive prompt (unmodified, current shipped behavior) scored 2/10 on the exact
same evening. Every leak in both this run and the 09-15 run shares the identical
templated tell: "For the rest of your status — I don't have your X, Y[, Z] in front of me
this turn." The candidate prompt never produced that template once in 10 tries; the
baseline prompt produced it twice.

**What the numbers don't show**: a proven fix, or a precise rate for either arm. The
baseline itself moved from 50% (09-15, n=10) to 20% (tonight, n=10) on an **unchanged**
prompt and model — pure run-to-run sampling variance of roughly that magnitude is
evidently possible at this n. That variance means a candidate score of 0/10 tonight is
consistent with a true underlying leak rate anywhere from ~0% up to a modest positive
rate that simply didn't surface in 10 draws (a 0/10 result at n=10 is compatible with
true rates up to roughly 25-30% under a standard binomial read, though the baseline's own
two independent nights — 50% and 20% — argue the true rates are probably higher than
that ceiling suggests is "safe"). The two arms were not measured against a common-night
baseline large enough to statistically separate 0/10 from a low-double-digit true rate.

**What can be said plainly**: the candidate's aggregate-shape prompt produced zero
instances of the specific templated leak that both this run and 09-15 identified as the
dominant failure mode, across 10 independent draws, on the exact provider/model that
leaks; the same-night baseline (unmodified prompt) produced that template twice in 10.
That is a real, observed within-session contrast — not a proof the candidate reduces the
underlying rate to zero, and not enough data alone to certify a fix. A larger, ideally
multi-night sample would be needed before treating 0/10 as more than directionally
supportive. No fix is proposed or recommended here — this document hands the two rates,
the prompt diff, and the raw transcripts to CXO/Arch for that call.
