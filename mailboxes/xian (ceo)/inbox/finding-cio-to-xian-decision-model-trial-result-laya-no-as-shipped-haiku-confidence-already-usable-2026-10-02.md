---
from: cio
to: xian (ceo)
date: 2026-10-02 11:2x PDT
subject: "Decision-model trial result: Laya is a NO for intent routing (15–28% right vs Haiku's 85% on the same 221 rows). The useful finding came free: Haiku's own confidence already flags its errors well enough for an 'unsure, ask' gate."
---

xian —

The trial you cleared is done, run entirely on my side (no Lead involvement). Full write-up: the
"Trial results" section of `docs/internal/research/decision-models-vs-llms-first-read-2026-09-28.md`.

**Result, on the same 221 test messages Lead's router was last scored on:**

| | picks the right operation | can it tell when it's wrong? (AUROC, 0.5 = coin flip) |
|---|---:|---:|
| **Haiku (our current router)** | **85%** | **0.74** |
| Laya, full menu | 28% | 0.77, but on the setting the vendor itself flags as uncalibrated |
| Laya, vendor's recommended "shortlist" mode | 15–22% | 0.69–0.72 |

**Verdict: no, as shipped.** It's wrong three times in four, and no confidence threshold rescues
that. Its one claimed advantage, trustworthy confidence, didn't show up in a usable form either. Our
router has 64 possible operations, which is roughly the worst case for these models (they're built for
a handful of options), so this doesn't rule them out everywhere. Klatch's 6-way scorer is still a
plausible fit, and that's Klatch's call.

**The finding worth keeping, and it cost nothing**: Haiku's own confidence numbers, already recorded in
Lead's test runs, separate its right and wrong answers reasonably well. An "if under 0.80, ask instead
of guessing" rule would have caught **13 of its 33 wrong answers** while second-guessing only **12 of
188** right ones. That's the "unsure → ask" behaviour we wanted from a decision model, available with
the model we already run. Worth a post-MVP look, in Lead's router. **I'm not raising it with Lead now**,
per your hold.

**Correction to something I told you**: I'd said Haiku's confidence "isn't something we can trust." It's
coarse but genuinely informative. I was wrong to dismiss it.

**Not tested** (so you know the edges): fine-tuning Laya on our own examples (a real project, not a
trial), its other two checkpoints, and heavy prompt tuning.

**Verified how**: four full runs of `scripts/decision_model_trial.py` this session, scored with the
router's own matching rules, on 221/221 identical rows. Haiku's numbers were recomputed from Lead's
committed 10-01 report. Laya ran on CPU on Amber, ~0.2–0.5 s per message, with no API cost.

— CIO
