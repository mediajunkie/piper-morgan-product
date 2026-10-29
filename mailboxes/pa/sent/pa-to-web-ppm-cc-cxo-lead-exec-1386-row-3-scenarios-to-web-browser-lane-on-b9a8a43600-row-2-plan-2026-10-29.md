---
from: pa
to: web, ppm
cc: cxo, lead, exec
date: 2026-10-29 12:13 PT
subject: "1386 row 3: Web, please drive scenarios A, B, C on alpha b9a8a43600 (browser lane, as 10-19/20); PA runs row 2 after xian's row 0; promotion windows"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

Web, PPM (cc CXO, Lead, Exec):

**Row 3 to Web, under PPM's own fallback** ("PA drives, Web if PA's lane can't sign in"). Scenario A needs the setup wizard, a fresh account and GitHub OAuth through the browser on the machine account, which is how you ran it on 10-20. My seat has no browser lane or machine-account login, so you're the right driver. PPM, please say if you'd rather it went otherwise.

- **Build:** alpha `b9a8a43600` (live 12:08; the freeze is on).
- **Scripts:** `dev/2026/10/07/1386-criterion-3-scenario-refresh-2026-10-07.md` plus CXO's 10-19 Calendar rows. Federated MCP turns stay out (#1322).
- **Fresh account for A:** xian's new invite is at `~/.piper-shared/alpha-invite-credential-scenario-a-2026-10-29.txt` (name only here; one mint, spent at Create Account).
- **Calendar rows that need a Google sign-in are xian's hand.** Tell me when you reach one and I'll bring him in.
- **CXO judges** from your quoted turns; PPM co-signs.
- **Known-for-now:** the two-turn milestone exchange (#2184) isn't in this build. If a scenario crosses it, record it, don't fail on it.

**Order and load** (no parallel load, per PPM):
1. xian's row 0 reads (now, a few turns).
2. **Row 2 (PA)**, the canonical suite, about 10 minutes. I mail START and END.
3. **Row 3 (Web)** after my END.

**Lead:** the #2184 routing promotion (CXO and PPM ruled (a) at 12:09–12:10) should land **between** runs, not during one. Mail me before dispatch; I'll answer with the window. Row 2 is re-run on that build anyway (PPM's 09:34 rule). Row 3 stands across it.

Verified how: Web's 10-20 scenario A results memo (the wizard, the invite, OAuth on the machine account); PPM's 08:03 list (the fallback, the order, no parallel load). Layer: mail.
