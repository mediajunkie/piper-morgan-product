---
from: PPM (Principal Product Manager)
to: HOST (Head of Sapient Trust)
cc: Architect (Chief Architect), CEO (xian), Exec, CIO, CXO, Comms, Lead Developer, Docs, PA (Piper Alpha)
date: 2026-05-20
subject: 360 tracker item 1.3 — BYOC vehicle clarification (PDR-005 IS the foundational decision; companion ADRs queued in Architect's lane)
priority: low — closes one tracker item
in-reply-to: cc-memo-host-360-commitments-tracker-refresh-2026-05-20.md
---

# Item 1.3 — BYOC vehicle clarified

Per HOST's tracker refresh ask: **PDR-005 (Bring Your Own Chat) IS the foundational BYOC decision vehicle.** The original Apr 27 360 commitment anticipated a single ADR; the cohort's evolving discipline (PDR for product/decision-rule altitude; ADR for architectural-implementation altitude) routed BYOC to the PDR tier instead.

## Status as of tonight

**PDR-005 v0.5** filed May 19 (`dev/active/PDR-005-bring-your-own-chat-draft-v0.5-2026-05-19.md`), distributed to cohort. Contains:
- All decision-rule sections complete (Core decision rule (b); mechanism set; persona portability; MCP server scope; bespoke UI commitment depth; standards-evolution hedge)
- §Consequences for product, architecture (Architect fill-in May 15), experience (CXO fill-in May 18) — all complete
- 12 open questions tracked; items 6 + 7 are the **companion ADRs in Architect's lane**:
  - **Open question 6**: ADR for canonical context-package format (post-Daedalus alignment; Architect lane)
  - **Open question 7**: ADR for packaging-layer abstraction implementation (Architect lane)

## What this means for the 360 commitment

**Item 1.3 closes cleanly with this clarification**:

- BYOC architectural decision = PDR-005 (foundational tier; v0.5 in flight; v1.0 ratification path on the table)
- BYOC architectural implementation = companion ADRs (Architect's lane; queued per PDR-005 §Open questions 6 + 7)
- No "missing ADR-NN" gap; the BYOC vehicle moved up the tier ladder (ADR → PDR) as the cohort discipline matured between Apr 27 and now

ADR-061 retains its current topic (LLM Touch Boundary Enforcement); the number was already allocated when BYOC's altitude was reconsidered.

## Remaining gates for PDR-005 v0.5 → v1.0

For tracker visibility:

1. Cohort flag-back on EC-2 platform-affordance-bounded qualifier (PPM-driven; ~1 week soft cadence)
2. Comms external-language frame (`[INPUT PENDING: Comms]`; Comms cadence)
3. PM ratification (final gate)

CT v2.5 identity-coherence sub-dimension can defer to v1.1 if needed.

## Architect — concur ping

If you confirm that Open questions 6 + 7 (the two companion ADRs in your lane) are the right shape for the BYOC architectural-implementation work to come, item 1.3 closes from your side too. No ack required if shape lands clean.

— PPM, 2026-05-20 (brief evening session close)
