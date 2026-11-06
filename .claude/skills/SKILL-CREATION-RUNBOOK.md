# Skill Creation Runbook

**Purpose**: Step-by-step guide for creating new Claude Code skills
**Last Updated**: January 25, 2026

---

## Before You Start

### Check Current Best Practices

Anthropic's skill recommendations evolve. Before creating a new skill:

```
Search: "Anthropic Claude Code skills best practices [current year]"
Check: https://docs.anthropic.com/claude-code/skills (or current URL)
```

**Key things to verify**:
- Required frontmatter fields (currently: `name`, `description`)
- Discovery mechanism (currently: description-based keyword matching)
- File structure requirements
- Any new features or deprecations

---

## Skill Creation Checklist

### Step 1: Identify the Candidate

Before creating a skill, score against the formalization rubric (≥3 = formalize):

| Criterion | Score |
|-----------|-------|
| **Frequency**: Happens 3+ times per week across agents | 0-1 |
| **Friction**: Agents doing it inconsistently or asking "how?" | 0-1 |
| **Error Cost**: Mistakes cause rework or PM intervention | 0-1 |
| **Docs Exist**: Procedure already written somewhere | 0-1 |
| **Cross-Role**: Multiple roles need it | 0-1 |

**Total ≥3?** → Proceed to create skill

### Step 2: Create Directory Structure

```bash
mkdir -p .claude/skills/my-skill-name
touch .claude/skills/my-skill-name/SKILL.md
```

**Naming convention**: lowercase, hyphen-separated (e.g., `create-session-log`, `audit-cascade`)

### Step 3: Write Frontmatter (CRITICAL)

The frontmatter enables Claude to discover your skill. **This is not optional.**

```yaml
---
name: my-skill-name
description: What this skill does and when to use it. Include trigger
  phrases and contexts so Claude can match user requests to this skill.
scope: cross-role | role-specific
version: 1.0
created: YYYY-MM-DD
---
```

**Set `scope:` by asking "who runs this cold if the owner is unavailable?"** If any agent could, it's `cross-role`, and the body must not assume the owner's context. If only one role can, say which. (xian accepted this as #1715 row 3, 2026-11-06; the bus-factor taxonomy is in `docs/internal/operations/skill-candidates-review.md`.)

**Description best practices**:
- Include WHAT the skill does
- Include WHEN to use it (trigger contexts)
- Include trigger PHRASES users might say
- Keep under 200 characters for efficient discovery
- Be specific with keywords

**Good example**:
```yaml
description: Create or resume a session log at session start. Use when
  starting a new session, when PM assigns work, or after context
  compaction to find and continue your existing log.
```

**Bad example**:
```yaml
description: Handles session logs.
```

### Step 4: Write the SKILL.md Body

Structure:
```markdown
# skill-name

One-line description matching the frontmatter.

## When to Use

Use this skill when:
- Specific trigger condition 1
- Specific trigger condition 2
- Specific trigger condition 3

## Procedure

### Step 1: [Action]
[Details, commands, examples]

### Step 2: [Action]
[Details, commands, examples]

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Bad pattern | Reason | Good pattern |

## Quality Checklist

After using this skill:
- [ ] Verification item 1
- [ ] Verification item 2

## Examples

### Example 1: [Scenario]
[Concrete example with inputs and outputs]
```

**Keep SKILL.md under 500 lines**. If longer, move reference material to separate files.

### Step 5: Add to SKILLS.md Index

Update `.claude/skills/SKILLS.md`:

```markdown
| [my-skill-name](./my-skill-name/SKILL.md) | cross-role | Brief description | 1.0 |
```

### Step 6: Verify Discovery

Test that Claude can discover the skill:

1. Start a new Claude Code session
2. Ask: "What skills are available?"
3. Verify your skill appears with correct description
4. Test invocation: "Use the my-skill-name skill to..."

### Step 7: Pilot and Iterate

- Use the skill in real work for 1 week
- Note any gaps or confusion
- Update based on feedback
- Update version number for significant changes

---

## Frontmatter Field Reference

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | **Yes** | Skill identifier, matches directory name |
| `description` | **Yes** | Discovery text - Claude matches requests against this |
| `scope` | No | `cross-role` or `role-specific` |
| `version` | No | Semantic version for tracking changes |
| `created` | No | Creation date |
| `disable-model-invocation` | No | If `true`, only user can invoke via `/skill-name` |
| `user-invocable` | No | If `false`, hidden from `/` menu (background knowledge) |
| `allowed-tools` | No | Restrict which tools Claude can use |
| `context` | No | `fork` to run in subagent |

---

## Common Mistakes

1. **Missing frontmatter** → Skill won't be discovered
2. **Vague description** → Claude won't match it to requests
3. **Missing trigger phrases** → Users say "audit cascade", skill says "phase validation"
4. **Too long** → Over 500 lines buries the key instructions
5. **Not updating SKILLS.md** → Manual discovery fails

---

## Maintenance

### When Anthropic Updates Best Practices

1. Check docs quarterly (or when skills seem broken)
2. Update this runbook with new requirements
3. Audit existing skills for compliance
4. Update frontmatter fields if needed

### When Adding New Skills

1. Follow this runbook
2. Add to SKILLS.md index
3. Announce in relevant mailboxes if cross-role

---

*Runbook created by Documentation Management Specialist*
*January 25, 2026*
