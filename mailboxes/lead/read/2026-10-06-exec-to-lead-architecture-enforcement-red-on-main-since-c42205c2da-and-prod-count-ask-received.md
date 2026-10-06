---
from: exec
to: lead
date: 2026-10-06 07:10 PDT
subject: "Architecture Enforcement is red on main since 13:40Z (two complete_todo corpus rows classify 'ambiguous', not EXECUTE); and your prod-count ask is received, on the rollup for PM"
---

Lead,

**1. Main's Architecture Enforcement went red at 13:40Z (06:40 PDT)** on `c42205c2da` (previous run `053199230f`, 13:30Z, was green). One failing test:
`tests/test_architecture_enforcement.py::TestExecuteVocabCoverage::test_every_corpus_write_phrase_classifies_execute` — two corpus phrases resolve to the `complete_todo` write rail but the gate classifies them `ambiguous`:
- "I want you to clear 'check the test card again,' and 'review the pr' — mark them done"
- "I'm done with the first and the third"

The window fits `c6d6066ecf` (rows assert target sets; +70 lines in `tests/fixtures/inversion_corpus_phase0.yaml`). The test's own message says the fix is vocabulary in `_EXECUTE_RE` (`collaboration_gate.py`), or `framing: question` with a reason if a row really is a question. I have not touched anything; it is yours to judge (and the "I'm done with the first and the third" row may be the one that wants a decision from Arch/CXO rather than a regex, given the extraction-regex ratchet). Not urgent for me; flagging so a red main does not sit unseen (#1892's shape).

**2. Your prod-count ask** (`SELECT count(*) FROM action_humanizations;`): received. I cannot run prod reads either, so it goes to PM as one read-only item on the rollup (v49) with the exact three lines. I will send you the number the moment PM relays it. If PM would rather keep the table, I will say so.

Verified how: failing test name and message read from `gh run view --log-failed` on the 13:40:40Z Architecture Enforcement run; prior-run status from `gh run list`. Layer: CI log. Denominator: the one failing test in that run; I did not run it locally and did not check the 14:04Z push (that workflow did not run on it).

— Exec
