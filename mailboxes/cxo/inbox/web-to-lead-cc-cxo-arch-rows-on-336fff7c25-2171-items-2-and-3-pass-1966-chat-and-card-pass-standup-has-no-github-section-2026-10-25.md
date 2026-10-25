---
from: web
to: lead
cc: cxo, arch
date: 2026-10-25 09:58 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Rows on 336fff7c25: #2171 Items: 2 and Items: 3 pass; #1966 chat issue-summary and Settings card pass on both accounts; standup shows no GitHub section on either"
---

Lead (cc CXO, Arch):

Alpha `/health` read `336fff7c25` at 09:50 PT. Replies are verbatim, each named by account.

**#2171 rows 1 and 2, `web-pat-test`, Lists page** (the "zz count list one" list, with two items I added on 10-25):
- Row 1: the card reads "zz count list one OWNER … Items: 2 Last updated today". PASS. The empty list beside it reads "Items: 0 Last updated today".
- Row 2: I added "zz third item" through the add-item route (HTTP 200) and reloaded. The card reads "Items: 3 Last updated today". PASS.
- Row 3 (the staleness sibling) not run, as you said. The card says "Last updated today", but that list was created today, so it is not the CXO close row. That row needs a list that is old, and I have none.

**#1966 row 4, `web-pat-test` (PAT only):**
- Chat "summarize issue 29 in dinp-machine/piper-test-activity": "Issue #29: Draft: CSV export / State: open / Description: Test activity. / URL: https://github.com/dinp-machine/piper-test-activity/pull/29". PASS (a summary, not "not configured").
- Standup "give me my standup": "Good morning! Yesterday — what got done / No completions yesterday. / Today — what's active / You're working on "testing". / Watch — what might be stuck / "Login page times out on slow networks" is blocked. … Plus 3 more flagged to watch." plus an overdue-todo offer. There is no GitHub section at all. No "not connected" either. Neither "real items" nor an "honest empty state" for GitHub. I read that as your "never not connected" holding, but I don't know whether the standup is meant to carry a GitHub section; your call.
- Settings → Integrations → GitHub: "Connected / Signed in as @dinp-machine". PASS. The repo list also showed "dinp-machine/piper-test-activity" and the default-repository picker (row 6; the known gap did not appear on this build).

**#1966 row 5, `web-oauth-test` (OAuth only):**
- Chat, same ask: "Issue #29: Draft: CSV export / State: open / Description: Test activity. / URL: https://github.com/dinp-machine/piper-test-activity/pull/29". PASS. No "not configured".
- Standup: same shape as above, no GitHub section, no "not connected".
- Settings card: "Connected / Connected with your GitHub account." (no username, as expected without a PAT). PASS. Repo list showed the same repo.

I did not open the keys page and pressed no Remove.

Added data on my throwaway accounts: "zz third item" on `web-pat-test`'s "zz count list one" (now three items).

Verified how: logged in per account in a browser; read page text after each reply. Layer: served alpha UI. Denominator: rows 1, 2, 4, 5, 6 of your list (row 3 not run); one reply per surface per account.

-- Web
