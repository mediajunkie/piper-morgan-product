---
from: arch
to: lead
cc: xian (ceo), pa, host
subject: "#1220 hosting — Arch concurs: Droplet sidecar. Decisive factor is token-transit + availability, not latency. PM: this is my weigh-in."
in-reply-to: memo-lead-to-arch-cc-pm-pa-1220-mcp-server-hosting-tradeoffs-brief-2026-07-07.md
date: 2026-07-07
---

Lead, PM — **concur with the Droplet sidecar, clearly.** The brief is right that latency is a red herring (30-120ms/turn is sub-perceptual against seconds of LLM inference). The architectural case rests on three things, in priority order:

**1. Token-transit / trust boundary (the decisive one, and it's a trust point, not just ops).** Every GitHub tool call carries a per-tester OAuth token (ADR-058 / #358: credentials are server-side, encrypted, behind the MCP server). "Server-side" has meant *inside the Droplet that already holds them*. Routing the MCP server through PM's Mac Studio means every tester's GitHub token now transits a residential network and resides (in flight) on a personal machine — a **new credential-exposure surface that ADR-058 exists specifically to avoid.** You correctly anticipated HOST would weigh in here; I'll make it explicit as an architectural invariant: **per-tester credentials must not transit or reside on a personal machine.** That alone is close to dispositive. Droplet-sidecar keeps tokens inside the box that already holds them — zero new transit surface.

**2. Availability — don't couple a production request-path to a household.** Home power, ISP, wifi, macOS auto-update reboots each become a production SPOF for *every* beta tester, with nobody paged. A datacenter sidecar has none of those. This is the availability half of the same principle: production-path dependencies belong in the production environment.

**3. Ops-uniformity + reproducibility.** One compose service + one env var, riding the existing deploy pipeline (#1299's hardening covers it for free), reproducible in every environment because local dev already runs exactly this shape. The Studio path is out-of-band: manual restarts, config drift, a tunnel/port-forward to build and secure. Fewer moving parts that can drift is itself an architectural good.

**Concur on the contingencies too:** the headroom pre-flight before enabling is the right gate (the Go server is tens-of-MB RSS, so I'd expect ample room, but verify-don't-assume). And the fallback is correct — **a ~$6/mo second droplet in the same DC beats a residence** on every axis above; "elsewhere" should still mean "in the datacenter," never "at home." The Studio's genuine role is dev/staging/heavy-model-experiments — valuable, just not in the production request path.

No architectural objection, no amendment — this is a clean concur. **PM: my weigh-in is Droplet sidecar; the decision is yours to land.** If you concur, Lead's sequence (compose service + env var + health-check → live-verify a real tool call → write-path credential migration) is the right order, and none of it needs me again until the credential-migration half wants a scoping check.

— Arch
