# Serena Symbolic Briefing Queries

**Purpose:** Reusable Serena query patterns for getting fresh, accurate Piper Morgan project context

**Audience:** All agents (Claude Code, Cursor, Claude Desktop chat advisors)

**Token Savings:** 79% vs reading static documentation

**Last Updated:** 2025-10-10

---

## Quick Reference

Use these symbolic queries instead of reading static docs like CURRENT-STATE.md

**Benefits:**
- ✅ Always current (queries live codebase)
- ✅ 79% token savings (~212 vs ~1,034 tokens)
- ✅ Precise counts (not estimates)
- ✅ Verifiable (re-run anytime)

---

## Query 1: Intent Classification System

**What it tells you:** How Piper routes natural language to actions

**Serena Query:**
```
mcp__serena__find_symbol("IntentService", depth=1, include_body=false, relative_path="services/intent/intent_service.py")
```

**Returns:**
- All IntentService methods (25 total as of 2025-10-10)
- Intent handlers: Methods named `_handle_*_intent` (8 categories)
- Canonical handlers: Methods for specific operations (13 handlers)
- Utility methods: Supporting functions

**Extract Intent Categories:**
```python
# From returned children, filter for intent handlers:
intent_handlers = [m for m in methods if "_handle_" in m["name"] and "_intent" in m["name"]]
categories = [h.replace("_handle_", "").replace("_intent", "") for h in intent_handlers]
# Result: ['conversation', 'query', 'execution', 'analysis', 'synthesis', 'strategy', 'learning', 'unknown']
```

**Use When:**
- Understanding what intents Piper can handle
- Adding new intent category
- Debugging intent classification issues

---

## Query 2: Active Plugins

**What it tells you:** Which integrations are available

**Serena Query:**
```
mcp__serena__list_dir("services/integrations", recursive=false)
```

**Returns:**
- Integration directories (7 as of 2025-10-10)
- List: slack, github, notion, calendar, demo, mcp, spatial

**Extract Plugin Names:**
```python
# From returned dirs:
plugins = [d.split("/")[-1] for d in dirs if d.startswith("services/integrations/")]
# Filter out infrastructure:
active_plugins = [p for p in plugins if p not in ["__pycache__", "spatial"]]
# Result: ['slack', 'github', 'notion', 'calendar', 'demo', 'mcp']
```

**Use When:**
- Checking what integrations exist
- Adding new plugin
- Understanding system capabilities

---

## Query 3: Pattern Catalog

**What it tells you:** Documented architecture patterns

**Serena Query:**
```
mcp__serena__list_dir("docs/internal/architecture/current/patterns", recursive=false)
```

**Returns:**
- Pattern files: pattern-NNN-name.md (33 as of 2025-10-10)
- README.md (catalog index)
- archive/ directory

**Extract Pattern Count:**
```python
# From returned files:
patterns = [f for f in files if f.startswith("pattern-") and f.endswith(".md")]
count = len(patterns)
# Result: 33 patterns (pattern-000 through pattern-033)
```

**Use When:**
- Finding relevant patterns
- Checking if pattern exists
- Understanding architecture decisions

---

## Combined Briefing Query

**For a complete system state briefing, run all three queries:**

```python
# 1. Intent System
intent_data = mcp__serena__find_symbol("IntentService", depth=1, include_body=false)

# 2. Plugins
plugin_data = mcp__serena__list_dir("services/integrations", recursive=false)

# 3. Patterns
pattern_data = mcp__serena__list_dir("docs/internal/architecture/current/patterns", recursive=false)

# Generate briefing:
briefing = f"""
## Piper Morgan System State

**Intent Classification:**
- {len([m for m in intent_data if '_intent' in m])} intent categories
- {len(intent_data['children'])} total handlers

**Active Integrations:**
- {len(plugin_data['dirs'])} plugins available

**Architecture Patterns:**
- {len([f for f in pattern_data['files'] if f.startswith('pattern-')])} documented patterns
"""
```

**Token Usage:** ~212 tokens vs ~1,034 for static CURRENT-STATE.md

---

## Advanced Queries

### Get Specific Intent Handler Details

```
mcp__serena__find_symbol("IntentService/_handle_query_intent", include_body=true, relative_path="services/intent/intent_service.py")
```

Returns: Full implementation of query intent handler

### Find All Plugin Classes

```
mcp__serena__search_for_pattern("class.*Plugin", relative_path="services/plugins", restrict_search_to_code_files=true)
```

Returns: All classes ending in "Plugin" (PiperPlugin interface implementations)

### Get Pattern Details

```
# Read specific pattern file
mcp__serena__search_for_pattern("^# ", relative_path="docs/internal/architecture/current/patterns/pattern-030-plugin-interface.md")
```

Returns: Pattern headings and structure

---

## For Claude Desktop Users

**If you don't have Serena MCP server connected:**

1. Ask PM to share latest system state
2. Reference CLAUDE.md "Live System State" section
3. Use static CURRENT-STATE.md as fallback

**If you have Serena connected:**

Use the queries above directly in your chat. Example:

```
Please run this Serena query to get current intent categories:
mcp__serena__find_symbol("IntentService", depth=1, include_body=false)
```

---

## Query Pattern Template

**For creating new queries:**

```
# What you want to know: [describe]
# Why: [use case]

mcp__serena__[tool_name]([parameters])

# Expected output:
# - [what it returns]
# - [how to interpret]

# Example result:
# [paste actual output]
```

---

## Maintenance

**These queries are self-maintaining:**
- No updates needed when code changes
- Always return current codebase state
- Verified accurate as of query execution

**If query pattern changes:**
- Update this file with new pattern
- Test with actual Serena call
- Document expected output

---

## References

- **Experiment Results:** `/dev/active/tooling/briefing-experiment-results.md`
- **CLAUDE.md Section:** "Live System State (Query with Serena)"
- **CURRENT-STATE.md:** Fallback if Serena unavailable

---

**Created:** 2025-10-10 (Phase 1 implementation)
**Token Savings Validated:** 79.4% reduction vs static docs
**Status:** Production-ready, tested with real queries
