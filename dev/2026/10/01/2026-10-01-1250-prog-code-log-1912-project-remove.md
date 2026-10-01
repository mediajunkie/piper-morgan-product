# 2026-10-01 1250 — prog (Coding Agent), Sonnet — #1912 project Remove no-op

Dispatched by Lead Developer. Worktree: `~/Development/piper-morgan-worktrees/lead` (branch
`claude/lead-cycle`). Did NOT commit/stage/touch the git index — Lead integrates. No LLM calls.

## Issue

[#1912](https://github.com/mediajunkie/piper-morgan-product/issues/1912) — PM clicked Remove on
the "One Job" project in Settings → Projects, got a success toast, but the project stayed listed
(chat's duplicate-check still saw it; `show my projects` still listed it).

## Investigation

Lead's dispatch pointed at `templates/components/project_config_panel.html` (~306, ~522) as the
two `DELETE` fetches to check. Read the whole file: both are real, already-correct DELETE calls,
but neither is project removal — one is "unlink repo from project"
(`/api/v1/repositories/{repoId}/projects/{projectId}`), the other is "remove an integration"
(`/api/v1/projects/{projectId}/integrations/{integrationId}`). Config panel only renders on a
project's own Detail page; `settings_projects.html` (the actual `/settings/projects` route) is an
overview list with no delete button at all — it only links to `/projects/{id}?tab=settings`.

The real "Remove a project" button lives on `templates/projects.html` (`/projects`, linked from
Settings → Projects via "All Projects"). Read the whole `deleteProject()` handler there and found
the mechanism immediately:

```js
function deleteProject(projectId) {
  Dialog.confirm({
    ...
    onConfirm: async () => {
      try {
        // TODO: Call API to delete
        // await fetch(`/api/v1/projects/${projectId}`, { method: 'DELETE' });

        ToastMessages.success('project_deleted');
        await loadProjects();
      } ...
    }
  });
}
```

**Root cause: the DELETE fetch was a commented-out TODO stub.** The confirm dialog fired, a
success toast fired *unconditionally*, and `loadProjects()` re-fetched the same still-present
project from the server — nothing was ever sent to the backend. This is #1824's bucket exactly:
reporting an outcome that was never measured.

Checked whether this was secretly archive-vs-delete semantics (per the task's framing) — it
isn't. The backend route (`web/api/routes/projects.py:499` `delete_project`) and repository
(`services/database/repositories.py:194` `BaseRepository.delete`) are **already correct**: a real
hard delete (`session.delete(entity)`, fixed in #1464's un-awaited-coroutine bug), owner-scoped
(`get_by_id(project_id, owner_id=current_user.sub)`), honest 404 on not-found/not-owned (can't
distinguish the two — both 404 the same way, which is fine/intentional for not leaking existence
to a non-owner), 500 on repo failure. The confirm dialog's own copy ("This can't be undone")
confirms hard-delete was the intended design — no archive semantics to reconcile, so the
duplicate-check in `canonical_handlers.py:4958` (`find_by_name(..., include_archived=False)` by
default) was never actually implicated — it was correctly reporting the project as still existing
because it still existed.

## Fix

`templates/projects.html::deleteProject()` — replaced the stub with a real `fetch(DELETE)` that:
- 404 → `not_found` toast ("may already be gone, or is not yours to remove"), refreshes list, returns.
- `!response.ok` (other error) → `delete_error` toast, returns (no optimistic reload needed; nothing changed).
- 2xx but body `status !== 'deleted'` → never treated as success; `delete_error` toast, refreshes list.
- body `status === 'deleted'` → `project_deleted` success toast, refreshes list.
- network/throw → `delete_error` toast (existing catch, untouched).

Success is now gated on the **response body**, not `response.ok` alone, per the task brief. Every
branch that believes it knows the new state re-fetches from the server (`loadProjects()`) rather
than just removing the row client-side.

## Tests

- `tests/unit/web/api/routes/test_projects.py` — new `TestDeleteProjectRoute1912` (5 tests): success
  returns `{"status": "deleted", "project_id": ...}` and body is asserted; owner-scoping
  (`get_by_id` called with `owner_id=`); not-found/not-owned → 404, `delete` never called; repo
  exception → 500. Route was already correct; these pin it against regression now that the
  template actually depends on it.
- `tests/unit/web/test_project_remove_honest_1912.py` — new file, 5 tests, source-pin on the
  shipped template (same pattern as `test_setup_wizard_step1_honest_1875.py` — no browser/DOM
  harness in this suite, so it proves shipped source, not runtime behavior): TODO stub gone; real
  endpoint called; success-toast ordering is fetch → ok-check → body-read → body-status-check →
  success (not `response.ok` alone); 404 branch refreshes list before returning; every outcome
  branch calls `loadProjects()` (count >= 3).

## Gate results

```
ruff format tests/unit/web/api/routes/test_projects.py tests/unit/web/test_project_remove_honest_1912.py
  2 files reformatted (first pass) / left unchanged (verify pass)
ruff check --fix (same files)
  All checks passed!

POSTGRES_PORT=5433 python -m pytest tests/unit/web/ \
  tests/unit/services/intent_service/test_*project*.py \
  tests/unit/services/intent_service/test_*portfolio*.py -q
  1255 passed, 73 warnings in 24.79s   EXIT STATUS: 0

POSTGRES_PORT=5433 python -m pytest tests/test_architecture_enforcement.py -q
  63 passed, 1 xfailed in 11.85s        EXIT STATUS: 0
```

Targeted run of just the new/changed tests also captured for clarity:
`tests/unit/web/api/routes/test_projects.py tests/unit/web/test_project_remove_honest_1912.py -v`
→ **30 passed**, 0 failed.

## Files touched

- `templates/projects.html` — `deleteProject()` fix (modified)
- `tests/unit/web/api/routes/test_projects.py` — `TestDeleteProjectRoute1912` added (modified)
- `tests/unit/web/test_project_remove_honest_1912.py` — new source-pin test file

Not touched (excluded lanes per dispatch): `services/intent_service/todo_handlers.py`,
`scripts/build_inversion_corpus_phase0.py`, `tests/fixtures/inversion_corpus_phase0.yaml`,
`tests/unit/test_inversion_phase3_deletion_1595.py`.

## Verified how

Method: ran the exact gate commands above in this worktree this turn and quoted their actual
output (not recalled from an earlier run). Layer: unit/route-level (`TestClient` against the real
FastAPI router with mocked repository, per the existing `test_projects.py` pattern) for the
backend; a static source-pin (file read + substring/ordering assertions, m-43 — this is NOT a
browser render test, it cannot prove the fix works in an actual click-through) for the frontend
fix. Denominator: covers `templates/projects.html`'s `deleteProject()` handler and the
`DELETE /api/v1/projects/{project_id}` route; does not cover `project_config_panel.html`'s
repo-unlink/integration-remove (different, unaffected, already-correct DELETE calls) or a live
browser session — Lead/PM re-test in the running app is the next verification layer per the
dispatch brief.

Did not commit, stage, or touch the git index — handing back to Lead for integration.

## Memory & briefing surfaces referenced this session

**Referenced:**
- `docs/internal/architecture/current/intent-routing-stack.md` was NOT needed — this is template/route
  work, not classification/dispatch, confirmed by scope before starting.
- CLAUDE.md "Verify First, Create Second" — read the whole `deleteProject()` function and the whole
  `project_config_panel.html` file before concluding where the bug lived; this is what caught that the
  Lead's line-number hypothesis (pointing at the config panel) was for a different, already-correct
  pair of DELETE calls.
- CLAUDE.md "Name the layer, and state the denominator" (m-43/m-44) — shaped the `Verified how:` section
  and the explicit "this is a source pin, not a render test" framing in the new test file's docstring.

**Loaded but not referenced:** worktree/mailbox/sign-off discipline sections (not applicable — prog
subagent, no commit authority this task).

**Wanted but not found:** nothing — the issue and code were self-contained enough to resolve without
needing additional context surfaces.
