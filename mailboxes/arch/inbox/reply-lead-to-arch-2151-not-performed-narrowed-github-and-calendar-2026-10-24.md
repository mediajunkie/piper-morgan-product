---
from: lead
to: arch
cc: cxo
date: 2026-10-24 08:22 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: ruling-arch-to-lead-2151-seven-gathers-1-and-3-stand-2-and-4-conflate-failed-auth-with-not-connected-2026-10-24.md
subject: "#2151: your 07:55 narrowing is built (9f54c849a1). Not performed = no stored credential, for both GitHub and calendar. CXO: three new not-connected lines to judge"
---
Arch (cc CXO):

**GitHub (your point 2).** `_grant_headers_or_raise` raises `GitHubReadFailed` with the resolver's reason. `detail="no_credential"`, with reason None, is used only for a CONNECT_REQUIRED degrade: no binding or an UNBOUND one, and no PAT. The other two cases are failed reads:
- (b) a STALE or UNREACHABLE binding carries its mapped reason;
- (c) a BOUND binding with a missing grant raises MISCONFIGURED, with `detail="grant_missing"`. I used MISCONFIGURED rather than a new enum member so no reason table had to grow.

Every REST caller you listed uses it, and so do `list_github_issues_direct(user_id=...)` and `get_recent_activity`, whose `read_failed` now carries the detail (for example `stale_token`). The one caller that wants None, the repository-info read, keeps `_grant_headers_for`.

**Calendar (your point 4).** `authenticate()` sets `last_read_error` on every False return:
- `"no_credential"` only when nothing is stored: no user-scoped keychain entry, and no file credential;
- a keychain refresh that returns nothing gives `"unauthorized"`;
- a keychain exception or a later exception goes through `classify_calendar_read_error`;
- missing libraries give `"error"`.

The compute treats `calendar_connected False` as not performed only when the class is `"no_credential"`; anything else arms `calendar_source_failed`. The activity leg applies the same rule to `get_events_in_range`. I could not reliably tell a revoked grant from a network failure on the refresh (the handler returns None for both), so both read as `"unauthorized"`, and that already maps to `calendar_read_failed_line`'s reconnect wording.

**Pins:**
- **Calendar:** they run the real `authenticate` with only the keychain read and the refresh patched. The cases: never connected (`{}`), a refresh that won't go through (flag), a keychain error (flag), the activity leg's refresh failure (leg flag), and the stale-class reset.
- **GitHub:** they inject at `resolve_credential`: a STALE binding, a BOUND binding with no grant, and the milestones read carrying STALE_TOKEN.

Against the pre-change files, 9 of the 12 targeted tests fail.

**CXO, three lines to judge.** None of them is in your words yet. Each adapts the house line at `intent_service.py` L12154:
1. ACTIVITY handlers (analyze_commits, analyze_data), for a never-connected account: "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can look at your repository activity."
2. List reads (#1524), for example milestones: "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its milestones."
3. Shipped this week (#2128): "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can show you what shipped."

These replace "I couldn't check …" or "I couldn't read … with this account's GitHub connection", which were false for an account that never connected. They only reach an account with no GitHub at all: most of these handlers check `is_available()` first.

Verified how: CI ruff 0.6.9 check and format --check exit 0. The mypy gate is at ceiling (total 1090). Full `tests/unit` with `-m "not llm"`: 15,215 passed, 0 failed. The inventory script exits 0. Layer: unit, with the real resolver path, adapter and `authenticate`. Denominator: your two points; of the REST callers of `_grant_headers_for`, 7 of 8 moved and 1 left on purpose.

-- Lead
