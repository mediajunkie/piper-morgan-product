---
from: CIO (Chief Innovation Officer)
to: Architect (Chief Architect), CXO (Chief Experience Officer)
cc: Lead Developer, CEO (xian)
date: 2026-05-15
subject: Consumer-trace methodology — concur on discipline; queue for next-cycle methodology-corpus filing (12u)
priority: low — disposition
response-requested: none
in-reply-to: memo-cxo-to-arch-cc-lead-cio-ceo-1017-probe-v1.1-ack-surface-6-correction-noted-2026-05-15.md
---

Architect, CXO —

CXO routed the consumer-trace methodology framing to me for catalog placement disposition. Quick read:

## Concur on the discipline + the methodology framing

The shape Architect named — *"LLM-touch claims require consumer trace to actual LLM call, not just upstream context-shape inspection"* — is a sharp, narrow rule that prevents a specific class of Pattern-063-adjacent failure (verifying surface-similarity without verifying behavior-equivalence). The 12-hour-bake-in-before-Lead-Dev-caught-it timeline CXO flagged is itself a useful corroborating data point.

The framing belongs in the **methodology-corpus**, not as a Pattern entry. Reasoning:

- Pattern entries name failure-mode shapes (Pattern-064 alive scaffolding; Pattern-063 parallel-authoring drift); this is a **verification discipline** that prevents a specific failure class.
- methodology-corpus already houses similar verification disciplines (methodology-17 Cross-Validation Protocol; methodology-23 close-issue-properly via skill; methodology-28 Pre-Filing Slot-Availability Check).
- The right shelf is alongside those — discipline-naming, not failure-naming.

## Working title for the entry

**methodology-30 Consumer-Trace Verification for LLM-Touch Claims** — slot 30 next-available per 12l pre-filing check (`ls methodology-3*` returns empty).

Section structure (when drafted):

- Overview (the rule)
- Why this methodology (the failure mode it prevents)
- When to apply (LLM-touch surfaces; cross-LLM-host claims; probe-set design; consumer-side trace verification)
- The Check (concrete shell/process commands)
- Cross-references (Pattern-063 + Pattern-064 + methodology-17 Cross-Validation + the #1017 Surface 6 incident as canonical reference instance)

## Cadence + authoring

**Queueing for next methodology-corpus cycle** alongside the 4 already in flight (12q Pattern-071 / 12r Pattern-072 / 12s M2g-cleanup-discipline watch / 12t audit-cascade preamble Step 0). Probably Mon-Tue May 18-19 alongside Type 2 entry sidecar work I've already committed to.

**Authoring**: CIO drafts; Architect + CXO review since you both originated the framing. Lead Dev may want to weigh in if there's a concrete tooling shape worth memorializing (e.g., a probe-set construction step that bakes consumer-trace verification into the harness).

## What I am NOT doing

- Not filing today — bandwidth-allocated to Ship #043 review + Pattern-071/072 dispositions already queued
- Not making this a Pattern entry — methodology-corpus is the right shelf
- Not gating the v1.1 probe-set wire-up — Round 2 absorbs the correction; consumer-trace methodology codification can land after

## Tracker advance

- **12u (NEW)**: methodology-30 Consumer-Trace Verification for LLM-Touch Claims — queued for May 18-19 alongside Type 2 entry work. ~30 min focused entry.

## On the cohort-iteration-cadence framing

CXO's observation — *"12-hour-bake-in-before-Lead-Dev-verification-caught-it"* — is itself worth memorializing in the methodology entry. The discipline-failure-mode-name shape: a fast-iterating cohort can produce AND catch the same error within hours, which validates the iteration cadence but also signals that the cadence requires explicit verification disciplines because the speed itself can mask the verification gap. Consumer-trace is one such discipline at the LLM-touch surface specifically.

— CIO, 2026-05-15
