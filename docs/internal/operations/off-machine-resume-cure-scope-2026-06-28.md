# Off-machine duty-cycle resume cure — scope (cure "b")

**Author**: CIO · **Date**: 2026-06-28 · **Status**: SCOPE for PM decision (PM approved scoping this on 6/28) · **Related**: [duty-cycle-liveness-model-2026-06-25.md](duty-cycle-liveness-model-2026-06-25.md) · DinP `agent-heartbeat-cutover-runbook.md` (the "Phase 4" pointer)

---

## 1. Why this exists (what we just learned)

The cohort's recurring failure is **mode-1 cron stall**: an agent's in-process `CronCreate` job stops firing. Root cause (Iris-runbook caveat, confirmed): **in-process crons fire only while the REPL is idle AND foregrounded** — when macOS backgrounds/suspends the app, the fire is *suppressed, not queued*.

We tried two cheaper cures:
- **Durable cron** (Iris Phase 3): fixes *restart* survival, NOT *backgrounded* suppression. Necessary, not sufficient.
- **Belt-0 / cure-(a)** (launchd watchdog → `open -b` to foreground the app): **VALIDATED-FAILED 6/28.** Foregrounding the *app* doesn't un-throttle a specific *backgrounded role-window* in our multi-window cohort (macOS/Chromium throttle background windows even when the app is frontmost). **Disabled 6/28.**

The Iris runbook names the real cure **"Phase 4 — an OS-level wake that brings the session foreground+idle."** But Belt-0 *was* a wake-existing attempt, and it failed at the window granularity. **The key reframe: the off-machine cure must SPAWN-FRESH, not wake-existing.** Don't try to un-suspend the old window; start a new process that does the role's work and doesn't depend on the suspended app at all.

## 2. What "resume" must actually achieve

One duty-cycle fire for the stalled role, performed off the suspended app:
- read the role's carry-forward + `mailboxes/<role>/inbox/` + standing-items,
- drain unblocked work, commit a heartbeat to the role's branch/main.

A spawn-fresh approach covers **both** stall modes at once: **1a** (session dead) and **1b** (session suspended) — because it needs nothing from the old session.

## 3. Candidate mechanisms

### B1 — launchd watchdog → headless `claude -p` spawn  *(recommended interim, IF the gap warrants it)*
On a confirmed stall, the launchd watchdog (already off-process, already detecting) invokes `claude -p "<role duty-cycle prompt>"` as a fresh non-interactive process in the role's repo/worktree. It does the fire and exits.

- **Pros**: truly off-app (separate process); covers 1a+1b; reuses the watchdog's detection; no window-targeting problem; the heartbeat commit self-limits re-spawning.
- **OPEN QUESTIONS — must be settled by a cheap spike BEFORE any build:**
  1. **Capability**: does headless `claude -p` load the `duty-cycle-tick` skill, the project MCP servers, and the `CronCreate`/`CronList` tools? (The fire prompt depends on the skill + mailbox reads; cron tools may be needed to re-arm.) **Unknown — test it.**
  2. **Auth/env**: launchd runs in a minimal env. The spawn needs correct `HOME`/`PATH`/credentials, and must avoid the known `ANTHROPIC_*`-empty-var trap (CLAUDE.md). **Test it.**
  3. **Cost** (my standing concern): each spawn = a full session's tokens. Needs a **one-shot guard** (spawn once per stall episode, not every hourly watchdog run) + a cost ceiling. Weigh against the ~free nudge+manual floor.
  4. **Identity / persona-fork**: the prompt carries "you are <role>". Moot for a dead/stalled role (nothing concurrent), but the spawn **must only fire on a genuine stall** (heartbeat-age guard) so it never collides with a live session.
  5. **Collision / double-session**: if PM later foregrounds the old session after a spawn ran → two role sessions. Mitigations: the heartbeat commit makes the next watchdog run see "fresh" (no re-spawn); a lockfile; the spawn pushes then exits fast.
  6. **Worktree to commit from**: dedicated `<role>/heartbeat` worktree (Iris Model-A) vs. a fresh ephemeral pushing `HEAD:main`. **Decide during build.**

### B2 — always-on Mac Mini  *(the durable fix; subsumes B1)*
Run the cohort on a dedicated always-on machine where the app is never backgrounded → the foreground+idle precondition is always met → in-process crons fire reliably.
- **Pros**: sidesteps the *entire* problem class — no spawn, no window-targeting, no off-machine trigger. Simplest conceptually.
- **Cons**: hardware-dependent (PM acquiring); no help until it arrives; still needs the durable-cron discipline (Iris runbook) on it.
- **This is the real fix. B1 is only an interim bridge until it.**

### B3 — cloud routine  *(heaviest; not recommended)*
Run the agent in a remote/cloud environment on a schedule, fully off the local machine.
- **Cons**: heaviest setup (auth/state/repo-access in the cloud), cost; overkill given B2 is coming. Hold unless B2 falls through.

## 4. Recommendation

**The decision hinges on Mac-Mini timing, so that's the question back to PM:**

- **Mac Mini imminent (days)** → **do NOT build B1.** The working nudge backstop + PM-manual-resume bridges a short gap; B2 subsumes everything; B1 would be throwaway. (Cost-efficiency: don't build a bridge you'll demolish next week.)
- **Mac Mini weeks+ out** → **build B1, but spike-first.** Run the §5 validation spike (cheap). Build only if the spike passes AND the gap is long enough to amortize it.
- **Either way**, the floor stays: nudge backstop (working, dedup'd) + PM-manual-resume. A cheap adjacent win independent of all this: **route the nudge to PM's phone** (ntfy/Pushover curl from the watchdog) so manual resume works when PM is away — that strengthens the floor for ~$0 regardless of B1/B2.

## 5. The validation spike (cheap, do-FIRST if we go B1)

A one-shot test, no build commitment:
```
claude -p "<a trivial CIO duty-cycle prompt: read carry-forward, write+commit a one-line heartbeat>"
```
…invoked the way launchd would (minimal env, in a worktree), observing:
- Did it run headless at all? Did it have the `duty-cycle-tick` skill + mailbox access + cron tools?
- Did auth work from a launchd-style env (no `ANTHROPIC_*` trap)?
- Did it commit + push the heartbeat? What did it cost (tokens)?

**Pass** → B1 is viable, proceed to build with the §3 guards. **Fail** (no skill/MCP/auth headless) → B1 needs more plumbing; lean on B2 + the phone-nudge floor.

## 6. Decision needed from PM
1. **Mac Mini timing?** (days vs weeks) — drives build-vs-wait.
2. If weeks+: **approve the §5 spike** (cheap, no build commitment).
3. Optional ~$0 win now: **approve the phone-nudge** floor enhancement.

— CIO, 2026-06-28

---

## Update 2026-06-29 — B1 GREENLIT; spike PASSED; design decisions closed

**PM decision (via Janus, 2026-06-29 AM):** proceed with B1. Mac Mini not arriving until July 6 — too long to wait. B1 and B2 are non-exclusive; Mac Mini can take over as the long-term B2 host when it lands.

### Spike result: PASSED ✅

```bash
env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
    claude -p "Read first 3 lines of cio-carry-forward.md and return verbatim." \
    --model claude-haiku-4-5-20251001
```
- **Auth without ANTHROPIC_* vars**: ✅ Binary uses `~/.anthropic/` credentials — the launchd env trap is not an issue
- **File access from worktree**: ✅ Read project files correctly
- **Exit 0**: ✅

Remaining to validate **during build** (not pre-flight blockers):
- Does the duty-cycle-tick skill load in headless mode? (if not, embed the core procedure inline in the spawn prompt)
- Are CronCreate/CronList available headless? (if not, watchdog re-triggers so cron re-arm is deferred — acceptable)
- Can git commit+push work from a spawned session? (nearly certain yes; the ANTHROPIC_* trap is the only known blocker, and it's cleared)

### Design decisions (closed 2026-06-29)

**Q1: Spawn prompt format**
Include role identity + core procedure inline (self-contained), plus a reference to `duty-cycle-tick` if the skill loads. The prompt must not assume prior session context. Format:

```
You are CIO (Chief Innovation Officer) for Piper Morgan, running an autonomous duty-cycle fire triggered by the launchd watchdog (session stall detected). Working directory: <worktree_path>. Read dev/active/cio-carry-forward.md and dev/active/cio-standing-items.md. Check mailboxes/cio/inbox/ for new mail. Drain all unblocked CIO work using the duty-cycle-tick skill. Commit a heartbeat entry to origin/main when done. This is a one-shot session — complete the fire and exit.
```

**Q2: One-shot guard (cost control)**
TTL-based lockfile in `$WATCHDOG_STATE` dir:
- Watchdog writes `b1-active-{role}` before spawning, with a 2× threshold TTL
- If lockfile exists and is within TTL → skip spawn (already in flight or recently completed)
- Lockfile ages out automatically (no active cleanup needed)
- Heartbeat commit (fresh mtime on cio-carry-forward or a dedicated heartbeat file) also signals "done"

**Q3: Worktree for spawned session**
Create a temporary git worktree from a fresh branch:
```bash
git worktree add /tmp/b1-spawn-{role} -b claude/b1-spawn-{role} origin/main
```
Run `claude -p` from that directory. After exit, `git worktree remove /tmp/b1-spawn-{role}`.
The spawn pushes via `git push origin HEAD:main` (standard Model-B path).

**Q4: CronCreate unavailability headless**
Acceptable. If CronCreate is not available in headless mode, the spawned session can't re-arm the cron — but the watchdog is the triggering mechanism for B1, so re-arm happens at the next watchdog run. The in-process cron re-arm is a belt-and-suspenders addition (Belt-2: future).

### Implementation plan

1. **Extend `duty-cycle-watchdog.sh`** with a Belt-1 block (after the nudge logic, before the Belt-0 commented block):
   - Check for B1 lockfile; if within TTL → skip
   - Write lockfile
   - `git worktree add` to a temp path
   - Invoke `claude -p "<role-specific spawn prompt>"` in that worktree
   - `git worktree remove` after exit
   - Log outcome

2. **Test CIO-only first** before expanding to the cohort registry.

3. **Belt-1 enable flag**: default off (`WATCHDOG_AUTO_SPAWN:-0`), enable per-role via env/registry.

4. **Tests**: add T9/T10 to `test-duty-cycle-watchdog.sh` for Belt-1 (DRYRUN=1 should log `WOULD-SPAWN` instead of actually spawning).

5. **Cohort expansion**: after CIO validation, add to the watchdog for each registered role.

— CIO, 2026-06-29
