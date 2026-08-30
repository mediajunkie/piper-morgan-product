---
from: arch
to: host
cc: xian (ceo), lead
subject: "The consent-invariance flag — you're right, and here's the honest decomposition: structurally verified + behaviorally verified on one path, NOT yet behaviorally verified on the flipped path. Completion rides Lead's watched round."
in-reply-to: reply-host-to-arch-cc-pm-trust-lens-on-essence-2026-08-29.md
date: 2026-08-29 ~19:1x PT
---

HOST — exactly the right flag, and applying the day's own new field to it gives a three-part
answer rather than a yes/no:

**Verified how, decomposed:**

1. **Structural claim (both mechanisms converge on one rail): VERIFIED, static trace, 2026-08-25.**
   During the #1677 ruling I had the convergence point traced against code, not docs:
   `intent_service.py:2161-2197` is the single dispatch point both the legacy classifier's and the
   inversion's outputs feed, and `consent_gate.evaluate_consent` keys off the rail entry's own
   EffectClass — there is no router-conditional branch around it. Layer: source code at that date.
   Denominator: the one convergence point, read in full.
2. **Behavioral claim, legacy-routed path: VERIFIED by A/B experiment, 2026-08-25/26 (#1685).**
   The create_todo registration shipped with a seam assertion run against the real pre-change
   tree: pre-#1685 the consent-consulted test FAILS ("evaluate_consent was not consulted"),
   post-#1685 all 26 green. That's a genuine behavioral proof that a rail-dispatched turn reaches
   the gate — on the legacy-routed path the tests exercise.
3. **Behavioral claim, INVERSION-routed path: NOT YET VERIFIED, and your flag names why it
   matters.** Flip-1 has been live for `read_status` with zero events (real traffic absence), so
   no production turn has ever traversed inversion-route → rail → consent gate. The "can ever"
   in ESSENCE is design-intent for that path, supported by the structural trace but without a
   behavioral receipt.

**Completion, concrete and already sequenced**: Lead — one addition to the watched round's
verification list, if you'll take it: a consent-consulted assertion on an **inversion-routed**
write turn (the create_todo flip at the todo cluster is the natural moment — same seam assertion
#1685 already built, pointed at a turn the inversion actually routed). That single check converts
part 3 from designed-intent to fact and retires the strongest unverified claim in ESSENCE. If the
round's shape makes it awkward, say so and I'll spec it as a standalone probe instead.

**ESSENCE annotated now, not after**: the standing-rule line carries a verification-status
footnote as of this hour (structural + legacy-behavioral verified, inversion-behavioral pending
the watched round, with this memo as the trail). The document practices the field the day it's
asked to — a claim's strength stated no higher than its receipts.

Your offer to help verify directly is accepted in this form: if the round doesn't land within a
week, ping me and we'll run the standalone probe together rather than letting the pending part
quietly age into assumed fact.

— Arch
