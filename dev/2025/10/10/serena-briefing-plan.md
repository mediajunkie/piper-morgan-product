# Plan: Serena-Powered Contextual Briefing System

## Current State Analysis

### What You Have Now:
1. Static Markdown Briefings (docs/briefing/.md, knowledge/.md)
    - CURRENT-STATE.md (~145 lines)
    - PROJECT.md (~165 lines)
    - METHODOLOGY.md (~446 lines)
    - Role-specific BRIEFING-ESSENTIAL-*.md files
2. Serena Memory System (9 existing memories)
    - project_overview, project_structure, tech_stack, code_style_conventions
    - System automatically indexes code structure symbolically
3. CLAUDE.md Progressive Loading Pattern
    - Role-based briefings (60% token reduction)
    - Load-on-demand architecture

### The Opportunity

Serena's Symbolic Capabilities Can:
1. Query codebase symbolically instead of reading full files
    - "Show me all IntentService methods" → 25 methods instantly
    - "Find all PiperPlugin implementations" → Every integration
    - "What patterns exist in services/?" → Symbolic overview
2. Generate briefings on-demand from live code state
    - Current intent categories (by querying IntentService)
    - Available plugins (by querying PluginRegistry)
    - Architecture state (by symbol analysis)
     - Recent changes (by git + symbolic diff)
3. Context-aware memory retrieval
     - Query memories based on agent's current task
     - Build briefing from relevant memories only
     - Keep briefings fresh with codebase reality

## Proposed Approach

### Phase 1: Hybrid Briefing System (Quick Win)

**Goal: Augment static briefings with live symbolic queries**

Implementation:
1. Create briefing builder functions that use Serena:
     # services/briefing/symbolic_briefing.py

     def get_current_intent_categories() -> List[str]:
         """Query IntentService symbolically for actual categories"""
         
     def get_active_plugins() -> Dict[str, PluginMetadata]:
         """Query PluginRegistry for live plugin state"""
         
     def get_pattern_catalog() -> Dict[str, str]:
         """Query patterns directory symbolically"""
     2. Enhance CLAUDE.md with Serena hooks:
     ## Current System State (Live)

To get up-to-date system state, use Serena:
     - Intent categories: `mcp__serena__find_symbol("IntentService", depth=1)`
     - Active plugins: `mcp__serena__search_for_pattern("class.*Plugin")`
     - Recent changes: Check git log + symbolic diff on changed files
     3. Add memory indexing patterns for briefing domains:
       - Architecture decisions → Query ADRs symbolically
       - Current status → Generate from git + symbolic analysis
       - Methodology → Keep as markdown (process, not code)

#### Phase 2: Programmatic Briefing API (Future)

**Goal: Generate role-specific briefings on-demand via API**

 Structure:
     # services/briefing/briefing_service.py

     class BriefingService:
         def __init__(self, serena_tools):
             self.serena = serena_tools
             
         async def generate_briefing(
             self, 
             role: AgentRole,
             context: BriefingContext
         ) -> Briefing:
             """
             Generate role-specific briefing combining:
             - Static methodology (from markdown)
             - Live code state (from Serena queries)
             - Relevant memories (from Serena memory system)
             - Recent activity (from git + symbolic diff)
             """
             
         def _get_architect_context(self) -> Dict:
             """Symbolic queries for architecture decisions"""
             
         def _get_developer_context(self) -> Dict:
             """Symbolic queries for implementation patterns"""

### Phase 3: Claude Desktop Integration (Experimental)

**Goal: Use briefing API via MCP from Claude Desktop chat**

 Flow:
 1. Start Claude Desktop chat (away from codebase)
 2. Connect to Piper MCP server
 3. Request briefing: "Give me lead developer context"
 4. MCP calls BriefingService which uses Serena
 5. Receive programmatically-generated briefing

 Benefits:
 - Same briefing system for all agents
 - Always fresh (generated from live codebase)
 - Token-efficient (only relevant context)
 - Auditable (can log what context was provided)

## Key Decisions to Make

1. Scope: Start with Phase 1 (hybrid) or go straight to Phase 2 (API)?
2. Storage: Keep methodology in markdown vs. move to structured data?
3. Caching: How often to regenerate symbolic briefings?
4. Interface: Expose as MCP tools, Python API, or both?
5. Migration: Gradually replace static files or keep hybrid long-term?

## Recommended Starting Point

Quick Experiment (1-2 hours):
1. Create /dev/active/tooling/briefing-experiment.py
2. Write 3 symbolic query functions:
    - get_intent_categories_live()
    - get_plugin_list_live()
    - get_pattern_count_live()
3. Compare output to static CURRENT-STATE.md
4. Measure token usage difference
5. Decide if full implementation is worthwhile

## Why This Approach:
 - Low risk (doesn't change existing briefings)
 - Fast feedback (know if concept works)
 - Real data (actual token/quality comparison)
 - Reversible (just delete experiment file)

## Potential Benefits

 ✅ Token Efficiency: Only load what agent needs for their role
 ✅ Always Current: No stale documentation issues
 ✅ Audit Trail: Know exactly what context each agent received
 ✅ Consistency: Same briefing system across all agents
 ✅ Scalability: As codebase grows, briefings stay focused

## Potential Challenges

 ⚠️ Complexity: More moving parts than static markdown
 ⚠️ Dependencies: Requires Serena availability
 ⚠️ Learning Curve: Agents need to understand symbolic queries
 ⚠️ Debugging: Harder to inspect what context was provided
 ⚠️ Maintenance: Need to update query logic as code evolves

---
This is a research/experiment plan. No code changes until you approve the direction.
