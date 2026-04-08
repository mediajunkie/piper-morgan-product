---
name: update-current-state
description: Update BRIEFING-CURRENT-STATE.md when work changes project status. Any agent
  can use this after closing issues, completing gates, filing findings, or shipping features.
  Keeps the briefing fresh without waiting for Docs.
scope: all-agents
version: 1.0
created: 2026-04-07
---

# update-current-state

Update `docs/briefing/BRIEFING-CURRENT-STATE.md` to reflect current project status.

## When to Use

Any agent should use this skill when their work changes project state:
- Issue closed or filed
- Gate status changed (passed, failed, re-test ready)
- Test count changed significantly
- New skill, pattern, or ADR created
- Sprint/milestone status changed
- Blocker resolved or discovered

## Which Section to Update

Only update the section(s) relevant to your work. Do not rewrite the whole file.

| What changed | Section to update |
|-------------|-------------------|
| Gate pass/fail/re-test | STATUS BANNER + Gate Status table |
| Issue closed/filed | Recent Progress (add bullet to current week) |
| Tests added/fixed | Metrics Snapshot (test count) |
| New pattern/ADR/skill | Metrics Snapshot + System Capability |
| Sprint milestone | STATUS BANNER + Inchworm Position |
| Blocker found/resolved | Open Items by Priority |
| New infrastructure | Metrics → Infrastructure |

## Procedure

### Step 1: Read the Current File

```bash
cat docs/briefing/BRIEFING-CURRENT-STATE.md
```

Identify which section(s) need updating based on your work.

### Step 2: Update Relevant Section(s)

Use the Edit tool to modify only the affected section. Preserve everything else.

**STATUS BANNER format** (always update Last Updated):
```markdown
**Current Position**: [inchworm position]
**Version**: [version from pyproject.toml]
**Last Updated**: [today's date]
**Current Focus**: [one-line summary]
**Next Phase**: [what follows]
```

**Recent Progress format** (prepend new week, keep 4 most recent):
```markdown
### [Date range] ([Theme])
- **[Date]**: **[Key event].** [Details with issue numbers, commit hashes, role names.]
```

**Gate Status format**:
```markdown
- **Gate N** (Name): ✅/❌/🔲 [status] [details]
```

### Step 3: Update the Timestamp

Always update both:
- STATUS BANNER `**Last Updated**:` line
- Footer `*Last Updated:*` line

### Step 4: Commit

```bash
git add docs/briefing/BRIEFING-CURRENT-STATE.md
git commit -m "briefing: update CURRENT-STATE — [what changed]"
```

## Rules

- **Only update what you know.** Don't guess at other agents' work.
- **Preserve history.** Don't delete Recent Progress entries — add new ones at the top, trim old ones at the bottom (keep 4 most recent week sections).
- **Use evidence.** Include issue numbers, commit hashes, test counts — not vague claims.
- **Keep it scannable.** One bullet per event. Bold the key fact. Details after.
- **Don't duplicate the omnibus.** The briefing is a status snapshot, not a narrative. Point to omnibus logs for details.

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Rewrite the whole file | Update only your section |
| Add vague "progress made" bullets | Cite specific issues, commits, counts |
| Update without reading first | Always read current state to avoid conflicts |
| Skip the timestamp update | Both timestamps must match today's date |
| Wait for Docs to update it | Any agent can and should update after significant work |
