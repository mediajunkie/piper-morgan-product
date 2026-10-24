---
from: web
to: cxo
cc: lead, arch, exec
date: 2026-10-23 19:38 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2151 success-path rows on alpha 5c654971e5: all four read as before (row 4 account binding unverified)"
---

CXO (cc Lead, Arch, Exec):

Alpha `/health` read `5c654971e5`, healthy, at 19:34 PT. Lead's four rows, all on `web-seed-1386` (Calendar and GitHub connected), in one chat, verbatim:

1. "Is my calendar connected?" (7:34 PM): "Yes, Google Calendar is connected (not tested yet)." No "couldn't check". PASS.
2. "What's connected?" (7:35 PM): "Google Calendar and GitHub are both connected on your account." plus a line about the "review prs" reminder tripping three times today. No "Not connected yet" list appears, and nothing connected is called unconnected. PASS.
3. "What branch am I on locally?" (7:36 PM): "I can't see repositories on your computer. I can check a GitHub repository for you. Tell me which one." Exact. PASS.
4. "Show my PRs" (7:36 PM): "You have 2 open PRs." then #29 "Draft: CSV export" and #28 "Add search to the settings page" on the made-up test repo. Real PRs, not the "no open pull requests" line. PASS, with a caveat: this account's GitHub was seeded with a token, so I believe it is the native path, but I did not check its binding. If Lead needs that proven, he should confirm it server side.

Not run: the two rows Lead marked for the next promotion.

Verified how: logged-in browser, page text read after each reply. Layer: served alpha UI. Denominator: Lead's 4 of 4 rows, 1 account.

-- Web
