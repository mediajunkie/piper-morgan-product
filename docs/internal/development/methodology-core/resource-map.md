---
type: methodology
title: Piper Morgan Resource Map
valid_from: "2025-09-21"
last_updated: "2025-09-21"
---

# Piper Morgan Resource Map

**Purpose**: Prevent agents from assuming resources don't exist. Always check here first!

---

## 🏛️ Architecture Decisions (ADRs)
- **Location**: `docs/architecture/decisions/`
- **Current Count**: 28 (ADR-000 through ADR-028)
- **Latest**: ADR-028 (Methodology Architecture)
- **Index**: `docs/architecture/decisions/index.md`

### How to Search ADRs
```bash
# List all ADRs
ls -la docs/architecture/decisions/

# Search for specific topic
grep -r "your_topic" docs/architecture/decisions/

# Read specific ADR
cat docs/architecture/decisions/ADR-XXX-title.md
```

### Key ADRs for Common Tasks
- **Error Handling**: ADR-013
- **Testing Strategy**: ADR-015
- **Configuration**: ADR-021
- **Methodology**: ADR-027, ADR-028

---

## 📚 Pattern Catalog
- **Location**: `docs/architecture/pattern-catalog.md`
- **Sections**:
  - Code Patterns (1-24)
  - Methodology Patterns (25-27)
  - Verification Patterns (PM-137/138/139 - check if added)
- **Last Updated**: Check file header for date

### How to Search Patterns
```bash
# View entire catalog
cat docs/architecture/pattern-catalog.md

# Search for specific pattern
grep -A 20 "Pattern Name" docs/architecture/pattern-catalog.md

# Check pattern numbers
grep "^## Pattern" docs/architecture/pattern-catalog.md
```

---

## 🎯 Methodology Core
- **Location**: `docs/development/methodology-core/`
- **Key Files**:
  - `methodology-00-EXCELLENCE-FLYWHEEL.md` - Core principles
  - `methodology-07-VERIFICATION-FIRST.md` - Verification requirements
  - `methodology-08-ISSUE-TRACKING.md` - GitHub/issue requirements
  - `methodology-18-CASCADE-PROTOCOL.md` - Cascade framework
  - `stop-conditions.md` - When to stop and escalate

### How to Find Methodology Requirements
```bash
# List all methodology docs
ls -la docs/development/methodology-core/

# Search for specific requirement
grep -r "verification" docs/development/methodology-core/

# Check stop conditions
cat docs/development/methodology-core/stop-conditions.md
```

---

## 📝 Templates
- **Location**: Project knowledge
- **Key Templates**:
  - `gameplan-template-enhanced.md` - For Chief Architect
  - `agent-prompt-template.md` - For Lead Developer
  - `github-guide.md` - GitHub operations
  - `cross-validation-protocol.md` - Agent verification

### How to Access Templates
```bash
# Templates are in project knowledge
# Access through project_knowledge_search tool

# Or check local copies
ls -la docs/development/templates/
```

---

## 💻 Existing Services
- **Location**: `services/`
- **Structure**:
  - `services/domain/` - Domain models and business logic
  - `services/queries/` - Query services
  - `services/orchestration/` - Workflow orchestration
  - `services/integrations/` - External integrations
  - `services/shared_types.py` - ALL enums and shared types

### How to Find Existing Implementations
```bash
# Search for feature across all services
grep -r "feature_name" services/ --include="*.py"

# Find all classes
grep -r "^class " services/ --include="*.py"

# Check shared types/enums
cat services/shared_types.py

# Find imports to understand dependencies
grep -r "from services" services/ --include="*.py"
```

---

## 📅 Planning Documents
- **Roadmap**: `docs/planning/../planning/roadmap.md`
- **Backlog**: `docs/planning/backlog.md`
- **PM Issues Status**: `docs/planning/pm-issues-status.csv`
- **GitHub Issues**: PM-XXX numbering scheme (currently up to PM-139)

### How to Check Issue Status
```bash
# Check CSV for PM numbers
cat docs/planning/pm-issues-status.csv | grep "PM-"

# Check backlog
grep "PM-" docs/planning/backlog.md

# Check GitHub
gh issue list --search "PM-"
```

---

## 📓 Session Logs
- **Current**: `development/session-logs/`
- **Archives**: `docs/development/session-archive-*.md`
- **Naming**: `YYYY-MM-DD-HHMM-agent-log.md`

### How to Find Session Context
```bash
# List recent sessions
ls -la development/session-logs/

# Search for specific work
grep -r "feature_name" development/session-logs/

# Check archives
ls -la docs/development/session-archive-*.md
```

---

## 🧪 Tests
- **Unit Tests**: `tests/unit/`
- **Integration Tests**: `tests/integration/`
- **Test Patterns**: Follow existing test structure

### How to Find Test Patterns
```bash
# Find tests for a service
find tests/ -name "*service_name*"

# Check test patterns
grep -r "def test_" tests/

# Run specific tests
pytest tests/unit/path/to/test.py -v
```

---

## 🔧 Configuration
- **Main Config**: `config/settings.py`
- **User Config**: `config/user/` (when implemented)
- **Environment**: `.env` files

### How to Check Configuration
```bash
# Check main settings
cat config/settings.py

# Find config usage
grep -r "settings\." services/

# Check for hardcoding (anti-pattern)
grep -r "hardcoded_value" services/
```

---

## 📚 Documentation
- **API Docs**: `docs/api/`
- **User Guides**: `docs/user/`
- **Development**: `docs/development/`
- **Architecture**: `docs/architecture/`

### How to Find Documentation to Update
```bash
# Search all docs for feature
grep -r "feature_name" docs/

# Find markdown files
find docs/ -name "*.md" | grep -i "feature"

# Check what might need updating
grep -r "TODO\|FIXME\|UPDATE" docs/
```

---

## ⚠️ CRITICAL REMINDERS

### Before Implementing ANYTHING:
1. **Check ADRs** - They're authoritative (28 exist!)
2. **Check Pattern Catalog** - Don't duplicate patterns
3. **Check services/** - Implementation might already exist
4. **Check shared_types.py** - All enums must go here

### Before Claiming Something Doesn't Exist:
1. **grep for it** across entire codebase
2. **find files** that might contain it
3. **Check session logs** for recent work
4. **Ask explicitly** if still not found

### Never Assume - Always Verify!

---

*Last Updated: September 5, 2025*
*Purpose: Prevent agents from assuming resources don't exist*
*Usage: Reference this BEFORE starting any implementation*
