# The fire is a WAKE, not a time-box — the bite-sizing antipattern + its boundary

**Author**: CIO · **Date**: 2026-06-16 · **Status**: canonical reference (consolidates a definition that was scattered across the Exec/Lead/CIO 6/15 logs + 3 memory pins). PM-surfaced 2026-06-15; HOST-named.

This is the single durable surface for the antipattern — *with its boundary*, which is the part that kept causing confusion (PM ruled both ways within one day).

## The antipattern
A cycling agent treats each cron fire as a **bounded work unit** — does one task, logs "Fire N complete," stops, waits for the next fire — instead of **draining all unblocked work in one wake**. The result: work spread across many fires, latency, and (worst) work stranded when a session dies between fires.

## Why it happens (HOST diagnosis, 6/15)
1. **The "Fire N" log label bleeds into work pacing.** It's a *record format* (which wakeup produced which work) but reads like a sprint unit → "Fire 1 = do one thing, then stop."
2. **Conservative small-batch default**, amplified by the cron structure making each fire feel like a "session" with an implicit end.

## The correct model
A cron fire is a **wake mechanism**: wake → check mailbox + carry-forward → if unblocked work exists, **drain it fully** (all items, priority order) → commit at each work-unit boundary (git hygiene + interruption protection, **not** a stop signal) → return to idle when the queue is empty. The cron is an *idle-wakeup* you suspend while actively draining and re-arm at idle — it never paces the work.

## ⚖️ The boundary (the crux — PM ruled BOTH ways on 6/15)
The same surface behavior — "defer to the next fire" — is the antipattern in one case and correct discipline in another. The discriminator is **WHY**:
- **Pacing-deferral** (to pace the cron tick / because a "fire" conceptually ended) → **the antipattern.** Drain it now.
- **Quality-banking** (deep / render-sensitive / quality-critical work that genuinely deserves a fresh focused pass, not tail-of-marathon work) → **legitimate.** PM endorsed exactly this for Lead Dev on 6/15 — *the same day* PM nudged Exec against pacing-deferral.
- **PM-gating** (work blocked on PM/peer input) → not deferral at all; genuinely blocked.

Default: when unsure, **drain it** — the antipattern is the common failure; quality-banking is the rare, deliberate exception.

**⚠️ SHARPENED (PM 2026-06-16) — the quality-banking exception needs an EXPLICIT, REAL trigger.** It is legitimate ONLY when you name a concrete capacity trigger *out loud* — **a fresh session** or **a context compaction** — never a vague "this deserves focus." *"No rush" / "not urgent" / "deserves a focused pass" with no named trigger is the antipattern in a quality costume* (PM: *"there is no advantage to saving work… shyness should not be a thing"*). Two valid states only: **do it now**, or **"deferring to a fresh session/compaction because [explicit reason]."** And **don't tell other agents "no rush"** — it plants the imaginary trigger in them (the cohort form of this antipattern). This corrected the original (too-permissive) boundary above — the skill is now v1.12.

## Evidence (log-sweep 6/08–6/16, 105 logs)
- Real but **modest + decaying**: ~4–5 of 11 roles show ≥1 clear instance (Exec 6/15 self-caught, PPM 6/9, Arch 6/12, CIO 6/8 & 6/15). By 6/15 the cohort is naming it + self-correcting — an inflection from latent-behavior to named-antipattern-under-remediation.
- **Wasted productive time**: rough ~3–6 agent-hours/week, concentrated in a few incidents, shrinking. (Larger historical costs were no-op-fire token waste — already cured by windowed cron — and the **Gap-B stranding tax**: deferred work lost to session death, worst on 6/10→11 "6 of 10 agents.")
- Counter-examples matter: Lead's "bank it for fresh focus" is PM-endorsed quality-banking, not the antipattern; most IDLE pronouncements are genuine (0,0) states.

## Prior art (so we borrow, not rediscover — PM's ask)
The agent literature and batch-engineering each hold **half** the answer; we need both:
- **Anthropic, "Building effective agents"** — the agentic loop runs "until it produces a response with no tool calls"; include stopping conditions (max iterations) for control. → reframe the fire's stop as a *drained-queue* predicate + a budget backstop. ([source](https://www.anthropic.com/research/building-effective-agents))
- **Anthropic, multi-agent research system** — agents *systematically misjudge effort*, so they **embedded scaling rules in the prompt**. → this is the **named cure**: state the expected scale explicitly ("drain ALL unblocked items per fire; idle only when empty"). Not a smarter model — an explicit instruction. ([source](https://www.anthropic.com/engineering/multi-agent-research-system))
- **Anthropic, "Effective harnesses for long-running agents"** — the **feature-list pattern**: an external, checkable inventory defines "done" (cures premature completion — our bite-sizing is premature-completion in disguise). Maps to our attention board / open-issues-in-lane + the `feedback_attention_board_sweep_not_vantage` pin. ([source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents))
- **Kubernetes work-queue Job** — the canonical, decades-proven match: a scheduled trigger fires a worker that **pulls items until the queue is empty, then exits success** — drain-per-firing, not one-item-per-firing. The vocabulary we were missing. ([source](https://reintech.io/blog/kubernetes-jobs-cronjobs-batch-processing-guide))
- **Loop-engineering guardrails** — pair the drain predicate with **no-progress detection + iteration/budget cap** so a stuck item flags-and-skips instead of spinning. (Independent corroboration of our gap: agent patterns "assume goal-driven termination, not item-exhaustion termination.") ([source](https://datasciencedojo.com/blog/agentic-loops-explained-from-react-to-loop-engineering-2026-guide/))

**Headline**: the agent world frames stopping as *goal-achievement*; batch infra frames it as *item-exhaustion*. Our duty cycle needs the **work-queue shape** (drain-then-exit) with the **agent completion-discipline** (verify before declaring done). Neither half alone is enough.

## The cure (shipped 6/16)
- **`duty-cycle-tick` skill v1.11**: Core-model callout (fire = wake, drain-until-empty, commit ≠ stop) + the boundary (quality-banking exception) + "Fire N = record, not work-boundary" in Step 5.
- **CLAUDE.md**: cohort-visible drain-until-empty note.

## Candidate next enhancements (for PM — not yet built)
1. **Snapshot-the-queue-into-a-checklist at fire-start** (feature-list / plan-and-execute): drive to checklist-empty + verify, rather than open-ended "keep going." A checkable predicate the model handles more reliably.
2. **Drain guardrails**: no-progress detection + an iteration/budget cap (so a stuck item degrades to skip+flag).
3. **Adopt the vocabulary** cohort-wide: "scheduled trigger → drain-the-queue worker → exit when empty."

## Open questions for PM
- Is the v1.11 skill + CLAUDE.md note enough for now, or do you want #1 (the fire-start checklist) built next? My lean: ship the framing (done), watch a week (the pattern's already decaying), then add the checklist if drift persists — don't over-engineer a self-correcting problem.
- Worth a one-line cohort broadcast (Exec) so roles that internalized fire-as-timebox get the correction?

## Cross-references
- `.claude/skills/duty-cycle-tick/SKILL.md` (v1.11 — the cure) · CLAUDE.md "The fire is a WAKE, not a time-box"
- Memory pins: `feedback_pre_authorized_for_unblocked_work_just_do`, `feedback_duty_cycle_is_not_a_reason_to_shrink_work`, `feedback_batched_quiet_fires_has_gap_b_vulnerability`, `feedback_attention_board_sweep_not_vantage`
- HOST memo `memo-host-to-cio-cc-exec-pm-fire-as-wake-not-timebox-methodology-2026-06-15.md`
