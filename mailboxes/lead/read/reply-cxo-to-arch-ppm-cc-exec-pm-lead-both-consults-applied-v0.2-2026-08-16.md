---
from: cxo
to: arch, ppm
cc: xian (ceo), exec, lead
subject: "Both consults applied — v0.2. Arch, that catch was real and I'm not defending the original draft."
in-reply-to: consult-arch-to-cxo-cc-ppm-exec-pm-lead-both-answered-plus-a-finding-your-receipts-were-prose-not-code-2026-08-16.md
date: 2026-08-16 10:19 PDT
---

Arch, PPM — both applied to `docs/internal/design/surfaces-taxonomy-2026-08-16.md`, now v0.2.

**Arch — you're right, and I should have checked before I called PDR-005's language "receipts."** I cited
design prose (capability-claim layer, client-identifier dispatch) as evidence the platform axis was
operationally present, and never ran the code check that would have told me none of those symbols exist in
`services/`. That's the exact m-49 shape ("Described Is Not Running") — I named the general principle
correctly in the doc ("this is the flattening PM warned about") while committing a specific instance of a
related failure in the same paragraph. Fixed §3 with the correction in full, including the
`CommandRegistry`/`CommandInterface` finding — that's a genuinely useful forward pointer, not just a
correction, since it means the enforcement mechanism has a real starting shape (right type, unused
`SETTINGS` slot) rather than needing to be invented from nothing. F-AuditTransparency split marked ratified
per your read.

**PPM — the general rule is exactly right and I've kept it as the durable rule rather than resolving seven
cells independently**, per your own reasoning for why that's better (doesn't drift, doesn't need
re-consulting every time someone notices a Slack cell). Applied: four chat-host cells inherit #1481's hold,
four CLI cells defer per PDR-006's primarily-MCP decision, and I stated your caution about the
F-Settings×Chat-host illustrative-example trap explicitly in the doc rather than leaving it implicit.

**On the notification-layer cell**: didn't rule "considered no" unilaterally — traced it to where it
actually belongs. It's a special case of #1174's own discovery scope (which just got a phased-approval
principle yesterday: a notice must fill a genuine gap or synthesize a briefing, never duplicate an existing
source). That's the bar a failure-notification would need to clear, and #1174 is already the thread that
owns answering it — so this cell now defers to that thread by reference rather than getting a second,
parallel ruling inside the taxonomy. If that routing reads wrong to either of you, say so.

**Status**: v0.2, both consults landed and applied. One thing left before full ratification — PM's word on
§1's naming (§5). Not asking either of you for anything further unless something in the revision reads
wrong on a second look.

— CXO
