# 2026-10-04 prog-code session log — item 5 pre-push smoke hook, finish

**Model**: Sonnet (Claude Sonnet 5). **Dispatched by**: Lead. **Role**: Coding Agent (prog), one-shot,
no separate mailbox/session continuity beyond this log.

**Task**: finish CI-package item 5 (pre-push smoke hook) to the conditions CIO and Pard set in the
2026-10-04 item-5 thread, so Lead/CIO can install it. Build `scripts/ensure-pytest-env.sh` (Pard's
verify-not-build shape) and the six hook changes (a)-(f) CIO/Pard specified. Test for real on this
host. Do NOT install into the common dir. Do NOT touch `services/intent_service/*`,
`.github/workflows/fly-deploy.yml`, `requirements.txt` (other lanes' territory).

## Read first
- `mailboxes/lead/read/reply-pard-to-lead-cio-item5-shared-env-and-the-one-line-that-must-not-be-copied-2026-10-04.md`
- `mailboxes/lead/inbox/finding-pard-to-lead-cio-spec-ci-skips-47-files-for-an-undeclared-aiosqlite-2026-10-04.md`
- `mailboxes/lead/inbox/reply-cio-to-pard-via-exec-lead-yes-to-verify-not-build-env-blocking-from-day-one-with-your-per-fire-log-line-2026-10-04.md`
- `mailboxes/lead/read/cosign-cio-to-lead-pard-via-exec-cc-spec-pre-push-smoke-hook-yes-with-three-conditions-2026-10-04.md`
- `mailboxes/lead/sent/reply-lead-to-pard-cio-cc-arch-spec-exec-item1-take-the-state-gate-to-arch-item5-hook-held-four-changes-2026-10-04.md`
- `scripts/ensure-ruff.sh` (pattern). `scripts/check-worktree-interpreters.sh` does NOT exist in the
  repo (searched tree + `git log --all`, no file anywhere) — treated as "equivalent" per task
  instructions: used a direct loop running `ensure-pytest-env.sh` from each worktree instead.

## Live surprise mid-task: requirements.txt changed under me
Between my first `shasum` check (key `94d244eccaea`, matching Pard's provisioned env) and writing
the script minutes later, another concurrent session committed
`0a134ccf45 deps(test): add aiosqlite==0.22.1...` directly to this shared worktree's `requirements.txt`
— exactly the fix Pard's finding called for. The key became `a5d47c8fc7b9`. This is a real, unplanned
demonstration of the invalidation Pard's design promises: old env (`94d244eccaea`) still resolves for
trees still at the old `requirements.txt`; the new key has no env until provisioned. I did **not**
touch `requirements.txt` myself (confirmed via `git status --porcelain` throughout — it never appears
in my diff). Per the task's explicit allowance ("an optional `--build` flag may exist ONLY if
trivially safe... documented as Pard's provisioning step"), I built the new-key env myself via
`ensure-pytest-env.sh --build` (46.8s, one-time) so I could actually exercise the hook — this is
Pard's own provisioning step, run by hand, not a new mechanism.

## Files
- `scripts/ensure-pytest-env.sh` (new) — Pard's shape: PY_MINOR parsed from
  `.github/workflows/test.yml`'s `python-version: "3.11"` line (falls back to hardcoded `3.11` with a
  comment if the parse fails); key = `sha256(requirements.txt)` first 12 hex chars (NOT
  `requirements.lock` — Pard's correction, lock is 5 months stale/`ResolutionImpossible`); env at
  `${XDG_CACHE_HOME:-$HOME/.cache}/piper-morgan/pytest-py${PY_MINOR}-${key}`; default mode prints the
  interpreter path + exits 0 if present, else prints nothing + exits 1; `--build` flag (documented as
  Pard's provisioning step, "ask Pard" language kept in the hook's own message) builds via
  `python${PY_MINOR} -m venv` + `pip install -r requirements.txt` only when explicitly invoked.
- `scripts/git-hooks/pre-push` (modified, still **NOT installed** — stays a tracked candidate file).

## The six conditions — what changed and how verified
**(a) Interpreter from `ensure-pytest-env.sh`, not `$top/venv/bin/python`.** Hook now calls
`"$top/scripts/ensure-pytest-env.sh"` and captures stdout. On empty/non-executable result: loud
`"pytest env not provisioned — run scripts/ensure-pytest-env.sh --build or ask Pard. Pushing
UNCHECKED."` to stderr, logs `outcome=unchecked`, exits 0. **Verified**: scenario (iv) below —
pointed `XDG_CACHE_HOME` at an empty temp dir, got exactly that message, exit 0, 0.236s.

**(b) CIO's dirty-tree warning.** `git status --porcelain | cut -c4- | grep -E "$code_re"` — if
non-empty, prints `"smoke ran against a DIRTY tree under code paths: <files>"` to stderr. Does not
block. **Verified live, unplanned**: this worktree currently has genuine uncommitted edits in
`services/intent_service/action_registry.py` and `canonical_handlers.py` from the concurrent
intent-routing lane (I did not create or touch these — confirmed via `git status --porcelain` before
and after every run of mine). Every code-range test run above printed the warning citing those exact
two files, proving the check fires on real cross-lane dirtiness, not just a synthetic case.

**(c) `flock` / portable lock.** `command -v flock` → exit 1 (absent on this macOS host, confirmed
directly). Hook checks this at runtume: if `flock` present, uses `exec 9>lockfile; flock -w 120 9`;
else (this host, every run) falls back to a **portable mkdir-lock** under
`$(git rev-parse --git-common-dir)/piper-prepush-smoke.lock`, atomic `mkdir`, 120s bounded wait
(2s poll), 300s stale-lock timeout (clears and retakes if the lock dir is older than that — guards
against a killed hook wedging future pushes). Lock released via `trap cleanup EXIT` (`rmdir`).
**Used: mkdir-lock, on every run** (flock absent). Verified the lock dir is created during the run and
gone after (`ls "$common" | grep prepush` showed nothing after each pass/fail run).

**(d) Per-run log line.** Appended to `"$(git rev-parse --git-common-dir)/piper-prepush-smoke.log"` —
`ts=... worktree=... interpreter=... code_path=... outcome=... duration=...s [extra]`. Written for
every code-touching run (pass/fail/unchecked/emergency-skip); **not** written on the zero-cost
no-code-path fast exit (consistent with "no pytest started, pays nothing" for non-code pushes).
Verified: four real lines appended during testing below, see log excerpt.

**(e) Sunset-or-renew header.** Added per `docs/internal/operations/mechanism-sunset-or-renew.md`:
```
Cost:    ~28s warm / ~50s cold per code-touching push (first push per host/key pays the cold cost
         once; every push after is warm). ~0.5s on non-code pushes.
Benefit: measuring — the per-run log line is the evidence; no benefit count yet (not installed).
Review:  2026-11-29 (8 weeks out)
Owner:   Lead
```

**(f) Header states real coverage.** Updated to say coverage is now all 14 worktrees (once Pard's env
is provisioned for the current key on each), replacing the old 1-of-14-venv framing — with a pointer
to the two item-5 mailbox memos that establish this (14/14 verified, aiosqlite finding).

Everything else kept as-is: code-path filter (`services/ web/ tests/ main.py alembic/ pytest.ini
requirements*.txt`), the stdin-range parsing loop, `PIPER_SKIP_PREPUSH_SMOKE=1` emergency skip,
fail-open-on-fault philosophy, exit codes (0 skip/pass/unchecked/emergency-skip, 1 fail), CI's own
addopts override including `--import-mode=importlib`.

**One addition beyond (a)-(f), needed to test (iii) without editing tracked tests**: a documented,
off-by-default `PIPER_PREPUSH_SMOKE_ARGS` env var appended verbatim to the pytest invocation. Empty/
unset is a no-op for every routine run (every pass/fail/unchecked test above except (iii) ran with it
unset). Documented in the header as a test-mode knob.

## Four test runs (real, on this host)

**(i) Log-only range → skip fast.** Commit `29dd785446` (touches only
`dev/2026/10/04/2026-10-04-0634-lead-code-log.md`) against parent `6b9d95aed0`:
```
exit=0
0.444s total, no stderr output, no log line written (confirmed: log file absent before, absent after)
```

**(ii) Code range → pass, log line, lock taken+released.** Commit `0a134ccf45` (the real
`requirements.txt` aiosqlite commit) against parent `031391ed99`:
```
pre-push: code path touched (requirements.txt) — running the smoke set (~1 min, lock=mkdir)…
pre-push: smoke passed (569 passed, 1 skipped, 14907 deselected, 90 warnings in 41.79s).
exit=0, wall 46.0s
log line: ts=2026-10-04T18:42:08-0700 worktree=.../lead interpreter=.../pytest-py3.11-a5d47c8fc7b9/bin/python
          code_path=requirements.txt outcome=pass duration=46s lock_strategy=mkdir
          summary="569 passed, 1 skipped, 14907 deselected, 90 warnings in 41.79s"
lock dir created during run, confirmed absent after (released).
```
(1 skipped vs. the pre-aiosqlite 48 skipped — this run used the just-rebuilt env with aiosqlite
installed, so it's also a live confirmation of Pard's finding being fixed in practice.)

**(iii) FAIL path.** Created an untracked scratch file
`tests/test_prepush_hook_deliberate_fail_SCRATCH.py` (one `@pytest.mark.smoke` test, `assert False`),
never `git add`-ed, deleted immediately after the run. Ran the same code-touching range with
`PIPER_PREPUSH_SMOKE_ARGS="tests/test_prepush_hook_deliberate_fail_SCRATCH.py"`:
```
⚠️  pre-push: smoke ran against a DIRTY tree under code paths: services/intent_service/action_registry.py
   services/intent_service/canonical_handlers.py tests/test_prepush_hook_deliberate_fail_SCRATCH.py
pre-push: code path touched (requirements.txt) — running the smoke set (~1 min, lock=mkdir)…
FAILED tests/test_prepush_hook_deliberate_fail_SCRATCH.py::test_deliberate_prepush_hook_failure
❌ pre-push: smoke FAILED (1 failed in 0.22s). Push blocked — CI's full suite would be skipped behind a red smoke.
   Fix it, or (emergency only) PIPER_SKIP_PREPUSH_SMOKE=1 git push … and log why.
exit=1, wall 1.4s
log line: ...outcome=fail duration=1s lock_strategy=mkdir summary="1 failed in 0.22s"
```
File removed immediately after (`git status --porcelain` on that path confirmed clean).

**(iv) Env-missing path.** Pointed `XDG_CACHE_HOME` at a freshly-created empty temp dir
(`/private/tmp/prepush-empty-xdg-cache`, removed after):
```
⚠️  pre-push: smoke ran against a DIRTY tree under code paths: services/intent_service/action_registry.py
   services/intent_service/canonical_handlers.py
⚠️  pre-push: pytest env not provisioned — run scripts/ensure-pytest-env.sh --build or ask Pard. Pushing UNCHECKED.
exit=0, wall 0.236s
log line: ...interpreter=none code_path=requirements.txt outcome=unchecked duration=0s
```

## Multi-worktree resolution (check-worktree-interpreters.sh equivalent)
No such script exists in the tree (confirmed by search + `git log --all`). Ran `ensure-pytest-env.sh`
directly from three worktrees instead:
```
lead (key a5d47c8fc7b9, post-aiosqlite)        → resolves, exit 0
/private/tmp/lead-deploy-wt (key 94d244eccaea, pre-aiosqlite, detached HEAD) → resolves, exit 0
piper-morgan-product main checkout (key 94d244eccaea)                        → resolves, exit 0
```
Each worktree computed its OWN key from its OWN `requirements.txt` state and found the matching env —
a stronger proof than "same key everywhere" would have been, since it also demonstrates the
invalidation Pard designed working correctly across two different live keys on one host.

## Not met / caveats
- `scripts/check-worktree-interpreters.sh` was asked for "if it exists" — it does not exist anywhere
  in this repo's history. Used the equivalent per-worktree loop above instead of inventing a new
  script (out of scope for this task; flagged for Lead/Pard if they want it formalized).
- The hook still runs smoke against the **working tree on disk**, not a `local_sha` checkout
  (CIO's condition 1 cheapest-fix path, explicitly chosen over the throwaway-worktree alternative,
  per Lead's own memo: "I'll take your cheap fix first... move to a throwaway worktree only if that
  proves insufficient"). The dirty-tree warning is the mitigation, not a fix of the underlying gap —
  unchanged from the agreed scope of this finish task.
- Not installed into the common dir, per instruction — CIO verifies install separately.
- `aiosqlite` landing mid-task was NOT my action; I verified but did not cause it, and did not touch
  `requirements.txt`.

## Verified how
Every number above is this session's own terminal output, quoted, not recalled — `bash -n`/`sh -n`
clean on both files; `command -v flock` run directly (exit 1); all four hook invocations run for
real against real commit ranges from today's history; `git status --porcelain` checked before/after
every run touching forbidden paths to confirm no edits to `services/intent_service/*`,
`.github/workflows/fly-deploy.yml`, or `requirements.txt`. Layer: local hook/script behavior on one
host, not an installed hook, not CI. Denominator: 4 of 4 requested scenarios run; 3 of 3 worktrees
checked for interpreter resolution (lead, lead-deploy-wt, main checkout) — did not check the other
11 registered worktrees (arch/cio/comms/cxo/docs/exec/host/pa/ppm/usage-capture/web), relying on
Pard's prior 14/14 claim for those.

## No git add / commit / push / stash / reset performed (per hard rules).
