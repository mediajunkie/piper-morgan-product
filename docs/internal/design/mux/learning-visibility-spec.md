# D1: Learning Visibility Specification

**Issue**: #431 MUX-VISION-LEARN
**Deliverable**: 1 of 7
**Question Addressed**: When and how do learnings appear to users?

---

## Core Principle

**Layered visibility aligned with trust gradient.**

Users see more of Piper's learning as trust develops. This mirrors how human colleagues share observations—cautiously at first, more freely as rapport builds.

---

## Trust-Gated Visibility Matrix

| Trust Stage | What User Sees | How It Appears | User Must Ask? |
|-------------|----------------|----------------|----------------|
| **Stage 1 (New)** | Nothing proactive | Only on explicit query | Yes, always |
| **Stage 2 (Building)** | On-request summaries | Response to "what have you learned?" | Yes |
| **Stage 3 (Established)** | Periodic reflections | Batched summaries, passive browsing | No (but can mute) |
| **Stage 4 (Trusted)** | Proactive insights | Contextual surfacing + full history | No (but can mute) |

---

## Visibility Modes

### Pull Mode (All Trust Levels)

User explicitly requests learning information.

**Triggers**:
- "What have you learned about [topic]?"
- "Why did you suggest that?"
- "Show me your insights"
- Navigating to Insight Journal in UI

**Response Format**:
```
Based on our work together, I've noticed:

- [Insight 1] (confidence: high)
- [Insight 2] (confidence: medium)

Would you like me to explain any of these?
```

**Language Pattern**: Present tense, first person, hypothesis framing.

### Passive Mode (All Trust Levels)

Learnings are browsable but not surfaced.

**Location**: Dedicated section in Piper's space (not notifications)

**Organization**: Topical with recency weighting
- Topics derived from work areas (calendar, projects, communication)
- Recent insights appear first within each topic
- Confidence indicators visible but subtle

**UI Principle**: User chooses to look; Piper doesn't draw attention.

### Push Mode (Stage 3+ Only)

Piper proactively surfaces relevant insights.

**Thresholds for Push**:
| Factor | Minimum |
|--------|---------|
| Confidence | 0.75+ |
| Relevance to current context | High |
| Trust level | Stage 3+ |
| Time since last push | 24+ hours |

**Push Language**:
- "Can I share something that might be relevant?"
- "I've noticed something that could help here..."
- "Having reflected on our recent work..."

**Anti-Pattern Language** (never use):
- "ALERT: Pattern detected"
- "I've been watching and noticed..."
- "While monitoring your activity..."

---

## Default vs Opt-In Settings

### Default Behavior by Stage

| Stage | Push | Passive | Pull |
|-------|------|---------|------|
| 1 | Off | Available | Available |
| 2 | Off | Available | Available |
| 3 | On (batched) | Available | Available |
| 4 | On (contextual) | Available | Available |

### User Overrides

Users MAY opt into pushier settings at any trust level:
- "Show me insights even though we're still getting to know each other"
- This is recorded as explicit preference, not trust progression

Users MAY opt into quieter settings at any trust level:
- "Don't proactively share insights"
- This mutes push mode without affecting trust level

**Design Note**: Opting for quieter settings should NOT be interpreted as trust regression. Some users prefer pull-only regardless of relationship quality.

---

## Timing Rules

### When Learnings Surface

**Push timing** (Stage 3+):
- During natural conversation pauses
- At start of new work sessions (morning standup)
- When context makes insight directly relevant
- Never during user's focused work (detect deep work mode)

**Reflection summaries** (Stage 3):
- Weekly by default
- Configurable: daily, weekly, biweekly, never
- Delivered at start of day, not interrupting

### When Learnings Do NOT Surface

- During active conversation flow
- When user has indicated "focus mode"
- Within 24 hours of previous push
- When confidence is below threshold
- When relevance to current context is low

---

## UI Placement Options

### Primary Location: Insight Journal

Dedicated, user-navigable space containing all learnings.

**Access**:
- Navigation menu item: "What Piper's Learned"
- Command: "show insights" or "what have you learned"
- Keyboard shortcut (configurable)

**Organization**:
```
Insight Journal
├── Work Patterns
│   ├── Meeting preferences (high confidence)
│   └── Communication style (medium confidence)
├── Project Insights
│   ├── [Project A] observations
│   └── [Project B] observations
├── People & Collaboration
│   └── Working relationships
└── Recent Reflections
    └── Last composting cycle results
```

### Secondary Location: Contextual Hints

For Stage 4 users, insights may appear inline:

**Example**: When scheduling a meeting:
> "Based on past patterns, you tend to prefer morning meetings for deep discussions. Want me to suggest morning slots?"

**Interaction**: User can dismiss, accept, or ask "why do you think that?"

### Tertiary Location: Morning Standup

Natural integration point for reflection summaries:

> "Good morning! A few things from my recent reflections:
> - I noticed the Johnson project tends to need attention on Fridays
> - Your calendar has been heavy on back-to-back meetings lately
>
> Anything you'd like me to dig into?"

---

## Confidence Display

### When to Show Confidence

| Context | Show Confidence? |
|---------|-----------------|
| Insight Journal browsing | Yes (subtle indicator) |
| Push surfacing | No (implies doubt) |
| User asks "why" | Yes (explains basis) |
| Uncertain inference | Yes (seeking confirmation) |

### Confidence Indicators

**Visual** (in Insight Journal):
- High (0.8+): Solid indicator
- Medium (0.6-0.8): Partial indicator
- Low (0.4-0.6): Outline only (pull-only, not pushed)

**Verbal** (in conversation):
- High: "I've noticed that..." (no qualifier)
- Medium: "I think..." or "It looks like..." (prefer over "It seems like...")
- Low: "I'm not sure, but it looks like..."

> **CXO Note (2026-01-23)**: Prefer "I think..." or "It looks like..." over "It seems like..." for medium confidence. "Seems" is slightly hedging; "think" and "looks like" are more direct while still expressing appropriate uncertainty.

---

## Privacy Considerations

### What's Never Shown Without Explicit Request

- Raw Session Journal entries (Stage 4+ on request only)
- Learning derivation details (available on "why" query)
- Cross-user patterns (never—Piper learns per-user only)
- Deleted or corrected learnings (permanently removed from view)

### Transparency on Request

User can always ask:
- "What data did you use to learn this?"
- "When did you notice this pattern?"
- "How confident are you in this?"

Piper must answer these honestly and completely.

---

## Success Metrics

This specification succeeds if:

- [ ] Users at Stage 1-2 never feel interrupted by learning
- [ ] Users at Stage 3+ find proactive insights helpful, not creepy
- [ ] Users can always find their way to the Insight Journal
- [ ] Confidence indicators help calibrate user trust in insights
- [ ] Users report feeling "informed" not "watched"

---

## Decision Record

### Insight Journal stage-specific visual treatment — keep generic (MVP)

**Decided 2026-06-16** (CXO + PPM dual-nod; closes #1048, the design question deferred from #1031 Q3).

The Insight Journal **page** does not differentiate its visual presentation by trust stage for MVP. It works at all four stages (server-rendered `window.trustStage` + endpoint behavior); the *presentation* stays generic.

**Rationale**: the Insight Journal is a **Pull-mode / browse-on-demand** surface — the user explicitly came to look. The trust gradient is most load-bearing on **proactive (Push)** surfaces, where "creepy vs. helpful" is at stake — not on a page the user deliberately opened. Stage-specific affordance gating (Options 2/3 in #1048) is post-MVP polish if ever warranted, not a beta requirement.

Supersedes the `Stage-specific visual treatment if any (TBD per spec)` placeholder from #1031.

---

## Related Specifications

- **D2**: Control Interface Patterns (how users modify what they see)
- **D4**: Insight Journal Surfacing Rules (detailed push/pull triggers)
- **D7**: Trust-Based Access Rules (how trust gates visibility)

---

*Specification: D1 Learning Visibility*
*Issue: #431 MUX-VISION-LEARN*
*Created: 2026-01-22*
