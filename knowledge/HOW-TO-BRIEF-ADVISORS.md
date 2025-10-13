# How to Brief New Advisors - PM Quick Reference

**Last Updated:** October 10, 2025, 7:05 PM
**For:** PM (that's you!) when onboarding new Lead Dev or Chief Architect chat advisors
**Context:** You optimized briefing flow today, saving 82% tokens. Here's how to use it.

---

## Before You Start

**Check:** Does the new advisor have Claude Desktop with Serena MCP access?

- ✅ **YES, they have Serena MCP** → Use **Track 1** below
- ❌ **NO, they're on Claude.ai web only** → Use **Track 2** below

---

## Track 1: Advisor Has Claude Desktop + Serena MCP ✅

### What to Tell Them (Copy-Paste Ready)

```
Welcome! Before we dive in, let's get you briefed efficiently.

First, run these three Serena queries to get current system state (~212 tokens):

1. Intent categories:
mcp__serena__find_symbol("IntentService", depth=1, include_body=false)

2. Active integrations:
mcp__serena__list_dir("services/integrations", recursive=false)

3. Architecture patterns:
mcp__serena__list_dir("docs/internal/architecture/current/patterns", recursive=false)

See knowledge/serena-briefing-queries.md for what these return.

Next, read your role briefing:
- Lead Developer → knowledge/BRIEFING-ESSENTIAL-LEAD-DEV.md (~650 words)
- Chief Architect → knowledge/BRIEFING-ESSENTIAL-ARCHITECT.md (~similar)

That's your briefing! (~2,000 tokens total vs 11,000 the old way)

Templates like agent-prompt-template.md (4K words!) are loaded just-in-time:
- Need to deploy agents? THEN read agent-prompt-template.md
- Need to create log? THEN read session-log-instructions.md
- Questions arise? THEN read specific methodology docs

Don't frontload everything - you'll burn 50% of context!
```

### Expected Flow

1. They run 3 Serena queries → see current state (~1 minute)
2. They read role briefing → understand responsibilities (~3 minutes)
3. They see JIT triggers → know what to load when needed
4. Total briefing time: ~4 minutes, ~2,000 tokens

### If They Ask Questions

**"What are these queries returning?"**
→ "See knowledge/serena-briefing-queries.md for examples. You'll get counts and lists: 8 intent categories, 7 plugins, 33 patterns as of today."

**"What if I need more detail?"**
→ "Check knowledge/claude-desktop-briefing-guide.md - it has scenarios and a cheat sheet."

**"Do I need to read CURRENT-STATE.md?"**
→ "No! The Serena queries replace that (79% token savings). CURRENT-STATE is for sprint/epic position only if you need it."

---

## Track 2: Advisor Does NOT Have Serena MCP ❌

### What to Tell Them (Copy-Paste Ready)

```
Welcome! You don't have Serena MCP access, so I'll run the system state queries for you.

[You run these three queries via Claude Code or Cursor with Serena:]

mcp__serena__find_symbol("IntentService", depth=1, include_body=false)
mcp__serena__list_dir("services/integrations", recursive=false)
mcp__serena__list_dir("docs/internal/architecture/current/patterns", recursive=false)

[Then paste the condensed results to them:]

Here's current Piper Morgan system state:

**Intent Classification:**
- 8 intent categories: conversation, query, execution, analysis, synthesis, strategy, learning, unknown
- 13 canonical handlers for specific operations
- 25 total methods in IntentService

**Active Integrations:**
- 7 plugins: slack, github, notion, calendar, demo, mcp, spatial

**Architecture Patterns:**
- 33 documented patterns (pattern-000 through pattern-033)
- 5 categories: Core Architecture, Data & Query, AI & Intelligence, Integration & Platform, Development & Process

Next, read your role briefing:
- Lead Developer → knowledge/BRIEFING-ESSENTIAL-LEAD-DEV.md (~650 words)
- Chief Architect → knowledge/BRIEFING-ESSENTIAL-ARCHITECT.md (~similar)

That's your briefing! Templates are loaded just-in-time when you actually need them.
```

### Your Workflow

1. **You run Serena queries** (via Code/Cursor agent with MCP)
2. **You paste condensed results** to advisor (~200 tokens)
3. **They read role briefing** (~650 words)
4. **Total briefing:** ~2,000 tokens (vs 11,000 old way)

### Alternative: Pre-Generated Daily Briefing

If you're onboarding multiple advisors in one day:

1. Run the 3 Serena queries once
2. Save output to `knowledge/BRIEFING-DAILY-2025-10-10.md`
3. Tell advisors: "Read knowledge/BRIEFING-DAILY-{today's date}.md"

This way you run queries once, multiple advisors can use result.

---

## Common Pitfalls to Avoid

### ❌ DON'T Say:
- "Read CURRENT-STATE.md first" → That's 1,034 tokens! Serena queries are 212 tokens.
- "Read all the methodology docs" → That's 2,000+ tokens! JIT loading only.
- "Check out agent-prompt-template.md" → That's 4,000 words! Only when deploying agents.

### ✅ DO Say:
- "Run these 3 Serena queries" (if they have MCP)
- "Here's the system state" (if you ran queries for them)
- "Read your role briefing - it's short"
- "Templates are loaded when you need them"

---

## Token Budget Comparison

### Old Way (Pre-Oct 10, 2025)
```
CLAUDE.ai-project-instructions: 150 words
BRIEFING-ESSENTIAL-LEAD-DEV: 650 words
00-START-HERE-LEAD-DEV: 1,100 words
BRIEFING-CURRENT-STATE: 1,034 tokens
agent-prompt-template: 4,000 words
session-log-instructions: 1,500 words
methodology docs: 2,000 words
---
TOTAL: ~11,000 tokens (50% of 200K context)
```

### New Way (Post-Oct 10, 2025)
```
CLAUDE.ai-project-instructions: 200 words (added Serena)
Serena queries OR condensed results: 212 tokens
BRIEFING-ESSENTIAL-LEAD-DEV: 650 words
JIT triggers (not loaded): 0 tokens
---
TOTAL: ~2,000 tokens (10% of context)
SAVINGS: 82% reduction
```

---

## Quick Reference Scripts

### Script 1: Brief Lead Dev with Serena Access

```
"Hey! Quick briefing process:

1. Run these 3 Serena queries [paste the 3 mcp__serena commands]
2. Read knowledge/BRIEFING-ESSENTIAL-LEAD-DEV.md
3. Done! (~2K tokens vs 11K the old way)

Templates load just-in-time when you need them. Don't frontload everything."
```

### Script 2: Brief Lead Dev WITHOUT Serena

```
"Hey! I'll get you briefed quickly.

[You run Serena queries via Code/Cursor]
[You paste condensed results - see Track 2 above]

Now read knowledge/BRIEFING-ESSENTIAL-LEAD-DEV.md

Done! (~2K tokens vs 11K the old way)"
```

### Script 3: Brief Chief Architect (Same Pattern)

Same as above but use:
- `knowledge/BRIEFING-ESSENTIAL-ARCHITECT.md` instead of LEAD-DEV
- Same Serena queries (system state is same for all roles)

---

## Files They Should Read (In Order)

### Always Read (Frontload)
1. **Serena query results** OR condensed system state you provide
2. **BRIEFING-ESSENTIAL-{ROLE}.md** - Their role-specific briefing

### Sometimes Read (JIT - Just In Time)
- **agent-prompt-template.md** → Only when deploying agents
- **session-log-instructions.md** → Only when creating first log
- **methodology-*.md files** → Only when methodology questions arise
- **BRIEFING-CURRENT-STATE.md** → Only if need sprint/epic position (not for system state!)

### Never Read (Unless Explicitly Needed)
- **BRIEFING-METHODOLOGY.md** → Only if deep dive on process needed
- **BRIEFING-PROJECT.md** → Only if context on Piper's purpose needed
- **gameplan-template.md** → Only Chief Architect creating gameplans
- **All other templates** → Only when specifically using them

---

## Validation Checklist

After briefing a new advisor, verify:

- [ ] Did they use ≤2,500 tokens for briefing? (Good!)
- [ ] Did they frontload agent-prompt-template? (Bad! That's 4K words)
- [ ] Did they read CURRENT-STATE for system capabilities? (Bad! Use Serena queries)
- [ ] Did they understand JIT loading concept? (Ask: "When do you read session-log-instructions?")
- [ ] Are they ready to start work? (Can they articulate their role and current system state?)

---

## Troubleshooting

### "They're at 50% context after briefing"
→ They frontloaded templates. Tell them to start over with just:
   1. Serena queries (or your condensed results)
   2. Role briefing
   3. JIT triggers

### "They can't find Serena tools"
→ They're on Claude.ai web, not Desktop. Use Track 2 (you run queries for them).

### "They're confused about what to read"
→ Show them this file. Point to Track 1 or Track 2 based on their MCP access.

### "They want the 'full context'"
→ Explain: The old way burned 50% context. New way is 10%. They get MORE working context by loading less briefing. Serena queries are always current (static docs can be stale).

---

## Success Stories to Reference

**Oct 10, 2025 - This Optimization:**
- Identified Lead Dev briefing was 11K tokens (50% context)
- Implemented Serena-first + JIT loading
- Achieved 82% reduction (11K → 2K tokens)
- Same pattern works for Chief Architect

**Key Insight:**
Front-loading everything "just in case" wastes context. Load system state via queries (always current), load templates only when actually using them.

---

## Version History

- **v1.0** (Oct 10, 2025, 7:05 PM) - Initial version
  - Track 1: With Serena MCP access
  - Track 2: Without Serena MCP access
  - Scripts for Lead Dev and Chief Architect
  - Validation checklist and troubleshooting

---

**File Location:** `/Users/xian/Development/piper-morgan/knowledge/HOW-TO-BRIEF-ADVISORS.md`

**Next Time You Brief an Advisor:**
1. Open this file
2. Check if they have Serena MCP access
3. Follow Track 1 or Track 2
4. Copy-paste the script
5. Verify with checklist
6. Done!

**You're welcome, Future PM! 👋**
