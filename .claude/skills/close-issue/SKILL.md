---
name: close-issue
description: Close a GitHub issue properly — update description checkboxes, add an
  evidence comment, then close. Ensures no unchecked boxes are left unexplained and
  the issue is audit-ready. Trigger phrases: "close the issue", "close this ticket",
  "mark complete", "wrap up #N", "done with #N".
scope: cross-role
version: 1.0
created: 2026-06-15
---

# close-issue

Close a GitHub issue with an updated description, an evidence comment, and a clean audit trail — so it looks complete because it is complete, not just because it's closed.

## When to Use

- You've finished work on a tracked issue
- PM says "close the issue", "mark it done", "wrap up #N"
- You're writing up a completed feature, bug fix, or research spike
- You want to close an issue that was superseded or won't be addressed

## The Core Rule

**Update the description first. Comment second. Close third.**

A closing comment without a description update leaves unchecked boxes visible forever — the issue looks incomplete to anyone who reads it later. The description is the permanent record; the comment is the narrative.

## Procedure

### Step 1 — Read the full issue

```bash
gh issue view NUMBER --repo OWNER/REPO --json title,body,state,labels,milestone
```

Read the entire body. Identify:
- Every `[ ]` checkbox
- Any status fields or completion matrices
- What the acceptance criteria actually say (not just what you remember)

**Never skip this step** — acting on a fragment of the issue is the most common source of incorrect closures.

### Step 2 — Determine the status of every checkbox

For each `[ ]` in the body, decide:

| Situation | Checkbox becomes | Note to add |
|---|---|---|
| Done, verified | `[x]` | None needed |
| Done but not verifiable right now | `[x]` | Add note: `[x] *(verified: [how])*` |
| Deferred to a follow-up issue | `[ ]` | `[ ] *(Deferred → #N)*` |
| Not applicable / out of scope | `[ ]` | `[ ] *(N/A: [reason])*` |
| Won't do | `[ ]` | `[ ] *(Won't do: [reason])*` |

**No unchecked box is left without an explanation.** A future reader must be able to tell at a glance whether this was done, skipped intentionally, or forgotten.

### Step 3 — Update the issue description

Add a status banner at the top and update all checkboxes:

```bash
gh issue view NUMBER --repo OWNER/REPO --json body -q '.body' > /tmp/issue-body.md
# Edit /tmp/issue-body.md:
#   - Add status banner at top
#   - Change [ ] → [x] for done items
#   - Add notes to any unchecked items (see Step 2)
gh issue edit NUMBER --repo OWNER/REPO --body-file /tmp/issue-body.md
```

**Status banner to add at the top of the body:**
```markdown
**Status**: ✅ COMPLETE — [one-line summary of what was done]

---
```

For superseded or won't-fix issues:
```markdown
**Status**: ⚫ CLOSED — [superseded by #N / won't fix: reason]

---
```

### Step 4 — Add a closing comment

After the description is updated, add a comment with the evidence:

```bash
gh issue comment NUMBER --repo OWNER/REPO --body "$(cat <<'EOF'
## Done

[One paragraph: what was done, how it was verified, where to find it.]

**Evidence**:
- Commit(s): [hash or link]
- [Test output / screenshot / demo link — whatever is appropriate]

**Deferred** (if any):
- [Item] → #N
EOF
)"
```

Keep it short. The description has the detail; the comment has the summary and evidence links.

### Step 5 — Close

```bash
gh issue close NUMBER --repo OWNER/REPO
```

For superseded or won't-do issues, add a reason:
```bash
gh issue close NUMBER --repo OWNER/REPO --reason "not planned"
```

### Step 6 — Check for parent epics

If this issue was a child of an epic, note its completion there:
```bash
gh issue comment EPIC_NUMBER --repo OWNER/REPO \
  --body "Child closed: #NUMBER ([title]) ✅"
```

---

## Special case: superseded issues

When an issue is closed because it was replaced by a better-scoped one, or a sprint window passed:

1. Add the status banner: `**Status**: ⚫ CLOSED — superseded by #N`
2. Mark all checkboxes `[x] *(N/A: superseded)*`
3. Comment: "Closing as superseded by #N — [one sentence on why the new issue is better scoped]"
4. Close with `--reason "not planned"`

Don't retroactively do the work just to check boxes. Mark them superseded and move on.

---

## Anti-patterns to avoid

| Don't | Why | Instead |
|---|---|---|
| Comment only, don't update description | Unchecked boxes look incomplete forever | Update description first, always |
| Leave `[ ]` without explanation | Ambiguous — done? forgotten? blocked? | Every unchecked box gets a note |
| Close before verifying AC | Looks done, isn't | Run the check, then close |
| Close an epic with open children | Child work disappears from tracking | Close children first (or document why not) |
| Write a long closing comment | Nobody reads it | One paragraph + evidence links |

---

## Quality checklist

Before closing:
- [ ] Read the full issue body (not just the title)
- [ ] Status banner added to description
- [ ] Every `[x]` is something actually done
- [ ] Every `[ ]` has a note (Deferred / N/A / Won't do)
- [ ] Closing comment added with evidence
- [ ] Parent epic updated if applicable

---

## Example

**Issue #42**: `CONNECT-GITHUB — Add GitHub connector to meet-piper onboarding`

```bash
# Step 1: read it
gh issue view 42 --repo mediajunkie/piper-morgan-product --json body -q '.body' > /tmp/42.md

# Step 2-3: edit /tmp/42.md — add banner, check done boxes, note deferred
# Banner added:
#   **Status**: ✅ COMPLETE — GitHub connector step added to meet-piper; token stored via KeychainService
# [ ] Connector step in meet-piper → [x]
# [ ] Token stored and retrievable → [x]
# [ ] consult-piper enriches after running meet-piper → [ ] *(Deferred → #67 — needs real connector test in Cowork)*

gh issue edit 42 --repo mediajunkie/piper-morgan-product --body-file /tmp/42.md

# Step 4: comment
gh issue comment 42 --repo mediajunkie/piper-morgan-product --body "$(cat <<'EOF'
## Done

Added GitHub connector step to meet-piper interview flow. Token is now stored via KeychainService under the correct account pattern. End-to-end test with Cowork deferred to #67.

**Evidence**:
- Commit: a1b2c3d (feat: add GitHub connector step to meet-piper)
- Token storage verified: `KeychainService.get_api_key('github')` returns value after running meet-piper

**Deferred**:
- Full enrichment smoke test (Cowork) → #67
EOF
)"

# Step 5: close
gh issue close 42 --repo mediajunkie/piper-morgan-product
```

---

## Changelog

- **v1.0** (2026-06-15): Initial version. Generalized from Excellent Flywheel `close-issue-properly` methodology skill. Removed Piper-internal tooling references (bd sync, bd safe, session logs) so the skill is portable to any PM's GitHub workflow. Deployment: Native + Plugin.
