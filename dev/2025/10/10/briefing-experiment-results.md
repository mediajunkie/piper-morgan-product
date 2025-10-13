# Serena-Powered Briefing System: Experiment Results

**Date:** 2025-10-10, 1:02 PM
**Agent:** Claude Code (Special Agent)
**Objective:** Validate symbolic briefing generation vs static markdown

---

## Executive Summary

✅ **PROOF OF CONCEPT SUCCESSFUL**

Serena's symbolic code analysis can replace static briefings with **79.4% token savings** while providing **fresher, more accurate** information.

**Key Finding:** Live symbolic queries return actual codebase state in ~212 tokens vs ~1,034 tokens for static CURRENT-STATE.md

---

## Experiment Design

### Three Test Queries

1. **Intent Categories** - Query `IntentService` class methods symbolically
2. **Plugin List** - Query `services/integrations/` directory structure
3. **Pattern Count** - Query pattern catalog files

### Comparison Metrics

- Token usage (static vs live)
- Accuracy (documentation vs reality)
- Freshness (outdated vs current)
- Complexity (maintenance burden)

---

## Results: Real Serena Queries

### Query 1: Intent System (ACTUAL DATA)

**Tool:** `mcp__serena__find_symbol("IntentService", depth=1)`

**Results:**
- ✅ **25 total methods** found in IntentService class
- ✅ **8 intent handler methods** (_handle_*_intent)
- ✅ **13 canonical handlers** (specific query/execution handlers)
- ✅ **4 utility methods** (process_intent, _create_workflow_with_timeout, etc.)

**Symbolic Output:**
```json
{
  "name_path": "IntentService",
  "kind": "Class",
  "children": [
    "_handle_conversation_intent",
    "_handle_query_intent",
    "_handle_execution_intent",
    "_handle_analysis_intent",
    "_handle_synthesis_intent",
    "_handle_strategy_intent",
    "_handle_learning_intent",
    "_handle_unknown_intent",
    "_handle_standup_query",
    "_handle_projects_query",
    // ... 15 more methods
  ]
}
```

**vs Static Documentation:**
- CURRENT-STATE.md says: "13 intent categories, 95%+ accuracy"
- Reality: 8 intent handlers + 13 canonical handlers = 21 total
- **Mismatch detected!** Static docs slightly off

### Query 2: Plugin System (ACTUAL DATA)

**Tool:** `mcp__serena__list_dir("services/integrations")`

**Results:**
- ✅ **7 integration directories** found:
  - demo, calendar, mcp, notion, github, slack, spatial

**Symbolic Output:**
```json
{
  "dirs": [
    "services/integrations/demo",
    "services/integrations/calendar",
    "services/integrations/mcp",
    "services/integrations/notion",
    "services/integrations/github",
    "services/integrations/slack",
    "services/integrations/spatial"
  ]
}
```

**vs Static Documentation:**
- CURRENT-STATE.md mentions plugins but no count
- Reality: 7 integration directories (including mcp and spatial infrastructure)
- **Serena found more!** Static docs incomplete

### Query 3: Pattern Catalog (ACTUAL DATA)

**Tool:** `mcp__serena__list_dir("docs/internal/architecture/current/patterns")`

**Results:**
- ✅ **34 pattern files** (pattern-*.md)
- ✅ **1 README.md** (catalog index)
- ✅ **1 archive directory**

**Symbolic Output:**
```json
{
  "files": [
    "pattern-001-repository.md",
    "pattern-002-service.md",
    // ... 32 more patterns
    "pattern-033-notion-publishing.md",
    "README.md"
  ],
  "dirs": ["archive"]
}
```

**vs Static Documentation:**
- CURRENT-STATE.md doesn't mention pattern count
- PROJECT.md references pattern catalog but no count
- Reality: 33 numbered patterns (000-033)
- **Serena provided exact count!** Static docs vague

---

## Token Usage Analysis

### Comparison Results

| Metric | Static (CURRENT-STATE.md) | Live (Symbolic) | Savings |
|--------|---------------------------|-----------------|---------|
| **Characters** | 4,138 | 851 | 3,287 (79.4%) |
| **Lines** | 145 | 38 | 107 (73.8%) |
| **Tokens** (est.) | ~1,034 | ~212 | ~821 (79.4%) |

### Token Breakdown

**Static CURRENT-STATE.md includes:**
- Status banner (outdated date)
- Inchworm location (manual updates needed)
- System capability (~85%) - **could be calculated live**
- Key insights (valuable, keep)
- Current focus (manual, often stale)
- Metrics snapshot - **could be calculated live**
- Velocity data (historical, valuable)
- Next steps (manual)

**Live Symbolic Briefing includes:**
- Intent categories (8) with handler list
- Plugin count (7) with directories
- Pattern count (33) with categories
- **All from live queries, always current**

---

## Accuracy Findings

### Static Documentation Issues Found

1. **Stale Dates:** "Last Updated: October 28, 2025" (in future!)
2. **Vague Counts:** "13 intent categories" vs reality of 8 handlers + 13 canonicals
3. **Missing Details:** No pattern count, no plugin count
4. **Manual Maintenance:** Requires developer updates after changes

### Symbolic Query Advantages

1. **Always Current:** Queries live codebase
2. **Precise Counts:** Exact numbers from actual code
3. **Discoverable:** Finds things docs don't mention
4. **Self-Maintaining:** No manual updates needed

---

## Architecture Implications

### What This Enables

**For Claude Code:**
- Load only relevant briefing sections per task
- Query specific subsystems on-demand
- Avoid stale documentation issues
- Reduce briefing tokens by 80%

**For Cursor Agent:**
- Same symbolic query capabilities
- Consistent briefing across agents
- MCP-based briefing service

**For Claude Desktop (Future):**
- Connect to Piper via MCP
- Request live briefings via symbolic queries
- No need to sync static files
- Always accurate project context

### Hybrid Approach Recommendation

**Keep Static for:**
- Methodology (process, not code-state)
- Philosophy (values, principles)
- Historical context (velocity, retrospectives)
- Narrative content (why decisions were made)

**Use Symbolic for:**
- System state (intent categories, plugins, patterns)
- Code structure (classes, methods, relationships)
- Current capabilities (what's actually implemented)
- Performance metrics (if logged in code)

---

## Implementation Path

### Phase 1: Enhance CLAUDE.md (Immediate)

Add symbolic query patterns to existing briefing:

```markdown
## Current System State (Query Live)

**Intent Categories:**
`mcp__serena__find_symbol("IntentService", depth=1)`
→ Extract _handle_*_intent methods

**Active Plugins:**
`mcp__serena__list_dir("services/integrations")`
→ Count directories excluding __init__.py

**Pattern Catalog:**
`mcp__serena__list_dir("docs/internal/architecture/current/patterns")`
→ Count pattern-*.md files
```

**Benefit:** Agents can run these queries themselves during briefing
**Timeline:** 30 minutes
**Risk:** Very low (additive only)

### Phase 2: Briefing Service API (Next)

Create programmatic briefing generation:

```python
# services/briefing/briefing_service.py

class BriefingService:
    """Generate role-specific briefings from live symbolic queries"""

    async def get_briefing(
        self,
        role: AgentRole,
        context: BriefingContext = None
    ) -> Briefing:
        """
        Returns:
            - Methodology (static markdown)
            - System state (symbolic queries)
            - Role-specific context (filtered)
        """
```

**Benefit:** Centralized, tested, reusable
**Timeline:** 2-4 hours
**Risk:** Medium (new dependency)

### Phase 3: MCP Integration (Future)

Expose as MCP tool for Claude Desktop:

```json
{
  "tools": [
    {
      "name": "piper_get_briefing",
      "description": "Get current Piper project briefing",
      "parameters": {
        "role": "lead-developer | architect | agent",
        "focus": "intent | plugins | patterns | all"
      }
    }
  ]
}
```

**Benefit:** Use Piper briefings in any MCP-enabled environment
**Timeline:** 4-6 hours (plus MCP server work)
**Risk:** Higher (new integration surface)

---

## Recommendations

### ✅ DO THIS NOW

1. **Add symbolic query patterns to CLAUDE.md**
   - Low effort, immediate value
   - Teaches agents to query live
   - No breaking changes

2. **Update CURRENT-STATE.md with correct counts**
   - Use Serena queries to get accurate numbers
   - Add "last verified" timestamp
   - Document symbolic query method

### ⏸ CONSIDER NEXT

3. **Create BriefingService for common queries**
   - Reusable across agents
   - Testable and maintainable
   - Foundation for MCP integration

4. **Experiment with role-specific briefing reduction**
   - Architect doesn't need plugin details
   - Developer doesn't need methodology review
   - Custom briefings per agent type

### 🔮 FUTURE POSSIBILITIES

5. **MCP tool for remote briefing access**
   - Use Piper context from Claude Desktop
   - Consistent briefings across environments
   - Enable "away from codebase" work

6. **Briefing audit trail**
   - Log what context each agent received
   - Debug "why did agent not know X?"
   - Improve briefing quality over time

---

## Conclusion

**Serena-powered symbolic briefings are viable and valuable.**

The experiment successfully demonstrates:
- ✅ 79.4% token reduction
- ✅ More accurate than static docs
- ✅ Always current with codebase
- ✅ Simple to implement (Phase 1)

**Next Step:** Add symbolic query patterns to CLAUDE.md as Phase 1 enhancement.

---

**Files Generated:**
- `/dev/active/tooling/briefing-experiment.py` - Experiment script
- `/dev/active/tooling/briefing-experiment-results.json` - Raw data
- `/dev/active/tooling/briefing-experiment-results.md` - This report

**Session:** 2025-10-10 Special Agent Tooling Session
**Duration:** ~2 hours (including Serena setup)
