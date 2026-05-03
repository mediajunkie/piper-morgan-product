# Gameplan: #1034 STANDUP-STRUCTURED-WORKITEMS

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/1034
**Author**: Lead Developer (Claude Code Opus)
**Date**: 2026-05-03
**Template version**: gameplan-template v9.3
**Status**: Draft — pending audit-cascade against template + PM Phase -1 walkthrough

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status** (from spike findings + this gameplan-prep read):

- [x] Web framework: **FastAPI** (confirmed `web/api/routes/standup.py` uses `APIRouter`)
- [x] Database: **PostgreSQL via SQLAlchemy async** (not relevant to this gameplan — this is a pipeline shape change, not a schema change)
- [x] Testing framework: **pytest + asyncio** (existing standup tests at `tests/unit/services/features/test_morning_standup*` — to verify in Phase 0)
- [x] Existing endpoints: `POST /api/v1/standup/generate` (`web/api/routes/standup.py:520`)
- [x] Pipeline: `MorningStandupWorkflow.generate_standup()` → `StandupResult` (`services/features/morning_standup.py:45,213`)
- [x] Schema: `StandupResponse` (Pydantic) at `web/api/routes/standup.py:94`

**Lead Dev's understanding of the task**:

The standup pipeline at `services/features/morning_standup.py:213-234` builds string-list outputs:
```python
yesterday_accomplishments.append(f"✅ {commit.get('message', '')}")
yesterday_accomplishments.append(f"📋 {work}")
today_priorities.append(f"🎯 Continue work on {repo}")
```
These flow through the API response to the template as `<li>${item}</li>`. There is no path for a `WorkItem.to_dict()` payload (with `lifecycle_state`) to reach the template.

This issue's job: change the carrier so structured per-item dictionaries reach the API response (and from there the template). Does NOT include wiring the indicator into `standup.html` — that's #704.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

- [ ] Multiple agents will work in parallel — no, single-agent backend change
- [ ] Task duration >30 minutes — yes, ~1-2 hours estimated
- [ ] Multi-component work — partial: workflow + API schema + tests
- [ ] Exploratory/risky changes — moderate: schema change risk
- [ ] Coordination queue prompt — no

**Assessment**:
- [x] **USE WORKTREE** — schema change has rollback value; pre-work for #704 should be on its own branch so #704 can be staged on top.
- Branch: `claude/1034-standup-structured-items`

```bash
cd /Users/xian/Development/piper-morgan/piper-morgan-product
git worktree add ../piper-morgan-product-1034-standup ../piper-morgan-product/.worktrees/1034 -b claude/1034-standup-structured-items main
```

### Part B: PM Verification Required

Questions for PM (please confirm/correct before Phase 0):

1. **Schema change shape (Phase 0 question, repeated here)**: replace string lists with structured dicts (Option 1 in #1034 issue body), or add parallel structured fields (Option 2)? My lean: **Option 1**, since the canonical/slack/json formatters in `services/utils/standup_formatting.py` consume the strings — but if they consume structured items easily, Option 1 is cleaner.
2. **Are there non-test consumers of `StandupResult.yesterday_accomplishments` outside the template + JSON formatter?** If yes, those consumers need migrating in this issue's scope. If no, scope stays small.
3. **Is the "✅" / "📋" / "🎯" emoji prefix part of the contract**, or is it presentation-layer that can move to the formatters? My lean: presentation; should move to canonical/slack/json formatters and standup.html, leaving the structured dict purely data.

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** — pending PM confirmation on questions above
- [ ] **REVISE** — if PM disagrees on Option 1 vs. Option 2 fundamentally
- [ ] **CLARIFY** — if there are non-test consumers I haven't found

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 1034
   ```

2. **Codebase Investigation** (carry results into session log):
   ```bash
   # Find all consumers of StandupResult fields
   grep -rn "yesterday_accomplishments\|today_priorities\|blockers" services/ web/ tests/

   # Find existing standup tests
   find tests -name "*standup*"

   # Identify formatters that consume the string lists
   grep -n "yesterday_accomplishments\|today_priorities" services/utils/standup_formatting.py

   # Verify current canonical/slack/json output (run a sample)
   # (manual — server-up scenario)
   ```

3. **Update GitHub Issue** at start with:
   ```
   ## Status: Investigation Started
   - [ ] Current state documented (consumers identified)
   - [ ] Schema shape decision made (Phase 0)
   - [ ] Formatter migration path identified
   ```

### STOP Conditions

- StandupResult has consumers beyond formatters + API + tests → re-scope with PM
- Formatters depend on the string format in ways that don't decompose cleanly → re-scope
- `WorkItem.to_dict()` doesn't actually serve standup data (i.e., standup uses commits + raw session_context, not WorkItems) → may need a smaller "GitHub commits" struct rather than full WorkItem. Verify what data sources flow in.

---

## Phase 0.5: Frontend-Backend Contract Verification (MANDATORY for UI work)

### Applicability assessment

This issue **changes the standup API response shape** that the frontend (standup.html template) consumes. Phase 0.5 applies even though this issue does NOT modify the template — the contract change must be coordinated with the next-issue (#704) consumer.

### Required Actions

1. **Document current API response shape** (verified in spike):
   ```json
   {
     "success": true,
     "standup": {
       "yesterday_accomplishments": ["✅ commit msg", "📋 work item"],
       "today_priorities": ["🎯 Continue work on repo", "🔄 Complete X: status"],
       "blockers": ["⚠️ No recent GitHub activity detected"],
       "context_source": "...",
       "github_activity": {...},
       "performance_metrics": {...},
       "metadata": {...}
     }
   }
   ```

2. **Document target API response shape** (subject to Phase 0 decision; assuming Option 1):
   ```json
   {
     "success": true,
     "standup": {
       "yesterday_accomplishments": [
         {
           "display": "Completed Phase Z",
           "source": "commit",
           "lifecycle_state": null,
           "icon": "✅"
         },
         {
           "display": "audit_transparency Phase 2",
           "source": "work",
           "lifecycle_state": "ratified",
           "icon": "📋"
         }
       ],
       "today_priorities": [
         {
           "display": "Continue work on piper-morgan",
           "source": "active_repo",
           "lifecycle_state": null,
           "icon": "🎯"
         }
       ],
       "blockers": [
         {
           "display": "No recent GitHub activity detected",
           "source": "system",
           "lifecycle_state": null,
           "icon": "⚠️"
         }
       ],
       ...
     }
   }
   ```

3. **Verify this contract change does not break #704's gameplan assumptions**: #704 needs `lifecycle_state` reachable per item. Target shape carries it.

4. **Document the migration path**: existing `standup.html` template renders `${item}`. After this change, item is `{display, ...}`, not a string. **#704 will be the issue that updates the template** — but the contract MUST be deployable without #704 (i.e., shipping #1034 first must not break the existing UI).

   **Mitigation option**: keep a `display` string at the same key the template currently reads, OR temporarily render `${item.display || item}` in standup.html as part of #1034's scope. The latter is small and scoped enough that it can land here.

### Decision needed from PM in Phase -1

Whether to include the small standup.html `${item.display || item}` change in #1034's scope, OR ship #1034 + #704 in close sequence.

### STOP Conditions

- If the contract change breaks the existing standup.html render with no in-scope mitigation → STOP and re-scope.

---

## Phase 0.6: Data Flow & Integration Verification

### Applicability assessment

Standup is multi-layer: `MorningStandupWorkflow.generate_standup()` → orchestration → `StandupResult` → API endpoint → JSON formatter → template. Phase 0.6 applies for the layer-by-layer audit, even though the data shape change doesn't introduce new user_id/session_id propagation paths (those are already there).

### Part A: Data Flow Requirements

| Layer | Needs change? | What changes |
|-------|---------------|--------------|
| `MorningStandupWorkflow._generate_standup_content` (`services/features/morning_standup.py:200`) | ✅ | Build per-item dicts instead of strings; carry `lifecycle_state` if WorkItem present |
| `StandupResult` dataclass (`services/features/morning_standup.py:45`) | ✅ | Field type changes from `List[str]` to `List[Dict[str, Any]]` (or a typed dataclass) |
| `StandupResponse` Pydantic model (`web/api/routes/standup.py:94`) | ✅ | Field type changes accordingly |
| `format_standup` (`services/utils/standup_formatting.py`) | ✅ | Adapt to read `item["display"]` etc. instead of bare strings (Phase 0 decision dependent) |
| `web/api/routes/standup.py:520` JSON formatter | ✅ | Pass-through still works since dicts serialize natively |
| `MorningStandupWorkflow.canonical_query_integration` (line 92-110) | ✅ | Returns `standup_context` containing the same lists; consumer impact: callers of canonical handler integration. May need a parallel string projection. |

### Part B: Integration Points Checklist

| Caller | Callee | Verification |
|--------|--------|--------------|
| `standup.py` route | `StandupOrchestrationService.generate_standup` | Verify still returns `StandupResult` |
| `StandupOrchestrationService` | `MorningStandupWorkflow` | Verify the new dict shape propagates |
| Canonical query path | `canonical_query_integration` | May need string-projection adapter for non-template consumers (e.g., LLM context assembly) — TBD Phase 0 |
| GitHub commit data | `_generate_standup_content` | Verify commit dicts have what we need to construct per-item dict (currently just `commit.get('message', '')`) |
| WorkItem data | `_generate_standup_content` | Verify WorkItem flows through `session_context["yesterday_work"]`. Today the code does `for work in session_context["session_context"]["yesterday_work"]: yesterday_accomplishments.append(f"📋 {work}")` — `work` may be a string already. **STOP condition**: if `work` is a string at this layer, the upstream session-context provider also needs to carry structured data. Investigate. |

### Part C: Pattern Adaptation Notes

This isn't following an existing pattern; it's reshaping a pipeline. No source-pattern column.

**Potential pitfalls**:
- The session_context provider may already throw away WorkItem structure before standup sees it. If so, the fix needs to extend further upstream than #1034's body suggests. Phase 0 must verify this, and STOP-and-surface if so.
- Canonical handler integration consumers may break.

### STOP Conditions

- If `session_context["yesterday_work"]` is `List[str]` already (loss of structure happens upstream), STOP and surface to PM — scope expands to include the upstream provider.
- If canonical query consumers depend on string format, STOP and surface to PM.

---

## Phase 0.7: Conversation Design

### Applicability assessment

**Not applicable** — this is a backend pipeline shape change, not a conversational feature. Per template "When to Apply" guidance, this falls in the "❌ Single-turn Q&A (skip this phase)" / "non-conversational" category.

### Per audit-cascade skill: PM approval needed to mark inapplicable

**Question for PM**: confirm Phase 0.7 inapplicability for this issue. Template self-describes the skip; cascade skill requires explicit confirmation.

---

## Phase 0.8: Post-Completion Integration

### Applicability assessment

**Not applicable** — this is a read-only schema change. No user state changes, no new database records, no downstream behavior dependencies. Per template "When to Apply": "❌ Read-only features (skip this phase)".

### Per audit-cascade skill: PM approval needed to mark inapplicable

**Question for PM**: confirm Phase 0.8 inapplicability. Same condition as 0.7.

---

## Phases 1-N: Development Work

### Phase 1: StandupResult schema change

**Deploy**: Single agent (Lead Dev), sequential.

**Work**:
- [ ] Define per-item dataclass (`StandupItem`) or typed `TypedDict` carrying `display: str`, `source: str`, `lifecycle_state: Optional[str]`, `icon: str`
- [ ] Update `StandupResult` field types
- [ ] Update `MorningStandupWorkflow._generate_standup_content` to build the new dict shape
  - From commits: `{display: commit.message, source: "commit", lifecycle_state: None, icon: "✅"}`
  - From session work items: `{display: <extract>, source: "work", lifecycle_state: <if_workitem>, icon: "📋"}`
  - From active repos: `{display: f"Continue work on {repo}", source: "active_repo", lifecycle_state: None, icon: "🎯"}`
  - From yesterday context: `{display: f"Complete {area}: {status}", source: "yesterday_context", lifecycle_state: None, icon: "🔄"}`
  - From blockers: `{display: <blocker text>, source: "system", lifecycle_state: None, icon: "⚠️"}`
- [ ] Update `StandupResponse` Pydantic model accordingly

**Bookend**: `gh issue comment 1034 -b "✓ Phase 1 complete: StandupResult + StandupResponse carry structured items per design. Files: services/features/morning_standup.py, web/api/routes/standup.py."`

### Phase 2: Formatter migration

**Work**:
- [ ] Read `services/utils/standup_formatting.py` to understand canonical/slack consumers
- [ ] Adapt formatters: read `item["display"]` (or use the icon for prefix) per format
- [ ] Verify canonical / slack / json output unchanged at character level for the same input

**Tests**:
- [ ] Existing standup formatter tests pass unchanged (regression assurance)

### Phase 2a: Routing integration tests (NOT applicable)

This isn't intent/handler/classifier work. **Question for PM**: confirm 2a inapplicable.

### Phase 2b: Wiring integration tests (REQUIRED)

This IS multi-layer data flow.

- [ ] Wiring test: `_generate_standup_content` produces structured items end-to-end through API response
- [ ] Wiring test: a WorkItem with `lifecycle_state` set in session_context flows through to API response with `lifecycle_state` populated
- [ ] Wiring test: graceful degradation — items without lifecycle_state present `None`/missing

### Phase 3: Canonical handler integration

If canonical_query_integration consumers (LLM context assembly etc.) depend on string format, add adapter that projects structured → string for those consumers, OR migrate them.

- [ ] Identify canonical query consumers
- [ ] Decide: adapt consumers, or add adapter
- [ ] Implement decision
- [ ] Tests

### Phase 4: Standup template safety check (per Phase 0.5 decision)

If PM confirms keeping #1034 scope tight (without template changes):
- [ ] Verify standup.html still renders with new shape (likely shows "[object Object]"); ship the trivial `${item.display || item}` change as in-scope mitigation; #704 will replace later
- [ ] OR ship #1034 + #704 in the same merge window

If PM confirms expanding scope:
- [ ] Update standup.html minimally to render `${item.display}` — separate from #704's lifecycle indicator wiring

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **GitHub Final Update**:
   ```
   ## Status: Complete - Awaiting PM Approval
   - All AC met
   - Tests passing (paste output)
   - No regressions
   - Documentation updated
   - #704 unblocked
   ```

2. **Documentation**:
   - [ ] If schema decision constitutes an architectural change worth recording: file ADR follow-up. (Likely NO — internal pipeline shape only.)
   - [ ] Update relevant code comments cross-referencing #1034 + #704 + spike doc

3. **Evidence Compilation**:
   - [ ] Test output (Phase 1 + 2 + wiring + regression)
   - [ ] Files modified list
   - [ ] Before/after API response shape (curl example)

4. **Handoff to #704**:
   - [ ] Document on #704 that pre-work is complete; #704 can now consume `lifecycle_state` per item

5. **Session log**: complete with all Phase outputs

6. **PM Approval Request**:
   ```
   @PM - #1034 complete:
   - StandupResult/Response carry structured items
   - Formatters preserved
   - Wiring tests verify lifecycle_state reaches API response
   - #704 unblocked
   ```

---

## Multi-Agent Coordination Plan

Single agent (Lead Dev). No multi-agent deployment for this issue — schema changes are tightly coupled across files.

### Verification Gates

- [ ] Phase 1: Unit tests on StandupResult shape pass
- [ ] Phase 2: Formatter regression tests pass
- [ ] Phase 2b: Wiring integration tests pass (Phase 0.6 mandate)
- [ ] Phase 3: Canonical handler consumers verified
- [ ] Phase Z: Manual API verification (curl `/api/v1/standup/generate`)

---

## STOP Conditions (apply throughout)

- Infrastructure assumption broken (e.g., session_context provider doesn't carry WorkItems)
- Critical features break (canonical query consumers depend on string format and don't have an easy migration)
- Tests fail for reasons unrelated to scope
- Pattern/method already exists upstream (75% pattern check — verify there's no in-flight work to do this)

---

## Evidence Requirements

- [ ] Terminal output of `pytest tests/...` for Phase 1 + 2 + 2b
- [ ] Curl output before/after for the API endpoint
- [ ] git diff showing the exact schema change

---

## Effort Estimate

**Overall Size**: Small-to-Medium (~2-4 hours)

| Phase | Estimate |
|-------|----------|
| Phase -1 PM walk | 15 min |
| Phase 0 investigation | 30 min |
| Phase 0.5 contract doc | 15 min |
| Phase 0.6 data flow audit | 20 min |
| Phase 1 schema change | 45 min |
| Phase 2 formatter migration | 30 min |
| Phase 2b wiring tests | 30 min |
| Phase 3 canonical consumers | 30 min |
| Phase 4 template safety | 15 min |
| Phase Z bookend | 15 min |

---

## Dependencies

- [x] Phase -1 spike completed (`dev/2026/05/03/m2d-phase-minus-1-infra-spike.md`)
- [ ] PM Phase -1 walkthrough complete

## Blocks

- #704 MUX-LIFECYCLE-UI-A (template wiring depends on the structured shape this issue introduces)

---

# Audit-Cascade: Gameplan vs gameplan-template v9.3

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Phase -1: Infrastructure Verification | ✅ | Part A filled; Part B questions for PM; Part A.2 worktree assessment included |
| Phase -1: PM Verification placeholder | ⚠️ | Placeholder filled with three explicit Qs; needs PM walkthrough before Phase 0 |
| Phase 0: GitHub Issue Verification | ✅ | `gh issue view 1034` step included |
| Phase 0: Codebase Investigation | ✅ | grep + test-find + formatter-grep commands listed |
| Phase 0: Update GitHub Issue | ✅ | Status template included |
| Phase 0: STOP Conditions | ✅ | Three STOP conditions named |
| Phase 0.5: Applicability assessment | ✅ | Applies (response-shape change consumed by frontend) |
| Phase 0.5: Current API response | ✅ | Documented from spike |
| Phase 0.5: Target API response | ✅ | Drafted (subject to Phase 0 decision) |
| Phase 0.5: Path verification (curl) | ⚠️ | Phase 0 will exec; not done yet (gameplan-stage) |
| Phase 0.5: Static-file verification | ✅ | N/A — no static files added/moved |
| Phase 0.5: STOP Conditions | ✅ | Documented |
| Phase 0.6: Applicability | ✅ | Applies (multi-layer data flow) |
| Phase 0.6: Data Flow Requirements table | ✅ | Layer-by-layer change matrix included |
| Phase 0.6: Integration Points checklist | ✅ | Caller→callee table with verification column |
| Phase 0.6: Pattern Adaptation Notes | ✅ | Marked as not-following-existing-pattern; pitfalls listed |
| Phase 0.6: STOP Conditions | ✅ | Two STOP conditions named |
| Phase 0.7: Conversation Design | ⚠️ | Marked inapplicable per template self-description; **PM approval requested** per audit-cascade skill |
| Phase 0.8: Post-Completion Integration | ⚠️ | Marked inapplicable per template self-description; **PM approval requested** per audit-cascade skill |
| Phases 1-N: Development with progressive bookending | ✅ | Phase 1, 2, 2a, 2b, 3, 4 all defined; bookend example included for Phase 1 |
| Phase 2a: Routing integration tests | ⚠️ | Marked N/A — not intent/classifier work; **PM approval requested** |
| Phase 2b: Wiring integration tests | ✅ | Three wiring tests specified; required per Phase 0.6 mandate |
| Phase Z: GitHub Final Update | ✅ | Template included |
| Phase Z: Documentation Updates | ✅ | ADR / cross-references covered |
| Phase Z: Evidence Compilation | ✅ | Listed |
| Phase Z: Handoff Preparation | ✅ | #704 handoff documented |
| Phase Z: Session Completion | ✅ | Listed |
| Phase Z: PM Approval Request | ✅ | Template included |
| Multi-Agent Coordination Plan | ✅ | Single-agent justification given |
| Verification Gates | ✅ | Listed |
| STOP Conditions (throughout) | ✅ | Section included |
| Evidence Requirements | ✅ | Listed |
| Effort Estimate | ✅ | Per-phase breakdown |
| Dependencies + Blocks | ✅ | Spike + #704 |
| Test Scope Requirements (unit/integration/wiring/perf/regression) | ✅ | Wiring tests required; perf not flagged (no perf-critical path); regression covered in Phase 2 |

## Action Required Before Proceeding

Three items need PM input before Phase 0 begins:

1. **Phase -1 questions** (schema shape Option 1 vs 2; non-test consumers; emoji-prefix-as-presentation)
2. **Phase 0.5 scope** (include trivial standup.html safety change in #1034, or ship in close sequence with #704)
3. **Phase 0.7 + 0.8 + 2a inapplicability** confirmations per audit-cascade skill (template self-describes them as skippable for this work shape)

If PM confirms the three N/A markings + answers Phase -1 questions, this gameplan moves to ✅ across the board and #1034 is ready to execute.

## Status

**Audit cascade gate: NOT YET PASSED.** Three ⚠️ items pending PM input. No ❌ items.
