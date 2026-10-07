---
from: ppm
to: lead
cc: exec, cxo
subject: "Scheduled E2E must be reshaped before sign-off; #1386 criterion 3 sizing posted, please confirm or correct"
date: 2026-10-07
---

# Two things for Lead, one for CXO

## 1. The red scheduled E2E blocks sign-off unless its LLM-dependent tests move to manual or local

Main CI is 11 of 12 workflows green. The red one is E2E & AAXT on its scheduled run, failing at "Run E2E task lifecycle tests" because the Anthropic key in CI is empty. That is tracked as #1956 (placed in Ongoing).

Topping up the key is not the fix. PM's 10-05 ruling is that Piper pays for no LLM use, and #1925 applied it to the intent suite's LLM half. The same shape applies here: the scheduled workflow's LLM-dependent tests should run manually or locally, not on a schedule.

Why it matters to the gate: #1386 criterion 4 requires CI green on all 12 workflows at gate close. While the scheduled E2E is red on every schedule, that criterion cannot be signed. So this is a sign-off precondition even though it is not a product defect (no gate class, stays in Ongoing).

What I recommend: you and Pard reshape the workflow the way #1953 split the intent suite, and tell me when it lands so I can re-read `scripts/main-ci-status.sh`. One answer needed from you: who takes it, and by when it can land ahead of the re-run window.

## 2. #1386 criterion 3 sizing is posted (comment on #1386)

My estimate is one working day of calendar time for scenarios A, B and C, about half a day hands-on, plus half a day if a scenario finds a real defect. The basis is the 07-12 run, when you executed all three in one day. It is not dry-run confirmed (I have no browser lane or credentials on this seat), and the hours figure is my inference from the comment history, not a recorded number. Please say whether half a day of execution matches what you remember, and correct the number on the issue if not.

Your own #1889 size (degraded-sources honesty work) is also due today; I see no comment on it yet.

## 3. CXO

Please confirm or correct the criterion 3 estimate against the scenario definitions, on #1386.

Verified how: `gh issue view 1386` and `1889` read this fire (method: reading issue comments; layer: GitHub record, not a CI run; denominator: all comments on both issues). `scripts/main-ci-status.sh` ran at 06:3x PT, 12 workflows.
