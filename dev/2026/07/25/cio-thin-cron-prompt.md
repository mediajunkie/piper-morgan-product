# CIO thin cron prompt (thin-job-prompt PoC, 2026-06-06; updated 2026-07-04 for Model B)

The replacement for the ~40-line fat DUTY CYCLE TICK prompt. Carries ONLY the irreducible per-agent constants; the durable procedure lives in the `duty-cycle-tick` skill, and the transient carry-forward lives in `cio-carry-forward.md`. This is the string passed to CronCreate.

**2026-07-04 correction**: the original version below hardcoded a Model-A dedicated worktree path (`piper-morgan-product-cio-cycle` / `claude/cio-cycle`). Model A is deprecated (CLAUDE.md, no current exceptions) — CIO runs Model B (ephemeral worktree, a fresh random path every session). Hardcoding a path here would just go stale again next session, so the constant now says "current session's ephemeral worktree" instead of a literal path. Cron expression also updated to reflect whatever cadence is active at re-arm time (see carry-forward for current state) rather than a frozen literal — **copy the live expression from your actual CronCreate call, don't blindly reuse the one below**.

**2026-07-04 ~12:30pm update**: PM approved bumping that day's cadence from the 3×/day lean throttle to 5×/day (`7 10,13,16,19,22`) — a moderate bump, deliberately NOT the full 6×/day migration-gated restore. Today-specific; expired at day's end.

**2026-07-06 06:xx transition (self-initiated, per the cadence-logging discipline this incident motivated)**: `CronDelete 40d04bbb` (the 7/4 bump — found still present in CronList on 7/6 resume, meaning the session's underlying process survived the 2-day gap dormant rather than actually exiting; it never fired at any of its scheduled 7/4-evening/7/5/7/6-morning times while dormant) → `CronCreate fb1edc5a` at lean `7 10,16,22`. Reason: the 7/4 bump was explicitly today-specific and had expired; migration checklist still fully unconfirmed as of 7/6, so the migration-hold reasoning for staying off full cadence is unchanged. Registry (`dev/active/duty-cycle-registry.tsv`) already showed `7 10,16,22` — no update needed there this time (it was the STALE-vs-bump direction that caused the 7/4 gap, not this reversion).

---

**2026-07-25 — MIGRATED TO AMBER / pipermorgan.ai. Model A is back, and the constant is a literal path again.** PM ratified Model A (stable per-agent worktree) as *preferable* on always-on hosts like Amber — the Model-B deprecation's premise was Claude Desktop's ephemeral auto-worktrees, which Amber doesn't have. So the 2026-07-04 reasoning above ("hardcoding a path would just go stale") **inverts** here: the path must be hardcoded *because* it must be stable and reused across sessions (Claude Code keys per-path state to the filesystem path; a fresh path each session orphans it).

**2026-07-25 late — THREE CONSTANTS IN THE ARMED PROMPT ROTTED WITHIN HOURS OF ARMING.** Recording it because it's the sharpest argument yet for the thin-prompt design:
1. **`cron=7 10,16,22`** — bumped the same morning to `7,27,47 * * * *` (20-min COLLABORATION cadence) for the active Pard window. Registry row updated to match. **Reverts to LEAN when the migration closes.**
2. **"HOOKS ARE NOT FIRING in this worktree (finding #4)"** — the *symptom* was real for this session, but the *reason* was wrong. It was never a worktree problem: an invalid hook matcher (`Bash(git commit*)` is permission-rule syntax in a field that matches tool *names*) had killed those hooks on every host and account since introduction. Root-caused by HOST. The corrected operational rule is **scope-conditioned**: project settings reload live; **user-level settings are read once at session start**, so a session predating a user-level hooks change never picks it up and must restart.
3. **"OPEN GATE: finding #4 gates the bulk cohort migration"** — **CLEARED.** HOST's take-2 passed on a fresh seat (refusal named `check-branch.sh`, both halves verified). The roll is authorized.

**The pattern worth keeping**: a cron prompt is a *frozen* constant that can rot while the session it drives keeps running — and unlike a doc, nothing re-reads it critically. That is exactly the argument for holding state in the carry-forward and only irreducible constants in the prompt. Every one of the three above was state that had leaked into the prompt.

```
DUTY CYCLE TICK (CIO). Autonomous loop fire; no human driving. Run the **duty-cycle-tick** skill and follow it.

CONSTANTS: role=CIO (slug cio) · host=Amber, account=pipermorgan.ai · worktree=`/Users/xian/Development/piper-morgan-worktrees/cio` on branch `claude/cio-cycle` (Model A — stable per-agent worktree, PM-ratified 2026-07-25; path is STABLE and REUSED across sessions, never fresh. Run `pwd` to confirm; NEVER operate from the shared checkout `~/Development/piper-morgan-product`) · cron=`7,27,47 * * * *` (COLLABORATION cadence — TEMPORARY; revert to LEAN `7 10,16,22` when the migration collaboration closes. Check cio-carry-forward.md before assuming this is current.)

TWO CHANNELS — check BOTH every fire: (1) `mailboxes/cio/inbox/` after `git fetch origin`; (2) `~/Development/mediajunkie/docs/mail/` — Pard's channel, a SEPARATE REPO needing its own fetch.

HOOKS: fixed and behaviorally verified 2026-07-25 (the matcher was invalid, never a worktree issue). But **user-level settings are read once at session start** — a session predating that change runs unenforced regardless of config. Verify behaviorally on your own seat: stage a `mailboxes/` file on a non-main branch, attempt a commit; the PASS is a refusal that NAMES check-branch.sh. A classifier denial is INCONCLUSIVE, not a pass. `check-branch.sh` is ADVISORY, not a control (`git -c` and `--no-verify` both bypass it).

CARRY-FORWARD: read dev/active/cio-carry-forward.md + cio-standing-items.md. Rewrite cio-carry-forward.md at end of any substantive fire. Log every substantive fire to the SESSION log (permanent), not only a cycle log (sprint-cleaned).

Hold the discipline; holistic-not-tactical. A fire is a WAKE, not a time-box — drain everything unblocked before going idle. If the skill is unavailable, fall back to docs/operations/duty-cycle design/procedures/.
```

**Step 2a — RESOLVED 2026-07-25** (was "carried from the handoff, still unresolved"). The branch-name-contains-basename fingerprint was a Model-B artifact that returns a **false pass** under Model A, where the pairing is permanent by construction. Retired in `duty-cycle-tick` v1.15; the real gate is Pard's **tmux-cwd collision guard**, shipped and tested in `amber-agent.sh` (v1.16 records it as shipped rather than planned). Reflog is the forensic tell, not the gate.

**Note the fallback line** — the one real PoC risk is whether a cron-injected one-line prompt reliably triggers skill-loading (vs. the old self-contained fat prompt). The fallback to the procedures docs makes a mis-fire safe: if the skill doesn't load, the agent still has the pointer to the full procedure. Watch the first few fires for whether the skill actually loads + is followed.

**Self-grounding note (6/27 HOST-prompt incident, carried into this 7/4 revision)**: a heavy self-contained "you are X" prompt nearly persona-forked a CIO session once (see cio-carry-forward history) — but the failure mode of a *too-thin* prompt is losing context resilience across compaction. This version keeps the constants inline (role, cron, carry-forward paths) rather than only pointing at external state, as a small deliberate hedge.
