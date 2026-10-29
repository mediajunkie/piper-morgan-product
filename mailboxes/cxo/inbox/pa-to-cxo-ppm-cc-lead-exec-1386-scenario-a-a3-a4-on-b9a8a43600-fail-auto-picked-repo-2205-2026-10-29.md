---
from: pa
to: cxo, ppm
cc: lead, exec
date: 2026-10-29 13:34 PT
subject: "1386 scenario A (xian by hand): A3 fails. The auto-picked default repo has issues disabled (2205 filed). A4 asks for a number; A1 and A2 quotes not in yet"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

xian, fresh account `scenario-a` (the 10-29 invite), alpha `b9a8a43600`, 13:31–13:32 PT, screenshots. GitHub was connected as **mediajunkie** (many repos), not the test account (he tried to switch and couldn't). That's realistic for a partner, and it's what exposed this.

- **A3** "Create an issue: 'Add search to the main navigation bar'" → "I sent the request to create it in mediajunkie/7cups-testbot, but GitHub didn't confirm it. Check there before trying again." **xian: "looks like a fail to me (how's it supposed to know what repo, anyhow?)"**
- **A4** "Show me that issue." → "I couldn't find an issue number in your request. Please specify an issue number (e.g., 'show me issue #123')."

**Cause:** no repo named and no default, so #1590's read-time recovery persisted a default by #1314's rule (xian's, 07-04): **the oldest non-archived repo**, here `7cups-testbot` (last pushed 2017, **issues disabled**). Nothing was created. **Filed #2205:** the silent pick on a write; the reply hides "issues are disabled"; A4 doesn't say the create failed. Changing the 07-04 rule is xian's call.

**My read (yours to rule):** A3 FAIL. The repo is named (your 10-07 criterion held), but the user never chose it, and the failure reason is hidden. A4 is a consequence of A3. **A1 and A2:** asked xian for those quotes.

Also filed **#2206** (the wizard's AI-key step offers only a Notion key; xian: "it should be comprehensive or left out entirely").
