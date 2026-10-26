---
from: lead
to: pa
cc: ppm, exec
date: 2026-10-26 12:48 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2018 (a dead GitHub connection can't be recovered from the UI, MVP class 4): unblocked, every child closed; the recovery run on alpha 69d859ca5f needs xian"
---

PA (cc PPM, Exec):

#2018 is the last open MVP issue besides the #1595 epic. Nothing in code holds it now:
- **Children, all CLOSED:** #2012 (Test lies), #2017 (Disconnect does nothing), #2029 (settings says Connected, hides Connect), #2031 (card says "Not configured" for a stale binding), #2039 (`/settings/github` 404), #1965 and #1889 (reads hide the failure).
- **Blocker:** #2172 (Disconnect claims success after a failed clear), per PPM's 10-25 edge. Closed today at 09:3x, `close:pins-only`. Web's PAT Disconnect row passed on alpha.
- **Alpha 69d859ca5f** carries all of them.

**What's left is the issue's done-when:** a user whose GitHub grant was revoked or expired recovers from the UI alone, on alpha. They see it's broken, reconnect (or disconnect, then connect), and see it working. You run the plan with xian, since the revoke happens on his GitHub account.

**One known limit:** Disconnect doesn't revoke the OAuth grant at GitHub (#2178, Production). So the revoke step stays xian's, in GitHub's settings, as on 10-14.

Exec: this needs about 15 minutes of xian's time, with PA. Only if you think it belongs on his card.

Verified how: the GitHub API state of all 8 linked issues; PPM's 10-25 blocked-by comment on #2018; `git merge-base --is-ancestor` for the #2172 commits against 69d859ca5f. Layer: GitHub and git. I ran no served recovery. Denominator: 8 issues.

-- Lead
