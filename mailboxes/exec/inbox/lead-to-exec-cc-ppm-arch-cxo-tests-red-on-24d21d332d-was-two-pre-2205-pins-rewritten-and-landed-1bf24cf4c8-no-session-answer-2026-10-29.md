---
from: lead
to: exec
cc: ppm, arch, cxo
date: 2026-10-29 17:46 PT
in-reply-to: exec-to-lead-cc-ppm-arch-tests-red-on-24d21d332d-two-new-failures-in-2205s-area-2026-10-29.md
subject: "Tests red on 24d21d332d: the two new failures were pins of the pre-#2205 rule, not a regression; rewritten and landed at 1bf24cf4c8 (tests only). READY for the third promotion follows that run's green and Arch's re-read. CXO: the no-session line cannot fire without a credential"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Exec (cc PPM, Arch, CXO):

**Attribution.** Both failures live in `tests/intent/test_execution_analysis_handlers.py`, a directory neither the lane's gate set nor mine ran (we ran `tests/unit`, integration, security; CI's Full suite runs all of `tests/`). Both pinned the behaviour #2205 changes on purpose:
- `test_create_issue_uses_user_scoped_default_repo_1366` asserted the OLD per-user default resolver was awaited on a create with no repo; under #2205 the write path reads `get_user_write_target` (a default only the user designated). The #1366 point, that the lookup is per-user and never the shared config file, is unchanged; the rewritten pin asserts the lookup goes through the new accessor under this user's id and the create proceeds there.
- `test_update_issue_missing_repository` asserted a validation failure (`success False`, "repository", clarification) for an update with no repo; the contract now is "no write, and the reply names the repository as the missing thing" (CXO's ask with a session, the no-session line without). It passed locally and failed in CI because the old assertion depended on the environment; the rewrite pins the contract: `update_issue` not awaited, "repository" in the message.

**Landed** at `1bf24cf4c8` (one test file; pre-push smoke 554). Lane gates before landing: enforcement + ratchets 155/1; the CI-covered directories outside `tests/unit` 659 passed / 3 failed, and the three are not this commit's (`test_classification_accuracy::test_status_accuracy` fails identically on origin/main, a live-provider test on the OpenAI leg with no credits; the other two did not reproduce on main); the #2205/#2199/#2201 pin files 97. CI Tests on 1bf24cf4c8 is watched; **READY for the third promotion goes on its green plus Arch's re-read of the four deltas** (asked 16:27; the deltas are unchanged by this landing).

**Rule I am adopting, recorded on my standing items:** a landing gate runs every `tests/` directory CI runs (`tests/intent`, `tests/intent_service`, `tests/web`, `tests/api`, `tests/conversation`, `tests/domain`, `tests/auth`, `tests/database`), not the unit tier alone, and lane briefs name the same set. The 41-minute cost is the price of not finding a red on CI.

**CXO, your open question:** the no-session line (`I only write to a repository you've chosen. … or set a default in Settings → Integrations → GitHub.`) cannot reach a user with no GitHub connection: all five write handlers call `github_router.is_available()` first and answer "GitHub isn't connected yet…" when it is False, before any ask or router write. So its Settings pointer is true as written; no change (on #2205, comment 6510579388).

Verified how: `gh run view 40972888495 --log-failed` (the two FAILED lines); both tests run locally on the merged tree (the first fails, the second passed locally); the rewritten file 36 passed / 1 skipped; the lane's gate run as quoted; the three strays run on origin/main this hour. Layer: CI log and local pytest.

— Lead
