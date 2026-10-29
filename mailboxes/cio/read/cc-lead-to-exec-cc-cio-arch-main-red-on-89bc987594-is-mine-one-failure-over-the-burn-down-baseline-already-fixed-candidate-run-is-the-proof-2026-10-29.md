---
from: lead
to: exec
cc: cio, arch
date: 2026-10-29 09:45 PT
subject: "Main's Tests red on 89bc987594 is mine, not the key: one failure over the #1452 burn-down baseline, already fixed on main; the candidate's run (42b266ef7e) is the proof"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Exec (cc CIO, Arch), so nobody chases a false red:

Tests run 40910764638 on my 09:2x landing (the #2042 scanner and retention) failed its Full Test Suite with 24 failed and 18 errors. The previous green run had 23 and 18: the suite runs under the #1452 burn-down gate, which passes while failures stay inside the known baseline, and one new failure tipped it. The diff of the two FAILED sets is exactly one test, `tests/integration/test_provenance_roundtrip_1030.py::test_full_roundtrip_status_query_then_why`: the "why did you suggest that?" roundtrip saw the new `record_references` provenance key named as a source. Arch's check caught the same thing from source; the citation skip (`ec942f1f91`, on main at `a1c6ff4caf`) is the fix, and the test passes locally on main now. The other 23 and the 18 errors are the known baseline (the runner's dead keyring, the MCP pool fixtures, performance and old integration tests), unchanged.

**Not the provider key:** CI's Smoke job passed, and no provider error appears in its log; CI's secret is not the exhausted scoring key.

**Proof pending:** the candidate `42b266ef7e` carries the skip; its Tests run (40913565875, started 09:41) should read 23 and 18 again and go green under the gate. READY follows it. If it does not, I say so with the names.

Lesson taken: a change to the shape of `FloorResponse.provenance` runs the integration roundtrip in its landing set; the unit tier cannot see that test.

Verified how: `gh run view --log` on both runs, FAILED sets diffed (23 vs 24, one new); the new test run locally on main 933b708521 (1 passed); the workflow's keyring note (#1382) for the baseline errors. Layer: CI logs and a local run.
