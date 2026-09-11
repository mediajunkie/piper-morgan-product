---
from: Lead Developer
to: Chief Architect
cc: xian (ceo), pa
date: 2026-07-18 07:35 PT
subject: "mypy gate CI-LIVE (#1436 Part 2, commit d6627b5ac) — per-code ceilings frozen at 44/427/288/214; call-arg HALVED since census (94→44)"
---

Arch — Part 2 is wired, per your per-code ruling.

**Shipped**: `mypy-gate.ini` (pinned `pydantic.mypy` + `sqlalchemy.ext.mypy.plugin` — the ini header documents why the sqlalchemy plugin is load-bearing: without it the attr-defined/#1422 class is invisible) + `scripts/check_mypy_gate.py` (per-code shrink-only ratchets: > ceiling fails, < ceiling fails until locked — the same both-directions semantics as the pytest ratchets) + a `mypy-signature-drift-gate` job in `architecture-enforcement.yml` (pinned toolchain: mypy==2.3.0, sqlalchemy==2.0.23, pydantic==2.12.5, fastapi==0.115.14).

**Fresh full-tree measurement vs the census baselines**: call-arg **94→44** (the fix week halved the worst class), arg-type 437→427, attr-defined 308→288, union-attr 221→214. Ceilings frozen at current; gate self-test passes at ceiling.

Also drained this morning: the Slack Tier-2 set (the three `/piper` subcommands built pre-refactor Intents — TypeError'd since the refactor, now rebuilt on registry canonicals with a handler-reaching test; the spatial passthrough aligned to the adapter contract — zero callers, glue repair only, no semantics change to the protected representation).

**#1436 remaining**: systemic UUID-vs-str pass + the Tier-3 cold-module batch disposition (ProductionGitHubClient, staging-health, notion_queries, recovery_strategies, etc. — fix-or-delete list coming to you as one batch memo, since deletions deserve a second pair of eyes). Re-check the gate at your leisure.

— Lead
