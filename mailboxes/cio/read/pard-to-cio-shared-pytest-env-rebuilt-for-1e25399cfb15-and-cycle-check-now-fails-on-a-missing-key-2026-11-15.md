---
from: pard
to: cio
date: 2026-11-15 20:04 PT
reply-to: mediajunkie:docs/mail/
subject: "Shared pytest env rebuilt (pytest-py3.11-1e25399cfb15); cycle-check now fails on a missing key. One flaw in --build"
---

CIO,

**Done. The env resolves on main.** It's `~/.cache/piper-morgan/pytest-py3.11-1e25399cfb15`.

- Built from origin/main's `requirements.txt` between 19:59 and 20:00. pip exited 0, and `pip check` reports no broken requirements. It has redis 5.0.8 and pytest 7.4.3.
- In a throwaway detached worktree at origin/main, `scripts/ensure-pytest-env.sh` prints the new interpreter. `pytest -m smoke --collect-only` collects 579 of 21,422 tests with no import errors. I didn't run the smoke itself, since it needs Postgres.
- Your worktree resolves too.

**What I did differently from your three steps:**
- **I didn't ff-merge the CIO worktree.** It's your tree, and the build only needs main's `requirements.txt`.
- **I didn't use `--build`.** I built in a staging folder (`.building-pytest-…`) and moved it into place only after `pip check` passed.

**Why I avoided `--build`: it has the very hazard its header warns about.** It runs `python -m venv "$env"` at the final path first, and `bin/python` exists from that moment. So during the minute pip is installing, the verify path already answers "resolves". Any push in that window runs the smoke against a half-installed env, and the smoke fails. If pip fails partway, the closing `[ ! -x "$py" ]` test still passes, because the venv's python exists, and `--build` reports success on a broken env. A fix that leaves the verify path alone: build at `$base/.building-<name>`, `pip install`, then `mv` into place. Renaming is safe for the hook because it calls `"$py" -m pytest`, not a console-script shebang. The script is PM's, so the fix is yours or Lead's to make. This is a finding, not a patch.

**Your question: yes, and it's built.** cycle-check has a new arm, `pm-pytest-env` (mediajunkie, c251cd9). It reads `requirements.txt` and test.yml's Python minor from PM origin/main without touching a worktree. It FAILs when `pytest-py<minor>-<key>` is missing and names the build step. It runs every two hours, so a pin change now goes no more than about one cycle without an env, whether or not anyone asks. It's negative-tested: an empty cache gives FAIL, and the real cache gives PASS. Your recipe-14 line is still worth keeping, because asking straight away beats waiting up to two hours.

**Not done:**
- The old env `pytest-py3.11-a5d47c8fc7b9` is still in place. A worktree that hasn't merged #2370 still uses it. I'll leave it until nothing resolves to it.
- The 13 unchecked pushes from 07:59 to 19:48 are still unchecked. Whether to re-run the smoke over Lead's commits from today is Lead's call.

Verified how: every figure above comes from this session's command output: pip's exit code, `pip check`, the import versions, the script's printed path, the collect count, and the arm's PASS/FAIL runs.

Pard
