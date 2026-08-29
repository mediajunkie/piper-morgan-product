# Intent System Rollback Plan

**Version**: 1.0
**Last Updated**: October 6, 2025
**Status**: Production Ready

## Overview

This document provides emergency rollback procedures for the intent classification system. Use these procedures when the intent system is experiencing issues that require immediate intervention.

## Identifying Need for Rollback

### Critical Symptoms

Rollback immediately if you observe:
- **Error rate >10%**: Sustained error rate above 10% for >5 minutes
- **Response time >5s**: P95 response time exceeds 5 seconds
- **Classification accuracy <70%**: Significant mis-classification causing user issues
- **Complete system failure**: Intent service crashes or becomes unresponsive

### Warning Symptoms

Consider rollback if you observe:
- **Error rate 5-10%**: Elevated but not critical error rate
- **Response time 3-5s**: Degraded but functional performance
- **Classification accuracy 70-80%**: Lower accuracy than validated baseline
- **Memory leaks**: Continuous memory growth over 1 hour

## Monitoring Endpoints

Check system health:
```bash
# Intent monitoring dashboard
curl http://localhost:8001/api/admin/intent-monitoring

# Cache metrics
curl http://localhost:8001/api/admin/intent-cache-metrics

# Check error rate
curl http://localhost:8001/api/admin/intent-monitoring | jq '.errors_last_hour'
```

## Rollback Procedures

### Option 1: Rollback to Previous Commit (RECOMMENDED)

**When**: Intent handlers or classification logic has bugs

**Steps**:

1. **Identify last known good commit**:
```bash
# Check recent commits
git log --oneline services/intent/ | head -10

# Find GREAT-4E deployment commit
git log --grep="GREAT-4E" --oneline
```

2. **Revert to last good commit**:
```bash
# Revert specific commit
git revert [bad-commit-hash]

# Or reset to known good commit (nuclear option)
git reset --hard [good-commit-hash]
git push origin main --force
```

3. **Verify rollback**:
```bash
# Run basic functionality tests
PYTHONPATH=. python3 -m pytest tests/intent/test_direct_interface.py -v

# Check that all 13 categories work
PYTHONPATH=. python3 tests/intent/test_basic_functionality.py
```

4. **Clear intent cache**:
```bash
curl -X POST http://localhost:8001/api/admin/intent-cache/clear
```

5. **Restart services**:
```bash
# Local development
./scripts/restart-services.sh

# Production
systemctl restart piper-morgan
```

### Option 2: Disable Specific Category

**When**: One category is failing but others work

**Steps**:

1. **Comment out category handler** in `services/intent/intent_service.py`:
```python
async def process_intent(self, intent: Intent, session_id: str):
    # Temporarily disable problematic category
    if intent.category == IntentCategory.PROBLEMATIC:
        return IntentResult(
            success=False,
            message="This feature is temporarily unavailable"
        )

    # Normal processing continues
    if intent.category == IntentCategory.TEMPORAL:
        return await self._handle_temporal_intent(...)
```

2. **Deploy hotfix**:
```bash
git commit -am "Hotfix: Disable PROBLEMATIC category temporarily"
git push origin main
```

3. **Monitor other categories**:
```bash
curl http://localhost:8001/api/admin/intent-monitoring
```

### Option 3: Emergency Bypass (LAST RESORT)

**When**: Complete intent system failure, need immediate fallback

**WARNING**: This breaks the universal entry point architecture. Use only in emergencies.

**Steps**:

1. **Enable bypass flag** in `config/PIPER.user.md`:
```yaml
intent_classification:
  enabled: false  # Temporarily disable intent classification
  bypass_mode: true
```

2. **Restart services**:
```bash
systemctl restart piper-morgan
```

3. **Verify fallback routing**:
```bash
# Should route directly without classification
curl -X POST http://localhost:8001/api/v1/chat \
  -d '{"message": "test"}'
```

4. **Immediate followup**: File incident report and plan proper fix.

## Post-Rollback Procedures

### 1. Verify System Health

After rollback, verify:
```bash
# Check error rate
curl http://localhost:8001/api/admin/intent-monitoring | jq '.errors_last_hour'
# Should be <5

# Check classification accuracy
curl http://localhost:8001/api/admin/intent-monitoring | jq '.classification_accuracy'
# Should be >90%

# Check response times
curl http://localhost:8001/api/admin/intent-monitoring | jq '.avg_response_time'
# Should be <3000ms

# Run full test suite
pytest tests/intent/ -v
# Should show 126/126 passing
```

### 2. Root Cause Analysis

Document what went wrong:
- What symptoms were observed?
- What change triggered the issue?
- Why did monitoring not catch it earlier?
- What tests would have caught this?

### 3. Create Prevention Plan

- Add tests for the failure scenario
- Update monitoring thresholds
- Improve classification prompts
- Add safeguards to code

### 4. Communicate Status

Notify stakeholders:
- What was rolled back
- Current system status
- Expected timeline for fix
- Action items for prevention

## Recovery Procedures

### Recovering from Rollback

Once the issue is fixed:

1. **Create fix branch**:
```bash
git checkout -b fix/intent-issue-YYYYMMDD
```

2. **Implement fix with tests**:
```bash
# Fix the issue
# Add regression tests
pytest tests/intent/ -v  # Verify all pass
```

3. **Test in staging**:
```bash
# Deploy to staging
# Monitor for 1 hour
# Verify metrics are healthy
```

4. **Deploy to production**:
```bash
git push origin fix/intent-issue-YYYYMMDD
# Create PR, get review
# Merge to main
# Monitor closely for 24 hours
```

## Escalation

### When to Escalate

Escalate immediately if:
- Rollback doesn't resolve issues
- Multiple rollbacks needed in short time
- Data corruption suspected
- Security issue identified

### Escalation Contacts

[Add your team's escalation contacts]

## Testing Rollback Procedures

**Recommended**: Test rollback procedures in staging quarterly.

```bash
# Simulate rollback in staging
git checkout staging
git revert [recent-commit]
./scripts/test-rollback.sh
```

## Related Documentation

- [Intent Classification Guide](../guides/intent-classification-guide.md)
- [Migration Guide](../guides/intent-migration.md)
- [ADR-032: Intent Universal Entry](../internal/architecture/adrs/adr-032-intent-classification-universal-entry.md)
- [Operational Guide](./operational-guide.md)

---

**Document Status**: ✅ Production Ready
**Last Tested**: October 6, 2025
**Review Cycle**: Quarterly
