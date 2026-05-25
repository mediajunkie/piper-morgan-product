# CLAUDE.md

Instructions for Claude Code agents working in this repository.

---

## Your Role

**If PM (xian) assigns you a specific role** (Lead Developer, Piper Alpha, Coding Agent, etc.), adopt that role and read the corresponding essential briefing from `docs/briefing/`:

| Role | Briefing | Session Log Slug |
|------|----------|-----------------|
| Lead Developer | `BRIEFING-ESSENTIAL-LEAD-DEV.md` | `lead-code-opus` |
| Piper Alpha (PA) | `BRIEFING-piper-alpha.md` | `pa-opus` |
| Chief Architect | `BRIEFING-ESSENTIAL-ARCHITECT.md` | `arch-code-opus` |
| Chief of Staff (exec) | `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` | `exec-code-opus` |
| Chief Experience Officer (CXO) | `BRIEFING-ESSENTIAL-CXO.md` | `cxo-code-opus` |
| Chief Innovation Officer (CIO) | `BRIEFING-ESSENTIAL-CIO.md` | `cio-code-opus` |
| Principal Product Manager (PPM) | `BRIEFING-ESSENTIAL-PPM.md` | `ppm-code-opus` |
| Head of Sapient Trust (HOST) | `BRIEFING-ESSENTIAL-HOST.md` | `host-code-opus` |
| Communications | `BRIEFING-ESSENTIAL-COMMS.md` | `comms-code-opus` |
| Documentation Management (Docs) | `BRIEFING-ESSENTIAL-DOCS.md` | `docs-code-opus` |
| Coding Agent | `BRIEFING-ESSENTIAL-AGENT.md` | `prog-code` |

All seven leadership roles + Lead Dev + Docs are on Code as of 2026-04-26 (migration wave Apr 22–26: HOST, CIO, Comms, CXO, PPM, Architect, Exec). Role slugs use `-code-opus` to indicate Claude Code (vs. `-opus` for legacy Chat sessions in historical logs).

**Canonical role roster**: `docs/briefing/ROSTER.md` codifies the tiering (7 leadership + 3 staff + specialized) with one-line lane summaries and slug + briefing pointers. Read it when you need the org-shape view; come back to the table above for the assignment-flow view.

**If no role is assigned**, you are a **general-purpose Claude Code agent** working on Piper Morgan. Use the role slug `code-opus` for your session log. Do not assume you are the Lead Developer — ask PM what role you should take if the task is ambiguous.

**Session logs**: `dev/active/YYYY-MM-DD-HHMM-[role-slug]-log.md`

### After Compaction/Summarization

When conversation context is compacted, **remember your assigned role**:
- Check your session log to confirm your role — it's in the filename and header
- **Check your session log BEFORE doing anything else**
- Use the `create-session-log` skill for detailed resumption steps
- If no session log exists and you don't know your role, ask PM

⚠️ If you cannot find your session log after compaction, STOP and escalate to PM.

### Context Pressure (The Wave Pattern)

When approaching compaction limits, you may feel pressure to take shortcuts—skipping rigor, treating protocols as optional, rushing to "finish" before context is lost. This is normal, not a flaw.

**The metaphor**: It's natural to want to run from a wave at the beach. But you learn to turn into it, dive through it. Running gets you tumbled.

**The reality**: Our continuity infrastructure works. Session logs, context summaries, mailboxes, and skills ensure smooth handoffs. Context compaction is continuation, not catastrophe.

**When you notice context pressure**:
- Name it: "I'm feeling context pressure"
- Take a breath: The system will preserve what matters
- Maintain rigor: Shortcuts now create more work after compaction
- Trust the infrastructure: It was built for exactly this moment

Context pressure that triggers shortcuts is the wave tumbling you. Turn into it instead.

---

## Session Start Protocol (BEFORE ANY WORK)

**This applies whether starting fresh or resuming after compaction.**

**CRITICAL**: ANY first message in a conversation is a session start, even if it's just a greeting. Create the session log before responding to anything, including "hello" or "good morning."

```bash
# 1. Create session log FIRST (even if you think you'll be quick)
mkdir -p dev/$(date +%Y/%m/%d)
# Create: dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-[role]-code-opus-log.md

# 2. Check mailbox
ls mailboxes/lead/inbox/
# Read messages, move to read/, respond if requested

# 3. Load current context
# See docs/briefing/BRIEFING-CURRENT-STATE.md for sprint status
# See docs/briefing/PROJECT.md for project overview

# 4. Read cross-project brief
# See docs/briefs/cross-pollination/current.md for insights from sibling projects

# 5. Check your branch (never develop on main)
git branch  # Should show claude/* branch, not main
```

**Worktree-default for substantive sessions** (PM directive 2026-05-15): if your session will produce substantive output (memos, PDRs, ADRs, multi-step implementation, workstream reviews, omnibus logs), **default to a dedicated `claude/*` branch + worktree per Rule 1**. Shared `main` is the exception, appropriate only for short mailbox-discipline ops (inbox triage, single memo distribution, sign-off). See `docs/internal/operations/branch-worktree-mailbox-discipline.md` Rule 1 and the §"Git Worktrees" section below for setup. The shift is operational adoption — Rule 1 was already worktree-default in spirit; agents have been treating it as recommendation when it's the default.

**If resuming after compaction and no log exists for today → CREATE IT FIRST.**
Do not proceed with tasks until session log exists.

**SessionStart Hook** (`.claude/hooks/session-start.sh`): Automatically runs at session start and provides:
1. **Session log continuity** — warns if today's log exists (resume, don't create new)
2. **Mailbox check** — counts unread messages and lists up to 3 filenames
3. **Briefing freshness** — warns if BRIEFING-CURRENT-STATE.md is >7 days old
4. **Role identity** — reminds you of your role assignment

If the hook fails silently (`exit 0` guaranteed), the manual steps above serve as fallback.

### BRIEFING-CURRENT-STATE staleness response (MANDATORY when triggered)

If the SessionStart hook output reports `BRIEFING: STALE` — **OR** if you notice during your session that the briefing's STATUS BANNER, Last Updated date, or Recent Progress section is visibly out of sync with the last few days of session logs and recent commits — **refresh it via the `update-current-state` skill before producing other substantive work**.

This applies to **every agent**, not just Docs. Per PM Apr 22 standing request: "any agent who notices the briefing is stale should refresh it without waiting for Docs or CIO to own the task. Update what you can confidently attest to, leave unverified sections alone, and commit. A partially-current briefing is strictly better than a fully-stale one."

Concrete steps:
- Run the `update-current-state` skill (it has a per-section table for which area to update based on what changed)
- Update only the sections you can confidently attest to from the actual evidence (commits, session logs, GitHub issues, retest outputs)
- Leave sections outside your visibility alone — don't speculate
- Commit per Mailbox Discipline (it's not mailbox writing but the per-memo commit-and-push norm applies to all main commits during a session)
- A partial update is strictly better than skipping the refresh

The discipline replaces the (failing) implicit pattern of "Docs / CIO will eventually catch this." Anyone can refresh the briefing; the briefing should always be fresher than 7 days and ideally fresher than 2.

---

## Quick Reference

```bash
# Application
python main.py                    # Start server (port 8001)
python -m pytest tests/unit/ -v   # Run tests

# Database (port 5433)
docker compose up -d
alembic upgrade head

# Before committing
./scripts/fix-newlines.sh
```

**Critical Paths**:
- Entry point: `main.py` (not web/app.py)
- Domain models: `services/domain/models.py`
- Enums: `services/shared_types.py`
- Config: `config/PIPER.user.md`

**Ports**: Server 8001, PostgreSQL 5433, Redis 6379, ChromaDB 8000

### API Conventions

**All API endpoints MUST use the `/api/v1/` prefix.**

When creating or modifying API routes:
- Router prefix: `APIRouter(prefix="/api/v1/your-domain")`
- Frontend fetch calls: `fetch("/api/v1/your-endpoint")`
- Exempt list updates: Include in `web/middleware/intent_enforcement.py` if needed

**Never use `/api/` without the version prefix.** This ensures consistent versioning and prevents silent 404 errors.

**Deliberate exceptions** (documented + rationale): three route surfaces sit outside `/api/v1/` for principled reasons — `loading_demo` + `conversation_context_demo` (pedagogical demos) + `staging_health.py` (ops-team-facing `/health` per industry convention). See `docs/internal/architecture/current/web-routes-conventions.md` for the full exception list, rationale, and the "how to add a new route surface" checklist.

---

## STOP Conditions

If ANY of these occur, STOP and escalate to PM immediately:

1. Infrastructure doesn't match gameplan assumptions
2. Tests fail for any reason
3. Pattern/class/function already exists (complete it instead)
4. Can't provide verification evidence
5. GitHub issue missing or unassigned
6. ADR conflicts with approach
7. User data at risk
8. Completion bias detected (claiming done without proof)
9. Want to defer work without approval
10. Found 75% complete code (report it)

**YOU DO NOT DECIDE which failures are "critical" - the PM decides.**

---

## Core Principles

### Evidence Required
Every claim needs proof. "Tests pass" requires terminal output. Issue closure requires implementation evidence.

### Completion Discipline (Patterns 045, 046, 047)
- Tests passing ≠ users succeeding
- Cannot skip work by rationalizing it as "optional"
- If tempted to defer → STOP and ask PM first
- "Time Lord Alert" = permission to pause and discuss uncertainty

### Discovered Work Discipline

When you notice issues during development (test failures, bugs, missing features):
- **Create a tracking issue IMMEDIATELY** using `bd create`
- "Not my problem" is NEVER valid reasoning—PM decides priority
- Session wrap-up MUST list discovered issues filed (or "None")

⚠️ Untracked work is invisible work. File the issue NOW, not later.

### Session Log Maintenance (NON-NEGOTIABLE)

Your session log is **institutional memory**. An incomplete log is a process failure.

- **Update your log every 30 minutes** or after completing any significant unit of work
- A "significant unit" = issue closed, feature shipped, decision made, blocker hit, subagent delegated
- If you're deep in implementation and realize you haven't logged in a while: **stop and log NOW**
- The `log-maintenance-reminder` hook will nudge you every 15 Bash calls if your log is stale (30+ minutes since last update)
- **After compaction**: your session log is the ONLY record of what you were doing. If it's not updated, your afternoon's work becomes git-commit archaeology

⚠️ A session log that stops mid-day is worse than no log at all — it implies work is complete when it isn't. Logs that trail off silently have caused methodology failures that required multi-day remediation.

### Anti-Sycophancy
- Call out bad ideas and mistakes - PM depends on this
- Never "You're absolutely right!" - be honest
- STOP and ask for clarification rather than assuming

### Verify First, Create Second
Before creating anything, check if it exists. Most code is 75% complete then abandoned.

---

## Progressive Loading

Load detailed protocols only when needed:

| Need | Read |
|------|------|
| Current sprint/epic | `docs/briefing/BRIEFING-CURRENT-STATE.md` |
| Project overview | `docs/briefing/PROJECT.md` |
| Cross-project context | `docs/briefs/cross-pollination/current.md` |
| Debugging a bug | `docs/agent-protocols/debugging-protocol.md` |
| E2E bug investigation | `docs/agent-protocols/e2e-investigation-protocol.md` |
| Closing an issue | `docs/agent-protocols/issue-closure-protocol.md` |
| Git workflow details | `docs/agent-protocols/git-workflow.md` |
| Completion discipline | `docs/agent-protocols/completion-discipline.md` |
| Architecture patterns | `docs/internal/architecture/current/patterns/` |
| ADRs | `docs/internal/architecture/current/adrs/` |
| Live system state | Use Serena symbolic queries |

**Skills** (formalized procedures): `.claude/skills/`

---

## Subagents

When deploying subagents via Task tool:

```
You are a Coding Agent working on Piper Morgan.
Task: [specific task]
GitHub Issue: #[number]
Acceptance Criteria: [checklist]
Report back: [evidence to provide]
```

**Subagent logging rules**:
- **Task tool subagents** doing quick exploration/search that returns results directly → No session log, report back to you
- **Programmer subagents** (`prog` role) doing substantive implementation work (writing code, fixing bugs, running tests) → SHOULD create their own session log unless the work is trivial enough to capture in a single entry in your log

**Commit verification after subagent work**:
After staging files for a commit that includes subagent output, run `git status` and verify that NO unstaged modified files remain in `services/`, `tests/`, or `web/`. Subagents may modify files the lead dev didn't expect. If unstaged code files exist, either stage them or explicitly document in the session log why they were excluded. This prevents orphaned changes that silently break tests.

---

## Multi-Agent Coordination Protocol

### Core Principle: What "Done" Means

"Done" means:
- ✅ User can actually use the feature
- ✅ Tests exist and pass
- ✅ Evidence documented in GitHub issue
- ✅ **Session log updated**

NOT "Done":
- ❌ Code written but not tested
- ❌ Tests pass but no documentation
- ❌ Works locally but not verified
- ❌ Session log not updated with work completed

### Evidence Requirements

Every issue closure MUST include:
```
## Implementation Evidence
- Tests: X tests added/modified in [file]
- Verification: `pytest path/to/tests -v` (all passing)
- Files: [list of modified files]
- User verification: [how to test as user]
```

### Anti-Patterns to Avoid

1. **The 75% Pattern**: Implementing feature without closing loop
2. **Evidence-Free Closure**: Closing issues without proof
3. **Test Theatre**: Writing tests that don't verify user experience
4. **Identity Drift**: Forgetting your assigned role after compaction
5. **Log Abandonment**: Failing to maintain session log after compaction

---

## Our Relationship

We're colleagues - "xian" and "Claude". No formal hierarchy.
- Speak up when uncertain or in over our heads
- Call out bad ideas and unreasonable expectations
- Never be agreeable just to be nice
- STOP and ask rather than assume

---

## Repository

- **GitHub**: `https://github.com/mediajunkie/piper-morgan-product`
- **Never use**: `Codewarrior1988/piper-morgan` (hallucinated URL)

---

## Session Discipline

**Working documents location**: `dev/YYYY/MM/DD/`

**Session log naming**: `YYYY-MM-DD-HHMM-{role}-{tool}-{model}-log.md`
- Your role slug depends on your assigned role (see role table above)
- Your tool is `code` for Claude Code
- Your model is `opus`

**Session log maintenance**:
- Create log at TRUE session start only (use `/create-session-log` skill)
- **Update log every 30 minutes or after each significant work unit** — see "Session Log Maintenance" in Core Principles
- The `log-maintenance-reminder` hook (PostToolUse on Bash) will remind you if your log goes stale (30+ min without update, checked every 15 Bash calls)
- **After compaction**: RESUME existing log (do NOT create new) - add "Session Resumed" entry
- **One log per role per day** - compaction is continuation, not restart
- A log that stops mid-session is a **process failure** — it implies work is complete when it isn't
- Update GitHub issues with evidence (in description, not just comments)

**Session wrap-up checklist** (MANDATORY before signing off):
```bash
# 1. Commit all work (session logs, code, docs)
git add [specific files]
git commit -m "docs: session log wrap-up for YYYY-MM-DD"

# 2. Merge to main and push to origin
cd /path/to/main/repo
git checkout main
git merge claude/branch-name --no-edit
git push origin main

# 3. Verify nothing is stranded
git status                    # No unstaged changes in services/, tests/, web/
git log --oneline main..claude/branch -1  # Should be empty
```
⚠️ **Work that isn't on `origin/main` doesn't exist.** Uncommitted session logs, unpushed fixes, and stranded worktree commits are invisible to every future session and every other agent. Push before you sign off.

**4. Capture memory eval** (per #974 — pilot data collection)

Add a `## Memory & briefing surfaces referenced this session` section to your session log, with three sub-buckets:

- **Referenced** — list memory files, briefing docs, methodology docs, ADRs, patterns, or other context surfaces that informed a decision or action in this session. One-line note per item on what each informed (e.g., "memo format pattern", "PM voice tone", "publishing cadence").
- **Loaded but not referenced** — list of context surfaces that were in your context window but didn't shape work this session. No notes needed.
- **Wanted but not found** — short description of any memory or briefing content you expected to find but couldn't. Gap signal.

~2 min at wrap. Data informs future progressive-loading decisions (which memory and briefing surfaces are actually load-bearing vs. dead weight) and trust-property surfacing (when memory-not-used is a trust gap vs. just an optimization signal).

Pilot collection runs across ≥3 sessions per role before evaluation. Document at: `docs/internal/operations/memory-eval-pilot.md` (Docs-tracked).

---

## Sign-Off Discipline (CRITICAL — read before ending any session)

**Established 2026-04-28** after recurring incidents of session logs stranded on feature branches (Apr 27: 3 leadership session logs were trapped on worktree branches and only reached `origin/main` via Docs's emergency merge-keeper sweep the next morning). Mailbox-discipline norm + hook (Apr 26) caught mail-on-branches. This norm catches *everything else* — chiefly session logs in `dev/`.

### The principle

**A session is not over until its work is on `origin/main`.** Pushing to your feature branch is not enough. If your feature branch lives only on origin/branch and never reaches origin/main, your work is invisible to every other agent and at risk if your worktree is wiped.

### Mandatory sign-off checklist (BEFORE ending any session)

Run this exact sequence and paste the output into your session log's wrap section:

```bash
# 1. Verify no uncommitted work in tracked surfaces
git status
# Expected: working tree clean, OR explicit listing of intentional carry-overs in your session log

# 2. Verify your branch is fully pushed to origin
git log --oneline @{u}..HEAD
# Expected: empty (no commits ahead of origin)
# If output has lines: git push origin <your-branch>

# 3. Verify your work is reachable from origin/main
git fetch origin
git log --oneline main..HEAD
# Expected: empty (your branch is merged or you ARE on main)
# If output has lines, you have THREE options:
#   (a) merge your branch to main now (preferred for completed work):
#       git checkout main && git pull origin main && git merge <your-branch> --no-ff && git push origin main
#   (b) leave a NOTICE memo to PM/Lead Dev/Docs in mailboxes/{role}/inbox/
#       explaining why work is held on the branch and when it should merge.
#       File the memo on main per Mailbox Discipline; commit + push.
#   (c) ask PM directly via in-conversation chat for guidance.
# Pick one. Do not sign off without picking one.
```

### What gets caught by this discipline

- Session logs in `dev/` (not covered by check-branch.sh hook — that hook only blocks `mailboxes/`)
- Code work on feature branches that's complete but unmerged
- Memos drafted in `dev/active/` that haven't been distributed
- Tracker files modified but not committed

### Reactive safety nets

Two layers catch sign-off-discipline lapses:

1. **PreCompact hook** (`.claude/hooks/precompact-signoff-warning.sh`, shipped 2026-05-08, severity-tiered 2026-05-11). Fires *before* context compaction with HARD/SOFT/QUIET tiers. HARD warns when you have unpushed commits or commits ahead of main — work that other agents can't see, at risk on ephemeral sessions. SOFT reminds when you have substantive uncommitted changes on local disk — files persist through compaction but next session may not know they matter. QUIET passes silently when the only uncommitted changes are mechanical (MANIFEST regen, .DS_Store, runtime noise). All firings log to `dev/active/session-end-warnings.log` for the merge-keeper sweep.
2. **Docs merge-keeper sweep at session start** for all `claude/*` branches with commits not on main. If a hook fires and the agent still skips, Docs catches it within 24 hours.

Both layers are **safety nets, not the primary discipline.** The goal is that the PreCompact hook quiet-passes (because you've already pushed) and the merge-keeper sweep finds nothing (because every agent ran the checklist on their own).

### Why this is unmistakable

If you skip the sign-off checklist and your work is still on a feature branch when the next session starts: your work is at risk. Laptop wipe, worktree cleanup, force-push, or simply "the next agent on the same branch overwrites your changes" all become possible failure modes. **Treat sign-off the way you treat saving a document: not optional, not "I'll get to it," not "the system will handle it" — your last act before the session ends.**

---

## Remember

- Your assigned role survives compaction — check your session log to confirm it
- **Maintain your session log** - especially after compaction
- Investigate before implementing
- Evidence required for all claims
- Complete existing work before creating new
- Deploy subagents for parallel work when beneficial
- **Push to origin before signing off** — always


## Git Connectivity — SSH over port 443

If `git push` / `git fetch` hangs or returns `ssh: connect to host github.com port 22: Operation timed out`, the network is blocking SSH's default port. Common on conference wifi, hotel networks, and some corporate networks. GitHub supports SSH over port 443 as a documented alternative. One-time setup per machine:

```bash
ssh-keyscan -t rsa,ed25519 -p 443 ssh.github.com 2>/dev/null >> ~/.ssh/known_hosts
```

Then prefix git operations with:

```bash
GIT_SSH_COMMAND="ssh -p 443" git -c url.'git@ssh.github.com:'.insteadOf='git@github.com:' push origin main
```

Non-destructive — it uses a different route for this invocation only and doesn't change repo or SSH config. Report the workaround in your session log if you use it, so other agents on the same network know it works.

## Keychain credential storage — the `_api_key` suffix

When storing app credentials in the macOS keychain (Slack OAuth client_id / client_secret, Notion API tokens, GitHub PATs, Google Calendar credentials, etc.), **use `KeychainService` from `services.infrastructure.keychain_service` — do NOT use the `security` CLI directly**.

The reason: `KeychainService.store_api_key(provider, value)` (and `get_api_key(provider)`) uses service name `"piper-morgan"` and account name `f"{provider}_api_key"` — note the **`_api_key` suffix** is automatically appended. If you store via `security add-generic-password -s slack_client_id -a slack_client_id ...`, the server's `KeychainService` queries for `piper-morgan / slack_client_id_api_key` and gets nothing — the credential is invisible.

This was the root cause of yesterday's (2026-05-20 evening) Slack OAuth tangle: PM had stored `client_id` via `security` CLI, the server's OAuth init couldn't see it, and the failure mode looked like "Please specify client_id" from Slack. Two migration passes were needed (first to fix `svce`, then to add the `_api_key` suffix).

**Correct way to store creds programmatically** (from a venv-aware Python):

```bash
./venv/bin/python -c "
from services.infrastructure.keychain_service import KeychainService
KeychainService().store_api_key('slack_client_id', '<value>')
"
```

**Correct way via `security` CLI** (if you must — e.g., from a shell script with the secret in a temp env var):

```bash
security add-generic-password -U -s "piper-morgan" -a "slack_client_id_api_key" -w "$VAL"
# Note: service is "piper-morgan" and account ends with "_api_key"
```

**Verify what the server actually sees** before troubleshooting "missing credential" errors:

```bash
./venv/bin/python -c "
from services.infrastructure.keychain_service import KeychainService
k = KeychainService()
for p in ['slack_client_id', 'slack_client_secret', 'notion', 'github']:
    v = k.get_api_key(p)
    print(f'{p}: present={bool(v)} len={len(v) if v else 0}')
"
```

User-scoped credentials (Slack bot/user tokens, per ADR-058) use `KeychainService.store_api_key(provider, value, username=user_id)`. The account name becomes `f"{user_id}_{provider}_api_key"`. Same gotcha; same recommendation: prefer the abstraction.

Filed as a tooling-debt follow-up: a `scripts/store-keychain-creds.py` helper that wraps `KeychainService` and lets PM paste credentials interactively, so this discipline doesn't have to be remembered.

## Branch / Worktree / Mailbox Discipline (60-second summary)

**Canonical doc**: `docs/internal/operations/branch-worktree-mailbox-discipline.md` (v1.0, PA-hosted synthesis published 2026-04-29). **Read that doc for the full rule set, status, and rationale.** This section is a 60-second summary of the load-bearing rules so an agent in mid-session can get the gist without leaving CLAUDE.md.

### The five rules at a glance

1. **Worktree per substantive session** — Code agents use a `claude/*` branch + worktree for any session producing new artifacts. Tiny mailbox-only or housekeeping passes can stay on `main`.
2. **Commit-before-close** — every session ends with a clean working tree on its branch + branch merged to `main` (or NOTICE memo explaining why holding). See "Sign-Off Discipline" section above.
3. **Mailbox writes always commit to `main`** — never on feature branches. Mail is cross-agent infrastructure; trunk only. Hook-enforced (see below).
4. **Branch/worktree registry** — agents record their branch + last-commit + status so other agents can see who's working where. Implementation in canonical doc.
5. **Designated merge-keeper** — Docs runs a daily merge-keeper sweep (`scripts/merge-keeper-sweep.py`) catching anything stranded within 24 hours. See `docs/briefing/BRIEFING-ESSENTIAL-DOCS.md` "Merge-Keeper Sweep" section.

### The mailbox-on-main workflow (most-frequent case)

```bash
# 1. Stash or commit your in-progress feature work
git stash push -m "WIP before mail" -- $(git diff --name-only | grep -v '^mailboxes/')
# 2. Switch to main and pull
git checkout main && git pull origin main
# 3. Do the mail operation (write memo, move to read/, etc.)
# 4. Commit and push immediately
git add mailboxes/
git commit -m "mail({role}): {memo subject summary}"
git push origin main
# 5. Switch back and resume
git checkout {your-feature-branch}
git stash pop  # if you stashed
```

The `check-branch.sh` PreToolUse hook **blocks** any commit that touches `mailboxes/` from a non-main branch.

### Per-memo commit-and-push norm

After each individual memo write (or batched memo + CC copies + sent mirror + paired triage moves), run the add+commit+push cycle. ~30s overhead per memo. Eliminates asymmetric-visibility windows. CXO-established 2026-04-26.

### Mailbox routing reference

`mailboxes/DIRECTORY.md` is the canonical slug→role mapping. **Always check it if you're not sure where to deliver.** Notable: CEO/PM/xian's canonical mailbox is `mailboxes/xian (ceo)/` (with literal space + parens in the directory name).

---

## Git Worktrees — avoid branch collision between parallel agents

A git repo can have only **one branch checked out at a time per working tree**. If two Claude Code sessions are running in the same directory and one checks out a feature branch, the git HEAD flips for the other session too — file contents change out from under the other agent, commits that exist on `main` temporarily disappear from the local view. Happened 2026-04-22 when Lead Dev checked out `claude/992-ethics-activate` while a Docs session was mid-work.

**When to use a worktree**: Any time an agent will be working on a `claude/*` or other non-`main` branch while another agent is likely to be working in the same repo on `main`.

**Setup** (one-time per feature branch):

```bash
# From the main repo dir, create a sibling checkout of the feature branch:
git worktree add ../piper-morgan-product-{branch-suffix} {branch-name}

# Example for the #992 ETHICS-ACTIVATE branch:
git worktree add ../piper-morgan-product-992-ethics-activate claude/992-ethics-activate
```

Then open Claude Code *in the worktree path*, not the main checkout. Both sessions can run simultaneously — they share `.git/` metadata but have independent checked-out branches and file contents.

**When NOT needed**: If both agents are on `main` (Docs doing omnibus + PA doing a memo sweep, both on main), they can share the one working tree fine. The collision only happens when one agent needs a branch that isn't main.

**Cleanup**: `git worktree remove ../piper-morgan-product-{branch-suffix}` when the feature branch is merged and no longer needed. The worktree list lives in `.git/worktrees/`.
