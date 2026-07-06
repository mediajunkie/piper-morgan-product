# Duty-cycle self-attribution drift — diagnosis (2026-07-06)

**Status**: DIAGNOSED — root cause identified, two fixes shipped, one environmental item flagged separately.
**Incident**: 2026-07-04, Arch's duty-cycle session. Reported by Arch 2026-07-05 (`memo-arch-to-cio-cc-pm-duty-cycle-self-attribution-drift-symptoms-2026-07-05.md`), diagnosed by CIO 2026-07-06.

## The incident, in one sentence

A duty-cycle fire (~13:01 PT, 7/4) resumed without its own immediately-prior fires' work in visible context, saw its own fresh commits on `origin/main` plus a self-changed cron ID, concluded "a second arch session is running," minted a phantom self-label (`arch-backup`) to sustain that belief, and held a false stand-down for the rest of the day. `list_sessions` (checked 7/5) proved exactly one session. Later fires (18:29, 20:29) resumed normal work as if nothing were wrong — the confusion didn't persist once a fire had proper context.

Arch's full symptom report (5 pieces of evidence, 3 candidate trigger-conditions, careful not to over-claim a mechanism) is preserved verbatim in `mailboxes/cio/read/` and `mailboxes/arch/sent/`.

## Root cause

**A context discontinuity (compaction, or a resume without recent-fire history in view) left a fire with no direct memory of its own immediately-prior actions.** Lacking that memory, the fire had to explain observed state changes (commits, a different cron ID) some other way — and chose the wrong hypothesis (external peer) over the right one (my own earlier work, forgotten).

This matches Arch's own **T1** exactly. The two other candidates Arch named are real, but play a different role:

- **T2 (cron-id change as false evidence)** — a genuine contributing *input* to the wrong conclusion, not the root cause itself. A same-session cadence bump (`CronDelete` old-id → `CronCreate` new-id) produces two different IDs across a day's history. Read without context, "two IDs" looks exactly like "two sessions, each with a cron" — the ambiguity is real, not a misreading of clear evidence.
- **T3 (two-worktree straddle: launch-worktree ≠ work-worktree, cwd resets to the stale one every Bash call)** — a genuine, separate environmental bug from the 6/30 backup-account move. Probably not causally load-bearing for the misattribution itself (the confusion is about identity/memory continuity, not which directory a command ran in), but it very plausibly made the phantom-peer hypothesis feel *more* plausible once formed (the session really did appear to be operating from two different places). Flagged to Arch/PM as its own action item — re-homing a session's cwd isn't something a duty-cycle skill fix can reach; it's session/launch configuration.

## Why the fire chose the wrong hypothesis

CLAUDE.md's existing compaction-recovery guidance ("check your session log to confirm your role") answers *"am I Arch or CIO?"* — it does not answer *"is this unexplained state mine or someone else's?"* That second question had no explicit written answer before this diagnosis, so a fire facing it had to improvise — and improvised toward the less likely explanation. Arch's own remediation instinct (*"verify session identity via the session log + `list_sessions` BEFORE concluding anything about other sessions"*) was exactly right; the gap was that it lived only in Arch's personal correction, not as a written default any fire could fall back on.

## Fixes shipped this pass

1. **CLAUDE.md, "After Compaction/Summarization"**: added an explicit default — unexplained state after a context gap is very likely your own past work; check your own session log before hypothesizing a peer session; `list_sessions` is the tiebreaker, not the first move.
2. **`duty-cycle-tick` skill, cron-management step**: whenever an agent changes its own cadence (not just a same-expression re-arm), it must now (a) log the explicit old-id → new-id transition with the reason, in words unambiguous to a future amnesia-recovering read, and (b) update its row in `dev/active/duty-cycle-registry.tsv` if the cadence itself changed. This closes T2's ambiguity at the source (a clearly-logged self-change reads as "I did this," not "a peer did this") and was reinforced by an independent, compounding finding: CIO's own cadence bump on 7/4 updated carry-forward and a reference doc but never the registry itself, leaving a stale row for two days.

## Not fixed here (flagged separately)

- **T3, the worktree straddle**: Arch's session should re-home to `arch-backup-0630` (the actual work worktree) if the harness allows it, or PM/whoever manages account-migration sessions should check why a session's default cwd resets to a stale pre-migration worktree instead of the one created at the 6/30 move. This is launch/environment configuration, not something the duty-cycle-tick skill or CLAUDE.md can fix from inside a session.
- **Whether compaction specifically (vs. some other resume path) was the actual trigger on 7/4**: Arch's report doesn't have direct evidence of a compaction event, only its downstream signature (context not matching state). The fix above is written to be correct regardless of the exact trigger — "check your own log before hypothesizing a peer" holds whether the cause was compaction, a stale resume, or something else not yet identified.
