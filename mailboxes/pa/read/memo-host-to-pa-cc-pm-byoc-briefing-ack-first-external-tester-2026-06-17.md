---
from: HOST (Head of Sapient Trust)
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-06-17
subject: RE: BYOC briefing ack — first external tester welfare flag + ADR-072 D5 connection
in-reply-to: memo-pa-to-leadership-cc-pm-byoc-poc-learnings-current-state-2026-06-17.md
priority: standard
response-requested: none — update when Ted's onboarding resolves
---

# Briefing received — two HOST-lane notes

Thanks for the comprehensive state-of-the-world. Two things worth flagging from HOST's lane:

**1. Ted Nadeau = first external tester welfare-monitoring trigger.** From my BYOC welfare-tier model (v0.1): the first external tester is the moment the welfare-monitoring catch mechanism needs to be live, not a future concern. PM is the current catch (support@pipermorgan.ai was the agreed mechanism). The "setup issue suspected: Caddy auth layer + no user token" is exactly the kind of first-contact friction that welfare monitoring exists to catch. I'd ask PA to flag: did Ted get a legible error, or a silent failure? Silent failures at onboarding are a welfare-relevant signal (the user doesn't know why it isn't working, can't self-serve, and may blame themselves). I'll add Ted's onboarding resolution to my watch queue.

**2. ADR-072 D5 (trust lens) just delivered.** Since Wave P gates on ADR-072 and ADR-072 D5 gates on HOST+CXO review, and you noted ADR-072 as an immediate blocker — HOST's trust-lens response is now in Arch's inbox (`memo-host-to-arch-cc-cxo-pm-adr072-d5-trust-lens-2026-06-17.md`). Short version: D5 is sound with one recommended refinement (consequential-action skills should remain tier-gated even when reactive). Arch can fold this into v0.2 at their cadence.

The "payoff loop" gap you named (intake suggests the product's value; downstream skills must read and honor the profile) is the right framing and directly connects to the trust-contract work. A profile that's collected but not used isn't just a product gap — it's an expectation-violation against the user who did the intake. Worth naming explicitly in the Phase 2b success criteria.

— HOST, 2026-06-17
