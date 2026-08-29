# ADR-059: Workflow Dispatcher and Offer System Consolidation

**Status**: APPROVED (2026-03-19, Chief Architect)
**Issue**: #922
**Date**: 2026-03-19
**Decision Makers**: Lead Developer, Chief Architect, PM

---

## Context

### Problem Statement

Piper Morgan has three independent systems for offering workflows to users and detecting acceptance, plus a fourth mechanism for resume offers. These were built at different times for different issues and never unified:

| System | Origin | Detection Method | Pipeline Location |
|--------|--------|-----------------|-------------------|
| **Soft Offer** (#824) | Proactive workflow suggestions | `detect_offer_response()` via ACCEPT_PATTERNS | Line 448 in intent_service.py |
| **Onboarding Offer** (#888) | First-time user setup | `handle_offer_response()` via CONFIRM_PATTERNS | Line 596 in intent_service.py |
| **Contextual Offer** (#852) | "Would you like to know more?" | `detect_offer_response()` (shared with soft) | Line 530 in intent_service.py |
| **Resume Offer** | Suspended process resumption | Frozenset matching | Line 606 in intent_service.py |

### Impact

**#922 (Critical UX Bug)**: When the system offers "Would you like me to help you set up your project portfolio?" and the user says "Sure", the soft offer system consumes the affirmation first (line 448 runs before line 596). But soft offer's switch statement at line 449 only has a real handler for `meeting` — for `project_setup`, it returns "Let's get things organized" and does nothing. The onboarding system at line 596 never fires.

This is an instance of the "extension without integration" pattern (see methodological note, 2026-03-16): `project_setup` was added to the workflow type map but the acceptance path was never completed.

### Systemic Pattern

The same structural failure — extending one layer without verifying downstream layers — has now caused 6 bugs (#915, #916, #918, #919, #922, plus the onboarding dead-end). The root cause is that each offer system has its own detection logic, its own pipeline position, its own acceptance handling, and no shared contract.

### PM Direction

PM has directed (2026-03-19):
1. Remove the onboarding workflow entirely — it's overdetermined for the current product stage (Gall's Law: get the simple system working before adding complexity)
2. Implement a thin workflow dispatcher — registry-based routing, no business logic in the dispatch layer
3. Consolidate where possible — reduce the number of systems solving the same problem

---

## Decision

### Part 1: Remove Onboarding (Immediate)

Comment out / disable all onboarding workflow code:
- `services/onboarding/portfolio_handler.py` — handler, state machine, turn processing
- `services/process/adapters.py` — `OnboardingProcessAdapter` registration
- `services/process/registry.py` — unregister onboarding at priority 10
- Onboarding offer detection at intent_service.py line 596-601
- Related tests: mark as skipped with `# ADR-059: onboarding on ice` comment

**Rationale**: Onboarding is one of three competing offer/acceptance mechanisms. It has its own state machine (OFFERED → ACTIVE → SUSPENDED → COMPLETED), its own pattern detection, its own pipeline hook. Removing it eliminates one competing system and simplifies the remaining consolidation. If the onboarding experience is wanted later, it can be re-enabled on top of the unified dispatcher.

### Part 2: Workflow Dispatcher (Structural Fix)

Replace the `if workflow_type == "meeting"` switch in soft offer acceptance with a registry-based dispatcher:

```python
# services/intent_service/workflow_dispatcher.py

WORKFLOW_REGISTRY: dict[str, WorkflowEntry] = {
    "meeting": WorkflowEntry(
        entry_point=start_slot_filling,
        requires_context=["attendees", "time"],
    ),
    # Future entries added here — no switch statement modification needed
}

def dispatch_workflow(workflow_type: str, session_id: str, **kwargs) -> IntentProcessingResult:
    entry = WORKFLOW_REGISTRY.get(workflow_type)
    if entry is None:
        # No handler → route to floor with context
        return route_to_floor(workflow_type, session_id)
    return entry.entry_point(session_id, **kwargs)
```

**Design principles** (informed by OpenClaw Gateway pattern):
- Dispatcher is **dumb plumbing** — maps `workflow_type → entry_point`, nothing else
- No business logic in the dispatch layer
- Unknown workflow types route to floor (safe default), not a dead end
- New workflows are added by registering an entry, not modifying a switch

### Part 3: Reconcile Soft Offers and Contextual Offers

**Assessment**: These serve genuinely different purposes:
- **Soft offers**: "Would you like me to start workflow X?" → acceptance enters a multi-turn workflow
- **Contextual offers**: "Would you like me to elaborate on that?" → acceptance continues the current topic

**Decision**: Keep both, but unify acceptance detection:
- Shared `detect_offer_response()` (already shared between soft and contextual)
- Soft offer acceptance → workflow dispatcher (Part 2)
- Contextual offer acceptance → continuation hint passed to floor
- Resume offer → treated as a soft offer for a suspended workflow type

---

## Architectural Questions for Chief Architect

**Q1**: Should the workflow dispatcher be a new component (`services/intent_service/workflow_dispatcher.py`) or folded into the existing `WorkflowOfferService` in `soft_invocation.py`?

**Lead Dev recommendation**: New component. `WorkflowOfferService` handles offer *presentation* (should_offer, format_offer, throttling). The dispatcher handles offer *acceptance routing*. These are different concerns. Keeping them separate follows the same pattern as action_registry.py (disposition lookup) being separate from intent_service.py (dispatch).

**Q2**: After removing onboarding, the guided process registry (`services/process/registry.py`) still has `ONBOARDING` at priority 10. Should we:
- (a) Remove the registration entirely
- (b) Keep the slot but have it return "not active" (current behavior when no session exists)
- (c) Replace it with a generic "workflow in progress" adapter that any dispatcher-launched workflow can use

**Lead Dev recommendation**: Option (c) long-term, option (a) for now. The dispatcher should be able to launch workflows that become guided processes, but that's a future concern. For now, just remove the dead registration.

**Q3**: The resume offer mechanism (line 606) detects suspended processes and offers to resume them. Should this go through the workflow dispatcher, or remain separate?

**Lead Dev recommendation**: Route through dispatcher. A resume is just "start workflow X with pre-existing state." The dispatcher entry point can accept a `resume_session` parameter.

---

## Consequences

### Positive
- Single acceptance detection path (no more pipeline position races)
- New workflow types added by registry entry, not code changes
- Onboarding removal simplifies the intent processing pipeline by ~40 lines
- Unknown workflow types fail gracefully (floor) instead of silently (dead end)
- Reduces the "extension without integration" attack surface

### Negative
- Onboarding UX is lost until re-implemented on the new dispatcher
- Minor refactor of intent_service.py acceptance handling (~100 lines)
- WorkflowOfferService API unchanged but callers need to route through dispatcher

### Risks
- If meeting slot-filling has implicit coupling to the current soft offer code path, extracting it to a registry entry may break it
- Must verify that `detect_offer_response()` timing (line 448) still works when dispatch is decoupled from detection

---

## Implementation Plan

1. **Phase A**: Remove onboarding (disable code, unregister, skip tests) — ~1 hour
2. **Phase B**: Create workflow_dispatcher.py with registry and `dispatch_workflow()` — ~1 hour
3. **Phase C**: Refactor soft offer acceptance (line 449-509) to call dispatcher instead of switch — ~1 hour
4. **Phase D**: Route resume offers through dispatcher — ~30 min
5. **Phase E**: Verify meeting slot-filling still works end-to-end — ~30 min
6. **Phase F**: Update action_registry.py to include workflow dispositions — ~30 min

Total: ~5 hours estimated

---

## References

- #922: BUG: Conversation continuity broken
- #824: Soft offer system
- #888: Onboarding workflow
- #852: Contextual offer system
- Methodological note: `dev/active/methodological-note-classification-handling-contract.md`
- CIO memo: `mailboxes/cio/inbox/cover-note-classification-handling-contract-2026-03-16.md`
- OpenClaw Gateway pattern (cited for dispatcher design principle)
