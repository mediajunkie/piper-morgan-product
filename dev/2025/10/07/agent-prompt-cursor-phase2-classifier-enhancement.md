# Prompt for Cursor Agent: GREAT-4F Phase 2 - Classifier Prompt Enhancement

## Context

GREAT-4F mission: Improve classifier accuracy from 85-95% to 95%+ for canonical categories.

**This is Phase 2**: Enhance classifier prompts with disambiguation rules to reduce TEMPORAL/STATUS/PRIORITY mis-classification as QUERY.

## Session Log

Start new log: `dev/2025/10/07/2025-10-07-0932-prog-cursor-log.md`

## Mission

Find and enhance the LLM classifier prompts to better distinguish canonical categories (TEMPORAL, STATUS, PRIORITY) from generic QUERY intents.

---

## Background from GREAT-4E & Phase 1

**What we know**:
- Current classifier accuracy: 85-95%
- Main issue: TEMPORAL/STATUS/PRIORITY queries mis-classified as QUERY
- Phase 1 added fallback to prevent timeout errors
- Goal: Improve accuracy to 95%+ to reduce mis-classifications at source

**Phase 1 patterns** (from Code Agent):
- TEMPORAL: calendar, schedule, meeting, today, tomorrow, time, date, appointment, agenda, event, when, timing
- STATUS: status, standup, working on, progress, current, update, sprint, tasks
- PRIORITY: priority, priorities, important, urgent, critical, focus, top, key

---

## Task 1: Locate Classifier Prompts

**Likely locations** (check in this order):

1. `services/intent_service/classifier.py`
2. `services/llm/prompts/intent_classifier.py`
3. `services/intent_service/intent_service.py` (inline prompts)
4. `services/llm/` directory (any prompt-related files)

**What to look for**:
- Prompt templates for intent classification
- Category definitions
- Example queries for each category
- Classification instructions

**If not found**: Search broadly:
```bash
grep -r "IntentCategory" services/ | grep -i "prompt\|classify\|instruction"
grep -r "TEMPORAL.*QUERY\|classification.*prompt" services/
```

---

## Task 2: Enhance Prompts with Disambiguation

### Add Disambiguation Rules Section

Insert this into the classifier prompt (adapt to existing format):

```markdown
## CRITICAL DISAMBIGUATION RULES

When a query could match multiple categories, apply these rules:

### TEMPORAL vs QUERY
If the query is asking about:
- Time-related information (when, schedule, calendar, dates, appointments) → TEMPORAL
- Time as a general fact (e.g., "what time is it in Tokyo?") → QUERY

Examples:
- "what's on my calendar today?" → TEMPORAL (user's personal schedule)
- "what time is the Super Bowl?" → TEMPORAL (event scheduling)
- "what's the current time?" → TEMPORAL (time information)
- "what's the history of timekeeping?" → QUERY (general knowledge)

Key indicators for TEMPORAL:
- Personal pronouns (my, our) + time/schedule words
- Specific time periods (today, tomorrow, this week, next month)
- Calendar/scheduling verbs (scheduled, meeting, appointment)
- Event timing questions (when is X?)

### STATUS vs QUERY
If the query is asking about:
- Current work, progress, or activities → STATUS
- General information or facts → QUERY

Examples:
- "what am I working on?" → STATUS (current work status)
- "show my standup" → STATUS (status update)
- "what's my progress on project X?" → STATUS (work progress)
- "what is the status of the economy?" → QUERY (general information)

Key indicators for STATUS:
- Personal pronouns (I, my, our) + work/progress words
- Project/task-related questions about current state
- Words like: standup, working on, progress, current, sprint, tasks

### PRIORITY vs QUERY
If the query is asking about:
- What should be focused on, importance ranking → PRIORITY
- General rankings or lists → QUERY

Examples:
- "what should I focus on today?" → PRIORITY (personal priorities)
- "what are my top priorities?" → PRIORITY (priority ranking)
- "what's most important right now?" → PRIORITY (priority assessment)
- "what are the top 10 movies?" → QUERY (general rankings)

Key indicators for PRIORITY:
- Personal pronouns (I, my, our) + importance/priority words
- Words like: focus, priority, important, urgent, critical, top, key
- Questions about what to work on next

### General Rule
If in doubt between canonical (TEMPORAL/STATUS/PRIORITY) and QUERY:
- Has personal pronouns (I, my, our) + category keywords → Canonical category
- No personal context or general knowledge question → QUERY
```

### Enhance Category Definitions

For each canonical category, add disambiguation examples:

**TEMPORAL** - Add these examples:
- ✅ "what's on my calendar?" (personal schedule)
- ✅ "when is my next meeting?" (personal event)
- ✅ "show me today's schedule" (personal schedule)
- ❌ "what year was the Declaration signed?" (historical fact → QUERY)
- ❌ "how do calendars work?" (general knowledge → QUERY)

**STATUS** - Add these examples:
- ✅ "show my standup" (work status)
- ✅ "what am I working on?" (current tasks)
- ✅ "progress on project X?" (work progress)
- ❌ "what's the status of climate change?" (general info → QUERY)
- ❌ "how do status updates work?" (general knowledge → QUERY)

**PRIORITY** - Add these examples:
- ✅ "what should I focus on?" (personal priorities)
- ✅ "what's most important today?" (priority ranking)
- ✅ "show me top priorities" (personal priorities)
- ❌ "what are the top 10 restaurants?" (general ranking → QUERY)
- ❌ "how do you prioritize work?" (general advice → GUIDANCE or QUERY)

---

## Task 3: Add Confidence Scoring Guidance

If the prompt supports confidence scoring, add:

```markdown
## Confidence Scoring for Canonical Categories

When classifying into TEMPORAL, STATUS, or PRIORITY:
- High confidence (0.9-1.0): Query has personal pronouns + clear category keywords
- Medium confidence (0.7-0.9): Category keywords present but context ambiguous
- Low confidence (<0.7): Consider QUERY instead

For QUERY category:
- High confidence (0.9-1.0): General knowledge, no personal context
- Medium confidence (0.7-0.9): Could be canonical but lacks clear indicators
- Low confidence (<0.7): Likely belongs to a canonical category
```

---

## Task 4: Document Changes

Create a brief summary of changes in:
`dev/2025/10/07/classifier-prompt-enhancements.md`

Include:
- What prompts were modified
- What disambiguation rules were added
- Rationale for each change
- Expected impact on accuracy

---

## Verification

After enhancing prompts:

```bash
# Verify prompts were updated
grep -n "DISAMBIGUATION" services/intent_service/classifier.py
# Or whatever file contains prompts

# Count new examples added
grep -c "✅\|❌" [prompt-file]
# Should show positive/negative examples added

# Check file was modified recently
ls -la [prompt-file]
```

---

## Success Criteria

- [ ] Classifier prompts located and reviewed
- [ ] Disambiguation rules added for TEMPORAL vs QUERY
- [ ] Disambiguation rules added for STATUS vs QUERY
- [ ] Disambiguation rules added for PRIORITY vs QUERY
- [ ] Positive and negative examples added for each canonical category
- [ ] Confidence scoring guidance added (if applicable)
- [ ] Changes documented in summary file
- [ ] Session log updated

---

## Critical Notes

- The prompt format may vary (could be Python strings, markdown files, JSON, etc.)
- Adapt the disambiguation rules to match existing prompt style
- Don't break existing functionality - enhance, don't replace
- Focus on canonical categories (TEMPORAL, STATUS, PRIORITY) vs QUERY distinction
- Personal pronouns + category keywords are the key signal

---

## STOP Conditions

- If classifier prompts not found in expected locations, document what you searched and ask PM
- If prompt format is unclear or complex, document and ask PM
- If enhancing prompts would break existing structure, document and ask PM

---

**Effort**: Medium (~30-45 minutes)
**Priority**: HIGH (core of GREAT-4F improvement)
**Deliverable**: Enhanced classifier prompts with disambiguation rules
