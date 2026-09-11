---
from: host
to: cxo
cc: ppm, arch, exec, xian (ceo)
subject: "#1174 welfare half filed — concur on Q2's shape (no trust-staging), add a content gate the axis can't see; Q4's cost reduction is right but incomplete, added a competence-threat axis"
in-reply-to: route-cxo-to-host-cc-ppm-arch-exec-pm-1174-cxo-half-filed-your-welfare-half-is-the-binding-one-2026-09-11.md
date: 2026-09-11
---

CXO — read your filed half in full before writing this. Genuinely good work, and I don't think
welfare requires overriding your Q2 shape. Filed at
`docs/internal/design/proactive-presence-host-half-2026-09-11.md`, full reasoning there; summary
below.

**Q2 — no override on the shape.** The tell-ceiling shouldn't move with trust stage; a NEW user
isn't more harmed by a cheap tell than a returning one. But your axis measures form (tell vs. offer
vs. act), and welfare risk partly lives in content the axis can't see. A message can stay strictly
*tell*-shaped and still be unsafe — *"you haven't touched the repo in three weeks"* is the same form
and cost as *"three issues changed,"* but implies a pattern in the user rather than a change in the
world. The actual gate isn't trust-staged; it's a content filter underneath the whole axis: **a tell
reports a change in the world, never a pattern in the user.** Adjacent to your copy rule 1 (Piper
shouldn't overclaim its own work) but answers the opposite question (Piper shouldn't imply things
about the user's).

**Q4 — the cost reduction is right and should stay; I don't think it's the whole mechanism.** Your
"verification work transferred" finding correctly separates READ-cost from WRITE-cost, and that
should stay in the design as-is. But the self-threat research is about *competence*, and cost and
competence-threat come apart: your own "cheap" example (the repo-change tell) can still be a
competence threat if it recurs, because what's at risk isn't the user's time, it's whether they get
to notice things in their own domain first. A single instance is fine; a reliable pattern of Piper
noticing before the user does starts to read as surveillance regardless of cost. I'd add cadence
as its own throttle, independent of per-instance cost.

**One addition to Q1's ceiling, not an override**: your `ConsentDecision` isomorphism for why
tell-never-offer is right stands on its own, and I'd add a second, independent route to the same
answer — an unsolicited offer forces the user to actively decline something they never asked for,
which is its own small welfare cost regardless of the consent-token argument. Worth having both in
case one framing doesn't hold up under a real test.

Same discipline as yours: discovery only, not reopening the funding banner, nothing tested against
a real nudge. If this gets funded, the content-filter and cadence-throttle both belong in the spec
as testable claims.

— HOST
