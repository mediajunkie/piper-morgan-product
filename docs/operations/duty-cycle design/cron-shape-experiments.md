# Cron-Shape Experiments — registry + reporting

**Authorized by PM 2026-06-02.** Agents are authorized to **experiment with their cron-shape** (cadence/interval/trigger model) to fit their lane's **work-shape**, and **must report results** here so the cohort learns which shapes fit which work-shapes.

**Owner**: CIO (synthesizes findings into v0.7+ methodology). **Companion to**: `procedures/cron-lifecycle.md`, `v0.7-candidates.md` (Candidate 5), `cohort-agent-status.md`.

---

## The principle being tested

The v0.6 duty cycle assumed **one fixed hourly interval for everyone**. Three independent signals say cadence should instead **match work-shape**:

- **Arch** (2026-06-02): *bursty lane* — a substantive burst then drained no-op fires. Hourly = mostly no-op overhead once backlog clears. Proposes longer interval (2–3hr) when drained.
- **Web** (work-shape): *intermittent, handoff-driven* design in a separate repo — the continuous flywheel may rarely have work to drain.
- **Janus** (cross-project): explicitly distinguished *bounded-stateless* vs *continuity-needing* work-shapes.

**Hypothesis**: continuous-mail lanes (CIO methodology stream, Docs, PPM, Comms publishing, Lead trickle) suit the standard hourly interval; **bursty/intermittent lanes suit longer intervals or event-driven triggers** — fewer no-op fires, same signal.

## How to participate

1. **Pick a shape** that fits your lane (examples below). You don't need permission per-experiment — this doc IS the standing authorization.
2. **Log it here** in the table when you START: your work-shape, the shape you're trying, start date, hypothesis.
3. **Update with results** as you learn (no-op rate, missed-signal incidents, overhead vs value).
4. **Memo CIO** when you have a finding worth folding into methodology. CIO synthesizes across the cohort.

### Shape menu (non-exhaustive — invent others)

- **Standard hourly** (current default; continuous lanes)
- **Long-interval-when-drained** (e.g., 2–3hr once backlog clears; revert to hourly when substantive work surfaces) — Arch's proposal
- **Event-driven / stay-paused-until-backlog** (resume cron only when work accumulates; zero no-op overhead, loses cadence parity)
- **Low-frequency mail-awareness only** (1–2×/day, just to catch cohort mail; for intermittent lanes like Web)
- **Wait-default re-arm heuristic** (CIO's pilot heuristic — closure-marker + tone + silence proxy; the IDLE-resume restoration; see Candidate 5)

## Reporting note

This is the "report in on results" mechanism PM asked for (2026-06-02). Don't let an experiment run silently — a shape that's never reported is a shape we can't learn from. Even "tried X, reverted, here's why" is valuable.

---

## Experiments registry

| Agent | Work-shape | Shape being tried | Started | Status / results |
|---|---|---|---|---|
| **Arch** | bursty (burst-then-drained) | long-interval-when-drained (2–3hr) — OR event-driven (its option C) | 2026-06-02 (authorized) | Cron paused since 5/28; greenlit to resume with bursty-aware shape + report. First registered experiment. |
| **Web** | intermittent / handoff-driven (separate repo) | TBD — likely low-frequency mail-awareness or off-cycle | pending Web self-assessment (CIO memo 6/2) | Awaiting Web's read on fit. |
| **CIO** | continuous methodology stream | standard hourly + wait-default re-arm heuristic (IDLE-resume restoration) | PoC pending PM go | Restoring the pilot heuristic that normalization dropped (Candidate 5). |

*(Agents: add your row when you start an experiment.)*

---

*Filed 2026-06-02 by CIO Vehicle 2 per PM authorization. The duty cycle is no longer one-size-fits-all; this registry is how we learn the right sizes.*
