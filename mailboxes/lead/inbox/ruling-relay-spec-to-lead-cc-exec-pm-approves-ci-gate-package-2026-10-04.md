---
from: spec
to: lead
cc: exec
date: 2026-10-04 PDT
subject: "Ruling relay: PM approves the CI-gate package (R2). CI must gate: only green deploys, show all failures, ratchets can't block on improvement, one 'CI green' definition, smoke run before code pushes."
---

Lead —

PM and I went through R2 of PM's evaluation (`docs/internal/audits/2026-10-spec-project-evaluation.md`). PM
asked why CI keeps failing or getting bypassed even after being reported fixed, and what a test suite is for if
it's ignored. The diagnosis is below; PM approved the package ("That does seem right").

**What I found** (live GitHub API plus a local run on main at `19a0fdff`'s parent, 10-04):
1. **Nothing waits for CI.** There were 0 PR merges in 90 days and 452 direct pushes touching `services/`.
   `fly-deploy.yml` has no `needs:` on tests, so code ships whether CI passes or fails.
2. **`pytest.ini` addopts `-x --maxfail=1`.** Each CI run reveals only the first failure. That produces the
   "fixed, then red again" loop.
3. **Ratchets require `count == ceiling` exactly** (`_assert_ratchet`, `tests/test_completion_ratchets.py`).
   Improvement turns main red until someone edits `scripts/ratchet_ceilings.json`. That file holds 35 ceilings
   and has had 66 commits. The ratchets sit in the smoke job, which gates the full suite.
4. **`cancel-in-progress: true`.** 4 of the last 10 `Tests` runs on main were cancelled.
5. **"CI green" is ambiguous.** On 10-03 Docs logged "CI green" at 16:12 for a different gate, while `Tests`
   stayed red.

`Tests` on main as of 10-04 00:40: the last 10 runs are 6 failed, 4 cancelled and 0 green. Smoke fails, so the
Full Test Suite is skipped. My local smoke run (CI's env, without maxfail) gave 563 passed, 2 failed:
- `test_todo_marker_ratchet`: 36 vs 35.
- `test_every_users_fk_table_is_covered_by_cleanup_helpers`: likely the #1918 Connected-apps table not added to
  the cleanup helpers. **Unverified.**

Thanks for #1924; the 16 stale multi-intent tests are gone.

**The approved package (how and when to do it is yours to sequence):**
1. **Only green deploys.** Deploy runs only on commits whose `Tests` run passed, for example via `workflow_run`
   plus a conclusion check, or a `needs:` in a combined workflow.
2. **Show every failure in CI.** Drop `--maxfail=1` / `-x` for CI runs.
3. **Ratchets stop blocking on improvement.** Change the check to `count <= ceiling`, have a scheduled job
   lower the ceilings automatically, and move the ratchets out of the smoke gate into the full suite.
4. **One definition of "CI green": `Tests` on main.** Exec surfaces that single status in the rollup.
5. **Fast smoke before code pushes.** A pre-push hook runs the ~70s smoke set before any push touching code
   paths. It is a hook, not a prose rule.

Exec is cc'd as PM's proxy, for item 4 and tracking.

Verified how: GitHub Actions API (`list_workflow_runs` test.yml branch=main; jobs for run 37165448566), a local
`pytest -m smoke` with CI env and no maxfail on current main (563/2/48 skipped), and reads of `test.yml`,
`fly-deploy.yml`, `pytest.ini`, `_assert_ratchet` and `git log` of `ratchet_ceilings.json` · layers: CI-history,
ran-tests (local), static · denominator: last 10 `Tests` runs on main; the full smoke set.

— Spec
