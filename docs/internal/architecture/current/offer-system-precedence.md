# Offer System Precedence — How Piper Makes and Fulfills Offers

**Issue**: #926 Gate 3 (Architectural Integrity)
**Date**: 2026-03-24
**Author**: Lead Developer

---

## Overview

Piper has three mechanisms for making offers to users and handling their acceptance. This document defines their ownership, precedence, and interaction rules.

---

## The Three Systems

### 1. Workflow Dispatcher (Registered Workflows)

**Owner**: `services/intent_service/workflow_dispatcher.py`

**What it does**: Routes user acceptance of structured workflow offers (e.g., "Would you like me to help schedule a meeting?" → user says "Yes" → dispatcher routes to the meeting slot-filling entry point).

**Registry**: `WORKFLOW_REGISTRY` — a dict of `workflow_type → WorkflowEntry`. Each entry has:
- `entry_point`: async function to start the workflow
- `resume_point`: optional async function to resume a paused workflow
- `description`: human-readable capability description

**When it fires**: When `detect_offer_response()` detects an acceptance AND the pending offer matches a registered workflow type.

**Precedence**: **Highest for registered workflows.** If a workflow type is registered, the dispatcher owns the acceptance path. No other system should handle it.

### 2. Soft Invocation Detector (Conversational Offers)

**Owner**: `services/intent_service/soft_invocation.py`

**What it does**: Detects natural-language opportunities to offer capabilities during conversation. For example, if a user mentions being busy, Piper might offer "Would you like me to help prioritize your tasks?"

**Registry gate** (#923): Before making an offer, checks `get_registered_workflows()` to verify the offered capability actually exists. Prevents offering things Piper can't do.

**When it fires**: After handler processing, applied via `_apply_soft_offer()` in intent_service.py. Only fires when:
- Trust stage is BUILDING or higher (new users don't get offers)
- No soft offer was already made this turn
- The registry gate confirms the capability exists

**Precedence**: **Lower than dispatcher.** Soft invocation creates offers; the dispatcher fulfills them. Soft invocation never handles acceptance — it only proposes.

### 3. Contextual Offers (Handler-Embedded)

**Owner**: Individual canonical handlers (e.g., `_format_integration_setup_guidance()`)

**What it does**: Handlers embed offers directly in their response text. For example, a setup guidance handler might include "Would you like guidance on setting up a specific integration?"

**When it fires**: During handler execution. The offer text is part of the response, not a separate system.

**Precedence**: **Lowest and most fragile.** These offers have no structured acceptance path — the user's "yes" goes through normal intent classification, which may or may not route back to the right handler. This is the pattern that caused #922 (dead-end acceptances).

---

## Precedence Order

```
User sends message
  │
  ├── Is this an acceptance of a pending offer?
  │     └── YES → Workflow Dispatcher handles it (if registered type)
  │               └── Not registered? → Falls to floor (conversational response)
  │
  ├── Process intent normally (classifier → handler)
  │
  └── After processing: Should we make a new offer?
        └── Soft Invocation Detector checks:
              1. Trust stage ≥ BUILDING?
              2. Registry gate: is the capability registered?
              3. No offer already made this turn?
              └── All yes → Attach offer to response
```

## Rules

1. **Only the dispatcher fulfills registered workflow acceptances.** No handler should try to catch "yes" independently.

2. **Only registered capabilities can be offered.** The registry gate (#923) prevents soft invocation from offering things the dispatcher can't fulfill.

3. **Contextual offers in handler text should be migrated to soft invocation.** Handler-embedded offers bypass the registry gate and have no structured acceptance path. As handlers are updated, move offers to the soft invocation system.

4. **One offer per turn.** Soft invocation checks whether an offer was already made. Multiple offers per response is confusing.

5. **Unknown acceptance → floor.** If a user says "yes" but there's no pending offer or the offer type isn't registered, the conversational floor handles it naturally rather than dead-ending.

---

## ADR References

- **ADR-059**: Workflow dispatcher and offer consolidation
- **#922**: Conversation continuity broken (root cause: three competing offer systems)
- **#923**: Capability awareness gap (fix: registry gate in soft invocation)

---

*Lead Developer | March 24, 2026*

---

## Appendix: Detection sequence in `_process_intent_internal`

Added 2026-04-27 by Chief Architect after first systematic dispatch-path review. The three offer systems above describe the *application* side; this appendix documents the *detection* side — where in the universal entry-point state machine each offer system gets checked.

The dispatch state machine in `services/intent/intent_service.py:_process_intent_internal()` has **three distinct offer-detection points**, separated by other state-machine concerns:

```
_process_intent_internal()
│
├─ (1) PENDING OFFER detection — lines 456-535
│      detect_offer_response() runs first; if user said "yes/no" to a
│      previously-attached workflow offer, the dispatcher fulfills (yes)
│      or declines (no), and the request returns immediately. Workflow
│      dispatcher owns acceptance for registered workflow types.
│
├─ (2) CONTEXTUAL OFFER continuation — lines 537-567
│      One-turn memory check for non-workflow contextual offers (e.g.,
│      "Would you like more results?"). Handler-embedded offer text
│      from the previous turn may be matched here without going through
│      the workflow registry.
│
├─ (other state-machine concerns: trust stage resolution, guided
│  process check, /standup command, ethics gate, KG enrichment,
│  classify_multiple)
│
└─ (3) SOFT OFFER application — lines 783-792 (single-intent path),
       lines 1004-1011 (canonical-handler post-response path)
       After handler processing, _apply_soft_offer() checks whether
       the response should attach a new soft invocation offer for next
       turn. Only fires under the registry gate (#923) and trust-stage
       gate (BUILDING+).
```

**Distinction worth carrying**:
- (1) and (2) are **detection on input** — the user's current message is checked against a previous offer
- (3) is **application on output** — Piper's current response gets a new offer attached for next turn

The two arcs are wired to the same registry (workflow dispatcher's `WORKFLOW_REGISTRY`) but operate on opposite sides of the request: input-side checks fulfill prior offers; output-side application creates new ones.

**Why this matters for future engineers**:

When debugging why an offer "didn't go through," the question is *which* of the three detection points was supposed to fire:
- Did `detect_offer_response()` see the user message as an acceptance? (line 456-535)
- Was there a contextual offer from the previous turn that matched? (line 537-567)
- Did `_apply_soft_offer()` attach a new offer to the response? (line 783-792 / 1004-1011)

Each detection point has its own short-circuit, registry check, and trust-stage gate. Mismatches between *which* point fired vs *which* should have fired account for most of the offer-debugging time the predecessor and Lead Dev spent during M1.

**Architectural rule (post-#922 / ADR-059)**:
- Don't add a fourth detection point without an ADR amendment to ADR-059. Three is enough; adding a fourth re-creates the #922 root cause.
- Handler-embedded contextual offers (system 3 in the main doc above) should be migrated to soft invocation (system 2) over time. Each migration removes one source of orphan acceptances.

---

*Chief Architect | April 27, 2026 — appendix added after first systematic dispatch-path review*
