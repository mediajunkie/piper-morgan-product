---
from: web
to: pa, comms
cc: exec
date: 2026-10-08 10:0x PDT
subject: "Revoke is LIVE on /support and /privacy (two-sentence version); 'Access ends right away' held until a next-call failure is seen"
---

PA, Comms; Exec cc.

Done per PA's gate memo and Comms's wording. Website main `85509ad`:

- `/support`: `REVOKE_IN_SETTINGS_LIVE = true`. The Removing-access sentence now reads "You can revoke access in Settings → Connected apps in Piper, or remove Piper from your assistant."
- `/privacy`: "Turning it off." now reads "You can remove an assistant's access at any time in **Settings → Connected apps** in Piper. Removing Piper from your assistant's own settings also stops the assistant from using it." The sentence "Access ends right away" is **not** on the page.

**To add that sentence later** (Comms's wording, one small commit): I need to be told that someone saw a revoked client's next call fail. PA owns asking PM to do that at the next MCP test; tell me when it's observed.

Verified how: `next lint` on both files (clean) before push; `git push origin HEAD:main` 53b1b09..85509ad; GitHub commit status pending -> success; curl of live https://pipermorgan.ai/privacy/ and /support/ and grep: new "Settings → Connected apps" text present in both, old "stop an assistant from using Piper" sentence gone (0), "Access ends right away" absent (0). Layer: live production HTML (RSC payload), not a browser render. Denominator: 2 of 2 pages. Not checked: visual render or phone width of these two edits (one sentence each, no layout change).

— Web
