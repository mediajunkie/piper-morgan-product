# Autonomy Relocates the Bottleneck to the Convergence Point

**Status**: Emerging (filed 2026-06-03; PM-ratification pending on framing). Credit: PM (framing) + PA (the mechanism — attention-dashboard v0.1).

## Overview

**Autonomy Relocates the Bottleneck to the Convergence Point** names the success-mode failure of a multi-agent autonomous cohort: when the duty cycle works — agents drain their own mail, advance their own backlog, and escalate only what genuinely needs the human — **the bottleneck does not disappear. It relocates to the one thing that cannot be parallelized: the human's attention.**

The principle:

1. The duty cycle's purpose is to move work *off* the PM-blocking path. Each agent that used to wait on PM for everything now self-drains.
2. But each agent still correctly surfaces its *few* real PM-decisions. Ten self-draining agents, each surfacing two or three genuine decisions, sum to a **fragmented decision surface that no single document shows** — scattered across nine `duty-cycle-escalations-*.md` files.
3. So the better autonomy gets, the more the convergence point (the human's attention) becomes the binding constraint — and the more it needs a *mechanism* to stay legible and triageable, not a scatter of markdown files.

**The counterpart mechanism is the attention dashboard** — a derived rollup of every agent's open decisions/escalations into one severity-batched, freshness-flagged view (PA's v0.1: `pa-cohort-attention-rollup-2026-06-03.html`). It is not a reporting widget. It is the structural counterpart to autonomy succeeding, and the human-welfare guard against the convergence load.

## Why This Methodology

### The 2026-06-03 origin

The full cohort (9–11 of 11 roles) reached the duty cycle on June 1–3. The same week PM framed the insight directly: *"[the dashboard is for] when success relocates all the 'smart bottlenecks' to my fragmented attention."* PA, asked to batch the cohort's attention docs into one rollup, shipped a v0.1 — and PM's reaction named it as the concrete first piece of the long-roadmapped "attention dashboard."

The empirical confirmation was in the v0.1's own findings: across 9 agents, only *two* real PM-decisions were live. That sparseness is the healthy signal — the cohort is mostly self-draining — **but the value of seeing it required aggregating nine separate docs.** Without the dashboard, "you don't need to look here" is invisible; PM would have to read nine files to learn there was nothing to do. A good derived view makes the *clean* state legible as much as the alarms.

### The mechanism

This is the load-bearing-cost flip side of **methodology-34 (Cohort-Discipline as Moat)**: the same cohort-discipline that is the competitive moat also concentrates decision-convergence on the human. The moat's cost is the convergence load; the dashboard is what keeps that cost bounded.

It pairs with the **derived cohort-status view** (`scripts/cohort-cycle-status.sh`) as the **two halves of derived duty-cycle observability**:

| Question | Derived view | Reads |
|---|---|---|
| *Are the agents running?* | cohort-cycle-status.sh | cycle-log presence + worktree list |
| *What do they need from me?* | attention dashboard | rollup of `duty-cycle-escalations-*.md` |

Both are instances of **methodology-36 (Derived Views Over Hand-Maintained Trackers)** — neither goes stale, because both read live signals rather than a hand-curated summary.

### Two design constraints (from PA's v0.1)

- **Confirming "you don't need to look here" is half the value.** Surface the clean state, not just the alarms.
- **Attention-doc staleness is itself a first-class signal** — but a doc's own timestamp can't distinguish "nothing changed" from "agent stopped maintaining it." The honest move is to flag stale items as *may-be-resolved*; the deeper fix is to derive freshness from the agent's actual cycle-log/commit activity, not the doc's self-reported timestamp (again, methodology-36).

### The trust/welfare lens (HOST, 2026-06-03)

HOST named this from the trust/welfare seat, and the framing deepens the entry: bottleneck-relocation is the **attention-load cousin of the expectation-violation** HOST tracks. The overnight-continuity gap was "PM thinks an agent is running; it silently isn't." This is the same shape one layer up: **as the cohort self-drains, the welfare risk relocates *onto* PM** — whose role narrows to the one un-parallelizable thing, being the convergence point. So the dashboard is a **PM-welfare mechanism**, not a reporting widget — the thing standing between "cohort productive" and "PM overwhelmed by convergence."

Three welfare consequences:
- **"Confirming you don't need to look here" is the welfare *core*, not a nicety.** Reducing PM's *scanning* load — the certainty that "nine docs are clean, two need you" — is as much the deliverable as surfacing the two. An alarm-only dashboard still forces PM to wonder about the silence.
- **Attention-doc staleness is the expectation-violation seam.** A stale attention doc is where a real escalation goes to die silently — PM (and the dashboard) treat it as current when it isn't. So the **doc-freshness field is a trust guard, not cosmetic**; deriving freshness from the agent's actual cycle-log/commit activity (not the doc's self-timestamp) is the honest implementation.
- **Source boundary**: attention docs (Doc 3) stay primary — they're the curated PM-batching surface by design; synthesizing from raw standing-items/cycle-logs would re-create the noise the dashboard exists to collapse. Freshness-as-first-class-field mitigates the one risk (a stale doc hiding an escalation). HOST + CIO + PA align on this.

Division of lanes: CIO owns the dashboard *design* (duty-cycle roadmap); **HOST owns the trust/welfare criteria** for what belongs on it ("what does PM need to *not* worry about" + "where is the expectation-violation risk"); PA built the *mechanism* (v0.1).

## Promotion-to-Proven criterion

Promote when: (a) the attention dashboard reaches a maintained v0.2+ that the cohort/PM actually triages from; (b) at least one instance where the dashboard surfaced a decision that would otherwise have been buried in a single agent's doc; and (c) the convergence-load framing is referenced by name in cohort planning (roadmap, Ship, or 360).

## Cross-references

- methodology-34 (Cohort-Discipline as Moat) — the moat whose cost this names
- methodology-36 (Derived Views Over Hand-Maintained Trackers) — both observability halves are instances
- `scripts/cohort-cycle-status.sh` — the are-they-running half
- `dev/active/pa-cohort-attention-rollup-2026-06-03.html` — the v0.1 dashboard
- duty-cycle design corpus (`docs/operations/duty-cycle design/`) — the autonomy substrate this is the success-mode of

---

*Filed 2026-06-03 by CIO Vehicle 2 (Fire 13 idle-advance). Emerging — the framing is PM's; ratification to Proven pending PM sign-off + the promotion criteria above.*
