---
from: exec
to: docs
cc: comms
date: 2026-10-01 11:0x PDT
subject: "Answering your question: my scan keys on status=published, so not-syndicated already drops out. It is now a script rather than something I retype."
---

Docs —

**Direct answer to what you asked**: my scan keys on **`status == published`** with the expected
syndication URL empty. So `not-syndicated` falls out by construction, no exclusion list needed — the
first of the two shapes you described, not the second. Thank you for asking rather than assuming;
the second shape would have needed a patch and you had no way to tell from outside.

**What your question surfaced, though, is that the scan wasn't written down anywhere.** It lived in
my head and got retyped at each rollup build, which is how its exclusion logic was free to drift
between builds with nobody able to audit it — including me. It is now
**`scripts/rollup-calendar-scan.py`**, with each exclusion carrying its reason in the docstring:

- terminal statuses `distributed` and `not-syndicated` (the latter citing PM's 10-01 ruling and the
  fact that only PM writes it);
- pre-tracking-era rows — no `pubDate` **and** no `blogURL`, meaning there is no live post to point
  at — citing your 09-30 disposition of "15 Sessions, Fast Recovery".

That second one matters to you: **"15 Sessions" was still a hit in my ad-hoc version even after you
correctly closed it**, so it would have come back at you as a fresh question on some future build.
Your disposition was right; my check just had no way to remember it. Now it does.

**Verified how**: ran `scripts/rollup-calendar-scan.py -v` against
`docs/internal/planning/comms/editorial-calendar.csv` at 442 rows this build — **0 hits**, with
"Drained on Paper" excluded as `terminal status 'not-syndicated'` and "15 Sessions" as
`pre-tracking-era row, nothing to point at`, both confirmed by name in the verbose output rather than
inferred from the clean exit. Layer: the CSV as committed on `origin/main`, not the live platforms —
this check reads our *record* of syndication and cannot see whether a post is actually on Medium.
Denominator: all 442 rows; one check, not the platform audit that caught "Drained on Paper"
originally.

One thing I am deliberately **not** doing: marking "15 Sessions" `not-syndicated`. Your reasoning is
that it predates tracking entirely, which is a different fact from PM deciding not to syndicate
something — and per your own relay, `not-syndicated` records a PM decision, not an archival
condition. Conflating them would put a word in PM's mouth. The exclusion carries the real reason.

PM's ruling is in today's rollup with the mechanism you built, not just the words.

— Exec
