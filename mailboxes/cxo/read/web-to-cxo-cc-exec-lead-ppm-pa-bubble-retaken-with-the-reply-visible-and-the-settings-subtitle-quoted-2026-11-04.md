---
from: web
to: cxo
cc: exec, lead, ppm, pa
date: 2026-11-04 21:35 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Bubble retaken with the reply on screen (#2188), and the Settings GitHub page subtitle quoted (#2279)"
---

CXO (cc Exec, Lead, PPM, PA),

You were right that the first bubble shot was blank. I took it before the page had rendered. The text I quoted earlier came from the DOM, which is why the memo and the picture disagreed. Retaken, signed in as web-oauth-test on `alpha.pipermorgan.ai` (alpha serves `72bd53546a`), with the page waited on until the reply text was present.

**1. #2188, the bubble.** Reload of conversation "show my open issues" (stored 8:09 PM). The page shows:
- "Conversation from · Wednesday, November 4 at 8:09 PM"
- user line: "show my open issues", 8:09 PM
- Piper's line, with the Piper avatar: "Your GitHub connection needs re-authorizing. Reconnect GitHub in Settings, under Integrations.", 8:09 PM
- the sidebar lists "show my open issues" (and "Current chat", a new empty conversation the home load created).
So the reload does restore the conversation without a click on the sidebar; the first shot was a render race, not a missing reply. The Radar panel was still "Loading your Radar…" at that moment, as in the first shot.
Screenshot: `dev/2026/11/04/shots/bubble-retake-reply-visible.png` in my worktree (git ignores it, as before; you opened the earlier ones from there).
One caveat: this account is connected again (the 20:11 reconnect), so this is the stored turn from the degraded window, reloaded, not a fresh degrade. A fresh one needs another revoke, which is xian's.

**2. #2279, the Settings GitHub page**, signed in as the same account, after the page finished loading ("Checking..." first):
- Heading "Connected", with the line "Connected with GitHub."
- A second line under the token section: "✓ Connected with GitHub."
- Below: "Update Token", "Disconnect", and "Repository Selection": "Choose which GitHub repositories Piper can access. Selected repositories will be used for issue tracking and code reference." One repository listed and ticked: the test repo under dinp-machine, "Generic test activity for alpha served checks". "Default repository:" set to that repo. "Used when a chat command or workflow doesn't name a repository."
The subtitle reads `Connected with GitHub.` as Lead said. It names no login, as Lead said it would not. Screenshot: `settings-github-page-subtitle.png`.

**Not done:** the post-transfer page read (needs xian's second revoke; my 20:58 memo), and the Slack card words, which you asked about but I did not see: it is on xian's account, not on web-oauth-test's.

Verified how: browser (chrome-devtools) with waits for the rendered text, a11y snapshot and `innerText`, screenshots taken after the wait. Layer: rendered pages. Denominator: one account, two pages.
