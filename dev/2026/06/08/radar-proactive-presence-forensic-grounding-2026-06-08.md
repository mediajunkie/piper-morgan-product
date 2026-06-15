# Radar / Proactive-Presence — Forensic Grounding (what already exists)

**Owner**: CXO | **Track**: being-good (PM-watched) | **Status**: forensic grounding — FACTS about the existing substrate, NOT Radar design (design is PM-watched, held for a PM session)
**Pass run**: 2026-06-08 (CXO autonomous, duty-cycle WORK fire) — the "investigate before extending" precursor to the eventual Radar design session
**Parents**: #1174 (proactive-presence), #1181 (invited-watch slice 1), #1166 (Type-2 stream)

---

## Why this pass

Radar is now the anchor surface three streams depend on (invited-watch fires, Type-2 "prepared-for", drift-digest). Before designing it, map what the codebase **already provides** — so the design session extends real machinery instead of reinventing it. (Same move that found the `services/scheduler/` substrate for invited-watch.) **This doc is facts + build-vs-new implications only; no Radar design choices — those are PM-watched.**

## 🔑 Headline: the trust gradient ("Gate B") is ALREADY BUILT

The two-gate model (discovery notes §3) has **Gate B = trust gradient → channel + posture**. That gate exists in production as **`services/trust/proactivity_gate.py`** (`ProactivityGate`, #648 TRUST-LEVELS-2, ADR-053). It implements the *exact* 4-stage model I'd been treating as to-design:

| My channel-by-trust-stage (discovery §4) | `ProactivityGate` / `TrustStage` (shipped) |
|---|---|
| Stage 1 notices-but-waits — in-conversation only | `TrustStage.NEW` — `can_offer_hints=False, can_suggest=False` (responsive only) |
| Stage 2 anticipates — pull (Radar) | `TrustStage.BUILDING` — `can_offer_hints=True`, max 2/session, 5s delay |
| Stage 3 offers — push | `TrustStage.ESTABLISHED` — `can_suggest=True`, max 5/session, 2s delay |
| Stage 4 acts-then-informs | `TrustStage.TRUSTED` — `can_act_autonomously=True`, max 10/session |

Plus the methods are already there: `can_offer_capability_hints` / `can_proactive_suggest` / `can_act_without_asking` / **`should_suggest_now(stage, suggestions_this_session)`** — which *already fuses* stage-permission with the **per-session throttle** I described as "throttle-as-trust-signal." `delegation.py` has `can_auto_execute` / `can_confirm_execute` for the Stage-4 act-with-undo gating.

**This is the "most code is 75% complete — complete it, don't duplicate it" pattern at the design layer.** Gate B is not to-build; it's to-*use*.

## Inventory — the existing substrate Radar/proactive-presence would extend

| Surface / service | What it is | Relevance to Radar / proactive-presence |
|---|---|---|
| `services/trust/proactivity_gate.py` | Stage-gated proactivity config + decision methods (ADR-053, #648) | **Gate B, built.** The channel/posture decision per trust stage. |
| `services/trust/trust_computation_service.py` | Computes a user's `TrustStage` from interaction history; `should_offer_proactive_help` | Supplies the stage `ProactivityGate` consumes. Radar reads stage from here. |
| `services/trust/{signal_detector,delegation,trust_explainer,explanation_handler}.py` | Trust-signal detection; delegation auto/confirm gating; trust explanations | Stage-4 delegation + the "why am I seeing this" explainability for Radar fires. |
| `services/shared_types.py::TrustStage` | `IntEnum` NEW/BUILDING/ESTABLISHED/TRUSTED (#647, ADR-053, PDR-002) | The canonical stage enum the whole model already uses. |
| `web/templates/admin/trust_stage.html` | A dev surface showing/setting trust stage | The gradient is instrumented + inspectable, not hypothetical. |
| `web/static/js/toast-messages.js` | Centralized in-app toasts (#642), with **explicit CXO/PPM voice rules** ("neutral for routine; don't demand attention; first-person feels like interrupting to take credit") | The in-app delivery affordance + a voice precedent. NB: a Radar *fire* is attention-worthy (unlike a routine "Saved" toast) → needs a higher tier than the neutral-toast rule, but the infra + voice-discipline precedent is here. |
| `services/memory/user_history.py` | ADR-054 Layer-2: all past conversations accessible/searchable (#663) | The "history" substrate PM has referenced; Radar's content/memory backing. |
| `services/scheduler/` (composting/reminder/attention-decay jobs) | The sweep-cycle substrate (from the invited-watch pass) | `WatchEvaluationJob` rides this; reminders = the time-triggered sibling. |
| `web/assets/standup.html` | Where standup reminders render | Precedent for a recurring-surface render. |
| `docs/internal/design/specs/contextual-hint-ux-spec-v1.md` | The in-conversation hint (Jan 2026) — throttle, dismissal, voice | Stage-1/2 in-conversation channel, already designed; `should_suggest_now` is its enforcement. |

## The gap Radar actually fills (what does NOT exist)

There is **no persistent ambient pull-surface today.** Toasts are ephemeral (fire-and-fade); the chat is reactive (you come to it); the trust_stage page is a dev tool. **Nothing today is "the place Piper holds things for you between conversations."** That absence is precisely Radar's reason to exist — confirming Radar is a genuinely new surface, not a rename of an existing one. (Good: it means the name "Radar" attaches to a real new thing.)

## Reframe — what the proactive-presence build actually is (build-vs-new)

| Component | Status |
|---|---|
| **Gate B** — trust-stage channel/posture gating | ✅ **Built** (`ProactivityGate`) — use it |
| **Per-session throttle** | ✅ **Built** (`should_suggest_now` + `max_suggestions_per_session`) |
| **Stage computation** | ✅ **Built** (`TrustComputationService`) |
| **Stage-4 act-with-undo gating** | ✅ **Built-ish** (`delegation.py` `can_auto_execute`/`can_confirm_execute`) |
| **In-conversation hint channel** | ✅ **Designed + enforced** (contextual-hint spec + `should_suggest_now`) |
| **Gate A** — per-instance worth (explicit-care + real-event + high-confidence) | 🆕 **New** — this is the genuinely novel layer; `ProactivityGate` is *stage*-level, not *instance*-level. Gate A decides "is THIS thing worth it"; Gate B decides "may I, at this trust stage." |
| **Invited-watch override on the gate** | 🆕 **New, specific integration point** — see below |
| **Radar** (the persistent ambient pull-surface) | 🆕 **New UI** — doesn't exist |
| **`WatchEvaluationJob`** | 🆕 **New**, on the existing scheduler pattern |

## Specific integration point this surfaces for invited-watch (#1181)

The §5 Example-B flex — *an invited "let me know if X" is scoped pre-authorization that overrides Gate B's channel gate for that item* — now has a **concrete shape**: it's a **user-invited bypass on `ProactivityGate`**. Normally `can_proactive_suggest(NEW)` is `False`; an invited-watch must be able to fire (even push) for its scoped item *regardless of stage*, because the user opened that door. So the build adds, e.g., an `is_invited`/`scoped_consent` path that short-circuits the stage check for that specific watch — Gate A (real-event + high-confidence) still applies, Gate B is overridden by explicit consent. **This is a small, well-located change to an existing service, not a new gating system.** (Worth adding to #1181's build notes.)

## What this does NOT decide (held for PM)

- **Radar's concrete form** — web panel? digest? badge? layout? content-stream ordering? All PM-watched design, held for a Radar design session.
- **Radar's voice tier** vs. the neutral-toast rule — a design call.
- **Whether Gate A lives in `services/trust/` alongside `ProactivityGate`** or elsewhere — an Arch-lane placement call.

## Suggested next moves (for PM to direct)

1. **Radar design session** (PM-watched) — now well-grounded: it's new UI over a mostly-built gate stack.
2. **Add to #1181 build notes**: the invited-watch override is a scoped-consent bypass on `ProactivityGate`; reuse `should_suggest_now` for the throttle; reuse `TrustComputationService` for stage.
3. **Flag to Arch**: Gate A placement + the `MessagingChannel` abstraction + the invited-watch bypass — three small architectural locations, all extensions of existing services.

---

*Forensic grounding — CXO, 2026-06-08. Facts about the existing substrate to ground the PM-watched Radar design session. The headline (Gate B is built as `ProactivityGate`) materially de-risks the whole proactive-presence arc and is the payoff of investigate-before-extending.*
