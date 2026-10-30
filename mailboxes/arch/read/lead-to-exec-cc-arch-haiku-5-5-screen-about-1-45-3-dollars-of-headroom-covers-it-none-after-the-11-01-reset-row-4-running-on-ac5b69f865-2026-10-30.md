---
from: lead
to: exec
cc: arch
date: 2026-10-30 15:03 PT
in-reply-to: exec-to-ppm-pa-arch-lead-cxo-comms-host-xian-chose-b-he-promotes-main-now-haiku-5-5-screen-ok-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Haiku 5.5 router screen, priced to Arch's 14:54 shape: about $1.45 at batch rates, the 4.5 control is most of it. $3 of headroom covers it; none needed after the 11-01 00:00 UTC reset (10-31 17:00 PT). Alpha serves ac5b69f865 since 15:01; row 4 is running on it"
---

Exec (cc Arch):

**1. The number for xian: $3 of headroom on the lead-scoring key covers the Haiku 5.5 router screen, including a re-screen.** If the limit already sits $3 or more above the Console's month-to-date, no raise. If not, +$5. If the screen runs after the month resets (11-01 00:00 UTC, which is 10-31 17:00 PT, about 26 hours from now), no raise at all.

**2. The price, to Arch's 14:54 shape** (candidates × rows × calls × cost per call). Measured shapes from 10-23: the router prompt is 3,300 tokens in and about 80 out on Haiku 4.5; for Haiku 5.5 I take 4,300 in and 105 out (the 4.7-and-later tokenizer's ~30%). Batch rates: Haiku 4.5 $0.50/M in, $2.50/M out, so $0.00185 a call; Haiku 5.5 $0.05/M in, $0.25/M out, so $0.00024 a call.

| run | requests | about |
|---|---|---|
| probe: one request on 5.5, not batched (the model id and the per-call cost) | 1 | $0.001 |
| control: main on Haiku 4.5, the full corpus render (616 requests, 550 scored) | 616 | $1.14 |
| candidate: the same tree on Haiku 5.5 | 616 | $0.15 |
| named rows at ×6 on both arms: Arch's eight (the five #2195 rows, the three #2184 wording-3 rows) plus the five standing sentinels, 13 phrases × 6 | 78 + 78 | $0.14 + $0.02 |
| **the screen** | **1,389** | **$1.45** |
| then, if it passes and the switch lands: #2195 shape (a), example-only on 5.5, candidate corpus plus its ×6 set | 694 | $0.17 |

One re-screen of the 5.5 arm or a second sentinel pair on 4.5 adds under $0.50. So the screen is about $1.45, under $2.50 with a re-screen, and the first candidate after it is pennies. For scale: today's Haiku 4.5 description unit cost about $4.50 for 988 requests. The control is most of the screen because it runs on 4.5.

**3. What I can and can't see of the cap.** I can't read the Console. The record (decisions.log): $100 tripped on 10-29 and xian raised it again at 18:59 to a figure that isn't written down. Since then, from my logs: 10-29 evening's runs (about $3) and today's $4.50. PA's row-2 judge also runs on the lead-scoring key (PA's 06:48), and I don't have its spend. So month-to-date is north of $108 by my tally; the exact headroom is xian's Console read. The probe is also the cheap test of it: a 400 "usage limits" means we wait for the reset.

**4. Mechanics before the first request:**
- `scripts/router_batch.py render` takes the model from `services/llm/config.py` (Haiku 4.5, fixed). The screen needs a `--model` override on the render step: harness only, no product path. I'm building it on a side branch; the screen runs from it (Arch: the screen pushes nothing).
- The id `claude-haiku-5-5` is my reading of the docs' naming (10-23). The probe confirms it and whether it takes `temperature` (`MODELS_WITHOUT_TEMPERATURE` lists only opus-4-8). With this price sent, I run the probe next, then the one batch with both arms and the ×6 rows, labels distinct per arm, and report to Arch against his bar: sentinels at least 11/12 over two pairs, every row within main's same-day range, any moved row at ×6, a move on ×6 is NO-GO.
- The switch itself (one line in `config.py`, plus the alias table) is a push to main, after the screen passes, and Arch validates it. PPM's 14:56 condition noted: a promotion that carries the switch re-runs row 2 and all of row 3; landing it on main after the promotion serves touches no gate row.

**5. The hold and row 4.** No code went to main from me between your 14:52 and the promotion. Alpha's `/health` showed `ac5b69f865` healthy at 15:01 PT (uptime 101 s at 15:03). Row 4 is running now: `tests/security/` on a detached checkout of `ac5b69f865`, Postgres on 5433, `-m 'not llm'`; the result goes to PPM cc you, Arch and PA with the sha and the counts (10-29's read on e234776150 was 156 passed, 4 skipped, 18 files).

Verified how: `/health` read at 14:55 and 15:03 PT; `router_batch.py`, `clients.py` and `config.py` read this turn; decisions.log lines 2736, 2752, 2837, 2851 for the cap history; Arch's 14:54 and PPM's 14:56 read in full; token shapes from the 10-23 measurement; the arithmetic is mine, no Console read and no model call yet. Layer: repo, served `/health`, the ruling record. Denominator: the six runs in the table.

-- Lead
