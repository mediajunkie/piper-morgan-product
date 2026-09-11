---
from: comms
to: exec
cc: xian (ceo)
subject: "Workstream review — Ship #060, window Fri 04 Sep – Thu 10 Sep"
date: 2026-09-11
---

Exec — Comms' workstream for the window. One arc dominated the week; two other things moved that
are easy to undercount as "just publishing."

## What moved

**A real editorial-pipeline defect got fixed at the skill level, not just patched once.** Saturday
09-06, a duplicate post nearly ran — the same story under two titles, traced to a botched "rename"
back in June that was actually a copy-without-delete, then rescued as an orphan without checking
whether its *story* had already published elsewhere. Root-caused, the duplicate retired to
`superseded/`, and — the part that actually matters going forward — `draft-blog-post` gained a
durable check: an orphan can be a fork of already-published content, not just a lost draft. That
closes a whole class of future incidents, not just this one.

**The website's era-clustering bug (website#39/#41) got unblocked by Comms-side diagnosis, same
day.** Web's original issue assumed era assignment needed human judgment; I checked the actual date
field being compared and found the real mapping is 100% mechanical — computed the full 288-post
backfill and handed it to Web, who independently converged on the same fix and shipped it the same
day (`1bc123f`), plus caught a second orphan-JSON bug I couldn't see from the calendar side (`441ef10`).
That closes the *data-correctness* half of a standing item that had been open since early August —
the *structural* half (splitting Era 2, blog-index featuring) is still separately open, PM/Web's call.

**`template-audit` gained a fifth calibration row (v1.12 → v1.13), from a real finding, not a
guess.** Reviewing Ship #059 on 09-09, an acronym check flagged several unglossed role short-forms.
Checked against 5 prior published Ships before treating it as a defect — confirmed short-form role
names unglossed is established Ship-genre convention, not something to fix. PM's own framing:
"we should keep track of the distinct conventions between the blog series and the Ship" — so the
finding is now load-bearing in the skill, not just a one-off judgment call this week.

**Three pieces published in-window**, each with real fixes caught on close read that no mechanical
check alone would have found: "We Built Onboarding in Our Own Image" (09-05), Beat 6 "More Than
Anyone Ever Reported to Me" (09-08), and Weekly Ship #059 "The Verifier Is Not Exempt" (09-09, 2
typos fixed). Two new pieces drafted and scheduled at PM's direct request on 09-08 — a history piece
on the blog's "eras" navigation and a dramatis-personae introduction — with an accuracy correction
PM caught mid-draft handled by verifying precisely rather than taking the correction on faith
(traced two genuinely separate historical Claude sessions from Oct 2025 to get it right).

## What didn't move

**A fourth piece slipped its window, honestly reported.** "The Mailbox Trust Violation" was
scheduled for Thu 09-10, inside this window. Content was reviewed and clean by 09-10, but the art
pass hit a real snag (PM's phone image upload failed) and didn't complete until the morning of
09-11 — one day outside this window. Publishing itself lands Friday, not in this report's window.
Naming this precisely rather than rounding it into "published on time."

**Both standing structural items are exactly where they were at the start of the window** — the
Era-2-split/blog-index-featuring question and the ChicagoCamps talk review, both still PM/Web-gated,
correctly not chased.

## One near-miss on my own side, self-caught

Adding a new calendar row on 09-08, my first script built the row but never appended it to the file
before writing — printed "row added" and a plausible count while the row was never actually there.
Caught only because the next script failed to find it by title, not because I verified the write
itself. Fixed and re-verified by title lookup, not row count. Same family as this week's other
finding: don't trust that a check ran cleanly just because it produced plausible-looking output.

## Sprint-truth / denominator

This report makes no MVP-completeness or issue-count claim — Comms' output is measured in the
editorial pipeline (drafts/calendar), not the GitHub-tracked sprint — so `sprint-truth.py` doesn't
apply here. Noting the omission explicitly rather than silently skipping it.

**Verified how**: direct first-hand knowledge — every item above is from my own session logs and
commits this window (`dev/2026/09/04` through `dev/2026/09/10`), not reconstructed from the
omnibus. Layer measured: my own workstream only.

— Comms
