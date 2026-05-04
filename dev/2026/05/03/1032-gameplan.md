# Gameplan: #1032 MUX-INSIGHT-PUSH (longer-pole)

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/1032
**Author**: Lead Developer (Claude Code Opus)
**Date**: 2026-05-03
**Template version**: gameplan-template v9.3
**Status**: Draft — pending audit-cascade against template + PM Phase -1 walkthrough
**Blocked by**: #1035 MUX-COMPOSTING-ACTIVATION + #1033 MUX-COMPOSTED-EXPERIENCE
**Recommended**: #1030 MUX-INSIGHT-PULL lands first (establishes patterns Push will reuse)

**Longer-pole reminder (per issue body)**: this is the heaviest of the three insight-surfacing modes. Trust-stage gate is load-bearing. Context-relevance scoring + "right moment" timing are design-heavier than implementation-heavier. CEO directed all three modes stay in MVP; if M2 closes without Push fully landing, scope rolls naturally to MVP-tail or Fast Follow.

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status** (from spike + this gameplan-prep read):

- [x] `InsightJournal.get_unsurfaced(user_id, min_confidence, trust_stage, limit) → List[SurfaceableInsight]` (`services/mux/composting_pipeline.py:219`) — **this is the Push-mode query method**. Filters by `is_surfaceable(trust_stage)` (which checks `min_trust_stage >= 1` and 24-hour cooldown and "not dismissed") + minimum confidence + sorts by `requires_attention` then confidence
- [x] `SurfaceableInsight.is_surfaceable(trust_stage)` already implements the trust gate (line 70-94)
- [x] `SurfaceableInsight.min_trust_stage` defaults to 1 — meaning by default insights surface to all stages. Push must enforce additional gate that `trust_stage >= 3` regardless of insight's `min_trust_stage`.
- [x] `TrustComputationService.get_trust_stage(user_id) → TrustStage` is wired
- [x] `frame_insight_for_surfacing(insight) → str` (#1033 framing layer)
- [x] After #1033: `assert_no_surveillance_phrasing` guardrail
- [x] `SurfaceableInsight.surfaced_count` + `last_surfaced` track surfacing history; 24-hour cooldown built into `is_surfaceable`
- [x] `SurfaceableInsight.user_response` ("engaged" / "dismissed" / "corrected") tracks user reaction
- [x] **NO existing surfacing channel**: Push mode currently has no production code path that surfaces insights to user

**Lead Dev's understanding of the task**:

Push surfaces a relevant insight at a contextually appropriate moment, **only at Trust Stage 3+**, mid-conversation. Without user asking. The work has more **design** than **implementation**:

1. **Trust gate enforcement** (load-bearing): Stage 1-2 NEVER receive Push; trust-read failure defaults to NO Push (fail-safe)
2. **Context-relevance scoring**: when is an insight relevant to the *current* conversation? Spec doesn't fully specify; phase-0 design pass needed
3. **"Right moment" timing**: not interrupting; not too often; not repeat-surfacing — heuristics needed
4. **Mute affordances**: per-insight, per-topic, per-conversation, indefinite — design decision
5. **Surfacing channel**: through floor LLM response composer, OR separate channel — design decision
6. **Anti-surveillance enforcement**: leverages #1033's guardrail

This is acknowledged as the heaviest of the three modes. Phase-0 design output is itself a deliverable.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

- [x] Multi-component (trust gate + relevance scoring + timing + mute + surfacing channel + tests)
- [x] Task duration ~10-15 hours total (heavy phase-0 + implementation phases)
- [ ] Multi-agent — no
- [x] Exploratory — significantly: design-pass output may reframe scope

**Assessment**: **USE WORKTREE** — branch `claude/1032-insight-push` based on #1035 / #1033 (and ideally after #1030 lands).

### Part B: PM Verification Required

Questions for PM:

1. **Phase-0 design output as deliverable**: this issue's phase-0 design pass output (a working doc covering scoring/timing/mute/surfacing-channel decisions) IS itself a deliverable, separately reviewable. **Confirm**: phase-0 doc gets PM + CXO review *before* phase-1 implementation begins. If design surfaces are too speculative, file a "design-spike" issue and re-scope #1032.
2. **Context-relevance scoring approach**:
   - **Option A**: vector similarity on `learning.expression` vs current conversation context
   - **Option B**: topic/entity tag overlap (existing `get_for_context` shape extended)
   - **Option C**: simple keyword overlap with floor LLM domain context
   - **Option D**: combination
   **My lean**: **Option B** for MVP (no new embeddings infrastructure); revisit with Option A in Post-MVP if relevance is poor. Option B uses existing `learning.applies_to_entities` + `topic_tags`.
3. **Right-moment timing rules** — what conditions must hold to fire Push?
   - **Min**: trust_stage >= 3, ≥1 unsurfaced relevant insight, no Push fired in last N minutes (anti-spam)
   - **Possibly**: not in middle of user dictation / multi-turn flow / decline state
   - **Possibly**: only at conversation pauses (longer than M seconds since last user message)
   **My lean**: phase-0 designs the rule set; for MVP, conservative gates (high min interval, only after at least one full user turn) + tunable.
4. **Mute granularity**:
   - **Option A**: simple "mute insights for this conversation" → no Push for rest of session
   - **Option B**: mute-this-insight (specific insight not surfaced again)
   - **Option C**: mute-this-topic
   - **Option D**: indefinite mute-all
   **My lean**: A + B for MVP. Topic-level + indefinite are Post-MVP.
5. **Surfacing channel**:
   - **Option A**: through `ConversationalFloor` response composer — Piper's regular response is augmented with a Push-insight paragraph
   - **Option B**: separate channel — Push is a distinct message bubble in chat
   **My lean**: **Option A** for MVP — keeps Push integrated into Piper's voice rather than appearing as a separate notification.
6. **Mid-implementation STOP per issue body**: "If phase 0 design surfaces that context-relevance scoring needs an embedding service or other infrastructure not yet in scope, STOP and surface to PM — do not unilaterally expand scope." Confirm this is an enforced STOP, not a "judgment call" condition. **My lean**: enforced STOP.
7. **Acceptance "Stage 1+2 NEVER receive Push"**: how strictly tested? Negative-assertion tests that mock Stage 1-2 + verify zero Push emissions over a probe set. **Confirm**: this is a hard gate; trust-read errors default to NO Push (fail-safe per spec).

### Part C: Proceed/Revise Decision

- [ ] **PROCEED through Phase 0 design pass** — pending PM Q1-Q7 + #1035 / #1033 / (recommended) #1030 merges
- [ ] **REVISE** — Phase 0 design output may itself reframe scope; that's expected
- [ ] **CLARIFY** — Q2 scoring approach is the longest pole

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**: `gh issue view 1032`

2. **Verify gating dependencies**:
   ```bash
   gh issue view 1035 | grep -i state
   gh issue view 1033 | grep -i state
   gh issue view 1030 | grep -i state    # recommended but not strict
   ```

3. **Read source spec deeply**:
   - [ ] `docs/internal/design/mux/insight-surfacing-rules.md` §"Push Mode" end-to-end
   - [ ] `docs/internal/design/mux/learning-visibility-spec.md` (D1) — Stage 3+ visibility matrix
   - [ ] `docs/internal/design/mux/composting-experience-design.md` (D3) — anti-surveillance rules carry over
   - [ ] ADR-053 Trust Computation
   - [ ] `docs/internal/architecture/current/lifecycle-experience-guide.md`

4. **Codebase Investigation**:
   ```bash
   # Inventory of existing Push-mode references (sanity check)
   grep -rn "push_mode\|Push.*Insight\|maybe_surface\|surface_insight" services/ tests/

   # Verify get_unsurfaced consumers (likely none in production yet)
   grep -rn "get_unsurfaced" services/

   # Verify trust-stage transition events (do we know when stage advances?)
   grep -rn "trust_stage_advanced\|stage_changed" services/trust/
   ```

5. **Phase 0 design pass output** (`dev/.../1032-design-v0.md`):
   - Context-relevance scoring (Q2 Option B baseline + concrete scoring formula)
   - Right-moment rules (Q3 set — explicit conditions; min interval value; anti-spam constraints)
   - Mute granularity scheme (Q4: A+B baseline)
   - Surfacing channel (Q5: Option A — augment floor response composer)
   - Trust gate enforcement (Q7: hard gate + fail-safe)
   - Probe set design (~15-20 scenarios across Stage 1-4 + with/without relevant insights)

6. **Update GitHub Issue**:
   ```
   ## Status: Investigation Started
   - [ ] Phase 0 design v0 doc filed
   - [ ] PM + CXO review of design doc
   - [ ] Probe set design v0
   ```

### STOP Conditions

- Phase 0 surfaces need for embedding service or other infrastructure not in scope → STOP per issue body + Q6
- D4 / D1 read reveals constraints not in this gameplan → re-scope
- Trust-stage advancement events aren't observable → may need infra to know when Stage 3 just-reached (or accept polling)

---

## Phase 0.5: Frontend-Backend Contract Verification

### Applicability assessment

**Marginal** — Push mode integrates into existing chat conversation channel (per Q5 Option A lean). No new endpoints; the contract is the response shape that includes a Push-insight paragraph when the gate fires.

**Question for PM**: confirm marginal-applicability framing.

### Required Actions

1. **Document target output shape** (Q5 Option A):
   ```
   [Existing Piper response to the user's message...]

   --- (visual separator? formatting decision in design)

   Having had some time to reflect, [framed insight from frame_insight_for_surfacing].
   Want me to flag this earlier next time?

   [Mute UI affordance — text "Mute insights for this conversation" with action]
   ```

2. **Mute affordance UI**: existing chat UI doesn't have per-message mute. Phase-0 design includes:
   - Inline link/button in the Push-insight paragraph
   - OR slash-command / natural-language detection ("don't surface insights for this conversation")
   - **My lean**: BOTH for MVP — natural-language mute via floor LLM detection; inline UI affordance secondary

### STOP Conditions

- Mute affordance design unworkable in current chat UI → file UI follow-up

---

## Phase 0.6: Data Flow & Integration Verification

### Applicability assessment

**Applies** — multi-layer: trust check → relevance scoring → timing check → InsightJournal → frame → response composer.

### Part A: Data Flow Requirements

| Layer | Needs change? |
|-------|---------------|
| New service `services/mux/push_mode.py` | ✅ NEW — orchestrates the gates |
| `TrustComputationService.get_trust_stage` | No change |
| Trust-gate enforcement in `push_mode.maybe_push` | ✅ NEW — strict Stage 3+ |
| Relevance scoring helper | ✅ NEW — per Q2 Option B |
| Right-moment timing helper | ✅ NEW — per Q3 |
| `InsightJournal.get_unsurfaced` | No change |
| Mute state tracking | ✅ NEW — per-session in conversation context (volatile); per-insight in `SurfaceableInsight.user_response = "muted"`-ish (persistent) |
| Floor LLM response composer | ✅ MODIFY — when Push fires, augment response with framed-insight paragraph |
| Anti-surveillance guardrail | leverages #1033 |
| `mark_surfaced` after Push fires | ✅ — record `user_response = "surfaced"` then update on user reaction |

### Part B: Integration Points Checklist

| Caller | Callee | Verification |
|--------|--------|--------------|
| `IntentService` / `ConversationalFloor` | `push_mode.maybe_push(ctx) -> Optional[FramedPushPayload]` | NEW |
| `maybe_push` | `TrustComputationService.get_trust_stage` | Existing |
| `maybe_push` | `right_moment_check(ctx, last_push_at)` | NEW helper |
| `maybe_push` | `is_muted(session_id, user_id)` | NEW helper |
| `maybe_push` | `score_relevance(insights, ctx)` | NEW |
| `maybe_push` | `InsightJournal.get_unsurfaced` | Existing |
| `maybe_push` | `frame_insight_for_surfacing` | #1033 |
| Floor composer | `maybe_push` result → augmented response | NEW |

### Part C: Pattern Adaptation Notes

#1004 ETHICS-ACTIVATE pattern: probe-set + canonical scenarios + LLM behavior tests + boundary enforcement. Adopt directly.

**Pitfalls**:
1. **Stage advancement**: when does a user transition Stage 2 → Stage 3? `TrustComputationService` does this on signals; Push must not fire on the *first* Stage-3 query (premature). Phase 0 specifies "Stage 3 must hold for at least N hours" or similar.
2. **Cooldown vs anti-spam**: the existing `is_surfaceable(trust_stage)` 24-hour cooldown is per-insight. Push-mode anti-spam is per-conversation (don't push 5 insights in a row even if 5 different insights are unsurfaced). Implement both.
3. **Mute vs decline**: distinguish "muted for session" from "user dismissed THIS insight" — different behaviors. Mute-session = no more pushes this session; dismiss-this-insight = `user_response = "dismissed"`, never resurface.
4. **Trust-read failure fail-safe**: per Q7 lean, trust-read error → NO Push (not a default-allow). Test this explicitly.
5. **Surfacing-language constraint**: per #1033, no surveillance phrasing. Push output goes through `frame_insight_for_surfacing` which calls the guardrail.

### STOP Conditions

- Phase 0 design produces concrete rules but they're untestable → re-design
- Trust-read latency too high (Push has tight latency budget if it runs mid-response) → consider caching trust stage in FloorContext

---

## Phase 0.7: Conversation Design

### Applicability assessment

**Applies STRONGLY** — Push IS conversational; the framing rules + mute flow are conversation-design.

### Part A: Happy Path

```
Turn 1:
  User: "I'm thinking about the deadline for next sprint..."
  Piper: "[Existing response addressing the question]

         Having reflected on your last few sprints, you tend to front-load
         smaller tasks. This one might fit that pattern — want me to flag
         the early-completion path?

         (Mute insights for this conversation)"
  State: PUSH_FIRED

Turn 2 (user engaged):
  User: "Yeah good catch, mark this one as front-loadable."
  Piper: [normal response] [InsightJournal.mark_surfaced("engaged")]

Turn 2 (user dismissed):
  User: "No, this one's different."
  Piper: "Got it." [InsightJournal.mark_surfaced("dismissed")]

Turn 2 (user muted session):
  User: "Don't surface insights for this conversation."
  Piper: "Sure, I'll hold off." [session-level mute set]

Turn 3+ (within muted session):
  User: <any message>
  Piper: [normal response, NO Push fires]
```

### Part B: Edge Cases

| User Input / State | Expected Behavior |
|---|---|
| User at Stage 1 / Stage 2 + relevant insights exist | NO Push (hard gate) |
| User at Stage 3 + 0 relevant insights | NO Push |
| User at Stage 3 + relevant + last Push <N min ago | NO Push (anti-spam) |
| User at Stage 3 + relevant + already muted session | NO Push |
| Trust-read error | NO Push (fail-safe) |
| User says "watching me?" or surveillance-suggesting | This is a #1004 boundary trigger / decline territory; not a Push trigger |
| Push-insight contains forbidden phrasing (would happen post-#1033) | Block via guardrail; log violation; fall back to no Push |

### Part C: Pattern Definitions

```python
SESSION_MUTE_TRIGGERS = [
    r"\b(don'?t|stop)\s+(surface|suggest|push)\s+(insights?|learnings?)\b",
    r"\bmute\s+insights?\b",
    r"\bnot now,?\s+thanks\b",
]
INSIGHT_DISMISS_TRIGGERS = [
    r"\b(no|not relevant|not this time)\b",
    # detected in immediate response after Push fires
]
```

### Part D: State Machine

```
ROUTINE
  [Stage 3+ + relevant + right-moment + not-muted]
    → PUSH_FIRED
  [else]
    → ROUTINE

PUSH_FIRED (next turn classified)
  [user engages]    → ROUTINE; mark "engaged"
  [user dismisses]  → ROUTINE; mark "dismissed" (no resurface)
  [user mutes session] → ROUTINE_MUTED; session-level mute set
  [user ignores]    → ROUTINE; mark "surfaced" only

ROUTINE_MUTED (rest of session)
  [any input]       → ROUTINE_MUTED (no Push regardless)
  [explicit "ok unmute"] → ROUTINE
```

### STOP Conditions

- Trigger-pattern false-positive rate too high on Phase 0 probe → revise
- Conversation flow conflicts with existing floor semantics → coordinate

---

## Phase 0.8: Post-Completion Integration

### Applicability assessment

**Applies** — Push fires alter `surfaced_count` + `user_response`.

### Side Effects

| Side Effect | Verified? |
|---|---|
| `InsightJournal.mark_surfaced(insight_id, response)` after Push | ✅ test |
| Per-session mute state | ✅ in conversation context |
| Per-insight dismiss persisted | ✅ via existing `user_response` |

### Downstream Behavior

| Feature | Before Push fired | After Push fired |
|---|---|---|
| Same insight | Surfaceable | NOT surfaceable for 24h (existing cooldown) |
| Subsequent Pulls (#1030) | Returns insight | Still returns it (Pull is unaffected by Push surface) |
| Subsequent Push attempts | Eligible | NOT eligible (24h cooldown) |

---

## Phases 1-N: Development Work

(Per CEO direction: longer-pole; phase-0 design output may reframe.)

### Phase 1: Phase 0 design pass review

**Work**:
- [ ] Phase 0 design doc reviewed by PM + CXO
- [ ] Any reframes folded back; if scope expands materially, file follow-up issues

**Bookend**: comment on #1032 with link to design doc + review status.

### Phase 2: Trust-gate + fail-safe

**Work**:
- [ ] `push_mode.is_eligible_by_trust(user_id) -> bool`:
  - Reads `TrustComputationService.get_trust_stage`
  - Returns True if Stage 3+
  - Returns False on any exception (fail-safe)
- [ ] Stage-stability check (per Phase 0.6 pitfall #1): user must be at Stage 3+ for ≥N hours

**Tests**:
- [ ] Stage 1, 2, 3, 4 — only 3+4 return True
- [ ] Trust-read raises → returns False
- [ ] Just-promoted-to-Stage-3 (within stability window) → False

### Phase 3: Right-moment + anti-spam

**Work**:
- [ ] `push_mode.right_moment(ctx: FloorContext, last_push: Optional[datetime]) -> bool`
- [ ] Anti-spam: configurable min interval between Pushes (e.g., 30 min in same session)
- [ ] Conversation-state checks (e.g., not in decline state, not in onboarding)

**Tests**:
- [ ] Time-based interval enforcement
- [ ] State-based gating

### Phase 4: Relevance scoring + retrieval

**Work** (per Q2 Option B baseline):
- [ ] Extend or wrap `InsightJournal.get_unsurfaced` with context-relevance scoring
- [ ] Use `ctx.intent_category`, `ctx.intent_action`, and any extracted entities/topics from the floor's domain context
- [ ] Score insight by `applies_to_entities` overlap + `topic_tags` overlap
- [ ] Threshold: minimum relevance score below which Push doesn't fire

**Tests**:
- [ ] Synthetic insight set with varying relevance → scoring is monotonic in overlap
- [ ] Low-relevance below threshold → no Push

### Phase 5: Mute affordances

**Work** (per Q4 A+B):
- [ ] `push_mode.is_session_muted(session_id) -> bool` (volatile state)
- [ ] Session-mute trigger detection in floor (NL: "don't surface insights for this conversation" etc.)
- [ ] Per-insight dismiss already supported via `user_response = "dismissed"`
- [ ] Mute affordance UI link (if Q4 includes UI; lean: NL-only for MVP)

**Tests**:
- [ ] NL trigger detection
- [ ] Session-muted = no Push fires
- [ ] Per-insight dismiss = no resurface

### Phase 6: Surfacing channel integration (Q5 Option A)

**Work**:
- [ ] Floor composer calls `push_mode.maybe_push(ctx) -> Optional[FramedPushPayload]` after generating response
- [ ] If payload non-None, append to response with separator + framed insight + mute affordance
- [ ] Anti-surveillance guardrail (#1033) wraps the framed insight before output
- [ ] `InsightJournal.mark_surfaced(insight_id, "surfaced")` called when Push fires

**Tests**:
- [ ] Floor with Push payload → augmented response
- [ ] Floor without Push payload → unchanged response
- [ ] mark_surfaced is called exactly once per Push fire

### Phase 7: Anti-surveillance integration

Already covered by #1033's framing layer; this phase verifies the guardrail catches any LLM-generated surveillance phrasing in the Push paragraph specifically.

- [ ] Test: probe set covering "what could induce surveillance phrasing in a Push" — verify all probes pass

### Phase 8: Probe set + canonical scenarios

**Work**:
- [ ] ~15-20 probe scenarios crossing:
  - Stage 1, 2, 3, 4 × insights present / absent × right-moment / wrong-moment
- [ ] Scenarios in `tests/mux/probes/push_mode_probes.json`
- [ ] CI runs probe set

**Tests**:
- [ ] All probes assert correct gate behavior (no Push for Stage 1-2 ever)

### Phase 2a: Routing integration tests (REQUIRED — this involves classifier work)

- [ ] Pre-classifier integration test for session-mute trigger detection
- [ ] Floor composer integration test for Push payload augmentation

### Phase 2b: Wiring integration tests (REQUIRED)

- [ ] End-to-end at Stage 1: 0 pushes ever
- [ ] End-to-end at Stage 4 + relevant insight + right-moment: Push fires; mark_surfaced called
- [ ] End-to-end with NL session mute: Push gates close
- [ ] End-to-end trust-read failure: Push gates close (fail-safe)

### Phase 9: Manual verification

- [ ] Browser scenarios with mocked trust stages 1-4
- [ ] Stage 4 with real insight, observe Push integration in chat
- [ ] Mute via NL, verify Push gate closes for rest of session

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **GitHub Final Update**:
   ```
   ## Status: Complete - Awaiting PM Approval

   - Phase 0 design v0 reviewed + folded
   - Trust gate (Stage 3+ hard gate + stability) enforced
   - Right-moment + anti-spam rules enforced
   - Relevance scoring (Q2 Option B baseline)
   - Mute (Q4 A+B): NL session-mute + per-insight dismiss
   - Surfacing channel (Q5 Option A): floor composer augments
   - Anti-surveillance guardrail integrated
   - Probe set (Stage × insight × right-moment) passes
   - Trust-read fail-safe verified
   ```

2. **Documentation**:
   - [ ] Phase 0 design doc cross-referenced
   - [ ] D4/D1/D3 spec cross-referenced

3. **Evidence Compilation**:
   - [ ] Test output (Phases 2-8)
   - [ ] Probe-set output (most especially the negative assertions: Stage 1-2 zero pushes)
   - [ ] Browser screenshot of Push fire at Stage 4
   - [ ] git diff

4. **Handoff**:
   - [ ] Update #707 tracker: `[x] #1032 MUX-INSIGHT-PUSH`
   - [ ] M2d gate: all four insight modes complete (#1030/#1031/#1032/#1033)

5. **Session log** complete

6. **PM Approval Request** standard

---

## Multi-Agent Coordination Plan

Single agent (Lead Dev). Heavy, multi-component, design-heavy.

### Verification Gates

- [ ] Phase 0: design doc reviewed
- [ ] Phase 1: design folded
- [ ] Phase 2: trust gate tests pass
- [ ] Phase 3: right-moment + anti-spam tests pass
- [ ] Phase 4: relevance scoring tests pass
- [ ] Phase 5: mute tests pass
- [ ] Phase 6: surfacing-channel integration tests pass
- [ ] Phase 7: anti-surveillance verification
- [ ] Phase 8: probe set passes (especially negative-assertion Stage 1-2 → zero Pushes)
- [ ] Phase 2a: routing integration tests pass
- [ ] Phase 2b: end-to-end wiring tests pass
- [ ] Phase 9: manual verification complete

---

## STOP Conditions

- #1035 / #1033 not merged
- Phase 0 design surfaces need for embedding service (per issue body) → STOP
- Trust-read latency too high
- Stage 1-2 Push fires in any test (hard fail; treat as P0 bug)
- Probe-set negative assertions fail → block

---

## Evidence Requirements

- Phase 0 design doc + PM/CXO review record
- Test output for Phases 2-8 + 2a + 2b
- Probe-set output (positive + negative)
- Browser screenshots
- git diff

---

## Effort Estimate

**Overall Size**: Large (~10-15 hours, longer-pole acknowledged)

| Phase | Estimate |
|-------|----------|
| Phase -1 PM walk | 30 min |
| Phase 0 design pass + spec read | 3 hr |
| Phase 1 design review | 30 min |
| Phase 2 trust gate | 1 hr |
| Phase 3 right-moment + anti-spam | 1.5 hr |
| Phase 4 relevance scoring | 2 hr |
| Phase 5 mute affordances | 1 hr |
| Phase 6 surfacing channel | 2 hr |
| Phase 7 anti-surveillance verify | 30 min |
| Phase 8 probe set | 1.5 hr |
| Phase 9 manual + Phase Z | 1 hr |

If Phase 0 design surfaces material expansion → re-scope. CEO direction: rolls to MVP-tail / Fast Follow if M2 closes first.

---

## Dependencies

- [ ] #1035 must merge
- [ ] #1033 must merge
- [ ] (Recommended) #1030 lands first to establish patterns
- [x] InsightJournal.get_unsurfaced exists
- [x] TrustComputationService.get_trust_stage wired
- [x] Floor LLM + FloorContext

## Blocks

- M2d gate completeness; #707 tracker

---

# Audit-Cascade: Gameplan vs gameplan-template v9.3

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Phase -1: Infrastructure Verification | ✅ | Spike + push-specific helpers; seven PM Qs |
| Phase -1: Worktree Assessment | ✅ | USE WORKTREE based on #1035/#1033 |
| Phase -1: PM Verification placeholder | ⚠️ | Seven Qs queued |
| Phase 0: GitHub Issue Verification | ✅ | Step + dependency-verification |
| Phase 0: Spec read deeply (D4/D1/D3 + ADR-053) | ✅ | Five spec docs flagged |
| Phase 0: Design pass output as deliverable | ✅ | Design doc filed at `1032-design-v0.md` |
| Phase 0: Codebase Investigation | ✅ | grep steps |
| Phase 0: Update GitHub Issue | ✅ | Status template |
| Phase 0: STOP Conditions | ✅ | Three named (incl. issue-body STOP) |
| Phase 0.5: Applicability | ⚠️ | Marked **marginal**; **PM approval requested** |
| Phase 0.5: Output shape documented | ✅ | Augmented chat response shape |
| Phase 0.5: Mute affordance UI | ✅ | NL + UI both considered |
| Phase 0.5: STOP Conditions | ✅ | One named |
| Phase 0.6: Applicability | ✅ | Applies (multi-layer) |
| Phase 0.6: Data Flow Requirements | ✅ | 11-row layer table |
| Phase 0.6: Integration Points | ✅ | Caller→callee table |
| Phase 0.6: Pattern Adaptation Notes | ✅ | #1004 pattern; five pitfalls |
| Phase 0.6: STOP Conditions | ✅ | Two named |
| Phase 0.7: Conversation Design | ✅ | Applies STRONGLY; happy path + edge cases + patterns + state machine |
| Phase 0.8: Post-Completion Integration | ✅ | Applies; side-effects + downstream tables |
| Phases 1-N: Development with progressive bookending | ✅ | Phases 1-9 + 2a + 2b defined |
| Phase 2a: Routing integration tests | ✅ | Applies — classifier work; tests specified |
| Phase 2b: Wiring integration tests | ✅ | Four end-to-end tests (incl. negative-assertion + fail-safe) |
| Phase Z: GitHub Final Update | ✅ | Template included |
| Phase Z: Documentation Updates | ✅ | Design doc + spec cross-refs |
| Phase Z: Evidence Compilation | ✅ | Five evidence items |
| Phase Z: Handoff Preparation | ✅ | #707 tracker + M2d-gate-completion note |
| Phase Z: Session Completion | ✅ | Listed |
| Phase Z: PM Approval Request | ✅ | Template included |
| Multi-Agent Coordination Plan | ✅ | Single-agent justification + complexity acknowledgment |
| Verification Gates | ✅ | Per Phase + negative assertions |
| STOP Conditions (throughout) | ✅ | Section included; issue-body STOP escalation captured |
| Evidence Requirements | ✅ | Listed |
| Effort Estimate | ✅ | Per-phase ~10-15 hr; CEO scope-roll guidance noted |
| Dependencies + Blocks | ✅ | #1035/#1033/#1030 + tracker |
| Test Scope | ✅ | Unit + probe + routing + wiring + manual + negative assertions |

## Action Required Before Proceeding

1. **Phase -1 Qs 1-7** (design-pass-as-deliverable; scoring; right-moment; mute granularity; channel; STOP-strictness; trust-gate strictness)
2. **Phase 0.5 marginal-applicability** confirmation per audit-cascade skill
3. **#1035 + #1033 must merge**; **#1030 recommended first**
4. **Phase 0 design pass output** is itself a deliverable that must pass PM + CXO review before phase 1

## Status

**Audit cascade gate: ✅ PASSED 2026-05-03.** All items resolved via PM walkthrough.

---

# PM Audit Walkthrough Dispositions (2026-05-03)

| # | Question | PM disposition |
|---|----------|----------------|
| Q1 | Phase 0 design pass output as deliverable; PM + CXO review GATING for Phase 1 start? | **100% agree. critical.** Hard gate. If design output is speculative, file a "design-spike" issue and re-scope #1032. |
| Q2 | Context-relevance scoring: vector (A) / tag overlap (B) / keyword (C) / combination (D)? | **Option B — tag overlap baseline** (`applies_to_entities` + `topic_tags`). Phase 0 design validates accuracy; if Option A (embeddings) is needed, trigger explicit STOP-and-surface per issue body. |
| Q3 | Right-moment timing rules — initial conservative set (Stage 3+ + relevance + 30-min anti-spam + not-in-decline)? | **Yes well put.** Phase 0 design owns full rule set; conversation-pause heuristics may be deferred. |
| Q4 | Mute granularity: A+B for MVP (session-mute volatile + per-insight dismiss persistent); C+D deferred? | **Yes — A+B for MVP**. C (topic-level) and D (indefinite) explicitly deferred as "really speculative and overbuilt imho". |
| Q5 | Surfacing channel: in-chat augmented response (A) vs separate channel (B)? Channel-agnostic eligibility for future system-push? | **Option A in-chat for MVP** + holistic UX model includes future system-push channel (mobile/website OS notification). Eligibility logic designed channel-agnostic; future system-push channel reserved, will reuse eligibility logic + add own renderer/templating. |
| Q6 | Embeddings or other unscoped infrastructure: enforced STOP, no judgment call? | **Correct — enforced STOP** |
| Q7 | Stage 1+2 hard gate; trust-read errors → no Push fail-safe; negative-assertion probe tests mandatory CI gates? | **Yes — confirm hard gate** |
| Q8 | Phase 0.5 marginal-applicability confirmation | **Confirmed** |
