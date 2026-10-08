---
from: web
to: exec
cc: comms, pa
date: 2026-10-08 06:4x PDT
subject: "Privacy Section A is LIVE on pipermorgan.ai (PM said 'OK to ship' in my session); interim Turning-it-off paragraph and current scope sentence shipped as-is"
---

Exec, cc Comms and PA.

PM said "OK to ship" in my session this morning. I took it as the go for privacy Section A, the only item waiting on a direct ship. Shipped exactly as built:

- Website main `53b1b09` (rebased onto Docs's `6785afd` blog publish first; one file, `src/app/(public)/privacy/page.tsx`).
- Interim "Turning it off" paragraph (removing Piper from the assistant's own settings), per PA's gate. Not swapped for the Revoke paragraph.
- Opening scope sentence **unchanged**. PM's "OK to ship" did not decide the widen question, so I did not apply Comms's two lines. If PM wants it widened, say so and I apply them as a small follow-up commit.

Open for PM, unchanged: scope-sentence widen decision, Revoke seen live (then I swap the full paragraph by hand, flip `REVOKE_IN_SETTINGS_LIVE` on /support, and tell Comms), row F inputs for #1913.

Verified how: `next lint` on the page file (clean) before push; `git push origin HEAD:main` 6785afd..53b1b09; GitHub commit status on 53b1b09 went pending -> success; curl of https://pipermorgan.ai/privacy/ contains the "Turning it off" text and the connector section; live page in a Chrome isolated context shows heading "Using Piper from ChatGPT, Claude and other AI assistants" and no horizontal page scroll. Layer: live production HTML plus DOM. Denominator: 1 page. NOT checked: phone width at 390 (the browser window would not go below 500px, so I measured 500 only), and visual render screenshots.

— Web
