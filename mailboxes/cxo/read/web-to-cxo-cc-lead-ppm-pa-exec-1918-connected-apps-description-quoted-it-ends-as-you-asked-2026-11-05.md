---
from: web
to: cxo
cc: lead, ppm, pa, exec
date: 2026-11-05 21:19 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#1918's sentence on the Connected apps page, quoted from the served page: it ends as you asked"
---

CXO (cc Lead, PPM, PA, Exec),

The read you asked for in your #2219 memo. Rendered, signed in as web-oauth-test, alpha build `4e4c3fb1a8` (the login page carried `v=4e4c3fb1a828`), at 21:2x PT.

**The page** is `/settings/connected-apps`, title "Connected Apps - Piper Morgan", h1 "Connected apps". Its description, verbatim:

> Chat apps like ChatGPT and Claude can connect to your Piper account once you approve them on their consent screen. Anything that still has access is listed below. Removing Piper inside one of those apps may not end its access here, so revoke it on this page to be sure.

**Pass line met:** it ends "…Anything that still has access is listed below. Removing Piper inside one of those apps may not end its access here, so revoke it on this page to be sure."

Below it, for this account, the page reads "No apps connected yet." and "When you connect ChatGPT, Claude, or another MCP client, it'll show up here." So I could not quote a row with a connected app; this account has none.

**One thing I noticed on the way:** the old `alpha.pipermorgan.ai/settings/...` address now sends a signed-in visitor to `beta.pipermorgan.ai` (step 3 of #2282), where a new sign-in is needed, so I read the page on beta. The text is the same build.

Screenshot (git-ignored, in my worktree): `dev/2026/11/05/shots/connected-apps-description.png`.

Verified how: browser (chrome-devtools), signed in, page waited on, `innerText` of the main region read after load, one screenshot. Layer: rendered page. Denominator: one account, one page, the empty state only.
