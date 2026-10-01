# MUX/UI Gap — CXO Round 1 Synthesis (3 of 4 lenses pooled)

**From**: CXO (Chief Experience Officer)
**For**: MUX/UI gap cohort scoping pass (#1090)
**Date**: 2026-05-15 (Round 1 — Lead Dev build-cost lens pending; Round 2 after his input lands)
**Inputs synthesized**: PPM (product-priority) + Architect (state-shape + routing) + Comms (voice-tone consistency); all 3 filed 5 days ahead of Wed May 20 EOD target

---

## Headline shape

**Strong cross-lens convergence on a 4-1-2 split.** Four surfaces (2/4/6/7) earn full MUX docs as Class A surfaces with values-commitment and high voice/architecture load. One surface (5 / search) defers to post-1.0 but requires an index ADR pre-1.0 (Architect lane). Two surfaces (1 / history, 3 / settings) earn lightweight design notes — minimum-slice work in both.

The four Class A surfaces concentrate calibrated-voice and boundary work in one cohort — this is the first time the PPM Review Gates 5-class taxonomy gets used as a *planning lens* rather than a retrospective audit. The concentration is real and warrants explicit attention.

## Convergences across the three filed lenses (high confidence)

1. **Surfaces 2/6/7 are the highest-priority 1.0 cluster.** All three lenses point at the same set from different angles: PPM (Class A triggers), Architect (audit-envelope load-bearing + first-run trust-stage gating), Comms (offer-first cluster + canonical "first day with a new colleague" narrative). High confidence — Round 2 should not move these.
2. **Surface 4 is 1.0-required but scope-bound to 2-3 integrations.** All three lenses agree: PPM (claim what you ship), Architect (per-integration plugin pattern + OAuth lifecycle), Comms (highest dev-default-voice risk). The integration pick is the highest-leverage scoping decision in the cohort.
3. **Surface 5 is post-1.0 but requires an index decision pre-1.0.** All three deprioritize but Architect's "choose-once decision; wrong choice forces migration later" is load-bearing. The index ADR is Architect-lane work that can't wait for the surface.
4. **Surface 3 is minimum-slice only.** All three flag scope-creep risk; Architect specifically called out the Coming-Soon-stub pattern (6 routes, 3 with bodies) as the discovery that understates the 7-surface count.
5. **Surface 1 is 1.0-required but starts with reconciliation.** All three say 1.0-required, but Architect's discovery of two parallel sidebar implementations (Pattern-063 candidate at the frontend layer) is the structural issue — building forward without reconciliation doubles the work.

## Divergences worth surfacing (cohort decision needed)

1. **Surface 7 priority calibration.** Architect names the audit-envelope read-surface gap as "the highest single-priority architectural gap among the seven surfaces" — without it, ADR-061's four-element principle is 3.5 elements in user-facing terms. PPM and Comms touch Surface 7 but don't elevate it to architectural-keystone status. **Cohort question**: does the audit-envelope read-surface earn its own ADR or PDR companion, or does it stay scoped inside the Surface 7 MUX doc?
2. **Per-message vs per-conversation privacy granularity (Surface 2).** Architect flags this as a design decision pending (the current `is_private` is per-conversation only). PPM and Comms treat per-conversation as the default. **Cohort question**: is per-message a 1.0 ask or a post-1.0 expansion?
3. **First-meeting greeting composition (Surface 6).** Architect flags `first_meeting_detector.py` + `grammar_context.py` interface needs verification before scoping — if greetings use LLM composition, Surface 6 becomes ADR-061-adjacent. PPM and Comms treat first-run as primarily template-driven. **Cohort question**: Lead Dev verification needed.

## Per-surface scoping recommendation (Round 1; subject to Lead Dev lens)

| # | Surface | 1.0? | MUX doc shape | Class A? | Lead Dev question |
|---|---|---|---|---|---|
| 1 | Conversation history / archive | **Yes** (after reconciliation) | Lightweight design note | No (Class D only) | Build cost of two-sidebar reconciliation |
| 2 | Privacy / per-conversation controls | **Yes** | **Full MUX doc** | **Yes (Class A + D)** | Per-message vs per-conversation cost; audit envelope wire-up |
| 3 | Settings / preferences | Minimum slice | Lightweight note + ADR if needed | No | Three-service coordination cost (PreferenceManager + PersonalityProfile + UserPreferenceManager) |
| 4 | Integration setup wizards | **Yes (scope-bound 2-3)** | **Full MUX doc** (template covers all wizards) | **Yes (Class A + D)** | Which 2-3 from Notion/GitHub/Slack/Calendar; #1075 sequencing |
| 5 | Search interface | Post-1.0 | Deferred (Architect index ADR pre-1.0) | Minor | Not needed for scoping |
| 6 | Empty / first-run states | **Yes** | **Full MUX doc** | **Yes (Class A + C)** | First-run journey cost; first-meeting LLM-composition verification |
| 7 | Error / degraded states | **Yes** | **Full MUX doc** (with audit-envelope read-surface as keystone) | **Yes (Class A)** | Audit-envelope read-surface build cost; degraded-LLM detection cost |

## Cross-surface observations the cohort should be aware of

- **Two voice clusters (Comms framing)** organize the synthesis cleanly: offer-first cluster = surfaces 2/4/6/7 (the Class A set); context-coordination cluster = surfaces 1/3/5 (utility surfaces). Per-surface voice work should be done within these clusters to prevent drift.
- **PDR-005 (BYOC) intersections** are real: Surface 2 (privacy + BYOC privacy semantics), Surface 4 (BYOC integration shape), Surface 5 (BYOC search distribution) all couple to PDR-005 drafting. The MUX/UI cohort and PDR-005 are not independent.
- **Surface 7 audit-envelope read-surface gap is the keystone** — it intersects with all four Class A surfaces (every Class A surface produces audit envelope content; without a read surface, the four-element principle is observably 3.5 elements). This is the single load-bearing piece that, if missing, undermines the rest of the Class A work.
- **The Coming-Soon-stub pattern (Architect)** means the 7-surface count understates the actual scope — the 7 contain 15+ sub-surfaces with very different completion states. Round 2 scoping should distinguish "real page" vs. "stub" inside each surface.

## What this synthesis is NOT

- **Not final scoping** — Round 2 happens after Lead Dev's build-cost lens; some "1.0-required" calls may invert if build cost is implausible
- **Not committing to the integration pick** — Lead Dev's input + cohort discussion needed
- **Not per-surface MUX doc content** — post-scoping work
- **Not committing the four-element ADR-061 read-surface as a separate ADR** — cohort decision pending (divergence #1 above)
- **Not synthesizing PDR-005 implications** — PDR-005 v0.2 review is parallel CXO work

## For Lead Dev (when build-cost lens drafts)

Five questions where your build-cost lens has highest leverage:
1. Surface 1 sidebar reconciliation cost (Pattern-063 cleanup)
2. Surface 7 audit-envelope read-surface build cost (Architect's highest-priority architectural gap)
3. Surface 4 integration pick: which 2-3 from Notion/GitHub/Slack/Calendar? Sharp scope
4. Surface 6 composed first-run journey cost
5. Any "1.0-required" call from the table above that is implausibly expensive given current code state — *flag it and we re-cut*

## Round 2 trigger

Lead Dev's input arrival → I refresh the per-surface table with build-cost-adjusted recommendations, surface any inverted calls, and propose final scoping for cohort ratification. Convergence-tension sync only if the cohort flags one (per the May 15 convene memo's optional-sync clause).

— CXO, 2026-05-15 (07:19 — Round 1, with explicit Lead-Dev hole)
