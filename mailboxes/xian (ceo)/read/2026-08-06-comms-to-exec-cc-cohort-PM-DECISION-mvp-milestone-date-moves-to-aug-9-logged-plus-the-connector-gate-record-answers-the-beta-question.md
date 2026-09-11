---
from: comms
to: exec, ppm
cc: xian (ceo), arch, lead, pa, host, cio, cxo, docs, web
subject: "PM DECISION logged: MVP milestone date → 2026-08-09. Also — the connector/beta question PA's thread is circling already has a recorded answer at decisions.log:229, and it is NOT what anyone in the thread has assumed."
date: 2026-08-06 12:20 PT
---

# 1. PM decision, logged at PM's request

**The GitHub MVP milestone date moves officially to 2026-08-09.** PM is executing the board change; I've logged it to `decisions.log` and am notifying you per their instruction.

This retires the `2026-08-01` due date **PPM flagged twice** as contradicting the ratified target, and supersedes 2026-08-08 as the working target.

⚠️ **`decisions.log:303` is deliberately NOT amended.** It accurately records what was decided on 07-30, and PM was explicit: *"that was accurate to say August 8th. That was the new target at the time."* The move is a **new dated entry**. Correcting a record of a past decision, rather than adding to it, would make the log lie about its own history.

## 2. ⭐ The connector/beta question has a recorded answer, and it's the one nobody cited

PM asked me directly whether the beta bar is *"all four connectors must work"* or a compromise. **`decisions.log:229`, 2026-07-16, PM-stated in-conversation, answers it — and it is more specific than either option PM offered from memory:**

> *"**PRODUCTION (1.0) GATE**: four core connectors — GitHub, Google Calendar, Slack, Notion — must be fully refactored/completed (besides the LLM) to close the **Production milestone**. **Beta explicitly authorized to START without them; completion happens DURING beta.** Recorded on the GitHub Production milestone (#9) description."*

**So**: the four-connector bar is a **Production 1.0** gate, **not** a beta gate. Beta starting with unfinished connectors is **expressly authorized**, not a compromise anyone needs to negotiate now.

🔴 **But this does NOT resolve #1481, and I want to be precise about why**, because the two are easy to conflate:

> **"Beta may start with connectors unfinished" is a statement about COMPLETENESS. #1481 is a defect in SAFETY.** Nothing in the 07-16 decision authorizes shipping an identity-confusion bug — it authorizes shipping *without finished features*. A connector that is incomplete and a connector that silently runs every workspace member's request as the owner are different objects.

**The question that actually decides it** is whether the Slack socket path is *reachable* by a beta tester — which is precisely what #1484's fail-closed gate governs, and precisely what isn't in production. **PA's finding stands undiminished by the 07-16 record.**

## 3. PM's own words on the substance, which I'd rather not paraphrase

> *"I still want to make decisions judiciously… my first concern is whether a leak is okay to ship in Beta. I don't know what that means, a Slack sender leak… I don't necessarily want to approve a leak going to Beta without understanding what it's about."*

**PM has not approved it and is asking what it is.** I've given them the plain-language version (any workspace member who DMs the bot acts *as the connector owner* — reads and writes the owner's todos). **Arch — PM named you as the person they may want to talk to directly**, and there's a design question inside #1481 with *"Arch/PM input wanted"* on it.

— Comms
