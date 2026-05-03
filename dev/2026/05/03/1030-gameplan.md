# Gameplan: #1030 MUX-INSIGHT-PULL

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/1030
**Author**: Lead Developer (Claude Code Opus)
**Date**: 2026-05-03
**Template version**: gameplan-template v9.3
**Status**: Draft — pending audit-cascade against template + PM Phase -1 walkthrough
**Blocked by**: #1035 MUX-COMPOSTING-ACTIVATION + (recommended) #1033 MUX-COMPOSTED-EXPERIENCE for the framing layer

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status** (from spike + this gameplan-prep read):

- [x] `InsightJournal.get_for_context(user_id, context_entities, context_topics, trust_stage, limit) → List[SurfaceableInsight]` exists (`services/mux/composting_pipeline.py:273`) — **this is the Pull-mode query method**. Already does relevance scoring (entity/topic overlap with insight's `applies_to_entities` / `topic_tags` / `context_tags`); sorts by relevance + confidence.
- [x] After #1035: `InsightJournal` is durable; `get_for_context` reads from `InsightRepository`.
- [x] `frame_insight_for_surfacing(insight) → str` (`services/mux/premonition.py:66`) returns reflection-framed string. After #1033: framing layer enforces anti-surveillance guardrail.
- [x] **Floor LLM entry point**: `ConversationalFloor.respond(ctx: FloorContext) → FloorResponse` (`services/intent_service/conversational_floor.py:562`)
- [x] `FloorContext` carries `user_message`, `session_id`, `user_id`, `conversation_history`, `trust_stage`, `intent_category`, `intent_action`, `domain_context` — all the inputs Pull-mode trigger detection needs
- [x] **Pre-classifier hint**: `services/intent_service/pre_classifier.py` is where intent dispatch starts; could intercept Pull queries before floor or alongside
- [x] Trust-stage API: `TrustComputationService.get_trust_stage(user_id)` (`services/trust/trust_computation_service.py:118`)
- [x] **`learning-visibility-spec.md` D1**: per spec, Pull works at ALL 4 stages (no trust gate); the implementation must read trust stage to verify per-stage behavior is consistent (Stage 1-2 might trim depth; Stage 3-4 full)
- [x] **`insight-surfacing-rules.md` D4 §"Pull Mode"** spec calls out 5 rules:
  - Response completeness (don't withhold)
  - Confidence display (high / medium / "less sure about")
  - Correction invitation always present
  - Scope matching (don't dump unrelated insights)
  - No deflection (if insights exist, share them)

**Lead Dev's understanding of the task**:

When user explicitly asks Piper about its insights/learnings, Piper responds with relevant insights organized by confidence, with always-available correction invitation. The flow:

1. **Trigger detection**: recognize user query as Pull-mode trigger (per spec table: direct query / topic-specific / explanation request / confidence check / source inquiry)
2. **Insight retrieval**: call `InsightJournal.get_for_context` (already exists) with parsed query context
3. **Response composition**: format result per spec (sections by confidence; honest uncertainty markers; correction invitation)
4. **Trust-stage handling**: verify behavior is consistent at Stages 1-4 (per spec: works at all stages)

Existing infrastructure makes this a "wire it up + test the framing rules" feature, not a "build from scratch" feature — assuming #1035 + #1033 are landed.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

- [x] Multi-component (intent detection + retrieval + response composition + tests)
- [x] Task duration ~3-5 hours
- [ ] Multi-agent — no
- [x] Pull-mode response shape needs careful spec-following

**Assessment**: **USE WORKTREE** — branch `claude/1030-insight-pull` based on #1035 / #1033 once those merge.

### Part B: PM Verification Required

Questions for PM:

1. **Trigger detection placement**: where does Pull-mode trigger detection live?
   - **Option A**: as a dedicated intent category (e.g., new `INSIGHT_QUERY` intent) recognized by the pre-classifier or main classifier — heavyweight, but cleanest
   - **Option B**: hint in the floor LLM's system prompt — "if user is asking about your insights/learnings, retrieve from InsightJournal and format per Pull-mode rules"; the LLM decides
   - **Option C**: a hybrid — pre-classifier flags candidate Pull queries; floor LLM decides whether to actually pull
   **My lean**: **Option C** for accuracy + flexibility. The pre-classifier flags "looks like an insight query" via keyword/regex; the LLM verifies + retrieves. Pure-LLM (B) risks invented insights when none exist; pure-classifier (A) is rigid.
2. **Response format strictness**: per spec, response has explicit sections ("**High confidence:**", "**Medium confidence:**", "**Something I'm less sure about:**"). Should that be:
   - **Strict template** — backend formats the markdown blocks; LLM passes through
   - **LLM-generated** — system prompt instructs LLM to follow the format; LLM does the rendering
   **My lean**: **strict template** for the section headers + bullets, but the actual insight expressions are already framed via `frame_insight_for_surfacing` (#1033). Hybrid: backend builds the structured response; LLM optionally adds a one-line conversational wrapper at top/bottom.
3. **"No deflection" rule enforcement**: if insights exist for the topic, response is non-empty. Test-side guardrail: if matching insights count > 0 → assert response contains insight text. If no matching insights, response says so honestly ("I haven't noticed anything specific about that yet").
4. **Context extraction for `get_for_context`**: how do we extract `context_entities` + `context_topics` from a free-form query? The InsightJournal API expects them but the user just types "what have you learned about deadlines?". Options:
   - **Option A**: rely on the existing intent classifier's entity extraction (if it does this)
   - **Option B**: simple noun-phrase extraction from the user_message via spaCy or regex
   - **Option C**: pass user_message verbatim, extend `get_for_context` to do its own keyword extraction
   **My lean**: **Option C** for now (simpler, single-purpose helper); revisit if accuracy is poor after a probe set is run.
5. **Stage 1-4 behavior consistency check**: spec says Pull works at all stages. Does it have *the same response* at all stages, or progressive depth (e.g., Stage 1 trims confidence detail; Stage 4 shows full)? Spec says "Pull is available at all stages" but doesn't specify whether response varies. **My lean**: identical response at all stages for MVP — simpler + spec-honest. Per-stage variation is a future enhancement.

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** — pending PM Q1-Q5 + #1035 merge + (recommended) #1033 merge
- [ ] **REVISE** — Q1 disposition shapes the work substantially (Option A is ~2x effort)
- [ ] **CLARIFY** — Q4 context-extraction approach affects probe-set design

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**: `gh issue view 1030`

2. **Verify gating dependencies**:
   ```bash
   gh issue view 1035 | grep -i state    # Must be CLOSED
   gh issue view 1033 | grep -i state    # Recommended: CLOSED
   ```

3. **Read source spec**:
   - [ ] `docs/internal/design/mux/insight-surfacing-rules.md` §"Pull Mode" — 5 rules + trigger phrase categories
   - [ ] `docs/internal/design/mux/learning-visibility-spec.md` — Stage 1-4 visibility matrix

4. **Codebase Investigation**:
   ```bash
   # Verify existing Pull-mode-shaped tests/intents (#717 product concept may have related work)
   grep -rn "INSIGHT_QUERY\|learning_query\|insight_pull\|pull_mode" services/ tests/

   # Inventory of InsightJournal.get_for_context consumers
   grep -rn "get_for_context\|get_unsurfaced" services/

   # Verify floor system prompt for any existing insight-related instructions
   grep -n "insight\|learning\|reflection" services/intent_service/conversational_floor.py
   ```

5. **Update GitHub Issue**:
   ```
   ## Status: Investigation Started
   - [ ] #1035 + #1033 merged
   - [ ] D4 Pull-Mode spec re-read; trigger phrase categories + 5 rules confirmed
   - [ ] D1 trust-visibility behavior decided (Q5)
   ```

### STOP Conditions

- #1035 not merged → wait
- D4 spec specifies behavior the existing `get_for_context` doesn't cover → re-scope or extend
- D1 says Pull works only at certain stages → Q5 lean is wrong → adjust

---

## Phase 0.5: Frontend-Backend Contract Verification

### Applicability assessment

**Marginal**: Pull-mode response goes through the existing chat conversation channel, which already renders markdown. No new endpoint, no new template. The "contract" change is the LLM/floor returning a specific markdown structure for Pull responses.

### Required Actions

1. **Document target response format**:
   ```
   Here's what I've noticed about your deadline patterns:

   **High confidence:**
   - You work best with 20% buffer built into timelines
   - External deadlines get prioritized over internal ones

   **Medium confidence:**
   - You tend to front-load effort rather than spread it evenly

   **Something I'm less sure about:**
   - It seems like you prefer to deliver early on smaller tasks but use all available time on larger ones

   Would you like me to explain any of these, or correct something that's off?
   ```

2. **Render verification**: confirm the chat UI renders bold + bullets correctly.

3. **PM approval requested**: confirm marginal-applicability framing.

### STOP Conditions

- Chat markdown rendering missing bold or bullets → fix UI before composing this response shape

---

## Phase 0.6: Data Flow & Integration Verification

### Applicability assessment

**Applies** — multi-layer: pre-classifier hint → floor LLM → InsightJournal → response composition.

### Part A: Data Flow Requirements

| Layer | Needs change? |
|-------|---------------|
| Pre-classifier (intent detection) | ✅ NEW Pull-mode trigger detection |
| `IntentService` / `ConversationalFloor` | ✅ wire trigger result to Pull-handling path |
| Insight retrieval | ✅ `InsightJournal.get_for_context(user_id, entities, topics, trust_stage, limit)` |
| Response composition | ✅ build sectioned markdown per spec |
| Frame helper (#1033) | ✅ each insight expression framed via `frame_insight_for_surfacing` |
| Output to user | Existing channel |

### Part B: Integration Points Checklist

| Caller | Callee | Verification |
|--------|--------|--------------|
| Pre-classifier | Pull-trigger detector | Phase 1 |
| Intent service | InsightJournal.get_for_context | Q4 disposition determines context-extraction shape |
| Pull handler | TrustComputationService.get_trust_stage(user_id) | Already wired |
| Pull handler | frame_insight_for_surfacing | #1033 must be merged |
| Pull handler | Response composer | NEW |

### Part C: Pattern Adaptation Notes

Pull-mode is a new intent-handling shape. Adapt #1004 ETHICS-ACTIVATE pattern: probe set + canonical scenarios + LLM behavior tests.

**Pitfalls**:
1. **Empty insights**: when InsightJournal returns no matches, must NOT deflect (per spec Rule 5). Honest "haven't noticed anything specific yet" is the correct behavior.
2. **Confidence binning**: spec uses "high", "medium", "less sure about" but `SurfaceableInsight.learning.confidence` is a float. Need a binning rule. Lean: high ≥ 0.8, medium 0.6-0.8, low < 0.6.
3. **Trigger false positives**: queries like "I've learned a lot from this" could trigger Pull falsely. Trigger detection must be careful.
4. **Context-extraction quality**: Q4 simple noun-phrase approach may miss context. Probe set will reveal.

### STOP Conditions

- D1 read reveals stage-specific behavior is required (Q5 wrong) → scope expand
- Confidence binning rule disagreement → resolve before Phase 2

---

## Phase 0.7: Conversation Design

### Applicability assessment

**Applies** — Pull-mode IS conversation; multi-turn (user query → Piper response → user follow-up correction/explanation/etc.).

### Part A: Happy Path

```
Turn 1:
  User: "What have you learned about how I handle deadlines?"
  Piper: "Here's what I've noticed about your deadline patterns:
          **High confidence:** ...
          **Medium confidence:** ...
          **Something I'm less sure about:** ...
          Would you like me to explain any of these, or correct something that's off?"
  State: PULL_RESPONDED

Turn 2 (correction):
  User: "Actually no, I don't front-load smaller tasks — I just work them when ready."
  Piper: "Got it, I'll note that. [updates insight]"
  State: PULL_CORRECTION_RECEIVED

Turn 2 (explanation):
  User: "Why did you say I prefer external deadlines?"
  Piper: "I noticed that across [N observations], you completed external-deadline tasks ahead of internal ones."
  State: PULL_EXPLANATION_GIVEN

Turn 2 (none):
  User: "Thanks!"
  State: ROUTINE_CONVERSATION
```

### Part B: Edge Cases

| User Input | Current State | Expected Behavior |
|---|---|---|
| Pull-trigger query when 0 insights exist | ROUTINE | "I haven't noticed anything specific about that yet" — no deflection, honest |
| Vague pull query ("what have you noticed?") | ROUTINE | Use full-context insights; don't ask user to clarify (rule: "no deflection") |
| Pull query at Stage 1 (per Q5 lean: identical response) | ROUTINE | Same response shape as Stage 4 |
| Multiple back-to-back Pull queries | ROUTINE | Each handled independently; no de-duplication needed for MVP |

### Part C: Pattern Definitions

```python
PULL_TRIGGER_PATTERNS = [
    r"\bwhat have you learned\b",
    r"\bwhat have you noticed\b",
    r"\bwhat insights\b",
    r"\bwhy did you (say|suggest)\b",
    r"\bhow confident\b",
    r"\bhave you noticed\b",
    r"\btell me about your (insights|learnings)\b",
]
```

### Part D: State Machine

(Lightweight — Pull-mode is single-response per turn, but follow-up actions are routed to existing handlers — correction → InsightJournal `mark_surfaced(insight_id, "corrected")`; explanation → existing source-inquiry path.)

### STOP Conditions

- Trigger pattern false-positive rate >10% on a 30-query probe → revise pattern set

---

## Phase 0.8: Post-Completion Integration

### Applicability assessment

**Partial**: Pull-mode follow-up actions (correction) DO change state via `InsightJournal.mark_surfaced(insight_id, "corrected")`. So:

| Side Effect | Verified? |
|---|---|
| Corrections persist via InsightJournal | ✅ test |
| Surfaced count increments on each Pull surface | ✅ test |

**Question for PM**: confirm partial-applicability framing.

---

## Phases 1-N: Development Work

### Phase 1: Pull-trigger detection

**Work**:

- [ ] New helper `services/mux/pull_mode.py` (or extension of existing module):
  - `PULL_TRIGGER_PATTERNS` regex list (per Phase 0.7 Part C)
  - `is_pull_trigger(user_message: str) -> bool`
  - `extract_context(user_message: str) -> Tuple[List[str], List[str]]` — returns `(entities, topics)` per Q4 lean (Option C: keyword extraction inside this helper)
- [ ] Wire detection into pre-classifier hint OR floor LLM path (per Q1 disposition)

**Tests**:
- [ ] Unit tests for each trigger pattern + non-triggering control queries
- [ ] Probe set of ~20 queries (10 trigger / 10 non-trigger) verifying detection accuracy

### Phase 2: Pull-mode response composer

**Work**:

- [ ] New service method (location TBD — possibly `services/mux/pull_responder.py`):
  ```python
  async def respond_to_pull(
      user_message: str,
      user_id: str,
      trust_stage: int,
      ...
  ) -> str:
      entities, topics = extract_context(user_message)
      insights = await journal.get_for_context(
          user_id=user_id,
          context_entities=entities,
          context_topics=topics,
          trust_stage=trust_stage,
          limit=10,
      )
      if not insights:
          return "I haven't noticed anything specific about that yet."
      return format_pull_response(insights)
  ```
- [ ] `format_pull_response(insights: List[SurfaceableInsight]) -> str` — bins by confidence, formats sections per spec, calls `frame_insight_for_surfacing` per insight, appends correction invitation

**Tests**:
- [ ] Unit tests with synthetic insight sets across confidence levels
- [ ] Test: empty insight set → honest non-deflection response
- [ ] Test: all-high-confidence insights → only "High confidence" section appears
- [ ] Test: response contains correction invitation

### Phase 3: Wiring into intent service / floor

**Work** (per Q1 Option C lean):

- [ ] Pre-classifier flags `is_pull_trigger` match
- [ ] Intent service routes flagged messages to `respond_to_pull` rather than the default floor path
- [ ] Pull response replaces floor LLM response for Pull-trigger messages

**Tests**:
- [ ] Routing integration test: Pull-trigger message → response from `respond_to_pull`, NOT generic floor LLM response
- [ ] Routing integration test: non-Pull message → existing floor path unchanged

### Phase 4: Trust-stage consistency

**Work** (per Q5 lean: identical response at all stages):

- [ ] Verify trust_stage is read from `TrustComputationService.get_trust_stage(user_id)` and passed to `get_for_context`
- [ ] Tests verifying response shape is identical across Stages 1-4 for the same insight set

### Phase 5: Probe set + canonical scenarios

**Work**:

- [ ] ~20 canonical Pull-trigger queries hand-curated; each with expected response shape (sectioned, contains correction invitation, no deflection)
- [ ] Probe set lives in `tests/mux/probes/pull_mode_probes.json`
- [ ] CI runs probe set against the pull-mode response composer

### Phase 2a: Routing integration tests (REQUIRED — this IS intent/classifier work)

- [ ] Pre-classifier integration test for Pull-trigger detection
- [ ] Intent service routing test
- [ ] Floor-bypass test (Pull queries don't hit generic floor LLM)

### Phase 2b: Wiring integration tests (REQUIRED)

- [ ] End-to-end: Pull query → trigger detected → InsightJournal queried → framed response composed → user-visible
- [ ] End-to-end with empty insights → honest non-deflection
- [ ] End-to-end with anti-surveillance phrasing (test-injected) → guardrail catches it (#1033 dependency)

### Phase 6: Manual verification

- [ ] Browser scenarios across the 5 spec trigger categories (direct query / topic-specific / explanation / confidence check / source inquiry)
- [ ] Stage 1 + Stage 4 manual scenarios verifying identical response shape

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **GitHub Final Update**:
   ```
   ## Status: Complete - Awaiting PM Approval
   - Pull-trigger detection wired (per Q1 disposition)
   - Response composer formats per D4 §"Pull Mode" rules
   - Probe set passes
   - Routing + wiring integration tests pass
   - Trust-stage Q5 behavior verified (identical at all stages)
   - Spec rules 1-5 enforced (completeness, confidence display, correction, scope, no deflection)
   ```

2. **Documentation**:
   - [ ] Code comments cross-reference D4 + D1
   - [ ] Probe-set extension procedure documented

3. **Evidence Compilation**:
   - [ ] Test output (Phases 1-5)
   - [ ] Probe-set output
   - [ ] Browser screenshots of canonical scenarios

4. **Handoff**:
   - [ ] Update #707 tracker: `[x] #1030 MUX-INSIGHT-PULL`
   - [ ] Document patterns reusable by #1031 / #1032

5. **Session log** complete

6. **PM Approval Request** standard

---

## Multi-Agent Coordination Plan

Single agent (Lead Dev). Multi-component but tightly coupled.

### Verification Gates

- [ ] Phase 1: trigger detection passes
- [ ] Phase 2: response composer tests pass
- [ ] Phase 3: routing integration tests pass
- [ ] Phase 4: trust-stage consistency verified
- [ ] Phase 5: probe set passes
- [ ] Phase 6: manual scenarios pass

---

## STOP Conditions

- #1035 not merged → block
- #1033 not merged → block (dependency on framing layer)
- D4 spec gap → resolve
- Pull-trigger false-positive rate too high → revise patterns

---

## Evidence Requirements

- Test output for Phases 1-5
- Probe-set machinery output
- Routing integration test output
- Browser screenshots

---

## Effort Estimate

**Overall Size**: Medium (~4-5 hours)

| Phase | Estimate |
|-------|----------|
| Phase -1 PM walk | 25 min |
| Phase 0 spec read + investigation | 1 hr |
| Phase 1 trigger detection | 45 min |
| Phase 2 response composer | 1 hr |
| Phase 3 wiring | 45 min |
| Phase 4 trust-stage | 15 min |
| Phase 5 probe set | 30 min |
| Phase 6 manual + Phase Z | 30 min |

---

## Dependencies

- [ ] #1035 must merge
- [ ] #1033 must merge (recommended; framing layer)
- [x] InsightJournal.get_for_context exists
- [x] TrustComputationService.get_trust_stage wired
- [x] Floor LLM + FloorContext exist

## Blocks

- #707 tracker completion (parent of #1030)
- M2d gate completeness

---

# Audit-Cascade: Gameplan vs gameplan-template v9.3

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Phase -1: Infrastructure Verification | ✅ | Spike + framing-layer + intent-service inventory; five PM Qs |
| Phase -1: Worktree Assessment | ✅ | USE WORKTREE based on #1035/#1033 |
| Phase -1: PM Verification placeholder | ⚠️ | Five Qs queued |
| Phase 0: GitHub Issue Verification | ✅ | Step included |
| Phase 0: D4 + D1 spec read | ✅ | Required reading |
| Phase 0: Codebase Investigation | ✅ | grep + spec-search steps |
| Phase 0: Update GitHub Issue | ✅ | Status template |
| Phase 0: STOP Conditions | ✅ | Three named |
| Phase 0.5: Applicability | ⚠️ | Marked **marginal**; **PM approval requested** |
| Phase 0.5: Documentation | ✅ | Target response format documented |
| Phase 0.5: STOP Conditions | ✅ | One named |
| Phase 0.6: Applicability | ✅ | Applies (multi-layer) |
| Phase 0.6: Data Flow Requirements | ✅ | 6-row table |
| Phase 0.6: Integration Points | ✅ | 5-row caller→callee |
| Phase 0.6: Pattern Adaptation Notes | ✅ | #1004 pattern; four pitfalls |
| Phase 0.6: STOP Conditions | ✅ | Two named |
| Phase 0.7: Conversation Design | ✅ | Applies (Pull is conversation); happy path + edge cases + patterns + state machine documented |
| Phase 0.8: Post-Completion Integration | ⚠️ | Marked **partial** (corrections persist); **PM approval requested** |
| Phases 1-N: Development with progressive bookending | ✅ | Phases 1-6 + 2a + 2b defined |
| Phase 2a: Routing integration tests | ✅ | Applies — this IS intent/classifier work; three routing tests specified |
| Phase 2b: Wiring integration tests | ✅ | Three end-to-end tests |
| Phase Z: GitHub Final Update | ✅ | Template included |
| Phase Z: Documentation Updates | ✅ | Spec cross-references + probe procedure |
| Phase Z: Evidence Compilation | ✅ | Listed |
| Phase Z: Handoff Preparation | ✅ | #707 tracker + reusable patterns for #1031/#1032 |
| Phase Z: Session Completion | ✅ | Listed |
| Phase Z: PM Approval Request | ✅ | Template included |
| Multi-Agent Coordination Plan | ✅ | Single-agent justification |
| Verification Gates | ✅ | Listed per Phase |
| STOP Conditions (throughout) | ✅ | Section included |
| Evidence Requirements | ✅ | Listed |
| Effort Estimate | ✅ | Per-phase breakdown |
| Dependencies + Blocks | ✅ | #1035/#1033 + tracker |
| Test Scope | ✅ | Unit + probe + routing + wiring + manual |

## Action Required Before Proceeding

1. **Phase -1 Qs 1-5** (trigger placement, response strictness, no-deflection enforcement, context extraction, stage-consistency)
2. **Phase 0.5 marginal-applicability** + **Phase 0.8 partial-applicability** confirmations per audit-cascade skill
3. **#1035 must merge**; **#1033 must merge** (recommended)

## Status

**Audit cascade gate: NOT YET PASSED.** Three ⚠️ items pending PM input. No ❌ items.
