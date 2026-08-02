# Learning System Verification Tests

**Version**: 0.8.0 (Alpha)
**For**: Alpha Testers & Developers
**Purpose**: Verify learning system is working correctly
**Last Updated**: November 12, 2025
**Issue**: #288

> ⚠️ **Partially superseded (2026-08-01, issue 1430)**: this doc predates the #300
> database-backed learning system. The dashboard now lives at `/learning`
> (served from `templates/learning-dashboard.html`); the old
> `web/assets/learning-dashboard.html` copy and its `user_id=current_user`
> query params were removed. All learning routes now derive the user from the
> authenticated session — steps below that pass a `user_id` or navigate to
> `/assets/learning-dashboard.html` no longer apply.

---

## Overview

This document provides step-by-step verification tests to confirm the learning system is functional. Tests are organized by complexity and time required.

**Test Levels:**

- **Quick Verification** (5 minutes): Basic health and functionality checks
- **Comprehensive Verification** (30 minutes): End-to-end workflow testing
- **Debugging Tests** (15 minutes): Troubleshooting when things go wrong

---

## Prerequisites

Before running these tests:

1. **Piper Morgan Running:**

   ```bash
   python main.py
   ```

   System should be accessible at `http://localhost:8001`

2. **curl Installed:**

   ```bash
   curl --version
   ```

   Or use any HTTP client (Postman, HTTPie, etc.)

3. **File System Access:**
   ```bash
   ls -la data/learning/
   ```
   Should see `learned_patterns.json` and `pattern_feedback.json`

---

## Quick Verification (5 Minutes)

### Test 1: System Health Check

**Purpose**: Verify learning system is running and accessible

**Steps:**

```bash
curl http://localhost:8001/api/v1/learning/health
```

**Expected Output:**

```json
{
  "status": "healthy",
  "services": {
    "learning_loop": "available",
    "cross_feature_knowledge": "pending_phase_2"
  },
  "note": "Cross-feature knowledge requires database integration (Phase 2)"
}
```

**Success Criteria:**

- ✅ Status: "healthy"
- ✅ learning_loop: "available"
- ✅ HTTP 200 OK response

**If Failed:**

- Check if Piper Morgan is running
- Verify port 8001 is accessible
- Check server logs for errors

---

### Test 2: Pattern Count Check

**Purpose**: Verify patterns are loaded from storage

**Steps:**

```bash
curl http://localhost:8001/api/v1/learning/analytics
```

**Expected Output:**

```json
{
  "total_patterns": 92,
  "average_confidence": 0.84,
  "patterns_by_feature": {
    "QUERY": 10,
    "CREATE_TICKET": 10,
    "test_feature": 18,
    ...
  },
  "pattern_type_distribution": {
    "query_pattern": 44,
    "workflow_pattern": 43,
    "user_preference_pattern": 5
  },
  "total_feedback": 0,
  "recent_patterns_24h": 0,
  "recent_feedback_24h": 0
}
```

**Success Criteria:**

- ✅ total_patterns > 0 (should be ~92 from testing)
- ✅ average_confidence > 0.0
- ✅ pattern_type_distribution shows multiple types
- ✅ HTTP 200 OK response

**If Failed:**

- Check if `data/learning/learned_patterns.json` exists
- Verify file has valid JSON
- Check file permissions (should be readable)

---

### Test 3: Pattern Storage File Check

**Purpose**: Verify pattern data files exist and are valid

**Steps:**

```bash
# Check file existence
ls -la data/learning/

# Count patterns in file
cat data/learning/learned_patterns.json | grep -c "pattern_id"

# View first pattern
cat data/learning/learned_patterns.json | head -30
```

**Expected Output:**

- File exists: `learned_patterns.json` (60KB+)
- File exists: `pattern_feedback.json` (2KB+)
- Pattern count: ~92
- Valid JSON structure

**Success Criteria:**

- ✅ Both files exist
- ✅ Files are readable
- ✅ JSON is valid (no syntax errors)
- ✅ Pattern count matches analytics

**If Failed:**

- Files missing: Run `python main.py` to initialize
- Invalid JSON: Check for corruption, restore from backup
- Permission denied: Run `chmod 644 data/learning/*.json`

---

### Test 4: Dashboard Access

**Purpose**: Verify learning dashboard loads and displays data

**Steps:**

1. Open browser
2. Navigate to: `http://localhost:8001/assets/learning-dashboard.html`
3. Wait 2-3 seconds for data to load

**Expected Output:**

- Dashboard loads (not blank)
- "Learning Status" card shows "Enabled" (green badge)
- "Learning Metrics" card shows pattern count
- "Pattern Distribution" card shows bar chart
- No error messages in console (F12)

**Success Criteria:**

- ✅ Dashboard renders correctly
- ✅ All 5 cards visible
- ✅ Metrics display numbers
- ✅ No JavaScript errors

**If Failed:**

- Check browser console (F12 → Console)
- Verify `web/assets/learning-dashboard.html` exists
- Try different browser
- Check for CORS errors

---

## Comprehensive Verification (30 Minutes)

### Scenario 1: Record and Retrieve Pattern

**Purpose**: Verify complete pattern learning workflow

**Time**: 10 minutes

**Steps:**

1. **Record a Query Pattern:**

```bash
curl -X POST http://localhost:8001/api/v1/learning/patterns \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_type": "query_pattern",
    "source_feature": "alpha_test",
    "pattern_data": {
      "query_template": "find issues in {project} with status {status}",
      "parameters": {
        "project": "piper-morgan",
        "status": "open"
      }
    },
    "initial_confidence": 0.75,
    "metadata": {
      "test_id": "alpha_verification_1",
      "timestamp": "2025-11-12T09:00:00Z"
    }
  }'
```

2. **Verify Pattern Created:**

```json
{
  "status": "pattern_learned",
  "pattern_id": "query_pattern_alpha_test_20251112_090000",
  "confidence": 0.75
}
```

3. **Retrieve Pattern:**

```bash
curl "http://localhost:8001/api/v1/learning/patterns?source_feature=alpha_test&min_confidence=0.5"
```

4. **Verify Pattern in Response:**

- Check `patterns` array contains your pattern
- Verify `pattern_id` matches
- Confirm `confidence` = 0.75
- Count should be at least 1

**Expected Results:**

- ✅ Pattern created successfully
- ✅ Pattern ID returned
- ✅ Pattern appears in retrieval
- ✅ All metadata preserved
- ✅ Confidence score correct

**Cleanup:**

```bash
# Pattern will persist - you can clear later via dashboard
```

---

### Scenario 2: Apply Pattern and Provide Feedback

**Purpose**: Verify pattern application and feedback loop

**Time**: 10 minutes

**Steps:**

1. **Apply the Pattern (from Scenario 1):**

```bash
curl -X POST http://localhost:8001/api/v1/learning/patterns/apply \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_id": "query_pattern_alpha_test_20251112_090000",
    "context": {
      "project": "piper-morgan",
      "status": "in_progress"
    }
  }'
```

2. **Verify Application Result:**

```json
{
  "status": "pattern_applied",
  "pattern_id": "query_pattern_alpha_test_20251112_090000",
  "result": {
    "success": true,
    "query": "find issues in piper-morgan with status in_progress",
    "confidence": 0.75,
    "pattern_id": "query_pattern_alpha_test_20251112_090000"
  },
  "confidence": 0.75
}
```

3. **Provide Positive Feedback:**

```bash
curl -X POST http://localhost:8001/api/v1/learning/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_id": "query_pattern_alpha_test_20251112_090000",
    "success": true,
    "feedback": "Pattern formatted query correctly",
    "context": {
      "test": "alpha_verification"
    }
  }'
```

4. **Verify Feedback Recorded:**

```json
{
  "status": "feedback_recorded",
  "pattern_id": "query_pattern_alpha_test_20251112_090000",
  "success": true
}
```

5. **Check Analytics for Feedback:**

```bash
curl http://localhost:8001/api/v1/learning/analytics
```

Verify `total_feedback` increased by 1.

**Expected Results:**

- ✅ Pattern applies successfully
- ✅ Query formatted correctly
- ✅ Feedback recorded
- ✅ Feedback count increases in analytics
- ✅ Pattern confidence may increase (check after multiple feedbacks)

---

### Scenario 3: Test Pattern Persistence

**Purpose**: Verify patterns survive system restart

**Time**: 10 minutes

**Steps:**

1. **Record Current Pattern Count:**

```bash
curl http://localhost:8001/api/v1/learning/analytics | grep -o '"total_patterns":[0-9]*'
```

Note the number (e.g., 93)

2. **Record a New Pattern:**

```bash
curl -X POST http://localhost:8001/api/v1/learning/patterns \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_type": "workflow_pattern",
    "source_feature": "alpha_persistence_test",
    "pattern_data": {
      "workflow_steps": [
        {"step": 1, "action": "create_issue"},
        {"step": 2, "action": "assign_issue"},
        {"step": 3, "action": "set_priority"}
      ]
    },
    "initial_confidence": 0.8
  }'
```

3. **Verify Count Increased:**

```bash
curl http://localhost:8001/api/v1/learning/analytics | grep -o '"total_patterns":[0-9]*'
```

Should be 1 more than before (e.g., 94)

4. **Restart Piper Morgan:**

```bash
# Stop server (Ctrl+C in terminal)
# Restart server
python main.py
# Wait for startup (5-10 seconds)
```

5. **Check Pattern Count After Restart:**

```bash
curl http://localhost:8001/api/v1/learning/analytics | grep -o '"total_patterns":[0-9]*'
```

6. **Retrieve Your Pattern:**

```bash
curl "http://localhost:8001/api/v1/learning/patterns?source_feature=alpha_persistence_test"
```

**Expected Results:**

- ✅ Pattern count same before/after restart
- ✅ New pattern still retrievable
- ✅ All pattern data intact
- ✅ No data loss

**If Failed:**

- Check file system for `data/learning/learned_patterns.json`
- Verify file was written (check timestamp)
- Check for disk space issues
- Review server logs for errors

---

## Debugging Tests (15 Minutes)

### Debug Test 1: Check File System State

**Purpose**: Diagnose storage-related issues

**Steps:**

```bash
# Check directory exists
ls -la data/learning/

# Check file sizes
du -h data/learning/*

# Check file permissions
stat data/learning/learned_patterns.json

# Count patterns in file
cat data/learning/learned_patterns.json | python3 -c "import json,sys; print(len(json.load(sys.stdin)))"

# Validate JSON syntax
python3 -m json.tool data/learning/learned_patterns.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"

# Check last modified time
ls -l data/learning/learned_patterns.json
```

**What to Look For:**

- Files exist and are readable
- learned_patterns.json > 10KB (indicates patterns present)
- JSON is valid (no syntax errors)
- Recent modification time (indicates active writing)
- Proper permissions (644 or 664)

---

### Debug Test 2: API Endpoint Verification

**Purpose**: Test all learning endpoints for availability

**Steps:**

```bash
# Health check
curl -w "\n%{http_code}\n" http://localhost:8001/api/v1/learning/health

# Analytics
curl -w "\n%{http_code}\n" http://localhost:8001/api/v1/learning/analytics

# Get patterns
curl -w "\n%{http_code}\n" "http://localhost:8001/api/v1/learning/patterns?min_confidence=0.0"

# Test invalid endpoint (should 404)
curl -w "\n%{http_code}\n" http://localhost:8001/api/v1/learning/nonexistent
```

**Expected HTTP Codes:**

- Health: 200
- Analytics: 200
- Patterns: 200
- Nonexistent: 404

**If Different:**

- Check routing configuration
- Verify API is registered
- Check for middleware issues
- Review server logs

---

### Debug Test 3: Pattern Data Integrity

**Purpose**: Verify pattern data structure is correct

**Steps:**

```bash
# Extract first pattern
python3 << 'EOF'
import json
with open('data/learning/learned_patterns.json') as f:
    patterns = json.load(f)
    if patterns:
        p = patterns[0]
        print(f"Pattern ID: {p.get('pattern_id', 'MISSING')}")
        print(f"Type: {p.get('pattern_type', 'MISSING')}")
        print(f"Source: {p.get('source_feature', 'MISSING')}")
        print(f"Confidence: {p.get('confidence', 'MISSING')}")
        print(f"Usage: {p.get('usage_count', 'MISSING')}")
        print(f"Success Rate: {p.get('success_rate', 'MISSING')}")

        required_fields = ['pattern_id', 'pattern_type', 'source_feature',
                           'pattern_data', 'confidence', 'usage_count',
                           'success_rate', 'first_seen', 'last_used',
                           'feedback_score', 'metadata']

        missing = [f for f in required_fields if f not in p]
        if missing:
            print(f"\n⚠️  Missing fields: {missing}")
        else:
            print("\n✅ All required fields present")
    else:
        print("❌ No patterns found")
EOF
```

**What to Check:**

- All required fields present
- Valid data types (confidence = float, usage_count = int)
- Timestamps in ISO format
- No null/None values in required fields

---

### Debug Test 4: Dashboard Console Check

**Purpose**: Identify JavaScript errors preventing dashboard from working

**Steps:**

1. Open browser
2. Navigate to: `http://localhost:8001/assets/learning-dashboard.html`
3. Open Developer Tools (F12)
4. Go to Console tab
5. Refresh page

**What to Look For:**

- ❌ Red errors about API calls
- ❌ CORS (Cross-Origin) errors
- ❌ 404 errors for missing resources
- ❌ JavaScript syntax errors
- ✅ "Learning status loaded" (or similar success messages)

**Common Errors:**

- `Failed to fetch`: API not responding
- `CORS error`: Server CORS config issue
- `user_id is not defined`: Configuration error
- `Cannot read property`: Data structure mismatch

---

## Performance Tests (Optional)

### Load Test: Multiple Pattern Operations

**Purpose**: Verify system handles rapid operations

**Steps:**

```bash
# Record 10 patterns quickly
for i in {1..10}; do
  curl -X POST http://localhost:8001/api/v1/learning/patterns \
    -H "Content-Type: application/json" \
    -d "{
      \"pattern_type\": \"query_pattern\",
      \"source_feature\": \"load_test\",
      \"pattern_data\": {\"query\": \"test query $i\"},
      \"initial_confidence\": 0.6
    }" &
done
wait

# Check all were recorded
curl http://localhost:8001/api/v1/learning/analytics | grep total_patterns
```

**Expected:**

- All requests succeed (HTTP 200)
- Pattern count increases by 10
- Response time < 500ms per request
- No errors in logs

---

## Test Results Checklist

Use this checklist to track your verification progress:

### Quick Verification

- [ ] Test 1: System Health Check - PASS/FAIL
- [ ] Test 2: Pattern Count Check - PASS/FAIL
- [ ] Test 3: Pattern Storage File Check - PASS/FAIL
- [ ] Test 4: Dashboard Access - PASS/FAIL

### Comprehensive Verification

- [ ] Scenario 1: Record and Retrieve Pattern - PASS/FAIL
- [ ] Scenario 2: Apply Pattern and Provide Feedback - PASS/FAIL
- [ ] Scenario 3: Test Pattern Persistence - PASS/FAIL

### Debugging Tests (if needed)

- [ ] Debug 1: File System State - PASS/FAIL
- [ ] Debug 2: API Endpoint Verification - PASS/FAIL
- [ ] Debug 3: Pattern Data Integrity - PASS/FAIL
- [ ] Debug 4: Dashboard Console Check - PASS/FAIL

---

## Reporting Issues

If tests fail, please report with:

1. **Test Name**: Which test failed
2. **Steps to Reproduce**: Exact commands run
3. **Expected Result**: What should have happened
4. **Actual Result**: What actually happened
5. **Error Messages**: Full error output
6. **Environment**:
   - OS: (macOS, Linux, Windows)
   - Python version: `python --version`
   - Piper version: 0.8.0
7. **Logs**: Relevant server logs

**Report To:**

- GitHub Issue: #288
- Or create new issue with label `learning-system`

---

## Related Documentation

- **User Guide**: [learning-system-guide.md](./learning-system-guide.md)
- **API Reference**: [docs/public/api-reference/learning-api.md](../public/api-reference/learning-api.md)
- **Known Issues**: [dev/active/ALPHA_KNOWN_ISSUES.md](../ALPHA_KNOWN_ISSUES.md)

---

_Last Updated: November 12, 2025_
_Issue: #288 (CORE-ALPHA-LEARNING-INVESTIGATION)_
_Sprint: A8 (Alpha Polish)_
