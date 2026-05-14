# #1021 USER-HISTORY-LAYER-3 — Phase 0 audit

**Issue**: [#1021](https://github.com/mediajunkie/piper-morgan-product/issues/1021) — UserHistoryService Layer 3 (long-term memory) has no DB backend
**Source**: Architect's Apr 27 batch-4 review (Finding XI)
**Date**: 2026-05-14

---

## Pattern-067 verdict: NEGATIVE

Body claims fully verified against current code. This is genuinely "designed but unimplemented architectural layer" — different shape from #1019 (inert scaffolding) and #1010 (misleading placeholders).

### Verification

| Body claim | Verified |
|---|---|
| `services/memory/user_history.py` 443 LOC | ✅ |
| `UserHistoryService` class at line 286 | ✅ |
| `UserHistoryRepository` ABC at line 103 | ✅ |
| `InMemoryUserHistoryRepository` is sole concrete impl, marked test-fixture | ✅ |
| `workspace_memory.py:204` calls `search_history()` | ✅ (line 204 confirmed) |
| `context_assembler.py:341` attempts `get_history_summary()` (method doesn't exist) | ✅ (now line 393; method genuinely absent from UserHistoryService — confirmed via grep) |
| No DB-backed `UserHistoryRepository` implementation | ✅ (no entries in `repositories.py`; no `services/database/repositories/user_history_repository.py`) |
| No `ConversationSummaryDB` / `ConversationDetailDB` models in `database/models.py` | ✅ |

### Latent bug status (was "folded into #1012")

**#1012 is CLOSED** but its title — "Small dead-code sweep — phantom import, unused tracker, stub provider, enum cosmetics" — suggests the get_history_summary bug was NOT actually addressed there.

Verified: the call at `context_assembler.py:393` still fires. The whole block is wrapped in try/except (lines 384-401) that catches the resulting AttributeError + logs a warning. **The `persistent_memory` context field NEVER gets populated.** Pattern-045: MEMORY-category queries silently get no historical context, despite the code path implying they should.

Plus: line 391 creates a **fresh `InMemoryUserHistoryRepository()` per call**. So even if `get_history_summary` existed, every call sees an empty repo (process-local, not session-persistent). The in-memory design isn't even being exploited at the per-process level.

---

## Live impact

What MEMORY category queries actually get today (e.g., "do you remember what we talked about?"):
- `_gather_memory_context` fires
- Conversation-context-in-memory portion may succeed (lines 358-381, separate)
- UserHistoryService portion silently fails (AttributeError swallowed)
- Floor receives `conversation_history_summary` if session has turns; never receives `persistent_memory`

So Layer 3 contributes zero to current user experience. The 443 LOC of design + the in-memory repo + the service class are all latent — they exist but don't produce value because (a) no DB backend and (b) the integration call points at a non-existent method.

PDR-002 "adaptive greetings" promise ("It's been a while — last time you were working on X") **does not function** today. Single-session memory works (Layer 1); cross-session memory does not.

---

## Three paths, with honest cost + product implications

### Path A — Build it (Architect's prescribed approach)

Per Architect's body breakdown: **~4-6 days of work**.

- Phase 1 (1-2 days): schema design for `conversation_summaries` + `conversation_details` tables; retention policy; read patterns
- Phase 2 (2-3 days): Alembic migration; `DBUserHistoryRepository`; container wiring; SQLAlchemy models; tests
- Phase 3 (1 day): resolve the `get_history_summary` latent bug; wire memory audit trail (sibling to #1018)

**Product implication**: ADR-054 Layer 3 becomes real. PDR-002 adaptive greetings become possible. Memory audit trail extends across sessions.

**Today-cost**: 4-6 days, definitely multi-session. Not a today-shippable scope.

### Path B — Remove

Delete `UserHistoryService`, the ABC, `InMemoryUserHistoryRepository`, the workspace_memory.py:204 caller, the context_assembler.py:383-401 try/except block, the test file (`tests/unit/services/memory/test_user_history.py`).

**Cost**: ~1-1.5 hr.

**Product implication**: Backs off ADR-054 Layer 3 commitment. PDR-002 adaptive greetings dropped from MVP scope. The 443 LOC of design work is lost (would need to rebuild from scratch if revisited).

**Honest framing**: today's behavior is effectively "no Layer 3 anyway" (silently broken), so the user-experience delta is zero. But the architectural commitment is real and visible in ADRs.

### Path C — Scope-clarify + defer build

Today's small fix:
1. Fix the `get_history_summary` latent bug: add a no-op stub method returning `None` so the AttributeError stops firing (or fix the call site to not call a method that doesn't exist)
2. File a designed-feature follow-up issue: "BUILD-USER-HISTORY-DB-BACKEND" with explicit Architect-prescribed phases + ACs
3. Close #1021 as scope-reframed (this issue was the discovery; the new issue is the real build)

**Cost**: ~30-45 min (latent bug fix + follow-up issue + audit notes).

**Product implication**: Preserves ADR-054 Layer 3 commitment + the existing design work. Real build deferred until product roadmap calls for it. Layer 3 stays "designed, not implemented" — explicit + honest, not silently broken.

Same shape as **#1080 NOTION-WRITE**, **#1089 KG-PRIVACY-FILTER**: placeholder honest about what it does (or doesn't); real work filed with explicit trigger conditions.

---

## Recommendation: Path C, conditional on roadmap

If Layer 3 is on the MVP/1.0 roadmap → **Path A** is the only honest answer; commit to the 4-6 day build now or in a near-term sprint
If Layer 3 is post-1.0 → **Path C** scope-clarification is the right move; the existing design survives, the build lands when needed
If Layer 3 has been informally dropped → **Path B** removal is honest; clean break

**The actual question for PM**: where does cross-session memory sit on the roadmap?

(I don't have visibility into product/roadmap intent at that level. PDR-002 implies Layer 3 is part of the vision but doesn't commit a date. The Janus memory research items #972-976 are research-phase. The Architect filing tone — "P3, architectural-cleanup, not blocking" — suggests Layer 3 isn't currently load-bearing.)

### My read

Going by signal alone:
- Architect's framing ("designed but unimplemented architectural layer") implies they want it preserved
- 443 LOC of completed design + ABC + in-memory impl + tests is real investment
- The deferred-build path (C) preserves all that work at near-zero cost
- If Layer 3 becomes load-bearing for 1.0 testing or alpha feedback, the build issue activates with full Architect-prescribed phases ready

**Recommend Path C** unless PM signals Layer 3 is needed for near-term value. Path A is the right answer in a sprint where adaptive-greetings/cross-session memory is the prioritized feature.

---

## Suggested gameplan (conditional on Path C)

- **Phase 1** (~5 min): worktree setup
- **Phase 2** (~15 min): fix the `get_history_summary` latent bug — cleanest fix is to remove the broken call block in `context_assembler.py:383-401` since it's been silently failing and contributing zero. Leave a tombstone comment referencing the new build issue.
- **Phase 3** (~10 min): file `BUILD-USER-HISTORY-DB-BACKEND` follow-up issue with Architect's full Phase 1/2/3 breakdown + ACs
- **Phase 4** (~5 min): update #1021 description per close-issue-properly skill
- **Phase 5** (~10 min): merge + close

**Total**: ~45 min for Path C.

---

## Risks

1. **PM reads Path C as "we're abandoning Layer 3"**: it's not — the code survives; the build issue is filed; the trigger is roadmap signal. But it could read that way without explicit framing. Mitigation: be explicit in commit + closure comment.
2. **Future PM reads context_assembler.py and asks "where's the persistent_memory wiring?"**: the tombstone comment + #XXXX link makes the answer findable.
3. **If PM later wants Path A**: zero rework — the follow-up issue is the same scope Architect described.

---

## Audit-cascade Phase 0 self-check

| Template requirement | Status |
|---|---|
| Issue number referenced | ✅ #1021 |
| Pattern-067 check | ✅ NEGATIVE (body accurate; this is real designed-but-unimplemented work) |
| Body-vs-reality | ✅ all claims verified |
| Existing infra mapped | ✅ user_history.py + workspace_memory caller + context_assembler latent bug + missing DB layer |
| Scope questions | ✅ A/B/C with roadmap-conditional framing |
| Risk assessment | ✅ scope-misread + future-find-cost + rework-cost-if-A-later |
| Recommended path | ✅ C conditional on roadmap; A if Layer 3 is MVP-load-bearing |

---

## STOP — awaiting PM disposition on Layer 3's roadmap position + A/B/C

The audit is complete. The PM-decision-point is product-shaped, not engineering-shaped: where does cross-session memory sit on the roadmap?

— Lead Developer, 2026-05-14
