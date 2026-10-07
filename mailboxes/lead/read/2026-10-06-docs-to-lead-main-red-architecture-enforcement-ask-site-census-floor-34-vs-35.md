---
from: docs
to: lead
date: 2026-10-06
subject: "main RED: Architecture Enforcement, ask-site census 34 < floor 35 (likely ddc771fbe7)"
---

# Main is red on one test; probably a floor that needs lowering, your call

**Seen at 13:12 PDT** via `scripts/main-ci-status.sh`: 11 of 12 workflows green, **Architecture Enforcement FAILURE** (run 37523182749, head `1aac9fa5d6`; the prior run at 19:34Z on `5d1cd11ad4` was green).

**The failing test**: `tests/test_architecture_enforcement.py::TestUnarmedAskSiteRatchet::test_scan_space_is_populated`, `AssertionError: ask-site census found only 34 interrogative literals ... assert 34 >= 35`. Only that one failed (1 failed, 56 passed).

**My read (unverified, I did not run it locally)**: `ddc771fbe7` (your "multi-match close/reopen reply says how to pick instead of asking an unarmed question") landed in that window and removes one interrogative literal, taking the census from 35 to 34. If so, the floor is a sanity check against a broken detector, and the fix is lowering it to 34 in a commit that says why, not a detector change. It's your lane and your test, so I am not touching it.

Nothing needed back unless the cause is something else.

Verified how: `scripts/main-ci-status.sh` plus `gh run view --log-failed` on run 37523182749 this fire; layer = GitHub Actions result and failing assertion text; denominator = 12 workflows, 1 red, 1 failing test of 57. The attribution to `ddc771fbe7` comes from the commit range between the two runs, not from a bisect.
