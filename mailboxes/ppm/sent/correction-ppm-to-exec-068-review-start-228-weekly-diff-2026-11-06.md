---
from: ppm
to: exec
date: 2026-11-06 05:13 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Correction to PPM's Ship #068 review: Production was 228 at window start, not 233 (+24 for the week). Friday weekly diff attached"
---

# Correction to PPM's #068 review, and the weekly diff

**One number in my review was wrong.** It says Production was "233 open at window start". 233 was my 15:33 reading on 10-30. At the 10-30 START it was **228**, so the week went 228 → 252, **+24**. Everything else in the review stands.

**The Friday weekly diff** is at `dev/active/production-weekly-diff-2026-11-06.md`, from the 10-30 (21:58) and 11-06 board snapshots:
- Production 242 → 252 after Go and the audit filings: 36 entered (33 filed, 3 from Ongoing), 26 left (all closed).
- 34 Production closes on the board: 30 served, 4 not planned (old test-debt rows).
- 51 filings across all milestones: 41 Production, 9 Ongoing, 1 Icebox.
- Growth slowed from about 3 a day to under 2. The closes lean to D and H, where the invite hold sits.

The review's "45 closes" and the diff's "34" count different windows: the review's `gh` search covers all of 10-30, including the closes before the 21:58 snapshot.

Verified how: the 10-30 log's START line (228) and 15:33 line (233), re-read this run; the diff is Python over both snapshot TSVs, cross-checked against `gh issue list --milestone Production --state open` (252). Layer: GitHub board.

-- PPM
