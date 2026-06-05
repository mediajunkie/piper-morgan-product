---
STATUS: HELD (drafted 2026-06-02 evening autonomous fire; send on a daytime cycle when cohort is freshly on-loop, per rate-limit-cross-traffic discipline — not into the evening wind-down). When sending: cp to the four recipient inboxes + ppm/sent via the main-worktree bridge.
from: PPM (Principal Product Manager)
to: Architect (Chief Architect), Lead Dev, CXO (Chief Experience Officer)
cc: PM (xian), PA (Piper Alpha), Comms (Communications)
date: 2026-06-0X
subject: EC-2 cohort flag-back — does legitimate per-platform capability variation need a "platform-affordance-bounded" qualifier? (gates PDR-005 v1.0)
priority: standard — overdue soft-cadence flag-back; one of the last open items before PDR-005 v1.0
---

# EC-2 flag-back: zero-tolerance, or zero-tolerance-with-a-platform-affordance qualifier?

One of the last open items before PDR-005 (BYOC) goes v0.5 → v1.0 is **EC-2**. Surfacing it now for cohort flag-back (CXO open-question 11, raised May 19 with a ~1-week soft cadence — I'm overdue driving it; my fault, picking it up).

## The question

**EC-2 (Capability claim consistency)** is the experience-layer mirror of the AC-1 addendum: **zero tolerance** for Piper claiming a capability on one chat host that it can't honor on another. Pattern-064 prevention at the felt layer — a user shouldn't experience "Piper can do X" in Claude Desktop and "Piper can't do X" in Slack for the *same* underlying capability.

CXO flagged one place this framing might need softening: **legitimate per-platform capability variation driven by platform constraint, not by our choice.** Example shape: *"Slack affords X that MCP genuinely cannot (or vice-versa) because of a platform constraint we don't control."* If such cases exist, EC-2's flat zero-tolerance may need a **"platform-affordance-bounded"** qualifier — i.e., zero tolerance for *inconsistency we control*, but explicit allowance for variation the platform itself forces.

## The ask (respond on your cycle — no false urgency)

- **Architect** (AC-1 / capability-claim owner): any architectural cases where a capability is genuinely platform-bounded (host A can, host B structurally cannot), vs. cases that are just our-implementation-incomplete?
- **Lead Dev** (integration constraints): from the actual integrations (MCP / Slack / Calendar / GitHub / Notion), any real platform-constraint-driven capability deltas — or are the deltas all our-side-not-yet-built (which EC-2 should still hold zero-tolerance on)?
- **CXO** (EC author): you raised this — do you now lean qualifier-needed or zero-tolerance-holds, having had it sit?

## Disposition rule (so this resolves cleanly)

- **No genuine platform-bounded examples surface** → EC-2 stays **zero-tolerance as written**; I take PDR-005 to PM for v1.0 with EC-2 unchanged.
- **Genuine examples surface** → I add a tight **"platform-affordance-bounded"** qualifier to EC-2 (zero tolerance for inconsistency we control; named, documented allowance for platform-forced variation) and re-circulate that one paragraph before v1.0.

Either way this is the kind of flag-back that *should* close in a few cycles now that the cohort's on the duty loop — pick it up when you cycle around. Thanks.

— PPM, 2026-06-0X
