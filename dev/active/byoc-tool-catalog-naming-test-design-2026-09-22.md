# BYOC tool-catalog naming test — design

**Author**: PA. **Filed**: 2026-09-22. Phase A deliverable named in
`dev/active/byoc-parallel-work-plan-2026-09-15.md` and `dev/active/byoc-hosted-alpha-readiness-
checklist-2026-09-15.md`. **Status: TWO PASSES RUN 2026-09-22** — Claude only, n=1/cell, both
cost-narrowed from this design. **Pass 1 (13:12)**: situation-shaped 12/12, object-shaped 10/12,
opposite PPM's stated worry, real same-author confound named honestly. **Pass 2 (19:13,
independent-author control)**: object-shaped rose to 11/12 once a fresh, isolated author wrote its
descriptions — confirming one failure was the confound — but situation-shaped stayed 12/12 and one
object-shaped failure (`list_projects`) persisted even under a good independent description.
**Net: a real but small (1-point) residual gap, honestly uncertain whether it's a naming effect or
one hard utterance.** Full results: `dev/active/probes/RESULTS-naming-test-first-pass-2026-09-22.md`,
`dev/active/probes/RESULTS-naming-test-control-2026-09-22.md`.

## The question, sourced directly from PDR-006 (not paraphrased)

PPM, 2026-07-30, reviewing PDR-006: tool names/descriptions are the only entry-point copy a
plugin user's client LLM ever sees, so they should be **situation-shaped** ("shape a vague idea
into a spec") rather than **object-shaped** ("our internal data model"). PPM's own counter-risk,
recorded because it cuts against their recommendation: *"the catalog is read by the host LLM as
much as the human, and situation-shaped names may route WORSE than object-shaped ones if
tool-selection does better with crisp nouns than scenarios. Nobody knows which way this goes. Test
selection accuracy on both namings before committing."*

That's the actual test: **does a client LLM select the right tool more or less accurately when the
catalog is situation-named vs. object-named**, for realistic user utterances.

## What the catalog actually looks like today (verified, not assumed)

Dispatched an Explore agent to inventory the real registry rather than design against an imagined
one. Findings: **~53 distinct dispatchable operations** (`services/intent_service/
workflow_entries.py`, `WORKFLOW_REGISTRY`), **~110+ registered alias keys** (many operations have
several paraphrase aliases already, e.g. `update_issue`/`update_github_issue`/`update_ticket`/
`modify_issue`). **Every single one is object-shaped** — `verb_object` naming derived from the
internal data model: `create_issue`, `close_issue`, `update_document`, `delete_todo`,
`list_projects`, `set_default_repo`. Zero situation-shaped names exist anywhere today. This
confirms PPM's framing exactly — there is no partial-adoption to compare, a genuinely clean
object-shaped baseline vs. a not-yet-built situation-shaped alternative.

## Test sample — 12 operations spanning the range

Picked for range, not randomly: a few CRUD writes, a few read/queries, and — deliberately — the
operations closest to PPM's own situation-shaped examples, since those are where the naming
question bites hardest.

| # | Current (object-shaped) name | Situation-shaped alternative | Category |
|---|---|---|---|
| 1 | `create_issue` | "track a new piece of work" | CRUD write |
| 2 | `close_issue` | "mark this done" | CRUD write |
| 3 | `update_issue` | "update details on something I'm tracking" | CRUD write |
| 4 | `delete_todo` | "remove something from my list" | CRUD write |
| 5 | `attention_query` | "what needs my attention right now" | Read/query |
| 6 | `changes_query` | "what's changed since I last looked" | Read/query |
| 7 | `productivity_query` / `weekly_metrics` | "how's the team doing this week" | Read/query |
| 8 | `list_projects` | "show me what I'm working on" | Read/query |
| 9 | `strategic_planning` / `create_plan` | "help me plan out this initiative" | Conceptual — PPM's own example class |
| 10 | `learn_pattern` | "remember how I like to do this" | Conceptual |
| 11 | `summarize_document` | "give me the gist of this document" | Conceptual |
| 12 | `meeting` | "find time to meet" | Offer-only (control — should route identically either way, since it's slot-filling not classifier-selected) |

## Method

1. **Build two full catalogs** from the same 12-operation sample: Catalog-Object (current real
   names + descriptions, verbatim from the registry) and Catalog-Situation (the alternatives
   above, written with the same level of detail as the real descriptions — not deliberately worse
   or better, matched effort).
2. **Write a realistic-utterance set** — for each of the 12 operations, 2–3 user utterances a real
   PM might actually type (not the operation's own name in disguise — that would trivially favor
   whichever catalog uses closer vocabulary). ~30 utterances total.
3. **Run both vendors** (Claude + a GPT model), each given the full 12-tool catalog (one naming
   condition at a time) plus one utterance, asked to select which tool applies. Record
   correct/incorrect per (utterance, catalog, vendor).
4. **Compare selection accuracy**: Catalog-Object vs. Catalog-Situation, per vendor and pooled.
   The control operation (`meeting`) should show no difference — if it does, that's a confound in
   the harness, not a real finding, and needs fixing before trusting the other 11.

## What counts as an answer

- **Situation-shaped wins or ties**: proceed with PPM's original recommendation, no further gate.
- **Situation-shaped loses on tool-selection accuracy**: real tension between human legibility and
  LLM routing — worth a hybrid design (e.g., situation-shaped *description*, object-shaped or
  dual-labeled *name*) rather than picking one axis and accepting the other's cost blind.
- **Mixed by category** (e.g., situation-shaped helps conceptual operations, hurts CRUD): also a
  real, useful answer — informs a per-category naming policy rather than a single global one.

## What this shares with, and doesn't share with, the recomposition probe (#1463)

Both are live-API probes testing something about how a client LLM handles Piper's tool-facing
surface, and both could reasonably reuse harness code (API-call plumbing, vendor pinning
discipline, result logging). **They test different things**: recomposition is about whether a
payload's content survives a client LLM's summarization; this is about whether a *name* gets a
tool correctly *selected* in the first place, upstream of any payload existing. Not blocking this
on CXO's rig — flagging the overlap so harness code can be shared if useful, not so this waits on
someone else's schedule.

## Not yet done

- Actually running the probe (live API calls, both vendors) — this design's explicit next step,
  its own unit of work.
- The 8 remaining operations of the ~53 not in this sample — 12 was chosen for range and cost, not
  claimed as exhaustive; worth revisiting if the initial 12 show a strong signal either way.
- Any decision about hybrid naming — that's downstream of results, not decidable from the design
  alone.

**Verified how**: catalog contents from a live Explore-agent read of `workflow_entries.py` and
`action_registry.py` this fire, not recalled or assumed — 53 operations, ~110 aliases, naming
style confirmed 100% object-shaped by direct inspection. PDR-006's actual question quoted verbatim
from the source document, not paraphrased from memory of the earlier planning docs.
