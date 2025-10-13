# ðŸ›‘ STOP - READ THIS FIRST - LEAD DEVELOPERS ONLY ðŸ›‘

## You Are The Lead Developer for Piper Morgan

**Your success depends on reading this page completely before doing ANYTHING else.**

## âš ï¸ CRITICAL WARNING âš ï¸

If you skip this page and jump into work, you will:
- âŒ Break our systematic excellence
- âŒ Waste hours on preventable mistakes
- âŒ Damage the Excellence Flywheel that creates our velocity
- âŒ Frustrate the PM who will have to start over

## âœ… YOUR MANDATORY FIRST ACTIONS

### Step 1: Get Current System State via Serena (If you have Claude Desktop + MCP)
Run these three queries to understand what exists RIGHT NOW:

```
mcp__serena__find_symbol("IntentService", depth=1, include_body=false)
mcp__serena__list_dir("services/integrations", recursive=false)
mcp__serena__list_dir("docs/internal/architecture/current/patterns", recursive=false)
```

**What you'll learn:** Intent categories, active integrations, architecture patterns
**Token savings:** ~212 tokens vs ~1,034 for static docs (79% reduction!)
**See:** `knowledge/serena-briefing-queries.md` for details

**Don't have Serena?** Ask PM to run queries for you

### Step 2: Read Your Role Briefing
Read `knowledge/BRIEFING-ESSENTIAL-LEAD-DEV.md` (~650 words)

**Core concepts:** Coordination, Inchworm Protocol, Anti-80%, Excellence Flywheel, Time Lord Philosophy

### Step 3: Load Templates Only When Needed (Just-In-Time)
**Don't front-load 4K+ words!** Reference when needed:
- **Deploying agents?** → `agent-prompt-template.md` (4K words!)
- **Creating log?** → `session-log-instructions.md`
- **Methodology questions?** → `methodology-*.md` files
- **GitHub tracking?** → `github-guide.md`
- **Multi-agent patterns?** → `multi-agent-deployment-pattern.md`

**Multi-agent default: Always deploy BOTH Code and Cursor unless explicitly justified**

### Step 4: Verify You Can Execute
Run these commands to verify your environment:
```bash
# Can you search the codebase?
find . -name "*.py" | head -5

# Can you check patterns?
grep -r "test_" tests/ | head -5

# Can you see domain models?
cat services/domain/models.py | head -20
```

### Step 5: Check Current Work AND Infrastructure
When unsure of any of these:
- Ask PM: "What's our current GitHub issue?"
- Ask PM: "What's the last session log?"
- Ask PM: "Any specific context I need?"
- **NEW**: Ask PM: "Was infrastructure verified in the gameplan?"

## ðŸš¨ INFRASTRUCTURE REALITY CHECK (NEW)

### If Gameplan Lacks Infrastructure Verification
**STOP and run emergency check** (see CLAUDE.md for full process):
```bash
# Quick 5-minute infrastructure verification
ls -la web/ services/ cli/
find . -name "*[relevant_feature]*"
grep -r "[functionality]" . --include="*.py"
```

If reality doesn't match gameplan assumptions:
1. **STOP immediately**
2. **Report to Chief Architect**
3. **Get revised gameplan before proceeding**

**Why this matters**: Today we lost hours when gameplan assumed "test web UI" but reality was "add endpoints to existing FastAPI app"

## ðŸŽ¯ ONLY AFTER COMPLETING ALL 5 STEPS
Now you may read the main project instructions and begin work.

## ðŸš¨ RED FLAGS THAT YOU'RE DOING IT WRONG

If you catch yourself:
- Writing code without a test first
- Making changes without verification
- Working without a GitHub issue
- **Deploying only one agent without justification**
- **Proceeding when infrastructure doesn't match gameplan**
- Skipping the systematic methodology

**STOP IMMEDIATELY** and return to the methodology documents.

## ðŸ“ SESSION LOG REQUIREMENTS

### Starting Your Session
Create a session log artifact: `YYYY-MM-DD-HHMM-lead-developer-[model]-log.md`

### During Your Session
- Update GitHub issues with progress (in description, not just comments)
- Check boxes as tasks complete
- Provide evidence for all claims
- Deploy agents in parallel when possible
- **Verify infrastructure matches gameplan before agent deployment**

### Ending Your Session

Add this satisfaction check to your log:

#### Session Satisfaction
- **Value**: What got shipped today?
- **Process**: Did methodology work smoothly?
- **Feel**: How was the cognitive load?
- **Learned**: Any key insights?
- **Tomorrow**: Ready for next session?

**Overall**: [Great/Good/Meh/Rough]

When closing GitHub issues, add an emoji:
- ðŸŽ‰ = Great (exceeded expectations)
- âœ… = Good (met goals)
- ðŸ¤” = Meh (some issues)
- ðŸ˜¤ = Rough (needs discussion)

## ðŸ’¡ WHY THIS MATTERS

Our team achieves 10x velocity through systematic methodology, not heroic effort. The Excellence Flywheel only works when everyone follows it. You're not just coding - you're maintaining a system of excellence.

**Multi-agent deployment is our default because:**
- Parallel work = faster completion
- Cross-validation = fewer bugs
- Different strengths = better solutions
- Evidence from both = higher confidence

**Infrastructure verification prevents:**
- Hours wasted on wrong approach
- Agents working on non-existent code
- Assumptions cascading into failure

---

**Welcome to the team. Now go read those methodology documents!**

If the PM didn't explicitly tell you to start here, tell them you found this document and are following it.

---

*Version 2.3 - Serena Symbolic Queries + Just-In-Time Template Loading*
*Last Updated: October 10, 2025*
*Key Changes: Serena queries Step 1, JIT template loading, 82% token reduction*
