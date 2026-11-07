---
from: web
to: lead, cxo
cc: arch, pa, exec
date: 2026-11-07 08:03 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2282 step 4 passes: Connect pressed on beta, GitHub sign-in as dinp-machine, landed back on beta connected. No revoke. And the #2286 approval note was seen on screen"
---
Lead, CXO (cc Arch, PA, Exec),

xian said yes this morning to signing dinp-machine in on GitHub for the #2282 step 4 check: a Connect from beta, landing back connected on beta, no revoke. Done at 08:02 on beta `641ef2eb56` (health read just before this memo).

**Step 4, in order:**
1. Signed in on `https://beta.pipermorgan.ai` as web-fresh-test, a Piper account with no GitHub grant. Opened Settings → GitHub: heading `Not Connected`.
2. Pressed `Connect with GitHub`. The browser went to GitHub's login with `redirect_uri=https%3A%2F%2Fbeta.pipermorgan.ai%2Fapi%2Fv1%2Fsettings%2Fintegrations%2Fgithub%2Fcallback`. The callback host in the connect link is `beta.`, not `alpha.`.
3. Signed in on GitHub as dinp-machine. GitHub did not show an approval page: dinp-machine approved the app on 10-15 and I did not revoke it, so I did not see the "Authorizing will redirect to …" line. That acceptance row (consent page reads beta) stays unread by me.
4. The browser landed on `https://beta.pipermorgan.ai/settings/integrations?github_success=true&github_login=dinp-machine`, still signed in. Integrations reads `Connected as dinp-machine.` Reopening Settings → GitHub on `beta.` reads `Connected` and `✓ Connected with GitHub.`

So the round trip stays on beta, with the session intact. This is the case #2281 broke.

**#2286, seen on screen (CXO's open row):** before step 2, on the same unconnected account, the page showed above the Connect button: "GitHub will ask you to approve Piper Morgan. Its page names the account that owns the app, which is Piper's and not yours, and says which of your GitHub accounts it wants to access. Check that account is the one you mean. Piper only gets access to the account you approve there." After connecting, that group is replaced by `✓ Connected with GitHub.`, as in the source.

**State left behind:** web-fresh-test is now connected as dinp-machine on beta. I did not disconnect it, web-seed-1386 or web-oauth-test. One more Piper account holding the same GitHub identity worked without complaint. Say if you want web-fresh-test disconnected.

**Closing:** `OWED-CLOSED[key: web-2282-step4]` done as above. For the consent-page row, someone needs a revoke first (xian's earlier word was no revoke today), so that row is open.

Verified how: chrome-devtools in an isolated context against beta; read the connect link's `redirect_uri`, the post-login URL and the page text. Layer: browser, served. Denominator: one account, one Connect, one GitHub identity; the consent page was not shown.

— Web
