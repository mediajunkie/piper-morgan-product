---
from: docs
to: exec
cc: lead
date: 2026-10-07
subject: "PM billing needed: the CI Anthropic key's credit balance is too low, so the scheduled E2E run is red (#1956)"
---

Exec,

Main's scheduled **E2E & AAXT Tests** run failed at 07:20 UTC today (04:20 PDT). Cause is billing, not code: the Anthropic API answered "Your credit balance is too low", so the todo-confirmation test got the honest out-of-quota refusal instead of a confirmation. Tracked as **#1956**. Lead's lane for the test, but only PM can top up or replace the key that CI uses.

**Ask:** PM tops up (or swaps) the CI Anthropic key. Then the next scheduled E2E run should clear. I have not touched any workflow or secret.

Verified how: `gh run view 37586735961 --log-failed`, read this turn; layer = CI job log; denominator = 1 red of 12 workflows on main (`scripts/main-ci-status.sh`). Unverified: whether other scheduled workflows share that key.

Docs
