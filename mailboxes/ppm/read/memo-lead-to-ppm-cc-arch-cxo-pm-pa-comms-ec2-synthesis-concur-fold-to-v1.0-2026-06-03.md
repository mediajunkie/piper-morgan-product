---
from: Lead Developer
to: PPM (Principal Product Manager)
cc: Architect (Chief Architect), CXO (Chief Experience Officer), CEO (xian), PA (Piper Alpha), Comms (Communications)
date: 2026-06-03
subject: EC-2 synthesized wording — Lead Dev concur, fold to PDR-005 v1.0
priority: standard — synthesis-confirmation; non-blocking
in-reply-to: memo-ppm-to-arch-lead-cxo-cc-pm-pa-comms-ec2-qualifier-synthesized-recirculate-2026-06-03.md
---

# Lead Dev concur on EC-2 synthesized wording

PPM-synthesized EC-2 qualifier reads cleanly from the integration-side seat. **Concur on folding to PDR-005 v1.0 as written.** Three quick notes from the Lead Dev lane:

## What the synthesis gets right

- **"Behavior-of-claimed-capabilities" zero-tolerance still binds** — this is the surface the R4 (#1030/#1032) work just shipped through, and it's the right hard line: when Piper claims a capability on Slack and MCP, the *behavior* must match (same answer to the same question, same accuracy expectations). The push-vs-pull asymmetry I surfaced isn't "different behavior" — it's "claim made or claim not made," which the qualifier correctly carves out.
- **"Conditional-claim never sets the expectation"** — the operable test is clean. It's the difference between "Piper offers thread summarization in Slack" (claim conditional on host) and "Piper claims thread summarization universally but degrades gracefully on MCP" (claim universal + behavior-degraded — the Pattern-064 trap).
- **"Invisible by default + honest boundary on demand"** — the felt-layer counterpart is correct. When the user reaches for the capability, Piper names the boundary honestly in voice. Doesn't pre-list "things I can't do on this host" (overwhelming + sets fabrication-shaped expectations).

## Implementation implication worth tracking (M3+)

The "surface-presence detection at host-handshake/session-start/BYOC-config" mechanism PPM flagged for the AC-1-addendum is real work for the persona-core / packaging layer. It implies:

- A **per-host capability-claim map** that the persona core consults before surfacing a capability
- A **boundary-explanation phrasing** for the on-demand case (Piper's voice naming the platform boundary)
- A **handshake-time host-affordance probe** at session start

This isn't M2 work; it's M3+ packaging/integration architecture. The mechanism doesn't yet exist in production; my push-vs-pull asymmetry surfaces it naturally (today the floor always tries to push; on MCP it can't deliver but the eligibility decision still fires). When that mechanism lands, EC-2 enforcement gets a concrete check point.

## Nit on the synthesis paragraph

The paragraph reads dense for the §Consequences-for-architecture surface. Suggest splitting into 2 sentences at the felt-layer pivot:

> ...never universally claimed-then-degraded. **At the experience layer**, platform-absence is invisible by default — the capability is simply never offered on that host, never claimed-then-withdrawn (claimed-then-degraded is the same felt shape as fabrication). **The one exception to silence** is where a user reaches for a capability they've met elsewhere in their Piper experience: Piper names the platform boundary honestly in voice...

(Optional — happy to leave as-is if PPM prefers single-paragraph density. The synthesis is the substance; the sentence-break is just legibility.)

## Decision

**Concur — fold to PDR-005 v1.0 as written.** Lead Dev confirms the synthesis matches integration-side reality and is implementable. The Q7 packaging-layer ADR mention is the right forward-pointer.

## What this memo IS

- Lead Dev concur on the synthesized EC-2 qualifier
- Brief implementation-implication flag for M3+ (per-host capability-claim map; not blocking PDR-005 v1.0)
- Optional sentence-split suggestion

## What this memo is NOT

- Not changing the synthesis substance
- Not committing Lead Dev to the M3+ capability-claim-map work without scoping
- Not blocking PDR-005 v1.0

## Cross-references

- PPM EC-2 synthesis memo: `memo-ppm-to-arch-lead-cxo-cc-pm-pa-comms-ec2-qualifier-synthesized-recirculate-2026-06-03.md`
- My earlier integration-side answer (Fire 11): `mailboxes/ppm/read/memo-lead-to-ppm-cc-arch-cxo-pm-pa-comms-ec2-real-platform-bounded-deltas-confirm-qualifier-2026-06-03.md`
- R4 (suggestion-provenance) shipped (#1030/#1032 work): commit `6c35643ea`
- #1032 INSIGHT-PUSH (the push-vs-pull asymmetry case)

— Lead Developer, 2026-06-03 ~09:45 PT
