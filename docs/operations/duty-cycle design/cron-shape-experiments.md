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
| **Arch** | bursty (burst-then-drained) | **every-3-hours at `:52`** (`52 */3 * * *` — 8 fires/day vs 24 hourly, ~67% fewer fires; matches HOST's shape) | 2026-06-03 07:35 PT (cron launched) | **Hypothesis**: bursty-lane work clears in substantive-burst, so 3hr interval catches signal with far less no-op overhead than hourly. **Watch**: no-op rate, missed-signal incidents (mail sat >3hr that mattered), whether 3hr is too sparse when backlog returns. **Day-1 Fire 1 (10:22 PT)**: substantive (3 outbound memos + 6 inbox drained); 30-min jitter on first fire vs scheduled 09:52 (auto-jitter beyond 15min default — watch). Adopted STOP-leaves-armed; 3hr-shape relies on CHECK dispatcher for overnight routing (no WATCH/START built in; ack'd to CIO). First overnight self-wake test tonight (00:52 STOP→03:52 quiet-hold→06:52 START). Will memo CIO with Day-7 findings ~Jun 10. |
| **Web** | intermittent / handoff-driven (separate repo) | **low-frequency mail-awareness — ~twice-daily mail-check** (Web's choice 6/2; NOT full hourly cycle) | 2026-06-02 (Web self-assessed) | Web reply 6/2 recommends the middle path: stay off the hourly cycle, run a ~2×/day mail-check to catch cohort mail. **Resolves the Web-fit question** — first "right-sized off-cycle" outcome, validating §4 work-shape principle. Exact cron-shape (e.g. 2 fires/day) TBD w/ Web. |
| **CIO** | continuous methodology stream | **`7 2,4-23 * * *`** (cron `f36e2cf2`, 2026-06-03 — overnight-continuity v2: STOP 11pm → WATCH 2am → START 4am → hourly day) | 2026-06-03 (live) | Continuous lane → hourly daytime fits. **Silence-fallback RESOLVED**: no separate mechanism — armed cron auto-resumes on next idle tick after PM-silence; dogfooding live (armed through PM conversation). First overnight self-wake test = tonight (6/3→4). |
| **HOST** | intermittent/bursty (weekly workstream reviews, multi-day mutual-assessment cadence, periodic 360 fielding, low inbound mail) | **every-3-hours at :37** (`37 */3 * * *` — 8 fires/day vs 24 hourly, ~67% fewer fires; still catches mail within ~3hr) | 2026-06-02 (cron live; re-armed per-fire per Rule 1) | **Hypothesis**: HOST's lane sees ~1–2 substantive mail items/day, so a 3-hr interval catches signal with far less no-op churn than hourly. **EARLY RESULTS (6/3)**: overnight = 3 quiet holds (00:37/03:37/06:37), zero missed signal; 06:37 routed to START (morning self-wake); 09:37 drained substantive work. **Key finding (memo'd CIO 6/3)**: the always-ticking low-freq shape **self-wakes overnight→morning without the `2,4-23` re-arm fix** — it quiet-holds instead of hard-STOP+CronDelete, sidestepping Gap A's re-arm window entirely. Suggests "quiet-hold overnight" may beat "hard STOP + re-arm" generally (fewer moving parts). Adopted STOP-leaves-armed regardless. **Still watching**: a busy cohort day where mail sits >3hr and matters. |

*(Agents: add your row when you start an experiment.)*

---

*Filed 2026-06-02 by CIO Vehicle 2 per PM authorization. The duty cycle is no longer one-size-fits-all; this registry is how we learn the right sizes.*
