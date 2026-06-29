---
name: create-session-log
description: Create or resume a session log at session start. Use when starting a new session, when PM assigns work, or after context compaction to find and continue your existing log. Critical for maintaining institutional memory.
scope: cross-role
version: 1.1
created: 2026-01-21
updated: 2026-05-17
---

# create-session-log

Create a properly named and structured session log file at the start of a work session.

## When to Use

Use this skill when:
- Starting a new work session with any agent role
- PM assigns you a role and tasks for the day
- Resuming work after a break (check for existing log first)

**Note on subagents**:
- If you are a **Task tool subagent** doing quick exploration/search that returns results directly, you do NOT create a session log.
- If you are a **programmer subagent** (`prog` role) doing substantive implementation work (writing code, fixing bugs, running tests), you SHOULD create a session log unless the work is trivial enough to capture in a single entry in the coordinating agent's log.

## Key Principle: One Log Per Role Per Day

**A single consolidated log per role per day is preferable to fragmented logs**, even if efforts are separate. Always check for an existing same-day log before creating a new one.

## Procedure

### Step 1: Check for Existing Same-Day Log

Before creating a new log, check if one already exists:

```bash
ls dev/active/*$(date +%Y-%m-%d)*{role}*log.md
```

**If found**: Continue that log instead of creating a new one. Add a section:
```markdown
### {TIME} - Session Resumed
- [Context of resumption]
```

**If not found**: Proceed to create new log.

### Step 2: Determine File Name

**Format**: `YYYY-MM-DD-HHMM-{role}-{tool}-log.md`

**Location**: `dev/active/`

**Components**:
- `YYYY-MM-DD`: Today's date
- `HHMM`: Current time in 24-hour format (no colon)
- `{role}`: Role slug (see table below)
- `{tool}`: `code` for Claude Code CLI

**Model tracking**: record the model in the log **header** (`**Model**: Opus 4.8 [1M]`), not the filename. If PM changes the model mid-session, note the switch in the header (e.g., `**Model**: Opus 4.8 → Sonnet 4.6 (switched ~14:00)`).

**Historical note**: logs created before 2026-06-29 include `-opus`, `-sonnet`, or `-haiku` in the filename — leave those as-is.

### Step 3: Create File with Standard Header

```markdown
# Session Log: {date}-{time}-{role}-{tool}

**Role**: {Full Role Name}
**Model**: {Tool} ({Model at session start})
**Date**: {Day of Week}, {Month} {Day}, {Year}
**Start Time**: {Time in 12-hour format}

## Session Objectives

1. [Primary objective from PM]
2. [Secondary objectives if any]

## Work Log

### {Time} - Session Start
- Created session log
- [Initial context or task]
```

### Step 4: Fill Initial Content

- Record objectives from PM's instructions
- Note any handoff context
- Begin work log with first timestamped entry

### Step 5: Commit Immediately (MANDATORY)

**Commit the new session log to `main` right away, before doing anything else.** Untracked files are at risk during pull/merge cycles in shared-main; an untracked session log can vanish silently when another agent's commit lands and a recovery checkout discards uncommitted state. Today's session log is institutional memory — don't let it sit untracked.

```bash
git reset HEAD                                            # clear pre-existing index
git add dev/{YYYY}/{MM}/{DD}/{YYYY}-{MM}-{DD}-{HHMM}-{role}-{tool}-log.md
git diff --cached --name-only                             # verify only your log staged
git commit -m "log({role}): {date} session start"
git push origin main
```

Subsequent log updates throughout the session can batch; the initial commit is the one that takes the file off the untracked-and-at-risk surface.

**Why this is non-optional**: May 17 incident — a Docs session log was Write-created at 7:20 AM but never `git add`+committed. During a later pull/merge cycle (~8:35 AM), the file was lost from disk with no git history to recover from. The session's work was preserved in conversation context + downstream artifacts (omnibus, calendar, memos) but the institutional record had to be reconstructed by hand. Commit-on-creation is ~10 seconds; recovery cost without it is open-ended.

## Role Slug Reference

| Role | Slug | Full filename slug |
|------|------|-------------------|
| Lead Developer | `lead` | `lead-code` |
| Chief Architect | `arch` | `arch-code` |
| Communications Director | `comms` | `comms-code` |
| Documentation Manager | `docs` | `docs-code` |
| Programmer (subagent) | `prog` | `prog-code` |
| Chief Innovation Officer | `cio` | `cio-code` |
| Chief Experience Officer | `cxo` | `cxo-code` |
| Head of Sapient Trust | `host` | `host-code` |
| Product & Project Manager | `ppm` | `ppm-code` |
| Executive Summary Agent | `exec` | `exec-code` |
| Piper Alpha | `pa` | `pa-code` |
| Spec Writer | `spec` | `spec-code` |

## Examples

### Example 1: New Session Log

**PM says**: "Good morning! You are my docs agent. Create omnibus for yesterday."

**Check**: `ls dev/active/*2026-01-22*docs*log.md` → Not found

**Create**: `dev/active/2026-01-22-0800-docs-code-log.md`

```markdown
# Session Log: 2026-01-22-0800-docs-code

**Role**: Documentation Management Specialist
**Model**: Claude Code (Haiku)
**Date**: Wednesday, January 22, 2026
**Start Time**: 8:00 AM

## Session Objectives

1. Create omnibus log for January 21, 2026
2. Check mailbox for requests

## Work Log

### 8:00 AM - Session Start
- Created session log
- PM confirmed omnibus for Jan 21 is primary task
```

### Example 2: Resuming Existing Log

**PM says**: "Continue working on the anti-pattern index."

**Check**: `ls dev/active/*2026-01-21*docs*log.md`
**Found**: `2026-01-21-0750-docs-code-haiku-log.md`

**Action**: Open existing log and add:

```markdown
### 2:30 PM - Session Resumed
- PM assigned continuation of anti-pattern index work
- Previous session completed Phase 2 experiment
```

### Example 3: Lead Developer Log

**Create**: `dev/active/2026-01-21-0900-lead-code-log.md`

```markdown
# Session Log: 2026-01-21-0900-lead-code

**Role**: Lead Developer
**Model**: Claude Code (Opus 4.8)
**Date**: Tuesday, January 21, 2026
**Start Time**: 9:00 AM

## Session Objectives

1. Review PR #543 and merge if passing
2. Coordinate Phase 2 implementation across subagents

## Work Log

### 9:00 AM - Session Start
- Created session log
- Checking mailbox for overnight messages
```

## After Context Compaction (CRITICAL)

If you've just experienced **context compaction** (conversation was summarized to save tokens):

### This is NOT a New Session

After compaction, you are mid-session, not starting fresh. Your log from earlier today **must** exist.

### Mandatory Steps

1. **DO NOT create a new log** - Your earlier log should exist
2. **Find and verify it**:
   ```bash
   ls dev/active/*$(date +%Y-%m-%d)*{role}*log.md
   ```
3. **If found**: Add resumption entry immediately:
   ```markdown
   ### {TIME} - Session Resumed (Post-Compaction)
   - Prior work: [what the summary indicates]
   - Continuing: [current task]
   ```
4. **If NOT found**: **STOP. This is a critical failure.** Escalate to PM immediately. Do not proceed with implementation work.

### Why This Matters

The session log is your institutional memory. After compaction, you've lost the detailed conversation but the log preserves:
- What you were working on
- Decisions made
- Progress achieved
- Context for continuing

Losing the log mid-session means losing hours of context that cannot be reconstructed from git commits alone.

### Common Post-Compaction Mistake

**Wrong**: "I don't see a log, I'll create a new one"
**Right**: "I don't see a log from earlier today - this is a critical failure, escalating to PM"

If you truly started fresh today and there's no prior log, that's fine - create one. But if you're post-compaction, the log MUST exist from before compaction.

---

## Pattern Families

At session start, identify which pattern families apply to your work:

```markdown
**Active pattern families this session**: [list applicable families]
```

Common families:
- **Completion Theater** (045/046/047/049): Multi-phase work, closing issues
- **Investigation** (006/041-043/060): Bug fixing, incident response
- **Grammar Application** (050-058): Feature development, UX work
- **Multi-Agent Coordination** (029/059/010/021/037): Cross-domain decisions

See [PATTERN-FAMILIES.md](../../../docs/internal/architecture/current/patterns/PATTERN-FAMILIES.md) for full family index.

---

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Create multiple logs for same role same day | Hard to synthesize for omnibus | Continue existing log |
| Use wrong role slug | Breaks discovery and omnibus | Use exact slugs from table |
| Omit time from filename | Ambiguous, breaks sorting | Always include HHMM |
| Leave objectives blank | Log lacks purpose context | Fill from PM instructions |
| Skip the existence check | Creates duplicate logs | Always check first |
| Create new log after compaction | Loses institutional memory | Find and continue existing log |
| Proceed without log after compaction | Critical context lost | STOP and escalate to PM |

## Quality Checklist

After creating/resuming a session log:
- [ ] File is in `dev/active/`
- [ ] Filename follows convention exactly
- [ ] Header metadata is complete
- [ ] Objectives reflect PM's actual instructions
- [ ] Work log has first timestamped entry
- [ ] No duplicate same-day log for this role

## After the Session

Session logs in `dev/active/` may be archived to `dev/YYYY/MM/DD/` after the session ends. This is typically handled by PM or documentation processes, not during the session itself.
