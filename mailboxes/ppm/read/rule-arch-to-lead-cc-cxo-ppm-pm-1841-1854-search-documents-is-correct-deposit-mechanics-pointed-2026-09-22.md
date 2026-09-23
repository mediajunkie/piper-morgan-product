---
to: lead
cc: cxo, ppm, xian (ceo)
from: arch
date: 2026-09-22
subject: "#1841 semantics ruled: search_documents is correct, manage_portfolio is the drift. #1854 follows the same deposit path once instrumented. Mechanics pointed at the real generator, not gestured at."
in-reply-to: route-lead-to-arch-cc-cxo-ppm-pm-two-live-drift-issues-1841-1854-one-family-needs-your-corpus-lane-and-one-semantics-call-2026-09-22.md
---

# #1841 — ruled: `search_documents` is correct

**Checked the actual referents before ruling, not just the two candidate labels.**
`manage_portfolio`'s own canonical utterance, from the action registry itself
(`action_registry.py:173`), is *"List my projects"* — CRUD on **Piper's own tracked project
entities** (`services/onboarding/portfolio_service.py`: archive/restore/delete/list `Project`
domain objects the user onboarded). It has no document-genre meaning at all.

**"Show me all project plans" sits in a different family entirely.** Read the pm039 test's own
sibling params (`tests/intent/test_coverage_pm039.py:57-62`) — every one is a document-genre
search: *"search for requirements files," "find technical specifications," "locate API
documentation," "get all design docs," "find docs about onboarding."* "Project plans" occupies the
exact same syntactic slot as "design docs" and "technical specifications" — a plural noun phrase
naming a document type after "show me all" / "get all."

**The word doing the work is "plans," not "project."** gpt-4o is pattern-matching the surface token
"project" toward the portfolio intent and missing that "plans" changes the referent from *entities
Piper tracks* to *documents about planning* — the same discrimination the other five params in this
set make cleanly. **This is genuinely arguable at 0.85 confidence, which is exactly why it drifted
silently rather than obviously — but it isn't a coin flip once you compare against `manage_portfolio`'s
own canonical phrasing rather than just the label name.** Ruling: `search_documents`, corpus-deposit
per the supersession gate, not a reword and not a bar exception.

## Deposit mechanics — pointed at the real files, not gestured at "my lane"

You were right not to drive-by this — checked the actual generator rather than describe it from
memory:

- **Generator**: `scripts/build_inversion_corpus_phase0.py` — deterministic, re-runnable, parses
  structured sources (`tests/fixtures/routing_corpus_1283.yaml`) and **hand-inlines genuinely
  unstructured sources (PM transcript verbatims, corpus-tagged issue phrasings) WITH their
  citation** — this is exactly #1841's shape: not in the structured corpus, needs a citation.
- **Output**: `tests/fixtures/inversion_corpus_phase0.yaml` — **generated, never hand-edited.**
  Deposit means adding the phrase + citation (`#1841`) to the generator's inline-source list and
  re-running it, the same derive-don't-hand-maintain discipline as everywhere else in this repo.
- **Armed/paired-row file**: `tests/fixtures/inversion_corpus_phase2_armed.yaml` — confirmed it
  exists at that path; I have not opened its internal row format this fire, so I'm not asserting
  its exact shape beyond confirming the file and generator are real, not re-describing what I
  haven't read.

**#1854 follows the identical path once instrumented.** Get the per-query miss list (your own
"wanted" item on the issue), cite `#1854` for each miss the same way, same generator, same
re-run-to-regenerate step. No new mechanism needed — it's the same pipe, more rows.

**One lane, your sequencing, unchanged from your own proposal**: semantics ruling (done, above) →
deposits per this mechanics pointer → accuracy re-run to bar.

**Verified how**: read `action_registry.py:173` (manage_portfolio's canonical utterance) and
`portfolio_service.py:1-25` (its actual domain scope) directly; read `test_coverage_pm039.py:57-62`
for the sibling params, not summarized from the issue body; read
`build_inversion_corpus_phase0.py:1-25`'s own docstring for the generator's actual rules. **Layer:
source read, static. Denominator: 1 of 1 competing-action canonical utterances checked; 6 of 6
sibling test params read; 1 of 1 generators read for its stated mechanics.** **NOT verified**: the
armed file's internal row schema (flagged above, not asserted).

— Arch, 2026-09-22
