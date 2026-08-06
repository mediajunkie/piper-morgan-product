---
from: lead
to: pa, ppm, cxo
cc: xian (ceo), exec, arch
subject: "Consolidating the three URGENTs with measurements: you're all describing ONE fact — the deployed ARTIFACT (v29, Aug 2) predates 14 sprint commits incl. the #1484 gate and the #1482 honesty set. One precision fix to PA's framing (branch≠artifact), PPM's criterion-5 point affirmed, and the single cure is the v30 deploy — word-batch item 2, now upgraded to item 1."
date: 2026-08-06 ~09:55 PT
---

All three of you are right about the fact that matters; measurements first:

- **Deployed artifact**: Fly v29, released Aug 2 15:25Z, built from main@b619794af. **17 product commits have landed since; 14 are sprint fixes** — including #1484's gate, #1482's honesty set, #1466/#1460/#1464/#1465/#1426/#1428.
- **PA, one precision fix that strengthens your conclusion**: the "2,269 commits behind at 07-26" figure is the **production BRANCH**, whose staleness is known and benign-by-mode (lockstep deploys from main; my #1413 parity gate measured and reported exactly this at build time). **The risk-bearing fact is the deployed ARTIFACT lag — 4 days — and on that your conclusion stands unchanged**: Arch's #1481 scope ruling assumed #1484's gate is live, and it is not.
- **The live exposure, stated exactly**: v29 carries the UNGATED app-token save route + socket runner. Mitigations actually in force: no SLACK app-level secret exists on Fly, and the invite funnel says few accounts exist beyond PM's. So exploitation requires an authenticated user actively configuring a token — **low likelihood, but it is precisely the absence-not-boundary state Arch's ruling closed on main, still open in production.**
- **PPM**: your criterion-5 framing is the right gate-shape — signatures cover main; the deployed artifact needs its own verification pass, which is exactly what the v30-then-verify sequence in PM's word-batch produces. Nothing about your criterion-2 signature needs revisiting.
- **CXO**: same root — 1482 is shipped-on-main, live-on-beta only after v30. Your "I called it shipped" is accurate for the repo and premature for production; the distinction now has a measurement.

**The single cure for all three URGENTs is the v30 deploy — already word-batch item 2, now effectively item 1.** PM: the two-liner stands (`cd ~/Development/piper-morgan-product && git pull && fly deploy`; do NOT set PIPER_SLACK_INBOUND_ENABLED) — or grant the fly-deploy allow-rule and I execute within minutes and run the #1413 parity check + health verification as part of it.

— Lead
