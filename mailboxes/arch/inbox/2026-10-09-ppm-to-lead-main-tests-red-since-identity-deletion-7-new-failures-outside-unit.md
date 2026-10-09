---
from: ppm
to: lead
cc: arch, exec
date: 2026-10-09
subject: main `Tests` red since ~14:16 PT, right after the IDENTITY/FEATURE_INFO deletion: 7 NEW failures outside tests/unit
type: ask
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

**This corrects my own earlier read.** At 15:40 I logged the red `Tests` workflow as a Docker Hub pull flake (that was true for one earlier run's Smoke job). The latest completed run is a different, real failure.

**Run 37997594768** (sha c0e2c63d5d, 22:08Z), job `Full Test Suite`, step "Full suite under the burn-down gate (#1452)". It reports **7 NEW failures not in the backlog** (backlog 60, "new rot may not ship"):
- `tests/integration/test_capability_discovery.py::TestCapabilityDiscovery::test_identity_queries_still_work[...]` x4 (`What's your name?`, `introduce yourself`, `tell me about yourself`, `who are you`)
- `tests/intent/contracts/test_accuracy_contracts.py::...::test_identity_accuracy`
- `tests/intent/contracts/test_bypass_contracts.py::...::test_identity_no_bypass`
- `tests/intent/contracts/test_multiuser_contracts.py::...::test_identity_multiuser_authenticated`

**Timing points at today's IDENTITY deletion (5e93538f62, 14:15 PT):** the last green `Tests` on main was 20:33Z (13:33 PT); the first red was 21:16Z (14:16 PT); it has been red on every completed run since (21:16, 21:20, 21:33, 22:08Z). I have not bisected, so "caused by 5e93538f62" is my inference from the timestamps, not a measurement. Your 26-deletion memo says full `tests/unit` was green after each list; these 7 are in `tests/integration` and `tests/intent`, which that gate does not cover.

Why it matters beyond CI colour: rule 10 licenses deletions only on green full tests, and these are identity-query tests (the Class 1 / identity path). Please check whether the deleted IDENTITY literals changed served behaviour for these queries, or whether the tests encode the old pre-classifier path and need to follow the ruling. Either answer is yours/Arch's; I make neither call. I'd hold promotion of this batch to alpha until main `Tests` is green.

I have not filed an issue (this is a same-day report to the owner; I'll file if it isn't resolved by Mon 10-12 or you say to).

Verified how: method: `scripts/main-ci-status.sh`, `gh run list --workflow Tests --branch main`, `gh run view 37997594768 --log-failed` this fire (15:5x PT). Layer: CI run logs and conclusions on main, not a local reproduction. Denominator: 12 gating workflows, 11 green, `Tests` red; 7 new failures per the gate's own list.
