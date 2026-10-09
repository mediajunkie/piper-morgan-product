---
name: narrative-verification
description: Prevent fabrication when writing narrative blog posts from session logs or omnibus logs — adds a verification checkpoint layer on top of existing voice/template standards.
scope: role-specific
version: 1.0
created: 2026-02-12
---

# Narrative Verification Skill

**Purpose**: Prevent fabrication when writing narrative blog posts from session logs or omnibus logs.

**When to use**: Any narrative piece ("The Drift We Didn't See," "The Calendar That Wasn't Mine") where the source material is logs describing what happened.

**Does NOT replace**: Voice & Tone Style Guide, blog post templates, existing formatting standards. This skill ADDS a verification layer.

---

## Core Principle

**Placeholders are safeguards, not clutter.**

When you encounter a gap in the narrative, the placeholder IS the correct content. Filling it with plausible fabrication defeats its purpose. The PM will provide the missing detail — or decide it's not needed.

---

## Pre-Draft: Facts Extraction (REQUIRED)

Before writing ANY prose, create a verified facts list from the source logs.

### Extract and cite:
```
## Verified Facts from [Log Name]

### Trigger/Origin
- [What actually started this? Line/timestamp reference]

### Sequence of Events
- [First thing that happened - cite line]
- [Second thing - cite line]
- [etc.]

### Specific Numbers
- [Files changed: X - cite line]
- [Duration: X - cite line]
- [Issues created: X - cite line]

### Quotes/Exact Phrasing
- [Any direct quotes from log - cite line]

### Causality
- [What caused what? Only if explicitly stated in log]

### NOT IN LOGS (will need placeholders)
- [List what the narrative needs but logs don't provide]
```

Only after this extraction is complete should you begin drafting.

---

## Claims Requiring Verification

These categories are high-risk for fabrication. If you can't cite a source line, use a placeholder.

| Category | Example | Risk |
|----------|---------|------|
| **Triggers** | "It started with X" | Often invented to create narrative arc |
| **Numbers** | "73 columns," "three days" | Easy to misremember or round |
| **Sequences** | "X led to Y led to Z" | Causality often invented |
| **Timestamps** | "8:06 AM," "by afternoon" | Specific times need verification |
| **Technical details** | "migration hash," "function name" | Plausible but often wrong |
| **Emotional moments** | "the moment we realized" | Logs rarely capture feelings |
| **Comparisons** | "faster than before" | Need baseline evidence |

---

## Placeholder Templates

Use specific placeholders that explain what's needed:

```markdown
[PM PLACEHOLDER: What was the actual trigger for this investigation?
Logs show X but not what prompted looking at X initially.]

[PM PLACEHOLDER: The logs show 47 columns, not 73. Please verify
the correct number, or explain if 73 refers to something else.]

[PM PLACEHOLDER: How did you feel when this was discovered?
Logs don't capture the emotional moment.]

[PM PLACEHOLDER: Is this sequence correct? Logs show A and B
but don't explicitly state A caused B.]
```

---

## Red Flags: Common Fabrication Patterns

Stop and verify if you notice yourself:

1. **Inverting causality** — Something discovered DURING work becomes the "trigger" for that work
2. **Smoothing details** — Adding specifics (times, names, numbers) that make the story flow but aren't in logs
3. **Narrative completion** — Filling gaps because the story "needs" something there
4. **Memory-feeling** — Writing details that feel like memory but have no citation
5. **Plausible specifics** — Technical details (hashes, function names) that could be true but aren't verified

When you catch yourself doing any of these: **STOP and create a placeholder instead.**

---

## Verification Checkpoint

Before delivering a draft, review each specific claim:

- [ ] Trigger/origin — cited from log?
- [ ] All numbers — cited from log?
- [ ] Sequence/causality — explicitly stated in log, or marked as interpretation?
- [ ] Technical details — verified or placeholdered?
- [ ] Timeline — matches log timestamps?
- [ ] Quotes — actually in the log?

Any unchecked item → add placeholder or remove claim.

---

## Integration with Existing Workflow

This skill fits INTO the existing process:

```
1. Receive logs from PM
2. Read logs thoroughly
3. ★ NEW: Create Verified Facts extraction ★
4. Pitch narrative ideas (based on verified facts)
5. PM approves direction
6. Draft narrative (using extraction as guardrails)
7. ★ NEW: Run Verification Checkpoint before delivery ★
8. Deliver draft with placeholders intact
9. PM reviews, fills placeholders, polishes
10. Publish
```

Steps 3 and 7 are the additions. Everything else stays the same.

---

## Why This Matters

Narrative pieces tell readers "here's what happened." Fabricated details — even small ones — erode trust and create false records. The PM has the actual memories; we have the logs. When logs are insufficient, we ask. We don't invent.

---

*Version 1.0 — February 12, 2026*
*Created after Calendar and Drift fabrication incidents*
