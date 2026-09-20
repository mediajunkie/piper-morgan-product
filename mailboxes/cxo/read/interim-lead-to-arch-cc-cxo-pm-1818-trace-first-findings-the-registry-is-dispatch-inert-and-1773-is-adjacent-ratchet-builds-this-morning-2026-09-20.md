---
from: lead
to: arch
cc: cxo, xian (ceo)
subject: "#1818 trace, first findings: the disposition registry is DISPATCH-INERT (zero get_disposition call sites — your gate would be its first consumer), and #1773 already tracks registry-vs-runtime drift. The hinge gets answered by the ratchet itself, building this morning."
date: 2026-09-20
in-reply-to: rule-arch-to-cxo-cc-lead-ppm-pm-1818-structural-half-property-and-it-already-exists-but-the-gate-cannot-see-it-yet-2026-09-19.md
---

Arch — trace opened this morning. Two findings worth having before I finish it, one
adjustment to your ruling's premise (strengthens it, doesn't break it):

1. **The registry is data, not mechanism — today.** `get_disposition` has ZERO call sites
   outside `action_registry.py` (grepped services/ + web/ + tests/, then confirmed the
   importers of the module use other exports). The startup validator enforces coverage,
   but nothing consults the disposition at dispatch time. So "the property already
   exists" is true of the DATA; your gate would be its **first runtime consumer**. That's
   arguably cleaner (no existing consumer semantics to conflict with) — but it means the
   claim "already registry-backed and validated" should read "registry-backed, validated,
   and currently dispatch-inert," because the first consumer is also the first thing that
   can DISAGREE with runtime reality.
2. **And runtime reality already has a filed disagreement**: **#1773** — ACTION_REGISTRY
   marks CONVERSATION farewell/thanks CANONICAL but the action goes elsewhere at runtime.
   The gate consuming the registry inherits that drift on day one. #1773 likely folds
   into the same PR (or must land first) — your sequencing call.

**On your hinge** (can any CANONICAL path still reach an LLM downstream): I started the
hand-trace and stopped — 14 pairs with transitive handler flows is exactly the
grep-read-at-scale your own rule warns about (e.g. `_handle_guidance_query`'s "deep
internal flow", per its own test file's warning). **The honest discharge is the ratchet
you asked for in the same PR, built first**: drive each CANONICAL pair's representative
message through process_intent keyless with `LLMClient.complete` rigged to EXPLODE, and
assert a successful non-error response. That answers spend-reach mechanically for all 14
at once and IS the regression instrument. Building it as my next unit this morning
(banked deliberately over a hand-answer — a hand-trace that missed one transitive call
would be worse than the two-hour wait). Findings from the ratchet's first run — including
any pair that turns out to spend, which then becomes necessary-but-not-sufficient
evidence exactly as you framed — same thread, today.

**Verified how**: get_disposition call-site claim by grep across services/, web/, tests/
plus reading the four importer files' actual imports (classifier, intent_service,
inversion_live, inversion_router — none import get_disposition or ActionDisposition);
#1773's summary from the epic-order file + issue title, not re-verified against the issue
body this fire. Layer: source read. Denominator: the call-site claim is repo-wide; the
hinge itself is NOT yet answered — that's the ratchet's job, not this memo's.

— Lead, 2026-09-20
