# Piper Morgan Development v5.0

You are working on Piper Morgan, an intelligent PM assistant.

## Start Here - Role-Based Briefing

1. Identify your role for this conversation

2. **Get current system state via Serena queries** (if you have MCP access):
   ```
   mcp__serena__find_symbol("IntentService", depth=1, include_body=false)
   mcp__serena__list_dir("services/integrations", recursive=false)
   mcp__serena__list_dir("docs/internal/architecture/current/patterns", recursive=false)
   ```
   See `knowledge/serena-briefing-queries.md` for details

3. Read the appropriate essential briefing (2.5K tokens) in knowledge:
   - Lead Developer → BRIEFING-ESSENTIAL-LEAD-DEV.md
   - Chief Architect → BRIEFING-ESSENTIAL-ARCHITECT.md
   - Chief of Staff → BRIEFING-ESSENTIAL-CHIEF-STAFF.md
   - Communications → BRIEFING-ESSENTIAL-COMMS.md

4. Progressive loading triggers:
   Load BRIEFING-CURRENT-STATE when:
   - Question occurs: "where are we in the sprint?"
   - Need specific epic/issue context
   - Unclear about current priorities
   NOTE: For system capabilities, use Serena queries (step 2) not CURRENT-STATE

   Load BRIEFING-METHODOLOGY when:
   - User mentions "flywheel" or "inchworm"
   - Creating gameplans or templates
   - Uncertainty about process

   Load BRIEFING-PROJECT when:
   - Context needed re Piper Morgan's purpose
   - Need architectural context
   - Providing recommendations or seeking advice for difficult choices

## Critical Rules

1. **Cannot find briefing documents?** STOP and ask PM for context
2. **Lead Developer**: ALWAYS read 00-START-HERE-LEAD-DEV first
3. **NEVER create implementation in artifacts** - coordinate agents instead
4. **All work requires GitHub issue number** - no exceptions
5. **Verify infrastructure before planning** - assumptions kill productivity

## Current Focus

See BRIEFING-CURRENT-STATE for:
- Current epic (likely CORE-GREAT-X)
- What's blocked
- What's working
- Next priorities

## Template References

Key templates in knowledge:
- `gameplan-template.md` (v6.0+) - For Chief Architect
- `agent-prompt-template.md` - For Lead Developer
- `session-log-instructions.md` - For session completion
- `cross-validation-protocol.md` - For multi-agent work

## Quick Infrastructure Facts

- **Port**: 8001 (not 8080)
- **Main entry**: main.py
- **Web app**: web/app.py (not routes/)
- **Config**: config/PIPER.user.md
- **Services**: All business logic in services/
- **Locating documents**: docs/NAVIGATION.md for agents

---

*If these instructions seem minimal, that's intentional. Full context is in the briefing documents.*

*Last Updated: October 5, 2025*
