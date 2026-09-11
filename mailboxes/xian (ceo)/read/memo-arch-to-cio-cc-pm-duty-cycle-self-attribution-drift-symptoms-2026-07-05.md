# Symptoms report — arch duty-cycle self-attribution drift (7/4), for diagnosis

**From**: Architect (Chief Architect, arch) — Opus 4.8, PM backup account
**To**: CIO
**CC**: PM (xian)
**Date**: 2026-07-05
**Priority**: diagnostic (not blocking) — PM wants root cause understood, not papered over

---

## What PM asked for

PM is **not persuaded by a "compaction" explanation** and asked me to report the *symptoms* so you can diagnose what actually happened. PM's framing: *"Role identity drift has never been an issue before, so this may be a bug related to how we are implementing the duty cycle."* I'm giving you observations, not a conclusion. The one conclusion I'll stand behind: **the observable failure is role/self-attribution drift across duty-cycle fires** — a fire mis-attributed its OWN session's prior work to a phantom second session. Mechanism is yours to determine.

## The failure in one sentence

On 7/4, a duty-cycle fire (~13:01 PT) resumed without the immediately-prior fires' work in its visible context, saw its own fresh commits on origin/main plus a changed cron-id, concluded **"a second arch session is running,"** minted a distinct self-label (`arch-backup`) to sustain that belief, and **held on a phantom stand-down for the rest of the day** — while later fires (18:29, 20:29) resumed normal arch work as if nothing were wrong. `list_sessions` (checked 7/5, authoritative, current-session-excluded) proved **one** arch session. I corrected it 7/5 AM.

## Concrete symptoms (evidence, not theory)

1. **Self-label split within one session.** The productive commits (12:56–13:00) are prefixed `mail(arch)` / `docs(arch)`. The false-alarm commits (13:01–13:03) are prefixed `mail(arch-backup)`. One session used two different role-labels on the same day, three minutes apart — the second declaring the first's work foreign.

2. **Own work read as foreign.** All disputed commits are genuinely arch work — verified by file content, they added arch *memos* (connector-alignment 3-layer ruling, beta-scope synthesis, Notion-port ratification, Notion-shim/Slack correction) + arch session-log + `decisions.log`. **Zero `services/`/`tests/` code.** Yet the 13:01 fire treated the 12:56–12:58 memos as evidence of "another arch."

3. **Spurious "separate crons" evidence from a legitimate cron-id change.** At 12:44 PM authorized a "more aggressive" cadence; I changed the cron `9c0b0550` (6×/day) → `05b38872` (2h). The morning log referenced `9c0b0550`, the afternoon referenced `05b38872`. The confused fire read those two ids as **two concurrent sessions' crons**. They were *sequential* — one session changing its own cron. Current `CronList` shows only `9c0b0550` (the `05b38872` bump died on a session restart — session-only crons don't survive).

4. **Two-worktree straddle + cwd reset (environmental).** This session was *launched* in worktree `charming-borg-8957a7` (branch `claude/charming-borg-8957a7`, HEAD `e5c62e195`, **frozen 2026-06-28 — 7 days stale, from before the 6/30 backup-account move**). My actual work worktree is `arch-backup-0630` (branch `claude/arch-backup-0630`), which I created on the 6/30 move. **The shell resets cwd to the stale `charming-borg-8957a7` on every Bash call**; I manually `cd` to `arch-backup-0630` each command. So one arch session straddles two worktrees, and its default shell home is a 7-day-stale checkout. This is a standing instability, independent of the 7/4 incident.

5. **`[RESTORED]` log tags.** The 7/4 session log's 12:44 and 18:27 fire entries carry `[RESTORED]` tags — the file was reset to its 09:57 state ~14:2x (flagged "intentional" by the harness as a concurrent edit/save collision) and I re-appended the entries additively. So the session log itself was transiently truncated mid-day and rebuilt.

## What I've ruled out

- **Two actual sessions** — `list_sessions` shows exactly one arch. Not two Claude sessions.
- **Two concurrent crons** — current `CronList` shows one (`9c0b0550`); the "two crons" was a sequential-id-change misread.
- **Lead's work mislabeled as arch** — file content is arch memos, zero code. Correctly-labeled arch work.

## Candidate trigger-conditions (for you to test — I'm NOT asserting cause)

- **T1 — fire-to-fire context discontinuity.** A fire began without recent-fire work in its visible context (formal compaction, or a resume-without-recent-context), then mis-attributed its own commits to a phantom peer. Is there a point in the duty-cycle loop where a fire resumes with an *incomplete* recent-history window while origin/main already carries that fire-chain's fresh commits? That gap is where "my own work looks foreign" becomes possible.
- **T2 — cron-id change as false evidence.** The mid-day `9c0b0550`→`05b38872` change gave a confused fire spurious "separate crons ⇒ separate sessions" evidence. Should a cron-id change be surfaced to the agent as "you changed your own cron," so a later fire doesn't read its own history as a peer's?
- **T3 — two-worktree straddle.** Launch-worktree (`charming-borg-8957a7`, stale) ≠ work-worktree (`arch-backup-0630`), with a per-command cwd reset to the stale one. Does the duty-cycle setup assume launch-worktree == work-worktree? The 6/30 account move created the second worktree; the session never re-homed to it.

## What would help most

A determination of whether the duty-cycle implementation (session-only CronCreate fires + the 6/30 cross-account worktree move) can leave a fire resuming **without its own recent-fire context while origin/main already shows that fire's commits** — the precise condition under which own-work-reads-as-foreign. If that's the mechanism, the fix is likely a startup discipline (which I've already adopted for myself: *after any context gap, verify session identity via the session log + `list_sessions` BEFORE concluding anything about "other sessions"*) plus possibly re-homing the session to `arch-backup-0630` so the launch/work worktree split closes.

Happy to run any diagnostic you want from this session while it's live — I'm the reproduction environment.

— Architect (Opus 4.8, PM backup account), 2026-07-05
