# Learning System User Guide

**Version**: 0.8.0 (Alpha)
**Status**: Experimental - Manual Activation Required
**Last Updated**: November 12, 2025
**Issue**: #288

---

## ⚠️ Alpha Status Notice

The learning system in Piper Morgan v0.8.0 is **experimental** and requires **manual activation**. It does NOT automatically learn from your conversations or usage patterns yet. This guide explains how to interact with the learning system and verify it's working.

---

## What is the Learning System?

The learning system allows Piper Morgan to capture patterns from your interactions and improve over time. It learns from:

- **Query patterns**: How you phrase requests
- **Workflow patterns**: Sequences of actions you perform repeatedly
- **Response patterns**: How you prefer information formatted
- **User preferences**: Your customization choices

**Privacy Note**: The system learns from metadata and patterns only. No personally identifiable information (PII) is stored.

---

## How Learning Works (v0.8.0)

### Automatic vs Manual

**In v0.8.0 Alpha:**

- ✅ **Pattern Loading**: Automatic (existing patterns loaded on startup)
- ✅ **Pattern Storage**: Automatic (patterns saved to disk)
- ❌ **Pattern Recording**: Manual (requires API call)
- ❌ **Pattern Application**: Manual (requires API call)

**What this means:**

- Piper won't automatically learn from your conversations
- You must use the Learning API or Dashboard to record patterns
- Patterns you record will be available immediately
- Future versions will support automatic learning

### What Gets Learned

When you manually record a pattern, the system stores:

1. **Pattern Type**: query, workflow, response, etc.
2. **Pattern Data**: The actual content of the pattern
3. **Confidence Score**: How confident the system is (0.0-1.0)
4. **Usage Count**: How many times it's been applied
5. **Success Rate**: How often it works well
6. **Feedback**: Your ratings on effectiveness

### Storage & Privacy

- **Location**: `data/learning/` directory
- **Format**: JSON files (human-readable)
- **Persistence**: Patterns survive system restarts
- **Privacy**: Only metadata stored, no conversation content
- **Control**: You can export, view, or delete all learning data

---

## Current System State

**As of v0.8.0:**

- ✅ **92 patterns** from October 2025 testing
- ✅ Learning infrastructure fully functional
- ✅ API endpoints working
- ✅ Dashboard available
- ⏸️ Automatic conversation learning: Not yet active
- ⏸️ Cross-feature knowledge sharing: Requires database (Phase 2)

**Active Features:**

- Pattern management API
- Learning dashboard
- Privacy controls
- Data export/import
- Manual pattern recording

**Inactive Features:**

- Automatic pattern detection
- Real-time learning from conversations
- Cross-feature knowledge sharing (requires database)

---

## Activating & Using Learning

### Step 1: Check System Status

**Via API:**

```bash
curl http://localhost:8001/api/v1/learning/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "services": {
    "learning_loop": "available",
    "cross_feature_knowledge": "pending_phase_2"
  }
}
```

**Via Dashboard:**

1. Open: `http://localhost:8001/assets/learning-dashboard.html`
2. Check "Learning Status" card
3. Should show: **Enabled** (green badge)

### Step 2: View Current Patterns

**Via API:**

```bash
curl http://localhost:8001/api/v1/learning/analytics
```

**Expected Response:**

```json
{
  "total_patterns": 92,
  "average_confidence": 0.84,
  "patterns_by_feature": {
    "QUERY": 10,
    "CREATE_TICKET": 10,
    "test_feature": 18
  },
  "total_feedback": 0,
  "recent_patterns_24h": 0
}
```

**Via Dashboard:**

1. Open Learning Dashboard
2. Check "Learning Metrics" card
3. View pattern counts and confidence scores

### Step 3: Record a Pattern (Manual)

**Example: Recording a Query Pattern**

```bash
curl -X POST http://localhost:8001/api/v1/learning/patterns \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_type": "query_pattern",
    "source_feature": "user_search",
    "pattern_data": {
      "query_template": "find issues in {project}",
      "parameters": {"project": "string"}
    },
    "initial_confidence": 0.7,
    "metadata": {
      "description": "Search issues by project name"
    }
  }'
```

**Response:**

```json
{
  "status": "pattern_learned",
  "pattern_id": "query_pattern_user_search_20251112_090000",
  "confidence": 0.7
}
```

### Step 4: Apply a Pattern (Manual)

```bash
curl -X POST http://localhost:8001/api/v1/learning/patterns/apply \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_id": "query_pattern_user_search_20251112_090000",
    "context": {
      "project": "piper-morgan"
    }
  }'
```

**Response:**

```json
{
  "status": "pattern_applied",
  "pattern_id": "query_pattern_user_search_20251112_090000",
  "result": {
    "success": true,
    "query": "find issues in piper-morgan"
  },
  "confidence": 0.7
}
```

### Step 5: Provide Feedback

```bash
curl -X POST http://localhost:8001/api/v1/learning/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_id": "query_pattern_user_search_20251112_090000",
    "success": true,
    "feedback": "Pattern worked perfectly",
    "context": {}
  }'
```

**Response:**

```json
{
  "status": "feedback_recorded",
  "pattern_id": "query_pattern_user_search_20251112_090000",
  "success": true
}
```

---

## Verifying Learning is Working

### Quick Check (2 minutes)

1. **Check Health:**

   ```bash
   curl http://localhost:8001/api/v1/learning/health
   ```

   Expected: `"status": "healthy"`

2. **Check Pattern Count:**

   ```bash
   curl http://localhost:8001/api/v1/learning/analytics
   ```

   Expected: `"total_patterns": <number>`

3. **View Patterns File:**
   ```bash
   cat data/learning/learned_patterns.json | head -20
   ```
   Expected: JSON array of patterns

### Comprehensive Check (10 minutes)

1. **Record a Test Pattern:**

   - Use API to record a pattern (see Step 3 above)
   - Note the `pattern_id` returned

2. **Verify Pattern Stored:**

   ```bash
   curl "http://localhost:8001/api/v1/learning/patterns?source_feature=test&min_confidence=0.0"
   ```

   - Check if your pattern appears in results

3. **Apply the Pattern:**

   - Use API to apply pattern (see Step 4 above)
   - Verify `"success": true` in response

4. **Submit Feedback:**

   - Provide positive feedback (see Step 5 above)
   - Check analytics for updated feedback count

5. **Restart System:**
   - Stop and restart Piper Morgan
   - Run analytics check again
   - Verify pattern count persisted

**Success Criteria:**

- ✅ Health check returns "healthy"
- ✅ Pattern count increases after recording
- ✅ Pattern appears in retrieval
- ✅ Pattern can be applied
- ✅ Feedback is recorded
- ✅ Patterns persist after restart

---

## Using the Learning Dashboard

**URL**: `http://localhost:8001/assets/learning-dashboard.html`

### Dashboard Features

1. **Learning Status Card**

   - Current status (Enabled/Disabled)
   - Toggle button to enable/disable
   - Visual indicator (green/red)

2. **Learning Metrics Card**

   - Total patterns learned
   - Active preferences
   - Success rate
   - Last updated timestamp

3. **Pattern Distribution Card**

   - Bar chart of pattern types
   - Counts by category
   - Percentage distribution

4. **Privacy Settings Card**

   - Share patterns across features (OFF by default)
   - Allow pattern suggestions (OFF by default)
   - Enable cross-user learning (OFF by default)
   - Store detailed metadata (OFF by default)
   - Analytics participation (OFF by default)

5. **Data Management Card**
   - Export data (JSON format)
   - Clear all data
   - Clear patterns only
   - Clear preferences only

### Using the Dashboard

**Enable/Disable Learning:**

1. Open dashboard
2. Click toggle button in "Learning Status" card
3. Confirm in dialog
4. Status updates immediately

**Export Your Data:**

1. Click "Export Data (JSON)" button
2. File downloads automatically
3. Review data in JSON viewer

**Clear Learning Data:**

1. Select data type from dropdown
2. Click "Clear Selected Data"
3. Confirm action
4. Data is removed (can't be undone)

**Keyboard Shortcuts:**

- `Ctrl+R`: Manual refresh
- `Ctrl+E`: Export data

---

## Troubleshooting

### "Learning System Not Working"

**Problem**: API returns errors or dashboard shows "unavailable"

**Solutions:**

1. Check if Piper Morgan is running:

   ```bash
   curl http://localhost:8001/health
   ```

   Expected: 200 OK

2. Verify learning files exist:

   ```bash
   ls -la data/learning/
   ```

   Expected: `learned_patterns.json` and `pattern_feedback.json`

3. Check file permissions:

   ```bash
   chmod 644 data/learning/*.json
   ```

4. Restart Piper Morgan

### "No Patterns Showing Up"

**Problem**: After using Piper, no patterns are recorded

**Explanation**: In v0.8.0, learning is **manual**. Patterns are not automatically recorded from conversations.

**Solutions:**

1. Use the Learning API to manually record patterns
2. Check existing patterns:
   ```bash
   curl http://localhost:8001/api/v1/learning/analytics
   ```
3. Future versions will support automatic learning

### "Dashboard Won't Load"

**Problem**: Dashboard page shows blank or errors

**Solutions:**

1. Check browser console (F12 → Console)
2. Verify file exists:
   ```bash
   ls -la web/assets/learning-dashboard.html
   ```
3. Try different browser
4. Check server logs for errors

### "Pattern Confidence Too Low"

**Problem**: Patterns not being applied due to low confidence

**Solutions:**

1. Check minimum confidence setting:
   ```bash
   curl http://localhost:8001/api/v1/preferences/learning_min_confidence?user_id=<your_user_id>
   ```
2. Provide positive feedback to increase confidence
3. Record pattern with higher initial confidence (0.7+)

### "Patterns Not Persisting"

**Problem**: Patterns disappear after restart

**Solutions:**

1. Check file permissions:
   ```bash
   ls -la data/learning/
   ```
2. Verify disk space:
   ```bash
   df -h
   ```
3. Check for errors in logs
4. Manually save patterns file

---

## Configuration

### User-Level Settings

**Via User Preferences API:**

- `learning_enabled`: Enable/disable learning (default: true)
- `learning_min_confidence`: Minimum confidence for pattern application (default: 0.5)
- `learning_features`: List of features enabled for learning (default: all)

**Via Privacy Settings:**

- `share_patterns`: Allow pattern sharing across features (default: false)
- `share_across_users`: Allow anonymized pattern sharing (default: false)
- `data_retention_days`: Days to retain learned data (default: 0 = forever)
- `allow_automation`: Allow intelligent automation (default: true)
- `allow_predictive`: Allow predictive assistance (default: true)

### System-Level Settings

**Storage Path**: `data/learning/`

- Can be changed in `QueryLearningLoop(storage_path="...")`

**Cleanup Thresholds**:

- Age: 30 days
- Min usage: 3 times
- Min confidence: 0.4

---

## Known Limitations (Alpha v0.8.0)

1. **Manual Activation Required**

   - Patterns must be explicitly recorded via API
   - No automatic learning from conversations
   - Future versions will support automatic detection

2. **Cross-Feature Knowledge Inactive**

   - Requires database integration (Phase 2)
   - Pattern sharing between features not yet available
   - API endpoints return "pending_phase_2" status

3. **Single-User Focus**

   - Patterns stored globally, not per-user
   - User filtering not yet implemented
   - Clear data affects all patterns

4. **Limited Pattern Types**

   - Core types implemented (query, workflow, response)
   - Extended types available but not well-tested
   - Integration patterns require Phase 2

5. **Dashboard Limitations**
   - User ID hardcoded as "current_user"
   - No multi-user support in UI
   - CSV export not implemented

---

## Your Feedback

**What We Need to Know:**

- [ ] Is learning recording patterns during your usage?
- [ ] Can you see patterns in the dashboard?
- [ ] Do patterns persist after restart?
- [ ] Is the manual API workflow clear?
- [ ] What features would benefit most from automatic learning?

**Report Issues:**

- Patterns not recording correctly
- Dashboard not loading or showing errors
- Unexpected learning behavior
- Performance concerns
- Privacy/security questions

---

## Future Enhancements (Post-Alpha)

**Planned for Beta:**

- Automatic pattern detection during conversations
- Real-time learning from user interactions
- Cross-feature knowledge sharing (with database)
- Per-user pattern filtering and isolation
- Improved confidence scoring algorithms
- Template-based pattern suggestions
- Advanced analytics and insights

**Under Consideration:**

- Machine learning for pattern discovery
- Collaborative filtering across users
- Predictive pattern recommendations
- Integration with external learning systems
- Pattern marketplace/sharing

---

## Related Documentation

- **API Reference**: [docs/public/api-reference/learning-api.md](../public/api-reference/learning-api.md)
- **Dashboard Guide**: [docs/api/learning-dashboard-guide.md](../api/learning-dashboard-guide.md)
- **Alpha Known Issues**: [dev/active/ALPHA_KNOWN_ISSUES.md](../ALPHA_KNOWN_ISSUES.md)
- **Verification Tests**: [docs/features/learning-system-verification-tests.md](./learning-system-verification-tests.md)

---

**For Developers:**

- Source Code: `services/learning/query_learning_loop.py`
- API Routes: `web/api/routes/learning.py`
- Tests: `tests/integration/test_learning_system.py`

---

_Last Updated: November 12, 2025_
_Issue: #288 (CORE-ALPHA-LEARNING-INVESTIGATION)_
_Sprint: A8 (Alpha Polish)_
