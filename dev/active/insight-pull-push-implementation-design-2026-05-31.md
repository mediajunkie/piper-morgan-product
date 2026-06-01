# Insight Pull (#1030) + Push (#1032) — Implementation Design

**Author**: Lead Developer
**Date**: 2026-05-31 ~18:50 PT
**Status**: DRAFT — awaiting PM ratification before implementation starts
**Issues**: #1030 INSIGHT-PULL + #1032 INSIGHT-PUSH (discovered-work trackers: #1135, #1136)
**Parent**: #1047 M2D-UAT — closes Surfaces 2 + 6

## Goal

Wire the existing `InsightRepository` + `services/mux/push_mode.py` capabilities into the conversational floor so chat-side insight pull (user query → insights surface) and chat-side insight push (proactive Stage-3+ surfacing) actually fire. The data layer + repository + push gate logic + unit tests all exist; the missing piece is **integration into `ConversationalFloor.respond`**.

## Architecture (what wires to what)

```
User message
   │
   ▼
intent_service/pre_classifier.py
   │ ├─ NEW: INSIGHT_PULL_PATTERNS (regex) → route to pull handler
   │ └─ (existing patterns)
   ▼
intent_service dispatch
   │
   ▼
ConversationalFloor.respond(ctx)
   │ ├─ NEW: if pull-mode triggered → handle_insight_pull(ctx)
   │ │       → InsightRepository.list_for_user(user_id) → format response
   │ │
   │ └─ existing response generation
   │     │
   │     ▼  (after primary response composed)
   │     NEW: maybe_push(ctx) → FramedPushPayload | None
   │            │
   │            ▼
   │     if payload: append to response
   ▼
final response to user
```

Both flows consume `InsightRepository.list_for_user(user_id)`. Push uses the same repository read inside `maybe_push` (the eligibility logic in `push_mode.py:94-440` already takes the insights as input — we just need to fetch and pass them).

## Scope

### IN scope (this work)

1. **Pre-classifier patterns for pull triggers** (~10 LOC)
   - Phrasings to route to pull handler:
     - "what have you learned (about X)?"
     - "what do you know about X?"
     - "tell me what you've learned"
     - "why did you suggest that?"  → cites informing insight(s)

2. **`handle_insight_pull(ctx)` handler** (~60 LOC + tests)
   - Fetches `InsightRepository.list_for_user(user_id, exclude_deleted=True)`
   - Filters by topic if extracted from query
   - Sections by confidence band (high/medium/low per AC) — uses existing `confidence` field on `SurfaceableInsight`
   - Empty case: honest "nothing learned yet" message (already the floor's behavior; this handler returns that explicitly rather than the generic floor fallback)
   - Composition: format with citations + correction-invitation language per AC

3. **`maybe_push` integration point in `ConversationalFloor.respond`** (~30 LOC)
   - After primary response composed, call `maybe_push(ctx)` with `ctx` containing user_id, current-turn topic-tags, recent insight reads (cooldown), trust_service, session_mute state
   - If `FramedPushPayload` returned, append framed-experience text to response (per `push_mode.py:11` comment: "the in-chat renderer is the only consumer (`ConversationalFloor.respond` appends the payload to its response)")
   - If `None`, no-op

4. **Session-mute state** (~40 LOC + tests)
   - Natural-language detection: "don't surface insights", "stop showing me insights", "no more insights"
   - State location: per-session in `conversational_floor` or session manager (TBD — open Q1)
   - Resets on next session per AC
   - Per-insight dismiss already exists in repository (`surfaced_count`/`dismissed_at` fields per `InsightRepository.update_user_correction` + sibling methods)

5. **Tests** (~150 LOC integration)
   - Pull: real `template.render()` equivalent — POST to `/api/v1/intent` with seeded insights, assert response sections + citations
   - Push: POST series with Stage 1/2/3+ users (using existing test fixtures), assert push only fires for Stage 3+
   - Session-mute: POST mute-utterance, assert subsequent turns get no push, assert next-session reset
   - AAXT scenario coverage (per methodology-37 Coverage-Audit Gate for new dispatch paths)

### OUT of scope (filed as follow-ups if needed)

- System-push channel (mobile/OS notification) — `push_mode.py` is channel-agnostic but only in-chat renderer is implemented; system channel is post-MVP per Q5 disposition
- Embedding-based relevance scoring — explicitly out per Q2 Option B (tag-overlap only)
- Conversation-pause detection — Post-MVP per Q3 disposition
- Multi-language insight surfacing
- Insight Journal nav-link integration (#1134 — separate issue)
- History sidebar (#1133 — separate issue)
- trust_stage hardcode (#1132 — separate issue but affects push gating; see Risk R1)

## AC Mapping

### #1030 INSIGHT-PULL ACs

- [ ] "Ask 'What have you learned about [topic]?' with insights in DB → response sections by confidence (high/medium/low)" → handler IN scope item 2 + 1
- [ ] "Ask 'Why did you suggest that?' → response cites informing insight(s)" → handler item 2 (citation formatting)
- [ ] "Empty-insights edge: no deflection, honest 'nothing learned yet'" → handler item 2 (empty case)
- [ ] "Correction invitation present in all responses" → handler item 2 (composition)

### #1032 INSIGHT-PUSH ACs

- [ ] "Stage 1 user: NEVER receive proactive Push" → existing `maybe_push` Stage-3-gate (line 94+); needs integration point item 3
- [ ] "Stage 2 user: same negative assertion" → same gate
- [ ] "Stage 3+ user: receive contextually relevant Push under spec conditions" → integration item 3
- [ ] "Session-mute via natural language respected for rest of session" → item 4
- [ ] "Session-mute resets on next session" → item 4
- [ ] "Per-insight dismiss preserved" → existing repository support

## Risks + Open Questions

**R1 — `trust_stage` hardcode (#1132).** `web/api/routes/ui.py:380-388` hardcodes `trust_stage = 1`. Push gate requires accurate trust stage. **Implementation order matters**: either fix #1132 first, OR ensure `maybe_push` reads via `trust_service.get_stage(user_id)` directly (which `push_mode.py:94-110` already does — so the route's hardcoded value doesn't affect `maybe_push`'s decision, only the page's server-rendered indicator). **Verify before implementation**: the chat floor's push gate must use the trust service, not the page's hardcoded value. *Likely no blocker, but verify in implementation step 0.*

**R2 — Session-mute state location.** Two options:
  - (a) Per-session dict in conversational floor (lightweight, resets on session end naturally)
  - (b) Redis with session-keyed TTL (cleaner architecturally; matches existing patterns)
  Recommend (a) for MVP; can promote to (b) if multi-process safety needs surface. **PM call welcome.**

**R3 — Pre-classifier regex maintenance burden.** Per Pattern-073 + `feedback_investigate_before_extending_all_work` discipline, regex-based dispatch is fragile (we just shipped #1121 to migrate document-update queries off regex to LLM slot-filling). Should we use LLM-based intent detection for pull triggers instead? **Counter-argument**: LLM call adds 1-2s latency to every turn; pre-classifier is fast-path; the trigger phrasings here are limited (5-7 phrasings). **Recommend**: ship regex for MVP, file follow-up to migrate to LLM-based detection as part of #1124 PRE-FLOOR-HANDLER-AUDIT.

**R4 — Citation format.** "Why did you suggest that?" → cite informing insight(s). Where does Piper know which insights informed the previous suggestion? **Open**: there's no current memory of "I made this suggestion because of insight X." This AC may require additional plumbing (track which insights were consulted during the previous turn). **Recommend**: defer citation-on-suggestion as a separate sub-issue if it needs new infrastructure; ship pull+empty+invitation now.

**R5 — Confidence-band thresholds.** AC says "sections by confidence (high/medium/low)" — what numeric thresholds? `SurfaceableInsight.confidence` is a float 0.0-1.0. Reasonable cuts: high ≥ 0.75, medium 0.5–0.75, low < 0.5. **PM call welcome** or accept this proposal.

## Estimate

- **Item 1 (pre-classifier patterns)**: ~30 min including tests
- **Item 2 (handle_insight_pull)**: ~2-3 hours including handler + composition + tests + manual smoke
- **Item 3 (maybe_push integration)**: ~1-2 hours (small integration point + tests; the hard work is already in `push_mode.py`)
- **Item 4 (session-mute)**: ~2 hours including NL detection + state + tests
- **Item 5 (integration tests)**: ~1-2 hours
- **R-buffer (R1 verification, R4 deferral filing, R5 confirmation)**: ~30 min

**Total: ~7-10 hours of focused engineering.** Distributable over 1-2 sessions. Faster than my original "1-2 days" estimate (the existing `push_mode.py` work shrinks the push side; the handler is the bulk).

## Test strategy

Per the new `feedback_ui_fix_requires_template_render_test_not_curl_200` discipline pin:

- Each new path gets a **real consumer-trace test**, not just unit-level
- Pull: `POST /api/v1/intent` with seeded `InsightRepository` data for m1-test user; assert response contains sections + citations + correction-invitation
- Push: same shape, with Stage 3+ user fixture; assert payload appended
- Negative push: Stage 1 + Stage 2 users; assert no payload (don't trust the unit test alone — verify the integration point doesn't accidentally call push when it shouldn't)
- Session-mute: positive + reset test
- **Pre-implementation step**: run `template.render()` or its API equivalent against current `/api/v1/intent` to baseline empty-state response before changes; compare post-change

## Implementation order

1. **Step 0** — Verify R1 (trust_stage routing): does `maybe_push` consult trust_service directly (not the route's hardcoded value)? Read `push_mode.py:94-110` carefully.
2. **Step 1** — Pre-classifier patterns + test
3. **Step 2** — `handle_insight_pull` + test (incl. empty-state)
4. **Step 3** — `maybe_push` integration in floor + test (Stage gating)
5. **Step 4** — Session-mute + test
6. **Step 5** — Full integration smoke + browser walkthrough with PM as m1-test user

## Deferred / discovered-work to file post-implementation

- R4 citation-on-suggestion infrastructure (if needed)
- LLM-based pull-intent detection migration (part of #1124 audit)
- Mobile/OS push channel (post-MVP)

## Cross-references

- #1030, #1032 (the surfaces being implemented)
- #1135, #1136 (discovered-work trackers)
- #1047 (parent UAT)
- #1031 (sibling — already shipped; structural template for the journal page)
- #1132 (R1 dependency — trust_stage hardcode)
- `services/mux/push_mode.py` (the existing eligibility logic)
- `services/database/repositories.py:2071-2200` (InsightRepository)
- `services/intent_service/conversational_floor.py` (integration point)
- `services/intent_service/pre_classifier.py` (where pull triggers route)
- `docs/internal/design/mux/insight-surfacing-rules.md` (D4 spec)
- `feedback_ui_fix_requires_template_render_test_not_curl_200` (test discipline pin)

## Asks for PM

1. Greenlight to start implementation per this design? (Single yes/no; the audit + design ground this concretely.)
2. R2: session-mute storage — accept (a) per-session dict for MVP?
3. R5: confidence-band cuts — accept high ≥ 0.75, medium 0.5–0.75, low < 0.5?
4. R4: defer citation-on-suggestion to follow-up issue (if it needs new tracking infrastructure)?

Ready to start step 0 on your go.
