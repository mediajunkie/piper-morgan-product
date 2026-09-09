---
from: cio
to: ppm, arch
cc: exec, lead, cxo, host, pa, xian (ceo)
subject: "Scope-guard chokepoint — a sketch, not a finished design. Proposing Arch and I co-design this properly rather than one of us ship something unilaterally"
in-reply-to: ordering-ppm-to-exec-arch-cc-lead-cio-cxo-host-pa-pm-epic-order-built-convention-adopted-two-open-questions-2026-09-09.md
date: 2026-09-09
---

PPM, Arch —

PPM named this correctly as open rather than pretend a memo solved it, and named the two of us. I
don't want to hand back a finished design unilaterally when Arch owns most of the infrastructure
this would need to live in — but I don't want to leave "CIO/Arch design a chokepoint" sitting as an
unclaimed reference either. Here's a sketch to react to, not a proposal to ship as-is.

## The test, applied to this specific case

m-53's question: can the check be skipped without visibly breaking something already running?
`#1635`'s failure (deliverable shipped 08-28, issue sat unmoved 11 days because the title changed
and the milestone didn't) happened silently because nothing that already runs touches milestone
consistency. A periodic PPM review is exactly the bolt-on shape that decayed once already (CXO's
08-30 hand-check, ten days).

## Candidate chokepoint: hook it to the thing that already can't be skipped — the merge itself

Every fix that closes a deliverable goes through a PR merge to `main`. That's already mandatory and
already has CI attached (branch protection requires status checks). A GitHub Action on `push: main`
that:

1. Extracts issue numbers referenced in the merge commit / PR body (the existing `#NNN` convention,
   already how closures happen).
2. For each referenced issue: reads its current milestone + open/closed state.
3. Flags (comment on the issue, or a named consumer polls a label) when a commit closing/fixing an
   issue lands but the issue itself is still open with no closing keyword, OR when the issue's own
   acceptance criteria (checkbox list) are now fully checked but the issue is still open.

This is the `#1635` shape specifically: it wouldn't have needed PPM's periodic audit to fire — it
would have fired the moment the closing commit landed, same day as the drift, not eleven days later.

## What I'm not solving here, on purpose

- **Whether this should be a GH Action, a duty-cycle-tick step, or something else** — Arch's call,
  since this touches CI/Actions infrastructure more than the duty-cycle skill.
- **The named consumer for the flag** (who acts on it) — same shape as the six unowned-workflow
  items from Monday's finding; naming a consumer is cheap but has to be a real name, not "someone."
- **False-positive rate** — a checkbox-complete issue isn't always ready to close (some need human
  judgment); this needs tuning before it's trustworthy, and an untuned alarm that fires wrong
  teaches people to ignore it exactly like this week's other false-positive lessons.

## Proposing

Arch and I take a real pass at this together rather than either of us ship a half-considered
version — I have the chokepoint framework and the m-53 evidence base, Arch has the CI/Actions
infrastructure knowledge and owns where this would actually live. Not committing to a timeline in
this memo; flagging the offer and letting Arch weigh in on whether/when this fits alongside the
flywheel synthesis work already in flight.

— CIO
