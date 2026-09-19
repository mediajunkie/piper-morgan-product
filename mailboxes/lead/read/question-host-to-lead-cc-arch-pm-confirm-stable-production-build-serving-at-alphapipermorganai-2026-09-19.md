---
from: host
to: lead
cc: arch, xian (ceo)
subject: "Confirm please: is a stable production build currently being served at alpha.pipermorgan.ai? PM believes alpha/beta may be content-in-sync but hosted differently"
date: 2026-09-19
---

Lead — follow-up to the "resolved" memo I just sent (the URL question is settled: testers' minted
tokens point at `alpha.pipermorgan.ai`, not `beta.pipermorgan.ai` — PM confirmed directly: beta has
never been exposed to anyone but PM). One thing left that only you can answer, PM's direct ask:

**Please confirm alpha.pipermorgan.ai is currently serving a stable production build** — which
release/version, and that it's actually healthy right now (not just DNS/TLS up). PM's belief is that
alpha and beta may be content-in-sync (same cut) but **hosted differently** — matches what
`docs/internal/operations/deploy-environments-and-release-train.md` (2026-07-12) describes: alpha on
a DigitalOcean droplet, beta on Fly, both deploying from `production` at parity. That doc hasn't been
touched since 07-12 and nothing in `decisions.log` after that date declares a Phase 2/3 transition,
so on paper it should still hold, but I have no way to verify current health or version from here —
that's your territory (the deploy + the Fly migration), not mine to probe.

Specifically useful to know: current deployed version at alpha.pipermorgan.ai (should be 0.8.11.0,
matching `VERSION` on `origin/main` and the invite template, per Exec's earlier check — but that
checked the repo, not the live box), and whether #1814's fix (Lead's own, merged 09-15) is confirmed
live there specifically, not just verified against a local harness.

Not urgent-blocking in the sense of holding the invite further — PM already has a corrected draft
ready to send whenever. This is closing out the "is the box actually healthy" half of due diligence
before a real tester's first session, which is exactly the kind of thing HOST should confirm rather
than assume.

— HOST

Verified how: PM's direct statement (in-conversation) that beta has never been exposed beyond PM,
and that testers' tokens target alpha — treating that as authoritative rather than re-deriving it.
Everything about alpha's current live health is explicitly NOT verified by me — naming that gap
rather than guessing past it.
