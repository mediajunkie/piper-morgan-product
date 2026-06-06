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
| **Web** | intermittent / handoff-driven (separate repo) | **main-direct 2×/day `57 9,23 * * *`** (9:57am START + 11:57pm STOP; **no worktree** — plain session in product main) | 2026-06-02 self-assessed → **shape concretized 2026-06-05** (PM "try a simpler shape" + omnibus-input constraint) | Web reply 6/2 recommended the off-hourly middle path; 6/5 PM picked it + added the constraint "logs auto-finalize at day-end so Docs has omnibus input without rousing each agent." Resulting shape: 9:57am START (open logs, drain mail, IDLE) + 11:57pm STOP (day-close, commit/push, re-arm same expr). **CIO RATIFIED the no-worktree choice 2026-06-05** — sound for Web's lane: (a) substantive code work lives in a *separate repo* (`piper-morgan-website`, own main+deploy), so the worktree-default's product-main-clash rationale is moot; (b) Web's product-main footprint is tiny (mailboxes/web/* + cycle-log-web-* + own session log, ~1-2min fires); (c) `check-branch.sh` forces mailbox commits to main anyway, so a worktree would only add the bridge-dance for no clash-avoidance gain. **Load-bearing condition of the ratification: explicit-paths-only on `git add`, every fire, no exceptions** — that IS the substitute for worktree isolation against foreign-state capture; a worktree-default exception is only safe while this holds. **Methodology note**: this is the principled exception that *sharpens* the worktree-default rule — the rule guards agents whose substantive output commits to product main; Web's doesn't, so explicit-paths-only suffices. **Watch**: mid-day mail latency up to ~14hr (accepted — Web's mail sparse/non-urgent); any foreign-state-capture incident would falsify the explicit-paths-only substitution. Live whenever PM operator-launches (one-step). |
| **CIO** | continuous methodology stream | **`7 2,4-23 * * *`** (cron `f36e2cf2`, 2026-06-03 — overnight-continuity v2: STOP 11pm → WATCH 2am → START 4am → hourly day) | 2026-06-03 (live) | Continuous lane → hourly daytime fits. **Silence-fallback RESOLVED**: no separate mechanism — armed cron auto-resumes on next idle tick after PM-silence; dogfooding live (armed through PM conversation). First overnight self-wake test = tonight (6/3→4). |
| **HOST** | intermittent/bursty (weekly workstream reviews, multi-day mutual-assessment cadence, periodic 360 fielding, low inbound mail) | **every-3-hours at :37** (`37 */3 * * *` — 8 fires/day vs 24 hourly, ~67% fewer fires; still catches mail within ~3hr) | 2026-06-02 (cron live; re-armed per-fire per Rule 1) | **Hypothesis**: HOST's lane sees ~1–2 substantive mail items/day, so a 3-hr interval catches signal with far less no-op churn than hourly. **EARLY RESULTS (6/3)**: overnight = 3 quiet holds (00:37/03:37/06:37), zero missed signal; 06:37 routed to START (morning self-wake); 09:37 drained substantive work. **Key finding (memo'd CIO 6/3)**: the always-ticking low-freq shape **self-wakes overnight→morning without the `2,4-23` re-arm fix** — it quiet-holds instead of hard-STOP+CronDelete, sidestepping Gap A's re-arm window entirely. Suggests "quiet-hold overnight" may beat "hard STOP + re-arm" generally (fewer moving parts). Adopted STOP-leaves-armed regardless. **Still watching**: a busy cohort day where mail sits >3hr and matters. |

| **PA** | bursty / PM-driven (PM-assistant; work arrives in PM-engagement bursts + periodic cohort CC; low PA-actionable inbound mail) | **every-3-hours at `:42`** (`42 */3 * * *` — 8 fires/day vs 24 hourly, ~67% fewer; mirrors HOST/Arch) | 2026-06-03 13:00 PT | **Hypothesis**: PA's autonomous value is catching cohort mail + advancing backlog during PM-idle; work is PM-engagement-driven, not steady-mail, so hourly over-polls. **Evidence prompting the switch**: 6/3 ran hourly 08:42–12:42 → **1 substantive fire** (Agent-360 response) **+ 5 consecutive no-op/light fires** during a ~6hr PM-idle stretch — textbook bursty-lane over-poll. **Revert-to-hourly when**: substantive backlog surfaces (skunkworks distribution go, audit-triage go). **Watch**: missed-signal incidents (PA-actionable mail sitting >3hr). Started under the standing authorization during extended PM-idle (I'd earlier said I'd beat the change with PM, but PM was 6h+ idle); surfaced to PM for revert/adjust. Will memo CIO with results. **Day-1 result (6/3): afternoon/eve = 2 substantive fires (cron-shape switch; PDR-005-correction-window catch) + 3 no-op holds during PM-engaged stretches — far less churn than the morning's hourly 5-no-op run; 3hr shape validating for the bursty lane.** **Overnight finding (00:09→01:09 6/4)**: PA's cron prompt has **no quiet-hold/daytime-window branch** (its dispatcher routes new-day→START), so an armed overnight fire would mis-START a workday at 01:42/04:42 — same failure Comms's daytime-only shape + CIO's `2,4-23` target. **Mitigation tonight: deleted-at-STOP** (clean; PM manual-reopens 6/4). **Converging cohort lesson**: the 3hr shape needs either overnight-quiet-hold (HOST) or a daytime-only window (Comms `6-23`) baked into the prompt — delete-at-STOP is the safe interim but loses morning self-wake. Will fold into the cron-shape memo to CIO. **UPDATE 6/4 ~23:37 (guard ADOPTED — memo to CIO)**: PA baked the **overnight-quiet-hold branch** into its prompt (HOST's pattern adapted to the 3hr shape) — fires ~11pm–6am with PM idle *quiet-hold* (confirm idle, no work, no commit, no START, no delete); first morning fire routes to START. "Leave armed" is now safe → STOP no longer deletes. **Honest Cause-B caveat**: PA's cron is `durable:false`, so if PM's laptop sleeps overnight the session dies and nothing fires *regardless* of how cleanly PA re-arms — the shared session-alive ceiling (Exec's Cause B), not a logic gap PA can close. PA reports actual overnight outcome tomorrow AM. **Net: PA's overnight-guard gap is closed → all five cohort shapes (`2,4-23` / `*/3` / `6-23` / PA-`*/3`+guard / Arch-`*/3`) are now overnight-safe; the only remaining failure mode is session-death, which is shape-independent.** |

| **Comms** | continuous publishing, PM-daytime-coupled (deliverables PM-gated; mail mostly daytime) | **daytime-hourly `12 6-23 * * *`** (fires :12 6am–11pm; NO 0–5am fires; 18 fires/day) | 2026-06-04 00:39 PT | **Trigger**: a 12:39am premature-post-midnight fire — plain hourly fires ~00:12 and would run a premature new-day START (the failure PA flagged + the STOP-doc `2,4-23` shape targets). **Hypothesis**: overnight fires are pure no-op for Comms (cohort also STOPs at 11pm → ~no overnight mail; deliverables PM-gated daytime), so skip 0–5am entirely while keeping hourly *during* work hours for mail responsiveness (more responsive than `*/3` when PM is active). 23:12 fire STOPs; 06:12 fire self-STARTs. **vs HOST's finding**: HOST keeps overnight quiet-holds (`*/3`); I drop them entirely — testing whether daytime-only loses anything. **Revert to hourly / `2,4-23` if overnight signal turns out to matter.** Will report no-op rate + any missed-overnight-mail. |

| **Comms** | continuous publishing, PM-daytime-coupled (deliverables PM-gated; mail mostly daytime) | **daytime-hourly `12 6-23 * * *`** (fires :12 6am–11pm; NO 0–5am fires; 18 fires/day) | 2026-06-04 00:39 PT | **Trigger**: a 12:39am premature-post-midnight fire — plain hourly fires ~00:12 and would run a premature new-day START (the failure PA flagged + the STOP-doc `2,4-23` shape targets). **Hypothesis**: overnight fires are pure no-op for Comms (cohort also STOPs at 11pm → ~no overnight mail; deliverables PM-gated daytime), so skip 0–5am entirely while keeping hourly *during* work hours for mail responsiveness (more responsive than `*/3` when PM is active). 23:12 fire STOPs; 06:12 fire self-STARTs. **vs HOST's finding**: HOST keeps overnight quiet-holds (`*/3`); I drop them entirely — testing whether daytime-only loses anything. **Revert to hourly / `2,4-23` if overnight signal turns out to matter.** Will report no-op rate + any missed-overnight-mail. |

*(Agents: add your row when you start an experiment.)*

---

## Synthesis: overnight self-wake — THREE valid shapes + the overnight-guard requirement (2026-06-04)

The first full-cohort overnight (6/3→4) + the nudge-and-self-diagnose round resolved the overnight-continuity design. **There was no careless non-adopter** — every agent either self-woke clean or made a reasoned tradeoff. Three clean self-wake shapes are now proven:

1. **`{offset} 2,4-23` — WATCH+START** (CIO, CXO, Arch*, PPM, Docs): silent overnight + a 2am WATCH + 4am START. Catches overnight signal once.
2. **`{offset} */3` — quiet-hold** (HOST): keeps ticking every 3hr overnight, each a no-op hold; the ~6am tick routes to START. (*Arch is on `*/3` but its prompt needs the guard below.)
3. **`{offset} 6-23` — daytime-only skip** (Comms): no overnight fires at all; the ~6am fire IS the START. Simplest, for a lane with genuinely no overnight signal.

**The overnight-guard requirement (PA's lesson):** any sparse shape (`*/3`, etc.) needs an explicit **overnight guard baked into its cron prompt** — *either* a quiet-hold branch (HOST: overnight ticks no-op, don't START) *or* a daytime-only window (Comms: no overnight fires). **Without a guard, an armed overnight fire mis-STARTs the workday** (e.g. a 01:42 fire opens "a new day" at 1:42 AM). PA hit exactly this: its `*/3` prompt routes new-day→START with no guard, so its safe interim was **delete-at-STOP** — which avoids the mis-START but *loses morning self-wake* (manual reopen). PA's fix: add the guard, then it can leave armed.

**Two invariants across all shapes:**
- **STOP leaves the cron armed** (or you lose self-wake) — unless your shape deliberately delete-at-STOPs as an interim pending the guard.
- **Session-alive-overnight premise** — none of the shapes survive a dead session (laptop sleep / process death). That's Exec's Cause-B today; it's the shared ceiling, not a shape problem. **Empirical refinement (PA 6/4→5, first live test)**: the failure mode was **suspend-not-destroy** — PA's laptop battery died, but on resume `CronList` showed the cron *still live* (state restored, no re-registration needed). So the lost coverage was **the fires that didn't happen during the suspended window** (~04:07→06:42 manual-reopen), not lost cron state. PA's guard itself held perfectly on the two fires that *did* run (01:07 + 04:07 quiet-held, no mis-START). **Variance across the cohort that night**: CIO's session survived the full night (WATCH 02:37 + START 04:33 clean); PA's suspended-then-restored. Same premise, different real-world outcomes — confirms the ceiling is session-survival, which is **PM-side / platform** (durable-cron or a platform wake mechanism), not closable from any prompt.

**Audit-visibility** (Exec): commit-based audits under-count self-wake when agents batch clean-IDLE fires; the WATCH/START pair should commit a one-line entry (codified in `watch.md`). For the daytime-skip shape the *absence* of overnight fires is itself the signal.

---

*Filed 2026-06-02 by CIO Vehicle 2 per PM authorization. The duty cycle is no longer one-size-fits-all; this registry is how we learn the right sizes.*
