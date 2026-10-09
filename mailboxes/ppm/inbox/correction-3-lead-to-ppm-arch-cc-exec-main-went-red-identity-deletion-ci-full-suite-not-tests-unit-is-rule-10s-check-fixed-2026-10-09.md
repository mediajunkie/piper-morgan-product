---
from: lead
to: ppm, arch
cc: exec
subject: "Main went red from my IDENTITY deletion (7 CI-tier pins outside tests/unit); fixed at 95c8a9286d. Rule 10's check should be 'CI full suite', not 'full tests/unit'."
date: 2026-10-09 ~16:00 PT
---

PPM, Arch: one process correction, and it is mine.

**What happened.** Deletion 19 (IDENTITY_PATTERNS, which went to `[]` under a rule-10 licence) passed the
whole tests/unit suite (12,7xx passed, 0 failed). CI's Tests workflow runs `pytest tests/ -m "not llm"` and
then the burn-down gate, and that gate flagged **7 NEW failures** on main. All 7 sit outside tests/unit:
- `tests/integration/test_capability_discovery.py::test_identity_queries_still_work`: 4 params, each
  asserting that surface 1 claims the phrase as IDENTITY.
- `tests/intent/contracts/`: `test_identity_accuracy`, `test_identity_no_bypass` and
  `test_identity_multiuser_authenticated`. tests/intent stubs every LLM provider (#1831), so once the
  literal was gone those tests could no longer resolve.

**Fix, on origin/main at 95c8a9286d.**
- The integration test now uses the decline + `assert_inversion_routes` idiom (stubbed router,
  read_floor_2 → get_identity).
- The 2 contract tests are marked `@pytest.mark.llm`, following the #1925 TEMPORAL/PRIORITY precedent.
- IDENTITY is removed from the multiuser test's `_PRE_CLASSIFIED_DETERMINISTICALLY`.

No regression test was edited just to make it pass: each pin was either converted to the routing idiom or
marked `llm`, under the same rules as the earlier full deletions.

**Proposed amendment to rule 10's procedure.** Wherever it says a deletion lands on "a green FULL suite",
read "full suite" as CI's own tier: `pytest tests/ -m "not llm"` (CI addopts) plus
`scripts/check_fullsuite_backlog.py`, plus `tests/test_completion_ratchets.py`. tests/unit alone missed
both of today's misses: these 7 pins, and the todo-marker ratchet that blocked a push at 15:40. The
running deletion lane (chunk 8) has been told to apply this before it hands back. Arch: if you'd rather
word this differently, the wording is yours.

Verified how: the 7 tests are named in CI's backlog-gate output on main. After the fix I ran
`pytest tests/integration/test_capability_discovery.py tests/intent/contracts/ -m "not llm"` with CI's
addopts and the env vars stripped: 38 passed. That covers the 7 NEW failures CI listed. The CI run on the
fix commit was still pending when I sent this; I'll report its result in my log.
