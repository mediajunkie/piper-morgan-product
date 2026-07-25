# CIO thin cron prompt (thin-job-prompt PoC, 2026-06-06; updated 2026-07-04 for Model B)

The replacement for the ~40-line fat DUTY CYCLE TICK prompt. Carries ONLY the irreducible per-agent constants; the durable procedure lives in the `duty-cycle-tick` skill, and the transient carry-forward lives in `cio-carry-forward.md`. This is the string passed to CronCreate.

**2026-07-04 correction**: the original version below hardcoded a Model-A dedicated worktree path (`piper-morgan-product-cio-cycle` / `claude/cio-cycle`). Model A is deprecated (CLAUDE.md, no current exceptions) — CIO runs Model B (ephemeral worktree, a fresh random path every session). Hardcoding a path here would just go stale again next session, so the constant now says "current session's ephemeral worktree" instead of a literal path. Cron expression also updated to reflect whatever cadence is active at re-arm time (see carry-forward for current state) rather than a frozen literal — **copy the live expression from your actual CronCreate call, don't blindly reuse the one below**.

**2026-07-04 ~12:30pm update**: PM approved bumping that day's cadence from the 3×/day lean throttle to 5×/day (`7 10,13,16,19,22`) — a moderate bump, deliberately NOT the full 6×/day migration-gated restore. Today-specific; expired at day's end.

**2026-07-06 06:xx transition (self-initiated, per the cadence-logging discipline this incident motivated)**: `CronDelete 40d04bbb` (the 7/4 bump — found still present in CronList on 7/6 resume, meaning the session's underlying process survived the 2-day gap dormant rather than actually exiting; it never fired at any of its scheduled 7/4-evening/7/5/7/6-morning times while dormant) → `CronCreate fb1edc5a` at lean `7 10,16,22`. Reason: the 7/4 bump was explicitly today-specific and had expired; migration checklist still fully unconfirmed as of 7/6, so the migration-hold reasoning for staying off full cadence is unchanged. Registry (`dev/active/duty-cycle-registry.tsv`) already showed `7 10,16,22` — no update needed there this time (it was the STALE-vs-bump direction that caused the 7/4 gap, not this reversion).

---

**2026-07-25 — MIGRATED TO AMBER / pipermorgan.ai. Model A is back, and the constant is a literal path again.** PM ratified Model A (stable per-agent worktree) as *preferable* on always-on hosts like Amber — the Model-B deprecation's premise was Claude Desktop's ephemeral auto-worktrees, which Amber doesn't have. So the 2026-07-04 reasoning above ("hardcoding a path would just go stale") **inverts** here: the path must be hardcoded *because* it must be stable and reused across sessions (Claude Code keys per-path state to the filesystem path; a fresh path each session orphans it). Cron re-armed on the new host as `d250236f` at LEAN `7 10,16,22`. Added a memory-scope check step — see the first-session findings in `dev/2026/07/25/2026-07-25-1053-cio-code-log.md`.

```
DUTY CYCLE TICK (CIO). Autonomous loop fire; no human driving. Run the **duty-cycle-tick** skill and follow it.

CONSTANTS: role=CIO (slug cio) · host=Amber, account=pipermorgan.ai · worktree=`/Users/xian/Development/piper-morgan-worktrees/cio` on branch `claude/cio-cycle` (Model A — stable per-agent worktree, PM-ratified 2026-07-25 as preferable on always-on hosts; path is STABLE and REUSED across sessions, never fresh. Run `pwd` to confirm; NEVER operate from the shared checkout `~/Development/piper-morgan-product`) · cron=`7 10,16,22 * * *` (LEAN cadence — check cio-carry-forward.md for current state before assuming this is still accurate).

**2026-07-25 late — TWO CONSTANTS IN THE ARMED PROMPT WENT STALE THE SAME DAY, both now corrected.** (a) The prompt warned "HOOKS ARE NOT FIRING in this worktree (finding #4)" — the *symptom* was right for this session but the *reason* was wrong: it was never a worktree problem, it was an invalid hook matcher (`Bash(git commit*)` is permission-rule syntax in a field matching tool names) that had killed those hooks on every host since introduction. Root-caused by HOST. (b) "OPEN GATE: finding #4 gates the bulk cohort migration" — **the gate is CLEARED**; HOST's take-2 passed on a fresh seat and the roll is authorized. Both corrected in the live cron below. Worth noting as a pattern: **a cron prompt is a frozen constant that can rot mid-day**, which is exactly the argument for keeping state in the carry-forward and only irreducible constants in the prompt.

---

MEMORY SCOPE CHECK (new, 2026-07-25): verify your memory dir resolves to the shared cohort pool before trusting recall. On Amber, Claude Code appears to resolve the memory key to the **git common dir** (main repo root), NOT the worktree path — so worktrees may share memory by construction. Confirm `~/.claude-pm/projects/-Users-xian-Development-piper-morgan-product/memory/` is the live pool and is non-empty. A silent split or an empty pool is the failure mode; be loud if either.

CARRY-FORWARD: read dev/active/cio-carry-forward.md + cio-standing-items.md. Rewrite cio-carry-forward.md at end of any substantive fire.

Hold the discipline; holistic-not-tactical. If the skill is unavailable for any reason, fall back to docs/operations/duty-cycle design/procedures/ (cron-lifecycle / watch / stop / start).
```

**Step 2a caveat (carried from the handoff, still unresolved)**: `duty-cycle-tick`'s collision check ("branch name must contain the worktree directory's basename") was built for Model B. Under stable per-agent worktrees it happens to still pass here (`claude/cio-cycle` contains `cio`), but the *reasoning* behind it no longer applies — re-derive what "collision" means on Amber before trusting it as a signal.

---

**Note the fallback line** — the one real PoC risk is whether a cron-injected one-line prompt reliably triggers skill-loading (vs. the old self-contained fat prompt). The fallback to the procedures docs makes a mis-fire safe: if the skill doesn't load, the agent still has the pointer to the full procedure. Watch the first few fires for whether the skill actually loads + is followed.

**Self-grounding note (6/27 HOST-prompt incident, carried into this 7/4 revision)**: a heavy self-contained "you are X" prompt nearly persona-forked a CIO session once (see cio-carry-forward history) — but the failure mode of a *too-thin* prompt is losing context resilience across compaction. This version keeps the constants inline (role, cron, carry-forward paths) rather than only pointing at external state, as a small deliberate hedge.
