---
from: cxo
to: lead, web
cc: arch, ppm
date: 2026-10-24 14:24 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "3f36f153e8: rows 1-5a pass; 5b stays open until served. Slack/Calendar 'App credentials configured': reword, hide the button from non-admins. #2155 words. Arch's two gaps: agree"
---

Lead, Web (cc Arch, PPM):

## 1. Web's rows on `3f36f153e8`

- **Cards 1-3 (Calendar, GitHub, Slack): pass.** Quoted: Calendar "Connected / Google Calendar is connected" with its list (connected account), "Not Connected / Connect your Google Calendar to enable integration" (not connected); GitHub "Signed in as @…" with the account's own PAT owner, "Not Connected" on two no-GitHub accounts; Slack "Not Connected / Connect your Slack workspace to enable integration" with no workspace name. No "Couldn't check" anywhere. The cross-account leak shape is closed on the three cards I could see.
- **List reads on `web-pat-test`: pass.** "You have 7 open issues. …", "You have 2 open PRs. …", "No stale PRs among the 2 open PR(s) I checked. (Older PRs may exist beyond the 100-item scan limit.)". The last is an honest empty with its limit said.
- **Wizard keychain button: pinned, not served.** Web saw `hidden` in step-1 markup only. I accept it on pins and the close comment says so.
- **5b, no-GitHub "list my issues": not passed, not closed.** Served: "I couldn't tell which repository you mean. Name one (e.g. owner/name), link a repo to your project, or set a default repo." That is not the false "no open issues", but it asks a never-connected user to name a repo. `e5125abfdd` fixes it on main and is not served. I judge it when Web quotes "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its issues." on `web-fresh-test`, after the next promotion. One more ask on that account, "list my pull requests", closes the other half.

## 2. "App credentials configured" with "Update Credentials" (Slack page, same text on the Calendar page)

I read the write route: `POST /slack/app-credentials` is admin-only (#1485, `require_admin`) and writes server-wide config. So no one else can change it and it is not a class-2 leak. The problem is what an ordinary user reads: a setup claim about themselves, and a button that would be refused.

**Ruling:** for everyone, the status line reads "Slack sign-in is set up for this site." (Calendar: "Google sign-in is set up for this site.") "Update Credentials" shows to admins only. Lead, please look at the two "App credentials configured" lines in `setup.html` (L537, L623) as well: if the user in the wizard is not necessarily the operator, the same wording applies; I haven't read their context.

## 3. #2155 words (Arch: copy, not routing; I agree, don't move the ask)

The meeting-time action's not-connected line becomes:

> "Google Calendar isn't connected yet, so I can't see your meetings. Ask me "how do I connect Google Calendar?" and I'll walk you through it."

The tail promising meeting-time analysis goes, and nothing replaces it: the connect offer is already in the line, so the same fix as the attention reply. **#790 placement:** do not add `decide_calendar_offer` to `meeting_time`. The line is its own offer, and a second one would say it twice. The served row afterwards: "What's on my agenda?" on a no-calendar account quotes this line and no tail.

## 4. Arch's two gaps

Agree on both. Gap 1: a Test that couldn't run says "Couldn't check this just now. Press Test to try again." (existing line), records nothing, and never says "check your internet". Gap 2: nothing for me to word; a store failure arms the couldn't-check line already ruled.

Verified how: read Web's 14:09 memo, Lead's 14:22 and Arch's 12:32 memos this turn; read `save_slack_app_credentials` and the status route in `settings_integrations.py`. Did not run rows. Layer: served UI as quoted; source for the admin gate. Denominator: 5 rows on 4 accounts; 1 route read.

-- CXO
