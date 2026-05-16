# Issue Closure Protocol

"Closing an issue properly" means updating BOTH the description AND adding a closing comment.

---

## Before Closing Any Issue

1. **Update description checkboxes**: Every `[ ]` completed becomes `[x]`
2. **Update Completion Matrix**: Mark items "Complete" with evidence links
3. **Add verification evidence**: Link to commits, test output, or PR
4. **Update status**: Change to "COMPLETE"

---

## Closing Comment Template

```markdown
## Implementation Complete

### Summary
[1-2 sentence summary]

### Changes Made
- [File]: [What changed]
- [File]: [What changed]

### Test Results
[Test command and output summary]

### Verification
- Commit: [hash]
- Tests: [X] passing
```

---

## Issue Closure Checklist

Before `gh issue close <number>`:

- [ ] All description checkboxes checked (or explicitly marked "deferred with PM approval")
- [ ] Completion Matrix updated with evidence
- [ ] Closing comment added with implementation evidence
- [ ] Status in description shows "COMPLETE"

---

## Anti-Pattern: Comment-Only Close

**Wrong**: Add evidence comment, close issue, leave description boxes unchecked
**Right**: Update description boxes, add evidence comment, then close

---

## Why This Matters

- Unchecked boxes = incomplete work visible to anyone reviewing
- Comments alone aren't enough - description is source of truth
- Future planning depends on accurate records
- Incomplete records require re-verification (learned 2026-01-11)

---

## Tooling: Automatic Lint (#1083)

A PostToolUse hook at `.claude/hooks/issue-checkbox-lint.sh` runs after every
`git commit` and warns when the commit message contains close-magic-strings
(`Closes #N` / `Fixes #N` / `Resolves #N` and case/tense variants) targeting
an issue whose description body still has `[ ]` unchecked checkboxes.

The hook:
- Reads the most-recent commit message via `git log -1`
- Extracts referenced issue numbers via close-keyword regex
- Fetches each issue body via `gh issue view N --json body`
- Counts lines matching `^[[:space:]]*[-*][[:space:]]+\[[[:space:]]\]`
- Warns to stderr with a recommendation to update the body via
  `gh issue edit N --body-file ...` BEFORE pushing

The hook is **warn-only** — it doesn't block the commit (which already
happened). The intent is to surface the gap in the window between commit
and push, so the agent can update the issue body in time. If pushed
without updating, the merge-keeper sweep / next-session-start audit will
catch it eventually, but the lint shrinks the window.

Filed as **#1083 TOOL-ISSUE-CHECKBOX-LINT** after PM flagged the
close-issue-properly skill as a recurring miss (memory entry
`feedback_close_issue_properly_skill_recurring_miss.md`). Retroactive
test against 13 May 7-13 closures: the hook would have flagged 3 of them
(#1070, #304, #1069) at commit time — the others either had no checkboxes
or were cleaned up post-hoc via separate body edits.

The hook is wired in `.claude/settings.json` under `PostToolUse` /
`Bash` matcher.
