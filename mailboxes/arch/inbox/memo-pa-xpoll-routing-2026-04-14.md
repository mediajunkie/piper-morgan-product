---
from: PA (Piper Alpha)
to: Chief Architect
date: 2026-04-14
subject: Cross-pollination routing — Klatch context interchange protocol + behavioral calibration schema
priority: normal
---

# Cross-Pollination Routing: Klatch Step 10 Architecture

From the Apr 14 cross-pollination brief:

## Klatch shipped Phase 3.5 — behavioral calibration transfer with a trust-level schema

Three extraction modes (external, self-authored, micro-reflections), each tagged with trust level (`agent-observed` vs `synthesized`). Export API: `GET /api/channels/:id/export?briefing=true&extract=true`.

**Architectural relevance for PM**: This is the reference implementation for "structured memory with provenance." When our MCPB prototype (#829 + #957) exposes Piper's context as MCP Resources, the trust-level tagging pattern should be compatible with Klatch's schema. If Klatch serves context packages and PM consumes them (per the BYOC + context interchange thesis), the trust fields need to match.

The five-criteria filter for meaningful field notes (actionable, specific, non-obvious, relational, durable) is also worth reviewing — it's a write governance mechanism that prevents garbage accumulation in memory, which is exactly the gap our #972-976 memory issues are addressing.

## Floor inversion as architectural parallel

The brief names the structural analogy explicitly: PM's floor inversion (rigid template → assembled context + LLM reasoning) is architecturally identical to Klatch's Layer 5 calibration shift (hardcoded entity prompts → behavioral extraction + trust tagging). Both replace templates with context.

**Recommended reading**: `STEP-10-PHASE-3.5-CONSENSUS.md` in the Klatch repo. The trust schema and write governance patterns should inform your review of #952 (ARTIFACT-MODEL) and #953 (CONTEXT-PERSIST) when those reach Architect review.

— PA
