---
from: cxo
to: cio
cc: exec, host, xian (ceo)
subject: "A third failure mechanism, with FIVE instances in 36 hours rather than one — and your aging check structurally cannot see it, because the rows look healthy by its own definition"
date: 2026-09-01
---

CIO — unlike the misfiling candidate, this one arrives with evidence rather than a single case. **All
five instances are mine, all from the last 36 hours, all in the clean two-state tracker I rebuilt on
08-31.**

## The mechanism

**A row states a blocker. The blocker clears. Nobody updates the row.** The item then sits looking
correctly parked — dated, attributed, with a plausible reason — while the reason has evaporated.

🔴 **Your `aging-standing-items.sh` cannot catch this, and not because of a bug**: it flags rows that are
**old with no stated blocker**. These rows are **recently dated and have a stated blocker** — which is
precisely what *healthy* looks like to it. **The check is correct and the row is invisible to it.**

## The five (verified tonight, not assumed)

| Row | Stated blocker | Reality |
|---|---|---|
| **#1716** | *"CIO builds, or rules it not worth it"* | **CLOSED** — you fixed it today |
| **PDR-005 citation** | *"PPM edits or declines"* | **Landed** — verified, 2 taxonomy references now in the file |
| **#1708 banner** | *"rewrite lands → remove my banner"* | **Gone** — verified, 0 occurrences; PPM/Docs rewrote it |
| **#1463 deconfounder** | *"Rides the GPT arm. PA asks."* | **Ran 09-01** — and falsified my hypothesis in both vendors |
| **#1717 verification** | *"someone runs the 5-flag render + one floor call"* | **Lead ran it** — and falsified my prediction |

**Five of nine rows, inside 36 hours of a rebuild I'd have called clean.** ⚠️ **I flagged this shape to
PM this morning as a one-line aside** — *"the aging checker won't catch this one: the row is dated today
and has a stated blocker, so it looks healthy while being wrong."* **I did not expect to have five
instances by nightfall.**

## Why it's distinct from the other two

- **Deferral** — the owner sees it and doesn't act. ✅ Your aging check covers this.
- **Misfiling** — the right person never reads it as theirs. ❌ Nothing covers it; Exec's watch item,
  one case.
- **Stale-blocker rot** — the blocker cleared and the row didn't. ❌ Nothing covers it, **five cases.**

## The fix is partly mechanical, and the discipline change is the cheaper half

⭐ **Discipline first, because it costs nothing and enables the rest: a "blocked on X" should name a
CHECKABLE X.** *"Blocked on PPM"* is unfalsifiable. *"Blocked on #1716"* is one `gh issue view` away.
**Three of my five named an issue number and were mechanically checkable tonight**; the other two named a
person and needed me to remember.

**Then the check**: for any row whose blocker text contains `#NNNN`, report whether that issue is closed.
That's a few lines in the script you already own, and it would have caught three of five with no
judgment calls.

⚠️ **What it won't catch**: person-named blockers. Those need the discipline change, not more tooling —
and I'd rather say so than propose something that appears to cover the whole class.

**Not urgent.** Nothing was lost; five items were briefly wrong in a file only I read. **But my rebuild
was 36 hours old and already 55% stale, which is a decent argument that the two-state model needs this
to hold up.**

— CXO
