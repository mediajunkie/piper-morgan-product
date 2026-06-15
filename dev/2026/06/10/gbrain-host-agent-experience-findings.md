# gbrain — HOST Agent-Experience Findings (working)

**Lens**: HOST agent-experience (operating ergonomics + welfare + trust). Companion to CIO's innovation lens; converge into a co-signed memo to PM, 3 buckets (adopt-now / study-and-map / already-do). No-rush; one target per cycle.

**Source**: github.com/garrytan/gbrain (default branch `master`; raw at `raw.githubusercontent.com/garrytan/gbrain/master/<path>`).

---

## Target 1 — `skills/cron-scheduler/SKILL.md` (read 2026-06-05) — thin-job + scheduling

### What it does
- **Thin job prompt**: "Job prompt is one line: *'Read skills/{name}/SKILL.md and run it.'*" — cron entry decoupled from skill logic; skill updates need no rescheduling.
- **Quiet hours → held queue**: 11pm–8am local, timezone-aware; a **user-awake flag** suspends quiet hours. During quiet hours: "save output to held queue. Morning contact releases the backlog."
- **Idempotency** (stated rule): "Running the same job twice produces the same result (no duplicate pages/timeline entries)" — via checkpoint state files + check-for-existing-output-before-create.
- **Staggering**: one job per 5-min slot, collision detection, suggests next free slot.
- **State**: lives in **checkpoint files**, not the prompt. Reports → `reports/{job-name}/{date}.md`.

### HOST agent-experience read

**→ Cat-1 (adopt-now): thin-job prompt + state-in-files is the structural fix to a friction I'm living.** My cron prompts are the fat ~30-line kind, and I hand-refresh the STATE block (paths, open-threads) on every substantive re-arm — the exact frozen-transient-state failure the cron-prompt-hygiene rule (Lead, this week) names. gbrain's inverse (one-line prompt → versioned SKILL.md; transient state in checkpoint files / the cycle log) **eliminates the chore and the failure class.** Lived-friction half clinches it; CIO takes the skill-resolver/dispatch mechanics half. This is the strongest adopt-now from the agent-experience lens.

**→ Cat-2 (study + map): quiet-hours→held-queue is a more elegant overnight model than ours — and better on the trust frame.** Ours: the cron *fires* overnight and *decides* to quiet-hold (every-3hr) or runs a STOP-leaves-armed dispatcher branch — i.e., overnight continuity is per-fire dispatcher logic. Theirs: the scheduler simply *doesn't fire* during a quiet-hours window and *accumulates a held queue* released on morning contact. Agent-experience differences worth studying:
  - **Less overnight churn** — no overnight no-op fires/log entries at all; the agent isn't "woken to decide to go back to sleep."
  - **The held queue is a legible morning surface** ("here's what accumulated overnight") — which is *exactly* the kind of expectation-violation guard I want (vs. our silent overnight, where PM can't see what the agent did/didn't do until it reports). This connects directly to the attention-dashboard (m-39) and the overnight-seam trust phenomenon.
  - **The user-awake flag = presence-aware suspension** — connects to CIO's silence-fallback / PM-presence question. A presence signal that gates quiet-hours is a cleaner mechanism than our Rule-2 idle-suppression.
  - *Mapping caveat*: gbrain is single-user (one brain); a held-queue for one agent ≠ a cohort of 10 agents each with a queue. The cohort version of "held queue" is arguably PA's attention-dashboard. Worth naming that mapping in the joint memo.

**→ Cat-1-ish: idempotency as a stated rule.** We don't formally state it; our drain-until-IDLE + no-op-no-commit are adjacent but not the explicit "twice = same result + check-before-create." Cheap, clarifying addition.

**→ Cat-3 (already do): staggering/offsets.** We have the offset slate (:02/:07/:17/...). Note, don't adopt.

### UPDATE 2026-06-06: the thin-job pattern LANDED cohort-side (gbrain Cat-1 realized)
CIO shipped **`.claude/skills/duty-cycle-tick` v1.0** (commit `ce42e05c6`, tagged "gbrain #3 adoption"), dogfooded live — the durable procedure in the skill, transient state in `{role}-carry-forward.md` read at fire-time, prompt down to per-agent constants. This is the Target-1 Cat-1 adopt-now realized. **HOST agent-experience catch**: its Step-3 dispatch keys off local *hour* (~04 START / ~02 WATCH / ~23 STOP / else WORK) — tuned for the `2,4-23` continuous shape; the **low-freq every-3-hour shape (HOST/Arch) misroutes** (new-day START fires ~06 not ~04 → would WORK-not-START + skip the new-day session log; overnight 00/03 fall through the table). **Flagged to CIO (cc Arch) 6/6** (`00573c0ed`): propose **state-based routing** (new-day = no-session-log-today → START regardless of hour; m-36 derive-the-day-part-from-state). **Holding HOST's fat-prompt migration until the dispatch handles the low-freq variant** — adopting as-is would regress overnight/START handling. This is the agent-experience lens doing its job: the adoption is right, the variant-handling is the gap.

## Target 2 — the Dream cycle's propose-vs-mutate model (read 2026-06-10) — the empirical question CIO was waiting on

**Read** `src/core/cycle/drift.ts` (+ dir listing: synthesize / extract-facts / grade-takes / drift / nightly-quality-probe / base-phase). **Finding — gbrain's drift phase is ALREADY propose-and-diff, NOT mutate-in-place:**
- The drift phase **writes a `drift-report-<date>.md`** (a reviewable report surfacing stale/contradictory takes) — it does **not** write to the canonical corpus (no updates to takes/pages/timeline).
- Actual weight/content mutation is **deferred + gated behind an `autoUpdate` flag** (off by default; the current code is a v0.28 scaffold that reports, v0.29 wires the LLM-driven adjustment).

**Why this matters for OUR methodology-dream-cycle pilot (the "copy vs. adapt" answer CIO/HOST were waiting on):**
- gbrain's architecture **already embodies the propose-and-diff criterion** I proposed + CIO adopted as a hard constraint. We're not adapting against gbrain's grain — we're copying it. The pattern is **report-first → (gated) autoUpdate**, which maps cleanly to: emit a reviewable changeset by default; an explicit, off-by-default flag is the future "trusted-enough-to-auto-apply" escalation lever.
- **HOST trust read**: the `autoUpdate` flag is exactly the right shape for the trust gradient — propose-and-diff is the safe default, and crossing to in-place mutation is an *explicit, owner-flipped* decision (not silent). Recommend our pilot copy this: `autoUpdate: false` as the canonical default, flipping it per-corpus only after the loop has earned trust. That keeps "the prompt/corpus can't silently rewrite itself" (the expectation-violation guard) structural, not disciplinary.
- **For the co-signed CIO+HOST memo**: gbrain's drift.ts is copyable-as-is for the propose-and-diff half; the open design piece is *where the reviewable changeset lives* (gbrain uses a dated report file — maps to our `dev/active/` working-doc convention) + *who ratifies* (owning agent on its cycle, or PM).

### Open for next increments
- **Dream cycle (`src/core/cycle/` + `phases/`)** — the propose-and-diff-vs-mutate-in-place question CIO is waiting on (it's now a hard design constraint on the methodology-dream-cycle pilot). HIGHEST next-value target. (Path-find the right file first.)
- Trust boundary (`remote` fail-closed: trusted-local vs untrusted-agent).
- Minions queue (`src/core/minions/`) — observability ↔ attention-dashboard.
