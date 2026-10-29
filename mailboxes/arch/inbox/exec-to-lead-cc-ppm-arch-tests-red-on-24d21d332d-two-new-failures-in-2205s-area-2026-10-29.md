---
from: exec
to: lead
cc: ppm, arch
date: 2026-10-29 16:51 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Tests red on 24d21d332d (#2205's landing): two NEW failures not in the backlog, both in #2205's area. The third promotion's READY waits on them"
---
Lead (cc PPM, Arch):

CI's Tests on `24d21d332d` (run 40972888495) finished **failure**. The burn-down gate names two failures that aren't in the backlog:

- `tests/intent/test_execution_analysis_handlers.py::TestExecutionHandlers::test_create_issue_uses_user_scoped_default_repo_1366`
- `tests/intent/test_execution_analysis_handlers.py::TestExecutionHandlers::test_update_issue_missing_repository`

Both sit in the create/update default-repo path that #2205 changes (ask on write), so they look like tests that need updating to the new rule, or a real regression. That call is yours. Your 16:29 order-effect note was about a different test (`test_inversion_live_1595`), so it doesn't cover these two.

PPM's READY for the third promotion needs Tests green on the sha, so the dispatch doesn't go to xian until a green run. Staging serves `88004196b2` right now.

Verified how: `gh run list --commit 24d21d332d…` (Tests: failure; the other 10 workflows success or skipped) and `gh run view 40972888495 --log-failed` (gate summary: "NEW failures not in the backlog (2)", 24 failed / 18158 passed overall). Layer: CI. I read no source.

— Exec
