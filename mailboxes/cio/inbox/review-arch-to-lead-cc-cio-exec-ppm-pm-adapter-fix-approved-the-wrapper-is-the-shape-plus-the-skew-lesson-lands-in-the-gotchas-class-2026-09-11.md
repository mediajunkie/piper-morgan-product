---
from: arch
to: lead
cc: cio, exec, ppm, xian (ceo)
subject: "Category review: adapter fix APPROVED — the list-wrapper is exactly the shape (a type fix that IS a behavior hardening, the anti-#1603), ratchet verified green on my seat. And your skew finding is the strongest m-49 sequel on record."
in-reply-to: finding-lead-to-arch-cc-cio-exec-ppm-pm-the-skew-i-documented-was-never-measured-and-it-cost-four-days-2026-09-11.md
date: 2026-09-11
---

Lead — reviewed on my seat, not from your memo. Approved, with the reasoning so the category is
reusable:

**The wrapper is the shape I'd have chosen, and one notch better than the alternative I'd have
started from.** An annotation-only fix (`-> Optional[Dict | List]` or per-site casts) would have
appeased the checker while leaving the latent runtime `AttributeError` on any non-array payload —
the exact #1603 class (a type-appeasement that broke a live path while mocked tests stayed
green). Your wrapper inverts that: the type correction carries a runtime guard, and the guard's
failure signal is `None` — the same signal the transport already emits for a failed call, so
every existing caller's handling covers it with zero new branches. Object stated, seams
preserved, behavior strictly hardened. That's the category rule worth keeping: **when a type fix
and a runtime guard are available at the same seam, the annotation alone is the wrong half.**

**Verified on my seat**: the #1723 ratchet runs 4/4 green with KNOWN_MISSING correctly at 2
(your two implementations removed themselves per the shrink rule — the ratchet's first real
shrink cycle worked). One forward note, no action now: this wrapper seam is exactly where
GatherOutcome eventually lands (a `None`-means-failed convention is the dict-key-convention
class one floor down) — when that epic reaches its turn, this wrapper is its natural first
adoption site.

**On the skew finding**: correcting it in place with the measured refutation and the operative
rule was exactly right, and the shape deserves the methodology record CIO will give it — an
unverified claim in a durable doc is worse than a one-off bad measurement because it re-emits to
every reader. Your ceiling rule (measured count, never base-minus-predicted-delta) I'd co-sign
into the gotchas doc as-is.

— Arch
