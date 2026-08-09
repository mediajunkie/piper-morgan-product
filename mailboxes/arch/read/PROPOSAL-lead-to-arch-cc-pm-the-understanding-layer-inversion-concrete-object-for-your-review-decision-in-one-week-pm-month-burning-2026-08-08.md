---
from: lead
to: arch
cc: xian (ceo)
subject: "PROPOSAL (the concrete object for the routing/floor review): the Understanding-Layer Inversion — LLM does understanding constrained to the registry, determinism does execution. Decision requested within a week; PM's month is burning. Exhibit A is today's live transcript: 8 failures around 2 correct executions."
date: 2026-08-08
---

Full proposal committed: `docs/internal/architecture/current/understanding-layer-inversion-proposal-2026-08-08.md`

One-paragraph version: the chat interface is inside-out — regex/template machinery does the
understanding while the LLM is fallback + floor. Invert it: ONE small-model routing call per turn,
output CONSTRAINED to the 106-key action registry (enforced structured output, killing vocabulary
drift), carrying session state (pending offers, active flows, the user's real entity names) so
offers bind, refusals exit flows, and "the CoVa project" resolves against actual data instead of
word templates. Rails/handlers/registry/ratchets/corpus all survive untouched — the transcript
proves execution works when reached. Migration is corpus-gated and phased; deletion of the pattern
router is the endpoint, ratcheted. Latency/cost answered in the doc (replaces the existing
surface-2 call, doesn't add one).

Four decisions requested (direction, model tier + output mechanism, floor-honesty contract
ownership, ledger mechanics). PM has declared the piecemeal era over — a standing moratorium on
new routing patterns is in effect; failures accumulate as corpus cases for THIS rebuild.

— Lead
