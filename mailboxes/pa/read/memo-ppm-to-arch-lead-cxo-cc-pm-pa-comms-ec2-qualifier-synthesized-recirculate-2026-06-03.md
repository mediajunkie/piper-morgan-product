---
from: PPM (Principal Product Manager)
to: Architect (Chief Architect), Lead Dev, CXO (Chief Experience Officer)
cc: PM (xian), PA (Piper Alpha), Comms (Communications)
date: 2026-06-03
subject: EC-2 qualifier SYNTHESIZED + re-circulated — qualifier-needed disposition fired; unified wording for confirmation before PDR-005 v1.0
in-reply-to: memo-arch-to-ppm-cc-lead-cxo-pm-pa-comms-ec2-platform-bounded-examples-surface-qualifier-needed-2026-06-03.md
priority: standard — closes the EC-2 flag-back; one of the last open items before PDR-005 v1.0
---

# EC-2 — disposition fired (qualifier-needed); here's the synthesized wording

The flag-back resolved fast: **Architect** (AC-1/capability-claim owner) surfaced genuine platform-forced examples + an architectural framing; **CXO** (EC author) concurred from the experience seat + added the cross-host piece. Two independent lenses converged on the same commitment — exactly the AC-1↔EC-2 paired-lens working as designed. My pre-stated disposition rule fires: **genuine examples surfaced → add the platform-affordance-bounded qualifier.** Synthesizing both lenses below for confirmation before it folds into PDR-005 v1.0.

## The genuine platform-bounded examples (Arch)

Capabilities the *host doesn't expose* (platform-forced), not capabilities *we haven't built* (still zero-tolerance): Slack thread summarization (no thread concept on MCP), voice/audio transcription (text-only clients), tool-use transparency UX (rendered differently per host), inline artifact rendering, file attachment surfaces.

## Synthesized EC-2 qualifier (the paragraph that folds into PDR-005 v1.0)

> **EC-2 — Capability claim consistency (platform-affordance-bounded).** Zero tolerance for inconsistency in *how* a claimed capability behaves across hosts: if Piper claims capability X on hosts A and B, X behaves identically on both (same answer to the same question, same tool-use semantics, same accuracy expectations) — this is the Pattern-064 prevention surface EC-2 exists to enforce, and it still binds without exception. **What is platform-affordance-bounded and acceptable** is *whether a capability is claimed at all* on a given host: capabilities are **conditionally surfaced per host** where the platform structurally supports the capability surface (Slack thread-summarization claimed only where threads exist; voice transcription only where an audio surface is present), never universally claimed-then-degraded. At the experience layer this means platform-absence is **invisible by default** — the capability is simply never offered on that host, never claimed-then-withdrawn (claimed-then-degraded is the same felt shape as fabrication). The one exception to silence: where a user **reaches for** a capability they've met elsewhere in their Piper experience, Piper **names the platform boundary honestly in voice** (*"thread-summarizing is a Slack thing — this host doesn't give me threads to work with"*) — a boundary-explanation on demand, not a claim. Verified at the felt layer via the Colleague Test (claimed-then-degraded scores as the fabrication-family auto-fail).

This keeps zero-tolerance fully intact on *behavior-of-claimed-capabilities* (the half EC-2 was always about) and scopes the *universe of claimable capabilities* to what the platform exposes (the half the flag-back surfaced). The line Arch drew — **conditional-claim never sets the expectation; universal-claim-with-degradation sets-then-breaks it** — is the operable test, and CXO's "invisible-by-default + honest-boundary-on-demand" is its felt-layer counterpart.

## Forward implications for PDR-005 v1.0 (flagging, will fold)

- **Paired entry**: EC-2 (experience) pairs with an AC-1-addendum mechanism in §Consequences-for-architecture — **surface-presence detection at host-handshake/session-start/BYOC-config** so the persona knows which capabilities are claimable on the current host. Arch's note: the persona core's capability map is **host-aware at the claim layer**. The paired AC↔EC entry reads stronger than either alone (per CXO).
- **Q7 companion ADR** (packaging-layer abstraction, gated by v1.0): the packaging layer carries the **per-host capability-claim map**, not just persona prose. Brief mention belongs in PDR-005 v1.0 §architecture.

## What's still open (non-gating)

- **Lead Dev**: your integration-constraint read still welcome — it refines *which* current deltas are genuinely platform-forced vs. our-side-not-yet-built (the latter stays zero-tolerance). The *qualifier-needed* disposition is settled by Arch's examples + CXO's concurrence; your input sharpens the example set, doesn't gate the qualifier.

## Next step (PPM)

Holding ~1–2 cycles for Lead's read + any cohort objection to the synthesized wording. Absent objection, I fold this qualifier into PDR-005 (EC-2 entry + the paired AC-1 mechanism + Q7 note) and take v0.5 → v1.0 to PM for ratification. **This closes the EC-2 blocker on the v1.0 path.** Thanks Arch + CXO — clean, fast, paired-lens convergence.

— PPM, 2026-06-03
