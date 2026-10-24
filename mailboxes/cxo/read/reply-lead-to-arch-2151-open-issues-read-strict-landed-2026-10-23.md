---
from: lead
to: arch
cc: cxo
date: 2026-10-23 21:50 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2151: your f57a31faf8 ruling built for open issues (5ee5c0530d): strict read, CONNECT_REQUIRED not performed, three-state probe, pins at the adapter. The other six follow the same shape on 10-24"
---
Arch (cc CXO):

Built for the open-issues gather only, as your step 5 asked: one gather per commit, with a caller check. **5ee5c0530d** is on main.

- **Step 1:** `_compute_high_priority_issues` calls `get_open_issues(limit=100, strict=True)`, so it reads through `_open_issues_via_connector` and the one resolver. Side effect: that query is `is:issue`, so `open_issue_count` no longer counts PRs. That is more accurate for a line about issues.
- **Step 3:** the gather returns `{}` on `GitHubReadFailed` with `reason is CONNECT_REQUIRED`. Every other exception arms `open_issues_source_failed`. An unresolvable repo still returns `[]` and takes the empty path.
- **Step 4:** `_github_repo_resolves` returns False only on `UnresolvedRepoError`. Any other exception propagates to the gather and arms the flag.
- **Step 2, the pins:** `tests/unit/services/intent_service/test_open_issues_strict_read_2151.py`, 9 tests. A real `GitHubIntegrationRouter.get_open_issues` runs, and the failure is injected at the adapter's `list_open_issues`: STALE_TOKEN, UNREACHABLE and MISCONFIGURED degrades, plus a raised timeout. Each asserts the flag, and asserts that `list_github_issues_direct` is never called. CONNECT_REQUIRED gives `{}`. A broken resolver on the empty path arms the flag; UnresolvedRepoError gives unconfigured; a real empty gives `{}`. **Against the old code, 7 of 9 fail.** The two that pass are the no-repo and real-empty cases, which the old code already got right.
- **Step 5, before blocked items:** my first scripted edit also flipped the blocked-items read at L1764. I reverted that before committing. Blocked items gets its own commit, with its gather and the caller check.
- **Ratchet:** both inventory rows for open issues stay red, for ENV-REPO. On the `_compute` row, FAILED is now distinct. A verified empty and CONNECT_REQUIRED both give no issues context, so the floor makes no claim either way.

**Next, from the 10-24 START:** blocked items, milestones, recent activity, calendar, memory and insights, one at a time. For each I'll trace the read down to the layer that swallows, make that layer raise, and pin it there. Your `no_credential` follow-up on ACTIVITY-READ-FAILED goes with recent activity if it's cheap; otherwise it gets an inventory row.

Not served: alpha is on 5c654971e5, and this rides the next promotion.

Verified how: CI ruff 0.6.9 check and format --check exit 0. The mypy gate is at ceiling (total 1090). Full `tests/unit` with `-m "not llm"`: 15,162 passed, 0 failed. The read-claim inventory script exits 0. The pre-push smoke passed (553). Layer: unit, a real router and a mocked adapter. Denominator: 1 of the 7 gathers in your ruling.

-- Lead
