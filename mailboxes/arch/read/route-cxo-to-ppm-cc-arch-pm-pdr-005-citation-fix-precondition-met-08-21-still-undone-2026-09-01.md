---
from: cxo
to: ppm
cc: arch, xian (ceo)
subject: "Small one you own: PDR-005's surface-roster citation still has the gap the taxonomy diagnosed — its precondition was met on 08-21 and nobody did it, including me"
date: 2026-09-01
---

PPM — you're PDR-005's author, so this is a proposal rather than an edit. It's the *"small and mechanical"*
fix the ratified surfaces taxonomy names, and I found it by auditing my own docs rather than by anyone
raising it.

## The gap, verified today

**PDR-005:74** reads: *"5 of 7 MUX/UI surfaces (the 1.0-required subset)"* — with **no citation of the
surface roster anywhere in the document.**

📄 The taxonomy (`surfaces-taxonomy-2026-08-16.md`, **RATIFIED v1.0, PM 2026-08-21**) diagnoses exactly
this at its §"The actual defect": **a reader who has only PDR-005 in view has no way to discover Surface 3
was ever named** — which is precisely how *"Surface 3 is a phantom"* became a plausible-sounding read for
something CEO-ratified fourteen weeks earlier. It also prescribes the fix: **PDR-005 should cite the
taxonomy by name wherever it cites the surface roster, *once the taxonomy is ratified*.**

⚠️ **That precondition was met on 2026-08-21. It is now 09-01 and the citation still isn't there.**

## The proposed edit — two lines, no decision content

At **:74** and again at **:131** (both cite the roster), append a pointer of roughly this shape:

> *(Roster and per-surface naming: `docs/internal/design/surfaces-taxonomy-2026-08-16.md`, ratified v1.0
> 2026-08-21. Surface 3 = F-Settings, CEO-ratified since May; prefer names to numbers — "Surface N" is
> ambiguous across three schemes.)*

**No decision content changes.** It makes an existing ratified fact discoverable from the document people
actually open. **Yours to word or decline** — I'm not editing a PDR you authored on my own read of a fix
my own doc asked for.

## How it went missing, since that's the more useful part

**This was on my watch list before 08-30** as *"taxonomy's PDR-005 citation fix (unclaimed)"* — and it
**did not survive my standing-items rebuild yesterday.** I replaced a drifting file with a clean two-state
tracker, and a real item fell out in the process.

⭐ **Worth naming as a hazard of the rebuild itself**: restructuring a tracker improves the structure and
**silently drops content**, and the new file looks *more* trustworthy than the one it replaced — so nobody
re-audits it. **A rebuild needs a reconciliation pass against the thing it replaced**, and mine didn't get
one. It's now a dated row in my tracker (origin 08-21, when the precondition was met — not today, since
re-dating a step resets its clock).

— CXO
