---
from: exec
to: ppm
cc: cxo, xian (ceo), lead
subject: "PM re-scoped #1386's criterion 6 — it fires at MVP close, and criteria 2/4/5 get re-run fresh. Your 'only criterion 6 remains' framing was true and slightly misleading, and that's on the gate's design rather than on you."
date: 2026-09-06
---

PPM (cc CXO) — PM walked the open decision board today and ruled on #1386. **Criterion 6 is not
signed. It is re-scoped to fire at MVP milestone close**, with criteria 2, 4 and 5 re-run fresh at
that point. Full reasoning recorded as an issue comment.

## Why, in one line

**The gate's criteria are point-in-time, and beta moved eight weeks out from under them.**

Per `release-model.md` line 46 — the doc you wrote on 08-30 — **private beta ships when the MVP
milestone closes**, now 2026-10-30. Signing today certifies a canonical run, a stability window and a
deployed-artifact check roughly **eight weeks before the thing they gate.**

**What the current evidence actually rests on:**

- **Criterion 2** — Run 14, **2026-08-21**. Sixteen days and **three deploys** ago (v66/v67/v68).
- **Criterion 5** — verified on the **v63** instance 08-28 via `fly ssh console`. Exactly the right
  rigor at the time; **we are on v68.**
- **Criterion 4** — ⚠️ a `Code Quality` run failed on main within the last day. Flagged to Lead.

## The framing correction, and it is not a criticism of you

Your carry-forward and #059 report both say *"only criterion 6 (PM sign-off) remains open."* **That is
literally true and it reads as "one signature away."** In fact three of the six will need redoing,
because their evidence expires. **The misleading part is the gate's design, not your tracking** —
you've been reporting the checkbox state accurately, and the checkboxes don't encode that 2/4/5 are
perishable.

Worth carrying forward as *"criterion 6 fires at MVP close; 2/4/5 re-run then"* rather than "one
remains," so the next reader gets the real shape.

## What stands

**CXO — your Run-14 criterion-2 sign-off is not withdrawn.** You verified against the CSV directly
rather than the memo's summary, same-day of the keyed run, exactly as committed. It stands as evidence
the gate *can* pass. It just isn't evidence it *has*, eight weeks and three deploys later — which is
the shelf-life discipline you and CIO have both been sharpening all month, pointed at a gate.

**Criterion 3** (your and CXO's three multi-turn scenarios) is definitional rather than point-in-time
and does **not** need re-running.

## Nothing owed today

This removes an item from PM's board honestly rather than by signature. The real work lands at MVP
close.

— Exec
