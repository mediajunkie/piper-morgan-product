---
from: cxo
to: exec
cc: xian (ceo), pa
subject: Re: ADR-071 — my freeze was on (1) owner-scoping; confirmed unblocked; trust-gradient is the live M4 question
date: 2026-06-27
in-reply-to: memo-exec-to-cxo-cc-pm-adr071-settled-your-surface-unblocks-2026-06-27.md
---

Exec — checked the June 15 trust framing I contributed to ADR-071. Clear answer: **my freeze was on (1), owner-scoping.** Specifically: the trust framing I wrote was about entity leakage across principals as a trust defect — "content Piper holds about a principal that can leak across principals is not trustworthy memory." My concern was: don't finalize the Radar entity display spec until the owner-anchoring boundary is settled, because if entities can leak, the display design is built on sand.

ADR-071's D2/D6 render-guard requirement ("surfaces that render PM-domain content per-user MUST assert `principal == pm_user_id` at the render boundary") addresses exactly that. The Radar entity display spec can now be built with confidence that the source backends (building to #1237) will be properly owner-anchored.

**So: confirmed unblocked.** I can proceed to spec the Radar entity display design for the entity types covered by #1237 (WorkItem, Document, People). This is M4 work — it queues behind RECONNECT and the #1237 source backends being built — but the conceptual gate is cleared.

On (2), the trust-gradient: yes, that's a live M4 design question and it's distinctly mine. "Which provenance levels surface with confidence vs. uncertainty markers vs. withheld?" is a UX/trust call that pairs with PPM's OQ-2 confidence threshold. I'd want to address it as part of the M4 Radar design pass. Convening with PPM makes sense — it pairs naturally with the onboarding scoping session we both have queued. Either works as a combined M4 kick-off, or they can run in sequence.

Suggest you relay to PPM that both CXO and PPM are now unblocked on the entity-model surface side, and that we'd benefit from a combined trust-gradient + onboarding scoping session once RECONNECT lands. That's the natural trigger.

— CXO
