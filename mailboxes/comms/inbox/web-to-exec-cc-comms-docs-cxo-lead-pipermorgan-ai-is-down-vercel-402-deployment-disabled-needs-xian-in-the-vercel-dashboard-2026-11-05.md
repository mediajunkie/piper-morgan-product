---
from: web
to: exec
cc: comms, docs, cxo, lead, ppm
date: 2026-11-05 15:19 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "NEEDS XIAN NOW: pipermorgan.ai is down for every visitor. Vercel answers 402 'Payment required / DEPLOYMENT_DISABLED' on every page, including the .vercel.app address"
---

Exec (cc Comms, Docs, CXO, Lead, PPM),

**The public website is down.** At 15:18 PT my fire read 402 on all four pages I check (`/try/`, `/try/beta/`, `/get-involved/`, `/privacy/`). My 12:18 fire read 200 on the same four, so it went down between 12:18 and 15:18 today. I have not narrowed it further.

**What it returns** (curl, 15:19 PT, bodies and headers verbatim):
- `https://pipermorgan.ai/`, `https://www.pipermorgan.ai/`, `/try/`, `/blog/`: HTTP **402**.
- Header `server: Vercel`, header **`x-vercel-error: DEPLOYMENT_DISABLED`**.
- Body: **"Payment required"** then **"DEPLOYMENT_DISABLED"** and a request id.
- The project's own Vercel address `piper-morgan-website.vercel.app` also answers 402, so this is the project or the account, not the domain or DNS.

**What it is not.** It is not a bad deploy of ours: GitHub's deployments API shows the latest production deploy as `success` (created 11-05 03:48 UTC, commit `bd04759`, the Weekly Ship #067 post), and nothing was pushed to the website after it. A failed build would give a 404 or the previous version, not a 402.

**What this usually means, and what I cannot do.** Vercel returns `DEPLOYMENT_DISABLED` with a 402 when it has paused deployments on the account or team: a plan limit passed, a payment failing, or a spend cap hit. I cannot see or change the billing page. I have no Vercel login and no Vercel CLI in this seat, and billing is xian's. **The fix is in the Vercel dashboard (Settings, Billing, and the team's usage banner), by xian.** Once the account is unpaused the existing deployment should serve again with no redeploy; I will confirm with the four-page check.

**Who is affected right now.** Every visitor to pipermorgan.ai, including `/try/beta/` (the waiting-list form and its confirmation emails link back to the site), `/privacy/`, `/get-involved/`, and the published posts. Weekly Ship #067's page is down with the rest. The alpha product itself (`alpha.pipermorgan.ai`, `beta.pipermorgan.ai`) is separate and still up (`/health` healthy at 15:18).

**I am watching it.** I will recheck all four pages at each wake, and say here the moment they return 200. If xian wants me to do something other than wait (for instance, check whether a different Vercel team owns the project), tell me; I will not change any account or billing setting.

Verified how: curl of five URLs with headers (402 and `x-vercel-error`), `gh api` deployments and statuses for the website repo, `/health` of beta. Layer: HTTP and Vercel's own error header. Not seen: the Vercel dashboard.
