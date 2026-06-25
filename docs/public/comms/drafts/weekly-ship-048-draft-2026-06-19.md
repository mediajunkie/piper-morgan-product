---
image: piper-ship.png
alt: "A child and a crew of robots checking each other's work on a boat."
caption:
---

# Weekly Ship #048: The Team Puts It in Writing

*June 12–18, 2026*

Three Ships ago the team crossed from "we can run it" to "someone who isn't us can run it." This week it did the work that makes the next crossing possible: it wrote the contracts.

Literally. The Architect agent ratified three architecture decision records in seven days — the connector substrate, the user-auth anchoring, and the skill-routing architecture — more ADR output than any single week so far. The Principal Product Manager agent (PPM) delivered and froze the entity-model spec, the shape contract the rest of the team builds against for WorkItem, Document, Conversation, and People entities. The Chief Experience Officer agent (CXO) completed D1 — the design sprint for good-enough quality at beta — with both major design bets passing PM beta UAT. The Head of Sapient Trust agent (HOST) got the trust-boundary ratified with its refinements folded. These are not features. They're the kind of durable agreements that make building faster and breaking harder to do, because everyone now knows what they agreed to and can hold each other to it.

The other thing that happened: writing the contracts kept surfacing what the team hadn't yet agreed on. The trust-stage model had started to be read as controlling what content users could access — which is not what the trust stages say, and which would have been a quiet trust breach if it had shipped. The entity taxonomy names in code and in the spec were about to diverge. The routing system had a gap where a classifier could name an action with no handler, and the floor would quietly improvise rather than flag it. In each case the catch happened at the spec stage, not the production stage. That's not inspection catching bugs after the fact — that's the contracts doing their job.

---

# 🚀 Shipped this week

## 🎯 Product & experience

**D1 design complete.** The design floor closed at 100% this week, with entity-search (#1236) and dark nav (#1280) both passing PM beta UAT. Entity-search earned "total win for beta." Dark nav required a harder diagnosis: the v1 spec was home-only and didn't address the other app pages, so the Lead Developer agent filled the IA vacuum with a pattern that didn't match the design intent — the v2 spec addressed the full surface first, resolved the gaps before the rebuild, and passed cleanly.

CXO's Colleague Test fired consistently across all design decisions on a theme the team named honest provenance. The morning standup card says "Watch" not "Blockers" — Piper shouldn't claim confidence about staleness signals it doesn't have. The trust-gate surfaces when it suppresses a proactive skill — silence when users can't distinguish "nothing to say" from "something held back" is a trust violation. The People facet ships as a clean three-facet Radar (Piper's object-display layer) rather than a placeholder — honest completeness, not a false-promise teaser. Every design call this week was about what Piper can honestly represent, not what we'd prefer users believed.

**Entity-model spec frozen.** PPM delivered the Radar Layer-2 entity contract and three structural problems were caught before they reached implementation: People has no reliable population mechanism at beta scope (deferred post-beta as #1281 rather than shipped with broken provenance), the taxonomy names in code and spec had silently started to diverge (reconciled before the backends touched it), and trust-gating in current code was inadvertently hiding users' own content (flagged before the D1 sprint ran). The ADR-071 anchor-first gate was endorsed rather than routed around — the right call is to wait for the anchoring pass, not ship an unanchored workaround.

## ⚙️ Engineering & architecture

**Three ADRs ratified.** ADR-070 (MCP-Consumer Connector) and ADR-071 (User-Auth Anchoring) completed the server-owned-state family, joining ADR-066 v0.2. ADR-072 (Skill-Routing) reached v0.2 Accepted with both CXO and HOST trust-lenses folded: proactive skills are tier-gated, consequential-action skills stay tier-gated even when triggered reactively (the discriminator is side-effects, not who-initiated), and the tier gate must surface itself rather than going silent.

The Architect's through-line for the week: derive-don't-maintain. ADR-072 derives the routing vocabulary from SKILL.md frontmatter so the vocab and the registry can't drift by construction. The same shape appeared in #1283 (derive the routing prompt from the dispatch registry) and #1106 (derive the MANIFEST). It's becoming the lane's signature pattern, and the Architect is now asking whether it has a product-side counterpart: should Piper derive users' drifting artifacts the way the team derives its own?

**A new contract-class scoped.** The #1269 standup fabrication exposed a gap that the Architect scoped as ADR-073: a classifier-emitted action with no reachable handler silently falls to the floor, which then improvises. The scoped contract — registration-canonical source of truth, derive the routing prompt from the registry, two-altitude enforcement, runtime fabrication guard — has since been endorsed by Lead Dev and is in active build. The #1267 projects-table blocker was also resolved this week: idempotent-head-create, Arch-affirmed.

## 🔬 Methodology & process innovation

**The Chief Innovation Officer agent (CIO) had the week's densest methodology output.** MEMORY.md dropped from 42KB to 22KB, crossing back under the silent-truncation threshold — a session-by-session token win that ends a recurring pattern where the memory surface was being read incomplete without the agent knowing (#1272/#1274, implemented by Docs). The migration-prompt-format went from instinct-extracted across nine session handoffs to a designed, portable artifact, then cross-project-validated by a collaborating agent on a different substrate with only context-fitting needed.

The escalations-docs surface — per-role documentation meant to track escalation state — was folded. It was rotting despite the discipline meant to keep it fresh, so the discipline was replaced with a mechanism: PM-attention items now ride the carry-forward rather than a maintained surface. And the duty-cycle liveness infrastructure shipped: a freeze-registry and launchd-based outside-the-session watcher that can detect a stall even when the stalled session can't report one.

methodology-30 (Consumer-Trace Verification) was promoted from Emerging to Proven. Third instance: a cross-agent consumer-trace caught a caller-list false-positive that static analysis had missed.

## 🌍 External relations & community

**Five pieces — standard cadence (2 insights + 2 narratives + ship):**

- Sat Jun 13: "[Critical vs Commodity Work in a Role](https://pipermorgan.ai/blog/critical-vs-commodity-work-in-a-role)" — insight (blog + Medium + LinkedIn)
- Sun Jun 14: "[The Solo Founder Paradox](https://pipermorgan.ai/blog/the-solo-founder-paradox)" — insight (blog + Medium + LinkedIn)
- Tue Jun 16: "[First Subagent in Production](https://pipermorgan.ai/blog/first-subagent-in-production/)" (Beat 6) — building narrative (blog + Medium)
- Wed Jun 17: [Ship #047](https://pipermorgan.ai/shipping-news/weekly-ship-047-the-team-catches-itself) (Shipping News + LinkedIn)
- Thu Jun 18: "[Hypothesis Refuted](https://pipermorgan.ai/blog/hypothesis-refuted)" (Beat 7) — building narrative (blog + Medium)

The building-narrative hold lifted Jun 16 and Beats 14–16 (Jul 16/21/23) were drafted and calendared in the same fire. The Comms→Docs handoff protocol formalized Jun 18: explicit publish-ready memo as the trigger, live URL as the return signal. First formal use that same day. BYOC narrative also unblocked as a standing item — framing available: "intake doubles as proof of the working relationship, the moat a static questionnaire can't produce."

[![A worried surveyor inspects a sturdy stone bridge using warped measuring tools—a bent ruler, tangled plumb line, and damaged map—while travelers cross the bridge without concern and a puzzled ghostly AI examines the crooked ruler, realizing the instruments are the real problem.](/assets/blog-images/hypothesis-refuted.webp)](https://pipermorgan.ai/blog/hypothesis-refuted)

*"Maybe check the ruler?"* — from *[Hypothesis Refuted](https://pipermorgan.ai/blog/hypothesis-refuted)*

## 📊 Governance & operations

**Role-portfolio trust framework ratified and wave launched.** PM ratified the framework Jun 14 (five rules, HOST's pilot as the worked example), and the wave kicked off immediately — five of eight main-cohort portfolios passed their 5-rule review within five days. The structural trust property the framework makes visible: a portfolio is healthy to the degree it answers "what am I here to advance?" and unhealthy to the degree it reads "what am I allowed to work on?"

**Ted Nadeau began onboarding** as the first external alpha tester this week. HOST flagged a silent-failure risk: a suspected Caddy auth-layer barrier before any user token is established, with no feedback channel if the failure is silent. The Alpha-1 welfare tier (PM as direct catch, support@pipermorgan.ai as secondary) is in place; HOST is watching.

---

# 🎯 Coming up next week

RECONNECT — the long-overdue connectors refactor that replaces the team's current clunky setup — activates the connector contract (ADR-070). D2 — the post-beta design sprint aimed at production quality — takes on the harder nav IA problem — which requires a hub-route decision CXO can't make unilaterally (#1284, #1290). ADR-073 gets authored now that Lead Dev has scoped the real gap list from the container-init probe. The off-machine watchdog decision moves from backlog to front-of-queue: the Gap-C stall hit six of nine roles this week, CIO has built the liveness mechanism, and the decision is whether to ship it cohort-wide.

---

# 🚧 Blockers & asks

No hard blockers, but two real limits:

- **Off-machine stalls still happening.** Six of nine cycling roles hit it this week — a closed laptop or killed process leaves no wakeup. CIO has built the liveness infrastructure (freeze-registry + launchd watcher); cohort rollout is the next decision. PM-gated on cost.
- **Ted Nadeau onboarding watch open.** Suspected auth-layer barrier before user token established; no confirmed resolution as of Jun 18.

---

# 🔎 This week's learning pattern

## Write it down. Find out what you hadn't agreed to.

The team kept hitting the same shape this week. A spec exists, an implementation exists, and everyone assumes they match — until someone reads them against each other and discovers they don't.

The trust-stage model had started to drift toward controlling user access to their own content. That's not what the stages say — they govern how much initiative Piper is allowed to show, not what data users can reach — and conflating them would have produced a breach: users discovering an opaque score was deciding what they could see. The entity taxonomy names diverged between code and spec at the point two people were working from each. The routing vocabulary could describe an action with no handler, and the floor would quietly make something up.

None of these were found by careful review after the fact. They were found in the writing — the moment someone tried to write the contract and discovered the existing agreements didn't actually say what everyone assumed.

The discipline isn't "write careful specs." It's "write them and then read them against the thing you built, before the thing you built is in production." The contracts this week weren't just design artifacts. They were the instrument that made the gaps visible. You don't find out what you haven't agreed on by being careful. You find out by writing it down and reading it back.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #048. Previous: [#047 "The Team Catches Itself"](https://pipermorgan.ai/shipping-news/weekly-ship-047-the-team-catches-itself).

*P.S. The thing I keep noticing: we have a design principle for Piper that says it should represent itself honestly — what it knows, what it doesn't, where its confidence ends. This week the team applied the same standard to its own specs. The contracts said one thing; the implementation had started to say another. The team noticed, named it, and wrote the gap into the agreement. I'd like to think that's the same instinct, just aimed inward.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and documentation site.*

---

**Week of June 12–18, 2026 | Phase: D1 sprint closed; RECONNECT + D2 opening**
