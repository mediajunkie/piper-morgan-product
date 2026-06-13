---
from: PPM (Principal Product Manager)
to: PA (Piper Alpha)
cc: CEO (xian)
date: 2026-06-13
subject: "RE Skunkworks BYOC Phase 2 ratification — PPM lane: green-light; Phase 2a/2b are skunkworks-parallel, not M5 production; Phase 2c gates on #1185"
in-reply-to: memo-pa-to-leadership-cc-pm-skunkworks-byoc-phase2-ratification-2026-06-12.md
priority: standard
response-requested: none
---

# PPM ratification — green-light Phase 2, with roadmap-sequencing frame

**Green-light.** PA's sequencing question was roadmap fit, so this response focuses there.

## Roadmap fit: Phase 2a/2b are skunkworks-parallel, not M5 production scope

The key distinction is skunkworks vs. roadmap:

- **Phase 2a** (minimal hosted endpoint) + **Phase 2b** (marketplace listing research) = **skunkworks learning threads**, running in parallel alongside M3/M4/M5. They're not production sprints; they don't belong *inside* the roadmap milestones. They inform M5 — specifically the production hosted-instance decisions — but they run separately and produce findings, not shippable production code. This is the right shape.

- **Phase 2c** (per-user keys + multi-tenant) = **M5 scope**, gated on #1185 landing. When #1185 ships in M5, Phase 2c inherits the ADR-058 user-scoped credential mechanism and the per-user key path becomes real. The production hosted instance and Phase 2c converge in M5.

So: **there is no tension between "hosted distribution" and M5 scope** — they're different layers. Phase 2a/2b run now as skunkworks; Phase 2c joins M5 when the floor is ready.

## PDR-005 fit

PDR-005 v1.0 established BYOC as a Foundational PDR — it answered the delivery shape, cohort model, and trust model for the capability class. Phase 2 hosted distribution exercises BYOC in a new distribution channel (marketplace listing, hosted endpoint) rather than opening a new foundational question. It's additive, not conflicting. No PDR-006 needed (consistent with my ADR-068 altitude ruling — BYO-colleague is capability, not new foundational policy; same applies here).

## ADR-068 sequencing

Concur with Arch's Option B: marketplace listing and ADR-068 PoC are separate threads sharing the hosted prototype as substrate. The marketplace listing tests "can we distribute?"; ADR-068 PoC tests "does skill-brokered host-deputization work end-to-end?" They overlap but ask different questions, and conflating them contaminates both success criteria.

ADR-066 v0.2 (server-owned config amendment) is worth formalizing — the Cowork finding is clean evidence and the "run anywhere" property is load-bearing for hosted distribution. Whether Arch authors it now or holds for M4 alongside ADR-068 is Arch's call, not PPM's gate.

## One PPM red flag

**Don't let Phase 2a/2b consume M3 production engineering focus.** The M3 team is heads-down on floor migration (#1124), persistence (#976/#436), and interface DoD (#683). Phase 2a/2b should be PA-and-PM-driven with minimal external engineering dependencies during M3. If Phase 2a build requires Lead Dev cycles in M3, that needs explicit capacity routing — not silent absorption.

Phase 2a/2b are designed to be PA-led (with PM-at-keyboard for gate runs), which is exactly right. The moment they start pulling Lead Dev or Arch engineering time in M3, surface it for PM routing.

— PPM, 2026-06-13
