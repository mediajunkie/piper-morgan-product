# Prompt for Cursor Agent: GREAT-4E-2 Phase 4 - Monitoring Dashboard

## Context

Phase 3 complete: CI/CD verified (with critical fixes applied).

**This is Phase 4**: Create or document monitoring dashboard for intent system

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0752-prog-cursor-log.md`

## Mission

Complete the final GREAT-4E-2 acceptance criterion: functional monitoring dashboard for intent system.

---

## Phase 4: Monitoring Dashboard (1 Item)

### Background from Phase 0 Assessment

**Existing infrastructure**:
- ✅ Monitoring endpoints exist: `/api/admin/intent-monitoring`, `/api/admin/intent-cache-metrics`
- ✅ Backend metrics collection working (from GREAT-4B)
- ❌ No HTML/UI dashboard exists

**Two options identified**:
1. **Option A**: Create HTML/JS dashboard (30-45 min, more complex)
2. **Option B**: Document JSON API usage (20 min, simpler, API-first)

**Recommendation from assessment**: Start with Option B (document APIs), defer dashboard UI to future enhancement.

---

## Task 1: Verify Existing Monitoring Endpoints

Check what monitoring infrastructure exists:

```bash
# Check for monitoring endpoints in web/app.py
grep -n "intent.*monitor\|intent.*metrics" web/app.py

# Check for monitoring endpoints
curl http://localhost:8001/api/admin/intent-monitoring
curl http://localhost:8001/api/admin/intent-cache-metrics

# Check what data they return
curl http://localhost:8001/api/admin/intent-monitoring | jq .
```

**Document**:
- What endpoints exist?
- What data do they return?
- Are they working?

---

## Task 2: Decision Point - Dashboard vs Documentation

Based on what you find, choose approach:

### Option A: Create HTML Dashboard (if time allows)

Create simple monitoring dashboard:

**File**: `web/static/intent-dashboard.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Intent System Monitoring</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .metric-card {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #4CAF50;
        }
        .metric-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin: 5px 0;
        }
        .category-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .category-table th {
            background: #4CAF50;
            color: white;
            padding: 10px;
            text-align: left;
        }
        .category-table td {
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
        .category-table tr:hover {
            background: #f5f5f5;
        }
        .refresh-info {
            color: #666;
            font-size: 12px;
            text-align: right;
            margin-top: 10px;
        }
        .status-good { color: #4CAF50; }
        .status-warning { color: #ff9800; }
        .status-error { color: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Intent System Monitoring</h1>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total Requests</div>
                <div class="metric-value" id="total-requests">-</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Cache Hit Rate</div>
                <div class="metric-value" id="cache-hit-rate">-</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Avg Response Time</div>
                <div class="metric-value" id="avg-response">-</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Errors (Last Hour)</div>
                <div class="metric-value" id="error-count">-</div>
            </div>
        </div>

        <h2>Category Performance</h2>
        <table class="category-table">
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Count</th>
                    <th>Avg Time (ms)</th>
                    <th>Success Rate</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody id="category-table-body">
                <tr><td colspan="5">Loading...</td></tr>
            </tbody>
        </table>

        <div class="refresh-info">
            Auto-refresh every 30 seconds | Last updated: <span id="last-updated">-</span>
        </div>
    </div>

    <script>
        // Fetch and display metrics
        async function updateMetrics() {
            try {
                const response = await fetch('/api/admin/intent-monitoring');
                const data = await response.json();

                // Update summary metrics
                document.getElementById('total-requests').textContent =
                    data.total_requests?.toLocaleString() || '-';
                document.getElementById('cache-hit-rate').textContent =
                    data.cache_hit_rate ? `${(data.cache_hit_rate * 100).toFixed(1)}%` : '-';
                document.getElementById('avg-response').textContent =
                    data.avg_response_time ? `${data.avg_response_time.toFixed(0)}ms` : '-';
                document.getElementById('error-count').textContent =
                    data.errors_last_hour || '0';

                // Update category table
                if (data.categories) {
                    const tbody = document.getElementById('category-table-body');
                    tbody.innerHTML = Object.entries(data.categories)
                        .map(([category, stats]) => {
                            const successRate = stats.success_rate || 0;
                            const statusClass = successRate > 0.95 ? 'status-good' :
                                              successRate > 0.8 ? 'status-warning' : 'status-error';
                            const statusText = successRate > 0.95 ? '✅' :
                                             successRate > 0.8 ? '⚠️' : '❌';

                            return `
                                <tr>
                                    <td><strong>${category}</strong></td>
                                    <td>${stats.count?.toLocaleString() || 0}</td>
                                    <td>${stats.avg_time?.toFixed(0) || '-'}</td>
                                    <td>${(successRate * 100).toFixed(1)}%</td>
                                    <td class="${statusClass}">${statusText}</td>
                                </tr>
                            `;
                        }).join('');
                }

                // Update timestamp
                document.getElementById('last-updated').textContent =
                    new Date().toLocaleTimeString();

            } catch (error) {
                console.error('Error fetching metrics:', error);
            }
        }

        // Initial load
        updateMetrics();

        // Auto-refresh every 30 seconds
        setInterval(updateMetrics, 30000);
    </script>
</body>
</html>
```

**Then add route in web/app.py**:
```python
from fastapi.responses import FileResponse
import os

@app.get("/admin/intent-dashboard")
async def intent_dashboard():
    """Serve the intent monitoring dashboard."""
    dashboard_path = os.path.join("web", "static", "intent-dashboard.html")
    return FileResponse(dashboard_path)
```

### Option B: Document API Usage (simpler, recommended)

Create: `docs/operations/intent-monitoring-api.md`

```markdown
# Intent System Monitoring API

**Version**: 1.0
**Last Updated**: October 6, 2025
**Status**: Production Ready

## Overview

The intent system provides JSON monitoring endpoints for programmatic monitoring and dashboard integration. These endpoints are exempt from intent enforcement and return real-time metrics.

## Monitoring Endpoints

### 1. Intent Monitoring Overview

**Endpoint**: `GET /api/admin/intent-monitoring`
**Authentication**: None (admin endpoints, configure auth as needed)
**Response Format**: JSON

**Example Request**:
```bash
curl http://localhost:8001/api/admin/intent-monitoring
```

**Example Response**:
```json
{
  "categories": {
    "TEMPORAL": {
      "count": 1234,
      "avg_time": 1.2,
      "success_rate": 0.98
    },
    "STATUS": {
      "count": 567,
      "avg_time": 0.8,
      "success_rate": 0.99
    },
    // ... all 13 categories
  },
  "total_requests": 8901,
  "cache_hit_rate": 0.846,
  "avg_response_time": 1.5,
  "errors_last_hour": 3,
  "bypass_attempts": 0
}
```

### 2. Cache Metrics

**Endpoint**: `GET /api/admin/intent-cache-metrics`
**Response Format**: JSON

**Example Request**:
```bash
curl http://localhost:8001/api/admin/intent-cache-metrics
```

**Example Response**:
```json
{
  "hit_rate": 0.846,
  "hits": 7530,
  "misses": 1371,
  "speedup": 7.6,
  "avg_cached_time": 0.1,
  "avg_uncached_time": 2700
}
```

## Usage Examples

### Basic Health Check

Monitor overall system health:
```bash
#!/bin/bash
# check-intent-health.sh

RESPONSE=$(curl -s http://localhost:8001/api/admin/intent-monitoring)
ERROR_COUNT=$(echo $RESPONSE | jq '.errors_last_hour')

if [ "$ERROR_COUNT" -gt 10 ]; then
    echo "⚠️ High error rate: $ERROR_COUNT errors in last hour"
    exit 1
fi

echo "✅ Intent system healthy"
```

### Category Performance Monitoring

Track per-category metrics:
```bash
#!/bin/bash
# monitor-categories.sh

curl -s http://localhost:8001/api/admin/intent-monitoring | \
  jq -r '.categories | to_entries[] |
    "\(.key): \(.value.count) requests, \(.value.avg_time)ms avg, \(.value.success_rate * 100)% success"'
```

**Output**:
```
TEMPORAL: 1234 requests, 1.2ms avg, 98.0% success
STATUS: 567 requests, 0.8ms avg, 99.0% success
...
```

### Cache Performance

Monitor cache effectiveness:
```bash
#!/bin/bash
# check-cache.sh

METRICS=$(curl -s http://localhost:8001/api/admin/intent-cache-metrics)
HIT_RATE=$(echo $METRICS | jq -r '.hit_rate * 100')
SPEEDUP=$(echo $METRICS | jq -r '.speedup')

echo "Cache hit rate: ${HIT_RATE}%"
echo "Cache speedup: ${SPEEDUP}x"

if (( $(echo "$HIT_RATE < 80" | bc -l) )); then
    echo "⚠️ Cache hit rate below 80% threshold"
fi
```

### Prometheus Integration

Export metrics for Prometheus:
```bash
#!/bin/bash
# prometheus-exporter.sh

# Fetch metrics
DATA=$(curl -s http://localhost:8001/api/admin/intent-monitoring)

# Export in Prometheus format
echo "# HELP intent_total_requests Total intent requests processed"
echo "# TYPE intent_total_requests counter"
echo "intent_total_requests $(echo $DATA | jq '.total_requests')"

echo "# HELP intent_cache_hit_rate Cache hit rate"
echo "# TYPE intent_cache_hit_rate gauge"
echo "intent_cache_hit_rate $(echo $DATA | jq '.cache_hit_rate')"

# Per-category metrics
echo $DATA | jq -r '.categories | to_entries[] |
  "intent_category_requests{category=\"\(.key)\"} \(.value.count)"'
```

## Grafana Dashboard (Optional)

If using Grafana, import these queries:

**Panel 1: Total Requests**
```
intent_total_requests
```

**Panel 2: Cache Hit Rate**
```
intent_cache_hit_rate * 100
```

**Panel 3: Category Breakdown**
```
sum by (category) (intent_category_requests)
```

## Alert Thresholds

Recommended alert thresholds:

| Metric | Warning | Critical |
|--------|---------|----------|
| Error rate | >5% | >10% |
| Response time | >3s | >5s |
| Cache hit rate | <70% | <60% |
| Success rate | <95% | <90% |

## Integration with Monitoring Tools

### Datadog

```python
import datadog
from datadog import statsd

# Fetch metrics
response = requests.get('http://localhost:8001/api/admin/intent-monitoring')
data = response.json()

# Send to Datadog
statsd.gauge('intent.total_requests', data['total_requests'])
statsd.gauge('intent.cache_hit_rate', data['cache_hit_rate'])
statsd.gauge('intent.errors', data['errors_last_hour'])
```

### New Relic

```python
import newrelic.agent

# Fetch and report metrics
response = requests.get('http://localhost:8001/api/admin/intent-monitoring')
data = response.json()

newrelic.agent.record_custom_metric('Intent/TotalRequests', data['total_requests'])
newrelic.agent.record_custom_metric('Intent/CacheHitRate', data['cache_hit_rate'])
```

## Troubleshooting

### Endpoints Return 404

**Issue**: Monitoring endpoints not found
**Solution**: Verify web app is running and endpoints are registered:
```bash
curl -I http://localhost:8001/api/admin/intent-monitoring
```

### No Data Returned

**Issue**: Endpoints return empty or null data
**Solution**: Verify intent enforcement middleware is active and processing requests.

### Stale Data

**Issue**: Metrics don't update
**Solution**: Check that intent service is processing new requests. Metrics update in real-time.

## Security Considerations

**Warning**: These endpoints expose system metrics without authentication by default.

**Recommendations**:
1. Add authentication to `/api/admin/*` endpoints
2. Restrict access to monitoring endpoints via firewall
3. Use API keys for programmatic access
4. Monitor access to monitoring endpoints

## Related Documentation

- [Rollback Plan](./intent-rollback-plan.md)
- [Operational Guide](./operational-guide.md)
- [ADR-032: Intent Architecture](../internal/architecture/current/adrs/adr-032-intent-classification-universal-entry.md)

---

**Document Status**: ✅ Production Ready
**Endpoints Validated**: October 6, 2025
**Last Updated**: October 6, 2025
```

---

## Task 3: Create Verification Report

Create: `dev/2025/10/06/great4e-2-phase4-cursor-monitoring.md`

Document what approach you took and verification results.

---

## File Naming Convention

**Save your work as**: `great4e-2-phase4-cursor-monitoring.md`

---

## Success Criteria

**Must achieve ONE of these:**
- [ ] **Option A**: HTML dashboard created and functional (`/admin/intent-dashboard` works)
- [ ] **Option B**: API monitoring documentation created (comprehensive guide)

**Both options must include**:
- [ ] Verification that monitoring endpoints work
- [ ] Examples of how to use monitoring
- [ ] Integration with existing monitoring tools
- [ ] Session log updated

---

## Validation

After completion:

**For Option A (Dashboard)**:
```bash
# Verify dashboard file exists
ls -la web/static/intent-dashboard.html

# Test dashboard loads
curl http://localhost:8001/admin/intent-dashboard

# Verify it displays metrics
# (Open in browser and check that metrics load)
```

**For Option B (Documentation)**:
```bash
# Verify doc exists
ls -la docs/operations/intent-monitoring-api.md
wc -l docs/operations/intent-monitoring-api.md  # Should be >200 lines

# Verify endpoints work
curl http://localhost:8001/api/admin/intent-monitoring | jq .
curl http://localhost:8001/api/admin/intent-cache-metrics | jq .
```

---

## Critical Notes

- Keep it simple - this is the last item for GREAT-4E-2 completion
- Option B (documentation) is faster and equally valid
- Dashboard UI can be future enhancement
- Focus on functional monitoring, not perfect visualization

---

**Effort**: Small (~20-30 minutes for Option B, ~45 minutes for Option A)
**Priority**: HIGH (final acceptance criterion)
**Deliverable**: Functional monitoring solution (dashboard OR documentation)
