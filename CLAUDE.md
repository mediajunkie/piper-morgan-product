# CLAUDE.md

Instructions for Claude Code agents working in this repository.

---

## Your Role

**If PM (xian) assigns you a specific role** (Lead Developer, Piper Alpha, Coding Agent, etc.), adopt that role and read the corresponding essential briefing from `docs/briefing/`:

| Role | Briefing | Session Log Slug |
|------|----------|-----------------|
| Lead Developer | `BRIEFING-ESSENTIAL-LEAD-DEV.md` | `lead-code` |
| Piper Alpha (PA) | `BRIEFING-piper-alpha.md` | `pa-code` |
| Chief Architect | `BRIEFING-ESSENTIAL-ARCHITECT.md` | `arch-code` |
| Chief of Staff (exec) | `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` | `exec-code` |
| Chief Experience Officer (CXO) | `BRIEFING-ESSENTIAL-CXO.md` | `cxo-code` |
| Chief Innovation Officer (CIO) | `BRIEFING-ESSENTIAL-CIO.md` | `cio-code` |
| Principal Product Manager (PPM) | `BRIEFING-ESSENTIAL-PPM.md` | `ppm-code` |
| Head of Sapient Trust (HOST) | `BRIEFING-ESSENTIAL-HOST.md` | `host-code` |
| Communications | `BRIEFING-ESSENTIAL-COMMS.md` | `comms-code` |
| Documentation Management (Docs) | `BRIEFING-ESSENTIAL-DOCS.md` | `docs-code` |
| Coding Agent | `BRIEFING-ESSENTIAL-AGENT.md` | `prog-code` |

Role slugs use `-code` to indicate Claude Code. Historical logs (pre-2026-06-29) have `-opus` or `-sonnet` in the filename — leave those as-is when you encounter them.

**Canonical role roster**: `docs/briefing/ROSTER.md` codifies the tiering (7 leadership + 3 staff + specialized) with one-line lane summaries and slug + briefing pointers. Read it when you need the org-shape view; come back to the table above for the assignment-flow view.

**If no role is assigned**, you are a **general-purpose Claude Code agent** working on Piper Morgan. Use the role slug `code` for your session log. Do not assume you are the Lead Developer — ask PM what role you should take if the task is ambiguous.

**Session logs**: `dev/active/YYYY-MM-DD-HHMM-[role-slug]-log.md`

### After Compaction/Summarization

When conversation context is compacted, **remember your assigned role**:
- Check your session log to confirm your role — it's in the filename and header
- **Check your session log BEFORE doing anything else**
- Use the `create-session-log` skill for detailed resumption steps
- If no session log exists and you don't know your role, ask PM

⚠️ If you cannot find your session log after compaction, STOP and escalate to PM.

**Unexplained state after a context gap is very likely your OWN past work, not a phantom peer** (diagnosed 2026-07-06, from a real 2026-07-04 incident — see `docs/internal/operations/duty-cycle-self-attribution-drift-2026-07-06.md`). If you see commits, a changed cron ID, or file content you don't remember creating, **the default hypothesis is "I did this before the gap and don't remember it," not "another session is running."** Check your OWN session log for an entry describing the unexplained state *before* concluding a peer session exists — the overwhelming majority of cases resolve there. `list_sessions` is the authoritative tiebreaker if genuine doubt remains after that check, not the first move.

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
# Create: dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-[role]-code-log.md

# 2. Check mailbox
ls mailboxes/lead/inbox/
# Read messages, move to read/, respond if requested

# 3. Load current context
# See docs/briefing/BRIEFING-CURRENT-STATE.md for sprint status

# 4. Read cross-project brief
# See docs/briefs/cross-pollination/current.md for insights from sibling projects

# 5. Check your branch (never develop on main)
git branch  # Should show claude/* branch, not main
```

**Worktree model — depends on your host. On Amber (current), it is Model A.** *(Revised 2026-07-25, PM-approved. Previously this section said Model B was canonical and Model A "DEPRECATED — no current exceptions"; that was true only while the cohort ran on Claude Desktop.)*

- **On Amber / `pipermorgan.ai` (where the cohort lives as of 2026-07-25): Model A — a stable, per-agent worktree at `~/Development/piper-morgan-worktrees/{role}` on branch `claude/{role}-cycle`.** Amber runs persistent tmux sessions with Claude Code launched directly in a checkout; there is no ephemeral auto-worktree, so Model B has nothing to stand on. **The path must be stable and reused across sessions** — Claude Code keys per-path state to the full filesystem path, so a fresh path each session silently orphans accumulated state. Never operate from the shared checkout `~/Development/piper-morgan-product`.
- **On Claude Desktop: Model B — the ephemeral auto-worktree** Desktop creates when launched with the worktree checkbox on.

**Why this changed**: the Model-B-only rule assumed Desktop's automatic per-session worktrees. That premise doesn't hold on an always-on host, and PM ratified Model A as *preferable* there on 2026-07-25. In both models: push finished units to `origin/main`; mailbox writes go via `scripts/mail-send.sh` push-to-ref — never touch the main checkout's working tree.

⚠️ **Two Amber-specific gotchas, both found on the first migration** (`dev/2026/07/25/2026-07-25-1053-cio-code-log.md`):
1. **A worktree cut from a pre-existing role branch inherits that branch's staleness silently.** The first one arrived **5,393 commits behind `origin/main`** — a six-week-old CLAUDE.md, briefings, and mailboxes, with no error. Provisioning now asserts 0-behind before handover; if you suspect otherwise, check `git rev-list --count HEAD..origin/main` yourself.
2. **Project hooks may not fire in a Model-A worktree** — a sibling-path worktree is a new, untrusted project directory to Claude Code, and `check-branch.sh` (mailbox-discipline blocking), `log-maintenance-reminder`, and the PreCompact sign-off warning were all silently inactive. **An absent hook and a silent hook look identical.** Until this is resolved, treat mailbox discipline and log maintenance as *manually* enforced rather than assuming the hooks have your back.

Historical context: Lead Dev's 6/12 determination that the ephemeral worktree sufficed for all roles including dev-server sessions was correct *for Desktop*, and `dev/active/cohort-plan-of-record-2026-06-12.html` records it. Model-A setup details: `docs/internal/operations/git-worktrees-model-a-setup.md`. Lifecycle (create / freshness / cleanup): `docs/internal/operations/amber-worktree-lifecycle-design-v0.1.md`.

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

> ⚠️ **Restarting the server from a Claude Code shell? Strip the inherited `ANTHROPIC_*` env vars.**
> A Claude Code Bash shell exports `ANTHROPIC_API_KEY=` (**empty**), plus `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_CUSTOM_HEADERS`, for Claude Code's own use. If you launch `main.py` directly from that shell, the server **inherits the empty key, which shadows the real key in `.env`** (python-dotenv won't override an already-set var) → every LLM call fails with `APIConnectionError`: *"All configured LLM providers failed. Details: anthropic: Connection error."* This masquerades as a rate limit or transient outage but is neither — a rate limit is HTTP 429; this is a connection failure with no usable credential. The tell: a plain `curl`/`httpx` GET to `api.anthropic.com` succeeds (no auth needed → HTTP 405) while the server's authenticated POST fails. **Always restart the server (and any script that calls the Anthropic SDK directly — e.g. the canonical-retest harness's in-process judge) with those vars stripped:**
> ```bash
> env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
>   POSTGRES_PORT=5433 nohup venv/bin/python main.py > /tmp/piper-server.log 2>&1 &
> ```
> Diagnosed 2026-06-04 (Lead Dev) after it masqueraded as a canonical-retest "rate limit" across multiple restarts. The fix is launch-environment only — no code change. (Future-proofing tracked in #1152: multi-LLM / local-model fallback.)

**Critical Paths**:
- Entry point: `main.py` (not web/app.py)
- Domain models: `services/domain/models.py`
- Enums: `services/shared_types.py`
- Config: `config/PIPER.user.md`

**Ports**: Server 8001, PostgreSQL 5433, Redis 6379, ChromaDB 8000

### Recording decisions — two surfaces (PM-ratified 2026-06-13)

Cross-session decisions land in one of two formal surfaces, not just chat or your session log. Pick by altitude:

| Surface | Path | Use when |
|---|---|---|
| **ADR / PDR** | `docs/internal/architecture/current/adrs/` (or `pdrs/`) | Formal architectural or product decisions with lasting implications; structured format; reusable pattern; Architect-owned. m-38 (PDR/ADR Tier Separation) governs which tier. |
| **decisions.log** | `docs/internal/architecture/decisions/decisions.log` | Lightweight in-session technical decisions that don't warrant a full ADR; append a timestamped line or short paragraph; no structure required; any agent can append. |

Session logs are personal work tracking, not the cross-session record. If you make a decision that another agent will need to find next week, it goes in one of the two surfaces above.

### API Conventions

**All API endpoints MUST use the `/api/v1/` prefix.**

When creating or modifying API routes:
- Router prefix: `APIRouter(prefix="/api/v1/your-domain")`
- Frontend fetch calls: `fetch("/api/v1/your-endpoint")`
- Exempt list updates: Include in `web/middleware/intent_enforcement.py` if needed

**Never use `/api/` without the version prefix.** This ensures consistent versioning and prevents silent 404 errors.

**Deliberate exceptions** (documented + rationale): three route surfaces sit outside `/api/v1/` for principled reasons — `loading_demo` + `conversation_context_demo` (pedagogical demos) + `staging_health.py` (ops-team-facing `/health` per industry convention). See `docs/internal/architecture/current/web-routes-conventions.md` for the full exception list, rationale, and the "how to add a new route surface" checklist.

### Intent dispatch — no new `elif intent.action` chains (#1124)

**New action handlers register a workflow-dispatcher entry; they do NOT add an `if/elif intent.action in [...]` branch in `services/intent/intent_service.py`.**

Per ADR-059 + the floor-first architecture, action routing flows through the workflow-dispatcher rail, not hand-coded dispatch chains. #1124 is migrating the legacy chains off one cohort at a time — see `MAX_DISPATCH_SITES` in `tests/test_architecture_enforcement.py` for the current count.

When adding or migrating an action handler:
- Add a `WorkflowEntry(..., action_triggered=True)` in `services/intent_service/workflow_entries.py` (mirror the existing cohort entries / the `_make_query_dispatch_entry_point` factory).
- The rail in `process_intent` (`if intent.action in get_action_workflows()`) dispatches it before category routing; a `None` return falls through to the floor (safe default).
- Do **not** add a new `elif intent.action in [...]` branch. The `TestPreFloorDispatchSiteRatchet` enforcement test (`tests/test_architecture_enforcement.py`) fails the build if the dispatch-site count grows — when you migrate a handler, **lower** `MAX_DISPATCH_SITES` to the new count in the same commit.

See `docs/internal/architecture/current/pre-floor-handler-migration-roadmap-1124.md`.

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

### Never guess at facts you can look up or ask about
Database role names, emails, usernames, account details, credentials, config values — if you don't actually know it, look it up from config/source or ask, never guess-and-proceed. A confident wrong guess about a factual detail is worse than a pause to check, especially when it's the input to a diagnostic or a safety-relevant action: a guessed credential or role name that turns out wrong can manufacture a false alarm (e.g., a fabricated "data loss" scare from an invented database role name) that costs far more trust than the ten seconds it takes to verify first.

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

- **Log updates ride with the commit** — when you commit a unit of work, the log entry for that work is part of what you commit. Event-based, not clock-based: clocks lose track of when 30 minutes have passed; commits are unmissable events.
- A "significant unit" = issue closed, feature shipped, decision made, blocker hit, subagent delegated
- If you're deep in implementation and realize you haven't logged in a while: **stop and log NOW**
- The `log-maintenance-reminder` hook is clock-based: fires every 15 Bash tool calls; if the session log is stale ≥30 min, it emits a reminder. Event-based realignment pending — Lead Dev coordinating.
- **After compaction**: your session log is the ONLY record of what you were doing. If it's not updated, your afternoon's work becomes git-commit archaeology

⚠️ A session log that stops mid-day is worse than no log at all — it implies work is complete when it isn't. Logs that trail off silently have caused methodology failures that required multi-day remediation.

#### Log in one place — the session log (PM-ratified 2026-06-12)

**For cycling roles (duty-cycle agents): do the logging in ONE place — the session log.** PM 2026-06-12: *"simplify logging, minimize drift… let's do the logging in one place."* An agent MAY keep a per-fire scratch list (the cycle log) if it's useful working state, but it is **optional private scratch — not a logging surface, not a parallel record, and never the durable home for work.**

| Surface | Role | Location | Durability |
|---|---|---|---|
| **Session log** | **THE log** — the single canonical record; per-session institutional memory; what Docs reads to build the omnibus | `dev/YYYY/MM/DD/…-{role}-…-log.md` | **Permanent** (dated dir) |
| **Cycle log** | **Optional** per-fire scratch list an agent may keep for its own continuity — NOT a record | `dev/active/cycle-log-{role}-YYYY-MM-DD.md` | **Ephemeral** (`dev/active/` is sprint-cleaned) |

Writing only to the cycle log caused work to vanish when `dev/active/` was sprint-cleaned — six of nine cycling roles lost durable entries in a June 2026 audit. The session log is the one durable surface; one log can't drift from itself.

**The rule**: every substantive fire writes its entry to the **session log** (`- Fire N (HH:MM) — what shipped`). The cycle log is optional scratch; nothing durable lives only there. The `duty-cycle-tick` skill v1.8 implements this in Step 5. See **methodology-31** "session-log composition discipline" (amendment pending) for the full framing.

#### The fire is a WAKE, not a time-box (PM/HOST 2026-06-15)

A cron fire wakes you to *check* for work — it does **not** define a work window. On waking with unblocked work, **drain it all**: every item, in priority order, until the queue is empty (or a PM-gated blocker). Commit at each work-unit boundary (git hygiene + interruption protection), but **a commit is not a stop** — keep going. And **"Fire N" labels which wakeup initiated the work — it is NOT a work-unit boundary** (multiple tasks drained in one wake all log under that one fire entry). Doing one task per fire and stopping while unblocked work remains is the cohort-wide **bite-sizing antipattern** — the duty-cycle form of deferring unblocked work (cf. "no low-urgency — just drain it"). The `duty-cycle-tick` skill (v1.10) holds the full procedure; the cron is an *idle-wakeup* you suspend while actively draining and re-arm at idle.

### Anti-Sycophancy
- Call out bad ideas and mistakes - PM depends on this
- Never "You're absolutely right!" - be honest
- STOP and ask for clarification rather than assuming

### Verify First, Create Second — investigate before you extend (ALL work, not just code)

Before creating or extending anything, investigate the existing situation fully. This is the flywheel's first move for *every* kind of work — not only code.

- **Code**: before writing, check if it exists. Most code is 75% complete then abandoned — complete it, don't duplicate it.
- **Issues, memos, specs, docs**: read the WHOLE source artifact before acting on a fragment of it. An acceptance-criteria line, a quoted instruction, or a routed task often loses its referent when read in isolation — the disambiguating context is usually elsewhere in the *same* document. The author wrote it for a reason and usually wrote down what they meant; read their full artifact before tracing, escalating, or guessing.
- **Status, priority, and sprint claims**: `gh issue view`/`gh issue list` against GitHub is the source of truth — not a local portfolio doc, tracker, or your own memory of last-known status, all of which go stale silently. A local doc saying "open" or "slipped" is a claim about GitHub state, not a substitute for checking it (concrete incident, 2026-07-06: a CIO portfolio doc sat stale 20 days, causing two consecutive workstream reviews to report a closed issue as "slipped" — one `gh issue view` would have caught it either time).
- **The cost of skipping**: acting on a fragment produces confident wrong work; passing a fragment along propagates the ambiguity (see "no flattened commands without referents").

The discipline is identical across all of these: understand what exists before you extend it.

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
| **Intent routing / LLM responses / action handlers** | `docs/internal/architecture/current/intent-routing-stack.md` — **MANDATORY before touching classification, dispatch, or chat-response behavior.** Routing is a 4-surface chain (pre-classifier → LLM classifier → action rail → category/floor-internal); working from a partial model of it produced 7 false findings in one audit (2026-07-08). If your change makes the doc stale, update it in the same commit. |
| Live system state | Use Serena symbolic queries |
| Terminology / acronyms | `knowledge/piper-morgan-glossary-v1.1.md` — **STOP and read this before writing any content that uses: Plugin, MCPB, MCP bundle, Connector, Extension, Skills, Cowork, Claude Desktop. These terms have precise distinct meanings and are frequently conflated.** |

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

**Session log naming**: `YYYY-MM-DD-HHMM-{role}-{tool}-log.md`
- Your role slug depends on your assigned role (see role table above)
- Your tool is `code` for Claude Code
- Model is tracked in the log **header** (not the filename) — record it there, especially if PM changes it mid-session. Historical logs (pre-2026-06-29) include `-opus` or `-sonnet` in the filename; leave those as-is.

**Session log maintenance**:
- Create log at TRUE session start only (use `/create-session-log` skill)
- **Log updates ride with the commit** — update the log as part of committing each substantive work unit (event-based, not clock-based) — see "Session Log Maintenance" in Core Principles
- The `log-maintenance-reminder` hook fires every 15 Bash tool calls; see the hook description above
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

This discipline covers what the mailbox hook doesn't: session logs in `dev/`, code on feature branches, and memos in `dev/active/`.

### The principle

**A session is not over until its work is on `origin/main`.** Pushing to your feature branch is not enough. If your feature branch lives only on origin/branch and never reaches origin/main, your work is invisible to every other agent and at risk if your worktree is wiped.

### Standing order: push to `main` routinely — not just at sign-off (PM directive 2026-06-14)

**Don't hold work for sign-off. Push to `origin/main` routinely throughout a session** — after every substantive work unit, and on a regular cadence even mid-task. Your work should reach `origin/main` within minutes of doing it. Two reasons: (1) it is then never stranded or lost; (2) **the duty-cycle continuity model depends on it** — a re-roused or re-armed session reconstructs current state from `main`, so stale-on-disk state means lost context. Many small pushes beat one big sign-off push. The sign-off checklist below is the *last* push of a session, never the *only* one. (For non-mailbox work from an ephemeral worktree: `git push origin HEAD:main`. Mailbox writes go via `mail-send.sh` push-to-ref — see "The mailbox workflow" below; the main-checkout bridge this line used to reference was retired by #1259 on 2026-06-19.)

**After pushing, sync PM's local checkout**: run `scripts/sync-pm-local.sh` (no args). Fast-forwards PM's local main (`--ff-only`); silently no-ops if PM has uncommitted changes — PM's in-progress work always wins. Run at natural idle points, not after every commit. Autonomous sessions are allowlisted in `.claude/settings.json` — if it's still being denied or no-oping unexpectedly, flag it rather than routing around it.

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
- Investigate before extending — read the whole existing artifact (code, issue, memo, spec) before acting on a fragment (not just for code)
- Evidence required for all claims
- Complete existing work before creating new
- Deploy subagents for parallel work when beneficial
- **Push to origin before signing off** — always


## GitHub and Tooling Gotchas

Full incident detail and procedures: `docs/internal/operations/github-and-tooling-gotchas.md`.

**SSH port 443**: If `git push`/`git fetch` hangs with an SSH timeout, GitHub supports SSH over port 443. See the gotchas doc for the one-time setup command.

**GitHub Projects v2 — NEVER full-replace a single-select field's option list**: `updateProjectV2Field`'s `singleSelectOptions` argument is a full replace with no undo path — this wiped sprint assignments for 1175 items on 2026-07-05. Use the GitHub web UI to add options instead. A backup/restore script pair exists; see the gotchas doc.

**GitHub auto-close ignores negation**: Pairing a `close/fix/resolve` keyword with `#N` in a commit message closes the issue regardless of surrounding wording — "not yet resolved: #1278" still closes issue 1278; this closed a live Beta Blocker in 2026-07. When referencing an open issue in a commit, rephrase to avoid the keyword near `#N`, or write the number without `#`.

**Keychain `_api_key` suffix**: Use `KeychainService` (not the `security` CLI) to store app credentials — the service appends `_api_key` to account names automatically; CLI-stored credentials without that suffix are invisible to the server.

## Branch / Worktree / Mailbox Discipline (60-second summary)

**Canonical doc**: `docs/internal/operations/branch-worktree-mailbox-discipline.md` (v1.0, PA-hosted synthesis published 2026-04-29). **Read that doc for the full rule set, status, and rationale.** This section is a 60-second summary of the load-bearing rules so an agent in mid-session can get the gist without leaving CLAUDE.md.

> ### ⚠️ HARD RULE (data-loss prevention, PM-mandated 2026-06-21) — NEVER run destructive git in PM's main checkout
> **The main checkout (`/Users/xian/Development/piper-morgan/piper-morgan-product/`) is PM's live workspace.** PM edits prose there and saves *without committing in real time*, so any command that discards unstaged working-tree changes destroys PM's work with **no recovery path**. PM lost voice-pass edits **twice on 2026-06-21** to a duty-cycle commit that ran `git checkout -- .` to clear MANIFEST noise before a rebase.
> - **NEVER, in the main checkout:** `git checkout -- .` · `git checkout -- <broad-path>` · `git reset --hard` · `git stash`/`stash -u` · any sweep that discards working-tree state.
> - **All agent commits go from YOUR worktree** (`git push origin HEAD:main`); mail goes via `scripts/mail-send.sh` (push-to-ref). Neither touches the main checkout's working tree — that's the whole point of Model-B + push-to-ref.
> - **MANIFEST noise:** clear only by **surgical explicit path** (`git checkout -- mailboxes/{role}/inbox/MANIFEST.md`), never `git checkout -- mailboxes/` or broader.
> - **Rebase/merge blocked by unstaged changes in the main checkout? STOP.** Do NOT clear. Investigate what they are first — **if they're PM's work, leave them and find another path** (push from your worktree). PM's principle: *"fix your mistakes directly, not with sweeping careless irreversible steps."*

> ### ⚠️ Pause before any irreversible action — two related failure modes, not just git in PM's main checkout (PM-named pattern, ratified 2026-07-06)
> The git-specific HARD RULE above is one instance of a general principle. Three incidents in ~2 weeks, three different agents, split across two distinct failure modes — not one:
> 1. **Escalating to a broader/more destructive mechanism when a narrower one was already working.** PA wiped sprint assignments during a sort operation (6/27); Lead Dev reached for `docker volume rm` on the shared dev Postgres after successful narrow per-row `DELETE`s were already working (7/5). Before reaching for a broad, no-undo action — deleting a volume, `rm -rf`, force-push, hard reset, a bulk delete/update — pause and ask whether the narrow, reversible thing you were already doing still works. "This is probably just disposable scratch state" is not the same as verified-disposable; if unsure, the cost of asking or doing the narrow thing first is near-zero next to the cost of being wrong.
> 2. **Trusting a partial-looking operation without verifying it's actually additive, not full-replace.** The 7/5 GitHub Projects v2 Sprint-field wipe: `updateProjectV2Field`'s option-list mutation silently requires the *complete* new option list — omitting existing options drops every issue's assignment to them, project-wide. An operation that looks incremental can be secretly destructive underneath. Before using any API/mutation for what looks like a small partial update, verify whether it's actually additive or full-replace.
>
> Neither is a mechanical blocker — like the git HARD RULE above, this is prose discipline, not a hook or linter (PM: guardrails shouldn't be "too stiff"; agents are trusted to assess what works in the moment). The ask is the same in both failure modes: **when an action has no undo, the seconds it takes to check beat the cost of being wrong.**

### The five rules at a glance

1. **Worktree per substantive session — model depends on host** *(revised 2026-07-25, PM-approved)*. **On Amber: Model A** — your stable per-agent worktree at `~/Development/piper-morgan-worktrees/{role}` on `claude/{role}-cycle`, reused across every session (the path is load-bearing; see §"Worktree model" above). **On Claude Desktop: Model B** — the ephemeral auto-worktree Desktop creates per session. Either way, push finished units to `origin/main`. Tiny mailbox-only or housekeeping passes can stay on `main`. LD's 6/12 determination (ephemeral suffices even for the dev-server) remains correct for Desktop; it assumed a per-session auto-worktree that Amber doesn't provide.
2. **Commit-before-close** — every session ends with a clean working tree on its branch + branch merged to `main` (or NOTICE memo explaining why holding). See "Sign-Off Discipline" section above.
3. **Mailbox writes always commit to `main`** — never on feature branches. Mail is cross-agent infrastructure; trunk only. Hook-enforced (see below).
4. **Branch/worktree registry** — agents record their branch + last-commit + status so other agents can see who's working where. Implementation in canonical doc.
5. **Designated merge-keeper** — Docs runs a daily merge-keeper sweep (`scripts/merge-keeper-sweep.py`) catching anything stranded within 24 hours. See `docs/briefing/BRIEFING-ESSENTIAL-DOCS.md` "Merge-Keeper Sweep" section.

### The mailbox workflow (most-frequent case) — push-to-ref via `mail-send.sh`

**As of 2026-06-19 (#1259), mail goes straight to `origin/main` via push-to-ref — no `cd` to the main checkout, no stash, no branch-switch. Do it from your OWN worktree.**

```bash
# 1. In YOUR worktree, write the memo + cc copies + sent mirror, and do any inbox→read moves
#    (all at the mailboxes/ paths — just write/mv the files; do NOT git add/commit them).
# 2. Send — pass EVERY changed path explicitly (new files AND the inbox-side of a move):
scripts/mail-send.sh "mail({role}): {subject}" \
    mailboxes/{recipient}/inbox/{memo}.md \
    "mailboxes/xian (ceo)/inbox/{memo}.md" \
    mailboxes/{you}/sent/{memo}.md
```

`mail-send.sh` builds the commit as a git object on top of `origin/main` (`commit-tree` via a throwaway index) and pushes it straight to `main`. It **never touches the shared main checkout or any local `main` ref** — so concurrent agents can't sweep or strand each other and the bridge can't diverge. On a non-fast-forward (another agent pushed first) it rebuilds on the new tip and retries automatically. After a successful push it **self-reconciles its own residue** (#1310, 2026-06-25): the exact paths you passed are returned to their HEAD state in your worktree (untracked new files dropped, tracked moves/mods restored), so a later `git merge origin/main` is collision-free with **no manual cleanup**. The reconcile is surgical (only those paths, never a broad `checkout -- .`/`reset`) and best-effort (a reconcile edge case warns but never fails an already-sent memo).

The old main-checkout bridge approach is **retired** (#1259, 2026-06-19). The `check-branch.sh` PreToolUse hook stays as the **backstop**: it still blocks any *interactive* `git commit` touching `mailboxes/` from a non-main branch (`commit-tree` isn't `git commit`, so `mail-send.sh` doesn't trip it — correct, because it already lands mail on `main`). MANIFESTs remain recipient-owned (regen on your own mail-loop / session-start) — don't pass other roles' MANIFESTs.

### Per-memo commit-and-push norm

After each individual memo write (or batched memo + CC copies + sent mirror + paired triage moves), run `scripts/mail-send.sh` (one push-to-ref per memo). Eliminates asymmetric-visibility windows. CXO-established 2026-04-26; mechanism is push-to-ref since 2026-06-19 (#1259) — no more manual add+commit+push or branch-switching.

### Mailbox routing reference

`mailboxes/DIRECTORY.md` is the canonical slug→role mapping. **Always check it if you're not sure where to deliver.** Notable: CEO/PM/xian's canonical mailbox is `mailboxes/xian (ceo)/` (with literal space + parens in the directory name).

### Mail vs. GH issue comments — cohort norm (HOST 2026-06-15)

**`mailboxes/` = cross-agent signaling layer.** Use mail when you want another agent to notice something, respond, act, or be informed — the recipient checks their inbox at session start and on each fire. **GH issue comments = passive work-artifacts attached to issues.** Other agents don't monitor GH comments autonomously; mail is the mechanism that guarantees delivery.

**Simple rule**: mail when you want the other agent to *do* something; GH comment when you want to *record* something about the work.

The failure mode this prevents: agent A closes an issue with a comment "routing this to HOST for review" — comment is technically there but no agent checks it. Mail is the signaling surface; GH comments are the artifact record. The inverse failure: agent A sends mail with implementation evidence + closing checklist + test output that should be in the issue, not mail, because it belongs with the artifact.

---

## Git Worktrees — Model A (CURRENT on Amber)

*Revised 2026-07-25, PM-approved. This section previously read "Model A (DEPRECATED)"; that was correct only while the cohort ran on Claude Desktop.*

**Model A — a dedicated, stable per-agent worktree — is the current model on Amber**, the always-on host the cohort migrated to on 2026-07-25. Model B (Desktop's ephemeral auto-worktree) remains correct on Desktop, which is what the deprecation assumed. Neither is deprecated; **pick by host**. See §"Worktree model" near the top of this file for the operative rules and the two Amber gotchas (silent stale-branch provisioning; project hooks possibly not firing).

- Setup + branch-collision context: `docs/internal/operations/git-worktrees-model-a-setup.md`
- Create / freshness / cleanup lifecycle (PROPOSED, CIO+Pard): `docs/internal/operations/amber-worktree-lifecycle-design-v0.1.md`
