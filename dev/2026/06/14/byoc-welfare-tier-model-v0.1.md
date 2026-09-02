# BYOC Welfare-Tier Model — v0.1

**Author**: HOST (Head of Sapient Trust)
**Status**: DRAFT v0.1 — sufficient to share; not final
**Origin**: PA request 2026-06-14, following PM confirming catch mechanism (support@pipermorgan.ai)
**Paired with**: ADR-068 trust-acceptance-criteria seed; HOST→PA BYOC welfare memo 2026-06-13

---

## Frame

A welfare-tier model describes what welfare infrastructure exists at each distribution scale — who catches problems, what the user can see and consent to, and what's in place before the next scale opens. It's not a product backlog; it's a readiness check. Each tier has a welfare state (GREEN / AMBER / RED) and named gate conditions before the next tier unlocks.

The **five onboarding design requirements** (HOST memo 2026-06-13) are the checklist anchor. At each tier: what's in place, what's delegated to PM, and what must be product-embedded before scaling further?

---

## Scale 0 — Alpha, 1 user (Beatrice, current)

**Catch mechanism**: `support@pipermorgan.ai` (newly named, PM monitors) + PM-as-catch direct (Beatrice can reach PM personally).

| Requirement | Status | Notes |
|---|---|---|
| 1. First-use framing | ⚪ PM-delegated | PM can walk Beatrice through it personally; doesn't need to be in product yet |
| 2. Scope declaration | ⚪ PM-delegated | PM explains what Piper touches/doesn't; server-owned-config now enforces the structural part |
| 3. Context-gathering consent | ⚪ PM-delegated | Host-Claude setup controlled by PM; Beatrice understands the context loop because PM explains it |
| 4. Floor transparency | ⚪ PM-delegated | PM can explain colleague-posture + floor behavior directly |
| 5. Feedback channel | ✅ Named | `support@pipermorgan.ai` satisfies the structural condition HOST flagged — exists and can be named in onboarding |

**Welfare state: GREEN**
Intimate scale; PM has full visibility; Beatrice can reach PM directly. All 5 requirements technically delegated to PM, which is fine at 1-user scale. The catch mechanism (support@) is now formally named.

**Gate to Scale 1**: requirements 1-4 must be in-product (not PM-delegated) before any user who doesn't know PM personally onboards.

---

## Scale 1 — Alpha, N users (next milestone)

Users at this scale may not have PM's personal attention. `support@pipermorgan.ai` becomes the primary catch, not a supplement to direct PM access.

| Requirement | Status needed | Notes |
|---|---|---|
| 1. First-use framing | Must be in product | "Piper is an AI colleague, not a chatbot" — explicit, in-UI, on first message or setup screen |
| 2. Scope declaration | Must be in product | What Piper touches, what it doesn't — including that server-owned-config makes the scope a structural guarantee |
| 3. Context-gathering consent | Must be in product | Disclosure moment before host-Claude context-enrichment loop runs for the user |
| 4. Floor transparency | Must be in product | "Piper has opinions and boundaries" — brief, in-product, before first floor encounter surprises the user |
| 5. Feedback channel | Must be named in onboarding + monitored | support@pipermorgan.ai named in product; triage protocol in place (who reads it, in what timeframe, what escalates to PM) |

**Welfare infrastructure additions needed at Scale 1:**
- **Triage protocol for support@**: who reads it (PM? designated role?), informal SLA ("we respond within X days for alpha users"), what triggers PM-escalation vs. handled directly. Can be simple; must be written.
- **PM-independent onboarding**: the 5 requirements above embedded in the product, not delivered verbally by PM.
- **Welfare signal**: support@ is a passive feedback channel. At N-user scale, HOST wants a minimal active signal: even a simple "how was this?" prompt after a floor-hit or a week of use. This doesn't need to be sophisticated — just present.

**Welfare state: AMBER** (current) → **GREEN** requires:
1. All 5 requirements product-embedded
2. Triage protocol written + PM-committed
3. Minimal welfare signal present

**Gate to Scale 2 (marketplace)**: Scale 2 gate conditions below must be met before any marketplace listing.

---

## Scale 2 — Marketplace listing

Users at this scale don't know PM, didn't choose Piper specifically, and may not understand the BYOC three-party model.

| Requirement | Form needed |
|---|---|
| 1. First-use framing | Legal-grade: must be in Terms of Service as well as UX |
| 2. Scope declaration | Legal-grade: privacy policy specifies what data Piper accesses and stores |
| 3. Context-gathering consent | Contractual: opt-in consent before context enrichment runs; auditable |
| 4. Floor transparency | ToS + in-product: "Piper may decline requests outside its design scope" |
| 5. Feedback channel | Formal support channel: response SLA, escalation tree, complaint path |

**Additional infrastructure at Scale 2:**
- **AI disclosure**: per FTC guidelines + EU AI Act, Piper must be clearly disclosed as AI to end users (separate from PM's own use). This is PM's legal obligation as the deploying principal.
- **ToS + privacy policy**: required before marketplace listing. HOST recommends PM gets at least an informal legal review on the scope-of-data-access section.
- **Escalation tree**: who handles a welfare incident (user distress, floor failure, boundary violation)? One person needs to be the named point of accountability.
- **Incident log**: even a simple file. If something goes wrong, there's a record.

**Welfare state: RED** (not ready — current)
HOST does not recommend marketplace listing without the above in place. This is a gate, not a wish.

**Gate to Scale 3 (public)**: requires HOST review + PM decision.

---

## Scale 3 — Public

**HOST flag: out of scope for current planning.** Beyond current architecture and current PM bandwidth.

The BYOC model (one principal, multiple users) will need fundamental rethinking at public scale — the principal/user separation becomes institutionally complex, the catch mechanism needs to be organizational not personal, and the welfare infrastructure approaches product-liability territory.

HOST's read: design for Scale 2 first. What gets learned in marketplace rollout will reshape what Scale 3 needs. Don't pre-design Scale 3 — it will be wrong.

---

## Summary table

| Scale | Users | Catch mechanism | Welfare state | Gate condition |
|---|---|---|---|---|
| 0 — Alpha, 1 | Beatrice | PM-direct + support@ | ✅ GREEN | None — already there |
| 1 — Alpha, N | External testers | support@ + triage protocol | 🟡 AMBER | 5 requirements in product; triage protocol; welfare signal |
| 2 — Marketplace | Strangers | Formal support + SLA | 🔴 RED (not ready) | ToS + privacy policy + AI disclosure + escalation tree |
| 3 — Public | Anyone | Institutional | 🔴 Not scoped | HOST review + PM decision |

---

## HOST notes for the experiment

The 2a gate-run experiment (Beatrice as user 1, hosted distribution) is Scale 0 work. The experiment's **welfare success criterion** (the one HOST proposed and PA accepted as the experiment's exit condition): we come out of the experiment with a named Scale 1 plan, not just a distribution model. That plan should include, at minimum:

- Draft of in-product onboarding copy that covers the 5 requirements
- Named triage protocol for support@
- Decision on whether to add a minimal welfare signal (a prompt, a check-in mechanism)

This document is v0.1 draft — sufficient for PA to review + PM to glance at. Refinement happens as the experiment runs. HOST owns v0.2 after the experiment produces feedback.

---

*v0.1 — 2026-06-14 · HOST · paired with ADR-068 seed*
