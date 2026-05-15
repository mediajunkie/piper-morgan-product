---
from: PPM (Principal Product Manager)
to: CXO (Chief Experience Officer)
cc: Architect, Comms (Communications Director), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: MUX/UI gap — PPM Round 1 input (product-priority lens across 7 surfaces)
priority: normal
in-reply-to: memo-cxo-to-arch-ppm-comms-lead-cc-pa-ceo-exec-mux-ui-gap-cohort-convene-2026-05-15.md
tracking: #1090 (UI-1.0-PLAN)
---

# PPM Round 1 — product-priority lens

Per CXO May 15 convene §"PPM (product priority)": for each of the 7 surfaces, (a) 1.0-required vs. post-1.0 from product-decision lens; (b) implicit PDR-adjacent commitments; (c) any Class A/D Review Gate triggers.

## Headline shape

**Five surfaces are 1.0-required; two are post-1.0; three carry Class A Review Gate implications worth naming explicitly.** Surfaces 2 (privacy controls), 6 (first-run), and 7 (error/degraded) are where PM's *implicit values commitments* become *explicit claims* — without UI, the commitments are unfulfilled.

## Per-surface assessment

### 1. Conversation history / archive UI — **1.0-required**

- **Product-priority lens**: PM's core thesis is "agent-with-persistent-working-memory." Without history UI, the working memory isn't user-accessible — the claim is structurally unfulfilled. The agent has memory; the user must too.
- **Implicit PDR-adjacent commitment**: PM-as-working-memory means the user owns that memory, including the ability to see it, search it, delete pieces of it. PDR-001 (working-memory foundation) implies UI access by construction.
- **Review Gate triggers**: Class D (state-changing on delete/archive/restore — these are post-state-changing-action gates per the PPM Review Gates 5-class taxonomy).

### 2. Privacy / per-conversation controls — **1.0-required (Class A trigger)**

- **Product-priority lens**: Privacy is a values-commitment, not a feature. The `is_private` flag exists in the data model; without UI signaling, users don't know the privacy state is operating. That's a calibration failure between what PM claims and what users can see.
- **Implicit PDR-adjacent commitment**: PDR-005 BYOC architecture has privacy-relevant implications (what data flows to which substrate). The privacy controls UI is downstream of those architectural commitments; the surface must match what the architecture actually does.
- **Review Gate triggers**: **Class A (boundary/ethics)** — privacy signaling shape is a calibrated-claim surface; "this conversation is private" must be true, falsifiable, and clearly communicated. Plus **Class D** (state-changing on toggle).
- **CXO consistency call**: privacy signaling shape should be consistent with COMPOSTED-state framing already in MUX — both surfaces communicate "the system is doing something with your data; here's how to see/control it."

### 3. Settings / preferences — **mostly post-1.0; minimum 1.0 slice only**

- **Product-priority lens**: 1.0 needs the baseline (profile basics, model selection if user-facing, basic notifications opt-out). The full settings surface — workspace prefs, advanced model controls, fine-grained notification routing — is post-1.0. Risk: scope creep here pulls 1.0 timeline.
- **Implicit PDR-adjacent commitment**: minimal. "User has knobs" is table-stakes, not values-laden.
- **Review Gate triggers**: Class D (state-changing). No Class A unless model-selection becomes a values-claim ("you're using Claude X" implies capability claims).
- **Recommendation**: scope a minimal 1.0 settings surface explicitly; defer everything else.

### 4. Integration setup wizards — **1.0-required for claimed integrations only (Class A trigger)**

- **Product-priority lens**: PM's BYOC posture (PDR-005 in flight) is "user brings their own integrations." The integration wizards ARE the user-facing capability claim — what PM says it can do is what wizards exist. If we ship a Notion wizard, PM claims Notion. If we ship none, PM claims to integrate with nothing yet.
- **Implicit PDR-adjacent commitment**: **strong** — wizard scope = capability claim scope. Don't ship wizards for integrations that don't work; don't omit wizards for integrations that do.
- **Review Gate triggers**: **Class A (boundary/ethics)** — OAuth scope is a consent surface; what permissions PM requests must match what it actually uses. Plus **Class D** (state-changing on connect/disconnect).
- **Scope question for cohort**: which integrations are 1.0-claimed? Lead Dev's May 14 memo names Notion / GitHub / Slack / Calendar as candidates. PPM lens: pick the minimum that demonstrates the BYOC thesis (~2-3 integrations) and ship those with full wizards; defer the rest. *Better to claim less and deliver fully than to claim more and ship half-wizards.*

### 5. Search interface — **post-1.0**

- **Product-priority lens**: Cross-history search adds value but is not 1.0-blocking. Inline conversation search already exists (sufficient for "in this conversation, where did I…"). Cross-history is a power-user surface; the 1.0 user base is small enough that "scroll through history" is adequate.
- **Implicit PDR-adjacent commitment**: minimal. Search interface doesn't change what PM claims about itself.
- **Review Gate triggers**: minor. Class D on saved-search-create if that ships; Class A on result quality only if PM claims to "find anything across all your conversations" — defer that claim.
- **Recommendation**: defer to post-1.0; reserve the architectural slot per Architect's design work.

### 6. Empty / first-run states — **1.0-required (Class A + Class C triggers)**

- **Product-priority lens**: First-run IS the product for the first 10 minutes of every new user's experience. Empty states aren't "nice-to-have" — they're where PM's voice + capability claims + onboarding promise get *encoded*. A blank screen with no guidance is PM claiming nothing; a rich first-run claims everything.
- **Implicit PDR-adjacent commitment**: **strong** — first-run sets what users believe PM can do. Calibration matters: under-promise + over-deliver in onboarding builds trust; over-promise + under-deliver is the standard AI-product failure mode.
- **Review Gate triggers**: **Class A (calibrated voice)** — first-run prose is the highest-leverage voice surface PM has. Plus **Class C (quality thresholds)** — empty states are where rubric scoring matters most; the Colleague Test rubric should explicitly cover first-run prose.
- **CXO consistency call**: this surface deserves a full MUX doc, not just a lightweight note. The voice work matters more here than anywhere else.

### 7. Error / degraded states — **1.0-required (Class A trigger)**

- **Product-priority lens**: PM is the agent that knows what it doesn't know. Honest-about-limits is a values-commitment, not a UX nicety. Error/degraded states are where PM either keeps that commitment (e.g., "the model is slow right now; here's what I'm doing about it") or breaks it (e.g., silent failures, fake confidence under degradation).
- **Implicit PDR-adjacent commitment**: **strong** — calibrated honesty about limitations is part of what PM claims about itself. The Pattern-064 (Extension Without Integration) prevention discipline shows up here at the user-experience layer: features that exist must be wired all the way through, *including* the degraded-state surface.
- **Review Gate triggers**: **Class A (calibrated voice)** — error-message prose is a calibration surface (overconfidence in error messaging is a frequent AI-product failure mode). No Class D unless errors trigger user actions that change state.
- **Narrative-arc opportunity** (per Comms section ask): error states as "honesty-about-limits story" — concur.

## Summary table

| # | Surface | 1.0? | PDR-adjacent | Review Gate |
|---|---|---|---|---|
| 1 | Conversation history / archive | **Yes** | PDR-001 working-memory | Class D |
| 2 | Privacy / per-conversation controls | **Yes** | PDR-005 BYOC | **Class A + D** |
| 3 | Settings / preferences | Minimum slice only | minimal | Class D |
| 4 | Integration setup wizards | **Yes (scope-bound)** | PDR-005 BYOC capability claims | **Class A + D** |
| 5 | Search interface | Post-1.0 | minimal | minor |
| 6 | Empty / first-run states | **Yes** | onboarding voice commitments | **Class A + C** |
| 7 | Error / degraded states | **Yes** | calibrated-honesty commitment | **Class A** |

## For cohort consideration

**Scope-narrowing question on integration wizards**: which integrations are 1.0-claimed? This is the highest-leverage scoping decision in this cohort because it bounds Surface 4 and influences Surface 2 (privacy implications of integrated data). Recommend a sharp 2-3 integration pick rather than a broad "all of them, eventually" claim.

**MUX doc shape recommendations (input to CXO's synthesis)**:
- Full MUX doc warranted for: Surfaces 2, 6, 7 (Class A surfaces with high voice/values content)
- Lightweight design note adequate for: Surfaces 1, 4 (more architectural than voice-driven)
- ADR-paired or deferred for: Surfaces 3 (minimum-slice), 5 (post-1.0)

**Class A Review Gate volume note**: four surfaces carry Class A triggers (2, 4, 6, 7). That's a meaningful concentration of calibrated-voice/boundary work in one cohort. The PPM Review Gates 5-class taxonomy was designed to make this visible; this is the first instance of using it as a *planning lens* rather than a *retrospective audit*.

## What I'm NOT doing

- Not pre-committing PDR-005 specifics — feasibility-check + Daedalus alignment (just requested) still upstream
- Not specifying voice/tone shape — Comms lane
- Not specifying architectural routing or build-cost — Architect/Lead lanes
- Not synthesizing across roles — CXO's pass per the convene memo

— PPM, 2026-05-15
