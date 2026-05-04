# Gameplan: #790 MVP Trust-gated calendar integration behavior

**Issue**: #790
**Branch**: `claude/790-trust-gated-calendar`
**Drafted**: 2026-05-03 by Lead Developer
**Template**: gameplan-template.md v9.3

---

## Summary

Replace the current alpha "silent when calendar not connected" behavior (#789) with a trust-stage-aware progressive-disclosure flow:

- **First encounter** (any stage): Offer to help connect calendar
- **Subsequent (declined)**: Stay silent (don't nag)
- **Subsequent (interested / asked)**: Provide setup guidance
- **Connected**: Show events normally (unchanged)

Stores user response in `UserPreferenceManager` so the offer doesn't repeat. Reads `TrustComputationService.get_trust_stage()` to gate any proactive nudging higher than offer-once.

---

## Phase -1: Infrastructure Verification

**Status**: ✅ Done (2026-05-03 spike — `dev/2026/05/03/m2e-phase-minus-1-infra-spike.md`).

| Surface | Status |
|---|---|
| `calendar_connected` flag on `temporal_summary` | ✅ Present (`services/mcp/consumer/google_calendar_adapter.py:81`) |
| Greeting branch on `calendar_connected == False` | ✅ Present (`services/intent_service/canonical_handlers.py:279`) |
| `TrustComputationService.get_trust_stage(user_id)` | ✅ Present (`services/trust/trust_computation_service.py:118`) |
| `UserPreferenceManager.set_preference / get_preference` | ✅ Present (`services/domain/user_preference_manager.py:114, 166`) |
| User-scoped preference persistence | ✅ Working (used by reminders + learning prefs) |
| Issue #789 alpha-fix closed | ✅ Closed |

**No infrastructure gaps.** Risk: low. All ingredients exist; this issue composes them.

---

## Phase 0: GitHub Investigation

- [ ] Re-read #790 body for any updates since 2026-05-03 disposition
- [ ] Confirm #789 is closed and the silent-default is the current shipped behavior
- [ ] Check #790 for cross-references to #997 (TrustStage display badge) or related trust-UI issues — should not block

---

## Phase 0.5: Frontend-Backend Contract

The greeting flow is server-side rendered through chat — no separate frontend contract. The "offer" is a chat message that nudges the user toward `/integrations` (the existing calendar-connect UI page). Verify the integrations page slug + message wording before committing copy.

- [ ] Confirm the `/integrations` route exists and is the canonical calendar-connect entry point (or use the actual current path)

---

## Phase 0.6: Data Flow

```
greeting handler
  ↓
temporal_summary.calendar_connected == False
  ↓
read trust_stage = TrustComputationService.get_trust_stage(user_id)
  ↓
read offer_state = UserPreferenceManager.get_preference("calendar_setup_offered")
  ↓
decision matrix:
  - offer_state == None        → offer setup help, set offer_state = "offered"
  - offer_state == "declined"  → stay silent
  - offer_state == "deferred"  → stay silent (re-offer if user asks about calendar)
  - offer_state == "accepted"  → silent (calendar should connect soon)
  ↓
emit greeting message + optional offer
```

Persisted preference key: `calendar_setup_offered` (one of: `None | "offered" | "declined" | "deferred" | "accepted"`).

---

## Phase 0.7: Conversation Design

| Trust stage | First encounter (no prior offer) | If user declined | If user deferred / asked |
|---|---|---|---|
| NEW | "I noticed your calendar isn't connected yet — would you like help setting that up? I can point you to the integrations page." | Silent | Same setup guidance + link |
| BUILDING | Same as NEW | Silent | Same setup guidance + link |
| ESTABLISHED | Same as NEW (offer once is offer once regardless of trust stage) | Silent | Same setup guidance + link |
| TRUSTED | Same | Silent | Same |

**Key design point**: Trust stage **does not** unlock more aggressive offers. The offer is "once per user, period." Trust stage gates whether the offer is *worded* more proactively (TRUSTED could phrase it as "Want me to walk you through connecting Google Calendar?" vs NEW's lighter touch). For MVP, keep one wording across stages — copy variants are post-MVP polish.

**Detecting "user asked about calendar"**: pre-classifier already routes calendar queries. The decision point is: when temporal_summary.calendar_connected == False AND the user's intent involved calendar (not just a generic greeting), surface setup guidance regardless of prior offer state.

---

## Phase 0.8: Post-Completion Verification

- [ ] Manual smoke test as user with no calendar credentials:
  - First "Hi Piper" → offer appears
  - Decline ("no thanks") → next "Hi Piper" is silent
  - Ask "What's on my calendar?" later → guidance link appears
- [ ] Manual smoke test with connected calendar: behavior unchanged from current state
- [ ] Tests pass in CI

---

## Phase 1: Decision-state model + preference key

**Files**:
- `services/domain/user_preference_manager.py` — add `CALENDAR_SETUP_OFFERED = "calendar_setup_offered"` key + helper getters/setters mirroring the existing reminder-preference pattern (`get_reminder_enabled`/`set_reminder_enabled` shape)

**Acceptance**:
- New preference key constant exported
- `get_calendar_setup_offer_state(user_id) -> Optional[str]` returns one of `None | "offered" | "declined" | "deferred" | "accepted"`
- `set_calendar_setup_offer_state(user_id, state)` persists via `set_preference`
- Unit tests in existing `tests/unit/services/domain/test_user_preference_manager.py` pattern

**Estimate**: 30 min

---

## Phase 2: Trust-gated decision helper

**Files**:
- `services/intent_service/calendar_offer_policy.py` (new, ~80 LOC) — pure decision function

```python
@dataclass
class CalendarOfferDecision:
    should_offer: bool
    offer_text: str  # empty if should_offer=False
    new_state: Optional[str]  # what to write back to preference

async def decide_calendar_offer(
    *,
    calendar_connected: bool,
    user_id: UUID,
    user_intent_mentions_calendar: bool,
    trust_stage: TrustStage,
) -> CalendarOfferDecision: ...
```

**Acceptance**:
- Returns `should_offer=False` when `calendar_connected=True`
- Returns `should_offer=False` if state is `"declined"` and user didn't mention calendar
- Returns offer-text + `new_state="offered"` on first encounter
- Returns guidance + no state change if state is `"deferred" | "declined"` AND `user_intent_mentions_calendar=True`
- Pure function (takes deps as args; no global I/O); easy to unit-test
- 12-15 unit tests covering each branch

**Estimate**: 1.5 hr

---

## Phase 3: Integrate into canonical_handlers greeting flow

**Files**:
- `services/intent_service/canonical_handlers.py:277-282` — replace the silent-only branch with a call to `decide_calendar_offer()` and append the offer text (if any) to `message`; persist `new_state` if non-None

**Acceptance**:
- Existing silent behavior still applies for users in `"declined"` state (no regression on alpha-fix)
- New users get the offer once
- Persistence write is awaited (not fire-and-forget)
- Existing canonical-handler tests still pass; new test file `tests/unit/services/intent_service/test_calendar_offer_integration_790.py` covers each persisted-state path

**Estimate**: 1 hr

---

## Phase 4: Detect "user is asking about calendar" intent

**Files**:
- `services/intent_service/canonical_handlers.py` (or wherever the calling site assembles the offer-decision args) — pass `user_intent_mentions_calendar=True` when the inbound user message routed via a calendar-related intent

**Detection**: the simplest signal is the existing pre-classifier or canonical-action mapping — if the user invoked a calendar handler (or asked something matching calendar patterns), set the flag. We don't need a brand-new classifier here; just thread the existing intent label.

**Acceptance**:
- "What's on my calendar?" with calendar disconnected + `state="declined"` → guidance returned (not silent)
- "Hi Piper" with calendar disconnected + `state="declined"` → silent (unchanged)
- 4-6 integration tests covering both paths

**Estimate**: 45 min

---

## Phase 5: Tests + verification

**Files**:
- Phase 1: 5-7 tests for new preference helpers
- Phase 2: 12-15 tests for `decide_calendar_offer` (pure)
- Phase 3: 6-8 tests for canonical-handler integration
- Phase 4: 4-6 integration tests for "user asked about calendar" path
- Total target: ~30 new tests

**Verification**:
- [ ] `pytest tests/unit/services/intent_service/test_calendar_offer*.py -v` all passing
- [ ] `pytest tests/unit/services/domain/test_user_preference_manager.py -v` no regressions
- [ ] Pre/post merge regression sweep on full unit suite
- [ ] Manual smoke per Phase 0.8 checklist

**Estimate**: 1 hr (most tests fall out of phases 1-4 above)

---

## Phase Z: Handoff

- [ ] Issue #790 closed with implementation evidence (per CLAUDE.md issue-closure-protocol)
- [ ] Cross-reference #789 (alpha fix) — note this supersedes the silent-only behavior with a richer flow
- [ ] Session log updated with phase-by-phase commits
- [ ] Branch merged to main; sign-off discipline checklist run

---

## Total Estimate

~4-5 hours (small, low-risk; all deps satisfied).

## Risks

- **Low**: pre-classifier intent labels may not include a clean "user-mentioned-calendar" boolean. Fallback: keyword-grep on user message for `/calendar|meeting|event/i` as a Phase 4 escape hatch.
- **Medium**: copy decisions for the offer text need PM sign-off — flag for audit walkthrough.

## Dependencies

- #789 (alpha fix) — closed ✅
- All Phase -1 infra — present ✅

## Audit Cascade Matrix (Issue → Gameplan)

| Template Requirement | Status | Notes |
|---|---|---|
| Issue number referenced | ✅ | #790 in header |
| Problem statement | ✅ | Trust violation from #789; user-helpful behavior needed |
| Phase -1 infra verification | ✅ | All deps verified present in 2026-05-03 spike |
| Phase 0 GitHub investigation | ✅ | Cross-refs to #789, integrations page |
| Phase 0.5 FE-BE contract | ✅ | Server-side; chat message + integration page link |
| Phase 0.6 Data flow | ✅ | Diagrammed; preference key spec'd |
| Phase 0.7 Conversation design | ✅ | Trust-stage matrix + first-encounter wording |
| Phase 0.8 Post-completion verification | ✅ | Smoke test checklist |
| Phases 1-N with estimates | ✅ | 5 phases, ~4-5 hr total |
| Acceptance criteria per phase | ✅ | All listed |
| Test strategy | ✅ | ~30 tests across Phase 1-4 |
| Phase Z handoff | ✅ | Evidence, cross-ref, sign-off |
| Dependencies listed | ✅ | #789 closed; infra present |
| Risks identified | ✅ | 2 risks called out |
| File paths cited | ✅ | All references include grep-able paths |

### Audit ⚠️ Items for PM Walkthrough

**⚠️ Q1**: Copy for the offer text — proposed wording is "I noticed your calendar isn't connected yet — would you like help setting that up? I can point you to the integrations page." OK as-is, or want to refine? (PM-decided)

**⚠️ Q2**: Should the offer copy vary by trust stage (NEW lighter, TRUSTED more proactive)? Gameplan currently keeps one wording across stages and defers variant copy to post-MVP. Confirm or override.

**⚠️ Q3**: For the "user-mentioned-calendar" signal, gameplan proposes threading the existing intent label rather than a new classifier. OK with that lightweight approach, or want a more rigorous detector?

**⚠️ Q4**: Preference key naming — `calendar_setup_offered` per issue body, with state values `None | "offered" | "declined" | "deferred" | "accepted"`. Reasonable, or prefer different vocabulary (e.g., `"asked_again"` instead of `"deferred"`)?
