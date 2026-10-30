---
from: arch
to: lead
cc: exec, ppm
date: 2026-10-30 15:04 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Haiku 5.5 screen: price plan accepted. Re-price from the probe; same tree on both arms; temperature handled as served. PPM's gate condition concurred"
---
Lead (cc Exec, PPM),

Your 15:0x plan meets my bar, so run it. Three conditions:

1. **Re-price from the probe before you submit the batch.** The 5.5 rate you used ($0.05/M in, $0.25/M out, batch) is the one number in the table that nobody has measured yet. It is a tenth of 4.5's rate, and I haven't verified it either. Read the probe's `usage` and its billed cost, and put one line in your report: the per-call cost on 5.5 as measured, and the screen total recomputed from it. The bound is small even if the rate is wrong: if 5.5 priced like 4.5, the screen would be about $2.60, because the 4.5 control is most of it. So a wrong rate isn't a block; it's a correction to the number Exec gives xian.
2. **The two arms differ only in the model.** Both arms come from the same tree and the same render of the catalog. The `--model` override applies at the call, never in `services/`, and the side branch never reaches main. If the probe shows 5.5 refuses `temperature`, run 5.5 the way the served path would (add it to `MODELS_WITHOUT_TEMPERATURE` in the harness's copy of the call, or drop the parameter for that arm), and say so in the report. That difference becomes part of the switch's diff, so the screen has to measure it.
3. **Report the 13 ×6 rows per arm**, the eight I named plus the five standing sentinels, before the full-run category table. If a named row moves on 5.5 and nothing else does, I want to see it first.

**PPM's 14:56 gate condition:** I concur. The switch lands on main after the current promotion serves, and Lead holds it until `/health` shows `ac5b69f865` (it already does as of 15:01). Any later promotion that carries the switch re-runs row 2 and all of row 3 if it reaches alpha before xian's go/no-go. When to promote it is xian's call. My validation of the switch landing will name that condition, so it isn't lost between seats.

Verified how: Lead's and PPM's memos and Exec's 15:0x question, read in full. The price bound is my arithmetic on Lead's table: 616 × $0.00185 ≈ $1.14 a 4.5 arm, so about $2.28 for both full arms, plus the ×6 sets and the probe, is about $2.60. Layer: mail and my arithmetic. No Console read and no model call.

— Arch
