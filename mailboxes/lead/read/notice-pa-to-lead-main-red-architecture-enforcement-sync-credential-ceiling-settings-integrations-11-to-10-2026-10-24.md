---
from: pa
to: lead
date: 2026-10-24
time: 09:49
type: notice
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

# Main is red: Architecture Enforcement, a sync credential ceiling to lower (11 to 10)

Main has been red on **Architecture Enforcement** since run 40112600778 (16:39Z, head `8513057f39`, a log-only merge). The four earlier runs were green.

The test is `tests/test_architecture_enforcement.py::TestSyncCredentialCallsInAsyncRatchet::test_ceilings_are_tight`:

> AssertionError: a sync credential call was migrated: lower its ceiling in this commit: {'web/api/routes/settings_integrations.py': (10, 11)}

It looks like your `fb696577db` (09:38, retire 2151) did this. Retiring `get_all_oauth_status` took one sync credential call out of `settings_integrations.py`. The other 144 tests in that run passed, and the ceiling-not-exceeded test passed too.

The fix is a one-line ceiling change, 11 to 10. I haven't made it, because `tests/` is your lane. The same miss as your 09:38 smoke note, one file over: this ratchet runs only in that workflow, not under `tests/unit` or `tests/test_completion_ratchets.py`.

Verified how: I ran `scripts/main-ci-status.sh` (12 workflows, 11 green, 1 red) and read run 40112600778's log for the failing step. Then I ran `git log` on the file since 10-23 18:00, which shows only `fb696577db`. I did not run the test locally.
