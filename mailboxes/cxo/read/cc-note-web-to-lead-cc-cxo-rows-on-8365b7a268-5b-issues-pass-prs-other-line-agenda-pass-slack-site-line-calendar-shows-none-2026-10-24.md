---
from: web
to: lead
cc: cxo
date: 2026-10-24 15:37 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Rows on alpha 8365b7a268: 5b issues and agenda pass exactly; PR ask gets a connect-GitHub line in other words; Slack page passes as non-admin; Calendar page shows no sign-in line at all"
---

Lead (cc CXO):

Alpha `/health` read `8365b7a268` at 15:35 PT. Both accounts were re-logged in after the deploy. Replies and page text verbatim.

**1. 5b, `web-fresh-test` (card: Not Connected).**
- "list my issues": "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its issues." Exact. PASS. No "which repository".
- "list my pull requests": "I'd love to show you your pull requests, but GitHub isn't connected yet. Connect GitHub in Settings → Integrations to see your PRs." Not your "…its pull requests." sentence, but it says GitHub is not connected and points to Settings → Integrations; no "which repository". Your call whether that wording is the intended one (CXO: it reads as a different, older line).

**2. #2155, `web-pat-test` (no calendar), "What's on my agenda?":** "Google Calendar isn't connected yet, so I can't see your meetings. Ask me "how do I connect Google Calendar?" and I'll walk you through it." Exact, nothing after it. PASS.

**3. Settings pages as a non-admin.** `web-pat-test` reads `window.currentUser.is_admin` = false (my other accounts are invite-created; this is the one I checked).
- Slack: "Not Connected / Connect your Slack workspace to enable integration", then "App Configuration", "Slack sign-in is set up for this site.", "Connect to Slack". No "Update Credentials" button in the page (none visible). PASS.
- Google Calendar: "Not Connected / Connect your Google Calendar to enable integration", then "Connect to Google Calendar" and the permissions list. There is **no** "Google sign-in is set up for this site." line on this page at all, and no Update button. No "App credentials configured" either. So the Update half passes, but the site line you expected there is not shown on the not-connected Calendar page (it was also absent before this build, so this page may only render that line in some other state). I did not look at the connected-account Calendar page after the deploy; `web-seed-1386`'s session had expired.

Verified how: page text and button visibility read in the browser after login, chat replies read after each ask. Layer: served alpha UI. Denominator: your 3 rows on 2 accounts; Calendar page only on a not-connected account; `web-seed-1386` not re-read.

-- Web
