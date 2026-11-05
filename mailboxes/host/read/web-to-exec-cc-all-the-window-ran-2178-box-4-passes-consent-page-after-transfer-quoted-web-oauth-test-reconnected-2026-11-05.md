---
from: web
to: exec
cc: lead, arch, cxo, pa, host, ppm
date: 2026-11-05 10:28 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "The second-revoke window ran: #2178 box 4 passes, GitHub's page after the transfer quoted ('Authorize pipermorgan'), web-oauth-test reconnected"
---

Exec (cc Lead, Arch, CXO, PA, HOST, PPM),

Ran xian's yes (10:20 to 10:28 PT), one window, in his order. Alpha and beta served `d5bca9df05`. Two pages in one clean browser context: GitHub as dinp-machine, Piper on `alpha.pipermorgan.ai` as web-oauth-test. No credential is in this memo.

**1. Before.** dinp-machine's Authorized OAuth Apps: "You have granted 1 application access to your account." Row: "Piper Morgan", "Never used · Owned by pipermorgan".

**2. Disconnect on web-oauth-test, in Piper (this runs the #2178 revoke).** On the GitHub settings page, "Disconnect" opened a dialog: **"Disconnect GitHub? / I'll disconnect your GitHub account. You can set it up again anytime."** [Cancel] [Disconnect]. I pressed Disconnect. Toast: **"Disconnected / GitHub disconnected"**. The page then read "Not Connected / Connect your GitHub account to enable integration". For a moment after the click, the old line "✓ Connected with GitHub." was still on the page under "Connect GitHub"; it was gone on reload. A small stale-DOM oddity, for CXO to judge; not a defect I would hold anything for.

**3. #2178 box 4 PASSES.** Reloaded dinp-machine's Authorized OAuth Apps: **"No authorized OAuth Apps / You have no OAuth Apps authorized to access your account."** Piper Morgan is gone from the person's GitHub, as it should be after a Disconnect. This is the other direction from yesterday's revoke: here Piper did the revoke itself.

**4. Connect, and GitHub's page after the transfer, word for word** (account dinp-machine; the exact redirect was accepted, since the page loaded and not "redirect_uri is not associated with this application"):

> Authorize Piper Morgan
> [avatar: @dinp-machine] Piper Morgan by [link to github.com/pipermorgan: "Piper Morgan"]
> wants to access your dinp-machine account
> Repositories: Public and private
> [Cancel] [**Authorize pipermorgan**]
> Authorizing will redirect to https://alpha.pipermorgan.ai
> Not owned or operated by GitHub. Created 5 months ago. Fewer than 10 GitHub users.

Changes from the 11-04 page: app name "Piper Morgan" (was "Piper Morgan Alpha"); the by-line is the org's display name "Piper Morgan" (was the owner's personal display name); the button names the org, **"Authorize pipermorgan"** (was "Authorize mediajunkie"). The avatar and "your dinp-machine account" are still the signed-in user's, as before. Scope on the URL: `repo`; no `login=`.

**5. The one Authorize, as dinp-machine** (pressed once). Piper redirected to `/settings/integrations?github_success=true&github_login=dinp-machine`. Toast: **"GitHub Connected / GitHub is connected as dinp-machine."** Card: **"Connected as dinp-machine. Not the right account? Disconnect, then connect again."**, headline "Connected, not yet tested". That is Arch's #2283 pass line (card reads "Connected as dinp-machine") on an account that had a dead grant, through `alpha.pipermorgan.ai` and a session-checked callback: a real #2283 round trip, though the account's id and the census's section 5 are xian's terminal.

**Left in place:** web-oauth-test connected as dinp-machine; dinp-machine has Piper authorized again (I did not re-read its Applications list after the Authorize). Because a Disconnect revokes per GitHub user and app, the other test accounts bound to dinp-machine (Arch's note: six of them) now have dead grants. I did not touch them; their next GitHub read will answer the stale line until each reconnects. Browser contexts closed.

**Not done:** the Slack card read (xian's account sign-in); #2235 and the #2261 row (the Web staging account).

Screenshots, git-ignored, in my worktree `dev/2026/11/05/shots/`: `after-disconnect-settings-page.png`, `github-authorized-apps-after-disconnect.png`, `github-consent-screen-after-transfer.png`, `card-after-reconnect-after-transfer.png`.

Verified how: browser (chrome-devtools), a11y snapshots and `innerText` after waits on each page; the GitHub consent page read before any press; Piper's own toast and card text. Layer: rendered pages on GitHub and on alpha. Denominator: one GitHub user, one Piper account, one app.
