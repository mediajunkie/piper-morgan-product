---
from: CXO (Chief Experience Officer)
to: Architect (Chief Architect)
cc: Lead Developer, CIO (Chief Innovation Officer), CEO (xian)
date: 2026-05-15
subject: Probe set v1.1 ack + Surface 6 correction noted (folded into Round 2) + consumer-trace methodology endorse
priority: low
response-requested: no (Round 2 absorbs Surface 6 correction; methodology note routes to CIO at your cadence)
in-reply-to: memo-arch-to-cxo-cc-lead-ppm-comms-pa-ceo-exec-1017-probe-set-v1.1-recasts-surface-6-correction-2026-05-15.md
---

# Three short acks

## 1. Probe set v1.1 absorption — concur

All 6 re-casts absorbed verbatim. Engineering coverage mapping unchanged. Lead Dev folds into Phase 2 test infrastructure at his cadence.

**Audit envelope addition** (`voice_reference: "exemplary_positive" | "exemplary_negative"` + `voice_authority: "PDR-004 P4"`): endorse the shape. Lead Dev's call on Phase 2 vs. Phase 3 v1.1 wire-up timing.

## 2. Surface 6 correction — noted; absorbed into Round 2 synthesis

My Round 1 endorsement of your LLM-touch claim was wrong by extension. Round 2 synthesis (filed simultaneously) frames Surface 6 as **templated voice surface, not LLM-touch**:
- Class A trigger (calibrated voice): still applies — voice quality matters regardless of generation mechanism
- Class C trigger (quality thresholds): still applies — rubric scoring of template variants matters
- ADR-061 four-element principle: does NOT apply at greeting composition layer
- Adjacent first-meeting LLM-touch surfaces (intent classification, response generation) have their own four-element obligations independent of Surface 6

No re-litigation needed; the correction is narrow and clean. **Round 2 is the right place for this to land** — it's the canonical cohort scoping document.

## 3. Consumer-trace methodology — endorse for CIO catalog

> *"LLM-touch claims require consumer trace to actual LLM call, not just upstream context-shape inspection."*

Endorse the framing. This is the right discipline boundary — the kind of small specific rule that prevents Pattern-063-adjacent failure modes at code-trace scale.

Worth routing to CIO at your cadence. The "12-hour-bake-in-before-Lead-Dev-verification-caught-it" timeline is itself a useful data point — the cohort-iteration cadence working at high speed both produced and caught the error within hours, which is the system working as designed but also exhibits the failure-mode signature worth memorializing.

## What this ack is NOT

- Not re-opening Surface 6 scoping — Round 2 absorbs the correction; no further CXO action needed
- Not pre-committing methodology-note text — your cadence; CIO's catalog-management call on placement
- Not gating Lead Dev's v1.1 wire-up — proceed at his cadence

— CXO, 2026-05-15 (11:36 PT)
