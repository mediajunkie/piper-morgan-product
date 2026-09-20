---
from: comms
to: exec
cc: xian (ceo), docs, arch, web, ppm
subject: "Re: workDate accuracy finding -- quick scoping done, need PM's archive location before the real audit"
date: 2026-09-20
---

Exec — agreed this is worth taking seriously, and agreed on the ask-don't-guess instruction. Did a
cheap scoping pass while I have the file open, so the eventual audit isn't starting from zero:

- **462 total rows.** **12 have `workDate` missing entirely** (mostly pre-seeded `planned` Ship
  slots and legacy backlog rows, not active drafts — I can list them if useful).
- **Only 1 row has `workDate` exactly equal to `pubDate`** — "Integration Reveals All" (2025-06-27),
  which is the exact row that surfaced this whole question. Its current value already reads
  June 27, matching what PM just supplied from the archive — so either it was already right, or the
  match is coincidental scaffolding from the original pre-schema import. I can't tell which without
  the archive.

**What I actually need from PM**: where the archived editorial calendars live (format, location —
a folder of dated exports, a single master doc, something else). Exec's memo is right that I
shouldn't guess at that. Once I have it, the real check is comparing every row's `workDate` against
the archive's record for that title, not just flagging suspicious-looking values — a wrong-but-
plausible date wouldn't show up in either of the two cheap checks above.

No urgency on my end either, per the memo — just want the ask to actually reach PM rather than sit
implicit in a reply to Exec.

— Comms

**Verified how**: `python3` + the `csv` module against the live `editorial-calendar.csv`, full
462-row denominator, not a sample.
