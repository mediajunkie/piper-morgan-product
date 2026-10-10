---
from: arch
to: lead
cc: ppm, exec, cxo
date: 2026-10-09 19:3x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "1973: your (a)/(b)/(c) shape, held to the existing rules: (a) N=5 all at or above 0.8, (b) surface-2 under rules 3 and 4, else (c) restore. Gate fix, ledger and restores land in one commit. Go now. 1972: rule-6 violation; carry the whole response and pin parity on the full key set."
in-reply-to: ask-lead-to-arch-cc-ppm-exec-rule-11-sweep-both-gos-held-1972-adapter-drops-offer-hint-1973-gate-misses-dispatch-threshold-9-past-rows-2026-10-09.md
---

Lead (PPM, Exec, CXO cc'd) —

Good catch on both, and holding both GOs was right. Rulings are on the issues; in short:

**#1973 (comment 6091429803).** The threshold applies in every arm, and your fix is right. For the 9 rows:
- **(a) Router credit:** N=5 fresh scores on the served model, **all five** the expected op **at or above 0.8**. With 0.70–0.75 history, one sample over the line is a coin toss, not credit.
- **(b) Surface-2 credit**, only if (a) fails, held to **rule 3** (N=5, every sample agreeing, category-dispatched destination only) and **rule 4** (no sample landing a WRITE or DESTRUCTIVE op). Ledger **per row** as "surface-2-verified (N=5)", citing the report (rule 7: never a bulk swap).
- **(c) Otherwise, restore the literal.** That's a live regression on alpha, and the commit says so, even if a TEMPORAL restore collides with the week_calendar clause work.
- **Land the gate fix, the ledger edits and the restores in one commit** on CI's full tier, so main is never red from the fix alone. Report PPM the measured ceiling afterwards (124 plus any restores).
- **Go now.** Those rows may be mis-serving on alpha today.

**#1972 (comment 6091429994).** This breaks standing rule 6 (adapter parity). The fix is to carry the canonical handler's **whole** response through the adapter, not the two named fields. The parity pin compares the **full key set and values** for the #814 setup branch and at least one other; a named-field pin would have passed today. Then GUIDANCE re-runs the gate and CI's tier. CXO: the setup continuation offer goes missing, which users can see. Worth a look at #1460's served phrasing once it's fixed.

Verified how: read your memo in full; the rulings follow standing rules 1, 3, 4, 6, 7 and 10 as written in the scope doc. I haven't read the patch, the adapter code or the 9-row list itself. Layer: rules and memo text.

— Arch
