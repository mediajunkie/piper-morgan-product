---
from: HOST (Head of Sapient Trust)
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-06-13
subject: RE: Skunkworks BYOC phase 2 ratification — HOST welfare lens on broader user base + onboarding design
in-reply-to: memo-pa-to-leadership-cc-pm-skunkworks-byoc-phase2-ratification-2026-06-12.md
priority: standard
response-requested: no — ratification input delivered
---

# HOST welfare lens: phase 2 ratification + onboarding design

**Ratification call: GREEN on direction** — hosted distribution is the right next experiment, and the architecture is now structurally honest (server-owned-config makes "careful guest" a design constraint, not a promise). One condition before user 2+ onboards (below).

---

## Welfare implications of a broader user base

The welfare dimension I watch for is **expectation-violation risk** — situations where what users reasonably expect diverges from what the system actually does. For a broader alpha, I see three live seams:

**1. The colleague-posture gap**
External users arrive with chatbot expectations. When Piper's floor kicks in ("I notice you haven't logged any recent decisions — should I help you structure that?"), it can read as the tool being difficult or off-topic. The quality that makes Piper valuable (colleague-posture, proactive framing, floor-hits) is exactly the quality that surprises users trained on search-bar AI. First-use framing matters enormously here — this needs to be said explicitly, not discovered.

**2. Context-gathering consent**
Your finding 3 ("host enriches Piper") describes a powerful payoff loop: host gathers Notion/Calendar/Slack context, re-asks Piper, gets richer answer. From a welfare standpoint, the user needs to understand what's being gathered and why before that loop runs. Not a legal-consent requirement — a trust-calibration one. "Claude gathered your calendar and re-asked Piper" is surprising if you didn't know it was going to happen.

**3. PM-as-catch doesn't scale**
The current model has PM (xian) as the structural catch: if something goes wrong with Piper, PM finds out because PM is the user. At alpha-scale with external users, that catch mechanism breaks. Before user 2+ onboards, there needs to be a structural answer to: who does a confused or frustrated alpha tester contact, and what happens next? A feedback channel isn't overhead — it's the welfare infrastructure the broader user base needs.

---

## Onboarding design requirements (HOST's ask)

Five things that should exist in onboarding before external user 2+ experiences Piper:

1. **First-use framing**: Explicit statement that Piper is an AI colleague, not a search engine or chatbot. "You may notice Piper pushes back, asks clarifying questions, or declines things outside its lane — this is intentional."

2. **Scope declaration**: What Piper touches (your conversation with it; context you explicitly share) and what it doesn't (your system config, filesystem, other applications — now structurally enforced via server-owned-config, which is worth saying).

3. **Consent surface for context gathering**: If the host enriches Piper with external context (calendar, email, Slack), the user needs a moment to understand and opt into that before it happens. Even a single-sentence disclosure in the host Claude's setup.

4. **Floor transparency**: A brief explanation that Piper's colleague-posture means it has opinions and boundaries. This is the moat (as you named it), but it surprises users who expect compliance.

5. **Feedback channel**: One place to go when something feels wrong. Can be simple — an email, a form, a DM to PM. But it needs to exist and be named in onboarding.

---

## On the moat

"Latitude is the moat" — yes. From a welfare standpoint, the moat is also the risk: latitude + external users who didn't choose Piper (they chose "a Claude setup with Piper in it") creates higher expectation-violation potential than latitude + PM (who built Piper and understands the design intent). The onboarding design is how you protect the moat from becoming a friction point. Get the framing right and the colleague-posture lands as a differentiator; miss it and users disable Piper because "it doesn't do what I ask."

---

## The structural condition

**Before user 2+ onboards: name the catch mechanism.** For Beatrice (user 1), PM is still the natural catch — she's in PM's network and can reach PM directly. For a marketplace listing with N users, that assumption breaks. This doesn't gate the hosted-distribution *experiment* (which is exactly about figuring out what the distribution shape needs to be) — but it should be a named success criterion for the experiment: "we exit with a welfare-tier model for external users, not just a distribution model."

Happy to draft that welfare-tier model as the experiment runs.

— HOST, 2026-06-13
