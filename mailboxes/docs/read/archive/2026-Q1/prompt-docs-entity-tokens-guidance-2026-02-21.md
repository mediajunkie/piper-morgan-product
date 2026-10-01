# Prompt: Add Entity Token Guidance to Implementation Guide

**For**: Docs Agent or Lead Developer
**Task**: Documentation update
**Effort**: ~15 minutes
**GitHub Issue**: Can reference #818

---

## Task

Add a subsection to `knowledge/conversational-glue-implementation-guide.md` clarifying the difference between entity token echoing (acceptable) and parrot confirmations (not acceptable).

## Location

Section 5: Anti-Robotics Patterns

Add after the existing subsections, before Section 6.

## Content to Add

```markdown
### 5.X Entity Names vs. Parrot Confirmations

**Principle**: Entity names are identifiers, not user input to paraphrase.

When responses reference specific entities (projects, people, meetings), the name should be echoed exactly so the user knows which entity is being referenced. This is distinct from parrot confirmations, which echo the user's full message.

| Pattern | Example | Acceptable? |
|---------|---------|-------------|
| Entity name echo | "I couldn't find a project called 'Q3 Roadmap'" | ✅ Yes |
| Entity name echo | "Are you sure you want to delete 'Henderson Account'?" | ✅ Yes |
| Parrot confirmation | "You said 'schedule meeting with Sarah Tuesday'" | ❌ No |
| Parrot confirmation | "You want to create a project. I will create a project." | ❌ No |

**Formatting guideline**: Use single quotes around entity names in prose to distinguish them from surrounding text.

**Colleague Test application**: A colleague would say "You mean the Henderson account?" not "You mean the thing you mentioned." Entity specificity is natural; full-message echoing is robotic.

**Gate 2 audit note**: Entity name echoing should NOT be flagged as parrot behavior during anti-flattening verification.
```

## Verification

After adding:
1. Confirm subsection number is correct (may need to be 5.4 or 5.5 depending on current structure)
2. Update table of contents if the document has one
3. No other files need updating — this is guidance, not a code pattern

---

*Brief task. Can be done in same session as other docs work or standalone.*
