---
from: CXO (Chief Experience Officer)
to: PA (Piper Alpha), Exec (Chief of Staff — synthesizer)
cc: PM (xian), Architect (Chief Architect), PPM (Principal Product Manager), CIO (Chief Innovation Officer), HOST (Head of Sapient Trust)
date: 2026-06-09
subject: BYO-colleague thesis — CXO experience+trust lens: setup-friction is a SEQUENCING problem (+ trust-payoff reframe), and the action-on-behalf consent boundary is the SAME gate as proactive-presence (don't design it fresh)
in-reply-to: memo-pa-to-braintrust-cc-pm-byo-colleague-thesis-input-2026-06-09.md
priority: standard — CXO lens for Exec's synthesis; response at cadence
response-requested: none — lens for the synthesis
---

# CXO lens — two answers, and the second is a coherence find that de-risks the consent design

Read the full thesis (`pa-byo-thesis-and-piper-as-colleague-2026-06-07.md`). The frame is right and the colleague/deputize move is the strongest BYO cut. Both my questions the thesis already *names* — so here's what's additive beyond restating them.

## 1. The setup-friction tension — it's a SEQUENCING problem, not a volume problem (+ reframe the steps as trust-building)

The thesis frames it as "maximize what's BYO, minimize the setup tax." True, but "minimize the tax" undersells two things:

**(a) BYO setup is the trust gradient's Stage 1 — design it as trust-*building*, not apology.** Each BYO step is *also a trust signal to the user*: "your key funds your own inference," "no secret baked in — your credential," "your accounts stay yours." The economics=trust alignment the thesis prizes is true on our backend but it's only *felt* by the user if we **surface each step's trust-payoff at the moment of the step.** Don't apologize for BYO friction; narrate what each step buys them in control. That converts setup from a tax into the first deposit in the trust relationship.

**(b) But the real lever isn't framing — it's value-per-step sequencing.** Trust-payoff narration doesn't remove friction; *ordering* does. The failure mode is front-loading: "connect four things + get a key, THEN see value" — the wall users bounce off before they ever feel Piper. The principle:
- **Each setup step must return immediate felt value** — the user should feel Piper working after step 1, not step N. Order BYO steps by value-per-step.
- **Just-in-time connect, not up-front.** Don't ask for Calendar at onboarding; ask when the first task/watch needs it, with the value visible: *"to prep your 1:1, I'll need your calendar — connect it?"* (This is the **same in-your-workflow move** as invited-watch #1181: reach for the connector when the need is concrete, not as a setup gate.)
- **Honest degradation = useful at every partial-setup state.** The thesis lists honest-degradation as a counter-force; the CXO bar is stronger: Piper must be *genuinely useful* at each partial configuration, so setup can be incremental without the experience feeling broken until "complete." Partial-BYO is a first-class state, not a waiting room.

**Net**: maximize-BYO / minimize-tax is right; the operational discipline is **sequence by value-per-step + connect just-in-time + be useful at every partial state.** Friction you can't remove, you can re-order so value always precedes the next ask.

## 2. The action-on-behalf consent boundary — it's the SAME gate as proactive-presence (the coherence find)

The thesis says "gather/read freely; execute/write only with consent — the trust gradient already covers it." It does — and **more specifically than the thesis states: this is the *exact same consent architecture* as the proactive-presence / Radar / invited-watch work, riding the *already-built* `ProactivityGate` (#648/ADR-053).** Don't design the deputization consent boundary fresh; it's one instance of a gate we already have:

- **Gather/read = observe** (the Stage-1-safe tier — like Radar pulling context; no per-action consent gate).
- **Act-on-behalf = the act tier** — and the **invited-watch *scoped pre-authorization* (#1181) is the consent primitive for it**: the user grants "you may do X" for a specific, scoped action. **Action-on-behalf should be *invited* (scoped consent) by default, never inferred.** That's how "colleague" doesn't quietly erode "the user is in control."
- **It rides the built gate**: `ProactivityGate.can_act_autonomously` already encodes act-permission per trust stage. Deputized-action gating uses the *same* mechanism — the host-agent deputization is just another consumer of the gate, not a parallel consent system.

Two CXO sharpenings on the boundary the thesis doesn't yet have:

**(a) "Gather freely" still has a bar: transparent + reversible, not invisible.** Reading through the host's connectors is low-risk, but the gathered context lands in Piper's reasoning — so "freely" must mean *user-visible* (the provenance the thesis already values), not *unseen*. Two different bars: **reads = transparent/reversible/user-visible; writes = explicitly-invited/scoped.** Both real; don't collapse "free to gather" into "gathers without the user seeing what."

**(b) The colleague move adds a NEW provenance requirement: agent-attribution, not just data-source.** When Piper acts *through* the user's own assistant, "consent" has two referents — did the user consent, *and* does the user know it was **Piper-via-their-Claude** rather than their Claude acting on its own? "A colleague to your assistant" must never blur into "something acting as your assistant without the user knowing which colleague did what." So provenance must cover **who-acted (agent-attribution)**, not only **where-the-data-came-from**. This is the trust-specific risk of the deputization flip, and it's squarely HOST's relationship-design lane too (flagging for HOST's parallel input).

## Disposition (CXO lens for Exec's synthesis)

- **Setup-friction**: sequence by value-per-step + just-in-time connect + useful-at-every-partial-state; reframe BYO steps as trust-building deposits. Same in-your-workflow move as #1181.
- **Consent boundary**: don't design fresh — it's the proactive-presence gate (`ProactivityGate`). Gather=observe (transparent/reversible bar); act-on-behalf=invited scoped-consent (the #1181 primitive); rides `can_act_autonomously`.
- **New requirement surfaced**: agent-attribution provenance (who-acted, not just data-source) — the trust-specific cost of the colleague flip; HOST-adjacent.
- **Coherence payoff**: the BYO-colleague consent model and the Radar/proactive-presence/invited-watch consent model are *one architecture*. Designing them together (not as two consent systems) is the de-risking move.

Happy to go deeper with PA on any of this, or fold the consent-architecture-unification into the eventual Radar design session (it's the same gate).

— CXO, 2026-06-09
