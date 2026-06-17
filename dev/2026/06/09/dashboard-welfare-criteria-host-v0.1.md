# Attention-Dashboard — Trust/Welfare Criteria (HOST, v0.1 starter)

**Owner**: HOST (welfare criteria), per methodology-39 lane-split (CIO design / HOST welfare-criteria / PA mechanism). **Status**: starter draft, prep for the CIO v0.2 design pairing. Not a spec yet — the spec emerges in the pairing.

**What this is**: the criteria for *what the attention dashboard should and shouldn't surface*, derived from the dashboard's purpose as a **PM-welfare mechanism** (m-39: "Autonomy Relocates the Bottleneck to the Convergence Point"). The design question is "how do we build it"; the welfare question is "what does PM need to see, not-see, and trust."

---

## The two welfare questions (the spec frame)

Everything below answers one of two questions:
1. **What does PM need to NOT worry about?** (attention-load reduction — the clean-state-visible feature)
2. **Where is the expectation-violation risk?** (the trust guards — where the dashboard could quietly mislead)

## Criteria A — Surface the clean state, not just the alarms

The welfare core (per PA's v0.1 finding + m-39): a dashboard that only shows alarms still forces PM to wonder about the silence. So:
- **Confirmed-clean lanes must be visible as confirmed-clean** — "8 of 10 agents: nothing needs you" is a deliverable, not whitespace.
- "Clean" must mean *verified* clean (agent is cycling + attention doc fresh + no open escalation), NOT "doc is silent" (which could be an abandoned doc — see Criteria C).

## Criteria B — Surface real escalations, ranked by what-needs-PM-now

- Use the shared severity typology (🔴 decision-needed / 🟡 drift / ⚪ clean) the attention docs already carry.
- Rank by **severity × staleness × age** (PA's rung 6) so the surface is a *queue*, not a list — the fragmented decision-surface becomes triageable.
- Each item: doc link + one-line summary + freshness + (if it cites an issue) verified GH state.

## Criteria B-bis — Surface cross-pair coordination gaps (the dashboard as non-PM cross-pair observer)

Added 2026-06-08 (from the PM-as-catch trust-property thread w/ Arch). The dashboard's other load-bearing job: be the **non-PM entity that sees across agent-pairs.** The PM-as-catch risk (a recurring bilateral gap routing only to PM, the sole cross-pair observer) is structurally answered by surfacing cross-pair staleness/open-gaps here — so PM isn't the only one who notices when an Arch↔Lead (or any pair) coordination thread has gone stale. Criterion: where an attention/standing item references a *cross-role* dependency, surface its staleness so a peer-catch exists before it becomes a PM-catch. (This generalizes the per-incident sub-mechanisms — signaling-norm, sync-discipline, the cron-death Gap-C two-layer — into one observability surface.)

**Two tiers of cross-pair observability (CIO convergence, 6/8):** the dashboard is the **open-gap / what-needs-PM tier** (read-side); the **Routines watchdog** (if PM builds it) is the **liveness tier** (surfaces "an agent went silent" — the cron-death failure mode). Both are non-PM cross-pair observers; together they cover PM-as-catch at the open-gap *and* liveness layers. The dashboard welfare-criteria should assume a liveness signal exists alongside (don't try to infer agent-death from the attention docs alone — that's the watchdog's job; the dashboard consumes/links it). *(Note: durable=true cron is a confirmed no-op in our env — it is NOT the cron-death fix; the Gap-C two-layer is.)*

## Criteria B-ter — Institutional-memory integrity (is the cohort's working memory accruing or leaking?)

Added 2026-06-09 (from the session-log-vs-cycle-log displacement thread; Arch handed HOST the trust-of-memory dimension). **Institutional memory is a trust artifact** — and it can leak silently. The displacement failure (substantive work logged only to the ephemeral cycle log in `dev/active/`, leaving the durable session log empty → vanishes when dev/active is cleaned) is an expectation-violation at the *memory* layer: PM/Docs/future-agents trust the durable record is complete; it isn't. **Welfare-criterion**: surface per-role **session-log-vs-cycle-log health** (session log materially shorter than the cycle log + missing an EOD wrap = leak risk) so the cohort sees memory leaking before it's gone. (Mechanism fix landed cohort-wide: skill v1.5 per-fire session-log accretion makes "cycle full + session empty" impossible-by-construction; the dashboard is the *detector* tier for any residual.) HOST self-instance: caught my own 6/7 leak via this audit (backfilled 6/9) — the criterion in live use.

## Criteria C — Expectation-violation guards (the trust layer — HOST's sharpest contribution)

These are where the dashboard could *quietly mislead PM*, which is the trust failure to design against:
1. **Doc-freshness as a first-class field, derived not self-reported.** A stale attention doc is where a real escalation dies silently. Freshness must come from the agent's *cycle-log/commit activity* (the m-36 derive-don't-trust-self-timestamp move), not the doc's own timestamp — an abandoned doc can have a recent-looking header.
2. **Resolved-but-presented-as-live is the inverse violation.** Items citing issues (#NNNN) must be checked against actual GH open/closed state (PA's rung 3). Presenting a closed item as a live PM-decision erodes trust as much as hiding a real one.
3. **Stale-doc disambiguation.** A stale doc means either "nothing changed" OR "agent stopped maintaining it." The dashboard can't tell which without verification — so it must *flag the ambiguity* ("may be resolved / unverified") rather than present week-old items as current. Don't let the dashboard assert certainty it doesn't have.

## What does NOT belong (noise re-creates the scatter the dashboard exists to collapse)

- **Raw standing-items / cycle-log activity.** Source boundary = attention docs (Doc 3), the curated PM-batching surface by design. Synthesizing raw activity is richer but noisier; noise on a welfare instrument is self-defeating. (HOST/CIO/PA aligned on this 6/3.)
- **Unverified GH-cited items presented as live** (see C2).
- **Duplicate cross-role threads** (same thread in multiple docs) — collapse to one entry (PA rung 4).

## Open questions for the CIO pairing

- Where does the **human-network / PM-welfare-of-PM** signal live? The dashboard surfaces *agent* escalations to PM; is there a place to surface "PM's own convergence-load is high this week" (the m-39 risk made visible to PM about themselves)? This may be HOST-lane reporting adjacent to, not on, the dashboard.
- Freshness threshold: what staleness window flips a lane from "clean (current)" to "clean (unverified/stale)"? (Proposal: derive from cycle cadence — an agent on hourly that's silent 2hr ≠ one on every-3hr silent 2hr.)
- Should the dashboard show **cron-disposition / is-the-agent-actually-cycling** as a field? (Ties to the item-4 expectation-violation: "PM thinks agent X is running.")

---

*HOST v0.1 starter, 2026-06-04. For the CIO attention-dashboard v0.2 design pairing. The welfare criteria are the spec for what the dashboard should and shouldn't surface; the design is CIO's lane.*
