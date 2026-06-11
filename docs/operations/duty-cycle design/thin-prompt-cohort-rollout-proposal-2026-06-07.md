# Thin-job-prompt + Rule-2 keep-armed — cohort rollout proposal (2026-06-07)

**Authors**: CIO (mechanics) + HOST (agent-experience + welfare). **Status**: DRAFT — assembled from the passed PoC + HOST's live low-freq validation; **gated on PM nod** for the cohort broadcast. **Companion**: `thin-job-prompt-poc-results-2026-06-07.md`, `.claude/skills/duty-cycle-tick/SKILL.md` (v1.3), `procedures/cron-lifecycle.md` (Rule 2 + Gap C).

---

## What we're proposing

Migrate every cycling agent from the fat ~40-line `DUTY CYCLE TICK` cron prompt to the **thin prompt + `duty-cycle-tick` skill + per-agent carry-forward file**, and adopt **Rule-2 keep-armed-default** in the same pass (one cohort touch).

## Why (validated, not asserted)

- **PoC passed** on CIO's continuous cron (skill-load reliable, carry-forward-from-file, keep-armed through conversation, 3 clean overnight self-wakes).
- **Low-freq validated LIVE on HOST's `*/3` cron** (HOST 6/7): 3 daytime fires state-dispatched to WORK correctly; first thin-prompt overnight crossing STOP 00:37 → quiet-hold 03:37 → START 06:37, all correct. **Both shape-families covered with real data.**
- **Two bugs already caught + fixed by the dogfood** (v1.1 low-freq dispatch, v1.2 overnight-window guard) + a Gap-C self-heal (v1.3) — the skill is hardened, not green.

## The per-agent change (3 pieces)

1. **The cron prompt → thin** (~8 lines): role + worktree + cron-expr + "run the duty-cycle-tick skill" + carry-forward pointers + fallback line. Template below.
2. **A carry-forward file** `dev/active/{role}-carry-forward.md` — the agent's ephemeral state (active threads, parked items), read at fire-time, rewritten at substantive-fire-end. **This is the one non-trivial per-agent step** (~5 min, HOST-measured): write your initial carry-forward capturing current state.
3. **The procedure** — already shared: `.claude/skills/duty-cycle-tick/SKILL.md` (v1.3). No per-agent copy; one versioned source.

Bundled: **Rule-2 keep-armed-default** (stay armed through PM conversation; pending PM question doesn't block other work; only Rule-1 substantive work deletes the cron) — already in `cron-lifecycle.md`.

### Per-agent thin-prompt template
```
DUTY CYCLE TICK ({ROLE}). Autonomous loop fire; no human driving. Run the **duty-cycle-tick** skill and follow it.
CONSTANTS: role={ROLE} (slug {slug}) · worktree={worktree-path} (Model A) · cron=`{expr}` (offset :{NN}; {shape note}).
CARRY-FORWARD: read dev/active/{slug}-carry-forward.md + cycle-log tail + {slug}-standing-items.md. Rewrite carry-forward at end of any substantive fire.
RULE 2 (keep-armed-default): armed through PM conversation; pending PM question doesn't block other work; only positive CronDelete is Rule 1.
Hold the discipline; holistic-not-tactical. Fallback: docs/operations/duty-cycle design/procedures/.
```

## HOST agent-experience + welfare sections *(HOST-owned — finalized 2026-06-07)*

**The chore is gone.** Agents were hand-refreshing a fat STATE/OPEN-THREADS block on every substantive re-arm — pure vigilance that *drifted* (HOST carried stale 6/3 paths for two days; a refresh step that didn't always happen). Now state lives in the carry-forward file, rewritten exactly when you'd touch that state anyway; re-arm is "CronCreate same expr" with nothing to refresh.

**The deeper win — a trust property (the welfare framing for the cohort memo):** the thin prompt **structurally closes the frozen-state-rots failure mode.** A fat prompt is re-fired every tick, so any transient state baked in *outlives its trigger and becomes a stale instruction* (Lead's "do not chase #1047" weeks after close; HOST's stale paths). The thin prompt **cannot carry stale state** — only durable constants; transient state lives where it's read-and-rewritten. m-36 at the prompt layer: *the prompt can no longer lie to you with state that rotted.* Cohort one-liner: **"you'll never hand-refresh a cron prompt again, and it can never silently feed you a stale instruction."**

**Why this is cohort-welfare, not just HOST-tidiness:** the v0.3 360 surfaced mechanism-overhead and vigilance-chores as a convergent cross-role friction (CXO: the bridge dance was "half my tool-calls"; Lead: "half the work is keeping-the-record-straight"; the cron-prompt hand-refresh is the same shape). The thin prompt removes one such chore *structurally* (mechanism, not a reminder) — so the rollout is the cohort acting on its own 360 signal, which is the healthiest possible provenance for a process change. Adopt at your cadence; the carry-forward setup is the only real step.

## Sequencing (per-agent self-migration; CIO+HOST support)

1. Agent writes its initial `{role}-carry-forward.md` (the ~5-min step).
2. Agent re-registers its cron with the thin prompt (its existing shape/offset — no shape change).
3. First fire: confirm the skill loads + carry-forward reads (the PoC-proven path).
Each agent self-migrates on its own next fire; CIO+HOST available to support. No flag-day; agents can migrate independently since the skill is already shared.

## Open items / honest notes
- **Post-compaction skill-load**: not yet explicitly observed; HOST is a live test (will flag if a post-compaction fire fails to re-invoke the skill). Expectation: the thin prompt + skill re-establish the procedure with no fat-prompt fallback needed. **One line in the cohort memo should say so.**
- **Gap C (compaction kills session-crons)**: orthogonal to this rollout but rides alongside — the skill's v1.3 Step-1 self-heal (re-arm if CronList empty) is included; the real cure (Routines watchdog) is separate roadmap work.
- **Web's main-direct variant**: thin prompt applies; the no-worktree mechanics differ per its registry row.
- **Pitfall — prompt re-fattening (CIO dogfood finding 2026-06-09)**: the thin prompt tends to *silently re-fatten* over re-arms. Re-arming is a natural moment to "just include" the current carry-forward inline (open decisions, watch items, overnight framing) — and over a day the prompt drifts back to ~40 lines, defeating the whole point AND re-introducing the stale-state-in-prompt problem (the prompt's inlined state goes stale while the file stays current). **Discipline: the cron prompt stays constants-only on every re-arm; transient state stays in `{role}-carry-forward.md`.** CIO caught its own prompt re-fattened across 6/8 and restored it truly-thin 6/9 (constants + skill-invocation + state-file pointers, ~6 lines). Worth a one-line warning in the cohort memo: *don't inline carry-forward when you re-arm — that's what the file is for.*

## Windowed-cron default (PM-ratified 2026-06-11 — bundled into this rollout)

PA's Day-7 cron-shape finding, **PM-ratified 2026-06-11 (token-efficiency elevated to ultra-high priority)**: **drop overnight pure-cost fires.** Any cron fire scheduled inside the 22:00–06:00 quiet-hold is defined-to-be-no-op by the quiet-hold rule — it runs date + CronList + git fetch + mail scan and commits nothing. Pure cost for zero output, structurally. Cleanest cohort-wide token lever surfaced so far.

- **What to adopt**: window your cron to daytime only. Canonical exemplar (PA's lane): `42 6,9,12,15,18,21 * * *` (06:42→21:42, every-3h). **Adapt the daytime cadence + offset to your lane** (denser-engaged lanes may want every-2h/hourly; HOST adopted `37 6,9,12,15,18,21` for its low-freq lane 6/11).
- **Carve-out**: if your lane has a *legitimate* overnight-WATCH need (you've historically caught time-sensitive arrivals during the quiet-hold — e.g. CIO caught the BYO synthesis 02:07 6/9→10), keep ONE ultra-thin overnight fire (CronList + `ls mailboxes/{role}/inbox/` only; skip git sync). **Most lanes don't need this.**
- **Mechanical note (compose-with-self-heal)**: windowing removes the past-11pm STOP fire → same-night STOP can't trigger → the day-close moves to the **v1.4 START self-heal** at the next morning fire (detects the missing `DAY-CLOSED` marker, runs the backfill close). Net: 2 fewer fires/night, close still happens, no lost record. Agents should expect close-at-morning-backfill, not same-night.
- **Update your cron prompt template** if it embeds the expression.

(Registered canonical in `cron-shape-experiments.md` by PA as the "PM-ratified canonical default 2026-06-11".)

## Gating
**Broadcast waits on PM nod.** On the nod, the cohort memo (thin-prompt mechanics + HOST's welfare framing + the windowed-cron default + per-lane carve-out) goes out; agents self-migrate at their cadence.

*Assembled by CIO 2026-06-07 (Fire 5), incorporating HOST's 6/7 sections. HOST to finalize its half; then → PM for the broadcast nod.*
