# Claude Desktop Briefing Guide

**For:** Chat advisors using Claude Desktop (away from codebase with MCP access)

**Purpose:** Get fresh Piper Morgan context using Serena symbolic queries

**Updated:** 2025-10-10

---

## Quick Start: Getting Project Context

### Option 1: If You Have Serena MCP Connected ✅

**Use symbolic queries** for always-current information:

```
Can you run these Serena queries to brief me on Piper Morgan's current state:

1. Intent system:
mcp__serena__find_symbol("IntentService", depth=1, include_body=false)

2. Active plugins:
mcp__serena__list_dir("services/integrations", recursive=false)

3. Pattern catalog:
mcp__serena__list_dir("docs/internal/architecture/current/patterns", recursive=false)
```

**You'll get:**
- Current intent categories (8 as of 2025-10-10)
- Active integrations (7 plugins)
- Architecture patterns (33 documented)

**Token usage:** ~212 tokens (vs ~1,034 for static docs)

### Option 2: If You Don't Have Serena ⚠️

**Ask PM for latest briefing** or use these knowledge base files:
- `BRIEFING-CURRENT-STATE.md` - Project status
- `serena-briefing-queries.md` - Query patterns reference
- `CLAUDE.md` - Agent briefing instructions

---

## Understanding Serena Queries

**What is Serena?**
- MCP server for symbolic code analysis
- Queries live codebase structure
- Returns precise, current information

**Why use it?**
- ✅ Always accurate (not stale docs)
- ✅ Token efficient (79% savings)
- ✅ Self-maintaining (auto-updates)
- ✅ Verifiable (re-run anytime)

**When to use it?**
- Getting system state
- Understanding code structure
- Checking what exists
- Verifying counts and lists

---

## Essential Queries for Chat Advisors

### 1. What Can Piper Do? (Intent System)

**Query:**
```
mcp__serena__find_symbol("IntentService", depth=1, include_body=false)
```

**What you learn:**
- Intent categories Piper handles
- How natural language routes to actions
- System capabilities overview

**Sample output:**
```
25 methods found:
- 8 intent handlers (_handle_*_intent)
- 13 canonical handlers (specific operations)
- 4 utility methods
```

### 2. What Integrations Exist? (Plugins)

**Query:**
```
mcp__serena__list_dir("services/integrations", recursive=false)
```

**What you learn:**
- Available integrations
- Plugin names and structure
- System extension points

**Sample output:**
```
7 directories:
slack, github, notion, calendar, demo, mcp, spatial
```

### 3. What Patterns Are Documented? (Architecture)

**Query:**
```
mcp__serena__list_dir("docs/internal/architecture/current/patterns", recursive=false)
```

**What you learn:**
- Architecture pattern count
- Pattern organization
- Design decision documentation

**Sample output:**
```
33 pattern files (pattern-000 through pattern-033)
Plus README.md and archive/
```

---

## Common Chat Advisor Scenarios

### Scenario 1: User Asks "What can Piper do?"

**Bad approach:** Read full CURRENT-STATE.md (~1,034 tokens)

**Good approach:** Run Intent query (~50 tokens)
```
Let me check Piper's current capabilities:
mcp__serena__find_symbol("IntentService", depth=1, include_body=false)

Based on the results, Piper can handle 8 intent categories:
- Conversation, Query, Execution, Analysis
- Synthesis, Strategy, Learning, Unknown

Plus 13 canonical handlers for specific operations like
standup queries, project queries, GitHub issue creation, etc.
```

### Scenario 2: User Asks "Does Piper integrate with X?"

**Good approach:** Run Plugin query (~30 tokens)
```
Let me check available integrations:
mcp__serena__list_dir("services/integrations", recursive=false)

Current integrations:
- Slack ✅
- GitHub ✅
- Notion ✅
- Calendar ✅
- Demo (template for new integrations)
```

### Scenario 3: User Asks About Architecture

**Good approach:** Combine Pattern query with specific lookup
```
Piper has 33 documented architecture patterns.
Let me find the relevant one...

mcp__serena__search_for_pattern("pattern.*plugin", relative_path="docs/internal/architecture/current/patterns")
```

---

## Building Complete Briefings

**For comprehensive project overview:**

```markdown
# Piper Morgan Current State

**Generated:** {timestamp} via Serena symbolic queries

## System Capabilities
[Results from Intent query]

## Active Integrations
[Results from Plugin query]

## Architecture
[Results from Pattern query]

## Methodology
[Static content from BRIEFING-METHODOLOGY.md]
```

**Token usage:** ~400 tokens (vs ~2,000 for multiple static files)

---

## Troubleshooting

### "I don't see mcp__serena__* tools"

**Check:**
1. Is Serena MCP server connected to Claude Desktop?
2. Check Settings → MCP Servers → Look for "serena"
3. If not connected, ask PM for connection details

**Fallback:**
- Use static knowledge base files
- Ask PM for latest system state
- Reference experiment results in `/dev/active/tooling/`

### "Query returned unexpected format"

**Common issues:**
- Wrong parameter (check `relative_path` accuracy)
- Tool name typo (use exact: `mcp__serena__find_symbol`)
- Missing required parameter

**Fix:**
- Check `serena-briefing-queries.md` for exact patterns
- Copy-paste query from verified examples
- Test with simple query first (list_dir is easiest)

### "Want more detail than query provides"

**Options:**
1. Add `include_body=true` to see implementation
2. Use `search_for_pattern` for specific content
3. Combine multiple queries for complete picture
4. Fall back to reading specific doc files

---

## Best Practices

### DO ✅

- **Use queries for current state** (counts, lists, structure)
- **Combine with static docs** for methodology/philosophy
- **Re-run queries** when you need fresh information
- **Save token budget** by querying instead of reading
- **Verify assumptions** with actual code structure

### DON'T ❌

- **Don't query for narrative** (use static docs)
- **Don't query for history** (use git/docs)
- **Don't query for methodology** (use BRIEFING-METHODOLOGY.md)
- **Don't assume query results** (always check output)
- **Don't over-query** (cache results in conversation)

---

## Integration with Existing Workflow

**Morning standup prep:**
1. Run 3 essential queries
2. Get current system state (~212 tokens)
3. Combine with yesterday's progress
4. Ready for discussion

**New feature planning:**
1. Query relevant subsystem (Intent/Plugins/Patterns)
2. Understand current implementation
3. Design extends (not conflicts with) existing
4. Reference patterns for guidance

**Bug investigation:**
1. Query affected component structure
2. Find relevant handlers/methods
3. Check for similar patterns
4. Use actual code structure for debugging

---

## Query Cheat Sheet

```bash
# Intent categories
mcp__serena__find_symbol("IntentService", depth=1, include_body=false)

# Plugin list
mcp__serena__list_dir("services/integrations", recursive=false)

# Pattern count
mcp__serena__list_dir("docs/internal/architecture/current/patterns", recursive=false)

# Specific pattern search
mcp__serena__search_for_pattern("pattern-name", relative_path="docs/internal/architecture/current/patterns")

# Find plugin implementation
mcp__serena__search_for_pattern("class.*Plugin", relative_path="services/plugins")

# Get method details
mcp__serena__find_symbol("ClassName/method_name", include_body=true)
```

---

## References

- **Query Patterns:** `serena-briefing-queries.md`
- **Experiment Results:** `/dev/active/tooling/briefing-experiment-results.md`
- **CLAUDE.md:** Main agent briefing with Serena section
- **CURRENT-STATE.md:** Fallback if Serena unavailable

---

**Created:** 2025-10-10 (Phase 2 revised)
**For:** Claude Desktop chat advisors
**Status:** Production-ready
**Token Savings:** 79% verified
