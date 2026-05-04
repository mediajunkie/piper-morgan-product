# Gameplan: #900 ENHANCE Standup 3-part structural collection and enhanced completion

**Issue**: #900
**Branch**: `claude/900-standup-3part-structural`
**Drafted**: 2026-05-03 by Lead Developer
**Template**: gameplan-template.md v9.3

**PM Q1 disposition (already received 2026-05-03)**: kept in MVP. Body's "may be polish, may not be MVP" caveat is resolved — proceed with full gameplan.

---

## Summary

Replace the current freeform `GATHERING_PREFERENCES → GENERATING → REFINING → FINALIZING` state machine with a structured 3-part collection flow (yesterday → today → blockers) plus enhanced completion detection (natural-language signals beyond explicit "done") plus partial-content persistence on escape/timeout.

These are quality-of-conversation improvements layered on top of #889's bug-fixed foundation.

---

## Phase -1: Infrastructure Verification

**Status**: ✅ Done (2026-05-03 spike — `dev/2026/05/03/m2e-phase-minus-1-infra-spike.md`).

| Surface | Status |
|---|---|
| `StandupConversationState` enum | ✅ `services/shared_types.py:208` |
| `StandupConversationManager` (state machine + transitions) | ✅ `services/standup/conversation_manager.py:45` |
| `StandupConversationHandler` (chat-side dispatcher) | ✅ `services/standup/conversation_handler.py` |
| `#889` (bug fixes for escape/timeout/suspend) | ✅ Closed — verified |
| `#888` (escape commands, suspend protocol) | ✅ Complete |
| `#1034` (StandupItem dataclass) | ✅ Closed (this session) |
| Suspend/resume mechanism | ✅ Functional via SUSPENDED state |

**Conclusion**: All deps satisfied. Risk: Medium (state machine surgery + new completion-detection logic + persistence semantics).

---

## Phase 0: GitHub Investigation

- [ ] Re-read #900 body
- [ ] Read #889 closure for any caveats noted
- [ ] Confirm #1034's StandupItem dataclass is the right structured shape for partial captures
- [ ] Check if Standup persistence already saves anything (or if everything is in-memory)

---

## Phase 0.5: Frontend-Backend Contract

Standup happens in chat — server-side rendered. No new UI. The user-facing change is **multi-turn prompted collection** instead of "tell me everything in one go."

Output shape per part (per-turn):
- After "yesterday" capture → bot asks "What's planned for today?"
- After "today" capture → bot asks "Any blockers?"
- After "blockers" capture → bot generates final standup

---

## Phase 0.6: Data Flow

```
User: "Standup"
  ↓
Handler creates StandupConversation { state=INITIATED }
  ↓
Handler asks: "What did you work on yesterday?"
  → state transitions INITIATED → GATHERING_YESTERDAY (new)
  ↓
User answers (or "skip"/"nothing")
  ↓
Handler stores yesterday StandupItems; checks completion signals
  → state transitions GATHERING_YESTERDAY → GATHERING_TODAY (new)
  ↓
"What's planned for today?"
User answers
  ↓
state → GATHERING_BLOCKERS (new)
  ↓
"Any blockers?"
User answers
  ↓
state → GENERATING
  ↓
LLM generates standup using all 3 parts (#1034 StandupItem-aware)
  ↓
state → FINALIZING → COMPLETE
```

**Persistence on suspend** (escape/timeout):
- Save current `(yesterday[], today[], blockers[])` snapshot to session_data alongside SUSPENDED state
- On resume, replay state + show captured content + ask the next-uncaptured-part's question

---

## Phase 0.7: Conversation Design

**Per-part prompts** (proposed copy, PM Q below):
- Yesterday: "What did you work on yesterday?"
- Today: "What's planned for today?"
- Blockers: "Any blockers or things you need help with?"

**Skip / nothing handling**: User can answer "skip", "nothing", "n/a", "no blockers" — accept these as empty for that part and move on.

**Completion signal detection** (heuristic-first, no LLM gate for MVP):
- Explicit "done" / "stop" / "that's all" / "that's it" → finalize early
- All 3 parts captured (any non-empty) → auto-finalize
- "nothing else" / "all good" after blockers → finalize
- Confidence threshold: simple substring/regex match for MVP. LLM-classification deferred to post-MVP.

**Partial persistence on escape**:
- User says "/escape" mid-flow → save what's captured + state machine context → SUSPENDED
- On resume ("standup" again), bot says: "Picking back up — you'd told me [yesterday]: …. What's planned for today?"
- Merge logic: if user resumes and says "actually let me restart yesterday", reset that part only (per-part rerun); fully starting over uses /escape→/standup again.

**Trust gating**: None for MVP — standup is user-initiated; no proactive intervention shifts based on trust. Trust does inform `morning_standup_offer` (#161-related), separately.

---

## Phase 0.8: Post-Completion Verification

- [ ] Manual smoke as user:
  - Full flow yesterday→today→blockers, completion auto-detect → standup generates
  - Skip-each-part flow → empty parts handled gracefully
  - "/escape" mid-flow → resume picks up correctly
  - Timeout mid-flow → resume picks up correctly
  - Multi-line input per part → stored as multiple StandupItems
- [ ] CI tests pass; no regression on existing standup tests
- [ ] #889 bug fixes still working (escape, timeout, suspend resume)

---

## Phase 1: State machine extension

**Files**:
- `services/shared_types.py` — extend `StandupConversationState` enum:
  ```python
  GATHERING_YESTERDAY = "gathering_yesterday"
  GATHERING_TODAY = "gathering_today"
  GATHERING_BLOCKERS = "gathering_blockers"
  ```
  (Keep existing GATHERING_PREFERENCES for backward compat / discovery flow; document its different role.)

- `services/standup/conversation_manager.py` — extend `VALID_TRANSITIONS` with the new states + transitions:
  - INITIATED → GATHERING_YESTERDAY (default new flow) | GATHERING_PREFERENCES (legacy preference-flow path)
  - GATHERING_YESTERDAY → GATHERING_TODAY | SUSPENDED | ABANDONED
  - GATHERING_TODAY → GATHERING_BLOCKERS | SUSPENDED | ABANDONED
  - GATHERING_BLOCKERS → GENERATING | SUSPENDED | ABANDONED
  - Keep all existing transitions intact

**Acceptance**:
- Enum extended without breaking existing imports
- All transitions explicit; invalid transitions raise clear errors
- 12-15 transition tests covering each new arrow

**Estimate**: 1.5 hr

---

## Phase 2: Per-part prompting + storage

**Files**:
- `services/standup/conversation_handler.py` — main flow logic. Add per-part:
  - prompt-text emission on entering each new state
  - capture handler that parses user reply into StandupItems
  - skip/nothing detection per-part
  - automatic transition to next state
  - hook into `StandupConversation.partial_capture` (new field on the conversation model)

- `services/standup/conversation_manager.py` (or a new `services/standup/standup_conversation.py`) — the in-memory conversation model needs three list fields:
  ```python
  @dataclass
  class StandupPartialCapture:
      yesterday: List[StandupItem] = field(default_factory=list)
      today: List[StandupItem] = field(default_factory=list)
      blockers: List[StandupItem] = field(default_factory=list)

      def is_complete(self) -> bool: ...  # any non-empty across all 3
      def is_empty(self) -> bool: ...  # all empty (used for "user hit escape immediately")
  ```

**Acceptance**:
- Per-part prompts emitted in correct sequence
- StandupItems parsed from user replies (mirror #1034 parsing)
- Skip/nothing detected case-insensitively for "skip", "nothing", "n/a", "no", "no blockers"
- 12-15 tests covering each part-prompt/capture/skip flow

**Estimate**: 3 hr

---

## Phase 3: Enhanced completion detection

**Files**:
- `services/standup/completion_detector.py` (new, ~80 LOC) — pure decision function

```python
@dataclass
class CompletionSignal:
    is_complete: bool
    reason: str  # "explicit_done" | "all_parts_captured" | "natural_signal" | "structural_full" | None

def detect_completion(
    *,
    user_message: str,
    capture: StandupPartialCapture,
    current_state: StandupConversationState,
) -> CompletionSignal: ...
```

**Detection rules (MVP, regex-based)**:
- Explicit done: `\b(done|stop|that's (it|all)|finish(ed)?|complete)\b`
- Natural completion: `\b(nothing else|all good|no more|that's everything)\b`
- Structural: `current_state == GATHERING_BLOCKERS and any non-empty parts captured`

**Acceptance**:
- 15-20 tests covering positive matches + negatives ("done with this thought" should NOT trigger early completion when user is mid-yesterday-capture)
- Pure function; easy to unit test

**Estimate**: 2 hr

---

## Phase 4: Partial persistence + resume

**Files**:
- `services/standup/conversation_handler.py` — on entering SUSPENDED:
  - Serialize `StandupPartialCapture` to session_data (JSON-able dict)
  - Persist current state-name
- On resume:
  - Deserialize partial capture
  - Recreate state machine at the previous state
  - Bot replays "Picking back up — you'd told me…" with captured content
  - Asks the next-uncaptured-part question

**Storage**: Use existing session/conversation persistence layer — `StandupConversation` likely already persists to DB or session-state. If purely in-memory, this issue requires adding persistence (might warrant a Phase 0 spike confirmation).

**Acceptance**:
- "/escape" mid-yesterday-capture → resume → captured yesterday is shown
- "/escape" between today and blockers → resume picks up at blockers
- "/escape" with empty capture → resume re-asks yesterday cleanly
- 8-10 tests covering each scenario

**Estimate**: 2.5 hr

---

## Phase 5: LLM generation integration

**Files**:
- `services/standup/conversation_handler.py` (GENERATING transition) — pass StandupPartialCapture to LLM as structured 3-part input
- Existing standup prompt-template likely needs minor schema adjustment to consume the structured shape (#1034-aware)

**Acceptance**:
- LLM receives structured 3-part input (not freeform blob)
- Output mirrors current standup format (markdown-rendered standup)
- 4-6 tests with mocked LLM verifying the input shape

**Estimate**: 1.5 hr

---

## Phase 6: Tests + verification

**Total target**: ~60 new tests across phases.

**Verification**:
- [ ] `pytest tests/unit/services/standup/ -v` — all passing
- [ ] Pre/post merge regression sweep
- [ ] Manual smoke per Phase 0.8

**Estimate**: 1 hr (mostly falls out of phases 1-5)

---

## Phase Z: Handoff

- [ ] Issue #900 closed with evidence
- [ ] Cross-reference #889 (bug fixes), #888 (escape protocol), #1034 (StandupItem)
- [ ] Session log updated; branch merged; sign-off discipline run

---

## Total Estimate

~12 hours (largest M2e gameplan; involves state machine surgery + new modules + persistence + LLM-prompt schema change).

## Risks

- **Medium**: in-memory vs persisted StandupConversation — Phase 4 persistence may surface that the conversation is currently in-memory only, which would require adding DB persistence (additional ~1-2hr scope). Phase 0 should confirm.
- **Medium**: completion detection false-positives — heuristic regex may match in user replies mid-capture. Tests must cover edge cases ("I'm done writing this part" should not finalize during yesterday).
- **Low**: existing standup tests may need substantial updates — preserve coverage but adapt to new state machine.

## Dependencies

- #889 (bug fixes) ✅ closed
- #888 (escape protocol) ✅ complete
- #1034 (StandupItem) ✅ closed
- All Phase -1 infra ✅

## Audit Cascade Matrix (Issue → Gameplan)

| Template Requirement | Status | Notes |
|---|---|---|
| Issue number referenced | ✅ | #900 |
| Problem statement | ✅ | Freeform → guided 3-part + completion + persistence |
| Phase -1 infra verification | ✅ | All deps verified |
| Phase 0 GitHub investigation | ✅ | Cross-refs to #889, #888, #1034 |
| Phase 0.5 FE-BE contract | ✅ | Multi-turn chat |
| Phase 0.6 Data flow | ✅ | State machine + persistence diagrammed |
| Phase 0.7 Conversation design | ✅ | Per-part copy, completion rules, skip/nothing |
| Phase 0.8 Post-completion verification | ✅ | Smoke list |
| Phases 1-N with estimates | ✅ | 6 phases, ~12 hr total |
| Acceptance criteria per phase | ✅ | All listed |
| Test strategy | ✅ | ~60 tests |
| Phase Z handoff | ✅ | Evidence, cross-refs, sign-off |
| Dependencies listed | ✅ | All closed/complete |
| Risks identified | ✅ | 3 risks |
| File paths cited | ✅ | All grep-able |

### Audit ✅ Items — PM Dispositions (2026-05-03)

**✅ Q1**: Per-part prompt copy. **PM**: "ship then iterate for efficient copy review pass." Workmanlike copy ships in this PR; folded into **#1043** (POST-MVP en-masse copy review).

**✅ Q2**: Completion detection scope. **PM**: "let's include." LLM-gated completion detection added to MVP scope. Phase 3 expands: regex remains as fast-path / fallback; LLM-classifier path with confidence threshold added. **Estimate updated: ~12hr → ~14hr**.

**✅ Q3**: Persistence boundary. **PM**: "proceed and discover - if you agree?" Lead Dev agreed. Phase 0 verifies whether StandupConversation persistence exists. If in-memory only, **STOP-and-ask** at that point: add DB persistence within #900 vs split into pre-work issue (consistent with split-related-issues memory).

**✅ Q4**: Backward compat. **PM**: "ok to keep." Keep `GATHERING_PREFERENCES` legacy path; rip later if unused.

**✅ Q5**: Default flow. **PM**: "confirm." `INITIATED → GATHERING_YESTERDAY` is default; quick-mode preference flag deferred to post-MVP.

### Updated total estimate

~14 hours (from ~12; added ~2 hr for LLM-gated completion detection per Q2).
