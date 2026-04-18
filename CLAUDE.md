# CLAUDE.md

Instructions for Claude Code agents working in this repository.

---

## Your Role

**If PM (xian) assigns you a specific role** (Lead Developer, Piper Alpha, Coding Agent, etc.), adopt that role and read the corresponding essential briefing from `docs/briefing/`:

| Role | Briefing | Session Log Slug |
|------|----------|-----------------|
| Lead Developer | `BRIEFING-ESSENTIAL-LEAD-DEV.md` | `lead-code-opus` |
| Piper Alpha (PA) | `BRIEFING-piper-alpha.md` | `pa-opus` |
| Chief Architect | `BRIEFING-ESSENTIAL-ARCHITECT.md` | `arch-opus` |
| Chief of Staff | `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` | `exec-opus` |
| Communications | `BRIEFING-ESSENTIAL-COMMS.md` | `comms-opus` |
| Coding Agent | `BRIEFING-ESSENTIAL-AGENT.md` | `prog-code` |

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

**If resuming after compaction and no log exists for today → CREATE IT FIRST.**
Do not proceed with tasks until session log exists.

**SessionStart Hook** (`.claude/hooks/session-start.sh`): Automatically runs at session start and provides:
1. **Session log continuity** — warns if today's log exists (resume, don't create new)
2. **Mailbox check** — counts unread messages and lists up to 3 filenames
3. **Briefing freshness** — warns if BRIEFING-CURRENT-STATE.md is >7 days old
4. **Role identity** — reminds you of your role assignment

If the hook fails silently (`exit 0` guaranteed), the manual steps above serve as fallback.

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
- Update log throughout session with timestamped entries
- **After compaction**: RESUME existing log (do NOT create new) - add "Session Resumed" entry
- **One log per role per day** - compaction is continuation, not restart
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
