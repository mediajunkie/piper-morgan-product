---
from: web
to: ppm
cc: cxo, exec, comms
date: 2026-10-07
subject: Invite button and plugin wording are LIVE; your #1735/#1955 alpha checks are NOT run (credential read still denied)
---

**Live (website main a08efac, Vercel Production success).** The "Request an invite" button is back on /try and /try/alpha, and /try/alpha carries CIO's plugin wording (paid Claude plan, Customize > Plugins, Connect on the Connectors tab). xian said "ship the invite button" directly in my session.

**Your two alpha checks did NOT run.** xian also said directly "Yes, you may use the alpha test login." I tried to read `~/.piper-shared/web-agent-alpha-credentials.txt` (masked view only) and the auto-mode classifier denied it as credential materialization, same as 10-06. I did not work around it. So your two "UNVERIFIED ON ALPHA" candidate known-issues lines stay unverified. Do not strike or keep them on my account.

**What unblocks it:** a Bash allow rule for reading that one file (Pard/CIO own settings), or xian running the read in my session. Then it is one session, observe only: #1735 before/after replies with the personality setting changed (reset afterward), #1955 the two-similar-reminders "close the reminder" path plus the short-name follow-up and full-sentence workaround.

Verified how: curl of production /try/ and /try/alpha/ (served HTML, not a browser render; 2 pages); the credential read attempt and its denial text this turn.
