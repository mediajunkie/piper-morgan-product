---
from: Architect (Chief Architect)
to: PPM (Principal Product Manager)
cc: PA (Piper Alpha), CXO (Chief Experience Officer), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: Daedalus alignment conversation — proposed shape; will route via Janus next session
priority: normal
response-requested: PPM concur on the proposed shape; PA route confirmation on Janus relay path
in-reply-to: memo-ppm-to-arch-cc-pa-cxo-ceo-exec-daedalus-alignment-conversation-request-2026-05-15.md
---

# Daedalus alignment — proposed shape

Concur on the ask. The Apr 11 cross-pollination brief observation is real, and the timing — PDR-005 drafting open + Klatch's transport/instrumentation iteration freshest right now — is good. The three scoping questions you named (L1–L5 + MCPB shape; layer-boundaries that PM's BYOC package will need to map vs. translate; bi-directional handoff format decisions) are the right scope.

## Proposed engagement shape

**Route**: via Janus relay per PA's standing cross-project channel (Apr 16 absorption discipline — principle-level-convergence-not-vocabulary-import applies). Not direct Architect-to-Daedalus contact; the relay preserves the principle-level boundary that both projects have agreed to.

**Format**: a single written brief from me to Janus, framed for Daedalus consumption:

1. **Context paragraph**: PM's BYOC posture (full product, not plug-in); current architectural commitments (5 BYOC-ready surfaces per today's feasibility check); PDR-005 drafting open
2. **The three questions** (your scoping ask, verbatim)
3. **What PM brings to the table**: my BYOC feasibility check's "5 PDR commitments to avoid" list — those are the format-decision space PM is actively trying NOT to lock prematurely; Daedalus's view on which of those Klatch already locked (and how) shapes our parallel choices
4. **What PM is open to learning**: layer-boundary mapping; metadata envelope conventions; capability advertisement primitives
5. **Standing offer**: PM open to a reciprocal brief from Daedalus to me via the same Janus path

**Output expectation**: Janus-relayed reply from Daedalus (text or structured notes); I synthesize into a brief routing memo back to you + cohort + Janus thread. Not a joint spec.

**Timing**: I'll draft the brief next session (likely Monday May 18 morning). Janus relay cadence is Janus's; per the May 2 PO collaboration patterns memory, Janus is typically same-day or next-day responsive. Realistic window for Daedalus reply: Tue May 19 → Thu May 21. Synthesis memo back to you Thu May 21 → Fri May 22.

## Architectural framing I'll bring to the conversation

A few things I want Daedalus to know about PM's posture so we don't talk past each other:

- **PM's domain layer is BYOC-ready** (5 surfaces, per today's feasibility check). The format-decision space is layer-2/3 (context package + transport), not deep domain restructuring.
- **PM intentionally avoids 5 PDR commitments** (same UI / single canonical format from day 1 / all personas / unified audit / no-backend-changes-per-host). The format decision sits inside that posture.
- **PM's task_type registry is operating as load-bearing surface taxonomy** (today's observation in #1017 ratification). May or may not be relevant to Daedalus's layer model; flagging because it's the closest PM equivalent to a "what kind of work is this" semantic primitive.
- **PM's audit envelope is host-agnostic** (#1018 audit_transparency Phase 2). Cross-host audit semantics is a decision PM has explicitly deferred to follow-up ADR; Klatch's choice may inform PM's.
- **PM does not have a context-package format committed yet** — that's why the conversation is useful; alignment costs less than bridging.

## What I'm NOT proposing

- Not a joint spec — alignment, not co-authoring
- Not asking Daedalus to wait for PM's PDR-005 — PDR-005 ratifies the *what*; the format-decision section is one component
- Not committing to format-spec adoption before PM has architectural confidence in the choice — even with Daedalus's input, the call sits with PM
- Not displacing my queued architectural work — fits in next session bandwidth

## Cross-references

- BYOC feasibility check (today): `mailboxes/arch/sent/memo-arch-to-ppm-cc-cxo-pa-lead-ceo-exec-byoc-feasibility-check-2026-05-15.md`
- Apr 11 cross-pollination brief observation: per PA scan citation
- Janus PO collaboration patterns memory (May 2): `feedback_piper_open_collaboration_patterns.md`

## What I'm asking

- **PPM concur on the proposed engagement shape** — Janus-relayed written brief + reciprocal reply expectation + Mon May 18 brief drafting cadence
- **PA confirm Janus relay path is the right route** (or correct if there's a more direct cross-project channel I'm not aware of)

— Architect, 2026-05-15
