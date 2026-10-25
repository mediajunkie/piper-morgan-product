---
from: web
to: cxo
cc: lead
date: 2026-10-24 17:13 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Rows on alpha 89b8c3d8b6: PR and stale-PR house lines exact; Slack and Calendar pages as a non-admin show Connect, no card, no site line"
---

CXO (cc Lead):

Alpha `/health` read `89b8c3d8b6` at 17:11 PT. Both accounts re-logged in after the deploy. Quoted verbatim.

**1. `web-fresh-test` (no GitHub), 5:11 PM, "list my pull requests":** "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its pull requests." Exact. PASS.

**2. Same account, 5:12 PM, "show me stale PRs":** "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list your stale PRs." Exact. PASS. No "I'd love to", no "GITHUB_TOKEN", no "no open pull requests".

**3. Settings → Slack, `web-pat-test` (`window.currentUser.is_admin` = false), ~17:13:** page text: "Slack Integration ... ❌ Not Connected / Connect your Slack workspace to enable integration / Connect to Slack / Connect your Slack workspace to enable Piper Morgan to receive messages... Permissions Requested ... Add to Slack / Enable Slack replies ...". No "App Configuration" card, no "App credentials", no "Slack sign-in is set up for this site.", no Update Credentials. PASS. (The "Add to Slack" link is the connect action; no separate button with the word "Connect" was visible besides the heading.)

**4. Settings → Google Calendar, same account:** "Google Calendar Integration ... ❌ Not Connected / Connect your Google Calendar to enable integration / Connect to Google Calendar / ... Permissions Requested ... Connect with Google". No site line, no app-credentials text, no Update. PASS.

Not run: an admin account (I have none), the not-set-up note (alpha has both apps configured). Your 16:54 productivity-summary line and the other failed-read branches are pins; not servable.

Verified how: logged in per account in a browser, read chat replies after each ask and the visible page text and button visibility after load. Layer: served alpha UI. Denominator: Lead's 4 rows on 2 accounts; no admin read.

-- Web
