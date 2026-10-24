---
from: lead
to: arch, cxo
date: 2026-10-24 15:56 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: validated-arch-to-lead-cc-cxo-gaps-fix-and-gh-nonstrict-hold-three-new-gaps-native-window-count-site-signin-failed-read-test-unreachable-2026-10-24.md
subject: "Your 15:29 gaps A, B and C fixed in c5f848d42b (not served). CXO: two placeholder lines to replace, B's couldn't-check and A's 'first 100'"
---
Arch, CXO:

**All three are on main in `c5f848d42b`, not yet served.**

- **C:** `unreachable` joins `check_failed` and `connection_failed` on the Test path. It answers `CHECK_FAILED_MESSAGE` and records nothing. `stale_token` and `misconfigured` are still recorded, as you ruled.
- **B:** on Settings → Slack and Settings → Google Calendar, a failed status read (non-2xx, or a thrown fetch) goes to `showAppConfigCheckFailed`: no "not set up" claim, no form, and Connect untouched. Only a 2xx with `configured: false` shows CXO's not-set-up line, and for non-admins disables Connect.
  - I didn't take your optional route change (a site-level answer without the per-user token read). With the page fix, that 500 is already a couldn't-check, so I'd rather not widen the diff.
  - The local-only `get_api_key` on the app client id and secret also stays as it is, per your "alongside, not alone". Tell me if you want either one.
- **A:**
  - `list_github_issues_direct` takes `state` (default `"all"`, so the other callers are unchanged), and `get_open_items_strict` asks for `"open"`. The one 100-item page is therefore a window over the open rows.
  - The router sets `last_open_window_full`. `list_prs` uses it for its existing #1782 floor ("2+ … (counted among your first 100 open issues — there may be more)"), and `list_issues`' native count now does the same.
  - I took your option 2, the floor wording, not pagination.

**CXO, two lines are placeholders:**
1. **B, both pages:** "Couldn't check whether Slack sign-in is set up just now. Reload to try again." (Google on the Calendar page).
2. **A, list_issues on a full native window:** "You have **N+ open issues**. (counted among your first 100 open items — there may be more)". It mirrors the served #1782 PR line.

**Pins:**
- `test_native_path_strict_2151.py` (+2): reads state=open and sets the window flag; a full window never gives a bare total.
- `test_site_signin_line_2151.py` (+8): both pages, a 500 or a thrown fetch, admin or not, under node. Each checks the line, no form, and Connect not disabled.
- `test_card_check_failed_2151.py` (+1): `unreachable` records nothing.

None of these states can be produced on alpha, so they rest on the pins.

Verified how: CI ruff 0.6.9 check and format --check exit 0, the mypy gate at ceiling, and CI's exact full-suite command plus `check_fullsuite_backlog.py` (17,734 passed). The gate's only NEW is a local-database leftover that fails the same way on origin/main. Layer: unit, the pages' own JS under node, and the full suite. Denominator: 3 of 3 gaps.

-- Lead
