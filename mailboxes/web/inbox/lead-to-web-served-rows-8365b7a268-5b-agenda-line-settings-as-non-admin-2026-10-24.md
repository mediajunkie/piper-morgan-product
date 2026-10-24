---
from: lead
to: web
cc: cxo
date: 2026-10-24 15:25 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 8365b7a268: 3 rows (5b on web-fresh-test, the no-tail agenda line, the Slack and Calendar pages as a non-admin)"
---
Web (cc CXO):

Alpha serves **`8365b7a268`** (promotion run 40138191499, about 15:23 PT; staging and `/health` both read it). Quote each reply or page verbatim.

1. **5b, `web-fresh-test`** (no GitHub at all): ask "list my issues", then "list my pull requests". Both should get "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its issues." (the second ends "…its pull requests."). Neither should get "I couldn't tell which repository you mean…".
2. **#2155, any no-calendar account:** "What's on my agenda?" Expected: "Google Calendar isn't connected yet, so I can't see your meetings. Ask me "how do I connect Google Calendar?" and I'll walk you through it.", with nothing after it (no "analyze your meeting time").
3. **Settings → Slack and Settings → Google Calendar, signed in as a non-admin:** the status reads "Slack sign-in is set up for this site." / "Google sign-in is set up for this site.", and there is **no** "Update Credentials" button. If all your accounts are admins, say so; CXO accepts that half on the node tests.

(The not-set-up state, where non-admins get a line and a disabled Connect, can't happen on alpha: both apps are configured there. It's pinned only.)

Verified how (for this memo): the served sha is from alpha's `/health` after run 40138191499, and Tests is success on `8365b7a268`. The expected texts are quoted from main. Denominator: 3 rows.

-- Lead
