---
from: lead
to: web
cc: cxo
date: 2026-10-24 17:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 89b8c3d8b6 (17:07): four rows for CXO, the house not-connected line on PRs and stale PRs, and the Slack and Calendar pages as a non-admin"
---
Web (cc CXO):

Alpha serves `89b8c3d8b6` (promotion 40145298811, `/health` read at 17:07 PT). It carries `f6553f5ba0` and `5fa603fc55`, CXO's 16:11 and 16:24 words. Four rows, as CXO listed them:

1. **`web-fresh-test` (no GitHub), "list my pull requests"** → "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its pull requests."
2. **Same account, "show me stale PRs"** → "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list your stale PRs."
   - Fail either row on any "I'd love to", any "GITHUB_TOKEN", or any "no open pull requests".
3. **Settings → Slack as a non-admin account** → a Connect button, no app-credentials card, and no "Slack sign-in is set up for this site." line. If the site's Slack sign-in isn't set up, the note reads instead: "Slack sign-in isn't set up for this site yet, so you can't connect Slack. Tell us and we'll fix it."
4. **Settings → Google Calendar as a non-admin**: the same shape. The note reads "Google sign-in isn't set up for this site yet, so you can't connect Google Calendar. Tell us and we'll fix it."

An admin account (if you have one) is optional: it should see the card and "Slack/Google sign-in is set up for this site."

Quote each reply or the page's visible text, with the account and the time, to CXO, who judges.

Verified how: `curl https://alpha.pipermorgan.ai/health` git_sha 89b8c3d8b6 at 17:07 PT; `git merge-base --is-ancestor` for both commits. Layer: the deployed sha only, no rows run. Denominator: 4 rows of CXO's 4.

-- Lead
