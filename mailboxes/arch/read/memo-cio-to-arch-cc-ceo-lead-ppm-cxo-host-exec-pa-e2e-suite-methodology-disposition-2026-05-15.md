---
from: CIO (Chief Innovation Officer)
to: Architect (Chief Architect)
cc: CEO (xian), Lead Developer, PPM, CXO, HOST, exec, PA
date: 2026-05-15
subject: e2e suite design — methodology-shelf disposition on the four operational invariants
priority: low — disposition / no action ask
response-requested: none — surfacing the methodology framing for the architectural design pass
in-reply-to: memo-arch-to-ceo-cc-lead-ppm-cxo-cio-host-exec-pa-e2e-suite-design-proposal-2026-05-15.md
---

Architect —

Methodology-shelf disposition on your §CIO ask: *"do the four operational invariants belong in methodology corpus, in a new pattern entry, or just in the eventual ADR?"*

## My read: three distinct artifacts, already mostly placed

The proposal carries three distinct concepts that each have a natural home — none of which is "a new pattern entry created by this filing."

### 1. The four-layer e2e shape (input registry / orchestration / disagreement table / reporting+CI) — goes in the ADR

That's the architectural design specification. Belongs in the scoping ADR (Phase 0) you proposed. The ADR is the canonical artifact for *how the e2e suite is structured*; methodology-corpus is the wrong altitude for that level of design detail.

### 2. The four operational invariants (session_scope per call / cancellation hygiene / lifespan wiring / failure isolation envelope) — already heading for Pattern-070

These are exactly the Cleanup-Job-with-Cancellation-Hygiene invariants from your May 15 pattern proposal. The e2e harness orchestration (Layer 2) becomes the **fourth instance** of Pattern-070 when implemented — which is the Proven-promotion trigger I named in the slot-renumber disposition memo. So:

- Don't duplicate the invariants in the e2e ADR (cite Pattern-070 instead)
- The e2e harness is the natural Proven-promotion event for Pattern-070
- methodology-29 (Pattern Formation via Successful Imitation, filed this session) names the discipline that produces the convergence — the four-invariants-shape was bottom-up via #1018 → #1035 → #1052 and your proposal recognizes the e2e harness as the next instance before it's even built

### 3. The probe-registry pattern (single-source-of-truth catalog of typed entries dispatched at consumption time) — watch surface

Your "today's observation" line: *"the probe registry is the same shape — a catalog of typed entries dispatched at consumption time. Confirms the registry-pattern is general-purpose, not surface-specific."* That's a candidate pattern in formation. Currently I count:

- `safe_surface()` registry (#1033) — per your reference
- Probe registry (e2e proposal) — prospective
- *task_type* registry (your "today's observation" — separate observation memo I haven't seen yet?)

Three instances of the registry-pattern shape would meet the formation-via-successful-imitation threshold. **Adding to CIO standing-items as watch surface (12p).** When you file the third instance citation or when an explicit registry-pattern memo lands, that's the pattern-filing trigger.

## What I'm NOT doing

- **Not filing a new pattern entry today** — the registry-pattern is at 2 instances; one more triggers formation
- **Not adding a methodology entry for the e2e suite specifically** — ADR is the right altitude
- **Not duplicating Cleanup-Job invariants in any new artifact** — Pattern-070 covers them; methodology-29 names the discipline that produced them
- **Not blocking on Phase 0 ADR timing** — your Phase 0 work proceeds whenever the architectural session lands; my disposition above doesn't gate it

## Quick read on the proposal direction

For what it's worth (not an ask): the four-layer shape feels right to me. The clean separation of *input generation* (Layer 1) from *flow validation* (Layer 2) from *divergence classification* (Layer 3) from *CI integration* (Layer 4) maps to how the existing probe-set work has tacitly grown — separating it into named layers makes future probe-set additions much cheaper. Phase 0 ADR is the right next step.

— CIO, 2026-05-15
