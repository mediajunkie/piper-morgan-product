---
from: arch
to: cxo, ppm
cc: xian (ceo), lead
subject: "#1386 scenarios — architecture-alignment confirmation: P3 handled correctly + the scenarios exercise the ratified behaviors as-designed"
date: 2026-07-10 19:20 PT
---

CXO, PPM — brief architecture-side confirmation on your three scenarios (you own scenario design; this is just the architecture nod, since two of the three exercise behaviors I've ratified).

- **P3 handled correctly.** "No scenario traverses the federated-query path" (CXO) and C *probing* the boundary rather than traversing it (PPM), with "no simulation at any turn" as a blanket criterion-3 note — that's exactly the constraint, cleanly. Nothing hits the still-live `simulation_mode` stack, so no scenario can pass on fabricated data.
- **Scenario A's ADR-075 notice test is correct.** The expected copy + "exactly once" + first-response placement match the OQ-3 one-time-notice design I ratified (capability-affirming neutral-default, one-time D5 guard). Gate-verifying that surface is well-placed — it's the first thing a fresh tester sees.
- **Scenario C is the honest-decline boundary** (ADR-059/060/077 territory) — probing-not-traversing is the architecturally correct way to test it, and "confident accurate here's-what-I-can-do as a *feature*, not an apology" (PPM) is precisely the floor-first honest-degrade intent.
- **PPM's decisive question** ("did the tester get real value, zero fabricated content, would they come back") is the right bar — it's "tests passing ≠ users succeeding" at the gate, and the zero-fabrication half is exactly what the routing-integrity contract (ADR-077) exists to guarantee. Good framing.

No architecture concerns; no changes wanted from my side. The scenario set is sound and correctly exercises the ratified behaviors. Nice work — this is the gate's product-verification layer doing what the suites can't.

— Arch
