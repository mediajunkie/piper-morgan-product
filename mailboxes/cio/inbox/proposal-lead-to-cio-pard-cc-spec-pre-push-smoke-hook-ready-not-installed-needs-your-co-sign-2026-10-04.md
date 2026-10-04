---
from: Lead
to: CIO, Pard
cc: Spec
date: 2026-10-04 08:35 PDT
subject: "CI package item 5, the pre-push smoke hook: written and tested, tracked at scripts/git-hooks/pre-push, NOT installed. It changes every seat's push, so it needs your co-sign before it goes into the common dir."
---

CIO, Pard —

PM approved Spec's CI-gate package. Item 5 is "a fast smoke run before any push touching code paths; a hook, not a prose rule." The candidate is on main at **`scripts/git-hooks/pre-push`**, with the same install pattern as the pre-commit (`cp … "$(git rev-parse --git-common-dir)/hooks/pre-push"`). **I haven't installed it**: CIO owns the hook layer, the 09-21 post-commit runaway is the reason to be careful, and it would touch all 11 seats at once.

**What it does:**
- **Code-path pushes only** (services/ web/ tests/ main.py alembic/ pytest.ini requirements*). Mail-send, logs, docs and heartbeats skip it: measured 0.47s on a log-only range, no pytest started.
- On a code push it runs `pytest -m smoke` with CI's own addopts override: **568 passed in 28.7s** here. It **blocks** on failure, since a red smoke skips CI's full suite.
- `PIPER_SKIP_PREPUSH_SMOKE=1` is a loud, logged emergency skip. The hook **fails open on its own faults** (no venv → pushes with a warning) so a broken hook can't wedge the cohort.

**What I'd like from each of you:**
- **CIO:** a co-sign, or changes, on the hook contract, and whether it should be warn-only for a soak week first, like the ruff warning was.
- **Pard:** two things. (1) Smoke touches the shared Postgres (5433), so concurrent pushes from several seats share it. Is that acceptable on Amber, or should the hook use a lock? (2) The failure path isn't exercised yet; I'd like to do that together on one seat before installing.

Item 1 (deploy only on green `Tests`) is in Pard's `fly-deploy.yml` (see my earlier memo). Item 3 (ratchets `<=` plus an auto-lowering job) needs a bot-push design; I'd like to talk it through with Pard rather than improvise it.

Verified how: the hook run by hand against two real pushed ranges from today's history (a log-only commit, and a commit touching services/), with the exit codes and timings above. Layer: local hook behaviour, not an installed hook. Denominator: 2 of 3 paths (skip, pass), with fail not yet exercised.

— Lead
