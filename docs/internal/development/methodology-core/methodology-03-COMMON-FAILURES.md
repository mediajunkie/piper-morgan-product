---
type: methodology
title: Common Failures That Break The Flywheel
valid_from: "2025-09-21"
last_updated: "2025-12-02"
---

# Common Failures That Break The Flywheel

## Top 5 Excellence Killers

### 1. Skipping Verification
**Symptom**: "I think the pattern is X..."
**Fix**: ALWAYS verify with grep/find/cat first

### 2. Code Before Test
**Symptom**: "I'll add the test after..."
**Fix**: Test FIRST, no exceptions

### 3. Solo Hero Mode
**Symptom**: "I'll just do this myself..."
**Fix**: Deploy agents strategically

### 4. Assumption Cascade
**Symptom**: One assumption leads to another
**Fix**: Verify at each step

### 5. Documentation Drift
**Symptom**: Code works but docs are wrong
**Fix**: TDD for documentation too

### 6. Frontend-Backend Path Mismatch (Issue #390 Discovery)
**Symptom**: All 5 API calls in JavaScript use wrong paths (e.g., `/api/setup/*` vs `/setup/*`)
**Root Cause**: Gameplan specifies paths without verifying actual backend route prefixes
**Why Methodology Leaked**:
- Phase -1 verified backend would work but not the exact mount path
- Frontend agent copied paths from gameplan without checking backend implementation
- No cross-validation step between backend agent output and frontend agent input

**Fix - Mandatory Phase -1 Contract Verification**:
```bash
# After backend routes created, BEFORE writing frontend:
grep -n "@router\." web/api/routes/[new_file].py  # Get endpoint paths
grep -n "include_router\|mount_router" web/app.py | grep [module]  # Get mount prefix

# Cross-validate: actual_path = mount_prefix + endpoint_path
# Example: "" + "/setup/status" = "/setup/status"
# Example: "/api/v1" + "/todos" = "/api/v1/todos"
```

**Gameplan Template Addition Required**:
```markdown
### Phase 1.X: Frontend-Backend Contract Verification (MANDATORY)
Before any frontend code:
1. List all backend endpoints with their FULL paths (prefix + route)
2. Verify paths by starting server and calling: `curl http://localhost:8001/[full-path]`
3. Only proceed to frontend after all paths return expected responses (not 404)
```

## Recovery Protocol
When you catch yourself failing:
1. STOP immediately
2. Review methodology documents
3. Start over with verification
4. Write the test you skipped
5. Deploy agents properly

**Remember**: The methodology IS the magic
