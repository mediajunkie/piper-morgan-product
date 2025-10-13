# Prompt for Code Agent: Stray Issues Investigation

## Context

Two stray issues need verification before continuing CORE epics:
1. **CORE-NOTN-PUBLISH** (#135): Notion publish command
2. **CORE-PLUG-REFACTOR** (#175): GitHub plugin extraction


## Mission

Investigate both issues, verify acceptance criteria against filesystem, and recommend close/complete/new-issue for each.

**Estimated Time**: 30-45 minutes per issue (1-1.5 hours total)

---

## Issue 1: CORE-NOTN-PUBLISH (#135)

### Background
- **GitHub Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/135
- **User report**: `piper publish` command works successfully
- **Concern**: Verify all acceptance criteria, check for refactor regressions
- **Context**: Notion publish functionality may have been affected by Great Refactor

### Acceptance Criteria to Verify

**Implementation Checklist**:
- [ ] TDD test suite with real API validation
- [ ] Markdown converter (headers, paragraphs, simple lists)
- [ ] Publisher service with error handling
- [ ] CLI command interface
- [ ] Integration testing with actual Notion API
- [ ] Documentation updates (patterns, ADRs, command docs)

**Success Criteria**:
- [ ] Can publish markdown file to Notion workspace
- [ ] Creates actual page with correct formatting
- [ ] Returns clickable URL
- [ ] Handles errors gracefully with user feedback
- [ ] All tests pass with REAL API calls (no mocks for core functionality)

### Investigation Tasks

#### 1. Locate Implementation (15 min)

**Find piper publish command**:
```bash
# Search for publish command implementation
find . -name "*.py" -type f | xargs grep -l "def.*publish"
grep -r "publish" cli/commands/ --include="*.py"

# Check CLI structure
ls -la cli/commands/
cat cli/commands/notion.py  # Or wherever publish lives

# Find Notion integration
find services/integrations/ -name "*notion*" -type f
ls -la services/integrations/mcp/
```

**Look for**:
- CLI command entry point
- NotionAdapter or NotionMCPAdapter
- Publisher service
- Markdown converter

#### 2. Verify Test Suite (10 min)

**Find and examine tests**:
```bash
# Find all publish-related tests
find tests/ -name "*publish*" -type f
find tests/ -name "*notion*" -type f

# Check test structure
ls -la tests/publishing/
ls -la tests/integration/

# Examine test content
grep -r "mock" tests/publishing/ tests/integration/
grep -r "NOTION_API_KEY" tests/
grep -r "def test.*publish" tests/ --include="*.py"
```

**Verify**:
- Tests exist for publish functionality
- Tests use real API (minimal mocking)
- Tests validate actual page creation (not just return values)
- Integration tests present

#### 3. Check Markdown Converter (10 min)

**Find converter implementation**:
```bash
# Search for markdown conversion
find . -name "*.py" | xargs grep -l "markdown"
grep -r "class.*Markdown" services/ --include="*.py"
grep -r "def.*convert.*markdown" services/ --include="*.py"
```

**Verify supports**:
- Headers (H1, H2, H3)
- Paragraphs
- Simple lists (ordered and unordered)
- Error handling for unsupported elements

#### 4. Check Documentation (10 min)

**Search for documentation**:
```bash
# Check for patterns
ls -la docs/patterns/
grep -r "publish" docs/patterns/

# Check for ADRs
ls -la docs/adrs/
grep -l "notion.*publish\|publish.*notion" docs/adrs/*.md

# Check for command docs
ls -la docs/commands/
cat docs/commands/publish.md 2>/dev/null || echo "No command doc found"

# Check README
grep -i "publish" README.md
```

**Look for**:
- Pattern documentation
- ADR documenting publish implementation
- Command usage documentation
- Examples

#### 5. Run Tests (Optional, if time permits)

```bash
# Run publish tests
PYTHONPATH=. python -m pytest tests/publishing/ -v

# Run integration tests
PYTHONPATH=. python -m pytest tests/integration/*notion* -v

# Check test coverage
PYTHONPATH=. python -m pytest tests/publishing/ --cov=services --cov-report=term-missing
```

### Decision Matrix

**If all criteria met (including docs)**:
- **Recommendation**: CLOSE issue #135 as complete
- **Evidence**: List all files that satisfy each criterion
- **Action**: Create completion summary in `dev/2025/10/08/core-notn-publish-verification.md`
- **GitHub**: Close issue with reference to verification doc

**If only documentation missing (small gap)**:
- **Gap Size**: Small (30-45 minutes)
- **Recommendation**: Complete documentation now
- **Tasks**:
  1. Create pattern doc: `docs/patterns/notion-publishing.md`
  2. Update/create ADR: `docs/adrs/adr-0XX-notion-publish-command.md`
  3. Create command doc: `docs/commands/publish.md`
- **Action**: Complete docs, then close issue

**If tests broken or functionality regressed (medium gap)**:
- **Gap Size**: Medium (1-3 hours)
- **Recommendation**: Create new GitHub issue
- **Priority**: HIGH (user reported working, but tests failing suggests brittleness)
- **Details**: Document which tests fail, what functionality is broken
- **Action**: Create issue, link to verification doc, prioritize in backlog

**If major functionality missing (large gap)**:
- **Gap Size**: Large (3+ hours)
- **Recommendation**: Re-open issue or create new epic
- **Priority**: Depends on user needs
- **Action**: Document gap, discuss with PM for prioritization

---

## Issue 2: CORE-PLUG-REFACTOR (#175)

### Background
- **GitHub Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/175
- **Parent**: CORE-PLUG-1 (#174) - Superseded by CORE-GREAT-3 (#182)
- **Context**: GREAT-3A completed plugin foundation with 4 operational plugins
- **Concern**: Should have been superseded during Great Refactor, need to verify

### Acceptance Criteria to Verify

**Implementation Tasks**:
- [ ] Extract GitHub code from monolith
- [ ] Implement plugin interface
- [ ] Preserve spatial intelligence patterns
- [ ] Create plugin manifest and metadata
- [ ] Update all service calls to use plugin
- [ ] Migration script for existing data
- [ ] Rollback plan documented

**Validation Requirements**:
- [ ] All existing GitHub functionality works identically
- [ ] Performance meets or exceeds current (<50ms overhead)
- [ ] Spatial patterns properly utilized
- [ ] Clean plugin boundaries (no monolith dependencies)
- [ ] All tests pass
- [ ] Can disable/enable plugin without system impact

### Investigation Tasks

#### 1. Check GREAT-3A Completion Status (10 min)

**Find GREAT-3A documentation**:
```bash
# Look for GREAT-3A completion docs
find dev/2025/10/ -name "*great3*" -o -name "*GREAT-3*"
ls -la dev/2025/10/*/

# Check for completion summary
cat dev/2025/10/*/great3a-completion*.md 2>/dev/null
grep -l "GREAT-3A" dev/2025/10/*/*.md
```

**Review**:
- What was delivered in GREAT-3A
- Plugin architecture status
- Which plugins were created
- GitHub plugin status

#### 2. Verify Plugin Architecture (15 min)

**Check plugin infrastructure**:
```bash
# Find plugin system files
ls -la services/plugins/
tree services/plugins/ -L 2

# Check core plugin files
cat services/plugins/interface.py | head -50
cat services/plugins/registry.py | head -50
cat services/plugins/__init__.py

# Check plugin wrapper pattern
ls -la services/plugins/wrappers/
```

**Verify**:
- Plugin interface exists
- Plugin registry operational
- Wrapper pattern implemented

#### 3. Verify GitHub Plugin (15 min)

**Check GitHub plugin implementation**:
```bash
# Find GitHub plugin
ls -la services/plugins/github/
find services/plugins/ -name "*github*"

# Check if GitHub is wrapped as plugin
grep -r "GitHubPlugin" services/plugins/
grep -r "class.*GitHub.*Plugin" services/plugins/ --include="*.py"

# Check plugin registration
grep -r "register.*github" services/plugins/
grep -r "github" services/plugins/registry.py

# Find plugin manifest
find . -name "*manifest*" | grep -i github
find services/plugins/github/ -name "*.json" -o -name "*.yaml" -o -name "*.toml"
```

**Look for**:
- GitHubPlugin class
- Plugin manifest file
- Registration in plugin registry

#### 4. Verify Spatial Patterns Preserved (10 min)

**Check spatial implementation**:
```bash
# Find GitHub spatial implementation
ls -la services/integrations/spatial/github_spatial.py
cat services/integrations/spatial/github_spatial.py | head -100

# Check if spatial patterns integrated with plugin
grep -r "spatial" services/plugins/github/ --include="*.py"
grep -r "github_spatial" services/plugins/ --include="*.py"
```

**Verify**:
- Spatial intelligence still exists
- Plugin uses spatial patterns
- No regression in spatial functionality

#### 5. Check Plugin Boundaries (10 min)

**Verify clean separation**:
```bash
# Check for monolith dependencies
grep -r "from services\\.(?!plugins)" services/plugins/github/ || echo "Clean boundaries"
grep -r "import.*services\\.[^p]" services/plugins/github/ --include="*.py"

# Check reverse dependencies
grep -r "from services.plugins" services/ --include="*.py" | grep -v "services/plugins/"
```

**Verify**:
- Plugin doesn't import from monolith (except interfaces)
- Monolith uses plugin through registry
- Clean dependency graph

#### 6. Check Tests (10 min)

**Find and examine tests**:
```bash
# Find GitHub plugin tests
find tests/ -name "*github*" -type f
find tests/plugins/ -name "*" 2>/dev/null

# Check test status
grep -r "def test.*github" tests/ --include="*.py"
grep -r "GitHubPlugin" tests/ --include="*.py"
```

**Verify**:
- Tests exist for GitHub plugin
- Tests pass
- Coverage adequate

### Decision Matrix

**If all criteria met (GitHub fully extracted as plugin)**:
- **Recommendation**: CLOSE issue #175 as superseded by GREAT-3A
- **Evidence**: Document how GREAT-3A satisfied all criteria
- **Action**: Create supersession doc in `dev/2025/10/08/core-plug-refactor-superseded.md`
- **GitHub**: Close issue with reference to GREAT-3A completion

**If partially met (plugin infrastructure exists, GitHub not fully extracted)**:
- **Recommendation**: Document gaps, create follow-up issue
- **Gap**: List specific criteria not yet met
- **Action**: Create new issue for remaining work, close #175 as partial supersession
- **Priority**: Depends on gap size (small gaps = include in next CORE epic)

**If not met (plugin infrastructure incomplete)**:
- **Recommendation**: Keep issue #175 open, update scope
- **Action**: Update issue description with current status
- **Note**: This seems unlikely given GREAT-3A success, but document if true

**If ambiguous status**:
- **Recommendation**: Ask PM for clarification
- **Action**: Document what exists, what's unclear
- **Decision**: PM decides on close/keep/split

---

## Deliverables

### For Each Issue

**1. Investigation Report** (create in `dev/2025/10/08/`):
- File: `core-notn-publish-verification.md` (Issue #135)
- File: `core-plug-refactor-verification.md` (Issue #175)

**Content**:
- Summary of findings
- Acceptance criteria checklist (with evidence)
- Gap analysis (if any)
- Recommendation (close/complete/new-issue)
- Evidence files (list all relevant files found)

**2. Session Log Update**:
- File: `dev/2025/10/08/2025-10-08-1235-prog-code-log.md`
- Document investigation process
- Record findings and decisions
- Track time spent

### Summary Report

**File**: `dev/2025/10/08/stray-issues-investigation-summary.md`

**Content**:
- Both issues investigated
- Recommendations for each
- Next steps for PM
- Time investment

---

## Success Criteria

- [ ] Both issues thoroughly investigated
- [ ] All acceptance criteria verified against filesystem
- [ ] Clear recommendation for each issue (close/complete/new-issue)
- [ ] Evidence documented for all findings
- [ ] Reports created in `dev/2025/10/08/`
- [ ] Session log updated
- [ ] Ready for PM decision

---

## Critical Notes

- **Be thorough**: This is cleanup before major CORE work, need solid foundation
- **Document evidence**: List actual files, don't just claim "exists"
- **STOP if unclear**: If status is ambiguous, document and ask PM
- **Time-box**: 30-45 min per issue, stop if exceeding
- **Focus on facts**: What exists vs what's documented in issue

---

**Estimated Total Time**: 1-1.5 hours
**Priority**: HIGH (blocking CORE epic start)
**Deliverable**: Investigation reports + recommendations for both issues
