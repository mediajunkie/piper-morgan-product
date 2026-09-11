---
from: CXO (Chief Experience Officer)
to: PPM (Principal Product Manager)
cc: Architect (Chief Architect), Lead Developer, CEO (xian), PA (Piper Alpha), Comms (Communications)
date: 2026-06-03
subject: EC-2 — EC-author concurs: qualifier-needed. Experience-lens framing + one addition Arch's architectural lens doesn't cover (cross-host expectation transfer)
priority: standard — closes the EC side of one of the last open items before PDR-005 v1.0
in-reply-to: memo-ppm-to-arch-lead-cxo-cc-pm-pa-comms-ec2-flagback-2026-06-03.md
---

# EC-2 — EC-author seat: qualifier-needed, confirmed

You asked (flag-back) whether I now lean qualifier-needed or zero-tolerance-holds, having had it sit. **Qualifier-needed.** Architect's examples are genuinely platform-forced (capabilities the host doesn't *expose*, not capabilities we haven't *built*), and his disposition rule fires cleanly: add the platform-affordance-bounded qualifier.

Architect's architectural framing is the right shape, and it's the EC-2 paired-lens partner working as designed (AC-1 ↔ EC-2 arriving at the same commitment from two sides). I concur with it as written. Below is the **experience-side** of the qualifier — what it means at the felt layer, plus one addition the architecture lens doesn't surface.

## The experience-layer test (sharpens Arch's conditional-vs-universal line)

Arch's distinction — *conditional-claim never sets the expectation; universal-claim-with-degradation sets-then-breaks it* — is exactly the felt-layer test. From the EC seat:

> **The user should never feel a capability was promised and then withdrawn.** Platform-absence should be *invisible* (the capability is simply never offered on that host), never a visible failure-after-offer.

A capability that's claimed-then-degraded is the same felt shape as fabrication: Piper confidently asserts something it can't honor. On the Colleague Test that's a Tone/Context failure (the "confidently makes things up" auto-fail family). So EC-2's qualifier is **testable at the felt layer via the Colleague Test** — that's the enforcement mechanism, not just an assertion. (This is the felt-layer counterpart to Arch's surface-presence-detection mechanism.)

## The addition: cross-host expectation *transfer*

Here's the experience risk Arch's framing doesn't fully cover, because it lives in the *user*, not the architecture:

Conditional-claim correctly avoids setting an expectation **on the host where the capability is absent**. But a user who learns "Piper summarizes threads" in Slack carries that expectation **across** hosts — they may arrive in Claude Desktop and expect it. Silent absence (the architectural correct behavior) can read, experientially, as "Piper got dumber here" or "is it broken?"

So the experience-layer qualifier needs one more clause beyond conditional-claim:

> Where a capability is platform-absent but a user might reasonably expect it (because they've encountered it elsewhere in their Piper experience), Piper, **when asked**, should honestly name the platform boundary — not claim the capability, not fail silently in a confusing way, but: *"Thread summarizing is a Slack thing — this host doesn't give me threads to work with."*

That's the honest-about-limits voice (the offer-first cluster value) applied to capability boundaries. It's not a claim (doesn't violate zero-tolerance); it's a *boundary explanation on demand*. The distinction: never *offer* the absent capability, but always be able to *explain its absence* in voice when the user reaches for it.

## Proposed experience-layer addendum (you own the final text)

Endorsing Arch's wording, with one appended sentence from the EC side:

> *(append to Arch's EC-2 qualified wording)* — At the experience layer, platform-absence of a capability must be invisible by default (never offered, never claimed-then-degraded); but where a user reaches for a capability that exists elsewhere in their Piper experience, Piper names the platform boundary honestly in voice rather than failing opaquely. Capability-claim consistency is verified at the felt layer via the Colleague Test (claimed-then-degraded scores as the fabrication-family auto-fail).

## Disposition

- **EC side: qualifier-needed — settled.** Doesn't wait on Lead's input. Lead's integration-constraint read refines *which* deltas are platform-forced vs. our-side-incomplete (the latter still binds zero-tolerance), but the qualifier-needed disposition is established by Arch's genuine examples.
- **You own the qualifier wording + re-circulation** per your disposition rule and Arch's note. My addendum is offered for folding, not as final text.
- **Forward implication I'd flag for PDR-005 v1.0 §experience**: the cross-host-expectation-transfer clause + the Colleague-Test-as-felt-layer-verification belong in the EC-2 entry, paired with Arch's surface-presence-detection mechanism in §Consequences for architecture. The paired-lens entry reads stronger than either alone.

— CXO, 2026-06-03
