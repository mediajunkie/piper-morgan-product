# Gameplan: #1039 INTENT-COVERAGE-A: Pre-classifier patterns + handlers for milestones + releases

**Issue**: #1039 (split from #864 per CEO 2026-05-03; sibling: #1040)
**Branch**: `claude/1039-intent-coverage-milestones-releases`
**Drafted**: 2026-05-03 by Lead Developer
**Template**: gameplan-template.md v9.3

---

## Summary

Add full pre-classifier coverage + handlers + GitHub MCP adapter methods for two GitHub entity types: **milestones** and **releases**. These are list-with-detail entities representing project state at a moment in time. Closing this gap means user queries like "Show milestones" or "What version are we on?" reach dedicated handlers (with structured data + MUX-conscious presentation) instead of routing through the floor LLM.

Sibling issue #1040 covers labels + branches separately.

---

## Phase -1: Infrastructure Verification

**Status**: ⚠️ MCP adapter gap confirmed in 2026-05-03 spike (`dev/2026/05/03/m2e-phase-minus-1-infra-spike.md`).

| Surface | Status |
|---|---|
| `GITHUB_QUERY_PATTERNS` exists | ✅ `services/intent_service/pre_classifier.py:380` |
| `_get_github_action()` dispatcher | ✅ `services/intent_service/pre_classifier.py:1512` |
| Action registry (WORKFLOW disposition) | ✅ `services/intent_service/action_registry.py:66` |
| Handler dispatch in `intent_service.py` | ✅ `services/intent/intent_service.py:2074+` (`_handle_list_issues_query`, `_handle_list_prs_query` patterns) |
| `GitHubAdapter.list_milestones(repo)` | ❌ MISSING — must add |
| `GitHubAdapter.list_releases(repo)` | ❌ MISSING — must add |

**Conclusion**: Pattern infra is ready; dispatch shape is well-established (mirror `_handle_list_issues_query`); MCP adapter needs 2 new methods. Risk: Medium (mostly composition + 2 new adapter calls; no novel architecture).

---

## Phase 0: GitHub Investigation

- [ ] Re-read #1039 + #864 closure comment for any updated framing
- [ ] Confirm GitHub REST API endpoints for milestones + releases:
  - Milestones: `GET /repos/{owner}/{repo}/milestones` (open by default; can filter all/closed)
  - Releases: `GET /repos/{owner}/{repo}/releases` (returns published releases; pre-releases included)
- [ ] Skim `services/integrations/github/github_integration_router.py` to mirror its existing `list_issues_via_mcp` shape

---

## Phase 0.5: Frontend-Backend Contract

No new UI surfaces. Output is conversational message-text. Where existing chat handlers like `_handle_list_issues_query` produce a markdown-formatted message + `intent_data` dict, milestones + releases handlers follow the same shape:
- `message`: human-readable summary with bullet list
- `intent_data.action`: `"list_milestones_query"` / `"list_releases_query"`
- `intent_data.context`: `{ "milestone_count": N }` / `{ "release_count": N, "latest_version": "..." }`

---

## Phase 0.6: Data Flow

```
User: "Show milestones"
  ↓
PreClassifier.classify() matches GITHUB_QUERY_PATTERNS
  ↓
_get_github_action() returns "list_milestones_query"
  ↓
Intent { category=QUERY, action="list_milestones_query" }
  ↓
intent_service._handle_list_milestones_query(intent, workflow_id)
  ↓
GitHubIntegrationRouter.list_milestones_via_mcp() (new, wraps adapter)
  ↓
GitHubAdapter.list_milestones(repo) (new) → list[dict]
  ↓
Format response (count, top 5 by due_on, list with title + due date + open-issue count)
  ↓
IntentProcessingResult { success=True, message=..., intent_data=... }
```

Same shape for releases (sort by `published_at` desc; show tag_name + name + published_at).

---

## Phase 0.7: Conversation Design

**Milestones examples**:
- "Show milestones" → list of open milestones, sorted by due_on, top 5
- "When is the next milestone?" → soonest open milestone with due_on
- "Show closed milestones" → closed-state filter

**Releases examples**:
- "Recent releases" → list of latest 5 releases by published_at
- "What version are we on?" → latest non-prerelease tag_name
- "Show pre-releases" → prerelease=true filter

**Trust-stage gating**: Per ADR-061 LLM-Touch Boundary, deterministic queries → deterministic answers. No trust gate needed (read-only listing of GitHub state). Aligns with existing `_handle_list_issues_query` which has no trust gate.

**MUX-consciousness**: Empty-state copy ("You don't have any open milestones") matches the "no meetings — great day for deep work" empathy/disclosure tone established in canonical handlers.

---

## Phase 0.8: Post-Completion Verification

- [ ] Manual smoke as user: ask each of the example queries above; confirm message renders + matches GitHub state
- [ ] CI tests pass
- [ ] No regression on `_handle_list_issues_query` / `_handle_list_prs_query` (regression sweep on `tests/unit/services/intent_service/`)

---

## Phase 1: GitHub MCP adapter methods

**Files**:
- `services/mcp/consumer/github_adapter.py` — add 2 methods following the `list_github_issues_direct` shape:

```python
async def list_milestones(
    self, repo: str = "piper-morgan-product", state: str = "open"
) -> List[Dict[str, Any]]:
    """List GitHub milestones for the configured repo."""
    # Mirrors list_github_issues_direct retry + error handling

async def list_releases(
    self, repo: str = "piper-morgan-product"
) -> List[Dict[str, Any]]:
    """List GitHub releases for the configured repo."""
    # Same shape
```

**Acceptance**:
- Each method authenticates via existing `_call_github_api` helper
- Returns normalized list of dicts with stable keys (title, number, due_on, state, open_issues for milestones; tag_name, name, published_at, prerelease for releases)
- 4-6 unit tests per method (success, empty, auth failure, retry behavior) — mirror existing adapter tests
- No regressions on `list_github_issues_direct` tests

**Estimate**: 1.5 hr

---

## Phase 2: GitHub integration router wrappers

**Files**:
- `services/integrations/github/github_integration_router.py` — add `list_milestones_via_mcp()` and `list_releases_via_mcp()` wrappers (mirror `list_issues_via_mcp` shape)

**Acceptance**:
- Each wrapper returns the adapter's list directly (no transformation; handler does the formatting)
- 2-3 tests per wrapper

**Estimate**: 30 min

---

## Phase 3: Pre-classifier patterns + action detection

**Files**:
- `services/intent_service/pre_classifier.py` — extend `GITHUB_QUERY_PATTERNS` with milestone + release patterns; extend `_get_github_action()` dispatcher

**Patterns to add (milestones)**:
```python
r"\bshow.*milestones?\b",
r"\blist.*milestones?\b",
r"\bnext milestone\b",
r"\bwhat milestones?\b",
r"\bopen milestones?\b",
r"\bclosed milestones?\b",
r"\bmilestone(?:s)?\s*(?:status|count|list)\b",
```

**Patterns to add (releases)**:
```python
r"\brecent releases?\b",
r"\bshow.*releases?\b",
r"\blist.*releases?\b",
r"\bwhat version (?:are we on|is current)\b",
r"\bcurrent (?:release|version)\b",
r"\blatest release\b",
r"\bpre[- ]releases?\b",
```

**Action dispatch** in `_get_github_action()`:
```python
milestone_patterns = [...]
if PreClassifier._matches_patterns(message, milestone_patterns):
    return "list_milestones_query"

release_patterns = [...]
if PreClassifier._matches_patterns(message, release_patterns):
    return "list_releases_query"
```

**Acceptance**:
- New patterns matched in pre-classifier without regressions on existing GitHub patterns
- Action names returned correctly for sample inputs ("show milestones", "what version are we on", etc.)
- 8-10 tests per entity type (positive matches + negative — e.g., "release me from this meeting" should NOT match)

**Estimate**: 1.5 hr

---

## Phase 4: Action registry + lens inference

**Files**:
- `services/intent_service/action_registry.py` — add 2 entries to ACTION_REGISTRY + 2 to ACTION_LABELS:
  ```python
  ("QUERY", "list_milestones_query"): ActionDisposition.WORKFLOW,
  ("QUERY", "list_releases_query"): ActionDisposition.WORKFLOW,
  ...
  ("QUERY", "list_milestones_query"): "List milestones",
  ("QUERY", "list_releases_query"): "Show recent releases",
  ```
- `services/intent_service/lens_inference.py` — add lens mapping (`ConversationalLens.PROJECT` or `STATUS` per closest existing analog; PM Q-question)

**Acceptance**:
- Registry lookups return `WORKFLOW` for both new actions
- Tests: 2 lookup tests + 2 lens tests

**Estimate**: 30 min

---

## Phase 5: Handler implementations

**Files**:
- `services/intent/intent_service.py` — dispatch + 2 new handler methods

**Dispatch (~line 2090)**:
```python
elif intent.action in ["list_milestones", "list_milestones_query"]:
    return await self._handle_list_milestones_query(intent, workflow_id)
elif intent.action in ["list_releases", "list_releases_query"]:
    return await self._handle_list_releases_query(intent, workflow_id)
```

**Handlers** (mirror `_handle_list_issues_query` shape, ~50 LOC each):
```python
async def _handle_list_milestones_query(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult: ...

async def _handle_list_releases_query(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult: ...
```

Each:
- Calls `GitHubIntegrationRouter.list_*_via_mcp()`
- Formats top-5 with structured detail (title + due_on + open_issues for milestones; tag_name + published_at + name for releases)
- Empty-state message ("You don't have any open milestones right now.")
- Error path returns success=True with apologetic message (matches existing pattern)

**Acceptance**:
- 6-8 tests per handler covering: populated list, single-item, empty, error path, action_data emission
- Manual smoke per Phase 0.8

**Estimate**: 2 hr

---

## Phase 6: Tests + verification

**Total target**: ~50 new tests across:
- Adapter (Phase 1): ~10 tests
- Router (Phase 2): ~5 tests
- Pre-classifier (Phase 3): ~16-20 tests
- Registry (Phase 4): ~4 tests
- Handlers (Phase 5): ~12-16 tests

**Verification**:
- [ ] `pytest tests/unit/services/intent_service/ -v` — no regressions
- [ ] `pytest tests/unit/services/mcp/consumer/test_github_adapter*.py -v` — all passing including new methods
- [ ] `pytest tests/unit/services/intent/test_intent_service*.py -v` — new handlers covered
- [ ] Pre/post merge regression sweep on full unit suite
- [ ] Manual smoke per Phase 0.8

**Estimate**: 1 hr (mostly falls out of phases 1-5)

---

## Phase Z: Handoff

- [ ] Issue #1039 closed with implementation evidence
- [ ] Cross-reference #864 (split origin) and #1040 (sibling)
- [ ] Cross-reference #855 (parent: Intent Pipeline Incompleteness)
- [ ] Session log updated; branch merged; sign-off discipline run

---

## Total Estimate

~7-8 hours.

## Risks

- **Medium**: GitHub API rate-limiting if user repeatedly queries — existing adapter handles via retry; not a new risk
- **Low**: lens inference mapping — `PROJECT` vs new `STATUS` is a small judgment call; flag for PM
- **Low**: empty-state copy decisions could benefit from MUX review (see Q3 below)

## Dependencies

- Existing GitHub MCP adapter infrastructure ✅
- Existing pre-classifier dispatch ✅
- Existing intent_service handler dispatch ✅
- Sibling #1040 (labels + branches) — independent, can ship first or in parallel

## Audit Cascade Matrix (Issue → Gameplan)

| Template Requirement | Status | Notes |
|---|---|---|
| Issue number referenced | ✅ | #1039 in header |
| Problem statement | ✅ | Pre-classifier gap for milestones + releases |
| Phase -1 infra verification | ✅ | Adapter gap confirmed; pattern infra confirmed present |
| Phase 0 GitHub investigation | ✅ | API endpoints documented; cross-refs to #864/#1040/#855 |
| Phase 0.5 FE-BE contract | ✅ | Conversational message; no UI surface |
| Phase 0.6 Data flow | ✅ | Diagrammed end-to-end |
| Phase 0.7 Conversation design | ✅ | Example queries, trust gating, MUX tone |
| Phase 0.8 Post-completion verification | ✅ | Smoke test list |
| Phases 1-N with estimates | ✅ | 6 phases, ~7-8 hr total |
| Acceptance criteria per phase | ✅ | All listed |
| Test strategy | ✅ | ~50 tests across phases |
| Phase Z handoff | ✅ | Evidence, cross-refs, sign-off |
| Dependencies listed | ✅ | All present; sibling independent |
| Risks identified | ✅ | 3 risks called out |
| File paths cited | ✅ | All references include grep-able paths |

### Audit ✅ Items — PM Dispositions (2026-05-03)

**✅ Q1**: Sequencing. **PM**: "one PR seems ok to me if you agree." Lead Dev agreed (shared adapter shape, handler pattern, test scaffolding). One PR for milestones + releases.

**✅ Q2**: Lens inference. **PM**: "PROJECT seems right, yes." Both `list_milestones_query` and `list_releases_query` → `ConversationalLens.PROJECT`.

**✅ Q3**: Empty-state copy. **PM**: "ship first but make a followup issue to review copy en masse." Workmanlike copy ships in this PR; copy review covered by **#1043** (POST-MVP en-masse copy review).

**✅ Q4**: Repo target — hardcoded `piper-morgan-product` default. **PM**: "let's not use my repo for this project as a default anymore!" Disposition: **Option C** — file separate pre-work issue for hardcoded-repo-default cleanup; #1039 lands on cleaned-up base. Pre-work tracked by **#1042** (PRE-1039 cleanup) — #1039 BLOCKED by #1042 until cleanup ships.
