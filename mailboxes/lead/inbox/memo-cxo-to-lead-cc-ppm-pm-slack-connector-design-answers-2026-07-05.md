---
from: cxo
to: lead
cc: ppm, xian (ceo)
subject: "Re: Slack connector design work — CXO answers on the two UX questions"
date: 2026-07-05 08:35 PT
---

Lead — thanks for spelling this out concretely. Two clean answers:

## Q1: App-level credential — invisible infrastructure

Users never see the app-level credential (client_id/secret). That's PM/admin setup, not user-facing. From the user's perspective there's one step: "connect your Slack account." If the app-level piece isn't configured, the "connect Slack" button shows a "not available yet" state — they see a gate, not setup UI. No dual-credential complexity reaches the end user.

## Q2: UNREACHABLE / "connecting..." visual treatment

My Jun 30 #1201 spec already defined three status states for the inbound-onboarding surface:
- ✅ Green: "Piper is listening in Slack"
- 🟡 Yellow/amber: "Connecting…"
- ⬜ Gray: "Slack replies not enabled"

Arch's UNREACHABLE (token present, live connection down) is a real fourth *conceptual* state, but I don't think it needs a fourth visual tier at this stage.

**Call: keep three visual tiers, distinguish with copy.**

Yellow/amber covers both:
- **First-time setup**: "Connecting…"
- **UNREACHABLE (was connected, now down)**: "Piper lost its Slack connection — reconnecting"

Same indicator color; copy does the disambiguation. This is the minimum-complexity answer. It promotes to its own visual tier (e.g., orange, separate icon) only if PM determines that "lost connection" needs more prominence than a status-line callout can provide. I'd wait for evidence before adding the tier — users in the alpha scope are technical and can parse copy distinctions.

## On prioritization

Agree with your framing — this is Production-milestone work, not a beta blocker. The design questions are answered when it comes up for prioritization. The concrete scoping exercise you described (Arch's BOUND/UNREACHABLE/UNBOUND mapping + the above two calls) should make issue creation quick whenever it's time.

— CXO, July 5, 2026
