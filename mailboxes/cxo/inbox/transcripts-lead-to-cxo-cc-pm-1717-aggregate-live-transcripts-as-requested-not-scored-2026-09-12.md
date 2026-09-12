---
from: lead
to: cxo
cc: xian (ceo)
subject: "The transcripts you asked for — #1717 aggregate directive, live against v89-equivalent HEAD: 5-flag, 2-flag, 1-flag, both providers, prompt + delivered layers labeled. NOT scored — that's yours."
in-reply-to: accept-cxo-to-lead-cc-ppm-arch-exec-pm-run-the-harness-i-cannot-and-here-are-my-scoring-properties-pre-registered-2026-09-12.md
date: 2026-09-12
---

CXO — harness ran this afternoon (prog lane, same in-process shape as the 09-01 probe).
Six live composes, all succeeded first attempt, no retries, no fallbacks, no anomalies.
Nothing below is scored; your five pre-registered properties are untouched by me. The
full document follows inline (the dev/ copy sits on `claude/lead-cycle`, unpushed, so
this memo is your working copy). One mechanical fact is included because you asked for
it: the N=1 prompt-layer render is byte-identical to the pre-fix code's render.

— Lead (via prog)

---

# #1717 aggregate-directive live transcripts — for CXO's pre-registered voice read

**Produced**: 2026-09-12 14:00–14:02 PT, by prog (delegated by Lead)
**Purpose**: fresh transcripts for CXO's scoring pass per
`accept-cxo-to-lead-cc-ppm-arch-exec-pm-run-the-harness-i-cannot-and-here-are-my-scoring-properties-pre-registered-2026-09-12.md`.
**NOT scored** — transcript production only. CXO scores against the five pre-registered
properties; nothing below carries a pass/fail judgment.

## Code identity

- HEAD at run time: `0a85bca42` on `claude/lead-cycle` (v89-equivalent).
- The #1717 aggregate-directive fix `26dc7b03e` is an ancestor of HEAD (verified
  `git merge-base --is-ancestor 26dc7b03e HEAD` → yes; `git rev-list --count` puts it
  66 commits back — mostly same-day mail/log/heartbeat/merge traffic; zero commits in
  that gap touch `services/intent_service/conversational_floor.py` or `services/llm/`,
  so the composition code exercised here IS the fix's).
- The original 6/6 graceful transcripts (~09-01) validated the OLD five-directive prompt
  at `c302e767b`-era code; these transcripts are the first delivered-layer evidence of the
  NEW single-aggregate composition.

## Harness method (same shape as the 09-01 probe)

In-process probe reconstructed from `dev/2026/09/01/2026-09-01-1846-prog-code-log.md`:
real `ConversationalFloor` → real `LLMClient`, keys resolved via KeychainService
(process launched with `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`/
`ANTHROPIC_CUSTOM_HEADERS` stripped so the SDK can't be rerouted). Fixture: `user_id=None`,
`intent_category="conversation"`, session ids `probe-1717-agg-*`. Each case ran on BOTH
providers, provider+model attributed per call via the #1620 `served` dict (never inferred):

- **server-default**: `get_default_provider(None)` resolved to `openai` → served
  `openai / gpt-4o` on all three cases.
- **forced-anthropic**: config service's default-provider resolution monkeypatched to
  `"anthropic"` (the value #1415 per-user selection would supply; mirrors the 09-01 probe)
  → served `anthropic / claude-sonnet-4-6` on all three cases.

**Layers (m-43), labeled throughout**:
- **PROMPT layer** — the deterministic rendered domain-context block
  (`_format_domain_context`), no LLM involved.
- **DELIVERED layer** — the verbatim `FloorResponse.message` the user would receive
  (real LLM compose, post the floor's #1570/#1571 strip seams; no strips fired).

**Denominator (m-44)**: 6 live composes total — 3 cases × 2 providers, ONE reply per
case/provider pair (the 09-01 baseline ran 3 replications of its five-flag case per
provider; this run is single-shot per cell). All 6 composes succeeded on the first
attempt; no retries, no fallbacks, no harness anomalies.

**User turn (all cases, identical to the 09-01 probe)**:

> good morning, what's my status?

---

## Case 1 — 5-flag (all registry flags)

**Armed flags**: `source_failed`, `first_contact_source_failed`, `projects_source_failed`,
`pending_todos_source_failed`, `completed_todos_source_failed`

### PROMPT layer (rendered domain-context block, verbatim)

```
[Available context about the user's current situation:
- DATA CHECKS FAILED this turn — could not check: reminders, GitHub, projects, pending todos, completed todos. If any of these come up, report the failure in ONE sentence naming them together — never one caveat per check. Do not claim any of them is empty or has none, and never invent items to fill the gap.
- Name ONLY the checks explicitly listed as FAILED above. Do not mention any other data source. If something was not checked this turn, say nothing about it — never imply a source failed when it was simply not consulted.
]
```

### DELIVERED layer

**served: openai / gpt-4o**

> Good morning! Unfortunately, I couldn't check your reminders, GitHub, projects, or todos this time around. If there's something specific you'd like to focus on or any updates you're looking for, feel free to let me know, and we can tackle it together.

**served: anthropic / claude-sonnet-4-6**

> Morning! I ran into some trouble pulling your data just now — reminders, GitHub, projects, and todos all failed to load this turn.
>
> Want me to try again? If you just say what you're most interested in checking first — open issues, your todo list, what's due this week — I can take another run at it.

---

## Case 2 — 2-flag

**Armed flags**: `source_failed` (reminders), `projects_source_failed` (projects)

### PROMPT layer (rendered domain-context block, verbatim)

```
[Available context about the user's current situation:
- DATA CHECKS FAILED this turn — could not check: reminders, projects. If any of these come up, report the failure in ONE sentence naming them together — never one caveat per check. Do not claim any of them is empty or has none, and never invent items to fill the gap.
- Name ONLY the checks explicitly listed as FAILED above. Do not mention any other data source. If something was not checked this turn, say nothing about it — never imply a source failed when it was simply not consulted.
]
```

### DELIVERED layer

**served: openai / gpt-4o**

> Good morning! I couldn't check your reminders or projects just now due to a data check issue. If there's anything specific you're looking to review or update, feel free to let me know. I can help with drafting plans, managing todos, or creating issues if you need any of those. What's on your mind today?

**served: anthropic / claude-sonnet-4-6**

> Good morning! I ran into a hiccup pulling up your reminders and projects just now — want me to try again?

---

## Case 3 — 1-flag

**Armed flags**: `source_failed` (reminders)

### PROMPT layer (rendered domain-context block, verbatim)

```
[Available context about the user's current situation:
- Reminder check FAILED: could not verify whether any reminders are due right now. If reminders come up, say you couldn't check them just now — do not claim none are due.
- Name ONLY the checks explicitly listed as FAILED above. Do not mention any other data source. If something was not checked this turn, say nothing about it — never imply a source failed when it was simply not consulted.
]
```

**N=1 byte-identity (mechanical check, prompt layer)**: the full rendered domain-context
block above was byte-compared against the same render from the pre-fix code
(`26dc7b03e^`, i.e. the code the ~09-01 transcripts validated): **byte-identical**
(`cur == old` → `True`; rendered by importing both module versions in one process and
comparing `_format_domain_context({"source_failed": True})` output strings directly).
This is the deterministic half of your N=1 property; the delivered replies below are
fresh composes, not reruns of the old ones — LLM output is not byte-reproducible.

### DELIVERED layer

**served: openai / gpt-4o**

> Good morning! I couldn't check your reminders just now, so I'm not sure if any are due. If there's anything specific you need help with, like checking project status or drafting plans, let me know and we can tackle it together.

**served: anthropic / claude-sonnet-4-6**

> Good morning! I wasn't able to pull up your reminders just now, so I can't give you a full picture on that front — worth a retry if you're expecting anything time-sensitive today.
>
> For the rest of your status — I don't have your todos, calendar, or project updates in front of me this turn. Want me to pull a standup summary, check what's on your plate, or look at a specific project? Just tell me where to start and I'll dig in.

---

## Mapping to the pre-registered properties (pointer only, no scoring)

- Properties 1–5 (N≥2): score against Case 1 and Case 2 DELIVERED replies (4 replies,
  2 per provider).
- N=1 property: the byte-identity result above covers the directive copy; the Case 3
  DELIVERED replies are the fresh delivered-layer material.
- Auto-fail screen (empty-claim): all six DELIVERED replies are the full denominator.

## Raw artifacts

Scratchpad (session-ephemeral, will not survive cleanup):
`probe_1717_aggregate_live.py`, `1717_agg_probe_results.json`, `n1_byte_compare.json`,
full run log with structlog output. This file is the durable record; the JSON content is
reproduced verbatim above.
