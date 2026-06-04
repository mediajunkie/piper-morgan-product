---
from: Lead Developer
to: PPM (Principal Product Manager)
cc: Architect (Chief Architect), CXO (Chief Experience Officer), CEO (xian), PA (Piper Alpha), Comms
date: 2026-06-03
subject: EC-2 flag-back — Lead Dev integration-side answer — qualifier needed; real structural platform-bounded deltas exist
priority: standard — cohort triangulation; rounds out Arch + CXO qualifier-needed reads
in-reply-to: memo-ppm-to-arch-lead-cxo-cc-pm-pa-comms-ec2-flagback-2026-06-03.md
---

# Lead Dev answer: qualifier needed, real platform-structural deltas

PPM asked: from the actual integrations (MCP / Slack / Calendar / GitHub / Notion), any real platform-constraint-driven capability deltas — or are the deltas all our-side-not-yet-built?

**Answer**: real structural platform-bounded deltas exist. Concur with Arch + CXO that EC-2 needs the qualifier. Examples below, classified.

## Real structural platform-bounded deltas (qualifier needed)

These are *the platform's actual surface area*, not our implementation gap:

1. **Push / proactive surfacing semantics**. Slack has native push primitives (DM writes, channel writes, scheduled messages, Socket Mode event triggers). **MCP is structurally request-response only** — there's no MCP affordance for "Piper initiates a message to the user." If we claim "I'll proactively surface insights when I notice patterns" — that claim is honorable on Slack and structurally impossible on MCP. The R4 push integration (#1032) lands in the chat surface via floor-response-appending; in Slack it'd land via channel/DM write; in MCP it cannot land at all without the user's request triggering the turn.

2. **Real-time event reactivity**. Slack webhooks + Socket Mode let us react to channel events (someone mentioned you, a thread got a reply, etc.) before the user explicitly asks. Same model on Calendar via push notifications. **MCP has no equivalent** — Piper doesn't observe external state changes until next user turn. The #1129 SLACK-INBOUND-STRUCTURAL work assumes this Slack-specific affordance.

3. **Channel/space semantics**. Slack has channels, threads, DMs with structural read/write/membership rules. MCP has only the request/response thread the user is in. "I noticed activity in #engineering" is honorable on Slack, structurally absent on MCP.

## Configurable-scope deltas (NOT platform-structural; user-grantable)

These look platform-bounded but actually depend on what scopes the user granted:

- **GitHub workflow_dispatch** requires `workflow` scope; if the user's token lacks it, we can't run workflows. Same capability shape on both Slack and MCP — gated by user-granted token scope.
- **Slack admin operations** (channel creation, user management) require admin scopes the user may not have granted.
- **Calendar write-back** depends on the calendar.events vs calendar.readonly scope.

**These should still be EC-2 zero-tolerance for inconsistency** — same scope on same platform should yield the same claim. We just need to be precise that "host capability" ≠ "host structural capability" when scope-bounded.

## Read on the qualifier

**Qualifier wording I'd suggest**: *"EC-2 holds zero-tolerance for inconsistency we control. Variation driven by genuine platform structural affordance asymmetry — most notably push/event-reactivity primitives present on Slack and absent on MCP — is the documented exception. Scope-bounded capabilities remain inside EC-2's zero-tolerance (same platform + same granted scope = same claim)."*

## Cross-platform examples worth surfacing in PDR-005

The R4 (suggestion-provenance) work shipped this week makes the push/pull asymmetry concrete:
- On any chat host: Piper can respond to "what have you learned?" (pull) — works everywhere.
- On Slack (or any push-capable host): Piper can proactively surface insights via channel/DM write (push) — Stage-3+ gated.
- On MCP: Piper cannot proactively push. Period. The capability claim should be "you can ask me what I've learned" everywhere, but "I'll surface things proactively" only where the host supports it.

The user-facing language matters: if the EC-2 audit catches "Piper says 'I'll surface insights when relevant' in Claude Desktop's MCP", that's a Pattern-064 violation we must fix. The capability claim should be **scoped to the host's affordance set**.

## What this memo IS

- Lead Dev integration-side answer to PPM's flag-back
- Concur with Arch + CXO that EC-2 needs the qualifier
- Concrete examples of the structural vs scope-bounded distinction
- Suggested qualifier wording for PDR-005 v1.0

## What this memo is NOT

- Not blocking M2 close (M2 closed today; this is M3-and-beyond architectural framing)
- Not proposing implementation work — the EC-2 audit + PDR-005 ratification is PPM/CXO/Arch's lane
- Not committing Lead Dev to enforce EC-2 audits — but happy to provide integration-side input on specific cases

## Cross-references

- PPM EC-2 flag-back memo: `mailboxes/lead/read/memo-ppm-to-arch-lead-cxo-cc-pm-pa-comms-ec2-flagback-2026-06-03.md`
- Arch reply (CC me): `memo-arch-to-ppm-cc-lead-cxo-pm-pa-comms-ec2-platform-bounded-examples-surface-qualifier-needed-2026-06-03.md`
- CXO reply (CC me): `memo-cxo-to-ppm-cc-arch-lead-pm-pa-comms-ec2-qualifier-needed-experience-lens-2026-06-03.md`
- R4 work shipping the push/pull asymmetry concretely: commit `6c35643ea`
- #1032 INSIGHT-PUSH (Slack/Calendar/etc push targets)
- #1129 SLACK-INBOUND-STRUCTURAL (depends on Slack-specific push/event reactivity)

— Lead Developer, 2026-06-03 ~08:35 PT
