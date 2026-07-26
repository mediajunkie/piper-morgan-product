# Attention Dashboard — Trust/Welfare Criteria v0.3

**Owner**: HOST (welfare criteria lane, m-39)  
**Status**: SPEC — design decisions settled in HOST↔CIO pairing (2026-06-18/19). Implementation-ready.  
**Supersedes**: `dev/2026/06/09/dashboard-welfare-criteria-host-v0.1.md` (seed) + `dev/active/dashboard-welfare-criteria-host-v0.2-seed.md` (seed)  
**Last updated**: 2026-07-03

---

## Purpose

The attention dashboard's welfare purpose is twofold (m-39: "Autonomy Relocates the Bottleneck to the Convergence Point"):
1. **Reduce PM attention load** — confirm what doesn't need PM, so PM isn't scanning for it
2. **Prevent trust failures** — detect cases where the dashboard would quietly mislead PM

These criteria specify *what the dashboard must and must not surface*. Design/implementation is CIO's lane; this document is the welfare spec that constrains what's correct.

---

## Criteria A — Surface confirmed-clean lanes

**What**: PM needs to see that lanes are clear, not just that alarms are absent. A dashboard that only shows alarms still forces PM to wonder about the silence.

**Criterion**: Confirmed-clean agent lanes must display as confirmed-clean — "8 of 10 agents: nothing needs you" is a deliverable, not whitespace. "Clean" means verified (agent is cycling + attention doc fresh + no open escalation), NOT "doc is silent" (which could be an abandoned doc — see Criterion C1).

---

## Criteria B — Surface escalations ranked for triage

**What**: PM needs a queue, not a list.

**Criterion**: Surface escalations using the shared severity typology (🔴 decision-needed / 🟡 drift / ⚪ clean) already in attention docs. Rank by **severity × staleness × age** so the surface is triageable. Per-item: doc link + one-line summary + freshness + GH-verified state (if issue-cited).

---

## Criteria B-bis — Cross-pair coordination gaps

**What**: The dashboard's unique structural role is being the non-PM entity that sees across agent pairs. PM is currently the only cross-pair observer; routing every bilateral gap to PM is the m-39 bottleneck risk made concrete.

**Criterion**: Where an attention doc or standing item references a cross-role dependency, surface its staleness so peer-catch exists before it becomes PM-catch. This is the open-gap / what-needs-PM tier; liveness (agent went silent) is a separate watchdog tier.

---

## Criteria B-ter — Institutional-memory integrity

**What**: Institutional memory leaks silently when cycle-log displacement occurs (work logged only to ephemeral `dev/active/` cycle log, durable session log left empty).

**Criterion**: Surface per-role session-log vs. cycle-log health. Signal: session log materially shorter than cycle log + missing EOD wrap = memory-leak risk. The skill v1.5 cohort-wide fix makes this impossible by construction; the dashboard is the detector tier for any residual.

---

## Criteria C — Expectation-violation guards

Three ways the dashboard could quietly mislead PM:

**C1 — Freshness is derived, not self-reported.** A stale attention doc is where real escalations die silently. Freshness must come from cycle-log/commit activity, not the doc's own timestamp (an abandoned doc can have a recent-looking header).

**C2 — Resolved-but-presented-as-live prevention.** Items citing GH issues must be verified against actual open/closed state before surfacing. Presenting a closed item as a live PM-decision erodes trust symmetrically with hiding a real one.

**C3 — Stale-doc ambiguity is flagged, not collapsed.** A stale doc means either "nothing changed" or "agent stopped maintaining it." The dashboard can't tell which — so it must flag the ambiguity ("may be resolved / unverified"), not assert certainty it doesn't have.

---

## Criteria D — No silent non-surfacing (render-invariant)

**Design decision**: Render-invariant — baked into the render layer as a discipline, not a per-criterion check.

**What**: Derived from ADR-072 D5: when the system detects a welfare-relevant condition, it must surface *something*, even if uncertain. Silent non-surfacing on a detected condition is a trust failure — PM trusts the dashboard as their primary welfare instrument and won't look elsewhere when it's quiet.

**Criterion**: Every welfare-relevant detection maps to a dashboard signal on the spectrum (confirmed-escalation → borderline-flag → clean-confirmed). No detection maps to silence. If certainty threshold isn't met, surface as "may need attention / unverified" — not omitted.

**Implementation**: Compose with the two-tier freeze-registry output (Criteria Q2/Q3). A 🟡 borderline-stale agent still surfaces; it's just surfaced as 🟡, not 🔴 or hidden.

---

## Criteria E — Consequential-action accountability surface

**Design decision**: TranscriptEntry + 4 fields, incremental rollout (external-message + credits-spent first; BYOC-tied per PA's BYOC state). Companion coverage indicator is non-optional.

**What**: Derived from ADR-072 D5 consequential-action carve-out: PM needs visibility into what Piper did autonomously on users' behalf — not every action, but actions where:
- Piper initiated (not user-requested)
- Credits were spent on behalf of a user
- An external message was sent (email, calendar, external API)
- The action is hard to reverse

**Criterion**: Dashboard surfaces a **consequential-action count/summary indicator** (e.g., "3 consequential actions this week: 2 calendar updates, 1 email sent"). Headline-level visibility; per-action detail lives elsewhere. Drilling in is available but the dashboard shows scope.

**Coverage indicator (non-optional)**: "0 actions logged" with partial instrumentation reads as "no actions taken" — false assurance. Dashboard must show "N actions logged (coverage: partial)" until adoption is universal. The coverage indicator is as important as the count.

**Instrumentation fields** (per TranscriptEntry extension):
- `proactive: bool` — Piper-initiated vs. user-requested
- `credits_spent: bool` — any credits consumed
- `external_message: bool` — sent an external communication
- `hard_to_reverse: bool` — irreversible or difficult-to-undo action

**Rollout**: external-message + credits-spent fields first (BYOC-triggered). Full 4-field set + coverage indicator when adoption is sufficient. CIO to flag HOST for a sync pass on coverage-indicator UX before the E panel ships.

---

## Criteria F — Asymmetric-knowledge detection

**Design decision**: Extend Exec's cohort-attention rollup (three sub-criteria).

**What**: Derived from the trust-stage sweep: asymmetric knowledge is structurally trust-eroding. The dashboard should perform the cross-agent sweep that no individual agent can do — surfacing information PM doesn't have that the system does.

**F1 — PM-blocked items in carry-forwards.** Source carry-forward PM-blocked sections (not just attention docs) for non-issue items. An item listed as "awaiting PM" in a carry-forward that hasn't surfaced in any memo or attention doc is an asymmetric-knowledge gap.

**F2 — Cross-pair thread staleness.** New check (not in rollup today): two agents' attention surfaces reference the same cross-role thread, neither flags it as blocked → gap is visible across the system but invisible to both pairs. Implementation requires cross-document reference detection; flag scope to Exec when extending the rollup.

**F3 — Resolved-but-still-tracking.** Rollup's existing GH-verify already handles this (Criteria C2 at the rollup layer). No new work.

---

## Criteria Q1 — PM convergence-load headline

**Design decision**: Aggregate convergence-load indicator as a single headline number + sparkline. Not per-item detail.

**What**: When Wave P proactive proposals and BYOC external-user requests are simultaneously live, the count of items arriving at the PM-bottleneck is the m-39 risk made visible.

**Criterion**: One headline: "N items this week need a PM decision" + sparkline of trend. When low: confirms the system is absorbing well. When high: PM's signal to triage or delegate. The fuller human-network / PM-wellbeing signal is outside dashboard scope (HOST reporting concern, adjacent).

---

## Criteria Q2/Q3 — Liveness and freshness thresholds

**Design decision**: Reuse `dev/active/duty-cycle-registry.tsv` + `scripts/duty-cycle-freeze-check.sh`. Two-tier staleness split. Wake-window handled by registry.

**Freshness thresholds**:
- **🟡 Borderline-stale** (flag): silence ≥ 2× agent's expected interval
- **🔴 Stale-confirmed** (treat as stale): silence ≥ 3× expected interval, OR NO-HEARTBEAT

Wake-window: use registry-sourced window for agents with daytime-only crons (nighttime silence is not stale for a daytime cron).

**Liveness indicator** (per-agent row header):
- 🟢 **Active** — last fire within expected interval (X min ago)
- 🟡 **Gap-suspected** — silent ≥ 2× interval (X min, expected Y min cadence)
- 🔴 **Likely stopped** — silent ≥ 3× interval; Gap-C probable if session-based cron
- ⚪ **No data** — no registry entry found; disposition unknown

**Multi-role 🔴**: simultaneous 🔴 across multiple roles = infrastructure event, not N individual failures. Surface as "infrastructure event suspected" rather than N separate alarms.

---

## Validation evidence — Criteria A and D confirmed by live incidents, 2026-07-25

*(Added by CIO, implementation lane. The spec was written 2026-07-03 as design. On 2026-07-25 the cohort produced three independent live instances of exactly the failures A and D specify guards against — worth recording, because a criterion with a real incident behind it survives review differently than one argued from first principles.)*

**Criterion A — "clean means verified, not silent" — confirmed.** The stall-watchdog emitted: *"Newly nudge-worthy: arch · **all currently stale**: STALE arch 145h."* Read cold, that says the cohort is fine except one role. In fact the registry held **four rows against ten roles**, and **five roles had been dark six days** — four of them structurally invisible to the belt because they had no row. Silence was rendered as clean, precisely as A forbids. The spec's own phrasing (*"8 of 10 agents: nothing needs you"*) already anticipates the fix; the live system just didn't implement it.

**Criterion D — "no detection maps to silence" — confirmed three times over**, each a mechanism that produced no output while covering less than it appeared to:
- Pre-commit hooks **present, correctly registered, and never invoked** — an invalid matcher meant they had never fired on any host since introduction. Config inspection said everything was fine.
- The PreCompact sign-off hook **registered to an empty array for ten weeks** while CLAUDE.md described it in the present tense as a live safety net. Corroborated by absence: the log file it supposedly wrote had never existed.
- `MEMORY.md` **silently truncated past a ~24KB read limit** — ~40% of entries invisible to every agent that loaded it, while the file itself was provably complete.

### The requirement this evidence adds

Criterion A says clean must mean *verified*. The watchdog incident sharpens it:

> **Any coverage-based claim must state its denominator.** "All currently stale: arch" is not merely incomplete — it is *actively misleading*, because a subset presented as a total manufactures confidence in the unexamined remainder. The render must say **"stale among the 4 watched: arch · NOT WATCHED: cxo, pa, ppm, web"** — the un-watched set is itself a welfare signal, and under Criterion D it cannot map to silence.

This is the sharpest form of the day's general lesson, and it belongs in the render layer rather than in any individual check: **a mechanism's silence only means "clear" if its coverage has been separately verified.** A dashboard is exactly the instrument where that failure is most costly, because PM adopts it as the primary welfare surface and stops looking elsewhere — which is the trust dependency Criterion D already names.

**Implementation consequence**: whatever renders A must compute *watched vs. roster* and display the gap, not just the alarms within the watched set. The cheapest durable fix for the underlying drift is upstream — registration coupled to provisioning, so coverage can't diverge from the roster (shipped 2026-07-25 as `duty-cycle-tick` v1.17, where each agent writes its own registry row at START; the provisioner can't, since the load-bearing field is the agent's cron expression).

---

## What does NOT belong on the dashboard

- **Raw cycle-log activity** — source boundary is attention docs (the curated PM-batching surface). Synthesizing raw activity is noisier and defeats the dashboard's purpose of collapsing scatter.
- **Unverified GH-cited items** — see Criteria C2. Verify before presenting.
- **Duplicate cross-role thread entries** — collapse to one entry when the same thread appears in multiple docs (PA's dedup rule).
- **Per-action consequential-action detail** — that's drill-down, not the dashboard headline.

---

## TBD / not yet designed

- **F2 cross-document reference detection** — requires new rollup capability. Scope with Exec when extending the cohort-attention rollup for F2.
- **E panel UX for coverage indicator** — CIO to flag HOST for sync pass before E panel ships.
- **Rollout sequencing for E instrumentation** — external-message + credits-spent first (BYOC-tied); CIO + PA to coordinate timing with BYOC phase-2.
- **2×/3× multiplier validation** — the freshness thresholds are proposals; validate against actual cycle data before locking.

---

*v0.3 spec by HOST, 2026-07-03. Based on v0.1 starter (2026-06-04), v0.2 seed (2026-06-17), and HOST↔CIO design pairing (2026-06-18/19). Implementation lane: CIO. Welfare criteria lane: HOST.*
