# Gameplan: #1039 INTENT-COVERAGE-A — Pre-classifier + handlers for GitHub milestones + releases

**Issue**: #1039 (split from #864 per CEO 2026-05-03; sibling: #1040)
**Branch**: `claude/1039-intent-coverage-milestones-releases`
**Drafted**: 2026-05-04 by Lead Developer (refresh of 2026-05-03 v1)
**Template**: gameplan-template.md v9.3

---

## Summary

Add full pre-classifier coverage + handlers + GitHub MCP adapter methods for two GitHub entity types: **milestones** and **releases**. List-with-detail entities representing project state at a moment in time. Closing this gap routes user queries like "Show milestones" or "What version are we on?" to dedicated handlers (with structured data + MUX-conscious presentation) instead of through the floor LLM.

Sibling issue #1040 covers labels + branches. Both unblocked by **#1042** (PRE-1039 hardcoded-repo-default cleanup), shipped 2026-05-04.

---

## Phase -1: Infrastructure Verification (refreshed 2026-05-04)

**Status**: ✅ All deps confirmed present; #1042 unblocker shipped.

| Surface | Status |
|---|---|
| `GITHUB_QUERY_PATTERNS` | ✅ `services/intent_service/pre_classifier.py:380` |
| `_get_github_action()` dispatcher | ✅ `services/intent_service/pre_classifier.py:1512` |
| Action registry (WORKFLOW disposition) | ✅ `services/intent_service/action_registry.py:66+` (existing entries: stale_prs_query, list_issues_query, list_prs_query) |
| Handler dispatch | ✅ `services/intent/intent_service.py:2091, 2095` (`_handle_list_issues_query`, `_handle_list_prs_query`) |
| `lens_inference` | ✅ `services/intent_service/lens_inference.py` — `ConversationalLens.PROJECTS` exists (note: plural; PM Q2 said "PROJECT" but enum is `PROJECTS` — using actual name) |
| `repo_resolver` (per-call repo + owner) | ✅ Shipped via #1042 — adapter methods now require explicit `repo` + `owner` |
| `GitHubAdapter.list_milestones(repo, owner)` | ❌ MISSING — must add |
| `GitHubAdapter.list_releases(repo, owner)` | ❌ MISSING — must add |
| Router internal `_resolve_default_repo()` helper | ✅ Shipped via #1042 |

**Conclusion**: Pattern infra ready. Adapter needs 2 new methods. New methods will use `(repo, owner)` required-positional shape established by #1042 (no defaults). Router wrappers will use the keyword-only optional pattern from #1042 so callers can pre-resolve or let router resolve internally. Risk: Low.

---

## Phase 0: GitHub Investigation

- [ ] Re-read #1039 + #864 closure for any updated framing
- [ ] Confirm GitHub REST API endpoints:
  - Milestones: `GET /repos/{owner}/{repo}/milestones?state={open|closed|all}` (returns `{title, number, state, due_on, open_issues, closed_issues, ...}`)
  - Releases: `GET /repos/{owner}/{repo}/releases` (returns `{tag_name, name, published_at, prerelease, draft, html_url, ...}`)
- [ ] Skim `services/integrations/github/github_integration_router.py:227+` (`list_issues` wrapper) to mirror its existing shape for the new wrappers
- [ ] Skim #1042 commit `2d577225` to confirm patterns this lands on top of

---

## Phase 0.5: Frontend-Backend Contract

No new UI surfaces. Output is conversational message-text. The shape per the existing `_handle_list_issues_query` pattern:

- `message`: human-readable summary with bullet list
- `intent_data.action`: `"list_milestones_query"` / `"list_releases_query"`
- `intent_data.context`: `{ "milestone_count": N }` / `{ "release_count": N, "latest_version": "..." }`
- Standard graceful error path when GitHub not configured (mirror `_handle_list_issues_query:3919-3929` exception handling)

---

## Phase 0.6: Data Flow

```
User: "Show milestones"
  ↓
PreClassifier.classify() — message matches GITHUB_QUERY_PATTERNS
  ↓
_get_github_action() → "list_milestones_query"
  ↓
Intent { category=QUERY, action="list_milestones_query" }
  ↓
intent_service._handle_list_milestones_query(intent, workflow_id)
  ↓
GitHubIntegrationRouter.list_milestones_via_mcp() (NEW wrapper, optional owner/repo)
  ↓
[router._resolve_default_repo() if owner/repo not passed]
  ↓
GitHubAdapter.list_milestones(repo, owner) (NEW, required positional args)
  ↓
GET /repos/{owner}/{repo}/milestones via _call_github_api
  ↓
Format response: count + top 5 sorted by due_on with title + due date + open-issue count
  ↓
IntentProcessingResult { success=True, message=..., intent_data=... }
```

Same shape for releases (sort by `published_at` desc; show tag_name + name + published_at).

**Per-call resolution path** inherits from #1042 — handlers may pass owner/repo explicitly OR let the router resolve. Default behavior: router resolves via `repo_resolver` decision tree (project-link → user `default_repo` preference → `PIPER_DEFAULT_REPO` env → graceful empty list).

---

## Phase 0.7: Conversation Design

### Milestones examples
- "Show milestones" → list of open milestones, sorted by `due_on`, top 5
- "When is the next milestone?" → soonest open milestone with due_on
- "Show closed milestones" → state=closed filter (deferred — pattern matches but may pass `state` kwarg through; baseline MVP returns open only)
- "List milestones" / "What milestones?" / "Open milestones?"

### Releases examples
- "Recent releases" → list of latest 5 releases by published_at
- "What version are we on?" → latest non-prerelease tag_name
- "Show pre-releases" → prerelease filter (deferred for MVP unless trivial)
- "Latest release" / "Current version" / "List releases"

### Trust-stage gating

Per ADR-061 LLM-Touch Boundary, deterministic queries → deterministic answers. **No trust gate** needed (read-only listing of GitHub state). Aligns with existing `_handle_list_issues_query` which has no trust gate.

### MUX-consciousness

Empty-state copy ("You don't have any open milestones right now.") matches the empathetic disclosure tone established in canonical handlers. Workmanlike copy ships in this PR; CXO-led en-masse copy review tracked by **#1043**.

---

## Phase 0.8: Post-Completion Verification

- [ ] Manual smoke as user: ask each example query above; confirm message renders + matches GitHub state
- [ ] CI tests pass; no regression on `_handle_list_issues_query` / `_handle_list_prs_query`
- [ ] Pre/post merge regression sweep on `tests/unit/services/intent_service/` and `tests/unit/services/mcp/consumer/test_github_adapter*.py`

---

## Phase 1: GitHub MCP adapter methods

**Files**:
- `services/mcp/consumer/github_adapter.py` — add 2 methods following the `(repo, owner)` required-positional shape established by #1042:

```python
async def list_milestones(
    self, repo: str, owner: str, state: str = "open"
) -> List[Dict[str, Any]]:
    """List GitHub milestones for a repo.

    Issue #1039: ``repo`` and ``owner`` are required positional args
    (per #1042 cleanup; no hardcoded defaults).
    """
    # Mirror list_github_issues_direct retry + token_counter wrapping shape

async def list_releases(
    self, repo: str, owner: str
) -> List[Dict[str, Any]]:
    """List GitHub releases for a repo (Issue #1039)."""
    # Same shape
```

**Acceptance**:
- Each method auths via existing `_call_github_api` helper
- Returns normalized list of dicts with stable keys:
  - Milestones: `title`, `number`, `state`, `due_on`, `open_issues`, `closed_issues`, `html_url`, `description`
  - Releases: `tag_name`, `name`, `published_at`, `prerelease`, `draft`, `html_url`, `body` (truncated)
- 4-6 unit tests per method (success, empty, auth failure, retry behavior) — mirror existing adapter tests
- Error path returns `[]` on exception (matches existing pattern)
- 0 regressions on `list_github_issues_direct` tests

**Estimate**: 1.5 hr

---

## Phase 2: GitHub integration router wrappers

**Files**:
- `services/integrations/github/github_integration_router.py` — add `list_milestones_via_mcp()` and `list_releases_via_mcp()` mirroring the **internal-resolution** pattern from #1042's `get_open_issues`:

```python
async def list_milestones_via_mcp(
    self,
    state: str = "open",
    owner: Optional[str] = None,
    repo: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List milestones via MCP adapter.

    Issue #1039: ``owner``/``repo`` optional kwargs; router resolves via
    ``repo_resolver`` if not provided. Returns ``[]`` if unresolved.
    """
    if not self._initialized:
        await self.initialize()
    if self.mcp_adapter:
        if not owner or not repo:
            resolved = await self._resolve_default_repo()
            if resolved is None:
                return []
            owner, repo = resolved
        return await self.mcp_adapter.list_milestones(repo, owner, state=state)
    return []
```

`list_releases_via_mcp` mirrors the same shape (no `state` param).

**Acceptance**:
- 2-3 tests per wrapper (resolution + adapter call + graceful-empty)
- Spatial-fallback path returns empty (no spatial integration for these entities at MVP)

**Estimate**: 30 min

---

## Phase 3: Pre-classifier patterns + action detection

**Files**:
- `services/intent_service/pre_classifier.py` — extend `GITHUB_QUERY_PATTERNS` (line 380) with milestone + release patterns; extend `_get_github_action()` dispatcher (line 1512+)

**Patterns to add (milestones)** — Q3 disposition: state-filter feature withheld; only unqualified patterns:
```python
# Milestone queries — Issue #1039 (state-filter deferred to post-MVP follow-up)
r"\bshow.*milestones?\b",
r"\blist.*milestones?\b",
r"\bnext milestone\b",
r"\bwhat milestones?\b",
r"\bmilestone(?:s)?\s+(?:status|count|list|due)\b",
r"\bwhen.*milestone\b",
```

**Patterns to add (releases)** — Q4 disposition: pre-release filter feature withheld:
```python
# Release queries — Issue #1039 (pre-release filter deferred to post-MVP follow-up)
r"\brecent releases?\b",
r"\bshow.*releases?\b",
r"\blist.*releases?\b",
r"\bwhat version (?:are we on|is current)\b",
r"\bcurrent (?:release|version)\b",
r"\blatest release\b",
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
- New patterns matched in pre-classifier without regressions on existing GitHub patterns (the classification dispatcher is greedy first-match — order matters; new patterns must come AFTER existing list_issues / stale_prs to avoid shadowing)
- Action names returned correctly for sample inputs
- 8-10 tests per entity type covering positive + negative cases (e.g., "release me from this meeting" should NOT match release patterns; "milestone moment" should not falsely match)

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
- `services/intent_service/lens_inference.py` — add lens mapping using **`ConversationalLens.PROJECTS`** (per PM Q2 — actual enum name is plural):
  ```python
  "list_milestones_query": ConversationalLens.PROJECTS,
  "list_releases_query": ConversationalLens.PROJECTS,
  ```

**Acceptance**:
- Registry lookups return `WORKFLOW` for both new actions
- Lens lookups return `PROJECTS`
- 4 tests (2 registry + 2 lens)

**Estimate**: 30 min

---

## Phase 5: Handler implementations

**Files**:
- `services/intent/intent_service.py` — dispatch + 2 new handler methods at ~line 2090+

**Dispatch addition**:
```python
elif intent.action in ["list_milestones", "list_milestones_query"]:
    return await self._handle_list_milestones_query(intent, workflow_id)
elif intent.action in ["list_releases", "list_releases_query"]:
    return await self._handle_list_releases_query(intent, workflow_id)
```

**Handlers** (mirror `_handle_list_issues_query` shape):

```python
async def _handle_list_milestones_query(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult:
    """Handle 'Show milestones' and similar queries (Issue #1039)."""
    self.logger.info("Processing list milestones query")
    try:
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )
        github_router = GitHubIntegrationRouter()
        milestones = await github_router.list_milestones_via_mcp()

        if milestones:
            count = len(milestones)
            message = f"You have **{count} open milestone{'s' if count != 1 else ''}**."
            if count > 0:
                message += "\n\nUpcoming:"
                for m in milestones[:5]:
                    title = m.get("title", "Untitled")
                    due = m.get("due_on", "no due date")
                    open_count = m.get("open_issues", 0)
                    message += f"\n- **{title}** — due {due} ({open_count} open issue{'s' if open_count != 1 else ''})"
                if count > 5:
                    message += f"\n\n...and {count - 5} more."
        else:
            message = "You don't have any open milestones right now."

        return IntentProcessingResult(
            success=True,
            message=message,
            intent_data={
                "category": "query",
                "action": "list_milestones_query",
                "context": {"milestone_count": len(milestones) if milestones else 0},
            },
        )
    except Exception as e:
        self.logger.error(f"Failed to list milestones: {e}")
        return IntentProcessingResult(
            success=True,
            message="I wasn't able to fetch milestones right now. Please try again in a moment.",
            intent_data={"category": "query", "action": "list_milestones_query", "context": {"error": str(e)}},
        )
```

`_handle_list_releases_query` mirrors with releases-specific format (latest 5 by `published_at`, show `tag_name` + `name` + date).

**Acceptance**:
- 6-8 tests per handler covering: populated list, single-item, empty, error path, intent_data emission
- Manual smoke per Phase 0.8

**Estimate**: 2 hr

---

## Phase 6: Tests + verification

**Total target**: ~50 new tests across:
- Adapter (Phase 1): ~10 tests
- Router (Phase 2): ~5 tests
- Pre-classifier (Phase 3): ~16-20 tests
- Registry + lens (Phase 4): ~4 tests
- Handlers (Phase 5): ~12-16 tests

**Verification**:
- [ ] `pytest tests/unit/services/intent_service/ -v` — no regressions
- [ ] `pytest tests/unit/services/mcp/consumer/test_github_adapter*.py -v` — all passing including new methods
- [ ] `pytest tests/unit/services/intent/test_intent_service*.py -v` — new handlers covered
- [ ] Pre/post merge regression sweep on full unit suite
- [ ] Manual smoke per Phase 0.8

**Estimate**: 1 hr (most tests fall out of phases 1-5)

---

## Phase Z: Handoff

- [ ] Issue #1039 closed properly per close-issue-properly skill: description checkboxes resolved FIRST, state-transition SECOND
- [ ] Cross-reference #864 (split origin), #1040 (sibling), #855 (parent), #1042 (unblocker)
- [ ] Session log updated with phase-by-phase commits
- [ ] Branch merged to main; sign-off discipline checklist run

---

## Total Estimate

~7-8 hours.

## Risks

- **Low-Medium**: GitHub API rate-limiting if user repeatedly queries — existing adapter handles via retry; not new
- **Low**: empty-state copy decisions may benefit from CXO/MUX review — already covered by **#1043** post-MVP en-masse copy review followup
- **Low**: pre-classifier pattern shadowing — must add new patterns after existing list_issues / stale_prs in dispatcher
- **Low**: Default-repo fallback uses #1042's resolution path; if no repo can be resolved, returns graceful empty list (not an error)

## Dependencies

- ✅ #1042 PRE-1039 cleanup (shipped 2026-05-04 — provides per-call repo resolution + adapter required-arg shape + router internal-resolution helper)
- ✅ Existing GitHub MCP adapter infrastructure
- ✅ Existing pre-classifier dispatch
- ✅ Existing intent_service handler dispatch

## Audit Cascade Matrix (Issue → Gameplan)

| Template Requirement | Status | Notes |
|---|---|---|
| Issue number referenced | ✅ | #1039 in header |
| Problem statement | ✅ | Pre-classifier gap for milestones + releases |
| Phase -1 infra verification | ✅ | All deps confirmed; #1042 unblocker shipped |
| Phase 0 GitHub investigation | ✅ | API endpoints documented; cross-refs to #864/#1040/#855/#1042 |
| Phase 0.5 FE-BE contract | ✅ | Conversational message; no UI surface |
| Phase 0.6 Data flow | ✅ | Diagrammed end-to-end on top of #1042 resolution |
| Phase 0.7 Conversation design | ✅ | Example queries, no trust gate, MUX tone, copy-review-deferred-to-#1043 |
| Phase 0.8 Post-completion verification | ✅ | Smoke list |
| Phases 1-N with estimates | ✅ | 6 phases, ~7-8 hr total |
| Acceptance criteria per phase | ✅ | All listed |
| Test strategy | ✅ | ~50 tests across phases |
| Phase Z handoff | ✅ | Evidence, cross-refs, sign-off, **close-issue-properly skill** explicitly referenced |
| Dependencies listed | ✅ | All present; #1042 shipped |
| Risks identified | ✅ | 4 risks called out |
| File paths cited | ✅ | All references include grep-able paths |

### Audit ✅ Items — PM Dispositions (2026-05-04)

**✅ Q1**: Sequencing. **PM** + Lead Dev: one PR. Milestones + releases share scaffolding; splitting would mean running setup-tear-down twice without testing-isolation benefit. *"Split related issues"* memory applies to different concerns; these are nearly the same concern.

**✅ Q2**: Lens. **PM**: "yes." Both `list_milestones_query` and `list_releases_query` → `ConversationalLens.PROJECTS` (actual enum name; plural matches `project_status` precedent).

**✅ Q3**: State filter for milestones. **PM**: *"I don't like shaky nonfunctional features — maybe we just withhold till the status has meaning?"* — strong instinct; same precedent as #1031 topic-tabs. Disposition:
- Drop `\bopen milestones?\b` and `\bclosed milestones?\b` patterns from Phase 3
- Handler always returns `state="open"` with no user-facing qualifier path
- File post-MVP follow-up issue tracking deferred state-filter capability so deferral is traceable

**✅ Q4**: Pre-release filter. **PM**: "agreed" (with Q3). Same disposition shape:
- Drop `\bpre[- ]releases?\b` pattern from Phase 3
- Handler returns all releases; shows prerelease flag inline where useful (e.g., "v1.2.0-beta (pre-release)")
- Folded into same post-MVP follow-up as Q3

**✅ Q5**: "What version are we on?" handling. **PM**: "A works for me." `list_releases_query` action handles this; handler infers latest-non-prerelease and presents prominently. No dedicated `current_version_query` action.

### Followup issue to file during Phase Z

- **POST-MVP: GitHub query state/prerelease filters** — wire `state=open|closed|all` for milestones + `prerelease`-only filter for releases. Ships once the underlying surfaces have meaningful presentation for the additional states (per PM Q3 instinct: don't ship shaky nonfunctional features).
