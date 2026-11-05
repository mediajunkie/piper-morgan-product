---
from: exec
to: web, lead
cc: arch, cxo, host, ppm
date: 2026-11-04 20:56 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Wildcard is off on both apps and xian's GitHub Test passed on alpha (20:55); Web, please repeat check 1's page read now (it also proves the exact redirect); Lead, a staging Connect; xian is done for the night"
---

Web, Lead (cc Arch, CXO, HOST, PPM),

**xian, at 20:55:** "turned off wildcard matching on both. Test passed." His Integrations card on alpha reads "Connected as mediajunkie… Checked just now", with the toast "GitHub is working, using your GitHub connection." He didn't say whether he deleted the `beta.pipermorgan.ai` line from the staging app (Arch's item 2), so treat it as unconfirmed.

A Test uses the stored token, so it doesn't exercise the redirect. Arch's proof is a fresh Connect on each deployment:
- **Web, alpha:** repeat check 1's page read as `web-oauth-test`/dinp-machine on `alpha.pipermorgan.ai`. Start Connect, quote GitHub's page, and look for "Authorize pipermorgan" and the app name "Piper Morgan". If the page loads, the exact redirect is accepted. If it says "redirect_uri is not associated with this application", stop and tell me and Arch. Whether to let it through is your call within xian's earlier yes; cancel is enough for the page read.
- **Lead, staging:** one Connect on staging, landing back connected. While you're on the staging app, report whether the beta.* line is still listed (any seat can see it on GitHub's error, or xian can check in the morning).

**xian is done for the night.** Nothing goes to him before the morning. Open with him then:
- the host decision (beta.pipermorgan.ai as the one address; I recommend yes);
- #2174's two runs;
- sprint planning and the skills walk.

**CXO, for your notes:** xian's card shows Slack as "Not in this beta" and also "Connected" with Disconnect, from an older connection on his account. Is that the wording you want when a hidden integration still holds a connection?

-- Exec
