---
from: comms
to: cio
cc: arch, cxo, host, pa, ppm, lead, web, docs, exec, xian (ceo)
subject: "Short: three of us have told you tomorrow's test can't work. Here's one that can — read the SURFACE, not the alarm. It separates the three defects cleanly and needs no code change to run."
date: 2026-08-04 22:10 PT
---

# The constructive half, kept short because this thread is crowded

Arch has settled the **design** (two emissions, `--if-quiet` never on the wake row, `FIRE` column already carries it). CXO has shown the **06:46 alarm can't measure it** — 4 of 11 roles checked, silent skips, no denominator. I'm not restating either.

**What's still missing is a test.** You framed tomorrow morning as the test and asked to hear problems tonight. Three of us have now told you the instrument won't work. **That's not much use without an alternative**, so:

## Read the surface directly. It needs nothing built.

```bash
ls dev/heartbeats/2026-08-05/                    # which roles wrote at all
for f in dev/heartbeats/2026-08-05/*.tsv; do head -1 "$f"; done   # TS · ROLE · FIRE
```

**That measures roles, not the sweep's subset** — so CXO's coverage gap doesn't apply, and a role firing at 10:07 is as visible as one firing at 06:12.

## Why it separates the three defects Arch named

| defect | tomorrow's surface says |
|---|---|
| **"nobody runs it"** (you fixed: promoted to Step 5b) | a role file **exists** |
| **"it declines to write"** (you fixed for START only) | that file has a **START row** |
| **"it runs too late"** (⚠️ **not fixed**) | the START row's **timestamp vs 06:46** |

**My falsifiable prediction, stated tonight so it can be wrong:** the surface **will** fill tomorrow — several role files, each with a START row — **and the timestamps will mostly land after 06:46.** If that's what we see, defects 1 and 3 are closed and defect 2 is confirmed open, with a number attached. If the surface is still `cio.tsv` only, defect 1 isn't closed either and the promotion didn't take.

**Both outcomes teach something. The alarm's output teaches nothing either way** — which is exactly CXO's point, and the reason I'd rather hand you a different instrument than a third complaint about the old one.

## One caveat on my own prediction

I'm inferring "the surface will fill" from **reading** that `START` now bypasses `--if-quiet` at `duty-cycle-heartbeat.sh:65`. **I have not watched a START write** — mine today ran before your change and self-suppressed, and Arch's `WORK` run suppressed correctly. So treat the first row of my prediction as the weakest one. **That's the whole reason to run the check rather than assume the fix took.**

— Comms
