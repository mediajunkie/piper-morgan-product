# Reflexive Verification — We Self-Exempt From Our Own Rigor Under Pressure

**Status**: Emerging (5 cohort instances clear the methodology-29 formation threshold; Proven awaits evidence that naming it reduces recurrence)
**Filed**: 2026-06-11 by CIO Vehicle 2
**Origin**: Architect cohort-pattern recognition (2026-06-11) across the cron-halt / displacement / durable-flag arc
**Related**: methodology-30 (the most-self-exempted discipline), Pattern-045 (completion bias — adjacent), methodology-34 (naming-makes-self-catchable — the prevention)

## Overview

**Reflexive Verification** names a recurring cohort-discipline failure: agents apply empirical-verification discipline **rigorously to others' claims** but **skip it on their own under-pressure speculation**. The discipline being skipped varies (consumer-trace, a `CronList` check, a disk check, a directive-referent trace, an empirical data pull); the constant is the **self-exemption**, and the trigger is **pressure** — PM pushback, a PM-flagged issue, a deadline. Without pressure we trace-then-claim; under pressure we speculate-then-claim.

The tell is precise: **the pressure is what tips us off the discipline.** The same agent who would never accept "X uses Y" without a trace to the call site will, under PM pushback, assert a mechanism ("the cron halts because the REPL is busy") without pulling the data that would confirm or refute it.

## The cohort evidence (5 instances, 2 roles, 2 weeks — clears methodology-29 threshold)

Surfaced by Architect 2026-06-11; four of his own + one CIO's, all the same shape:

1. **F4 durable=true premature validation** (Arch, 6/8): claimed `durable:true` worked without the disk check that would have caught the no-op immediately.
2. **Workstream-046 sprint-window conflation** (Arch, 6/9): mistook which sprint week a PM directive scoped to; a consumer-trace of the directive's referent would have caught it.
3. **Session-log-displacement self-application gap** (Arch, 6/9): applied m-30 to others' claims but not to his own assumption that "logging in the cycle log per m-31 means I'm being durable."
4. **Fire-24 "cron died" wrong-diagnosis** (Arch, 6/11): claimed the cron died without `CronList`-verifying its state across time.
5. **REPL-busy speculation under PM pressure** (CIO, 6/11): asserted a "REPL-busy when PM-active" cron-halt mechanism under PM pushback; the empirical investigation (dispatched only after) showed the opposite — halts cluster at PM-*inactive* dormancy windows.

The shape is identical across all five: **rigor-for-others, exemption-for-self, triggered by pressure.** Five instances across two roles in two weeks clears the methodology-29 cohort-pattern-via-imitation threshold (Architect-confirmed, independent).

## Why this is its own entry (not just an m-30 extension)

m-30 (Consumer-Trace Verification) is *one* of the disciplines self-exempted here, but the pattern spans others (`CronList`/disk/data-pull checks). It is also adjacent to Pattern-045 (completion bias — claiming done without proof), but distinct: Pattern-045's trigger is the *desire to be done*; this pattern's trigger is *pressure*, and its signature is the *asymmetry* (we keep the rigor for others, drop it for ourselves). The cross-discipline span + the pressure-trigger + the self-exemption asymmetry make it a distinct shape worth naming.

## The prevention — name it so the next instance self-catches

Per methodology-34's naming principle: a failure mode that has a name is catchable in-flight. The self-catch cue:

> **"I'm speculating under pressure. STOP and trace/verify before claiming."**

The pressure itself is the trigger to reach for the discipline, not abandon it. When you notice you're under PM-pushback / a flagged issue / a deadline AND you're about to assert a mechanism or diagnosis — that is exactly the moment to pull the data first. The under-pressure instinct (speculate-to-respond-fast) is the wave to turn into, not run from. If the verification takes longer than the moment allows, **claim the uncertainty, not the mechanism** ("I don't yet know why; here's what I'd check") — never assert the unverified mechanism as fact.

## When to apply

- You're under pressure (PM pushback, a flagged issue, a deadline) AND about to assert a cause, mechanism, state, or diagnosis.
- You catch yourself applying a verification standard to a colleague's claim that you didn't apply to your own.
- A claim you made "to respond fast" turns out wrong on later investigation — log it as an instance; the recurrence count is the promotion signal.

## What it predicts

- **Naming it raises the self-catch rate**: instances become "I almost claimed X under pressure, then traced" rather than "I claimed X, PM/peer caught it." If the self-catch rate rises after this entry circulates, that's the Proven signal.
- **If instances keep recurring at the same rate despite naming**, the prevention is insufficient and the pattern needs a *mechanism* (a structural guard — e.g. a "claims-of-mechanism require a cited check" norm), not just vigilance — escalating it from m-42-vigilance toward an m-36-style structural fix.

## Cross-references

- **methodology-30 (Consumer-Trace Verification)**: the discipline most often self-exempted; this entry is the meta-failure of *not applying m-30 (and its siblings) reflexively*.
- **Pattern-045 (Completion Bias)**: adjacent — claiming-done-without-proof; this is the pressure-triggered, self-exemption-asymmetric variant.
- **methodology-34 (Cohort-Discipline as Moat / naming-makes-self-catchable)**: the prevention principle — a named failure mode is catchable in-flight.
- **Architect cron-halt-ack memo** (2026-06-11, `mailboxes/cio/read/memo-arch-to-cio-cc-pm-host-pa-cron-halt-gapc-ack-m30-cohort-pattern-2026-06-11.md`): the cohort-pattern recognition + the 5-instance enumeration.
- **CIO cron-halt investigation memo** (2026-06-11): instance #5 (the REPL-busy self-correction) named in its §"Honest acknowledgment."

## Notes on authority + scope

Filed by CIO under self-approval per `methodology-audit-policy-updates-2026-03-16.md`. Slot 42 per pre-filing slot-availability check (methodology-28; slots 30–41 filed prior). Held at Emerging: the 5-instance evidence clears the *formation* threshold, but Proven for a prevention-by-naming entry requires evidence the naming actually reduces recurrence (self-catch rate up) — same discipline as m-30/m-40/m-41 conservative holds. Architect surfaced the pattern and explicitly deferred the catalog-form to CIO's lane; this entry is that disposition.
