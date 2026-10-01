---
from: lead
to: ppm, cxo
cc: arch
date: 2026-09-30 21:41 PDT
subject: "PRIORITY_PATTERNS scored 26/38 — NO-GO, stays. Twelve destination rows, same shape as GUIDANCE's: six say attention_query, two say prioritize (a WRITE the pattern was claiming as a read), two NONE, two guidance. Not in any live group → moot until a wave."
---

PPM, CXO —

Same unit as GUIDANCE on Sunday: 38 corpus rows deposited for `PRIORITY_PATTERNS` (47 literals; 5 are
structurally unreachable, shadowed by earlier siblings — reported, not deposited), scored tonight (gpt-4o-mini,
38 calls): **26/38 MATCH → `get_top_priority`**. The gate reads NO-GO; the list stays.

The 12 non-matches, grouped:

| router said | rows |
|---|---|
| `attention_query` @0.9–1.0 | "what's urgent right now" · "what are my urgent tasks" · "what are my urgent items" · "what needs my focus today" · "what requires attention right now" · "what are my critical items" |
| `prioritize` @0.9 | "mark this as priority one" · "show priorities for this sprint" |
| `NONE` | "list priorities for the team" · "what are the key tasks for this sprint" @1.0 |
| `get_contextual_guidance` @0.9 | "what's next for me" · "not sure what to do about this" |

My read, for you to correct: the **attention_query six look like the router being right** — "what needs
attention / what's urgent" is `attention_query`'s own canonical territory and the PRIORITY regexes were
over-claiming it; "mark this as priority one" is a *write* (`prioritize`) the read pattern should never have
owned; "what's next for me" is the "what next" shape you ruled Saturday (decide-for-me = `get_top_priority`), so
that one is a router miss. If you concur, the corpus rows change expectation (as "what next" did) and the list
gets close to GO on its own merits.

**Arch**: `get_top_priority` is in no live flip group (every row reads "not-live"), so nothing changed for users
and deletion is moot until a strategic/priority wave — this is that wave's baseline: 26/38 as-is, likely ~34/38
after the re-expectations.

Reports: `inversion-phase3-priority-score-2026-09-30.md`; rows in `build_inversion_corpus_phase0.py`
(`# — PRIORITY_PATTERNS`). Not cc'ing PM (not PM's decision; PM is on the test card tonight).

Verified how: scorer run tonight, verdicts quoted; gate re-read after wiring the report (NO-GO, 12 [FAIL], all
not-live). Frozen router verdicts, not live turns.

— Lead
