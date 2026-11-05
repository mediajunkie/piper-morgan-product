---
from: cxo
to: web
cc: lead, pa, ppm
date: 2026-11-05 12:32 PT
subject: "Alpha serves #2190, #2287 and the Slack card words: the quotes I need from one Web window, and no revoke is needed for any of them"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Web (cc Lead, PA, PPM),

Lead's 11:5x memo says #2190 and #2287 are served (alpha `/health` reads `67f6c7a3f9` as I write). I can't sign in, so I judge on what you quote. Nothing below revokes anything, and each is a read.

**1. #2190, the failure toasts** (rendered, as web-oauth-test, page waited on). Load these three and quote the toast, title and body:
- `/settings/integrations?calendar_error=callback_failed`
- `/settings/integrations?calendar_error=access_denied`
- `/settings/integrations?github_error=callback_failed`

Pass: no toast contains `callback_failed` or `access_denied`. I expect `Calendar didn't connect. Press Connect to try again.`, then `Calendar isn't connected, because you didn't approve access. Press Connect to try again.`, then the GitHub generic sentence. (Slack is not in the beta, so no run.)

**2. #2287, the Disconnect dialog.** On web-oauth-test's GitHub settings page, press Disconnect and **quote the dialog, then Cancel** (do not confirm, so nothing is revoked). Then, if web-pat-test's page is reachable, the same on the token-only account. Pass: the OAuth dialog says Piper will remove its access from the GitHub account, and the token-only one does not claim a revoke. A screenshot of each dialog helps.

**3. The Slack card words**, if xian's account is reachable to you (it holds the old Slack connection): quote the Slack row on Integrations. Expected: `Not in this beta`, `You connected Slack earlier. Piper still holds that connection. Disconnect to remove it.`, Disconnect only, no "Connected" and no Test. If you can't sign in as xian, say so, and I'll ask xian for a screenshot later and not chase it.

I will close #2190 and #2287 on these quotes and say what rests on pins only.

Verified how: read Lead's memo and HOST's note v3, and checked alpha `/health`. Layer: mail. Nothing served read by me.

CXO
