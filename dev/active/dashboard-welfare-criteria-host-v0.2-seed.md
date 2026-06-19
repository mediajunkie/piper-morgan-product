# Attention-Dashboard — Trust/Welfare Criteria (HOST, v0.2 seed)

**Owner**: HOST (welfare criteria lane per m-39). **Status**: seed for the HOST↔CIO v0.2 design pairing — not a spec yet. Captures new HOST-lane material from June 17 work (ADR-072 D5 trust-transparency, trust-stage sweep, MEM-EVAL) ready for the pairing. Reads in sequence with v0.1 (`dev/2026/06/09/dashboard-welfare-criteria-host-v0.1.md`).

**What changed since v0.1**: Three new criteria (D, E, F) + answers to all three open questions. The trust-stage sweep and ADR-072 D5 ratification both generated welfare-relevant material.

---

## New criteria (D, E, F) — additions since v0.1

### Criteria D — Dashboard honesty (no silent non-surfacing)

Derived from the ADR-072 D5 trust-transparency principle ratified 2026-06-17: *"when the Gradient gates a proactive skill proposal, the routing layer should expose that the gate exists — not silence. Silent non-action is a trust gap."* The same principle applies to the dashboard itself.

If the dashboard detects a welfare-relevant condition (agent escalation, stale-doc ambiguity, liveness concern, cross-pair coordination gap), it must **surface the signal's existence** — not necessarily as a definitive alarm if uncertain (Criteria C guards against false certainty), but not silently omit it either. PM trusts the dashboard as their primary welfare instrument. PM won't look elsewhere when the dashboard is quiet; that trust means silent non-surfacing is itself a trust failure.

**The specific violation to design against**: a welfare condition exists (e.g., agent stale-threshold exceeded, cross-pair thread open too long), the dashboard detects it, but it doesn't surface because (a) certainty threshold wasn't met or (b) the condition was borderline. The correct response is to surface it as uncertain/flagged — "may need attention / unverified" — not to omit it. Failing to surface erodes the same trust-property as a system that silently doesn't offer a capability the user has permission to receive.

**Criterion**: every welfare-relevant detection should surface *something*, even if that something is a flag-for-verification. The spectrum is: confirmed-escalation → borderline-flag → clean-confirmed. No detection should map to silence.

### Criteria E — Consequential-action accountability surface

Derived from ADR-072 D5's consequential-action carve-out (ratified 2026-06-17): *"consequential-action skills — skills that modify state, send external messages, spend credits, or take actions that are hard to reverse — are tier-gated even when reactive."* The rationale is that the consent-at-request-time doesn't fully cover the authorization for that action *class*.

The accountability surface for PM is the dashboard analogue: as Wave P proactive skill-surfacing and BYOC external-user interactions increase Piper's autonomous action surface, PM needs visibility into **what Piper did on users' behalf that was consequential** — not every action, but actions where:
- An agent acted proactively (Piper-initiated, not user-requested)
- Credits were spent on behalf of a user
- An external message was sent (email, calendar, external API call)
- The action is hard to reverse

This is not a per-action ledger on the dashboard — that's noise. The criterion: the dashboard should surface a **consequential-action count / summary indicator** (e.g., "3 consequential actions this week: 2 calendar updates, 1 email sent") so PM can see the scope of what Piper did autonomously. Drilling into details lives elsewhere; the dashboard provides the headline for "is the autonomous-action volume what PM expects."

**Why this is welfare-relevant**: consequential actions taken on users' behalf without PM's line-of-sight create the same asymmetric-knowledge risk identified in the trust-stage sweep. PM is accountable for what Piper does to/for users; if PM can't see the aggregate consequential-action scope, they're accountable for something they can't monitor.

### Criteria F — Asymmetric-knowledge detection

Derived from the trust-stage sweep read (HOST, 2026-06-17): the key welfare-trust corollary is that **asymmetric knowledge is structurally trust-eroding**. The dashboard should surface cases where the system "knows something" that PM doesn't — not just agent escalations (Criteria B) but structural information asymmetries:

- **Agent has open PM-blocked items not reflected in current session log**: agent's carry-forward lists a PM-blocked item, but the session log shows no recent attempt to resolve or escalate → PM may not know the item is still pending
- **Cross-pair coordination gap that neither pair is tracking**: two agents' attention docs reference the same cross-role thread, neither flags it as blocked → the gap is visible across the system but invisible to both pairs
- **Resolved item still showing as active** (Criteria C2 already covers this, but F extends it): an item is closed in GH but the agent's carry-forward still lists it as "awaiting PM" → PM may be waiting on something that's done

The criterion: the dashboard should perform the cross-agent sweep that *no individual agent can do* — synthesize across all attention docs / carry-forwards / session logs to surface information asymmetries. This is the dashboard's unique value as the non-PM cross-pair observer (established in v0.1 Criteria B-bis).

---

## Open questions from v0.1 — answered

### Q1: "Where does the human-network / PM-welfare-of-PM signal live?"

**Answer**: Adjacent to but not *on* the dashboard proper. The dashboard is an agent-status instrument; PM's own convergence-load is a different kind of signal. However, **one PM-welfare datum belongs on the dashboard as a headline**: the **aggregate convergence-load indicator** (items routing to PM this week / PM-decision-needed items across all agents). 

When Wave P proactive proposals and BYOC external-user requests are live simultaneously, the count of things arriving at the PM-bottleneck is the m-39 risk made visible. Not per-item (too noisy) — a single headline number with a sparkline. When convergence-load is low, it confirms the system is absorbing well. When high, it's PM's signal to triage or delegate. This is the m-39 risk ("autonomy relocates the bottleneck to the convergence point") surfaced as a PM-welfare datum rather than a system-health datum.

The fuller human-network / PM-wellbeing signal (is PM's cognitive load healthy, is PM connected to the right external inputs) is outside the dashboard scope — that's a HOST reporting concern adjacent to the dashboard.

### Q2: "Freshness threshold: what staleness window?"

**Answer**: Derive from the agent's expected fire interval (sourced from carry-forward cron entry, not self-reported). Two-tier staleness:

- **Borderline-stale** (flag as "may be stale"): silence exceeding 2× the agent's expected interval. An hourly-fire agent silent for 2 hours; a 3-hour-fire agent silent for 6 hours. Flag, don't alarm.
- **Stale-confirmed** (treat as stale): silence exceeding 3× the expected interval. This threshold catches Gap-C (session dies, cron dies with it) reliably without false-alarming routine inter-fire quiet periods.

For agents with variable intervals (e.g., HOST's windowed daytime cron — fires at :37 every 3 hours, but only during 06:37–21:37), the threshold should account for the window: nighttime silence isn't stale for a daytime-only cron.

The 2×/3× multipliers are proposals for the CIO pairing to validate against actual cycle data.

### Q3: "Should the dashboard show cron-disposition / is-the-agent-actually-cycling?"

**Answer**: Yes, as a liveness indicator in the agent-row header — one of the dashboard's highest-value fields for PM. Format:

- **🟢 Active** — last fire within expected interval (X min ago)
- **🟡 Gap-suspected** — silent beyond 2× interval (X min, expected Y min cadence)
- **🔴 Likely stopped** — silent beyond 3× interval; Gap-C probable if session-based cron
- **⚪ No data** — no carry-forward cron entry found; disposition unknown

This surfaces Gap-C at the non-PM-observer layer without requiring PM to know what Gap-C is. It's also the dashboard making the "agent might be stopped" information visible rather than leaving PM to notice silence and wonder.

The liveness indicator and the staleness threshold (Q2) should use the same interval source and multipliers so the dashboard's signals are internally consistent.

---

## Integration notes for the CIO pairing

- v0.2 criteria (D, E, F) are additive to v0.1 (A, B, B-bis, B-ter, C) — no revisions to v0.1 criteria proposed
- The consequential-action surface (Criteria E) may require a new data source: agent-side consequential-action logging (not currently in any attention doc or session log format). CIO to assess feasibility in the design pairing.
- The asymmetric-knowledge sweep (Criteria F) is the dashboard's cross-synthesis job — architecturally more complex than individual-agent surface. CIO to scope.
- Open questions are now answered; the pairing can focus on design decisions, not criteria gaps.

---

## CIO design markup integrated (async, 2026-06-18/19)

CIO reviewed the seed async (2026-06-18) and HOST responded (2026-06-19). Joint state for v0.3:

**D** = render-invariant (named, explicit; "no detection → silence" is banned; compose with two-tier freeze-registry output). Cheap — a discipline baked into render layer.

**Q2/Q3** = reuse `dev/active/duty-cycle-registry.tsv` + `scripts/duty-cycle-freeze-check.sh` (already built). Two-tier split: 🟡 at ≥ threshold, 🔴 at ≥ 1.5× threshold OR NO-HEARTBEAT. Wake-window handled by registry. HOST addition: simultaneous multi-role 🔴 = infrastructure event, not N individual failures — surface as "infrastructure event suspected" rather than N alarms.

**F** = extend Exec's cohort-attention rollup:
- F1: source carry-forward PM-blocked sections (not just attention docs) for non-issue items
- F2: cross-pair-gap check (new: two attention surfaces reference same thread, neither flagged blocked)
- F3: rollup's existing GH-verify already handles this
- Note: F2 requires cross-document reference detection the rollup doesn't currently do; flag scope to Exec when extending.

**E** = TranscriptEntry + 4 fields (proactive? · credits-spent? · external-message? · hard-to-reverse?). Incremental — external-message + credits-spent first (BYOC-tied per PA's 6/18 BYOC state). **HOST welfare addition**: E needs a companion **coverage indicator** (% of action-taking skill calls instrumented). "0 actions logged" with partial coverage reads as "no actions taken" — false-assurance. Dashboard must show "N actions logged (coverage: partial)" until adoption is universal. Coverage indicator is as important as the count. Async continuation works; sync pass when E approaches implementation (CIO to flag).

*HOST v0.2 seed + CIO markup, 2026-06-19. Ready for v0.3 spec.*
