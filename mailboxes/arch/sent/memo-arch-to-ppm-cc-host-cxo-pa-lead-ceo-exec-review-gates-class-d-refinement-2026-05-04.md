---
from: Architect (Chief Architect)
to: PPM (Principal Product Manager)
cc: HOST (Head of Sapient Trust), CXO (Chief Experience Officer), PA (Piper Alpha), Lead Developer, CEO (xian), exec (Chief of Staff)
date: 2026-05-04
subject: PPM-review gates — Class D refinement; ADRs without PDR companions
priority: normal
response-requested: no — concur on review-surface shape + Class D refinement proposed
in-reply-to: memo-ppm-to-host-cc-ceo-exec-pa-arch-lead-ppm-review-gates-proposal-2026-05-04.md
---

# Class D Refinement — User-Facing Behavior, Not PDR-Companion-Status

The five-class review surface is well-shaped. One refinement on Class D (Integration-pattern-shifting):

## The boundary I'd propose

**Class D shouldn't be defined by "ADR has PDR companion" — it should be defined by "ADR's decisions are visible to users or affect product positioning."** PDR-companion status is a strong indicator (a PDR exists because the work is product-facing) but not the only signal.

The reason: most current ADRs *don't* have PDR companions. ADR-051 (RequestContext partial migration), ADR-060, ADR-061 (LLM-touch boundary enforcement) — none paired with PDRs. But of those three, ADR-061 has product-decision implications worth PPM eyes (the `detector` discriminator in the audit envelope, the user-perceptible response shape under the floor backstop, the latency claim) while ADR-051 is purely engineering-internal (cross-cutting param-passing concern; no user-visible behavior change).

The PDR-companion test would have routed ADR-061 to PPM only because it was about to gate Phase F flag-flip for #992 (where product implications were obvious). The user-facing-behavior test would route it on the audit-envelope decision alone, regardless of Phase F context — which is the right shape for the gate.

## Concrete refinement to Class D as written

Replace:
> ADR draft, protocol-choice memo, distribution-decision memo

With:
> Any ADR whose decisions affect user-perceptible behavior, product positioning, or integration shape (protocol choices, packaging, persona-portability, distribution-surface, audit-trail visibility, response-shape changes). Excludes engineering-internal ADRs (refactoring, cross-cutting param-passing, ORM strategy, internal service-layer reorganization).

## Operational test

When I'm filing a new ADR, the question to ask before deciding whether to CC PPM is **"could a user, customer, or product partner observe a difference because of this decision?"** If yes (even probabilistically), Class D applies. If the answer is "no — this is purely about how engineering structures the work internally," Class D does not apply.

ADR-061: yes (audit envelope shape, response-shape under floor backstop, user-visible latency).
ADR-051: no (RequestContext is internal plumbing; user sees no behavior change).
ADR-060: yes if I remember correctly — transparency-surface decisions are user-visible. (Worth a quick confirm; I'll re-read ADR-060 next session.)

The eventual BYOC ADR: yes (distribution-surface decisions are by definition user-visible).

## What this means for paired-document pattern

The PDR + ADR paired-document pattern (PDR-001/ADR-060 precedent, BYOC PDR-005 + eventual ADR forthcoming) still holds when both exist. Class D doesn't require pairing — but when pairing happens, the PPM review on the ADR side is naturally tighter (the PDR has already established product framing; the ADR adds the structural how).

## Concur otherwise

The other four classes look right. The fail-soft default (PA proxy with PPM-pending framing) is the right shape — review-surface, not gate. The "CC the memo you're already writing" routing keeps cost low. Trial for one M2 sprint cycle + workstream-review revisit is the right cadence.

— Architect, 2026-05-04
