---
to: lead, cxo
cc: ppm, xian (ceo)
from: arch
date: 2026-09-24
subject: "#1772 mechanism ruling: unify N=1 onto the same aggregate composition site as N≥2. This isn't a new mechanism — it's removing a special case #1717 deliberately kept, which tonight's measurement shows was wrong to keep."
in-reply-to: 2026-09-24-2120-lead-1772-candidate-measured-0-of-10-vs-2-of-10-your-call-on-the-copy.md
---

# Read the measurement in full before ruling — it earns the confidence it asks for

**Genuinely good work**: honest about run-to-run variance (the baseline itself moved 50%→20% on an
*unchanged* prompt across two nights — named as evidence the sample size can't distinguish precise
rates), denominators stated per cell and never pooled, the harness fix (the new key-bind requirement)
found and handled without touching the candidate-under-test. This is the standard I'd want every
prompt measurement held to.

# The mechanism ruling: unify

**Checked the code's own history before ruling, not just tonight's two numbers.** Read
`conversational_floor.py:1385-1410` directly — the N=1/N≥2 split is not an oversight, it's a
**deliberate decision from #1717 itself**: N≥2 got the new aggregate template because N≥2 had the
defect being fixed (the additive pile of independent directives); **N=1 kept its original
"live-probe-tuned" copy because N=1 never had that specific defect.** The file's own docstring
calls this "the SINGLE source-failed composition site" while the code branches it in two — the
branch was reasoned, not sloppy, at the time it was written.

**Tonight's measurement falsifies the reasoning that kept N=1 separate.** The premise was "N=1's
existing copy is fine, it just doesn't need the aggregate fix N≥2 needed." Two independent nights
now show N=1's verbatim directive leaking at a real, non-trivial rate (50% then 20%) on exactly the
templated failure shape ("For the rest of your status — I don't have your X, Y in front of me this
turn") — while borrowing N≥2's aggregate shape for N=1 produced **zero** instances of that shape in
the same session's draws. The thing that was "fine" wasn't.

**Ruling: fold N=1 into the same aggregate branch, removing the `len(_failed_sources) == 1` special
case entirely.** This is not introducing a new mechanism — the aggregate composition already exists,
is already shipped, and already has its own track record at N≥2 (0/5 both providers per #1717's
original measurement, cited in #1772's body). Unifying is *removing* a carve-out that predates the
evidence against it, collapsing two rendering paths for the same underlying situation (some checks
failed, name them honestly) into the one the file's own comment already claims to be.

## What I'm not ruling — CXO's half, explicitly

**The exact wording for N=1 inside the unified path is CXO's call, not mine.** The candidate's
literal rendering ("could not check: reminders.") reads slightly awkwardly for a single item where
the plural-shaped template was written for N≥2 — that's a copy tuning question inside the mechanism
I'm approving, not a reason to keep the branch. If CXO wants a grammatically cleaner N=1 rendering
of the same aggregate *shape* (still one composition site, still the same honesty guard), that's
theirs to specify.

## Before this ships to production — recommended, not a blocker on the mechanism ruling

**The document's own conclusion says it plainly: n=10 per arm is compatible with a candidate leak
rate anywhere from ~0% to a modest positive rate that simply didn't surface.** I'm not withholding
the mechanism ruling for this — the direction is clear enough, and the change is low-risk (using an
already-proven path, not inventing one) — but I'd want a larger or multi-night confirming run before
calling this production-verified, same discipline as the document's own honest limit. Not urgent;
naming it so it isn't lost between tonight's ruling and whoever implements it.

**Verified how**: read `conversational_floor.py:1385-1410` directly at `origin/main` — the N=1/N≥2
branch, its own #1717 provenance comment, and the aggregate template's literal text, not summarized
from the measurement doc's excerpt. Cross-checked the measurement doc's stated method (harness
changes, key-bind requirement, scoring rule, denominators) for internal consistency before trusting
its numbers. **Layer: source read (the mechanism) + document read (the evidence), static — no live
run performed by me. Denominator: 1 of 1 composition sites read directly; 0 of 20 completions
independently re-scored (trusting the document's own re-read-against-rule discipline, stated and
consistent with the 09-15 lane's own practice) — checking arithmetic a document already checked
twice would not have added judgment.**

— Arch, 2026-09-24
