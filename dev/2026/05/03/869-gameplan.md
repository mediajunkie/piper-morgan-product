# Gameplan: #869 Project configuration IA — Project Detail as primary, Settings as overview

**Issue**: #869
**Branch**: `claude/869-project-config-ia`
**Drafted**: 2026-05-03 by Lead Developer
**Template**: gameplan-template.md v9.3

---

## Summary

Resolve duplicate-config-UI ambiguity by making **Project Detail page** the canonical configuration surface for a single project (with a Config tab), and reshaping **Settings → Projects** as an overview-list that links *to* Project Detail rather than re-implementing the config UI.

CXO Option C (Both) per 2026-02-28 memo. No #861 rework — Settings → Projects survives but evolves; Project Detail gains a Config tab.

---

## Phase -1: Infrastructure Verification

**Status**: ✅ Done (2026-05-03 spike — `dev/2026/05/03/m2e-phase-minus-1-infra-spike.md`).

| Surface | Status |
|---|---|
| `templates/project_detail.html` (446 LOC, no tabs currently) | ✅ Present — needs tab structure added |
| `templates/projects.html` (project list, 433 LOC) | ✅ Present |
| `templates/settings_projects.html` (1044 LOC; full config UI) | ✅ Present — needs trimming to overview-list-only |
| `web/api/routes/ui.py:468` (`/projects/{project_id}` route) | ✅ Present |
| API endpoints `/api/v1/projects/...`, `/api/v1/projects/{id}/repositories`, `/api/v1/projects/{id}/integrations` | ✅ Used by settings_projects.html — same APIs serve Project Detail Config tab |
| `#861` (interim Settings → Projects) | ✅ Closed; per CXO memo no rework required |
| URL pattern `/projects/{id}?tab=settings` | ❌ Not implemented — needs query-param-driven tab activation |

**Conclusion**: All API endpoints + templates exist. Front-end-heavy work + light cross-page navigation refactor. Risk: Medium (UX surface change; needs visual review).

---

## Phase 0: GitHub Investigation

- [ ] Re-read #869 + CXO 2026-02-28 memo (already linked in body)
- [ ] Re-read PDR-003 (first-class entities) for any updated framing
- [ ] Confirm #861 closure includes Settings → Projects implementation we're now reshaping
- [ ] Skim `templates/components/` for any existing tab component

---

## Phase 0.5: Frontend-Backend Contract

**No new API endpoints**. Both Project Detail Config tab and Settings → Projects use the same existing endpoints:
- `/api/v1/projects/{id}` (project metadata)
- `/api/v1/projects/{id}/repositories` (linked repos)
- `/api/v1/projects/{id}/integrations` (project integrations)
- `/api/v1/repositories/{repo_id}/projects/{project_id}` (link/unlink repo)

The change is purely in the **templates + JS** layer.

---

## Phase 0.6: Data Flow

```
Path A: User on a project, wants to add a repo
  → /projects/{id}  (Overview tab default)
  → User clicks "Config" tab
  → /projects/{id}?tab=settings  (URL updates without navigation; tab activates)
  → Repo + integration UI loads (same components used by settings_projects)

Path B: User wants to review all integrations
  → /settings/projects  (overview list)
  → Sees row per project: name + repo-count + integration-count + last-activity
  → Clicks a project row → /projects/{id}?tab=settings  (lands on Config tab)
  → Same Config UI

Two paths → one canonical config UI.
```

---

## Phase 0.7: UX Design

**Project Detail page tabs** (3 proposed; PM Q below):
- **Overview** (default, current page content): project name, description, work items
- **Config**: linked repositories + integrations (extracted from settings_projects)
- **Activity** (optional, post-MVP): recent events / commits / PR mentions

**Settings → Projects overview list** (post-trim):
- Table: Project Name | Repo Count | Integration Count | Last Activity | Actions
- Clicking a row → `/projects/{id}?tab=settings`
- Removes inline config form (delete the duplicated repo/integration management forms)
- Keeps "Create new project" CTA (existing)

**URL contract**:
- `/projects/{id}` → Overview tab default
- `/projects/{id}?tab=settings` → Config tab active
- `/settings/projects` → Overview list (no inline config)

**Visual**: tab-style component (likely existing or new — Phase 0 spike checks `templates/components/`). If no tab component exists, add a lightweight one to `templates/components/tabs.html` (~80 LOC).

**MUX-consciousness**: A user who arrives at Project Detail by clicking a project from anywhere should never wonder "where do I configure this?" — answer: right here, click Config. A user who wants the cross-project view goes to Settings.

---

## Phase 0.8: Post-Completion Verification

- [ ] Manual smoke as user:
  - Navigate to `/projects/{id}` → Overview tab default; project loads
  - Click Config tab → URL updates to `?tab=settings`; repos + integrations load
  - Direct-link to `/projects/{id}?tab=settings` → lands on Config tab directly
  - Add/remove a repo from Project Detail Config tab → persists
  - Add/remove an integration → persists
  - Navigate to `/settings/projects` → overview list shows all projects with status
  - Click a project row → lands on `/projects/{id}?tab=settings`
  - Settings → Projects has NO inline config UI (just the overview)
- [ ] No broken navigation between pages
- [ ] Existing `/settings/projects` API calls still work (backward compat with bookmarks)
- [ ] CI tests pass; no E2E regressions

---

## Phase 1: Tab component + Project Detail tab structure

**Files**:
- `templates/components/tabs.html` (new) — generic tabs component (Jinja partial + JS for activation)
- `templates/project_detail.html` — restructure layout to wrap content in a tab container; tabs: Overview (current content) + Config (placeholder for Phase 2)

**Acceptance**:
- Tab component handles 2-N tabs declaratively
- URL query param `?tab=...` activates corresponding tab on load
- Clicking a tab updates URL via `history.replaceState` (no page reload)
- Default tab = first if no query param
- 6-8 unit tests on the JS tab activation logic (Jest-style or Pytest harness)
- Existing Project Detail content lives entirely under Overview tab; nothing breaks

**Estimate**: 2.5 hr

---

## Phase 2: Project Detail Config tab content

**Files**:
- `templates/project_detail.html` — populate Config tab with linked-repos + integrations sections
- Reuse JS/HTML from `templates/settings_projects.html` — extract into `templates/components/project_config_panel.html` (shared partial)
- Update `settings_projects.html` to use the same partial (Phase 3 will trim it differently — for Phase 2 just consolidate the markup)

**Acceptance**:
- Config tab loads linked repos via existing `/api/v1/projects/{id}/repositories`
- Config tab loads integrations via existing `/api/v1/projects/{id}/integrations`
- Add/remove repo + add/remove integration flows work identically to current Settings → Projects
- 8-10 frontend tests covering tab content load + actions

**Estimate**: 3 hr

---

## Phase 3: Settings → Projects overview reshape

**Files**:
- `templates/settings_projects.html` — strip the inline config UI; replace with overview list:
  - Table per project: name, repo count, integration count, last-activity
  - Each row links to `/projects/{id}?tab=settings`
  - Keeps "Create new project" CTA
- `web/api/routes/...` — confirm if a "project status summary" endpoint exists (`/api/v1/projects` likely returns enough; if not, lightweight enrichment to include repo_count + integration_count)

**Acceptance**:
- Settings → Projects no longer has inline repo/integration forms
- Overview list shows status summary per project
- Clicking a row routes to Project Detail Config tab
- Bookmarks to `/settings/projects` still work (page just looks different)
- 6-8 tests covering overview list + click-through

**Estimate**: 2.5 hr

---

## Phase 4: Cross-page navigation tightening

**Files**:
- `templates/projects.html` — confirm project list rows link to `/projects/{id}` (not `?tab=settings` — overview is default landing)
- `templates/components/navigation.html` — verify Settings link goes to `/settings/projects` (overview), not the old config UI

**Acceptance**:
- All "Configure project" CTAs lead to `/projects/{id}?tab=settings`
- All "All projects" CTAs lead to `/settings/projects`
- No orphan links to deleted/refactored sections

**Estimate**: 45 min

---

## Phase 5: Tests + verification

**Total target**: ~30 frontend/integration tests across phases.

**Verification**:
- [ ] `pytest tests/unit/templates/test_project_detail*.py -v`
- [ ] `pytest tests/unit/templates/test_settings_projects*.py -v`
- [ ] Pre/post merge regression sweep
- [ ] Manual smoke per Phase 0.8 (full path A + path B)
- [ ] Visual review screenshot saved to dev/2026/05/MM/

**Estimate**: 1 hr

---

## Phase Z: Handoff

- [ ] Issue #869 closed with evidence
- [ ] Cross-reference #861 (interim implementation), CXO 2026-02-28 memo, PDR-003
- [ ] Session log updated; branch merged; sign-off discipline run

---

## Total Estimate

~10 hours (front-end-heavy; visual review checkpoints).

## Risks

- **Medium**: existing JS in `templates/settings_projects.html` (1044 LOC) is intermixed with config-form logic + event handlers. Extraction must be clean — risk of regression on existing functionality.
- **Medium**: tab component if not present needs to be generic enough for future use (#869 sets the IA pattern for PDR-003 first-class entities).
- **Low**: `/settings/projects` URL change perception — users with bookmarks still land on a valid page, just rearranged content. Not a breaking change.

## Dependencies

- All Phase -1 infra ✅
- #861 closed ✅
- No new dependencies on other M2 issues

## Audit Cascade Matrix (Issue → Gameplan)

| Template Requirement | Status | Notes |
|---|---|---|
| Issue number referenced | ✅ | #869 |
| Problem statement | ✅ | Two valid IA paths → one canonical config UI |
| Phase -1 infra verification | ✅ | All templates + endpoints present |
| Phase 0 GitHub investigation | ✅ | CXO memo + PDR-003 + #861 cross-refs |
| Phase 0.5 FE-BE contract | ✅ | No new endpoints; existing APIs |
| Phase 0.6 Data flow | ✅ | Path A and Path B diagrammed |
| Phase 0.7 UX/Conversation design | ✅ | 3-tab proposal, URL contract, MUX framing |
| Phase 0.8 Post-completion verification | ✅ | Comprehensive smoke list |
| Phases 1-N with estimates | ✅ | 5 phases, ~10 hr total |
| Acceptance criteria per phase | ✅ | All listed |
| Test strategy | ✅ | ~30 tests |
| Phase Z handoff | ✅ | Evidence, cross-refs, sign-off |
| Dependencies listed | ✅ | All present/closed |
| Risks identified | ✅ | 3 risks |
| File paths cited | ✅ | All grep-able |

### Audit ✅ Items — PM Dispositions (2026-05-03)

**✅ Q1**: Tab structure. **PM**: "yes A is fine — thanks for the context." Option A: 2 tabs (Overview + Config) for MVP. Activity tab design + content tracked by **#1045** (POST-MVP Project Detail Activity tab).

**✅ Q2**: Tab component creation. **PM**: "acceptable." Generic tabs partial may be created during execution if Phase 0 verifies none exists.

**✅ Q3**: Settings → Projects status enrichment. **PM**: "I am OK with a lightweight backend enrichment." Lightweight enrichment of existing `/api/v1/projects` endpoint (~30 min). No separate `/api/v1/projects/overview` endpoint.

**✅ Q4**: Config tab content extraction pattern. **PM**: "ok with consolidation pattern." Transitional shared partial (`templates/components/project_config_panel.html`) used by both Project Detail and `settings_projects.html` during Phase 2; settles to single home in Project Detail after Phase 3 trim.

**✅ Q5**: Backward compatibility. **PM**: "ok without special case." `/settings/projects` keeps working as overview list. No single-project redirect special case.

**✅ Q6**: PDR-003 generalization. **PM**: "project only for now ok." Project-only for MVP; Repository / Product extensions deferred per PDR-003 Phase 1 out-of-scope per issue body.
