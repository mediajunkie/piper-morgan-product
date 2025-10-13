# Gameplan: GREAT-4E-2 - Complete Validation Documentation & Operations

**Date**: October 6, 2025
**Epic**: GREAT-4E-2 (Completion of GREAT-4E)
**Context**: Complete missing 7 acceptance criteria from GREAT-4E
**Effort**: Medium (2-3 hours)

## Mission

Complete the remaining acceptance criteria for GREAT-4E that were not finished in the initial implementation: documentation, CI/CD integration, monitoring dashboard, and rollback plan.

## Background

GREAT-4E achieved 18/25 acceptance criteria (72%). Missing items:
- 6 documentation items (0/6)
- CI/CD integration
- Monitoring dashboard
- Rollback plan

These are not optional - they're part of the original acceptance criteria.

## Phase 0: Assessment & Planning
**Both Agents - Small effort**

### Verify What Exists
```bash
# Check for any existing documentation
ls -la docs/guides/intent*.md
ls -la docs/adrs/adr-032*

# Check CI/CD current state
cat .github/workflows/ci.yml | grep -i intent

# Check monitoring endpoints from GREAT-4B
grep -r "metrics\|monitor" services/intent_service/

# Check for rollback documentation
find docs/ -name "*rollback*"
```

### Document Current State
Create checklist of what actually needs to be created vs updated.

## Phase 1: Documentation Completion (6 items)
**Code Agent - Medium effort**

### Required Documents

1. **ADR-032 Update** (docs/adrs/adr-032-intent-universal.md)
   - Add implementation details from GREAT-4A-E
   - Document 13 categories
   - Include performance metrics
   - Note canonical handler pattern

2. **Intent Patterns Guide** (docs/guides/intent-patterns.md)
   - List all 13 categories with examples
   - Show classification patterns
   - Include confidence thresholds
   - Document common mis-classifications

3. **Classification Rules** (docs/guides/intent-classification-rules.md)
   - Pre-classifier rules
   - LLM classifier prompts
   - Category disambiguation
   - Fallback handling

4. **Migration Guide** (docs/guides/intent-migration.md)
   - How to add new intent categories
   - How to add new handlers
   - Testing requirements
   - Common pitfalls

5. **Categories Reference** (docs/reference/intent-categories.md)
   - Complete enumeration of 13 categories
   - Handler mappings
   - Response formats
   - Performance expectations

6. **README Update** (README.md)
   - Add intent system section
   - Link to guides
   - Basic usage examples

## Phase 2: CI/CD Integration
**Cursor Agent - Small effort**

### Add Intent Bypass Detection

In `.github/workflows/ci.yml`:
```yaml
- name: Check Intent Bypass Prevention
  run: |
    python scripts/check_intent_bypasses.py
    if [ $? -ne 0 ]; then
      echo "Intent bypass detected!"
      exit 1
    fi

- name: Classification Accuracy Gate
  run: |
    python tests/intent/test_classification_accuracy.py
    # Must maintain >90% accuracy
```

### Verify Integration
- Push test commit
- Verify CI runs intent checks
- Document in PR

## Phase 3: Monitoring Dashboard
**Code Agent - Medium effort**

### Define Reasonable Scope

**NOT overengineered** - Simple metrics endpoint:
```python
# services/intent_service/monitoring.py

async def get_intent_metrics():
    """Simple monitoring dashboard data"""
    return {
        "categories": {
            "TEMPORAL": {"count": x, "avg_time": y, "success_rate": z},
            # ... for all 13 categories
        },
        "total_requests": total,
        "cache_hit_rate": cache_rate,
        "avg_response_time": avg_time,
        "errors_last_hour": error_count,
        "bypass_attempts": bypass_count
    }
```

### Add Endpoint
```python
# In web/app.py
@app.get("/api/v1/intent/metrics")
async def intent_metrics():
    """Monitoring dashboard endpoint"""
    return await get_intent_metrics()
```

### Simple HTML Dashboard
Create `web/static/intent-dashboard.html`:
- Table showing metrics per category
- Auto-refresh every 30 seconds
- No complex visualization (keep it simple)

## Phase 4: Rollback Plan
**Cursor Agent - Small effort**

### Create Rollback Documentation

`docs/operations/intent-rollback-plan.md`:

```markdown
# Intent System Rollback Plan

## Identifying Need for Rollback
- Error rate >10%
- Response time >500ms sustained
- Classification accuracy <80%

## Rollback Steps
1. Revert to previous commit:
   ```bash
   git revert [commit-hash]
   git push origin main
   ```

2. Clear intent cache:
   ```bash
   curl -X POST http://localhost:8001/api/v1/intent/cache/clear
   ```

3. Restart services:
   ```bash
   systemctl restart piper-morgan
   ```

4. Verify rollback:
   ```bash
   python tests/intent/test_basic_functionality.py
   ```

## Monitoring After Rollback
- Check error logs
- Monitor classification accuracy
- Verify handler responses
```

## Phase Z: Final Validation
**Both Agents**

### Verify Completion
```bash
# All 6 documents exist
ls -la docs/guides/intent*.md | wc -l  # Should be 4+
ls -la docs/adrs/adr-032*  # Should exist
grep -i "intent" README.md  # Should have section

# CI/CD active
grep "intent" .github/workflows/ci.yml

# Monitoring endpoint works
curl http://localhost:8001/api/v1/intent/metrics

# Rollback plan exists
cat docs/operations/intent-rollback-plan.md
```

### Update GREAT-4E Issue
Check all remaining boxes with evidence links.

## Success Criteria (7 items)

- [ ] ADR-032 updated with implementation details
- [ ] Intent patterns guide created
- [ ] Classification rules documented
- [ ] Migration guide created
- [ ] README.md updated with intent section
- [ ] CI/CD integration active (bypass detection)
- [ ] Monitoring dashboard functional (simple metrics)
- [ ] Rollback plan documented

**TOTAL: Must achieve 7/7 = 100%**

## Agent Division

**Code Agent** - Phases 1, 3
- Documentation creation (6 items)
- Monitoring dashboard

**Cursor Agent** - Phases 2, 4
- CI/CD integration
- Rollback plan

## STOP Conditions

- If existing documentation conflicts with implementation
- If CI/CD pipeline not accessible
- If monitoring reveals unexpected issues

## Critical Notes

- Keep monitoring simple (metrics endpoint, not full dashboard)
- Documentation should reflect actual implementation
- CI/CD should use existing scripts from GREAT-4B
- Rollback plan should be practical, not theoretical

---

*Ready to complete GREAT-4E properly!*
