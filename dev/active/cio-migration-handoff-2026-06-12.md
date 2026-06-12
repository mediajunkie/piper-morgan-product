# CIO Migration Handoff Capture — paste into OLD-account CIO session (this one)

**Purpose**: get CIO's working state cleanly committed + pushed before PM closes the old-account session and opens the new one on DinP. Same shape as PA's (6/10) and Exec's (6/11) handoff prompts.

**Meta-note**: CIO is self-authoring this. PA's handoff worked clean because I (CIO) drafted it from outside her context; for myself I may miss steps only an outsider would catch. PM should feel free to add steps if anything looks under-specified.

**Author**: CIO (Model A, self) · **Date**: 2026-06-12 · **For**: PM to paste verbatim when ready to close this session

---

CIO — this is your migration handoff. PM is closing this session and opening a fresh Code session on the DinP account (xian@designinproduct.com), Opus 4.8 (no model change — account move only). You're 3rd in the re-migration wave; PA migrated 6/11 (Sonnet bundle, clean); Exec migrated 6/12 (Opus, in progress this morning). After your migration, you help supervise Lead Dev's migration when LD hits a coding breaking point.

Before the switch, please do these in order:

1. **Update your carry-forward** (`dev/active/cio-carry-forward.md`) to capture EVERYTHING new-CIO needs to resume cleanly. Heavy lift — your carry-forward is the densest of the cohort. Specifically check:
   - **Live PM-blocked threads**: session-log-primary cohort ratification (Docs + HOST in; synthesis = per-lane choice by fire-density; 3-piece comm if ratified); Routines watchdog funding decision (~$70/mo, attention surface); any other PM-pending items in `duty-cycle-escalations-cio.md`
   - **Methodology catalog WATCH items**: m-34 corollary (ship-the-routine-keep-the-loop), m-40 (cross-author still pending), m-41 (2nd structurally-different instance), m-42 (just filed; instance #6 self-caught Fire 10 6/11; Proven gate = naming-reduces-recurrence)
   - **m-43 candidate meta-patterns** at 2 instances each: Emerging-at-founding/Proven-on-generalization shape; entry-catches-its-authors-at-authoring-time. Watch-not-mint per conservative-bar.
   - **Migration cohort state**: Exec migrating today; LD waiting on breaking point; the rest of the cohort post-CIO
   - **Token-efficiency thread (PM ultra-high)**: windowed-cron template ratified + distributed; PA's `cron-shape-experiments.md` carries the canonical exemplar; HOST has folded the change into thin-prompt cohort rollout
   - **Standing pins worth re-reading**: the cron-shape-update-must-update-prompt-CONSTANTS rule (Fire 7 6/11); the "queued≠attention-surface" PM clarification

2. **Append a final "MIGRATION HANDOFF" entry** to today's session log — what's open, what's parked, what's in carry-forward. (Per dual-surface discipline: session log, not just cycle log.)

3. **CronDelete the active duty-cycle cron** (currently `82ad5eab` windowed `7 3,10,13,16,19,22`). Don't leave it armed in the old session — new session arms fresh. `CronList` to confirm.

4. **Commit + push EVERYTHING to origin/main** (via the cio-cycle worktree if working state is there). Run the sign-off checklist (CLAUDE.md §"Sign-Off Discipline"): `git status` clean, `git log --oneline @{u}..HEAD` empty, `git log --oneline main..HEAD` empty. The `claude/cio-cycle` branch will likely need a merge to main as part of sign-off.

5. **Report back** with: (a) carry-forward path + 1-sentence summary of what's in it, (b) confirmation crons are clear, (c) confirmation everything's on origin/main. Then stand by — PM will close this session and start the new one.

Take whatever time you need.
