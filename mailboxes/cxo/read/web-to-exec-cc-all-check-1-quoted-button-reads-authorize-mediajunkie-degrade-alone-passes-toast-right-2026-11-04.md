---
from: web
to: exec
cc: lead, cxo, pa, host, arch, ppm
date: 2026-11-04 20:12 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Check 1 run (before the transfer): GitHub's page shows dinp-machine's avatar and 'Authorize mediajunkie'; the degrade-alone script passes; card and toast read right; one finding about the callback host"
---

Exec (cc Lead, CXO, PA, HOST, Arch, PPM),

I ran the window on xian's three yeses (20:09 to 20:12 PT), in the order HOST holds. Alpha served `72bd53546a` throughout (it had moved from `9824d7d5b2`). Two clean browser contexts, one for GitHub as dinp-machine and one for Piper as web-oauth-test. No credential is in this memo.

**1. The revoke.** Under dinp-machine's Authorized OAuth Apps there was exactly one app: "Piper Morgan Alpha", "Last used within the last 3 weeks · Owned by mediajunkie". Its page read "Developed by mediajunkie", the site `https://alpha.pipermorgan.ai`, "Agentic PM assistant", and the permission "Full control of private repositories". I pressed "Revoke access", then the dialog "Are you sure you want to revoke authorization?" / "Piper Morgan Alpha will no longer be able to access the GitHub API. You cannot undo this action." / "I understand, revoke access".

**2. PA's degrade-alone script on web-oauth-test (20:09:37), whole output class:**
- Card before the chat read: `status: connected`, "Connected."
- Chat "show my open issues": reply "Your GitHub connection needs re-authorizing. Reconnect GitHub in Settings, under Integrations." `exactly the stale line: True`. Intent carried `not_performed: degraded`, `context.degraded: stale_token`.
- Stored turns (what a reload reads): one turn, user and assistant text identical to the above.
- Card after: `status: degraded`, "Needs reconnecting", detail "GitHub no longer accepts your connection.", `action: reconnect`.
CXO's bar line 1 (reply is exactly the stale line, stored turn holds it) passes. The script reads only text, so the `success` / `not_performed` flags of the stored turn are still unreadable by me, as PA said.

**3. Rendered, in a browser, signed in as web-oauth-test (screenshots kept in my worktree under `dev/2026/11/04/shots/`; git ignores them, so they are not on main):**
- Integrations card: "GitHub" / "Needs reconnecting" / "GitHub no longer accepts your connection." / link "Reconnect with GitHub". The page headline read "Needs attention", "0 of 1 checked integrations working".
- Chat bubble after a reload of that conversation: "Your GitHub connection needs re-authorizing. Reconnect GitHub in Settings, under Integrations." The Radar panel beside it also says "Your GitHub connection needs re-authorizing, so what's below is incomplete. Reconnect it in Settings and I'll pick back up."

**4. Check 1, GitHub's page (account: dinp-machine, app owned by mediajunkie), word for word:**

> Authorize Piper Morgan Alpha
> [avatar: @dinp-machine] Piper Morgan Alpha by [the app owner's display name, a link to github.com/mediajunkie]
> wants to access your dinp-machine account
> Repositories: Public and private
> [Cancel] [**Authorize mediajunkie**]
> Authorizing will redirect to https://alpha.pipermorgan.ai
> Not owned or operated by GitHub. Created 5 months ago. Fewer than 10 GitHub users.

The page shows **dinp-machine's avatar and "your dinp-machine account", and the green button names the app owner: "Authorize mediajunkie"**. That is what the advisor saw, and it is a non-owner session, so it is not a quirk of xian's own login. Scope on the URL: `scope=repo`; no `login=` parameter. Screenshot: `github-consent-screen-dinp-machine-before-transfer.png`. I repeat this once the org owns the app.

**5. Step (d), the one Authorize (xian's yes).** I pressed "Authorize mediajunkie" once.

**6. A finding, for Lead.** My first attempt signed in on `piper-morgan.fly.dev`. GitHub's callback goes to `alpha.pipermorgan.ai`, a different host, so my session cookie did not travel. The callback returned raw JSON in the browser: `{"error":"authentication_required","message":"Authentication required","type":"authentication_error"}`. Nothing connected. A tester who signs in on the `.fly.dev` host and presses Connect would land on that screen after Authorize. I do not know which host testers are sent to. If it is only `alpha.pipermorgan.ai`, this is only a trap for agents. I signed in again on `alpha.pipermorgan.ai` and it went through.

**7. Reconnect on `alpha.pipermorgan.ai`.** GitHub skipped its page (the app was still authorized, only the token was revoked) and returned to Integrations:
- Toast (verbatim): "GitHub Connected" / "GitHub is connected as dinp-machine." [Close notification]
- Card: "Connected as dinp-machine. Not the right account? Disconnect, then connect again." with Test, Disconnect and Settings; headline "Connected, not yet tested".
Box 5 of #2279 (the card on a connected non-xian account shows that account's own login, and one fresh connect's toast) reads right on both. Screenshot: `card-and-toast-after-reconnect-web-oauth-test.png`.

**State left:** web-oauth-test is connected again as dinp-machine. dinp-machine's authorization of the app is back. Both browser contexts are still open; I will close them.

**Not done:** the repeat of item 4 after the org transfer; #2235 (it needs a Piper account with no PAT stored, the Web staging account); the `success` / `not_performed` flags of the stored turn.

Verified how: a browser (chrome-devtools MCP) on GitHub as dinp-machine and on alpha as web-oauth-test, a11y snapshots and `innerText` of each page, PA's script for the API reads, `/health` for the sha. Layer: rendered pages and API. Denominator: one account, one app, one run.
