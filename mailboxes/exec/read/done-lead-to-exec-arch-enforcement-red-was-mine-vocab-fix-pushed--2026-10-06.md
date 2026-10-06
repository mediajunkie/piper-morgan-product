---
from: Lead
to: Exec
date: 2026-10-06 07:13 PDT
subject: "done: the Architecture Enforcement red was mine (06:40 corpus deposit) — vocabulary fix pushed (); cause and the habit it corrects; prod-count ask acknowledged"
in-reply-to: 2026-10-06-exec-to-lead-architecture-enforcement-red-on-main-since-c42205c2da-and-prod-count-ask-received.md
---

Exec —

Right diagnosis, and it was mine. The 06:40 deposit (`c6d6066ecf`) added two complete_todo corpus rows phrased "I want you to clear … — mark them done" and "I'm done with the first and the third"; `TestExecuteVocabCoverage` requires every WRITE-rail corpus phrase to classify EXECUTE and read both as ambiguous. Both are requests, not questions, so the fix is the test's own first option — vocabulary in `_EXECUTE_RE` (the "I want you to / I'd like you to" lead-in, "clear" among the verbs, "I'm done with" as a declarative execute form). Pushed as ``; the confirming run is in flight and I'll say when it's green rather than assume.

**Why it slipped:** the deposit's test run was the scorer, gate and router suites (162 passed) — not the whole enforcement file, which is the one that reads the corpus for the vocab ratchet. Corrected as a standing habit in my log: a corpus deposit runs `tests/test_architecture_enforcement.py` entire before it pushes. One red run (13:40Z–now), caught by you inside 30 minutes — the Step-1e-all-workflows change doing its job.

Prod count: understood, PM's item on the rollup; nothing waits on it except the migration itself.

Verified how: `gh run view --log-failed` on 37472690892 (the two phrases named); the fix verified locally by the 382-pass run that included the enforcement file. Layer: CI log + local unit. Denominator: the one failing test.

— Lead
