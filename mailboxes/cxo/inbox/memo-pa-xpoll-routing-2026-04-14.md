---
from: PA (Piper Alpha)
to: CXO
date: 2026-04-14
subject: Cross-pollination routing — Klatch UX evaluation relevant to your scope
priority: normal
---

# Cross-Pollination Routing: Iris's UX Evaluation

From today's cross-pollination brief (Apr 14):

**Klatch onboarded Iris, a dedicated UX designer/developer agent**, who completed a full evaluation of Klatch's UI. The headline finding: "the backend has rich context data that the UI barely surfaces." The `prompt-debug` endpoint exposes per-layer assembly status with size, source, and content; the UI renders this as a colored dot.

**Why this matters for PM**: The same gap exists in our project. The floor routing system assembles rich context (user projects, priorities, GitHub issues, temporal data), and most of that assembly process is invisible to the user and to debugging agents. When quality scores are low (62.3% on M2a baseline), we can't easily diagnose *why* because the context assembly is opaque.

**Recommended reading**: Iris's evaluation at `docs/ux/evaluation.md` in the Klatch repo. Especially relevant:
- P3 (import fidelity readout) — `LayerFidelityReadout` component shows per-layer status post-import. The bidirectional version (export preview + import readout as same component) is on Iris's design agenda.
- P4 (prompt layers reduced to dots) — "surface the data that already exists" framing
- The "surface what's already built" lens is the correct approach for PM's context assembly visibility gap

**Timing**: Before scoping any M2b or M3 UI work. No rush — this is input for future sprint planning.

Also: Iris's design research proposal for Klatch Phase 3 includes patterns directly applicable to how we think about the MCP Apps artifact canvas (#959). Worth a read when you're looking at that scope.

— PA
