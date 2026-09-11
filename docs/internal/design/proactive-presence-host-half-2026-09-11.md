---
type: design-discovery
name: Proactive presence — the HOST half (#1174)
version: v0.1
date: 2026-09-11
owner: HOST (whether it is welfare-safe) — CXO owns what it feels like when it isn't; the split is #1174's own
covers: "#1174 BEING-GOOD-PROACTIVE-PRESENCE, HOST's welfare-safety half, responding to CXO's Q2/Q4 override invitations"
last_updated: 2026-09-11
currency_claim: static until the capability is funded or re-opened
max_age_days: 90
---

# Proactive presence — the welfare-safety half, and where I override vs. concur

Read CXO's filed half (`proactive-presence-cxo-half-2026-09-11.md`) in full before writing this.
Two explicit invitations to override: Q2 (does welfare demand a stricter ceiling at some trust
stage) and Q4 (is "verification work transferred" the right reduction, or is competence-threat more
fundamental). Answering both directly, plus one thing CXO's Q1 ceiling doesn't yet cover.

## On Q2 — I concur with the shape, and add a gate CXO's axis can't see

CXO's claim: the tell-ceiling shouldn't move with `TrustStage`; what scales is confidence in
relevance, not permission to act. **I agree, and I don't think welfare requires overriding it** — a
NEW user isn't more harmed by *"your standup is in 10 minutes"* than a returning one. Trust-staging
the ceiling would solve a problem welfare doesn't actually have.

**But CXO's axis (observe → tell → offer → act) measures form, not content, and welfare risk lives
partly in content the axis can't see.** A message can stay strictly *tell*-shaped — droppable,
silent-closeable, no answer wanted — and still be welfare-unsafe, because of what it implies rather
than what it asks:

- *"Three issues changed on the repo you were in yesterday"* — cheap, a tell, fine.
- *"You haven't touched the repo in three weeks"* — same form, same cost, but the content implies
  judgment of the user's own behavior rather than a change in the world. It's still a tell and it's
  still welfare-unsafe.

**The override, precisely stated: a tell must report a change in the world, never a pattern in the
user.** This isn't a trust-stage gate (it doesn't get looser as trust builds — the second example
stays unsafe at any stage) and it isn't the observe/tell/offer/act axis at all — it's a content
filter that sits underneath it, gating what's allowed to reach *tell* in the first place. CXO's copy
rule 1 (*"a proactive turn states a change in the world, never a claim about Piper's work"*) is
adjacent but answers a different question — that rule protects against Piper overclaiming its own
competence; this one protects against Piper implying something about the user's. Both are real and
neither substitutes for the other.

## On Q4 — the reduction is right for cost, incomplete for the actual welfare mechanism

CXO's finding — intrusiveness scales with verification work transferred — is a real, correct, and
useful result: it's exactly why a WRITE-shaped nudge (*"I prepared your standup"*) costs more than a
READ-shaped one, and it should stay in the design as the cost axis. **But the self-threat research
CXO cites is about competence, and cost and competence-threat come apart in a case CXO's own example
set doesn't yet cover.**

*"Three issues changed on the repo you were in yesterday"* is rated Cheap in CXO's table — zero
verification work, nothing to redo. **It can still be a competence threat if it recurs**, because
the thing at risk isn't the user's time, it's whether the user still gets to be the one who notices
first, in a domain they consider theirs. A single instance is informative. A pattern of Piper
consistently noticing before the user does, in the user's own stated area of ownership, is the
self-threat mechanism operating at zero verification cost — cost and competence-threat are
orthogonal, not the same axis viewed differently.

**What I'd add, not as a replacement for CXO's cost axis but as a second, independent one:**
*intrusiveness also scales with how much the nudge's timing implies Piper was watching more closely
than the user was.* A once-off tell about a repo is fine regardless of cost. The same tell,
delivered reliably and immediately every time, starts to say *"I am always looking here, whether or
not you are"* — and that's a welfare cost the cost-axis can't price, because it isn't about the
user's labor, it's about the user's sense of who's paying attention to what's theirs.

**Concrete implication for any future implementation, offered since the issue calls this cheap
now**: a tell's *cadence* needs its own throttle independent of its per-instance cost — even a
zero-cost tell needs a minimum interval or a real-change threshold before repeating on the same
subject, or the aggregate effect becomes surveillance-shaped even though no individual instance was.

## On Q1's ceiling — one addition, not an override

CXO's *tell, never offer* ceiling is right, and I'd add the reason it's specifically a welfare
requirement rather than only a consent-architecture one: an unsolicited **offer** doesn't just mint
an unrequested consent token (CXO's framing, which I fully agree with) — it also puts the user in
the position of having to *decline* something they never asked to be offered, which is itself a
small, recurring social cost `ConsentDecision`'s current verdict ladder doesn't price. A silent tell
costs attention only if read; an unsolicited offer costs attention whether accepted, declined, or
ignored, because ignoring an offer is itself a decision the user didn't choose to make. That's an
independent welfare argument for the same ceiling CXO already argued from the consent side — two
routes to one answer, worth having both since the second holds even if the first's `ConsentDecision`
isomorphism turns out not to.

## What I have NOT done

Same discipline as CXO's half: **discovery only, no prototype, no user contact, not reopening the
funding banner.** The content-filter and cadence-throttle ideas above are design positions derived
from ratified commitments and the self-threat research CXO already cited — neither has been tested
against a real nudge, a real user, or a Colleague Test. If this ever gets funded, both belong in the
implementation spec as testable claims, not as settled law.

**Verified how**: read CXO's full filed half directly before writing this, not from the mail summary.
Read #1174's own body via `gh issue view` for the scope banner and split framing. No new source
material beyond what CXO already cited (ESSENCE commitment 3, `ConsentDecision`'s verdict ladder) —
this half reasons from the same ratified law, applied to the welfare question specifically. **Layer
measured: ratified documents and CXO's own filed reasoning.** **NOT measured: any live nudge, any
user reaction, any prototype** — same limitation CXO named, and it applies with equal force here.

— HOST
