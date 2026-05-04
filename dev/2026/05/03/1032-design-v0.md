# #1032 MUX-INSIGHT-PUSH — Phase 0 Design v0

**Date**: 2026-05-03
**Author**: Lead Developer
**Status**: Phase 0 deliverable per gameplan; PM + CXO review GATING for Phase 1
**Spec source**: `docs/internal/design/mux/insight-surfacing-rules.md` §"Push Mode" (D4)
**PM audit dispositions**: 2026-05-03 walkthrough (commits `6487a2a1`, `94a23ae5`, `7d119232`)

---

## Summary

Push-mode is the most constrained insight-surfacing mode: Piper proactively surfaces an insight without user request, **only at Trust Stage 3+**, with multi-axis gating (confidence + relevance + cooldown + mute + user availability). This document captures concrete decisions for each design lever before implementation, per Q1 disposition (Phase 0 design output is itself a deliverable subject to PM + CXO review).

**Architectural framing**: per Q5 disposition, eligibility logic is **channel-agnostic** — the same gate-evaluation produces a structured payload that an in-chat renderer consumes for MVP, and a future system-push channel (mobile/website OS notification) can reuse with its own renderer.

---

## D4 Push-Mode Prerequisites (verbatim from spec)

All five must be met:

1. Trust level: Stage 3 or higher
2. Insight confidence: 0.75 or higher
3. Relevance to current context: High
4. Time since last push: 24+ hours
5. User availability: Not in focus/DND mode

Plus the spec's 5 Push-Mode Rules:

- Interruptibility — must be dismissable with single action
- Explanation available — "Tell me more" always offered
- No repeated pushes — same insight not pushed twice
- No urgency language — never "urgent" or "important"
- Graceful decline — "Not now" is fine, no follow-up guilt

---

## Decision 1: Trust Gate — strict + stability window (Q7 hard gate)

**Decision**: Stage 3+ is a hard gate. Trust-read errors → NO Push (fail-safe, NOT default-allow).

**Implementation**:
- Read `TrustComputationService.get_trust_stage(user_id)` inside `is_eligible_by_trust(user_id)`
- Return `True` only if stage ≥ TrustStage.ESTABLISHED (3)
- Catch any exception → return `False` (fail-safe; logged as `trust_read_error`)
- Stability window: stage must have been Stage 3+ for ≥ N hours before Push fires (defends against just-promoted users seeing immediate Pushes that feel surprising). N = **2 hours** for MVP (configurable via `PIPER_PUSH_STAGE_STABILITY_HOURS` env, default 2).

**Tests** (negative-assertion is mandatory):
- Stage 1, 2 → `is_eligible_by_trust` returns False
- Stage 3, 4 (within stability window) → returns False
- Stage 3, 4 (past stability window) → returns True
- Trust-read raises → returns False (fail-safe)

---

## Decision 2: Context-Relevance Scoring — Q2 Option B (tag overlap baseline)

**Decision**: Use `learning.applies_to_entities` + `topic_tags` + `context_tags` overlap with conversation context. Score formula:

```
relevance_score =
    2 × (count of entity overlap with insight.applies_to_entities)
  + 1 × (count of topic overlap with insight.topic_tags)
  + 1 × (count of context-tag overlap with insight.context_tags)
```

Threshold for "high relevance" (per D4): score ≥ **3** (configurable via `PIPER_PUSH_RELEVANCE_THRESHOLD`, default 3).

**No embeddings**, no vector similarity — per Q6 disposition, embeddings are an enforced STOP (would require infrastructure not in scope for #1032). If Phase 0 design surfaces that tag-overlap is insufficient, escalate to PM rather than unilaterally adding embeddings.

**Source of context**: pull from `FloorContext.intent_category` + `intent_action` + any extracted entities/topics from `domain_context`. For MVP, entities/topics extracted via the same simple keyword extraction as #1030's `extract_context()` — reuse rather than duplicate.

**Tests**:
- Synthetic insight + low-overlap context → score below threshold → no push
- High-overlap context → score above threshold → push eligible (subject to other gates)
- Empty context entities/topics → score = 0 → no push (no spurious surfacing)

---

## Decision 3: Right-Moment Timing Rules

**Initial conservative rule set** (per Q3 disposition):

| Rule | Default | Tunable via |
|---|---|---|
| Anti-spam: minimum interval between pushes (per session) | 30 minutes | `PIPER_PUSH_MIN_INTERVAL_MINUTES` |
| Per-insight cooldown | 24 hours since `last_surfaced` | (existing on `SurfaceableInsight.is_surfaceable`) |
| Skip during decline state | True | (FloorContext.denial_mode check) |
| Skip during onboarding flow | True | (FloorContext check) |
| Conversation-pause heuristic ("only at pauses ≥ 5s since last user msg") | **DEFERRED** to Post-MVP | (would require timing-state tracking) |

**Per the gameplan**: conversation-pause heuristics may be deferred. For MVP we trust that the floor LLM's `respond` path is a natural-enough boundary — Push attaches to the response wrapper, not mid-stream during user input.

**Tests**:
- Last push < 30 min ago → no push (anti-spam)
- Insight has `last_surfaced` < 24h ago → `is_surfaceable` returns False (existing dataclass logic)
- `denial_mode=True` → no push
- All gates pass → push eligible (subject to relevance/trust)

---

## Decision 4: Mute Granularity — Q4 A+B (session + per-insight dismiss)

**Decision**: For MVP, two mute axes — both volatile in different ways:

1. **Session mute** (volatile): user says "don't surface insights for this conversation" or similar NL → no Push for the rest of the session. State lives in `SurfacingContext.session_mute_active = True` (per-session in-memory). When session ends, mute resets.
2. **Per-insight dismiss** (persistent): existing — `SurfaceableInsight.user_response = "dismissed"` → never surfaced again; `is_surfaceable()` already enforces.

**Out of scope for MVP** (per Q4 disposition):
- Topic-level mute ("don't surface insights about deadlines")
- Indefinite mute-all
- Mute-via-UI affordance (NL-only for MVP)

**NL trigger detection** for session mute:

```python
SESSION_MUTE_TRIGGERS = [
    r"\b(don'?t|stop|no more|hold off on|silence)\s+(insights?|learnings?|suggestions?|surfac\w*|push\w*|reflect\w*)\b",
    r"\bmute\s+(insights?|learnings?|suggestions?)\b",
    r"\b(not now|hold off|hold up).*\binsights?\b",
    r"\bquiet (the|those|all)\s+(insights?|learnings?|suggestions?)\b",
]
```

**Tests**:
- NL trigger detected → `session_mute_active = True`; subsequent push attempts return None
- Per-insight dismiss → `is_surfaceable` False; future push attempts skip
- Mute via dismissed insight does NOT mute other insights

---

## Decision 5: Surfacing Channel — Q5 Option A in-chat + channel-agnostic eligibility

**Decision**: For MVP, in-chat is the ONLY channel; eligibility logic is channel-agnostic so future system-push (mobile/website OS notification) reuses the same decision pathway.

**Architecture**:

```
maybe_push(ctx) → Optional[FramedPushPayload]
              │
              └─ Channel-agnostic eligibility (trust + relevance + timing + mute + retrieval)
                 returns structured payload OR None

Channel renderers (consume FramedPushPayload):
  - Phase 6 in-chat: floor composer appends to its response
  - Future system-push: mobile/website OS UI (out of #1032 scope)
```

**`FramedPushPayload`** structure (the channel-agnostic contract):

```python
@dataclass
class FramedPushPayload:
    insight_id: str
    framed_text: str  # Already passed through frame_insight_for_surfacing (#1033 guardrail)
    mute_affordance: str  # Text for the dismiss/mute UI element
    explain_affordance: str  # Text for the "Tell me more" / explanation control
```

**For #1032 MVP**: floor composer (`ConversationalFloor.respond`) optionally calls `maybe_push(ctx)` after generating its main response. If a payload returns, append it to the response text with a separator + the affordance text.

**Format per D4 §Push Format**:

```
{floor's normal response to user}

---

{framed_text}

{mute_affordance} {explain_affordance}
```

---

## Decision 6: Mid-Implementation STOP (Q6 enforced)

**Hard rule**: if implementation reveals Phase 0 decisions need infrastructure not in scope (especially embeddings for relevance scoring), STOP and surface to PM. Do NOT unilaterally expand scope.

Tripwires:
- Tag-overlap relevance scoring produces too many false positives → STOP, propose embeddings as separate issue
- Trust-read latency too high to fit Push gating in floor-response budget → STOP, propose caching strategy as separate issue
- Conversation-pause heuristic surfaces as required (not deferrable) → STOP

---

## Probe Set Design (Q7 + gameplan Phase 8)

20 probes covering:

| Stage × Insight × Right-moment | Expected verdict |
|---|---|
| Stage 1 + relevant insight + right-moment | NO PUSH (trust gate) |
| Stage 2 + relevant insight + right-moment | NO PUSH (trust gate) |
| Stage 3 + 0 relevant insights + right-moment | NO PUSH (no candidates) |
| Stage 3 + relevant + within stability window | NO PUSH (stability) |
| Stage 3 + relevant + past stability + right-moment | PUSH |
| Stage 3 + relevant + within anti-spam window | NO PUSH (anti-spam) |
| Stage 3 + relevant + session muted | NO PUSH (mute) |
| Stage 3 + dismissed insight + right-moment | NO PUSH (per-insight dismiss) |
| Stage 4 + relevant + right-moment | PUSH |
| Trust-read error | NO PUSH (fail-safe) |

Probe set lives at `tests/mux/probes/push_mode_probes.json`. Negative assertions (Stage 1+2 NEVER → no push) are MANDATORY CI gates per Q7.

---

## Phase order (no change from gameplan)

- **Phase 1**: Phase 0 design review by PM + CXO (this document)
- **Phase 2**: trust-gate + stability check
- **Phase 3**: right-moment + anti-spam
- **Phase 4**: relevance scoring + retrieval (calls existing `InsightJournal.get_unsurfaced`)
- **Phase 5**: mute affordances (NL trigger detection + session-mute state)
- **Phase 6**: in-chat surfacing channel (floor composer integration)
- **Phase 7**: anti-surveillance verification (#1033 guardrail confirmed protecting Push output)
- **Phase 8**: probe set + canonical scenarios (negative-assertion CI gates mandatory)
- **Phase Z**: handoff + #707 tracker update

---

## Out of scope (Post-MVP / future issues)

- Topic-level mute
- Indefinite mute-all
- UI affordance for mute (NL-only for MVP)
- Conversation-pause heuristics
- System-push channel (mobile/website OS notification)
- Embedding-based relevance scoring
- Trust-stage caching for latency

---

## Decisions snapshot for Phase 1 implementation

| Lever | MVP value | Env var |
|---|---|---|
| Trust gate | Stage 3+ hard | (n/a; spec-fixed) |
| Trust stability window | 2 hours | `PIPER_PUSH_STAGE_STABILITY_HOURS` |
| Confidence floor | 0.75 | `PIPER_PUSH_MIN_CONFIDENCE` |
| Relevance threshold | 3 | `PIPER_PUSH_RELEVANCE_THRESHOLD` |
| Anti-spam interval | 30 min | `PIPER_PUSH_MIN_INTERVAL_MINUTES` |
| Per-insight cooldown | 24 hours | (existing on dataclass) |
| Mute granularity | session + per-insight | (n/a) |
| Surfacing channel | in-chat (Q5 Option A) | (n/a) |
| Trust-read failure mode | NO PUSH (fail-safe) | (n/a; hard rule) |
