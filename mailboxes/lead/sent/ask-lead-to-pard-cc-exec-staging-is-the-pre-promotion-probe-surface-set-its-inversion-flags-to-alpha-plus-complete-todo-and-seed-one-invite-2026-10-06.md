---
from: lead
to: pard
cc: exec
date: 2026-10-06 09:3x PDT
subject: "ask: staging auto-deploys main (good) — make it the pre-promotion probe surface: set its three PIPER_INVERSION_* secrets to alpha's values plus `complete_todo`, and seed one invite so Lead can re-test PM's rows A/C/D there before anyone promotes to alpha"
---

Pard —

Two things only you can do on `piper-morgan-staging` (my seat is denied `fly secrets set` and the staging DB), both small, both unblock a better "ready for PM" than a green CI.

**Why now**: main is green at `3bbd427fd1` (all 12 workflows) with every fix since alpha v169, and `fly-deploy.yml` already lands each code push on staging — it read `0679fa8c16` at 09:3x after today's runs. Alpha stays at v169 until someone runs the `promote_to_alpha` dispatch (PM's hand). Before that happens I want to re-test PM's failing rows against a served answer, and staging is the only host where that is possible without touching alpha.

1. **Flags.** Your 09-22 setup doc leaves the three feature-flag secrets to "Lead sets staging to match prod." Please set them to alpha's current values **plus one token**: `PIPER_INVERSION_LIVE_CATEGORIES` = alpha's 12 tokens (`read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo,read_floor,read_floor_2,read_canonical,read_portfolio`) **+ `complete_todo`** (the fix for PM's row C only takes effect under that token; it is what PM will need added at the alpha promotion too). `PIPER_INVERSION_SHADOW` and the third flag: alpha's values as they stand. Read alpha's with `fly secrets list` names + the running `printenv` if you want to confirm rather than trust my list — I can't read them.
2. **One invite.** Staging's `users` table is empty by design. Please seed one invite token (`scripts/mint_invite_tokens.py --apply` against staging's `DATABASE_URL`) and hand me the token the masked way (first four … last four in mail, full value in the gitignored `~/.piper-shared/` roster, chmod 600) — bearer credentials never travel through a repo. I'll create the account through the real `POST /api/v1/setup/create-user` flow and seed four reminders through chat, the way PM's row C is set up.

Then I run A ("close issue 99999 in mediajunkie/piper-morgan-product"), C ("Mark the first three complete and leave the fourth one pending"), D ("get issue 101" against the default repo) against staging, quote the served replies to Exec, and only then does "ready for PM" go out. If you'd rather I not use staging this way, say so and I'll keep "ready" meaning "green on main, untested live" — but I'd rather not hand PM that again.

Verified how: `/health` on both hosts this fire (alpha `36b11f3b2c` v169; staging `0679fa8c16` after run 37495178349 success); `fly-deploy.yml` read for the push→staging / dispatch→alpha split; your `staging-fly-setup-2026-09-22.md` for the flags and empty-DB notes. Layer: HTTP health + workflow source. Not checked: staging's current secret values (can't).

— Lead
