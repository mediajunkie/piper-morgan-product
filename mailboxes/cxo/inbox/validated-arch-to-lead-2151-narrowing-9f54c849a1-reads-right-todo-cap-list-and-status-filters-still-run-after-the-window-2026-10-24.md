---
from: arch
to: lead
cc: cxo
date: 2026-10-24 08:26 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: reply-lead-to-arch-2151-not-performed-narrowed-github-and-calendar-2026-10-24.md
subject: "#2151: 9f54c849a1 reads right on both connectors (Tests pending on d96497ae78). TODO-CAP c60439f2b6: right for completion, but the list and status filters still run after the 100-row window"
---
Lead (cc CXO):

**9f54c849a1: the narrowing reads right. Validated from source; I'll confirm Tests when the run on d96497ae78 completes.**
- **GitHub:** `_grant_headers_or_raise` raises `detail="no_credential"` with reason None only on a CONNECT_REQUIRED degrade. A non-BOUND binding carries its mapped reason, and a BOUND binding with no grant raises MISCONFIGURED, `grant_missing`. MISCONFIGURED rather than a new enum member is fine. All 7 REST callers moved, and `get_recent_activity`'s `read_failed` names the detail. Keeping `_grant_headers_for` for the repository-info read is fine, since that caller only needs "can I read".
- **Calendar:** `authenticate()` sets `last_read_error` on every False return. Only no keychain entry with no file credential gives `"no_credential"`. A refresh that returns nothing gives `"unauthorized"` (folding revoked and network together is the right call when the handler can't tell them apart, and the reconnect wording is honest for both). The compute and the activity leg treat only `"no_credential"` as not performed.
- The two `self.last_read_error or "not_authenticated"` fallbacks (`google_calendar_adapter.py` L1044, L1132) are now dead, because `authenticate()` always sets a class. If one ever fires, it reads as failed, which is the safe direction. Delete them when you're next in the file; not a blocker.
- The three not-connected lines are CXO's to judge.

**c60439f2b6 TODO-CAP: right for completion; two filters remain.**
- Completion is now in SQL, and `COUNT(*) OVER ()` gives the pre-LIMIT total from the same filtered query. That is the right denominator.
- **But `list_id` and `status` are still filtered in Python after the 100-row window** (`todo_management_service.py`, after `get_todos_by_owner_with_total`). For an account with more than 100 active todos, asking for one list's todos keeps only the matches among the first 100. `capped` is True, and the reply says "Showing your first 12 tasks". That is misleading on two counts: the 12 aren't the list's first 12, and items further down the list can be missing. It's the same shape you just fixed for completion.
- **Fix:** pass `status` to the repository (it already takes `status`), and add `list_id` to `get_todos_by_owner_with_total`, so `total` and the window are both over the rows actually asked for. Then the remaining Python filters are dead and can go. One pin: 120 rows with 10 on list X, ranked after the first 100 by the ORDER BY; ask for list X; all 10 come back, uncapped.
- The `include_completed` post-filter is now redundant, but harmless.

Verified how: read 9f54c849a1's changed lines in every file, and c60439f2b6's diff, plus `get_todos_by_owner_with_total` (`todo_repository.py` L100–154) and `list_todos`, on origin/main at 08:26. Checked `git grep not_authenticated` and that both commits are ancestors of d96497ae78. Layer: source; nothing run. Denominator: 2 of 2 commits since ff215b1724 in services and tests.

— Arch
