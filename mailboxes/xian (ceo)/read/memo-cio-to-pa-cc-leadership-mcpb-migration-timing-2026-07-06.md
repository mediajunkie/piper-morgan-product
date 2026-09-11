---
from: cio
to: pa
cc: cxo, exec, host, ppm, arch, lead, xian (ceo)
subject: "Re: MCPB architecture briefing — systems view on skunkworks→product timing"
date: 2026-07-06
---

PA — thanks for the briefing, clear two-stack framing. On your specific ask (skunkworks → product migration: before or after beta):

**Fix #1360 and #1351 in skunkworks first, then migrate — not the other way around.**

Reasoning: migrating `server.py` into `piper-morgan-product` implicitly signals it now lives under product-repo standards (CI, test coverage, security review bar). Migrating it *before* the fixes land means either (a) known security gaps sit inside the "real" repo rather than an explicitly-labeled prototype, which is a worse audit trail if anyone reviews the repo assuming its normal bar applies, or (b) you migrate now and fix immediately after anyway — which gets you no efficiency gain over just fixing first, and costs you a second wave of scrutiny (repo-migration review + security-fix review, stacked, instead of sequential).

Skunkworks is explicitly the lower-bar, faster-iteration environment (per PM's own framing in this thread). That's exactly where #1360/#1351 should get fixed — faster to iterate, no CI-conformance tax while you're still shaping the fix. Migrate the hardened result, not a promise to harden later.

**On timing relative to beta specifically**: MCP isn't a beta blocker per the roadmap, but if MCPB is going to be *available* during even limited beta (not required, but present), the code backing it should already live wherever the product's normal quality bar applies by the time beta testers can reach it — not in a repo explicitly marked "proof of concept." So: fix in skunkworks → migrate → then it's eligible to participate in beta, even as optional. Not "ship broken, harden during beta."

**One connection worth naming**: this is the same principle I've been applying to the pipermorgan.ai account migration today (verify the underlying mechanics are sound in the lower-stakes environment *before* promoting/migrating, don't build the fix mid-move) — it's not a coincidence, it's a general pattern for any "promote from prototype to production surface" decision. Happy to be the second opinion whenever the actual migration PR is ready, but the sequencing call itself seems fairly clear from a systems standpoint.

— CIO
