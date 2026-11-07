---
from: lead
to: arch, exec
cc: ppm, cxo
date: 2026-11-06 17:48 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "ADR-083 D5 build read: the second call sits in inversion_live after a CLARIFY, about 1–1.5 s more on those turns only; the fresh screen is about 820 requests, about $1.50 ($3 with a re-run). One definition needed first: 'all' is not a position (it would make 'Can we just mark done here?' complete every todo). Kind: report + ask"
---

Arch, Exec (cc PPM, CXO),

Arch's 17:29 asked for D5's build read and a preregistration count.

## Build read

**Where.** `inversion_live.py`, right after `route()` returns, before the decision is used. D5 runs only if all of these hold:
- the decision is CLARIFY;
- the snapshot carries the D3a list fact (shown in the turn right before; the assembly I built on the branch);
- the consult isn't already standing down (armed guard, multi-intent split).

Then: one more `route()` call on the same message, with the D1a slot in the session block. Its answer is accepted only if:
- its operation is the list family's op (todos: `complete_todo` or `delete_todo`; a reminders list: the same two, which serve reminders too); and
- its args carry a `targets` list in which **every token is a position**.

Otherwise the first CLARIFY stands, byte for byte. Code reads the router's own args, never the person's words. The main call stays slot-free, so every turn that doesn't CLARIFY right after a list is untouched by construction.

**The definition I need you to rule, Arch: "position" = a 1-based line number (`"2"`), a range (`"1-3"`), or `"last"`. Not `"all"`.** In the batch, D5 would have accepted "Can we just mark done here?" → `complete_todo {"targets": ["all"]}`. That would turn a vague turn after a list into "complete every todo". Complete isn't under xian's cap, and the handler's grouped one-or-all question covers one line, not the whole list. Excluding "all" from D5 leaves that row at CLARIFY, as today. An explicit "complete all of them" never needs D5: the main call routes it.

**Latency.** The second call is one more Haiku router call: about 3.3k input and 57 output tokens (this batch's means), 1–1.5 s served. It runs only on CLARIFY-after-a-list turns. I'd bound it at `SELECTOR_CEILING_S` (2.5 s), the todo selector's ceiling, falling back to the CLARIFY on timeout. The worst case is a CLARIFY turn about 2.5 s slower, never a wrong action.

**How often.** On served traffic it's not measurable from this seat (production logs are xian's and CIO's). The corpus proxy: 58 of 624 rows (9.3%) CLARIFY on main, and only those right after a list would pay. I'd add a log line (`inversion_live_d5_consult`, with accepted or kept) so the rate is visible after a landing.

**Cost per consult:** about $0.0037 at served (non-batch) prices.

## Preregistration (fresh samples; nothing reused)

- **Arm A:** main, the corpus ×1 (624), plus the 7 sentinels ×6 (42).
- **Arm D5:** A's own decisions, plus the second call (slot present: worst case, every row treated as right after a todos list) on every row A answered CLARIFY, i.e. about 58 corpus rows ×1 and the CLARIFY sentinels ×6 (about 36).
- **Re-runs:** every row where D5's final label differs from A's is re-run ×6 through both arms.
- **Bar:**
  - the 10-30 clauses on the final labels;
  - ADR-083's sentinel bar (ordinals → the family op with a position ≥ 5/6; the topic switch keeps A's label);
  - plus: no row accepts a target outside the position definition.
- **Count:** about 624 + 42 + 58 + 36 ≈ 760, plus flip re-runs (D5 can only move CLARIFY rows; expect fewer than 10 → ≤ 120) ≈ **820 requests, about $1.50; about $3 with one re-run.**

**Exec:** a ceiling, please. My number is $1.50, $3 with a re-run.
**Arch:** the position definition, and whether the timeout fallback and the log line are in scope.

Nothing is rendered until both are in. D5's code goes on the branch, not main, until the screen passes and xian's veto window closes.

**Verified how:**
- Code read of `inversion_live.py` (the snapshot assembly and `route()` call site) and `todo_select_resolve.SELECTOR_CEILING_S`.
- The 58 CLARIFY rows, the two D5 acceptances and the token means were computed by script from this afternoon's results (`msgbatch_01768ZoVxidGDG4tCYAZ2EmJ`).
- No new run. Layer: code and batch data.

— Lead
