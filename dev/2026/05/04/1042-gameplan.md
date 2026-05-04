# Gameplan: #1042 PRE-1039 Remove hardcoded 'piper-morgan-product' repo default in GitHub adapter + handlers

**Issue**: #1042
**Branch**: `claude/1042-repo-default-cleanup`
**Drafted**: 2026-05-04 by Lead Developer
**Template**: gameplan-template.md v9.3

---

## Summary

Remove the silent `piper-morgan-product` (and `piper-morgan`) repo defaults that have propagated across the GitHub MCP adapter, integration router, intent-service handlers, and several adjacent surfaces. Replace with **per-call repo resolution**: project-scoped → user-default-preference → graceful "which repo?" error. Pre-work for #1039 + #1040 so new methods don't inherit the same anti-pattern.

PM 2026-05-03: *"let's not use my repo for this project as a default anymore!"*

---

## Phase -1: Infrastructure Verification

### Hardcoded callsite inventory (full sweep — broader than issue body's "initial sweep")

**Direct `"piper-morgan-product"` defaults**:
| File | Line | Method | Notes |
|---|---|---|---|
| `services/mcp/consumer/github_adapter.py` | 253 | `list_github_issues_direct(repo, owner)` | **Also has hardcoded `owner="mediajunkie"`** |
| `services/mcp/consumer/github_adapter.py` | 313 | `get_closed_issues(repo)` | |
| `services/mcp/consumer/github_adapter.py` | 347 | `get_github_issue_direct(issue_number, repo, owner)` | **Also has hardcoded owner** |
| `services/mcp/consumer/github_adapter.py` | 631 | `list_issues_via_mcp(repo)` | |
| `services/mcp/consumer/github_adapter.py` | 701 | `get_issue_via_mcp(issue_number, repo)` | |
| `services/integrations/github/github_integration_router.py` | 207 | `repo=repo_name or "piper-morgan-product"` | Fallback when caller doesn't pass |
| `services/intent/intent_service.py` | 3134, 3432, 3477, 3641, 3684, 3825 | 6 handler callsites | Literal strings (not arg defaults) |
| `services/queries/query_router.py` | 908 | Literal | |
| `services/queries/query_router_spatial_migration.py` | 133 | `{"owner": "mediajunkie", "name": "piper-morgan-product"}` | |

**`"piper-morgan"` (no -product suffix) callsites**:
| File | Line | Notes |
|---|---|---|
| `services/mcp/consumer/consumer_core.py` | 148, 189, 198 | `kwargs.get("repo", "piper-morgan")` fallbacks |
| `services/intent/intent_service.py` | 3882, 9600 | `repository="piper-morgan"` literals |
| `services/features/morning_standup.py` | 215, 310 | `["piper-morgan"]` active-repos lists |
| `services/place/place_service.py` | 61 | `get_github_place(repo_name="piper-morgan")` default |

**Excluded (NOT repo references)** — service-name / JWT-issuer / User-Agent / keychain-service identifiers; these legitimately use "piper-morgan" as the product/service name, not as a repo.

### Resolution-strategy infrastructure check

| Capability | Status | Path |
|---|---|---|
| `Repository` domain model | ✅ exists | `services/domain/models.py:348` + `RepositoryDB` at `services/database/models.py:864` |
| `ProjectRepositoryLink` (project ↔ repo association) | ✅ exists | `services/domain/models.py:397` + DB at `:939` |
| Project-scoped repo resolution helper | ❌ missing | Repository links exist; need a helper that returns the repo for the current project context |
| User-default-repo preference key | ❌ missing | No `default_repo` preference exists in `UserPreferenceManager`; would need to be added (mirror `CALENDAR_SETUP_OFFERED` pattern from #790) |
| "Current project" context | ⚠️ partial | Some surfaces have project context (e.g., `/projects/{id}` URL); chat surfaces don't have ambient project context |

**Conclusion**: Resolution strategy 1 (project-scoped) is doable but needs a helper. Strategy 2 (user-default preference) requires new preference-key infra. Strategy 3 (graceful error) is straightforward. Risk: Medium — meaningfully larger than the issue body suggests; needs scope decision before phase 1.

---

## Phase 0: GitHub Investigation

- [ ] Re-read #1042, #1039, #1040 bodies for any cross-issue scope notes
- [ ] Confirm M2e gate language doesn't already presume the cleanup is finished
- [ ] Skim `RepositoryRepository` (services/database/repositories.py around `get_project_links`) for the API shape we'd consume
- [ ] Check whether any ADR (#866 era?) prescribes the repo-resolution decision tree

---

## Phase 0.5: Frontend-Backend Contract

No new UI. The user-facing change is **conversational**: when a query can't resolve a repo, Piper says *"Which repo would you like to look at?"* (or similar) instead of silently using the dev team's repo. Resolution decisions happen server-side; chat surfaces are unchanged structurally.

---

## Phase 0.6: Data Flow

```
GitHub query handler (e.g., _handle_list_issues_query)
  ↓
Resolve repo via per-call helper:
  1. Did caller pass a repo arg explicitly? → use that
  2. Is there project context (URL/session)? → look up linked Repository
  3. Does user have a default_repo preference? → use it
  4. None of the above? → return UnresolvedRepoError → handler emits "Which repo?"
  ↓
GitHubIntegrationRouter wraps with the resolved repo
  ↓
GitHubAdapter calls API with the resolved repo (no default fallback at adapter level)
```

**Helper shape (proposal)**:
```python
@dataclass
class ResolvedRepo:
    owner: str
    name: str
    source: Literal["explicit", "project", "user_default"]

class UnresolvedRepoError(Exception):
    """Raised when no repo can be resolved for a query."""

async def resolve_repo(
    *,
    user_id: Optional[UUID],
    project_id: Optional[str],
    explicit: Optional[str] = None,  # "owner/name" string from caller
) -> ResolvedRepo: ...
```

---

## Phase 0.7: Conversation Design

When `UnresolvedRepoError` is raised in a handler, the response message should be empathetic + actionable:

> "I don't know which repo you mean — tell me 'owner/repo' or link a repository to this project on the integrations page."

Stage variants and copy refinement out of scope for MVP (one wording across stages, mirror #790 Q2 disposition).

---

## Phase 0.8: Post-Completion Verification

- [ ] Manual smoke: as a user with no project context + no default repo, run `_handle_list_issues_query` → see graceful "which repo?" message
- [ ] Manual smoke: as a user inside a project that has a linked repository → see issues for that repo
- [ ] Manual smoke: as a user with a configured default-repo preference → see issues for that repo
- [ ] CI tests pass; no regressions in existing GitHub query handlers

---

## Phase 1: Repo-resolution helper

**Files**:
- `services/integrations/github/repo_resolver.py` (new, ~120 LOC) — `resolve_repo()` + `ResolvedRepo` dataclass + `UnresolvedRepoError`
- Reads `ProjectRepositoryLink` via `RepositoryRepository.get_project_links` (or similar)
- Reads user-default via `UserPreferenceManager.get_default_repo` (Phase 1.5 helper)

**Acceptance**:
- Pure async function (no global state)
- ~15-20 unit tests covering all branches: explicit arg, project-scoped, user-default, unresolved, project-with-multiple-linked-repos (return first? error? PM Q2 below)

**Estimate**: 2 hr

---

## Phase 1.5: User default-repo preference (mirror #790 pattern)

**Files**:
- `services/domain/user_preference_manager.py` — add `DEFAULT_REPO = "default_repo"` key + `get_default_repo` / `set_default_repo` helpers (mirror `CALENDAR_SETUP_OFFERED` pattern)
- Validation: `"owner/name"` format

**Acceptance**:
- Preference key + helpers
- ~6-8 unit tests
- Note: no UI for setting this preference yet (out of scope for #1042; could be filed as follow-up if PM wants)

**Estimate**: 45 min

---

## Phase 2: Adapter cleanup

**Files**:
- `services/mcp/consumer/github_adapter.py` — 5 methods + 2 owner-defaults

**Approach**: change signature so `repo` is required (no default). Callers must pass an explicit value. Existing internal callers (router) updated to pass through.

```python
# Before
async def list_github_issues_direct(
    self, repo: str = "piper-morgan-product", owner: str = "mediajunkie"
): ...

# After
async def list_github_issues_direct(
    self, repo: str, owner: str
): ...
```

**Acceptance**:
- All 5 adapter methods take `repo: str` (no default) + `owner: str` (no default where applicable)
- Adapter unit tests updated to pass explicit args
- 0 regressions in adapter test suite

**Estimate**: 1.5 hr

---

## Phase 3: Integration router cleanup

**Files**:
- `services/integrations/github/github_integration_router.py` — line 207 fallback removed; router now requires resolved repo from caller

**Acceptance**:
- Router methods take `repo: str` from resolved value
- Router internal call to adapter passes through unchanged

**Estimate**: 30 min

---

## Phase 4: Handler thread-through (intent_service.py + others)

**Files**:
- `services/intent/intent_service.py` — 6 hardcoded `"piper-morgan-product"` callsites + 2 `"piper-morgan"` callsites
- For each handler that calls a GitHub method: wire `resolve_repo()` at the top, propagate or render UnresolvedRepoError as graceful message
- `services/queries/query_router*.py` — 2 callsites (verify if they're hot or dead code)
- `services/mcp/consumer/consumer_core.py` — 3 fallbacks (verify if reachable from production paths)
- `services/features/morning_standup.py` — 2 callsites (PM Q3 below: do these need same treatment?)
- `services/place/place_service.py` — 1 default arg

**Acceptance**:
- All listed callsites use `resolve_repo()` or pass through caller's resolved repo
- Handler-level tests assert UnresolvedRepoError → graceful message path
- 0 regressions in existing GitHub query handler tests

**Estimate**: 3-4 hr (depends heavily on which downstream callsites PM scopes in vs out)

---

## Phase 5: Tests + verification

**Total target**: ~45-60 new tests across phases.

**Verification**:
- [ ] `pytest tests/unit/services/mcp/consumer/test_github_adapter*.py -v` no regressions
- [ ] `pytest tests/unit/services/intent/test_intent_service*.py -v` no regressions on GitHub-handler tests (some may need updates)
- [ ] `pytest tests/unit/services/integrations/github/` no regressions
- [ ] Pre/post merge regression sweep on full unit suite
- [ ] Manual smoke per Phase 0.8

**Estimate**: 1.5 hr (most tests fall out of phases above)

---

## Phase Z: Handoff

- [ ] #1042 closed with implementation evidence (per close-issue-properly skill — description checkboxes resolved FIRST)
- [ ] Cross-reference #1039 (unblocks) + #1040 (also unblocks) + #1043/copy-review (related)
- [ ] Memory entry update if any new patterns surfaced
- [ ] Session log updated with phase-by-phase commits
- [ ] Branch merged to main; sign-off discipline checklist run

---

## Total Estimate

~10-12 hours (significantly larger than the issue body suggested; reflects full-sweep scope including #intent_service.py + adjacent files).

## Risks

- **Medium**: behavior change — queries that previously silently worked against `piper-morgan-product` will now fail with "which repo?" if user has no project context AND no default-repo preference. This is desired but **needs migration path**: an env-var fallback for dev environments? a one-time migration setting `default_repo=piper-morgan-product` for current users? See PM Q4.
- **Medium**: tests that mock adapter methods without args may break en masse. Phase 2 will surface the count; some test rework expected.
- **Low**: discovery of additional callsites during phase 4 — full grep already done but downstream handlers may have shadow paths.

## Dependencies

- All Phase -1 infra confirmed
- No external blockers

## Audit Cascade Matrix (Issue → Gameplan)

| Template Requirement | Status | Notes |
|---|---|---|
| Issue number referenced | ✅ | #1042 in header |
| Problem statement | ✅ | Hardcoded defaults across 8+ files; PM directive |
| Phase -1 infra verification | ✅ | Full callsite inventory + resolution-strategy infra audit |
| Phase 0 GitHub investigation | ✅ | Cross-refs to #1039/#1040; ADR check pending |
| Phase 0.5 FE-BE contract | ✅ | Server-side; conversational graceful-error |
| Phase 0.6 Data flow | ✅ | Resolution decision tree + helper shape |
| Phase 0.7 Conversation design | ✅ | Graceful-error copy proposed |
| Phase 0.8 Post-completion | ✅ | Smoke checklist for 3 user scenarios |
| Phases 1-N with estimates | ✅ | 5 phases + Phase 1.5; ~10-12 hr |
| Acceptance criteria per phase | ✅ | All listed |
| Test strategy | ✅ | ~45-60 tests |
| Phase Z handoff | ✅ | Closure protocol + memory update |
| Dependencies listed | ✅ | All confirmed |
| Risks identified | ✅ | 3 risks; behavior-change is the load-bearing one |
| File paths cited | ✅ | All grep-able |

### Audit ✅ Items — PM Dispositions (2026-05-04)

**✅ Q1**: Scope. **PM**: "A" — Full sweep across all 8+ files in this issue. Estimate ~10-12 hr.

**✅ Q2**: Multi-repo project resolution. **PM**: "A for MVP ... it's an edge case." First link by `created_at`; edge-case documented.

**✅ Q3**: `morning_standup.py active_repos`. **PM** (refined): "let's try to get some minimal default_repo solution working." Disposition:
- The `["piper-morgan"]` literal is REMOVED in this issue (no actual-repo-as-default left in the code anywhere)
- Replacement uses the `default_repo` preference (Phase 1.5 helper) when set; `[]` empty list otherwise + structured warning log
- Full active-repos resolution (per-project + per-user fully wired) is filed as a followup issue

**✅ Q4**: Migration path. **PM**: "B" — `PIPER_DEFAULT_REPO` env var as dev/last-resort fallback; logs deprecation warning when used; production graceful-error path otherwise.

**✅ Q5**: Owner cleanup. **PM**: "yes and again my github username (mediajunkie) does not belong in the core product!" Scope expanded — full grep across services/ + web/ for `mediajunkie` reveals MORE callsites than just the 2 originally flagged:

**Full `mediajunkie` inventory (in scope for this issue)**:
| File | Line(s) | Type |
|---|---|---|
| `services/configuration/piper_config_loader.py` | 397, 399 | Config defaults |
| `services/config/github_config.py` | 82, 83 | GitHubConfig dataclass defaults |
| `services/intent_service/canonical_handlers.py` | 4322, 4458 | **🚨 USER-FACING chat messages** ("e.g., mediajunkie/piper-morgan"; "'unlink mediajunkie/piper-morgan from Piper Morgan'") |
| `services/queries/query_router_spatial_migration.py` | 133, 262 | Spatial migration defaults |
| `services/mcp/consumer/github_adapter.py` | 185, 222, 249, 314 | Endpoint URL templates (string formatting) |
| `services/integrations/spatial/github_spatial.py` | 422 | Endpoint URL template |
| `services/place/place_service.py` | 103, 117 | `source_url` fallback strings |
| `services/domain/models.py` | 359, 361, 1070 | Docstring examples + sample URL — sanitize to generic placeholders |

The chat-message templates at `canonical_handlers.py:4322, 4458` are the worst offenders — they actively show PM's username to users.

**✅ Q6**: User-default preference UI. **PM**: "let's fold it into #869." Default-repo preference UI scope folded into #869 (Project config IA). Will comment on #869 + update its scope at next walkthrough refresh.

### Updated total estimate

~12-14 hours (from ~10-12; expanded by full mediajunkie sweep + chat-message template fixes).

### Followup issues to file during Phase Z

1. **STANDUP-ACTIVE-REPOS**: full active-repos resolution (per-project + per-user fully wired); supersedes the minimal default_repo treatment landing here
