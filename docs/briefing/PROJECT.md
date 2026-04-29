# PROJECT.md - Piper Morgan Development

## Repository Information

**CRITICAL**: Always use the correct repository URL:
- **GitHub Repository**: `https://github.com/mediajunkie/piper-morgan-product`
- **Local Directory Name**: `piper-morgan` (legacy naming, but repo is `piper-morgan-product`)
- **NEVER use**: `Codewarrior1988/piper-morgan` (this is a hallucinated URL that has infected docs)

**Branch Discipline**:
- **`main`**: Active development. Agents work here or on feature branches/worktrees (`claude/*`).
- **`production`**: Released builds only. Alpha testers pull from this branch.
- Releases are tagged on `main` and pushed to `production`. No post-tag work lands on `production`.
- Upgrade instructions in release notes should reference `production`, not `main`.

## Vision

Piper Morgan is an intelligent PM assistant that transforms how product managers work with AI agents. By combining spatial intelligence, domain-driven design, and systematic orchestration, Piper becomes a true thought partner who learns and adapts to each PM's unique style and needs.

We're building this with a revolutionary approach: one human PM collaborating with AI agents as the entire development team. This isn't just about building a product - it's about discovering new methods for human-AI excellence.

## Current State

> **📊 For current sprint/epic position and version, always see `docs/briefing/BRIEFING-CURRENT-STATE.md`**
>
> This document describes the project's stable context (vision, architecture, methodology).
> Current state changes frequently - check BRIEFING-CURRENT-STATE.md for the latest.

We follow the Inchworm Protocol: complete each piece 100% before moving forward. No exceptions. The 75% Pattern (components abandoned before completion) is our primary anti-pattern to prevent.

## Technical Foundation

**Core Stack**:

- Python 3.11+ with AsyncIO
- FastAPI for web framework
- PostgreSQL with AsyncSession
- Domain-Driven Design architecture

**Key Patterns**:

- Everything through services (no direct DB access)
- Plugin architecture for integrations
- Spatial intelligence (8-dimensional context)
- Intent classification as universal entry
- MCP protocol for agent communication

**File Structure Reality**:

```
main.py             # Primary backend application entry point
web/app.py          # FastAPI web framework (933 lines, refactor at 1000)
services/           # All business logic here
cli/commands/       # Direct command implementations
config/             # PIPER.md and user config
```

## Development Methodology

**Inchworm Protocol** (ADR-035): Sequential completion. Each epic 100% done before next begins.

**Excellence Flywheel** (v2.0): see `docs/internal/development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md` for the canonical three-layer reformulation (Concept / Practice / Mnemonic). The Practice layer's five practices: (1) Verify Before Building, (2) Test What Matters Not What's Easy, (3) Coordinate Through Structure, (4) Track to Completion with Evidence, (5) Audit the Composition. The canonical doc is the source of truth.

**Evidence-Based Progress**: No "done" without proof. Terminal output, test results, working demos.

## Core Systems

> **Note**: For current operational status, see `docs/briefing/BRIEFING-CURRENT-STATE.md`

| System | Location | Purpose |
|--------|----------|---------|
| Intent Classification | `services/intent_service/` | Universal entry point for all requests |
| Integrations | `services/integrations/` | Slack, GitHub, Notion, Calendar, MCP, Spatial |
| Orchestration | `services/orchestration/` | Workflow coordination |
| Learning | `services/learning/` | Preference and pattern learning |
| Knowledge | `services/knowledge/` | RAG system with embeddings |

## Learning Philosophy

Every problem discovered is a gift - we found it now rather than later. We value:

- Diligence over speed
- Completion over features
- Evidence over assumptions
- Learning from every attempt

When something doesn't work as expected, that's exciting - we've learned something new about our system.

## Resources and Navigation

**Navigating Documentation**:
For complete documentation structure, see: **docs/NAVIGATION.md**

**Key Documents**:

- `docs/briefing/BRIEFING-CURRENT-STATE.md` - Current sprint/version/position (check this first!)
- `docs/internal/architecture/current/adrs/` - Architectural Decision Records
- `docs/internal/architecture/current/patterns/` - Pattern Catalog
- `docs/internal/planning/roadmap/` - Current roadmap

**Finding Things**:

```bash
# Find implementation
grep -r "ClassName" . --include="*.py"

# Find patterns
cat docs/internal/architecture/current/patterns/ | grep -A 10 "Pattern Name"

# Check what exists
ls -la services/
ls -la web/
```

## Standards to Maintain

1. **Domain Separation**: Business logic never in controllers
2. **Config Separation**: User config never in system code
3. **Spatial Intelligence**: All plugins must implement
4. **Complete Work**: No TODOs without issue numbers
5. **Evidence Required**: No claims without proof

## Success Indicators

You're succeeding when:

- Your code completes something unfinished
- Your tests lock in that completion
- You find a problem others missed
- You resist adding a workaround
- You take time to do it right

## Remember

"We do these things not because they are easy, but because we thought they would be easy!" 😉

The path is clearer today than it has ever been. We have strong aversion to leaving things unfinished. Every session moves us closer to excellence.

---

_Welcome to the Piper Morgan project. Your contribution matters._

**Document Maintenance**: This document describes stable project context. For current state (version, sprint position, active issues), always check `docs/briefing/BRIEFING-CURRENT-STATE.md`.

*Last Updated: March 14, 2026*
