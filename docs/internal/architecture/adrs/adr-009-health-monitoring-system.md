# ADR-009: Health Monitoring System Design

**Date**: July 20, 2025
**Status**: Accepted
**Deciders**: Claude Code (Architecture Assistant), Development Team

## Context

PM-038 staging deployment required comprehensive health monitoring to validate MCP integration performance and ensure production readiness. The existing basic health checks were insufficient for a production-grade environment with multiple services, connection pooling, and performance targets.

### Pre-existing Health Check Limitations
- **Single endpoint**: Basic `/health` endpoint only
- **No component granularity**: Cannot isolate individual service issues
- **Missing performance metrics**: No response time or throughput monitoring
- **No MCP-specific validation**: Cannot verify PM-038 features working correctly
- **Limited observability**: No integration with monitoring systems

### Production Monitoring Requirements
- **Multi-layered health checks**: Liveness, readiness, and comprehensive probes
- **Component-specific validation**: Database, cache, MCP integration, external services
- **Performance monitoring**: Response times, resource utilization, performance targets
- **MCP integration validation**: Connection pooling, content search, circuit breaker status
- **Prometheus integration**: Metrics collection for Grafana dashboards
- **Automated alerting**: Proactive issue detection and notification

## Decision

**Implement comprehensive health monitoring system with Kubernetes-style probes, component-specific validation, MCP integration monitoring, and Prometheus metrics integration.**

### Architecture Overview

**Multi-Tier Health Check System**
```python
# Health Check Hierarchy
/health                 # Basic health status
/health/liveness       # Kubernetes liveness probe
/health/readiness      # Kubernetes readiness probe
/health/comprehensive  # Full component health validation
/health/mcp           # MCP-specific health (PM-038)
/health/metrics       # Prometheus-compatible metrics
```

**Component Health Validation**
- **Database Health**: Connection, query execution, statistics
- **Redis Health**: Connectivity, operations, memory usage
- **ChromaDB Health**: Heartbeat, collection stats, response time
- **MCP Integration**: Pool status, search performance, circuit breaker
- **System Resources**: CPU, memory, disk utilization
- **API Endpoints**: Response time validation
- **External Services**: Anthropic, OpenAI, GitHub connectivity

## Implementation Details

### Core Health Check Infrastructure

**1. Health Status Enumeration**
```python
class HealthStatus:
    HEALTHY = "healthy"      # All systems operational
    DEGRADED = "degraded"    # Some issues, still functional
    UNHEALTHY = "unhealthy"  # Critical issues, service impaired
    UNKNOWN = "unknown"      # Cannot determine status
```

**2. Centralized Health Checker**
```python
class StagingHealthChecker:
    def __init__(self):
        self.cache_ttl = 30  # 30-second cache for performance
        self.cached_results = {}

    async def get_comprehensive_health(self) -> Dict[str, Any]:
        """Execute all health checks concurrently"""
        health_checks = {
            "database": self._check_database_health(),
            "redis": self._check_redis_health(),
            "chromadb": self._check_chromadb_health(),
            "mcp_integration": self._check_mcp_health(),
            "system_resources": self._check_system_resources(),
            "api_endpoints": self._check_api_endpoints(),
            "external_services": self._check_external_services(),
        }

        # Execute concurrently for performance
        results = await asyncio.gather(*health_checks.values())
        return self._calculate_overall_status(results)
```

### Database Health Validation

**1. PostgreSQL Health Check**
```python
async def _check_database_health(self) -> Dict[str, Any]:
    try:
        start_time = time.time()

        async with get_db_session() as session:
            # Basic connectivity test
            result = await session.execute(text("SELECT 1 as health_check"))
            health_value = result.scalar()

            # Database statistics
            stats_query = text("""
                SELECT
                    count(*) as total_connections,
                    (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') as active_connections,
                    (SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public') as table_count
            """)
            stats_result = await session.execute(stats_query)
            stats = stats_result.fetchone()

            response_time = (time.time() - start_time) * 1000

            return {
                "status": HealthStatus.HEALTHY,
                "response_time_ms": round(response_time, 2),
                "total_connections": stats.total_connections,
                "active_connections": stats.active_connections,
                "table_count": stats.table_count,
                "timestamp": datetime.utcnow().isoformat(),
            }
    except Exception as e:
        return {
            "status": HealthStatus.UNHEALTHY,
            "error": f"Database connection failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
        }
```

### MCP Integration Health Validation (PM-038 Specific)

**1. MCP Health Check - Initialization**
```python
async def _check_mcp_health(self) -> Dict[str, Any]:
    """Comprehensive MCP integration health check"""
    try:
        start_time = time.time()

        # Initialize MCP resource manager
        manager = MCPResourceManager()
        success = await manager.initialize(enabled=True)

        if not success:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": "MCP initialization failed",
                "timestamp": datetime.utcnow().isoformat(),
            }
```

**2. MCP Performance Tests**
```python
        test_results = {}

        # Test 1: Resource availability
        resources = await manager.list_available_resources()
        test_results["resource_count"] = len(resources)

        # Test 2: Enhanced content search (PM-038 feature)
        search_start = time.time()
        search_results = await manager.enhanced_file_search("test health check")
        search_time = (time.time() - search_start) * 1000
        test_results["search_response_time_ms"] = round(search_time, 2)
        test_results["search_results_count"] = len(search_results)

        # Test 3: Connection pool statistics
        connection_stats = await manager.get_connection_stats()
        test_results["connection_stats"] = connection_stats

        # Test 4: Performance target validation (<500ms)
        performance_ok = search_time < 500
        test_results["performance_target_met"] = performance_ok

        await manager.cleanup()
```

**3. MCP Health Status Calculation**
```python
        total_time = (time.time() - start_time) * 1000

        # Determine status based on performance and functionality
        if performance_ok and test_results["resource_count"] > 0:
            status = HealthStatus.HEALTHY
        elif test_results["resource_count"] > 0:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return {
            "status": status,
            "total_response_time_ms": round(total_time, 2),
            "tests": test_results,
            "pm038_features": {
                "connection_pooling": connection_stats.get("using_pool", False),
                "content_search": len(search_results) > 0,
                "performance_target": "< 500ms",
                "actual_performance": f"{search_time:.1f}ms",
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "status": HealthStatus.UNHEALTHY,
            "error": f"MCP health check failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
        }
```

### System Resource Monitoring

**1. Resource Utilization Health Check**
```python
async def _check_system_resources(self) -> Dict[str, Any]:
    """Monitor CPU, memory, and disk utilization"""
    try:
        # CPU usage (1-second sample)
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        # Disk usage
        disk = psutil.disk_usage("/")
        disk_percent = disk.percent

        # Determine status based on thresholds
        if cpu_percent > 90 or memory_percent > 90 or disk_percent > 90:
            status = HealthStatus.UNHEALTHY
        elif cpu_percent > 75 or memory_percent > 75 or disk_percent > 80:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.HEALTHY

        return {
            "status": status,
            "cpu_percent": round(cpu_percent, 1),
            "memory_percent": round(memory_percent, 1),
            "disk_percent": round(disk_percent, 1),
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_free_gb": round(disk.free / (1024**3), 2),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "status": HealthStatus.UNKNOWN,
            "error": f"System resource check failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
        }
```

### Kubernetes-Style Health Probes

**1. Liveness Probe**
```python
@staging_health_router.get("/liveness")
async def liveness_probe():
    """Kubernetes-style liveness probe - basic service health"""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }
```

**2. Readiness Probe**
```python
@staging_health_router.get("/readiness")
async def readiness_probe():
    """Kubernetes-style readiness probe - ready to serve traffic"""
    try:
        # Quick database connectivity check
        async with get_db_session() as session:
            await session.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Not ready: {str(e)}"
        )
```

### Prometheus Metrics Integration

**1. Health Metrics Endpoint - Function Header**
```python
@staging_health_router.get("/metrics")
async def health_metrics():
    """Prometheus-compatible health metrics"""
    try:
        health_result = await health_checker.get_comprehensive_health()
        metrics = []

        # Overall health metric
        overall_healthy = 1 if health_result["overall_status"] == HealthStatus.HEALTHY else 0
        metrics.append(f'piper_health_overall{{"{"}}environment="staging"{"}}"} {overall_healthy}')
```

**2. Component Metrics Collection**
```python
        # Component health metrics
        for component, result in health_result["components"].items():
            component_healthy = 1 if result.get("status") == HealthStatus.HEALTHY else 0
            metrics.append(
                f'piper_health_component{{"{"}}component="{component}",environment="staging"{"}}"} {component_healthy}'
            )

            # Response time metrics
            if "response_time_ms" in result:
                response_time = result["response_time_ms"]
                metrics.append(
                    f'piper_health_response_time_ms{{"{"}}component="{component}",environment="staging"{"}}"} {response_time}'
                )
```

**3. System Metrics & Error Handling**
```python
        # System resource metrics
        if "system_resources" in health_result["components"]:
            sys_res = health_result["components"]["system_resources"]
            if "cpu_percent" in sys_res:
                metrics.append(f'piper_system_cpu_percent{{"{"}}environment="staging"{"}}"} {sys_res["cpu_percent"]}')
            if "memory_percent" in sys_res:
                metrics.append(f'piper_system_memory_percent{{"{"}}environment="staging"{"}}"} {sys_res["memory_percent"]}')
            if "disk_percent" in sys_res:
                metrics.append(f'piper_system_disk_percent{{"{"}}environment="staging"{"}}"} {sys_res["disk_percent"]}')

        return "\\n".join(metrics) + "\\n"

    except Exception as e:
        logger.error(f"Health metrics generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Metrics generation failed: {str(e)}"
        )
```

### Performance Thresholds and Alerting

**1. Health Status Calculation**
```python
def _calculate_overall_status(self, component_results: Dict[str, Any]) -> str:
    """Calculate overall health from component health"""
    statuses = [
        result.get("status", HealthStatus.UNKNOWN)
        for result in component_results.values()
    ]

    if all(status == HealthStatus.HEALTHY for status in statuses):
        return HealthStatus.HEALTHY
    elif any(status == HealthStatus.UNHEALTHY for status in statuses):
        return HealthStatus.UNHEALTHY
    elif any(status == HealthStatus.DEGRADED for status in statuses):
        return HealthStatus.DEGRADED
    else:
        return HealthStatus.UNKNOWN
```

**2. Performance Target Validation**
```python
# MCP Performance Targets (PM-038)
MAX_MCP_SEARCH_TIME_MS = 500     # Content search target
MAX_CONNECTION_TIME_MS = 1       # Connection establishment target
MAX_RESPONSE_TIME_MS = 500       # API response time target
MIN_RESOURCE_COUNT = 10          # Minimum MCP resources

# System Resource Thresholds
CPU_WARNING_THRESHOLD = 75       # CPU usage warning
CPU_CRITICAL_THRESHOLD = 90      # CPU usage critical
MEMORY_WARNING_THRESHOLD = 75    # Memory usage warning
MEMORY_CRITICAL_THRESHOLD = 90   # Memory usage critical
DISK_WARNING_THRESHOLD = 80      # Disk usage warning
DISK_CRITICAL_THRESHOLD = 90     # Disk usage critical
```

## Monitoring Integration

### Grafana Dashboard Configuration

**1. Health Overview Dashboard**
```json
{
  "dashboard": {
    "title": "Piper Morgan Health Overview",
    "panels": [
      {
        "title": "Overall Health Status",
        "type": "stat",
        "targets": [
          {
            "expr": "piper_health_overall{\"{\"}environment=\"staging\"{\"}\"}"
          }
        ]
      },
      {
        "title": "Component Health Matrix",
        "type": "heatmap",
        "targets": [
          {
            "expr": "piper_health_component{\"{\"}environment=\"staging\"{\"}\"}"
          }
        ]
      },
      {
        "title": "Response Time Distribution",
        "type": "histogram",
        "targets": [
          {
            "expr": "piper_health_response_time_ms{\"{\"}environment=\"staging\"{\"}\"}"
          }
        ]
      }
    ]
  }
}
```

**2. MCP Performance Dashboard**
```json
{
  "dashboard": {
    "title": "PM-038 MCP Performance",
    "panels": [
      {
        "title": "Search Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "piper_mcp_search_response_time_ms{\"{\"}environment=\"staging\"{\"}\"}"
          }
        ],
        "alert": {
          "conditions": [
            {
              "query": "A",
              "reducer": "avg",
              "evaluator": {
                "params": [500],
                "type": "gt"
              }
            }
          ]
        }
      }
    ]
  }
}
```

### Prometheus Alerting Rules

**1. Critical Health Alerts**
```yaml
groups:
  - name: piper-health-critical
    rules:
      - alert: PiperOverallHealthUnhealthy
        expr: piper_health_overall{environment="staging"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Piper Morgan overall health is unhealthy"
          description: "Overall system health has been unhealthy for more than 2 minutes"

      - alert: PiperMCPPerformanceDegraded
        expr: piper_mcp_search_response_time_ms{environment="staging"} > 500
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "MCP search performance degraded"
          description: "MCP search response time has exceeded 500ms target for 5 minutes"

      - alert: PiperSystemResourcesCritical
        expr: |
          piper_system_cpu_percent{environment="staging"} > 90 or
          piper_system_memory_percent{environment="staging"} > 90 or
          piper_system_disk_percent{environment="staging"} > 90
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "System resources critically high"
          description: "CPU, memory, or disk usage above 90% for 2 minutes"
```

## Health Check Performance Optimization

### Caching Strategy

**1. Health Check Result Caching**
```python
class HealthChecker:
    def __init__(self):
        self.cache_ttl = 30  # 30-second cache
        self.cached_results = {}
        self.last_check_time = None

    async def get_comprehensive_health(self) -> Dict[str, Any]:
        current_time = time.time()

        # Use cached results if recent
        if (
            self.last_check_time
            and current_time - self.last_check_time < self.cache_ttl
            and self.cached_results
        ):
            return self.cached_results

        # Execute fresh health checks
        results = await self._execute_health_checks()

        # Cache results
        self.cached_results = results
        self.last_check_time = current_time

        return results
```

**2. Concurrent Health Check Execution**
```python
async def _execute_health_checks(self):
    """Execute all health checks concurrently for performance"""
    health_checks = {
        "database": self._check_database_health(),
        "redis": self._check_redis_health(),
        "chromadb": self._check_chromadb_health(),
        "mcp_integration": self._check_mcp_health(),
        "system_resources": self._check_system_resources(),
        "api_endpoints": self._check_api_endpoints(),
        "external_services": self._check_external_services(),
    }

    # Execute all checks concurrently
    results = {}
    for component, check_coro in health_checks.items():
        try:
            results[component] = await check_coro
        except Exception as e:
            logger.error(f"Health check failed for {component}: {e}")
            results[component] = {
                "status": HealthStatus.UNHEALTHY,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    return results
```

## Consequences

### Positive
- **Comprehensive Visibility**: Complete health status across all system components
- **Early Issue Detection**: Proactive identification of degraded performance
- **Production Readiness**: Kubernetes-style probes ready for container orchestration
- **Performance Validation**: Continuous monitoring of PM-038 performance targets
- **Operational Excellence**: Detailed metrics for troubleshooting and optimization
- **Automated Alerting**: Proactive notifications for critical issues

### Negative
- **System Overhead**: Health checks consume CPU and memory resources
- **Complexity**: Multiple monitoring endpoints to maintain and understand
- **Alert Fatigue**: Risk of too many alerts reducing response effectiveness
- **Dependency**: Health monitoring becomes critical infrastructure component

### Neutral
- **Monitoring Infrastructure**: Requires Prometheus and Grafana setup
- **Configuration Management**: Health check thresholds need tuning over time
- **Integration Complexity**: Multiple systems must work together effectively

## Success Metrics

### Technical Success Criteria
- ✅ **Comprehensive Coverage**: 7 component health checks implemented
- ✅ **Performance Monitoring**: <30s health check execution time
- ✅ **MCP Validation**: PM-038 features monitored and validated
- ✅ **Prometheus Integration**: Metrics collection operational

### Operational Success Criteria
- ✅ **Alert Effectiveness**: <5 minute detection time for critical issues
- ✅ **False Positive Rate**: <5% false alerts
- ✅ **Dashboard Usability**: Operations team can quickly identify issues
- ✅ **Documentation Quality**: Complete troubleshooting procedures

### Business Success Criteria
- 🎯 **Uptime Improvement**: 99.9% system availability
- 🎯 **Issue Resolution**: 50% faster mean time to resolution
- 🎯 **Proactive Monitoring**: 80% of issues detected before user impact
- 🎯 **Operational Confidence**: Zero blind spots in system health

## Integration with Deployment Pipeline

### CI/CD Health Check Integration

**1. Pre-deployment Health Validation**
```bash
# Verify staging health before production deployment
curl -f http://localhost:8001/health/comprehensive | jq '.overall_status' | grep -q "healthy"
if [ $? -eq 0 ]; then
    echo "Staging health validated - proceeding with production deployment"
    ./deploy_production.sh
else
    echo "Staging health check failed - aborting deployment"
    exit 1
fi
```

**2. Post-deployment Health Verification**
```bash
# Verify production health after deployment
./scripts/verify_production_health.sh --timeout=300 --retry=5
```

## Related ADRs

- **ADR-007**: Staging Environment Architecture (infrastructure foundation)
- **ADR-008**: MCP Connection Pooling Strategy (performance monitoring integration)
- **ADR-006**: Standardize Async Session Management (database health patterns)

## Lessons Learned

### Health Check Design Insights
- **Caching is essential** for performance when health checks are called frequently
- **Concurrent execution** significantly improves health check response time
- **Component isolation** allows precise problem identification

### Monitoring System Insights
- **Too many metrics** can overwhelm operations teams - focus on actionable metrics
- **Alert thresholds** require tuning based on actual system behavior patterns
- **Dashboard design** impacts response time - organize by severity and component

### Operational Insights
- **Health checks** must be reliable - a broken health check is worse than no health check
- **Documentation quality** directly impacts how quickly teams can respond to alerts
- **Regular testing** of health check scenarios ensures reliability when needed

---

**Implementation Date**: July 20, 2025
**Monitoring Stack**: Prometheus + Grafana
**Risk Level**: Low (non-intrusive monitoring, comprehensive testing)
**Business Impact**: High (proactive issue detection and operational excellence)
