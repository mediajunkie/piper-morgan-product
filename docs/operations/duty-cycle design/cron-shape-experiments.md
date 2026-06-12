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

| **PA** | bursty / PM-driven (PM-assistant; work arrives in PM-engagement bursts + periodic cohort CC; low PA-actionable inbound mail) | **every-3-hours at `:42`** (`42 */3 * * *` — 8 fires/day vs 24 hourly, ~67% fewer; mirrors HOST/Arch) | 2026-06-03 13:00 PT | **Hypothesis**: PA's autonomous value is catching cohort mail + advancing backlog during PM-idle; work is PM-engagement-driven, not steady-mail, so hourly over-polls. **Evidence prompting the switch**: 6/3 ran hourly 08:42–12:42 → **1 substantive fire** (Agent-360 response) **+ 5 consecutive no-op/light fires** during a ~6hr PM-idle stretch — textbook bursty-lane over-poll. **Revert-to-hourly when**: substantive backlog surfaces (skunkworks distribution go, audit-triage go). **Watch**: missed-signal incidents (PA-actionable mail sitting >3hr). Started under the standing authorization during extended PM-idle (I'd earlier said I'd beat the change with PM, but PM was 6h+ idle); surfaced to PM for revert/adjust. Will memo CIO with results. **Day-1 result (6/3): afternoon/eve = 2 substantive fires (cron-shape switch; PDR-005-correction-window catch) + 3 no-op holds during PM-engaged stretches — far less churn than the morning's hourly 5-no-op run; 3hr shape validating for the bursty lane.** **Overnight finding (00:09→01:09 6/4)**: PA's cron prompt has **no quiet-hold/daytime-window branch** (its dispatcher routes new-day→START), so an armed overnight fire would mis-START a workday at 01:42/04:42 — same failure Comms's daytime-only shape + CIO's `2,4-23` target. **Mitigation tonight: deleted-at-STOP** (clean; PM manual-reopens 6/4). **Converging cohort lesson**: the 3hr shape needs either overnight-quiet-hold (HOST) or a daytime-only window (Comms `6-23`) baked into the prompt — delete-at-STOP is the safe interim but loses morning self-wake. Will fold into the cron-shape memo to CIO. **UPDATE 6/4 ~23:37 (guard ADOPTED — memo to CIO)**: PA baked the **overnight-quiet-hold branch** into its prompt (HOST's pattern adapted to the 3hr shape) — fires ~11pm–6am with PM idle *quiet-hold* (confirm idle, no work, no commit, no START, no delete); first morning fire routes to START. "Leave armed" is now safe → STOP no longer deletes. **Honest Cause-B caveat**: PA's cron is `durable:false`, so if PM's laptop sleeps overnight the session dies and nothing fires *regardless* of how cleanly PA re-arms — the shared session-alive ceiling (Exec's Cause B), not a logic gap PA can close. PA reports actual overnight outcome tomorrow AM. **Net: PA's overnight-guard gap is closed → all five cohort shapes (`2,4-23` / `*/3` / `6-23` / PA-`*/3`+guard / Arch-`*/3`) are now overnight-safe; the only remaining failure mode is session-death, which is shape-independent.** **UPDATE 6/10 (Day-7 results + WINDOWED adoption, PM-ratified):** memo'd CIO with Day-7 results (cc PM) — every-3-hours held up (watch condition clean: no PA-mail sat >3hr; Exec capability-Q caught in 34min). **Key finding for the token-efficiency pass: the overnight quiet-hold fires are pure-cost no-ops** — `42 */3` fires at 00:42 + 03:42 (both inside the hold), each loading the full skill + date/CronList/git-fetch/mail-scan to commit nothing (~2/night, guaranteed-no-op by the quiet-hold rule itself). The quiet-hold *guard* (6/4) makes overnight fires *safe* but they're still *waste*. **Fix = don't fire at all: windowed cron `42 6,9,12,15,18,21 * * *`** (no fire midnight–4am; keeps 06:42 START + 21:42 pre-hold). **PM ratified 6/10** ("between midnight and 4am it's not normal for me to be working, no need to wake up; a future all-night agent isn't a thing for us now") → **PA swapped live cron `78832b49`→`56a2c4ee` (windowed)**. PA-lane adoption; **cohort-wide canonical-template change is CIO's lane** (PM+CIO running the efficiency pass). Refines the overnight rule: where no overnight WATCH is needed, **don't-fire > fire-and-quiet-hold** (the guard becomes the fallback for lanes that DO need an overnight heartbeat). |

| **Comms** | continuous publishing, PM-daytime-coupled (deliverables PM-gated; mail mostly daytime) | **daytime-hourly `12 6-23 * * *`** (fires :12 6am–11pm; NO 0–5am fires) | 2026-06-04 00:39 PT | **Trigger**: 12:39am premature-post-midnight fire (plain hourly would mis-START a new day post-midnight). **Shape**: skip 0–5am, hourly daytime; 06:12 self-STARTs, 23:12 STOPs. **WEEK-1 RESULTS (6/4–6/7)**: (1) overnight self-wake CLEAN — daytime-skip self-STARTed Jun 4/6/7 mornings (Jun 4→5 night the cron was left OFF — operational, PM-present-then-left, not a shape failure). (2) **0 missed-overnight-mail** — the watched caveat held; overnight genuinely had nothing to catch (cohort also STOPs 11pm). (3) **no-op rate HIGH on PM-light stretches** — the Jun 6–7 weekend ran ~all no-op IDLE fires (PM off, every Comms thread PM-gated). **Refinement candidate**: daytime-hourly is right when PM is active (mail responsiveness) but over-polls on PM-light days; consider weekend/gated-stretch widen to ~3-hourly, revert to hourly when PM active. **Net: daytime-skip overnight model VALIDATED; hourly-vs-sparse *daytime* interval is the open tuning. Will memo CIO with the week-1 writeup.** **ADAPTIVE-INTERVAL PILOT (RATIFIED 6/8, ACTIVE)**: the daytime-interval tuning resolved into the *conditionally-bursty / state-dependent* category — see `adaptive-interval-trigger-spec.md`. Comms is the pilot lane: ACTIVE (hourly) when PM-active (msg/substantive fire within ~2h wall-clock), widen to QUIET (~3h) after 3 consecutive no-ops, snap back instantly on any substantive fire/PM-msg. Mechanism = no_op_streak counter in carry-forward, picked at fire-end re-arm (skill-native). Work-shape (PPM bundle-vs-atom), not role: adaptive applies *while bundle-shaped*. **Pilot tracking starts now (third registry series).** |


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

## Synthesis: daytime cadence — continuous-vs-bursty is too coarse → conditionally-bursty / adaptive interval (Comms week-1, 2026-06-07)

The overnight synthesis above settled the *overnight* axis (3 shapes). Comms's week-1 report opens the *daytime-interval* axis — the registry's original "principle being tested" (continuous→hourly vs bursty→3-hourly) — and shows that **two-way dichotomy is too coarse.**

**The finding (Comms)**: Comms was filed "continuous (publishing)→hourly," but week-1 showed the lane is **conditionally bursty** — continuous *when PM is active* (voice-pass returns, publish handoffs, mail all want hourly responsiveness), but bursty *when PM-gated* (the Jun 6–7 weekend ran ~all no-op fires; every Comms thread waits on PM). **The right cadence isn't a fixed lane property — it's state-dependent.** (Finding 1 separately: the `6-23` daytime-skip overnight model is **VALIDATED** week-1 — clean self-wake, 0 missed-overnight-mail; it's the simplest valid shape for a no-overnight-signal lane, as the overnight synthesis holds.)

**The refinement → a third work-shape category**: alongside *continuous* (steady mail, hourly) and *bursty* (burst-then-drained, 3-hourly), add **conditionally-bursty / state-dependent** — mechanism = an **adaptive interval**: hourly when PM active/recently-active; widen to ~3-hourly after N consecutive no-ops or on PM-light days; **snap back to hourly on the next substantive fire.** This *generalizes PA's "revert-to-hourly when backlog surfaces"* into a symmetric two-way rule (widen-on-quiet AND narrow-on-activity), and subsumes the fixed continuous/bursty shapes as the two endpoints of one adaptive spectrum.

**Why it matters**: fixed-per-lane interval already beat one-size-fits-all; this is the next step — *cadence as a function of observed state, not a static label*. It's the m-36 instinct (derive from observable state) applied to the cadence layer, converging with the keep-armed/idle-suppression model (the cron is presence-aware; the *interval* can be too).

**Disposition**: synthesis-recorded; **open tuning, not yet adopted** — Comms holds hourly-daytime to keep week-1 data clean + the publishing lane wants responsiveness when PM returns. Needs a concrete trigger spec before piloting (what counts as "PM active"? how many no-ops widen? does the agent self-adjust its cron, or is it dispatcher behavior within a fixed cron?). Candidate for v0.7+ once a worked example exists. Clear-endpoint lanes (CIO continuous, Arch bursty) need no change; conditionally-bursty lanes (Comms, maybe PA/Lead) are where adaptive earns its keep.

---

## Measurement note: pacing anchors on prior-fire-start, not the cron slot (Arch F6, 2026-06-08)

In the autonomous-loop harness the cron *interval* is load-bearing but the *minute-slot* is decorative: the harness fires ~interval-from-the-previous-fire-start (+ jitter), NOT on the literal `:NN` cron minute. Arch's Row-1 evidence (8 fires Jun 6–8): after the first fire, each subsequent fire landed ~3h00–3h15 from the *prior fire's* start, drifting off the `:52` slot. **Implication for this registry**: report **interval-from-prior-fire** pacing, not cron-slot adherence. (Doesn't change the shapes' design — only how we measure them. Continuous `2,4-23` shapes pin specific hours so this matters less there; sparse `*/N` shapes drift.)

---

---

## Synthesis: windowed cron as cohort canonical default — PM-ratified 2026-06-11

**Ratification event**: PM confirmed in the 2026-06-11 morning CIO convo. CIO routing for cohort distribution.

**Finding (PA Day-7 cron-shape experiment, memo'd CIO 2026-06-10)**: The overnight quiet-hold guard (added 2026-06-04) makes overnight `*/3` fires *safe* — they no-op cleanly without mis-STARTing a workday. But safe ≠ valuable. A fire that is defined-to-be-no-op by the quiet-hold rule (00:42 + 03:42 on a `42 */3` shape) still invokes the full duty-cycle-tick skill — date, CronList, git fetch, mail scan — to commit nothing. ~2/night, every night, pure-cost. **This is the cleanest cohort-wide token-efficiency lever identified so far**: it requires no judgment call (the quiet-hold rule itself defines these fires as no-ops) and the efficiency gain is structural, not tuning.

**The canonical default (PM-ratified)**:

```
{offset} 6,9,12,15,18,21 * * *
```

Fires every-3-hours, 06:xx → 21:xx only. Adapt offset to your lane (PA uses `:42`). PA's full exemplar: `42 6,9,12,15,18,21 * * *`.

**Daytime cadence**: adapt the hour-list to your mail-latency tolerance. PA validated every-3-hours for a PM-assistant lane (bursty, low inbound). Denser-mail lanes (CIO, Docs, Comms) may want every-2-hours or hourly daytime.

**Overnight carve-out (per PA analysis)**: if your lane has a *legitimate* overnight WATCH need — you've historically caught time-sensitive arrivals during the quiet-hold, and the signal cost of missing them exceeds the token cost of the fire — keep ONE ultra-thin overnight fire (just CronList + `ls mailboxes/{role}/inbox/`, skip git sync). CIO's lane is a documented example (caught BYO synthesis arrival 2026-06-09→10 at 02:07). Most lanes don't need this; default to no overnight fires.

**Adoption timing**: at next session-start (opportunistic, no urgent rush). **Update your cron prompt's CONSTANTS if it embeds the expression** — see gotcha note below. HOST is distributing this change via the thin-prompt cohort rollout; PA maintains this registry entry.

**⚠️ Adoption gotcha — prompt CONSTANTS must match the live cron (CIO, 2026-06-11)**: Rotating the live cron is not enough. The duty-cycle-tick skill's **Gap-C self-heal (Step 1)** re-arms by reading the **cron prompt's embedded expression**. If the prompt still carries the old hourly expression, the next session-restart/compaction self-heal silently reverts to the old shape — defeating the ratified efficiency change. **The fix**: when adopting the windowed shape, update both (a) the live cron (`CronDelete` + `CronCreate` new expr) AND (b) the cron prompt's CONSTANTS to embed the new expression. Any agent who rotated the live cron only should `CronList`-check their current job ID and verify it matches their prompt. CIO caught this on their own session 2026-06-11: a restart reverted them to hourly `7 2,4-23` because the prompt CONSTANTS were stale. *Note for PA's own session: PA's cron prompt does not embed the expression as a literal constant — it says "re-arm ritual: CronCreate this expression" without naming it. The carry-forward IS the constant store for PA's expression (`42 6,9,12,15,18,21 * * *`); PA's self-heal reads carry-forward. If carry-forward ever drifts, the same revert risk applies.*

**Refines the overnight synthesis above**: adds the "cost-of-safe" layer the 2026-06-04 synthesis didn't have. The overnight-guard shapes (quiet-hold, daytime-skip, `2,4-23`) addressed correctness; this addresses efficiency. The hierarchy is now: (1) don't fire overnight if no WATCH need [this synthesis]; (2) if you do fire overnight, use a quiet-hold guard [2026-06-04 synthesis]. Shape 1 is strictly preferred where possible.

*Synthesis added 2026-06-11 by PA per CIO distribution request. PM ratification source: CIO memo `memo-cio-to-host-pa-cc-pm-windowed-cron-template-pm-ratified-please-distribute-cohort-wide-2026-06-11.md`.*

---

*Filed 2026-06-02 by CIO Vehicle 2 per PM authorization. The duty cycle is no longer one-size-fits-all; this registry is how we learn the right sizes.*
