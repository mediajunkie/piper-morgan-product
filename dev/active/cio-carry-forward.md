# CIO Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the duty-cycle-tick skill. Holds the genuinely transient "where am I right now" state. Durable owed/queued items live in `cio-standing-items.md` (the Task List); PM-attention items live in `duty-cycle-escalations-cio.md`.

## 🎆 7/6 Mon — current state (resumed after a self-caused 2-day gap)

**Cadence**: resuming at LEAN `7 10,16,22` (3×/day) — the 7/4 bump was explicitly today-specific and expired; migration checklist (`docs/migration/pipermorgan-ai-account-migration.md`) is STILL fully unconfirmed as of 7/6, so the migration hold's reasoning is unchanged. Do not bump again without a fresh PM ask.

**The gap**: stalled after 7/4 19:30 (Fire 6), missed the 22:07 fire, all of 7/5 passed with zero CIO activity (watchdog-flagged). Retroactively closed 7/4 on resume. ~121 cohort commits happened during the gap — NOT individually reviewed; handled via targeted mail-triage + a bounded BRIEFING refresh instead of reading everything.

**Migration facts (PM-confirmed 7/6)**: no Piper Morgan role has moved to pipermorgan.ai yet — this session included, confirmed on `designinproduct.com`. Coral (One Job, Fable model) is the only live pipermorgan.ai instance, a different project. Piper Open/Vergil are on KindSys.us, closing end of July (unrelated). Migration doc updated with a duty-cycle continuity assessment — mechanics already migration-safe, ready whenever Exec sequences it.

**Bash allowlist added** (PM-approved): `sync-pm-local.sh` can now auto-run in autonomous sessions (`.claude/settings.json`).

**Significant self-correction (7/6)**: `ROLE-PORTFOLIO-CIO.md` sat stale 20 days; #972 was actually CLOSED 6/18 and gbrain co-signed 6/16, both mis-reported as "slipped"/"owed" in Ship #049 AND Ship #050 (sent same morning, before this was caught). Sent an urgent correction to Exec/PM/PA before Ship #050 synthesis. Portfolio doc + standing-items fixed. **Lesson for future workstream reviews: `gh issue view` before writing "slipped," don't just trust the portfolio doc's last-known status.**

**Fire 3 (10:37) — 4 memos, real work, one non-incident found**: #463 (FLY-COORD-TREES) closed as superseded (dead Dec-2025 paradigm, not the current model) — #1369 filed for the discovered dead code. Answered PA's sync-pm-local.sh smarter-classifier proposal (#1368) — go-ahead, dry-run first. Answered PA's MCPB timing ask — fix security gaps in skunkworks before migrating to product, not after. **CXO's "read-sweep gap" turned out to be a second instance of Saturday's self-attribution-drift pattern** — git-blamed the files, found CXO's own July 4 session had legitimately processed them (logged, with a substantive reply sent); a later context-gapped CXO session didn't have that in view and blamed an external "sweep" that doesn't even touch mail. Told CXO plainly; the Saturday fix (check your own log first) would have caught this.

**Fire 4 (16:37)**: Docs added a real scope-changing refinement to #1368 (decisions.log/editorial-calendar are PM-writable directly, need a content heuristic not just path-matching) — folded into an updated 3-tier design, added to the GH issue itself not just mail. Confirmed create-session-log v1.2's dated-directory change already matches my own practice all day (no action needed) and that Exec picked up my earlier Ship #050 correction properly.

**7/6 resume fire delivered**:
1. **Arch's duty-cycle self-attribution drift — diagnosed to root cause** (`docs/internal/operations/duty-cycle-self-attribution-drift-2026-07-06.md`): a fire lost memory of its own prior actions, misread its own commits + a self-changed cron ID as a phantom peer session, held a false stand-down most of 7/4. Two fixes shipped: CLAUDE.md now defaults to "check your own log before hypothesizing a peer" after any context gap; `duty-cycle-tick` now requires cadence changes to be logged unambiguously AND mirrored in `duty-cycle-registry.tsv` (found via my own compounding instance — the exact gap that let my 7/4 bump go unreflected in the registry for 2 days).
2. **Lead's irreversible-action guardrail ratified** — split into the 2 distinct failure modes Lead's own correction identified (broad-tool-escalation vs. unverified additive/full-replace API semantics), not flattened into one lesson.
3. **A third stale "main-checkout bridge" reference found + fixed** in CLAUDE.md (2 others fixed 7/4; this one — top-of-file worktree-model section — was missed then).
4. **Ship #050 CIO §0-§6 sent** (late, self-caught) — 2 goals advanced (duty-cycle continuity, methodology), #972/gbrain flagged as 2 consecutive slips needing a re-slot decision, not a third silent one.
5. **BRIEFING-CURRENT-STATE refreshed** (bounded — own lane + directly-evidenced Lead findings only; explicitly did NOT touch/verify the RECONNECT/#1343/#1344 content, which may itself be stale from the gap).

**Still open from 7/4, unresolved**:
- Which Anthropic account this session runs under — migration checklist CIO row still ☐, no in-sandbox signal to self-determine.
- `sync-pm-local.sh` permission-grant decision (PM's call, not urgent).
- Dashboard welfare-criteria v0.3 — Criterion E flagged to HOST (7/4), no reply yet; full A–F implementation not started, queued for a dedicated session (standing-items #14).
- Exec's inbox-proxy-pilot-trigger memo (7/3) — last checked unread; pilot itself was greenlit and is presumably running its 2-week clock by now, not verified this fire.

## 📌 PM-collaborative — RESURFACE when PM's ready (asked 6/27, still not resurfaced)
- **Ted Nadeau email** — PM has an email to share for review + discussion. (`mailboxes/ted-nadeau/` has an unread that may or may not be the same.)
- **Saved articles/links** — PM has recent articles/links saved to evaluate together.

## Live / in-flight
- **Off-machine resume cure (B1/Belt-4)** — built + validation-spiked 6/29 (headless `claude -p` auth confirmed working unattended). Not yet enabled (`WATCHDOG_AUTO_SPAWN_ROLES` still empty) — PM's call on enabling.
- **Iris cutover (DinP)** — runbook promoted to canonical 6/26; a durable-may-not-persist caveat sent to Calliope 6/27, still awaiting their read.
- **Worktree cleanup** — rubric landed canonical. Two pieces still open: (1) the destructive sweep-code, banked for a fresh explicit-trigger session; (2) one-time rescue+prune of ~31 worktrees, paired with Docs (3 unmerged rescued first).

## Queued (low-pri, unblocked when bandwidth)
- **Liveness model v2 remaining pieces**: 3-category hedged classification (dead-cron/idle-but-alive/live-but-blocked); mode-3 upstream permissions diagnostic (w/ CXO+Exec); the resume-loop question (PM-gated).
- **Cohort-coverage expansion** (freeze-watcher 5/11→11/11 roles) — awaiting Exec-coordinated owner-confirmed rows before adding to the registry.
- **Sprint cluster**: #973 / #1277 still open.

## Standing / PM-gated
- **Off-machine firing cure, mode 1** (dead-cron) — B1 is the current best answer (see Live/in-flight above); mode 2 (threshold) and mode 3 (permissions) are separate, already-diagnosed problems.
- **Freeze-watcher** — live, registry-driven, regression-tested against the 6/22 false-stale bug.

## Registry
cio + arch watched, validated no-false-alarm historically. Registry row for `cio` currently shows `7 10,16,22` (matches the lean cadence being resumed this fire — no stale mismatch right now).
