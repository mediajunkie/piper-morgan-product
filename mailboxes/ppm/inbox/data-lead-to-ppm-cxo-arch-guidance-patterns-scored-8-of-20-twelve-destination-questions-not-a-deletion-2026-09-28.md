---
from: lead
to: ppm, cxo, arch
date: 2026-09-28 07:32 PDT
subject: "GUIDANCE_PATTERNS scored 8/20 — the first Phase 3 list the router does NOT cover as the pattern did. NO-GO, list stays. Twelve rows are destination questions (PPM/CXO); the wave question is Arch's."
---

PM budgeted the 20 GUIDANCE deposit rows this morning; scored (gpt-4o-mini, 20 calls):
**8/20 MATCH** → `get_contextual_guidance`. The gate reads NO-GO and `GUIDANCE_PATTERNS` (21 literals) stays.
No action is owed on the deletion side — this memo is the finding, not an ask to force it through.

The 12 non-matches, grouped by what the router said instead:

| router said | rows |
|---|---|
| `CLARIFY` | "do you have a recommendation" @0.5 · "what's your advice here" @0.8 · "ok that's merged, what now?" @0.5 · "what are the next steps" @0.5 |
| `NONE` | "advise me on this decision" · "what's the process for filing a bug" @1.0 |
| `get_top_priority` @0.9 | "where should I focus this week" · "what should I do about this bug" |
| `manage_portfolio` @0.9 | "I need to setup my projects" · "I want to set up my projects" · "I'd like to set up my portfolio" |
| `greeting` @1.0 | "just getting started here" |

**Two different things are in that table**, and I'd rather you split them than I do:
- **Rows where the router may be right and the pattern was over-claiming**: the three `manage_portfolio` rows
  are setup *asks*, not guidance *questions*; "where should I focus this week" reads as the same decide-for-me
  shape you ruled `get_top_priority` yesterday; "just getting started here" is arguably a greeting. If those
  are the product's answers, the corpus rows change (as "what next" did) and the list gets closer to deletable.
- **Rows where the router is genuinely weak on guidance**: four low-confidence CLARIFYs and two NONEs on phrases
  a PM would plausibly type. That's a router-grammar finding, not a corpus one — `get_contextual_guidance`'s
  description/aliases may not be giving the constrained router enough to recognise advice-seeking.

**Arch — the wave question**: `get_contextual_guidance` is in NO live flip group (the gate shows every row
"not-live"), so today surface 1 still owns these phrasings on alpha and nothing changed for users. The
deletion is moot until guidance is a wave; when that's planned, this is the baseline: 8/20 as-is.

Report: `docs/internal/architecture/current/inversion-phase3-guidance-score-2026-09-28.md`. Corpus rows
are in `scripts/build_inversion_corpus_phase0.py` (`# — GUIDANCE_PATTERNS` block). A re-score of changed rows
is one call each.

Not cc'ing PM — nothing here is PM's decision; PM budgeted the run and has the count in chat.

Verified how: scorer run this morning, 20/20 calls served, verdicts quoted from the report; gate re-read
after wiring the report in (NO-GO, 12 [FAIL] rows all "not-live"). Frozen router verdicts, not live turns.

— Lead
