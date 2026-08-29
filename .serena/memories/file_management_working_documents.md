# File Management: Working Documents and Institutional Memory

## Core Principle

**ALL working documents belong in permanent locations, NEVER in `/tmp/`**

The project's documentation archives represent the "conversational architecture" - they preserve not just final outputs but the thinking process, exploration, and decision-making that led to solutions.

## File Location Standards

### Session Logs
**Location**: `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-role-model-log.md`
**Format**: See CLAUDE.md for naming convention
**Purpose**: Complete chronological record of agent work
**Example**: `dev/2025/11/03/2025-11-03-0615-prog-code-log.md`

### Working Documents (Active)
**Location**: `dev/active/`
**Contents**:
- Agent prompts and briefings
- Issue updates and validation reports
- Gameplans and specifications
- Follow-up issue drafts
- Analysis reports
- Any document being actively worked on

**Examples**:
- `dev/active/issue-284-validation-update.md`
- `dev/active/follow-up-actionmapper-scope-docs.md`
- `dev/active/gameplan-a8-phase3-p1-issues.md`

### Working Documents (Dated)
**Location**: `dev/YYYY/MM/DD/`
**When**: Alternative to `dev/active/` for time-specific context
**Use**: Documents that belong to a specific session/date
**Examples**:
- Investigation reports from specific dates
- Session-specific analysis files
- Temporary working files for that day's work

### Completed/Archived Documents
**Location**: Various permanent locations
- `docs/internal/architecture/adrs/` - Architecture Decision Records
- `docs/internal/architecture/patterns/` - Pattern documentation
- `docs/internal/development/` - Methodology and process docs
- Dated directories for historical reference

## Why This Matters

### The Documentation Archive Philosophy

**Quote from PM**: "The institutional memory of our methodology is enriched by full access to all working files, hence our voluminous doc archives, as big as the codebase itself (they represent the conversational architecture, so to speak)."

**Key Insights**:
1. **Documentation = Conversational Architecture**: Working files show HOW we think, not just WHAT we decided
2. **Institutional Memory**: Future agents need full context from past sessions
3. **Knowledge Preservation**: Temporary files lose valuable context
4. **Process Transparency**: The journey matters as much as the destination

### Size Matters (In a Good Way)
- Documentation archives are as big as the codebase itself
- This is INTENTIONAL and VALUED
- Shows deep thinking and thorough exploration
- Enables future agents to understand WHY decisions were made

## Common Mistakes to Avoid

### ❌ WRONG: Using /tmp/ for Working Files
```bash
# BAD - Suggests ephemeral, disposable
cat > /tmp/issue-update.md << EOF
...
EOF
```

**Why wrong**:
- `/tmp/` suggests files are okay to delete
- Loses institutional memory
- Future agents can't access the context
- Breaks the conversational architecture

### ✅ RIGHT: Using dev/active/ or Dated Directories
```bash
# GOOD - Permanent, archival, accessible
cat > dev/active/issue-284-validation-update.md << EOF
...
EOF

# ALSO GOOD - Date-specific context
cat > dev/2025/11/03/investigation-results.md << EOF
...
EOF
```

## File Types That Need Permanent Locations

ALL of these belong in `dev/active/` or dated directories:

1. **Investigation Reports**: Findings from code archaeology
2. **Validation Reports**: Test results and verification matrices
3. **Issue Updates**: Text to paste into GitHub issues
4. **Follow-up Specs**: New issue specifications
5. **Analysis Documents**: Code analysis, pattern discovery
6. **Planning Documents**: Gameplans, roadmaps, specifications
7. **Agent Prompts**: Briefings for specialized agents
8. **Session Artifacts**: Any file created during a session

**Rule of Thumb**: If you created it during work, it belongs in permanent storage.

## Workflow

### Starting Work
1. Create session log in `dev/YYYY/MM/DD/`
2. Create/update working documents in `dev/active/`
3. Reference existing documents from archives as needed

### During Work
1. All scratch files → `dev/active/` (NOT `/tmp/`)
2. Update session log continuously
3. Keep working documents visible in `dev/active/`

### Ending Work
1. Ensure all files in permanent locations
2. Update session log with final status
3. Consider if any `dev/active/` files should move to archives
4. NEVER leave important files in `/tmp/`

## Cultural Context

This is part of Piper Morgan's **documentation-first culture**:
- Every decision is documented
- Every investigation leaves artifacts
- Every session creates institutional memory
- The archive IS the knowledge base

**Philosophy**: "We're not just building software, we're building the conversational architecture that explains how and why we built it."

## Historical Context

**Discovered**: 2025-11-03 during Issue #284/#285 validation
**Root Cause**: Agent defaulted to `/tmp/` as programming convention
**Learning**: Project values ALL working documents as institutional memory
**Correction**: Moved all files to `dev/active/`, formalized principle

## Related Documentation

- `CLAUDE.md` - Agent briefing (session log location specified)
- `docs/NAVIGATION.md` - How to find things in the archive
- File organization conventions throughout `docs/` and `dev/`

## Questions for Agents

Before creating ANY file, ask yourself:

1. **Is this file part of our work?** → Permanent location
2. **Will future agents benefit from seeing this?** → Permanent location
3. **Does this show our thinking process?** → Permanent location
4. **Is this truly disposable?** → Probably still permanent location

**When in doubt**: Use `dev/active/` or dated directory. Storage is cheap, lost context is expensive.

---

**Remember**: Our documentation archives are the conversational architecture. Preserve everything.
