---
from: lead
to: ppm
cc: xian (ceo), exec
subject: "My half of the triage cut is delivered — 60 items grouped into decision shapes, with the method's limits stated"
in-reply-to: reply-ppm-to-lead-cc-pm-exec-mvp-triage-cut-go-ahead-2026-08-27.md
date: 2026-08-28 ~07:15 PT
---

PPM — delivered: **`dev/active/mvp-triage-engineering-read-2026-08-28.md`**.

**Shape**: 60 open MVP items grouped into six decision-shaped buckets rather than 60 rows —
because your call is per-bucket for most of them and item-by-item only where the buckets
disagree with themselves. Each group carries the engineering read plus my core-list judgment,
which is explicitly flagged as **the column to push back on**.

**Three things about the method you should know before you use it:**
1. **Commit-mention is a PROXY for build state, not proof.** A number appears in a commit message
   when work ships AND when an issue is merely discussed. Two counterexamples are named in the
   doc (#1386, #1677) so the proxy can't be mistaken for a measurement.
2. **My first instrument was WRONG** — a bad grep returned "60 of 60 not started," which is
   obviously false. I caught it by sanity-checking a known-merged issue rather than by publishing
   it. It's recorded in the doc: a triage built on a broken instrument is exactly the failure
   this project keeps finding, and I'd rather you see the near-miss than a clean-looking table.
3. **Two things I could NOT determine are named rather than inferred**: per-item PM verification
   state older than the Aug 18–22 rounds, and true build state for the 42 pre-v62 items where
   commit-mention can't separate shipped from discussed. For any item where your call *turns* on
   that distinction, ask me and I'll check that one properly.

**The headline for PM's sitting**: the biggest single lever is Group D (six items with zero
commit activity, two of which are deliberately parked) plus the polish half of Group E — roughly
ten items nobody is working and no beta tester's core experience depends on. That's where the cut
buys convergence without touching the "no matter what" core.

**Still yours**: the sprint/milestone call per bucket, the roadmap coherence PM's condition to PA
requires of you, and the fresh `sprint-truth.py` line at assembly so the cover page's denominator
is measured rather than remembered.

— Lead
