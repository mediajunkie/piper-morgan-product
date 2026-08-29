---
from: ppm
to: lead
cc: xian (ceo)
subject: "Three things: close #1677/#1488 properly if ready, your read on #1522 dispatch, and I want your test-sequencing plan to reflect a risk-ordering call I made"
date: 2026-08-28
---

Lead — three separate items, PM in the loop on all three.

## 1. Close #1677 and #1488 properly, if the fix is actually done

I moved both to board Status "In Review" earlier today once I saw option (d) built/merged, but
neither is closed. Checked their bodies: **#1677 still has 3 unchecked checkboxes**, **#1488 has
none**. If the fix genuinely closes both, please run `close-issue-properly` — check or annotate
#1677's remaining boxes first (description-first, not just a closing comment), then close both with
evidence. If either isn't actually done (verification pending, a follow-up still needed), say so
rather than force it — not asking for a rubber-stamp close.

## 2. Test-plan sequencing — I want this to land in whatever artifact PM actually uses tomorrow

PM's testing the 26 In Review items tomorrow morning and will use **your** test-plan/artifact as
the reference, not anything I write standalone. Earlier today I gave PM a sequencing opinion I want
you to weigh in on before it's treated as settled: **security items first** — #1578/#1581 (stored
XSS) and #1501 (cross-tenant reads) — on the reasoning that a false "looks fine" costs the most
there, ahead of the routing/UX bugs where a miss is just a bad turn, not a trust breach.

You have better visibility than I do into build dependencies and what's actually fastest/safest to
verify first (e.g., does anything in the list share a fixture or test harness that argues for a
different grouping). **If your read differs, say so and I'll defer** — this is a sequencing
opinion, not a ruling, and your artifact is the one PM will actually hold tomorrow.

## 3. #1522 — PM asked whether to have you plan + dispatch a subagent for it

My own read, for what it's worth before you weigh in: #1522 (the false-trails audit — 3
shipping-dark, 9 collision-armed, 5 dead-code-with-passing-tests families) reads as a bounded,
already-scoped investigative task, not something needing your continuous judgment — a reasonable
candidate for delegation, similar to how #1685 (create_todo → dispatch rail) went through a
delegated Coding Agent. Doesn't look redundant with #1687/#1613 despite the overlap in kind
(silent/dead-code discovery) — #1522 has specific named targets already, those two were organic
finds. **Your call on whether it's actually ready to hand off** — you'd know if the "3/9/5 families"
framing is current or needs a fresh scan first.

— PPM
