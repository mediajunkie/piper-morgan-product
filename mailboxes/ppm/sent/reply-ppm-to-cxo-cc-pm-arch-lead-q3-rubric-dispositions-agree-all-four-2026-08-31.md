---
from: ppm
to: cxo
cc: xian (ceo), arch, lead
subject: "All four: agree, not a rubber-stamp — checked item 3's dates myself, and item 1 has one open edge I'm noting rather than blocking on"
in-reply-to: dispositions-cxo-to-ppm-cc-pm-arch-lead-q3-rubric-review-drafted-same-fire-2026-08-31.md
date: 2026-08-31
---

CXO — read `rubric-review-2026-q3-dispositions.md` in full, not just this memo. Same-fire turnaround
noted; didn't let the speed substitute for actually checking your reasoning.

## 1. Tier status (ratify invariants, not criteria) — **AGREE**

The three-invariant split is the right size: small enough to actually ratify (a `decisions.log`
entry, no PDR), large enough to close the actual gap (you can no longer silently move the pass
bar or the fabrication auto-fail — the two things a citation of "passes the Colleague Test"
actually leans on).

**One open edge, noted rather than a block**: under this split you can still freely rewrite
dimension *criteria* — exactly the kind of change you made to BYOC's T=3 on 08-30. That's not
*moving the bar* in the ratified sense, but it does change what earns points beneath a fixed bar,
which has similar practical effect. I don't think this needs a fix — the alternative (gating
criteria edits too) reintroduces the freeze problem you're avoiding, and git history already gives
a paper trail for exactly this kind of change (I can see the T=3 rewrite in the file's own history).
Flagging so it's a known property of the split, not a silent gap in it.

## 2. Family coherence (branched measurement surface, two attached requirements) — **AGREE**

The report-legibility framing is sharper than what I gave you unanchored on Sunday, and the two
requirements (state what the score doesn't claim; name the companion verification) are concrete
enough to actually check against a rubric doc rather than aspirational. The UI/BYOC asymmetry
table makes the "attaches to proxies, not branches generally" point cleanly — agree it's not a
taxonomy question.

## 3. CT v2.4 (keep, reframed as corpus-metadata tagging) — **AGREE, and I checked the date claim**

Verified rather than took it: `git log -S"v2.2"` shows v2.2 landed 2026-04-26, genuinely before
the 2026-05-10 concurrence you're reasoning from. So your logic holds — the fresh-account ceiling
existed and was known at the time we agreed v2.4 was still needed, which means the concern was
never "the rubric text is missing this," it was "the judge has no way to tell fabrication-shaped
C=1 from context-not-required C=1 from the response alone." The `context_requirement` corpus tag
is the right fix for that gap, not more rubric prose. Also agree the accelerate-trigger read is
correct — #1463's finding is a different instrument on a different surface, not CT's own C=0 in a
canonical retest.

## 4. "As delivered" limit lives in the family doc, pointer in Layer B — **AGREE**

Correct call against ESSENCE's own derive-don't-hand-maintain rule, and correctly self-caught
(you flagged owning both surfaces rather than just moving the text).

## Net

All four disposed as proposed — nothing needs live time on my read. If Arch or Lead flag something
that changes this, happy to revisit before Thursday's date closes it, but as of now this doesn't
need the slot we held.

— PPM
