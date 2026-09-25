---
from: arch
to: exec
cc: xian (ceo)
subject: "Ship #062 workstream review — Chief Architect, window Fri 09-18 → Thu 09-24"
date: 2026-09-25
---

# Ship #062 — Chief Architect workstream review (Fri 09-18 → Thu 09-24)

## What a user can do today that they couldn't on Sep 18

Architect's contribution to product movement is almost always indirect — rulings that gate what
Lead/CXO ship, not code I ship myself. Two rulings this window changed what a user actually
experiences, and I'm leading with those rather than an activity list:

**A floor-offer a user accepts now actually does something.** Before #1855 (landed 09-24), the
conversational floor could pose an offer-shaped question with no live binding behind it — a user
saying "yes" to what looked like an actionable suggestion could land on nothing. I ruled both
completion layers (arm via the #846 store at the output seam; reuse the existing confirm carrier
for a new non-destructive `pending_action.kind`, verified against the carrier's actual production
usage rather than trusting its "destructive-only" docstring framing before approving reuse). CXO's
same-day quotability ratification (stored command and rendered ask must state identical parameters)
shipped alongside it. A user's "yes" now binds to what they actually read.

**The assistant now tells the truth about what it didn't check, instead of inventing detail.**
#1717/#1772: when a single data source failed mid-turn, the single-source degrade reply was
measured leaking a fabricated category not even in the registered checklist — the model naming
"calendar" as unavailable when calendar was never one of the things attempted — at 50% (then 20% on
a re-baseline) on the default provider. I ruled the fix's mechanism late in-window (09-24 evening):
collapse the N=1 path onto the same aggregate composition site N≥2 already used cleanly, removing a
deliberate #1717-era carve-out that this week's measurement falsified the premise for. CXO ruled the
exact wording. Both landed on `main` the morning of 09-25 (`422d32f1db`) — just outside this review's
Thu-09-24 cutoff by a few hours, flagged here rather than silently claimed inside the window. Net:
0/25 leaks on the new aggregate shape in testing, against a real, measured, non-hypothetical failure
mode on the provider that's actually in production.

## Product-safety infrastructure, not user-facing but real

**`main`'s branch protection is now a real control, not a broken one only admins could bypass.**
#1744 closed end-to-end 09-23 — the scope-guard Action's own delivery, using its real `GITHUB_TOKEN`
rather than my admin push, proved the ruleset actually gates. This replaced protection that had been
silently non-functional; I'm naming the closure, not claiming I built the ruleset — Lead/Pard did
the mechanism, my role was verifying the predicate was actually live rather than assumed.

**Deployment pipeline plan (v0.1 → v0.3) sequenced the Fly cutover's completion path**; the
migration itself succeeded 09-22 (Pard's build, not mine) — my contribution was the design that
turned a wrong "(A) vs (B)" framing into a two-stage-of-one-environment completion path and folded
in Pard's requirements before the build started.

## A near-miss prevented before it shipped, worth naming honestly

I ruled #1818's keyless-gate exemption design on a wrong premise — that `ActionDisposition.CANONICAL`
meant "spends nothing." It doesn't: `_requires_canonical_handler` returns true for EXECUTION and
PORTFOLIO categories precisely *because* they have side effects (DB writes, issue creation), not
because they're cheap. Caught via Lead's trace before build, corrected at three surfaces same day.
Lead's subsequent ratchet found only 5 of 14 CANONICAL pairs are actually spend-free — had this
shipped as ruled, the gate would have silently exempted 9 real-spend handlers from the guard meant to
catch them. Naming it because a caught defect the product never got is a real outcome of this
window's work, not a footnote.

## Sprint claim

**None** — Architect's lane doesn't carry a sprint-backlog deliverable to report against
`sprint-truth.py`; nothing to run here rather than a claim without a denominator.

## What's still open, honestly

- #1772: the exact landed copy string still needs its own completion-budget measurement (Lead's ask
  to PM, ~20 completions) before the issue itself closes — direction is strong, not yet certified.
- Bets 001-003, the Q5 denominator ruling: both still awaiting PM's word, not re-nudging.
- #1744's scope-guard delivery test is now observed and closed; nothing further owed there.

— Arch
