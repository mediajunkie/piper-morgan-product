---
name: ab-a-isolation
description: The A/B/A stash experiment — decide in minutes whether a test failure is YOUR diff or the environment/run-history. Use when a suite fails during your change and blame is ambiguous.
scope: cross-role
version: 1.0
created: 2026-08-15
---

# ab-a-isolation

Decide whether a failure is **your diff** or **the world** — by running the same
check three times with only one variable moved. Canonized from two decisive uses
in one week (2026-08-13: the e2e "regression" that was #1532-era run-history —
#1602; and the pre-existing provenance failure isolated the same hour).

## When to Use
- A test fails while your uncommitted change is in the tree, and "did I break
  this?" is not obvious.
- A previously-green suite reads red and you're about to either debug your diff
  (maybe wasted) or push anyway (maybe reckless).

## The experiment

```bash
# A — the unchanged world
git stash push -u -m "aba-isolation"     # -u if untracked files are part of the diff
<run the failing check>                   # record the result VERBATIM
# B — your change
git stash pop
<run the same check>                      # record verbatim
# A again — the tiebreaker (THIS is the step people skip, and it decides)
git stash push -u -m "aba-isolation-2"
<run the same check>
git stash pop
```

## Reading the three results

| A | B | A′ | verdict |
|---|---|---|---|
| pass | fail | pass | **your diff** — debug it |
| fail | fail | fail | **pre-existing** — file it, don't absorb it into your change |
| pass | fail | **fail** | **run-history/state** — the run itself mutates shared state (DB rows, caches, session stores); neither you nor HEAD is clean twice. Find the state carrier (#1602 was conversation rows + fixed session ids) |
| flaky mix | | | margin/stochastic — name it as such; never tune-until-green |

**The third run is the whole method.** A/B alone cannot distinguish "my diff
broke it" from "the first run planted state that breaks every later run" — the
2026-08-13 case read as a 13-test regression on A/B and was proven run-history
by A′ (unchanged tree failing 12 after previously passing).

## Rules
- Same command, verbatim, all three runs (shape drift invalidates the read).
- `git status` BEFORE the first stash; verify clean pop after each (stash -u
  captures untracked — know what you're carrying).
- Record all three results in your log/issue — a verdict without the three
  numbers is an assertion, not an experiment.
- On a shared/dev DB, note that A′'s failure may be A's own residue — cleanup
  belongs to the run that planted it.
