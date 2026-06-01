# R4: Suggestion-Provenance Tracking — Design (Option d, proper)

**Author**: Lead Developer (with discovery+synthesis workflow `wf_b382f529-e9a` — 4 agents, 18 suggestion sources mapped, 6 risks identified)
**Date**: 2026-06-01 ~06:55 PT
**Status**: DRAFT — awaiting PM ratification on 4 asks before implementation
**Issues**: closes #1030 R4 AC ("Why did you suggest that?" cites informing insight); generalizes to whole floor

## Architecture decision

**Dual-surface, source-declarative capture**:
1. `FloorResponse.provenance: Dict[str, Any]` — populated at the moment context is fed to the LLM (not after the LLM responds)
2. `ConversationContext.turn_provenance: dict[UUID, dict[str, Any]]` sidecar — survives the 10-turn / 30-min window for "why did you suggest that?" lookups

**Why source-declarative, not LLM-declared**:
- LLM citations would hallucinate IDs we never gave it
- Post-hoc inference (parse response for entity matches) is lossy + brittle
- Source-declarative is honest: we capture what we GAVE the LLM. "Why did you suggest X?" gets "I had your 2pm meeting, three open todos, and #1089 blocked — I drew on those." Truthful, even if the LLM didn't explicitly cite each one.

**Storage tiers**:
- In-memory sidecar (30-min/10-turn window) → O(1) lookup, zero DB cost
- Optional promotion to existing `ConversationTurnDB.turn_metadata` JSONB — no Alembic migration

## "Why did you suggest that?" intent

New pre-classifier pattern set `PROVENANCE_PATTERNS` placed BEFORE `TRUST_PATTERNS` (since `\bwhy did you\b` already partially matches TRUST). Narrow verb-list (mention/bring/suggest/recommend/surface/raise/flag), NOT generic ("do" stays with TRUST).

New `IntentCategory.PROVENANCE` + action `explain_suggestion`. CANONICAL handler `ProvenanceHandler` looks up `conv_context.get_last_turn_provenance()` and formats colleague-voice citation. Deterministic lookup, NOT routed through floor.

## 18 suggestion sources mapped

The audit found 18 distinct gather paths in `context_assembler.gather_context()` that feed `domain_context` keys the floor renders. Top sources by surface area:

- insight-pull, insight-push (recent #1030/#1032 work)
- next-meeting, next-free-block, time-available (calendar)
- pending-todos, completed-todos
- blocked-items, active-milestones, recent-activity (GitHub + Slack)
- user-projects, user-priorities, urgent-items
- trust-profile, conversation-history-summary, capabilities, active-integrations

Each gets a per-key provenance entry: `{source, identifier, fetch_timestamp, optional URL}`.

## Estimate

**21 hours across 10 steps.** Larger than my initial 6-10 estimate — the proper-version surface is bigger than I scoped. Two-day calendar realistically with regression sweeps.

| Step | Hours |
|---|---|
| 1. Add PROVENANCE category + action enums | 0.5 |
| 2. Pre-classifier PROVENANCE_PATTERNS with precedence | 1.5 |
| 3. `turn_provenance` sidecar on ConversationContext | 1.5 |
| 4. FloorContext + FloorResponse extensions | 2.5 |
| 5. ContextAssembler per-gatherer provenance metadata | 3 |
| 6. Thread provenance through 3 floor callsites | 2.5 |
| 7. ProvenanceHandler in canonical_handlers.py | 3 |
| 8. Push-mode insight provenance + selection-reason | 1.5 |
| 9. Tests (5 test files, unit + integration) | 4 |
| 10. Telemetry + observability | 1 |

## Risks

**R1 — Pre-classifier collision with TRUST/MEMORY.** `\bwhy did you\b` is partially matched by existing TRUST `\bwhy did you (do|just|go ahead)\b`. *Mitigation*: PROVENANCE_PATTERNS check FIRST; narrow verb-list (mention/suggest/recommend, not "do"); regression test on disambiguation edges.

**R2 — Provenance sidecar unbounded growth.** *Mitigation*: `_prune_old_turns()` extended to drop provenance in lockstep; size assertion (~2KB JSON/turn cap).

**R3 — Multi-source dedup invisibility.** `recent_activity` silently de-dupes Slack DM vs mention. *Mitigation*: `dedup_decisions` field on provenance entry; ProvenanceHandler surfaces when relevant.

**R4 — Persistence opportunism.** ConversationTurnDB persistence isn't systematic today; cross-session provenance silently misses. *Mitigation*: document in-memory window as the v1 contract; flag as PM ask (Q1).

**R5 — LLM coverage drift.** If a new gather key is added to context_assembler but not to `_format_domain_context`, provenance silently ghosts. *Mitigation*: registry refactor (`_DOMAIN_CONTEXT_FORMATTERS: Dict[str, Callable]`); architectural-test assertion that gatherer↔formatter↔provenance triangle is complete (methodology-37 cousin).

**R6 — Push-mode parallel timing.** Push appends AFTER main floor response. *Mitigation*: two-phase sidecar write (floor response provenance first, then push_insight merged in).

## Oversight-audit synthesis (PM "scan for other similar oversights" ask)

The discovery agent flagged STATUS/PRIORITY handlers + PremonitionService as Pattern-073 candidates. **Cross-reference shows both are wrong**:

- **STATUS/PRIORITY**: not dead code. `intent_service.py:10628-10640` explicitly routes them through Action Gate to `_handle_floor_with_context()` (Issue #911 Phase 2). The "CANONICAL" disposition label in `action_registry.py:52-54` is misleading — actual dispatch is FLOOR via Action Gate.
- **PremonitionService**: `frame_insight_for_surfacing` IS used in production (`push_mode.py:436-438`). Some class methods may be unused; class-level "dead" is wrong.

**Disposition recommendation**:
- (a) Push back on Survey 2's findings — file:line counter-evidence above
- (b) File one discovered-work issue for **`ActionDisposition` naming clarity** (~30min fix, low priority) — perhaps split CANONICAL into CANONICAL_HANDLER vs CANONICAL_REGISTERED_BUT_FLOOR_ROUTED, OR add explicit comment
- (c) File a narrow audit task for PremonitionService method-level usage (not class-level "dead") before any removal

Better characterized as Pattern-062 (synthesis-without-cross-reference) on the audit's part than Pattern-073.

## PM asks

**Q1 — Cross-session provenance in v1 scope?** Current recommendation: in-memory only (30-min/10-turn window). Cross-session lookup is opportunistic via existing `turn_metadata` JSONB; not guaranteed. If users will ask "why did you mention X three days ago?" we'd need separate workstream to make turn persistence systematic. Adds ~6-8 hrs. **Default**: defer to follow-up; in-memory contract is enough for MVP.

**Q2 — ProvenanceHandler reply format**:
- (a) Terse: "Drawing on: calendar, 3 todos, #1089"
- (b) **Colleague-prose**: "When I mentioned that, I was drawing on your 2pm meeting with Maria and the three open blockers in piper-morgan-product as of this morning" *(recommended)*
- (c) Integration-source explicit: "via Google Calendar"

Recommend (b) with optional (c) attribution when user pushes further. Worth a sample read before lock-in.

**Q3 — Provenance for canonical-handler paths?** Floor-only for v1 (one capture surface in `respond()`) is simpler. Canonical handlers (PORTFOLIO/TEMPORAL/GUIDANCE/CONVERSATION) have deterministic responses where provenance would be largely tautological ("because you asked"). **Default**: floor-only for v1, file canonical-handler provenance as follow-up.

**Q4 — Oversight-audit disposition?** Per above: push back on Survey 2's two findings with counter-evidence; file ONE clarity issue (ActionDisposition naming); file ONE targeted audit for PremonitionService method-level. **Default**: this is the recommendation.

## Implementation order

Step 1 → 2 → 3 → 4+5 in parallel → 6 (integration) → 7 → 8 (parallel with 7) → 9 (continuous) → 10. Step 9 (tests) gets written incrementally as each step lands, not at the end.

PM ratify the 4 asks → I start Step 1 → daylight today + tomorrow lands the work. Honest landing target: tomorrow EOD if R4 (proper) is the only substantive engineering this session.

## Cross-references

- `dev/active/insight-pull-push-implementation-design-2026-05-31.md` — yesterday's R1-R5 design (for shape)
- Workflow synthesis: `wf_b382f529-e9a` (transcript dir in run logs)
- `services/intent_service/conversational_floor.py:618-684` — primary integration point
- `services/intent_service/context_assembler.py:115-188` — gather_context exit
- `services/intent_service/conversation_context.py:82-108` — sidecar location
- `services/intent_service/pre_classifier.py:670+` — PROVENANCE_PATTERNS placement
- `services/database/models.py:1157-1215` — ConversationTurnDB.turn_metadata JSONB reuse
- `feedback_omnibus_source_drift` memory pin — Pattern-062 synthesis-without-cross-reference (applied to the audit findings)
