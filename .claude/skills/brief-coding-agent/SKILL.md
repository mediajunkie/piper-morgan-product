---
name: brief-coding-agent
description: Generate a standard "Coding Agent" subagent prompt from a GitHub issue number. Use when deploying a coding subagent via the Task tool, when PM/Lead Dev says "brief a coding agent for #N", or before delegating implementation work, so the briefing is consistent and carries the real CLAUDE.md conventions.
scope: cross-role
version: 1.0
created: 2026-06-15
---

# brief-coding-agent

Given a GitHub issue number, produce a standard Coding Agent subagent prompt in the
CLAUDE.md `## Subagents` format — so you don't hand-write the briefing each time you
deploy a coding subagent. Standardizes briefing quality; reduces per-deployment overhead.

## When to Use

Use this skill when:
- You're about to deploy a coding subagent (`prog` role) via the Task tool for a tracked issue
- PM or Lead Dev says "brief a coding agent for #N" / "spin up a subagent on #N"
- You're delegating implementation work and want a consistent, evidence-grounded briefing

**Do NOT use** for quick exploration/search subagents (those get no session log and report
back inline — see logging rule in Step 4). This skill is for substantive implementation work.

## Procedure

### Step 1: Fetch the issue

Repo is `mediajunkie/piper-morgan-product` (never the hallucinated `Codewarrior1988/...`).

```bash
gh issue view <N> --json number,title,body,labels,assignees
```

**Stop if** the issue doesn't exist or is unassigned — that's a STOP condition (#5 below).
Don't fabricate the task from the number alone.

### Step 2: Extract title, AC checklist, number, labels

Read the WHOLE issue body before extracting — the AC line often loses its referent in
isolation (CLAUDE.md "Verify First, Create Second"). Pull:
- **title** — for the `Task:` line
- **acceptance-criteria checklist** — the `- [ ]` / `- [x]` lines in the body, **verbatim**
- **number** + **labels** — for the `GitHub Issue:` line and context

Inline helper (title + AC; eyeball the rest from the full JSON):

```bash
gh issue view <N> --repo mediajunkie/piper-morgan-product --json number,title,body \
  --jq '"Task: " + .title + "\nGitHub Issue: #" + (.number|tostring) + "\nAcceptance Criteria:\n" +
        ([.body | split("\n")[] | select(test("^\\s*- \\[[ xX]\\]"))] | join("\n"))'
```

If the body has no `- [ ]` lines, the issue lacks an explicit AC checklist — note that to the
subagent and reconstruct AC from the issue body (don't ship an empty `Acceptance Criteria:`).

### Step 3: Generate the standard subagent prompt

Fill the CLAUDE.md `## Subagents` template exactly:

```
You are a Coding Agent working on Piper Morgan.
Task: <title>
GitHub Issue: #<number>
Acceptance Criteria:
<the AC checklist, verbatim>
Report back: tests added/passing with the exact `pytest path -v` command, files changed, and how to verify as a user.
```

### Step 4: Carry the real conventions into the prompt (do NOT invent new ones)

Append these as reminders so the subagent's output is audit-ready. All three are existing
CLAUDE.md conventions — cite them, don't paraphrase into something new:

- **Evidence Requirements** (CLAUDE.md "## Implementation Evidence") — the report back MUST include:
  ```
  ## Implementation Evidence
  - Tests: X tests added/modified in [file]
  - Verification: `pytest path/to/tests -v` (all passing)
  - Files: [list of modified files]
  - User verification: [how to test as user]
  ```
- **Subagent logging rule** (CLAUDE.md "Subagent logging rules") — a `prog` subagent doing
  substantive implementation SHOULD create its own session log; trivial work captured in a
  single entry can report back inline instead.
- **STOP conditions** (CLAUDE.md "## STOP Conditions") — instruct the subagent to STOP and
  escalate rather than push through. Most relevant for coding:
  - Pattern/class/function already exists → **complete it, don't duplicate it**
  - Tests fail for any reason → STOP
  - Found 75% complete code → report it (don't silently rebuild)
  - Can't provide verification evidence → STOP
  - "YOU DO NOT DECIDE which failures are critical — the PM decides."

### Step 5: After the subagent finishes — commit verification

Per CLAUDE.md "Commit verification after subagent work": after staging files for a commit
that includes subagent output, run `git status` and verify NO unstaged modified files remain
in `services/`, `tests/`, or `web/`. Subagents may touch files you didn't expect.

```bash
git status --short services/ tests/ web/   # expect empty after staging
```

If unstaged code files remain, either stage them or document in your session log why they're
excluded — prevents orphaned changes that silently break tests.

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---|---|---|
| Hand-write a bespoke briefing each time | Drifts in quality; omits Evidence/STOP conventions | Use this skill — one consistent template |
| Paraphrase AC instead of copying it | Subtle drift from the issue's actual criteria | Copy the `- [ ]` lines verbatim |
| Drop the Evidence Requirements block | Subagent returns "done" without proof (Pattern-045) | Always append the `## Implementation Evidence` shape |
| Invent new STOP/logging rules | Cohort conventions fragment | Cite the real CLAUDE.md conventions only |
| Skip Step 5 commit verification | Orphaned subagent edits break tests later | `git status` on services/tests/web after staging |
| Brief from the issue number alone | Confident wrong task if you didn't read the body | Fetch + read the WHOLE issue first |

## Quality Checklist

Before handing the generated prompt to the Task tool:
- [ ] Issue fetched and **exists + is assigned** (else STOP)
- [ ] AC checklist copied **verbatim** (or its absence noted)
- [ ] Prompt matches the CLAUDE.md `## Subagents` shape (Task / GitHub Issue / AC / Report back)
- [ ] Evidence Requirements block included (tests + `pytest` command + files + user verification)
- [ ] Logging rule + STOP conditions carried as reminders
- [ ] Step 5 commit-verification noted for after the subagent returns

## Examples

### Example: Briefing a subagent for issue #1124

```bash
gh issue view 1124 --repo mediajunkie/piper-morgan-product --json number,title,body,labels,assignees
```

Generated prompt:

```
You are a Coding Agent working on Piper Morgan.
Task: Migrate legacy elif intent.action dispatch chains to the workflow-dispatcher rail
GitHub Issue: #1124
Acceptance Criteria:
- [ ] Add WorkflowEntry(..., action_triggered=True) for the migrated cohort
- [ ] Lower MAX_DISPATCH_SITES to the new count in the same commit
- [ ] TestPreFloorDispatchSiteRatchet passes

Report back:
## Implementation Evidence
- Tests: tests added/modified in [file]
- Verification: `pytest tests/test_architecture_enforcement.py -v` (all passing)
- Files: [list of modified files]
- User verification: [how to test as user]

Reminders:
- prog role → create your own session log for this implementation work.
- STOP and escalate if: the handler already exists (complete it, don't duplicate);
  any test fails; you find 75%-complete code (report it); you can't show evidence.
  You do NOT decide which failures are critical — the PM does.
```

Then deploy via the Task tool. After it returns: `git status --short services/ tests/ web/`
(expect empty after staging) before committing.
