# Gameplan: #1040 INTENT-COVERAGE-B: Pre-classifier patterns + handlers for labels + branches

**Issue**: #1040 (split from #864 per CEO 2026-05-03; sibling: #1039)
**Branch**: `claude/1040-intent-coverage-labels-branches`
**Drafted**: 2026-05-03 by Lead Developer
**Template**: gameplan-template.md v9.3

---

## Summary

Add full pre-classifier coverage + handlers + GitHub MCP adapter methods for two GitHub entity types: **labels** and **branches**. These are taxonomy-style entities — flat lists rather than progress-points-in-time. Closing this gap means user queries like "What labels do we use?" or "Active branches" reach dedicated handlers instead of routing through the floor LLM.

Sibling issue #1039 covers milestones + releases. Same architecture, separate-but-mirrored implementation. Ship order: PM-decided (issue body suggests milestones > releases > labels > branches by likely user-query frequency).

---

## Phase -1: Infrastructure Verification

**Status**: ⚠️ MCP adapter gap confirmed in 2026-05-03 spike (`dev/2026/05/03/m2e-phase-minus-1-infra-spike.md`).

| Surface | Status |
|---|---|
| `GITHUB_QUERY_PATTERNS` exists | ✅ `services/intent_service/pre_classifier.py:380` |
| `_get_github_action()` dispatcher | ✅ `services/intent_service/pre_classifier.py:1512` |
| Action registry | ✅ `services/intent_service/action_registry.py:66` |
| Handler dispatch in `intent_service.py` | ✅ `services/intent/intent_service.py:2074+` |
| `GitHubAdapter.list_labels(repo)` | ❌ MISSING — must add |
| `GitHubAdapter.list_branches(repo)` | ❌ MISSING — must add |

**Conclusion**: Same shape as #1039. Risk: Medium-Low (smaller queries — labels are simple, branches are simple).

---

## Phase 0: GitHub Investigation

- [ ] Re-read #1040 + #864 closure comment
- [ ] Confirm GitHub REST API endpoints:
  - Labels: `GET /repos/{owner}/{repo}/labels` (returns name + color + description)
  - Branches: `GET /repos/{owner}/{repo}/branches` (returns name + commit + protected)
- [ ] Skim sibling #1039 PR (when filed) to mirror its router/handler shape

---

## Phase 0.5: Frontend-Backend Contract

No new UI surfaces. Output is conversational message-text following the existing `_handle_list_issues_query` shape:
- `message`: human-readable list
- `intent_data.action`: `"list_labels_query"` / `"list_branches_query"`
- `intent_data.context`: `{ "label_count": N }` / `{ "branch_count": N, "default_branch": "..." }`

---

## Phase 0.6: Data Flow

```
User: "What labels do we use?"
  ↓
PreClassifier matches GITHUB_QUERY_PATTERNS
  ↓
_get_github_action() returns "list_labels_query"
  ↓
Intent { category=QUERY, action="list_labels_query" }
  ↓
intent_service._handle_list_labels_query(intent, workflow_id)
  ↓
GitHubIntegrationRouter.list_labels_via_mcp() (new)
  ↓
GitHubAdapter.list_labels(repo) (new)
  ↓
Format response (count + list with name + color swatch + brief description)
  ↓
IntentProcessingResult
```

Same shape for branches (sort: default branch first, then alphabetical or by recent commit).

---

## Phase 0.7: Conversation Design

**Labels examples**:
- "What labels do we use?" → list of all labels grouped by color or category
- "Show issue labels" → same
- "What labels are MVP?" → filter for `MVP` or labels matching the term (out of scope for this issue — flag as future)

**Branches examples**:
- "Active branches" → all open branches, default-marked
- "Show feature branches" → branches with `claude/*` or `feature/*` prefix (the issue body uses "feature branches" as a colloquialism — could match all non-default branches)
- "What branch are we on?" → query about local context — out of scope for #1040 (this is git-state, not GitHub-state)

**Trust-stage gating**: None (read-only deterministic queries). Same as #1039.

**MUX-consciousness**: Labels output should be visual-friendly in chat — color emoji or hex-readable. For MVP, plain-text list with optional color hex; visual swatches deferred to post-MVP.

---

## Phase 0.8: Post-Completion Verification

- [ ] Manual smoke as user: ask each example query; confirm output
- [ ] CI tests pass
- [ ] No regression on prior pre-classifier patterns

---

## Phase 1: GitHub MCP adapter methods

**Files**:
- `services/mcp/consumer/github_adapter.py` — add 2 methods:

```python
async def list_labels(
    self, repo: str = "piper-morgan-product"
) -> List[Dict[str, Any]]:
    """List GitHub labels for the configured repo."""

async def list_branches(
    self, repo: str = "piper-morgan-product"
) -> List[Dict[str, Any]]:
    """List GitHub branches for the configured repo."""
```

**Acceptance**:
- Auth via existing `_call_github_api` helper
- Normalized return shape (labels: name, color, description; branches: name, protected, default)
- 4-6 unit tests per method (success, empty, auth failure, retry)
- No regressions on existing adapter tests

**Estimate**: 1.5 hr

---

## Phase 2: GitHub integration router wrappers

**Files**:
- `services/integrations/github/github_integration_router.py` — add `list_labels_via_mcp()` and `list_branches_via_mcp()` (mirror `list_issues_via_mcp` shape)

**Acceptance**:
- Each wrapper passes through to adapter unchanged
- 2-3 tests per wrapper

**Estimate**: 30 min

---

## Phase 3: Pre-classifier patterns + action detection

**Files**:
- `services/intent_service/pre_classifier.py` — extend `GITHUB_QUERY_PATTERNS` + `_get_github_action()`

**Patterns to add (labels)**:
```python
r"\bwhat labels?\b",
r"\bshow.*labels?\b",
r"\blist.*labels?\b",
r"\bissue labels?\b",
r"\blabel(?:s)?\s*(?:list|count)\b",
r"\b(?:available|all)\s+labels?\b",
```

**Patterns to add (branches)**:
```python
r"\bactive branches?\b",
r"\bshow.*branches?\b",
r"\blist.*branches?\b",
r"\bfeature branches?\b",
r"\b(?:open|current)\s+branches?\b",
r"\bwhat branches?\b",
```

**Action dispatch**:
```python
label_patterns = [...]
if PreClassifier._matches_patterns(message, label_patterns):
    return "list_labels_query"

branch_patterns = [...]
if PreClassifier._matches_patterns(message, branch_patterns):
    return "list_branches_query"
```

**Acceptance**:
- 8-10 tests per entity type (positive + negative — "label this as urgent" should not match list-labels)
- No regressions on existing patterns

**Estimate**: 1.5 hr

---

## Phase 4: Action registry + lens inference

**Files**:
- `services/intent_service/action_registry.py` — 2 new entries each in ACTION_REGISTRY + ACTION_LABELS:
  ```python
  ("QUERY", "list_labels_query"): ActionDisposition.WORKFLOW,
  ("QUERY", "list_branches_query"): ActionDisposition.WORKFLOW,
  ...
  ("QUERY", "list_labels_query"): "List labels",
  ("QUERY", "list_branches_query"): "Show branches",
  ```
- `services/intent_service/lens_inference.py` — add lens mapping (PM Q below)

**Estimate**: 30 min

---

## Phase 5: Handler implementations

**Files**:
- `services/intent/intent_service.py` — dispatch + 2 new handlers (mirror `_handle_list_issues_query`)

**Dispatch (~line 2090)**:
```python
elif intent.action in ["list_labels", "list_labels_query"]:
    return await self._handle_list_labels_query(intent, workflow_id)
elif intent.action in ["list_branches", "list_branches_query"]:
    return await self._handle_list_branches_query(intent, workflow_id)
```

**Handlers** (~50 LOC each):
```python
async def _handle_list_labels_query(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult: ...

async def _handle_list_branches_query(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult: ...
```

Each:
- Calls router method
- Formats top-N (labels: full list with color hint; branches: default first, then top 10)
- Empty-state copy
- Error path with apologetic fallback

**Acceptance**:
- 6-8 tests per handler
- Manual smoke per Phase 0.8

**Estimate**: 1.5-2 hr

---

## Phase 6: Tests + verification

**Total target**: ~45 new tests across phases. Pre/post merge regression sweep.

**Estimate**: 45 min

---

## Phase Z: Handoff

- [ ] Issue #1040 closed with evidence
- [ ] Cross-reference #864 (origin) + #1039 (sibling) + #855 (parent)
- [ ] Session log updated; branch merged; sign-off discipline run

---

## Total Estimate

~6-7 hours (slightly less than #1039 — entity output simpler).

## Risks

- **Low-Medium**: pattern overlaps — "label this as urgent" should NOT match list-labels intent. Negative tests are critical.
- **Low**: branches output could grow large for repos with many branches; cap at top 20 + total count.

## Dependencies

- Same as #1039: existing GitHub MCP adapter, pre-classifier dispatch, intent_service handler dispatch ✅
- Sibling #1039 (milestones + releases) — independent

## Audit Cascade Matrix (Issue → Gameplan)

| Template Requirement | Status | Notes |
|---|---|---|
| Issue number referenced | ✅ | #1040 |
| Problem statement | ✅ | Pre-classifier gap for labels + branches |
| Phase -1 infra verification | ✅ | Adapter gap; pattern infra present |
| Phase 0 GitHub investigation | ✅ | API endpoints + sibling cross-ref |
| Phase 0.5 FE-BE contract | ✅ | Chat message; no UI |
| Phase 0.6 Data flow | ✅ | Diagrammed |
| Phase 0.7 Conversation design | ✅ | Examples + scope-edge notes (out-of-scope: filtering, local-branch-state) |
| Phase 0.8 Post-completion verification | ✅ | Smoke list |
| Phases 1-N with estimates | ✅ | 6 phases, ~6-7 hr |
| Acceptance criteria per phase | ✅ | All listed |
| Test strategy | ✅ | ~45 tests |
| Phase Z handoff | ✅ | Evidence, cross-refs, sign-off |
| Dependencies listed | ✅ | All present |
| Risks identified | ✅ | 2 risks |
| File paths cited | ✅ | All grep-able |

### Audit ✅ Items — PM Dispositions (2026-05-03)

**✅ Q1**: Ship sequencing. **PM**: "sequence sounds good." #1039 ships first, then #1040.

**✅ Q2**: Local-git "what branch are we on?" scope edge. **PM**: "file a followup to be triaged later." Out-of-scope for #1040; tracked by **#1044** (FOLLOWUP local-git branch query handler).

**✅ Q3**: Label color presentation. **PM**: "yes ok for now... CXO can reevaluate display over time." Ship plain-text for MVP; visual review deferred (covered under **#1043** en-masse copy review and CXO ongoing review).

**✅ Q4**: Lens inference. **PM**: "comfirmed." Both `list_labels_query` and `list_branches_query` → `ConversationalLens.PROJECT`.

**✅ Q5**: Branch filter scope. **PM**: "all non-default." Match all non-default branches for MVP; filter syntax (`claude/*` patterns etc.) deferred.

### Inherited from #1039 Q4

#1040 also inherits the hardcoded-repo-default cleanup (#1042). Land **#1042 → #1039 → #1040** in that order; the new methods (`list_labels`, `list_branches`) use the same per-call repo-resolution pattern established by #1042 and used by #1039.
