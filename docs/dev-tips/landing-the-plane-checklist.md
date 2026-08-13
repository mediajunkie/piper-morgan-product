# Landing the Plane: Session End Checklist

**What this is**: the checklist Piper Morgan's own coding agents run at the end of every session, kept here for transparency into how the team actually works — not a set of steps you need to follow as a visitor. If you're building your own agent-workflow discipline, the shape below (discover → verify → close → sync → report) may be useful as a reference.

**Purpose**: Ensure no work is lost, all tasks are tracked, and the codebase is in a clean state before ending a session.

**When to use**: At the end of every Piper Morgan coding-agent session, before the agent shuts down.

---

## Pre-Flight Check

Before starting the landing sequence, verify you're ready:

- [ ] All work-in-progress committed or stashed
- [ ] Current task at a logical stopping point
- [ ] You know which epic/issues you worked on this session

---

## Landing Sequence (Execute in Order)

### Step 1: Discover and File Remaining Work

**Check for undocumented work**:
```bash
# Ask yourself:
# - Did I notice any bugs?
# - Did I see tech debt?
# - Are there follow-ups needed?
# - Did I defer anything mentally?
```

**File discovered work**:
```bash
bd create "Bug: [description]" --priority P1
bd create "Tech debt: [description]" --priority P2
bd create "Follow-up: [description]" --priority P3

# Link back to parent work
bd dep add <new-issue-id> <parent-issue-id> --type discovered-from
```

**Verify**: `bd list` shows all work tracked, nothing in your mental TODO

---

### Step 2: Run Quality Gates (if code changed)

**Run tests**:
```bash
pytest tests/ -xvs
```

**If tests pass**: ✅ Proceed to Step 3

**If tests fail**: ❌ DO NOT close parent issue
```bash
# File blocker issue
bd create "P0 Blocker: Tests failing in [area]" --priority P0
bd dep add <blocker-id> <parent-id> --type blocks

# Keep parent issue open
# Document failure in parent issue notes
bd edit <parent-id> --notes
```

---

### Step 3: Verify Completion Criteria

**For each issue you want to close**:

1. **Read acceptance criteria** from gameplan/prompt
2. **Check every criterion**:
   - [ ] All functionality implemented?
   - [ ] All tests passing?
   - [ ] Documentation updated (if required)?
   - [ ] Manual testing complete (if required)?

3. **If ALL met**: ✅ Proceed to close
4. **If ANY not met**:
   - Option A: Complete the missing work
   - Option B: Request deferral
     ```bash
     bd edit <issue-id> --notes
     # Add: "@PM-approval-needed: Missing [criterion] because [reason]"
     # WAIT for PM response before closing
     ```

---

### Step 4: Close Completed Issues

**Only close if**:
- All acceptance criteria met ✅
- Tests passing ✅
- No open blockers ✅

**Close the issue**:
```bash
bd close <issue-id>
```

**Verify**:
```bash
bd show <issue-id>
# Status should be "closed"
```

---

### Step 5: Check Epic Status

**Before closing any epic**:

```bash
# List all children
bd list --parent <epic-id>
```

**Verify ALL children are**:
- [ ] Status = "closed" OR
- [ ] Have `@PM-approved: defer to [milestone]` annotation

**If ANY children open without approval**: ❌ CANNOT close epic
- Complete remaining children OR
- Request PM approval for deferral

**If all children resolved**: ✅ Can close epic
```bash
bd close <epic-id>
```

---

### Step 6: Sync Database

**Push all changes to remote**:
```bash
bd sync
```

**Verify sync succeeded**:
```bash
# Should show "Sync complete" or similar success message
# No error messages about conflicts
```

**Check git state**:
```bash
git status
```

**Expected output**:
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**If uncommitted changes exist**: ❌ Something's wrong
- Review what wasn't committed
- Commit manually or stash appropriately
- Re-run `bd sync`

---

### Step 7: Verify Clean State

**Final checks**:

```bash
# No uncommitted Beads changes
bd status

# No uncommitted git changes
git status

# No stale stashes (optional cleanup)
git stash list
git stash clear  # If stashes no longer needed

# Beads database consistent
bd list | grep "in_progress"
# Should only show issues you're actively working on next session
```

---

## Post-Landing Report

**Document for next session**:

Create handoff note in `dev/YYYY/MM/DD/[timestamp]-session-handoff.md`:

```markdown
# Session Handoff - [Date] [Time]

## Completed This Session
- Closed issues: [list]
- Commits: [git log --oneline -5]

## In Progress
- Open issues: [bd list | grep in_progress]
- Next priorities: [bd ready --json]

## Discovered Work Filed
- [List of new issues created]

## Blockers
- [Any P0 issues filed]

## Notes for Next Session
- [Context, decisions, things to remember]
```

---

## Emergency Checklist (If Rushed)

If you're low on time, AT MINIMUM do:

1. [ ] `bd create` for ANY work you discovered but didn't finish
2. [ ] `bd sync` to persist changes
3. [ ] `git status` to verify clean state
4. [ ] Leave note about incomplete landing in session log

Better to file issues quickly than lose work silently.

---

## Red Flags (Do Not Land If...)

🚨 **STOP and fix before landing**:

- [ ] Tests are failing (file P0 blocker instead)
- [ ] Epic closed but children still open
- [ ] Uncommitted code changes
- [ ] `bd sync` shows conflicts
- [ ] Mental TODO items not filed as issues
- [ ] Closed issue without meeting acceptance criteria

---

## Success Criteria

You've successfully landed the plane when:

✅ All discovered work tracked in Beads
✅ All completed issues closed
✅ All quality gates passed
✅ Beads database synced
✅ Git working tree clean
✅ No mental TODOs remaining
✅ Handoff note created for next session

---

## Common Mistakes

**Mistake**: "I'll file that issue later"
**Fix**: File it NOW or you'll forget

**Mistake**: Closing issue with "mostly done"
**Fix**: Review acceptance criteria - ALL must be met

**Mistake**: Closing epic with open children
**Fix**: Check `bd list --parent` first

**Mistake**: Skipping quality gates "to save time"
**Fix**: File P0 blocker if tests fail, don't hide failure

**Mistake**: Deferring without PM approval
**Fix**: Add `@PM-approval-needed` and WAIT

---

**Remember**: The discomfort of open issues is a feature, not a bug. It keeps work visible and prevents silent completion rot.
