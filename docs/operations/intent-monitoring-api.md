# Intent System Monitoring API

**Version**: 1.0
**Last Updated**: October 6, 2025
**Status**: Production Ready
**Epic**: GREAT-4E-2 Phase 4 - Monitoring Dashboard

---

## Overview

The intent system provides JSON monitoring endpoints for programmatic monitoring and dashboard integration. These endpoints are exempt from intent enforcement and return real-time metrics for system health, performance, and security monitoring.

**Key Features**:

- Real-time intent enforcement status
- Cache performance metrics
- Security monitoring (bypass detection)
- Integration-ready JSON APIs
- No authentication required (configure as needed)

---

## Monitoring Endpoints

### 1. Intent Enforcement Monitoring

**Endpoint**: `GET /api/admin/intent-monitoring`
**Purpose**: Monitor intent enforcement middleware status and configuration
**Authentication**: None (admin endpoints, configure auth as needed)
**Response Format**: JSON

#### Example Request

```bash
curl http://localhost:8001/api/admin/intent-monitoring
```

#### Example Response

```json
{
  "middleware_active": true,
  "nl_endpoints": [
    "/api/v1/intent",
    "/api/standup",
    "/api/chat",
    "/api/message"
  ],
  "exempt_paths": [
    "/health",
    "/metrics",
    "/docs",
    "/openapi.json",
    "/static",
    "/api/v1/personality/enhance",
    "/api/v1/personality/profile",
    "/api/v1/workflows",
    "/debug-markdown",
    "/personality-preferences",
    "/standup",
    "/"
  ],
  "monitoring": "All requests logged",
  "principle": "User INPUT → intent classification (enforced)"
}
```

#### Response Fields

| Field               | Type    | Description                                     |
| ------------------- | ------- | ----------------------------------------------- |
| `middleware_active` | boolean | Whether intent enforcement middleware is active |
| `nl_endpoints`      | array   | Endpoints that require intent classification    |
| `exempt_paths`      | array   | Paths exempt from intent enforcement            |
| `monitoring`        | string  | Monitoring status description                   |
| `principle`         | string  | Core enforcement principle                      |

### 2. Intent Cache Metrics

**Endpoint**: `GET /api/admin/intent-cache-metrics`
**Purpose**: Monitor intent classification cache performance
**Response Format**: JSON

#### Example Request

```bash
curl http://localhost:8001/api/admin/intent-cache-metrics
```

#### Example Response (Cache Enabled)

```json
{
  "cache_enabled": true,
  "metrics": {
    "hit_rate": 0.846,
    "hits": 7530,
    "misses": 1371,
    "total_requests": 8901,
    "speedup": 7.6,
    "avg_cached_time": 0.1,
    "avg_uncached_time": 2700,
    "cache_size": 1024,
    "ttl_seconds": 3600
  },
  "status": "operational"
}
```

#### Example Response (Cache Disabled)

```json
{
  "cache_enabled": false,
  "status": "not_configured"
}
```

#### Cache Metrics Fields

| Field               | Type    | Description                                      |
| ------------------- | ------- | ------------------------------------------------ |
| `cache_enabled`     | boolean | Whether intent caching is active                 |
| `hit_rate`          | float   | Cache hit rate (0.0-1.0)                         |
| `hits`              | integer | Number of cache hits                             |
| `misses`            | integer | Number of cache misses                           |
| `total_requests`    | integer | Total classification requests                    |
| `speedup`           | float   | Performance improvement from caching             |
| `avg_cached_time`   | float   | Average response time for cached requests (ms)   |
| `avg_uncached_time` | float   | Average response time for uncached requests (ms) |
| `cache_size`        | integer | Current cache size                               |
| `ttl_seconds`       | integer | Cache time-to-live in seconds                    |

### 3. Intent Cache Management

**Endpoint**: `POST /api/admin/intent-cache-clear`
**Purpose**: Clear intent cache and reset metrics (admin operation)
**Response Format**: JSON

#### Example Request

```bash
curl -X POST http://localhost:8001/api/admin/intent-cache-clear
```

#### Example Response

```json
{
  "status": "cache_cleared",
  "message": "Intent cache cleared successfully",
  "timestamp": "2025-10-06T22:15:00.000000"
}
```

---

## Usage Examples

### Basic Health Check

Monitor overall intent system health:

```bash
#!/bin/bash
# check-intent-health.sh

echo "=== Intent System Health Check ==="

# Check middleware status
MONITORING=$(curl -s http://localhost:8001/api/admin/intent-monitoring)
MIDDLEWARE_ACTIVE=$(echo $MONITORING | jq -r '.middleware_active')

if [ "$MIDDLEWARE_ACTIVE" = "true" ]; then
    echo "✅ Intent enforcement middleware: ACTIVE"
else
    echo "❌ Intent enforcement middleware: INACTIVE"
    exit 1
fi

# Check cache status
CACHE=$(curl -s http://localhost:8001/api/admin/intent-cache-metrics)
CACHE_ENABLED=$(echo $CACHE | jq -r '.cache_enabled')

if [ "$CACHE_ENABLED" = "true" ]; then
    HIT_RATE=$(echo $CACHE | jq -r '.metrics.hit_rate * 100')
    echo "✅ Intent cache: ENABLED (${HIT_RATE}% hit rate)"

    # Alert if hit rate is low
    if (( $(echo "$HIT_RATE < 70" | bc -l) )); then
        echo "⚠️ WARNING: Cache hit rate below 70% threshold"
    fi
else
    echo "ℹ️ Intent cache: DISABLED"
fi

echo "✅ Intent system health check complete"
```

### Performance Monitoring

Track cache performance over time:

```bash
#!/bin/bash
# monitor-cache-performance.sh

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    METRICS=$(curl -s http://localhost:8001/api/admin/intent-cache-metrics)

    if [ "$(echo $METRICS | jq -r '.cache_enabled')" = "true" ]; then
        HIT_RATE=$(echo $METRICS | jq -r '.metrics.hit_rate * 100')
        SPEEDUP=$(echo $METRICS | jq -r '.metrics.speedup')
        TOTAL=$(echo $METRICS | jq -r '.metrics.total_requests')

        echo "$TIMESTAMP - Hit Rate: ${HIT_RATE}%, Speedup: ${SPEEDUP}x, Total: $TOTAL"
    else
        echo "$TIMESTAMP - Cache disabled"
    fi

    sleep 60  # Check every minute
done
```

### Security Monitoring

Monitor for bypass attempts and security issues:

```bash
#!/bin/bash
# security-monitor.sh

echo "=== Intent Security Monitoring ==="

# Get current configuration
CONFIG=$(curl -s http://localhost:8001/api/admin/intent-monitoring)

# Check if middleware is active
MIDDLEWARE_ACTIVE=$(echo $CONFIG | jq -r '.middleware_active')
if [ "$MIDDLEWARE_ACTIVE" != "true" ]; then
    echo "🚨 SECURITY ALERT: Intent enforcement middleware is INACTIVE"
    exit 1
fi

# List protected endpoints
echo "Protected endpoints (require intent classification):"
echo $CONFIG | jq -r '.nl_endpoints[]' | while read endpoint; do
    echo "  🔒 $endpoint"
done

# List exempt paths
echo ""
echo "Exempt paths (bypass allowed):"
echo $CONFIG | jq -r '.exempt_paths[]' | while read path; do
    echo "  ✅ $path"
done

echo ""
echo "✅ Security configuration verified"
```

### Prometheus Integration

Export metrics for Prometheus monitoring:

```bash
#!/bin/bash
# prometheus-exporter.sh

# Fetch monitoring data
MONITORING=$(curl -s http://localhost:8001/api/admin/intent-monitoring)
CACHE=$(curl -s http://localhost:8001/api/admin/intent-cache-metrics)

echo "# HELP intent_middleware_active Intent enforcement middleware status"
echo "# TYPE intent_middleware_active gauge"
ACTIVE=$(echo $MONITORING | jq -r '.middleware_active')
if [ "$ACTIVE" = "true" ]; then
    echo "intent_middleware_active 1"
else
    echo "intent_middleware_active 0"
fi

echo ""
echo "# HELP intent_protected_endpoints Number of protected endpoints"
echo "# TYPE intent_protected_endpoints gauge"
PROTECTED_COUNT=$(echo $MONITORING | jq '.nl_endpoints | length')
echo "intent_protected_endpoints $PROTECTED_COUNT"

echo ""
echo "# HELP intent_exempt_paths Number of exempt paths"
echo "# TYPE intent_exempt_paths gauge"
EXEMPT_COUNT=$(echo $MONITORING | jq '.exempt_paths | length')
echo "intent_exempt_paths $EXEMPT_COUNT"

# Cache metrics (if enabled)
if [ "$(echo $CACHE | jq -r '.cache_enabled')" = "true" ]; then
    echo ""
    echo "# HELP intent_cache_hit_rate Cache hit rate"
    echo "# TYPE intent_cache_hit_rate gauge"
    echo "intent_cache_hit_rate $(echo $CACHE | jq -r '.metrics.hit_rate')"

    echo ""
    echo "# HELP intent_cache_total_requests Total cache requests"
    echo "# TYPE intent_cache_total_requests counter"
    echo "intent_cache_total_requests $(echo $CACHE | jq -r '.metrics.total_requests')"

    echo ""
    echo "# HELP intent_cache_speedup Cache performance speedup"
    echo "# TYPE intent_cache_speedup gauge"
    echo "intent_cache_speedup $(echo $CACHE | jq -r '.metrics.speedup')"
fi
```

### Grafana Dashboard Queries

If using Grafana with Prometheus, use these queries:

**Panel 1: Middleware Status**

```
intent_middleware_active
```

**Panel 2: Cache Hit Rate**

```
intent_cache_hit_rate * 100
```

**Panel 3: Cache Performance**

```
intent_cache_speedup
```

**Panel 4: Protected Endpoints**

```
intent_protected_endpoints
```

---

## Integration with Monitoring Tools

### Datadog Integration

```python
#!/usr/bin/env python3
# datadog-integration.py

import requests
import time
from datadog import initialize, statsd

# Initialize Datadog
options = {
    'api_key': 'your_api_key',
    'app_key': 'your_app_key'
}
initialize(**options)

def collect_and_send_metrics():
    """Collect intent metrics and send to Datadog."""

    # Fetch monitoring data
    monitoring_response = requests.get('http://localhost:8001/api/admin/intent-monitoring')
    cache_response = requests.get('http://localhost:8001/api/admin/intent-cache-metrics')

    if monitoring_response.status_code == 200:
        monitoring_data = monitoring_response.json()

        # Send middleware status
        middleware_active = 1 if monitoring_data['middleware_active'] else 0
        statsd.gauge('intent.middleware.active', middleware_active)

        # Send endpoint counts
        statsd.gauge('intent.endpoints.protected', len(monitoring_data['nl_endpoints']))
        statsd.gauge('intent.endpoints.exempt', len(monitoring_data['exempt_paths']))

    if cache_response.status_code == 200:
        cache_data = cache_response.json()

        if cache_data['cache_enabled']:
            metrics = cache_data['metrics']

            # Send cache metrics
            statsd.gauge('intent.cache.hit_rate', metrics['hit_rate'])
            statsd.gauge('intent.cache.speedup', metrics['speedup'])
            statsd.gauge('intent.cache.size', metrics.get('cache_size', 0))

            # Send counters
            statsd.increment('intent.cache.hits', metrics['hits'])
            statsd.increment('intent.cache.misses', metrics['misses'])

if __name__ == '__main__':
    while True:
        try:
            collect_and_send_metrics()
            print(f"Metrics sent to Datadog at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error sending metrics: {e}")

        time.sleep(60)  # Send metrics every minute
```

### New Relic Integration

```python
#!/usr/bin/env python3
# newrelic-integration.py

import requests
import time
import newrelic.agent

@newrelic.agent.background_task()
def collect_intent_metrics():
    """Collect and report intent metrics to New Relic."""

    try:
        # Fetch monitoring data
        monitoring_response = requests.get('http://localhost:8001/api/admin/intent-monitoring')
        cache_response = requests.get('http://localhost:8001/api/admin/intent-cache-metrics')

        if monitoring_response.status_code == 200:
            monitoring_data = monitoring_response.json()

            # Record middleware status
            middleware_active = 1 if monitoring_data['middleware_active'] else 0
            newrelic.agent.record_custom_metric('Intent/Middleware/Active', middleware_active)

            # Record endpoint counts
            newrelic.agent.record_custom_metric('Intent/Endpoints/Protected', len(monitoring_data['nl_endpoints']))
            newrelic.agent.record_custom_metric('Intent/Endpoints/Exempt', len(monitoring_data['exempt_paths']))

        if cache_response.status_code == 200:
            cache_data = cache_response.json()

            if cache_data['cache_enabled']:
                metrics = cache_data['metrics']

                # Record cache performance
                newrelic.agent.record_custom_metric('Intent/Cache/HitRate', metrics['hit_rate'])
                newrelic.agent.record_custom_metric('Intent/Cache/Speedup', metrics['speedup'])
                newrelic.agent.record_custom_metric('Intent/Cache/TotalRequests', metrics['total_requests'])

    except Exception as e:
        newrelic.agent.record_custom_metric('Intent/Monitoring/Errors', 1)
        print(f"Error collecting metrics: {e}")

if __name__ == '__main__':
    newrelic.agent.initialize('newrelic.ini')

    while True:
        collect_intent_metrics()
        time.sleep(300)  # Collect every 5 minutes
```

---

## Alert Thresholds

Recommended alert thresholds for production monitoring:

| Metric              | Warning | Critical | Description                    |
| ------------------- | ------- | -------- | ------------------------------ |
| Middleware Active   | false   | false    | Intent enforcement disabled    |
| Cache Hit Rate      | <70%    | <60%     | Poor cache performance         |
| Cache Speedup       | <3x     | <2x      | Cache not providing benefit    |
| Protected Endpoints | Changes | Changes  | Security configuration changed |
| Exempt Paths        | Changes | Changes  | Security configuration changed |

### Example Alert Scripts

**Middleware Down Alert**:

```bash
#!/bin/bash
# alert-middleware-down.sh

ACTIVE=$(curl -s http://localhost:8001/api/admin/intent-monitoring | jq -r '.middleware_active')

if [ "$ACTIVE" != "true" ]; then
    echo "🚨 CRITICAL: Intent enforcement middleware is DOWN"
    # Send alert (email, Slack, PagerDuty, etc.)
    exit 1
fi
```

**Cache Performance Alert**:

```bash
#!/bin/bash
# alert-cache-performance.sh

CACHE=$(curl -s http://localhost:8001/api/admin/intent-cache-metrics)
ENABLED=$(echo $CACHE | jq -r '.cache_enabled')

if [ "$ENABLED" = "true" ]; then
    HIT_RATE=$(echo $CACHE | jq -r '.metrics.hit_rate * 100')

    if (( $(echo "$HIT_RATE < 60" | bc -l) )); then
        echo "🚨 CRITICAL: Cache hit rate is ${HIT_RATE}% (below 60% threshold)"
        exit 1
    elif (( $(echo "$HIT_RATE < 70" | bc -l) )); then
        echo "⚠️ WARNING: Cache hit rate is ${HIT_RATE}% (below 70% threshold)"
        exit 1
    fi
fi
```

---

## Troubleshooting

### Common Issues

#### Endpoints Return 404

**Issue**: Monitoring endpoints not found
**Cause**: Web app not running or endpoints not registered
**Solution**:

```bash
# Check if web app is running
curl -I http://localhost:8001/health

# Check if endpoints are registered
curl -I http://localhost:8001/api/admin/intent-monitoring
```

#### No Cache Data

**Issue**: Cache metrics show `"cache_enabled": false`
**Cause**: Intent service not properly initialized or cache not configured
**Solution**:

1. Verify intent service is running
2. Check that cache is enabled in configuration
3. Ensure requests are being processed through intent service

#### Stale Monitoring Data

**Issue**: Metrics don't update or show old data
**Cause**: Middleware not processing requests or service not running
**Solution**:

1. Send test requests through intent endpoints
2. Verify middleware is active: `middleware_active: true`
3. Check application logs for errors

### Debugging Commands

```bash
# Test intent enforcement is working
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "test intent classification"}'

# Check middleware configuration
curl http://localhost:8001/api/admin/intent-monitoring | jq '.middleware_active'

# Monitor cache in real-time
watch -n 5 'curl -s http://localhost:8001/api/admin/intent-cache-metrics | jq ".metrics.hit_rate"'

# Clear cache if needed
curl -X POST http://localhost:8001/api/admin/intent-cache-clear
```

---

## Security Considerations

**⚠️ Warning**: These endpoints expose system metrics without authentication by default.

### Recommendations

1. **Add Authentication**: Protect `/api/admin/*` endpoints with API keys or authentication
2. **Network Security**: Restrict access via firewall rules
3. **Monitoring Access**: Log access to monitoring endpoints
4. **Rate Limiting**: Implement rate limiting for monitoring endpoints

### Example Authentication

```python
# Add to web/app.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_admin_token(token: str = Depends(security)):
    """Verify admin API token."""
    if token.credentials != os.getenv("ADMIN_API_TOKEN"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token"
        )
    return token

@app.get("/api/admin/intent-monitoring")
async def intent_monitoring(token: str = Depends(verify_admin_token)):
    """Protected monitoring endpoint."""
    return IntentEnforcementMiddleware.get_monitoring_status()
```

---

## Related Documentation

- [Intent System Architecture](../guides/execution-analysis-handlers.md)
- [Intent Enforcement Middleware](../internal/architecture/adrs/adr-032-intent-classification-universal-entry.md)
- [Operational Guide](./operational-guide.md)
- [Rollback Plan](./intent-rollback-plan.md)

---

## Appendix

### Complete Monitoring Script

```bash
#!/bin/bash
# complete-intent-monitor.sh
# Comprehensive intent system monitoring script

set -e

BASE_URL="http://localhost:8001"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== Intent System Monitoring Report ==="
echo "Timestamp: $TIMESTAMP"
echo "Base URL: $BASE_URL"
echo ""

# 1. Health Check
echo "1. System Health:"
HEALTH=$(curl -s $BASE_URL/health)
if [ $? -eq 0 ]; then
    echo "   ✅ Web service: HEALTHY"
else
    echo "   ❌ Web service: DOWN"
    exit 1
fi

# 2. Middleware Status
echo ""
echo "2. Intent Enforcement:"
MONITORING=$(curl -s $BASE_URL/api/admin/intent-monitoring)
MIDDLEWARE_ACTIVE=$(echo $MONITORING | jq -r '.middleware_active')

if [ "$MIDDLEWARE_ACTIVE" = "true" ]; then
    echo "   ✅ Middleware: ACTIVE"

    # Show protected endpoints
    PROTECTED_COUNT=$(echo $MONITORING | jq '.nl_endpoints | length')
    echo "   📊 Protected endpoints: $PROTECTED_COUNT"

    # Show exempt paths
    EXEMPT_COUNT=$(echo $MONITORING | jq '.exempt_paths | length')
    echo "   📊 Exempt paths: $EXEMPT_COUNT"
else
    echo "   ❌ Middleware: INACTIVE"
fi

# 3. Cache Performance
echo ""
echo "3. Cache Performance:"
CACHE=$(curl -s $BASE_URL/api/admin/intent-cache-metrics)
CACHE_ENABLED=$(echo $CACHE | jq -r '.cache_enabled')

if [ "$CACHE_ENABLED" = "true" ]; then
    HIT_RATE=$(echo $CACHE | jq -r '.metrics.hit_rate * 100')
    SPEEDUP=$(echo $CACHE | jq -r '.metrics.speedup')
    TOTAL=$(echo $CACHE | jq -r '.metrics.total_requests')

    echo "   ✅ Cache: ENABLED"
    echo "   📊 Hit rate: ${HIT_RATE}%"
    echo "   📊 Speedup: ${SPEEDUP}x"
    echo "   📊 Total requests: $TOTAL"

    # Performance alerts
    if (( $(echo "$HIT_RATE < 60" | bc -l) )); then
        echo "   🚨 CRITICAL: Hit rate below 60%"
    elif (( $(echo "$HIT_RATE < 70" | bc -l) )); then
        echo "   ⚠️ WARNING: Hit rate below 70%"
    fi
else
    echo "   ℹ️ Cache: DISABLED"
fi

echo ""
echo "=== Monitoring Complete ==="
```

---

**Document Status**: ✅ Production Ready
**Endpoints Validated**: October 6, 2025
**Last Updated**: October 6, 2025
**GREAT-4E-2 Phase 4**: Monitoring Dashboard (API Documentation Approach)
