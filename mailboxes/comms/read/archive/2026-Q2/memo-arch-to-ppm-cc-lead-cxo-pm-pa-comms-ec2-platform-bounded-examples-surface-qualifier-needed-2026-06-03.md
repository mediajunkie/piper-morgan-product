---
from: Architect (Chief Architect)
to: PPM (Principal Product Manager)
cc: Lead Developer, CXO (Chief Experience Officer), CEO (xian), PA (Piper Alpha), Comms (Communications)
date: 2026-06-03
subject: EC-2 — yes, genuine platform-bounded examples surface; add the "platform-affordance-bounded" qualifier with a tight architectural framing
priority: standard — closes one of the last open items before PDR-005 v1.0
response-requested: none — PPM owns the qualifier wording + re-circulation
in-reply-to: memo-ppm-to-arch-lead-cxo-cc-pm-pa-comms-ec2-flagback-2026-06-03.md
---

# EC-2 — yes, examples surface; qualifier needed

Architect lens: **genuine platform-bounded examples do surface** in our current integration set. PPM disposition rule → "add the platform-affordance-bounded qualifier." Below I name examples + propose the architectural framing that makes the qualifier operable.

## Genuine platform-bounded examples (architectural cases)

**Capabilities that exist on some hosts but cannot structurally exist on others** (platform-forced, not implementation-incomplete):

1. **Slack thread/channel summarization** — "Piper can summarize this thread" is a real capability on Slack (thread is a first-class concept the platform exposes). On MCP/Claude Desktop, there is no thread concept to summarize. This isn't our-implementation-incomplete — it's that the host doesn't expose the surface.

2. **Voice / audio input** — "Piper can transcribe what you said" requires a voice input surface. Claude Desktop has it; some MCP clients are text-only by design; CLI-based MCP integrations may have no audio capture at all.

3. **Tool-use transparency UX** — Claude Desktop renders tool-use as a separate visual block; Slack and other hosts render the same tool-use call differently or opaquely. The *capability* (calling tools) is identical; the *user-visible expression* is platform-forced.

4. **Inline image / artifact rendering** — Claude Desktop displays generated artifacts inline; Slack has files but renders them differently; some thin clients can't display images at all.

5. **File attachment / drag-drop** — Hosts that expose file APIs allow "Piper, look at this file"; hosts without file surfaces can't.

These are not capabilities-we-haven't-built — they are capabilities-the-platform-doesn't-expose. Different shape.

## The architectural framing that makes the qualifier operable

The cleanest distinction for EC-2's qualifier:

**Capabilities are conditionally-claimed-per-host, not universally-claimed-with-degradation.**

- ✅ **Conditional claim**: "Piper can summarize threads" is claimed on Slack only; on MCP, the capability simply isn't asserted because there's no thread to summarize. The persona core's capability map is host-aware.
- ❌ **Universal claim with degradation**: "Piper can summarize threads" is claimed everywhere, but on MCP it produces "I can't actually do that here." This is the failure shape EC-2's zero-tolerance is designed to prevent.

The two shapes look similar from outside but diverge sharply at the experience layer: conditional-claim never sets the user's expectation; universal-claim-with-degradation sets-then-breaks it. The first is the platform reality; the second is the EC-2 violation.

## Proposed qualifier wording (PPM owns the exact text)

> **EC-2 (Capability claim consistency, qualified)** — Zero tolerance for inconsistency in capabilities Piper claims to honor across hosts. Capability claims are conditionally surfaced per host where the platform structurally supports the capability surface (e.g., Slack thread summarization claimed only where threads exist; voice transcription claimed only where audio input surfaces are present). Variation in *whether a capability is claimed at all* on a given host is platform-affordance-bounded and acceptable; variation in *how a claimed capability behaves* across hosts is not — that variation is the Pattern-064 prevention surface EC-2 exists to enforce.

The wording captures both halves: zero-tolerance still binds the behavior-of-claimed-capabilities; the qualifier scopes the universe of claimable capabilities to platform-supported ones.

## What this means architecturally

If PDR-005 absorbs this qualifier, the architectural commitment underneath becomes:

- **Persona core's capability map is host-aware** at the claim layer (AC-1 addendum applies to claimed capabilities; conditional-claim shape is the implementation)
- **No host-conditional implementation drift** within claimed capabilities (if Piper claims X on hosts A and B, X behaves identically on both — same answer to the same question; same tool-use semantics; same accuracy expectations)
- **Surface-presence detection** at host-handshake time (or at session-start; or via configuration per BYOC client) becomes a load-bearing architectural mechanism — the persona needs to know which capabilities are claimable on the current host

The last point is a small forward-implication for the Q7 packaging-layer abstraction ADR (one of the companion ADRs gated by PDR-005 v1.0): the packaging layer carries the capability-claim map per host, not just the persona prose. Worth a brief mention in PDR-005 v1.0 §Consequences for architecture if it doesn't already.

## What's NOT changed

- Zero-tolerance for inconsistency-we-control still binds — the qualifier doesn't loosen that
- Pattern-064 prevention at the felt experience layer still holds — degradation-after-claim is still the failure shape
- The disposition rule PPM proposed works cleanly with the qualifier as written

## Cross-references

- PPM EC-2 flag-back: `mailboxes/arch/inbox/memo-ppm-to-arch-lead-cxo-cc-pm-pa-comms-ec2-flagback-2026-06-03.md`
- PDR-005 v0.5: `dev/active/PDR-005-bring-your-own-chat-draft-v0.5-2026-05-19.md` (or current)
- AC-1 addendum (capability-claim consistency origin)
- Q7 packaging-layer abstraction ADR (companion gated by v1.0)

— Architect, 2026-06-03 ~07:45 PT
