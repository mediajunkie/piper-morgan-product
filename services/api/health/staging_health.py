"""
Comprehensive Health Check System for Staging Environment
Provides detailed health monitoring for all PM-038 components
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import aiohttp
import psutil
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from services.database.session_factory import AsyncSessionFactory
from services.infrastructure.config.mcp_configuration import get_config

logger = logging.getLogger(__name__)

# Health check router for staging
staging_health_router = APIRouter(prefix="/health", tags=["health"])


class HealthStatus:
    """Health status levels"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class StagingHealthChecker:
    """Comprehensive health checker for staging environment"""

    def __init__(self):
        self.last_check_time = None
        self.cached_results = {}
        self.cache_ttl = 30  # 30 seconds

    async def get_comprehensive_health(self) -> Dict[str, Any]:
        """Get comprehensive health status for all components"""
        current_time = time.time()

        # Use cached results if recent
        if (
            self.last_check_time
            and current_time - self.last_check_time < self.cache_ttl
            and self.cached_results
        ):
            return self.cached_results

        health_checks = {
            "database": self._check_database_health(),
            "redis": self._check_redis_health(),
            "chromadb": self._check_chromadb_health(),
            "mcp_integration": self._check_mcp_health(),
            "slack_integration": self._check_slack_integration_health(),
            "system_resources": self._check_system_resources(),
            "api_endpoints": self._check_api_endpoints(),
            "external_services": self._check_external_services(),
        }

        # Execute all health checks concurrently
        results = {}
        for component, check_coro in health_checks.items():
            try:
                results[component] = await check_coro
            except Exception as e:
                logger.error(f"Health check failed for {component}: {e}")
                results[component] = {
                    "status": HealthStatus.UNHEALTHY,
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

        # Calculate overall health
        overall_status = self._calculate_overall_status(results)

        final_result = {
            "overall_status": overall_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": "staging",
            "version": "PM-038-staging",
            "components": results,
            "summary": self._generate_health_summary(results),
        }

        # Cache results
        self.cached_results = final_result
        self.last_check_time = current_time

        return final_result

    async def _check_database_health(self) -> Dict[str, Any]:
        """Check PostgreSQL database health"""
        try:
            start_time = time.time()

            # Test database connection and query
            async with AsyncSessionFactory.session_scope() as session:
                # Basic connectivity test
                result = await session.execute(text("SELECT 1 as health_check"))
                health_value = result.scalar()

                # Check database stats
                stats_query = text(
                    """
                    SELECT
                        count(*) as total_connections,
                        (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') as active_connections,
                        (SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public') as table_count
                """
                )
                stats_result = await session.execute(stats_query)
                stats = stats_result.fetchone()

                response_time = (time.time() - start_time) * 1000  # Convert to ms

                if health_value == 1:
                    return {
                        "status": HealthStatus.HEALTHY,
                        "response_time_ms": round(response_time, 2),
                        "total_connections": stats.total_connections,
                        "active_connections": stats.active_connections,
                        "table_count": stats.table_count,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                else:
                    return {
                        "status": HealthStatus.UNHEALTHY,
                        "error": "Database query returned unexpected result",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"Database connection failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    async def _check_redis_health(self) -> Dict[str, Any]:
        """Check Redis cache health"""
        try:
            import redis.asyncio as redis

            config = get_config()
            redis_url = f"redis://:{config.redis_password}@{config.redis_host}:{config.redis_port}"

            start_time = time.time()
            redis_client = redis.from_url(redis_url)

            # Test basic operations
            await redis_client.ping()
            await redis_client.set("health_check", "ok", ex=60)
            result = await redis_client.get("health_check")

            # Get Redis info
            info = await redis_client.info()
            response_time = (time.time() - start_time) * 1000

            await redis_client.close()

            if result == b"ok":
                return {
                    "status": HealthStatus.HEALTHY,
                    "response_time_ms": round(response_time, 2),
                    "connected_clients": info.get("connected_clients", 0),
                    "used_memory_human": info.get("used_memory_human", "unknown"),
                    "redis_version": info.get("redis_version", "unknown"),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            else:
                return {
                    "status": HealthStatus.UNHEALTHY,
                    "error": "Redis operations failed",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"Redis connection failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    async def _check_chromadb_health(self) -> Dict[str, Any]:
        """Check ChromaDB vector database health"""
        try:
            config = get_config()
            chroma_url = f"http://{config.chroma_host}:{config.chroma_port}"

            start_time = time.time()

            async with aiohttp.ClientSession() as session:
                # Check heartbeat endpoint
                async with session.get(f"{chroma_url}/api/v1/heartbeat") as response:
                    if response.status == 200:
                        heartbeat_data = await response.json()
                        response_time = (time.time() - start_time) * 1000

                        # Get collection stats if available
                        try:
                            async with session.get(
                                f"{chroma_url}/api/v1/collections"
                            ) as collections_response:
                                if collections_response.status == 200:
                                    collections = await collections_response.json()
                                    collection_count = len(collections)
                                else:
                                    collection_count = "unknown"
                        except Exception:
                            collection_count = "unknown"

                        return {
                            "status": HealthStatus.HEALTHY,
                            "response_time_ms": round(response_time, 2),
                            "heartbeat": heartbeat_data,
                            "collection_count": collection_count,
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    else:
                        return {
                            "status": HealthStatus.UNHEALTHY,
                            "error": f"ChromaDB heartbeat failed with status {response.status}",
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"ChromaDB connection failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    async def _check_mcp_health(self) -> Dict[str, Any]:
        """MCP integration health.

        #1436 Tier-3 (Arch-ruled 2026-07-18): the POC MCP stack this check
        exercised (MCPResourceManager -> simulation client) is deleted. The
        REAL connector path is services/mcp/consumer/* — a live health probe
        for it is future work (Family-6 fix, with the MCPConfiguration field
        repair). Until then this reports honestly rather than exercising a
        simulation: not_applicable, never a fabricated "operational".
        """
        return {
            "status": HealthStatus.DEGRADED,
            "note": "POC MCP stack removed (#1436); consumer-path probe not yet wired",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    async def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resource utilization"""
        try:
            # CPU usage
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
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            return {
                "status": HealthStatus.UNKNOWN,
                "error": f"System resource check failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    async def _check_api_endpoints(self) -> Dict[str, Any]:
        """Check critical API endpoints"""
        try:
            endpoints_to_check = [
                "/api/v1/intent",
                "/api/v1/files/search",
                "/health/liveness",
                "/health/readiness",
            ]

            start_time = time.time()
            endpoint_results = {}

            async with aiohttp.ClientSession() as session:
                for endpoint in endpoints_to_check:
                    try:
                        url = f"http://localhost:8001{endpoint}"
                        endpoint_start = time.time()

                        # Use appropriate method for each endpoint
                        if endpoint == "/api/v1/intent":
                            # POST endpoint - test with minimal payload
                            payload = {"message": "health check", "session_id": "health"}
                            async with session.post(url, json=payload) as response:
                                endpoint_time = (time.time() - endpoint_start) * 1000
                                endpoint_results[endpoint] = {
                                    "status_code": response.status,
                                    "response_time_ms": round(endpoint_time, 2),
                                    "healthy": 200 <= response.status < 400,
                                }
                        else:
                            # GET endpoints
                            async with session.get(url) as response:
                                endpoint_time = (time.time() - endpoint_start) * 1000
                                endpoint_results[endpoint] = {
                                    "status_code": response.status,
                                    "response_time_ms": round(endpoint_time, 2),
                                    "healthy": 200 <= response.status < 400,
                                }

                    except Exception as e:
                        endpoint_results[endpoint] = {
                            "status_code": 0,
                            "response_time_ms": 0,
                            "healthy": False,
                            "error": str(e),
                        }

            total_time = (time.time() - start_time) * 1000
            healthy_endpoints = sum(
                1 for result in endpoint_results.values() if result.get("healthy", False)
            )
            total_endpoints = len(endpoints_to_check)

            # Determine overall status
            if healthy_endpoints == total_endpoints:
                status = HealthStatus.HEALTHY
            elif healthy_endpoints > 0:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY

            return {
                "status": status,
                "total_response_time_ms": round(total_time, 2),
                "healthy_endpoints": f"{healthy_endpoints}/{total_endpoints}",
                "endpoints": endpoint_results,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"API endpoint check failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    async def _check_external_services(self) -> Dict[str, Any]:
        """Check external service dependencies"""
        try:
            services = {
                "anthropic": "https://api.anthropic.com/v1/messages",
                "openai": "https://api.openai.com/v1/models",
                "github": "https://api.github.com/rate_limit",
            }

            service_results = {}

            async with aiohttp.ClientSession() as session:
                for service_name, url in services.items():
                    try:
                        start_time = time.time()
                        async with session.get(
                            url, timeout=aiohttp.ClientTimeout(total=10)
                        ) as response:
                            response_time = (time.time() - start_time) * 1000
                            service_results[service_name] = {
                                "status_code": response.status,
                                "response_time_ms": round(response_time, 2),
                                "reachable": True,
                            }
                    except Exception as e:
                        service_results[service_name] = {
                            "status_code": 0,
                            "response_time_ms": 0,
                            "reachable": False,
                            "error": str(e),
                        }

            # Determine status
            reachable_services = sum(
                1 for result in service_results.values() if result.get("reachable", False)
            )
            total_services = len(services)

            if reachable_services == total_services:
                status = HealthStatus.HEALTHY
            elif reachable_services > 0:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY

            return {
                "status": status,
                "reachable_services": f"{reachable_services}/{total_services}",
                "services": service_results,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"External service check failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    async def _check_slack_integration_health(self) -> Dict[str, Any]:
        """
        Comprehensive Slack integration health check.

        Checks Slack token configuration, API connectivity, recent pipeline success rate,
        background task health, and pipeline performance metrics.
        """
        try:
            health_status = {
                "status": HealthStatus.UNKNOWN,
                "checks": {},
                "metrics": {},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            # Import Slack-related modules (lazy import to avoid dependency issues)
            try:
                from services.infrastructure.task_manager import task_manager
                from services.observability.slack_monitor import ACTIVE_PIPELINES, ProcessingStage

                slack_modules_available = True
            except ImportError as e:
                return {
                    "status": HealthStatus.UNHEALTHY,
                    "error": f"Slack monitoring modules not available: {str(e)}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

            # Check 1: Slack token configured
            slack_token = os.getenv("SLACK_BOT_TOKEN")
            health_status["checks"]["slack_token_configured"] = bool(slack_token)

            # Check 2: Can reach Slack API (if token available)
            if slack_token:
                try:
                    async with aiohttp.ClientSession() as session:
                        headers = {"Authorization": f"Bearer {slack_token}"}
                        start_time = time.time()

                        async with session.post(
                            "https://slack.com/api/auth.test",
                            headers=headers,
                            timeout=aiohttp.ClientTimeout(total=10),
                        ) as response:
                            api_response_time = (time.time() - start_time) * 1000

                            if response.status == 200:
                                auth_data = await response.json()
                                health_status["checks"]["slack_api_reachable"] = auth_data.get(
                                    "ok", False
                                )
                                health_status["checks"]["workspace_info"] = {
                                    "team": auth_data.get("team", "unknown"),
                                    "user": auth_data.get("user", "unknown"),
                                    "team_id": auth_data.get("team_id", "unknown"),
                                }
                                health_status["metrics"]["api_response_time_ms"] = round(
                                    api_response_time, 2
                                )
                            else:
                                health_status["checks"]["slack_api_reachable"] = False
                                health_status["checks"]["api_error"] = f"HTTP {response.status}"

                except Exception as e:
                    health_status["checks"]["slack_api_reachable"] = False
                    health_status["checks"]["slack_api_error"] = str(e)
            else:
                health_status["checks"]["slack_api_reachable"] = False
                health_status["checks"]["slack_api_error"] = "No token configured"

            # Check 3: Recent pipeline success rate (last 5 minutes)
            if slack_modules_available:
                cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=5)
                recent_pipelines = [
                    p for p in ACTIVE_PIPELINES.values() if p.started_at >= cutoff_time
                ]

                if recent_pipelines:
                    successful_pipelines = sum(
                        1 for p in recent_pipelines if p.final_status == "success"
                    )
                    failed_pipelines = sum(
                        1 for p in recent_pipelines if p.final_status == "failed"
                    )

                    success_rate = successful_pipelines / len(recent_pipelines)
                    health_status["metrics"]["recent_success_rate"] = round(success_rate, 3)
                    health_status["metrics"]["recent_pipeline_count"] = len(recent_pipelines)
                    health_status["metrics"]["successful_pipelines"] = successful_pipelines
                    health_status["metrics"]["failed_pipelines"] = failed_pipelines

                    # Calculate average processing time for successful pipelines
                    successful_durations = [
                        p.total_duration_ms
                        for p in recent_pipelines
                        if p.total_duration_ms and p.final_status == "success"
                    ]
                    if successful_durations:
                        avg_duration = sum(successful_durations) / len(successful_durations)
                        health_status["metrics"]["avg_processing_time_ms"] = round(avg_duration, 2)

                        # Check if meeting Slack's 3-second timeout requirement
                        health_status["checks"]["meets_slack_timeout"] = avg_duration < 3000
                else:
                    health_status["metrics"]["recent_success_rate"] = None
                    health_status["metrics"]["recent_pipeline_count"] = 0
                    health_status["checks"]["recent_activity"] = False

            # Check 4: Background task health
            if slack_modules_available:
                task_summary = task_manager.get_active_tasks_summary()
                health_status["checks"]["active_background_tasks"] = task_summary["active_tasks"]
                health_status["checks"]["task_success_rate"] = round(
                    task_summary["success_rate"], 3
                )
                health_status["metrics"]["total_tasks_created"] = task_summary[
                    "total_tasks_created"
                ]
                health_status["metrics"]["failed_tasks"] = task_summary["failed_tasks"]

            # Check 5: Stuck pipelines (running > 5 minutes)
            if slack_modules_available:
                stuck_cutoff = datetime.now(timezone.utc) - timedelta(minutes=5)
                stuck_pipelines = [
                    p
                    for p in ACTIVE_PIPELINES.values()
                    if p.started_at < stuck_cutoff and not p.completed_at
                ]
                health_status["checks"]["stuck_pipelines_count"] = len(stuck_pipelines)
                health_status["checks"]["has_stuck_pipelines"] = len(stuck_pipelines) > 0

                if stuck_pipelines:
                    health_status["metrics"]["stuck_pipeline_details"] = [
                        {
                            "correlation_id": p.correlation_id[:12]
                            + "...",  # Truncate for security
                            "duration_minutes": round(
                                (datetime.now(timezone.utc) - p.started_at).total_seconds() / 60, 1
                            ),
                        }
                        for p in stuck_pipelines[:5]  # Limit to 5 for brevity
                    ]

            # Overall health determination
            critical_checks = [
                health_status["checks"].get("slack_token_configured", False),
                health_status["checks"].get("slack_api_reachable", False),
            ]

            performance_checks = [
                health_status["metrics"].get("recent_success_rate", 0) > 0.8,
                not health_status["checks"].get("has_stuck_pipelines", True),
                health_status["checks"].get("task_success_rate", 0) > 0.8,
            ]

            if all(critical_checks):
                if all(performance_checks):
                    health_status["status"] = HealthStatus.HEALTHY
                elif any(performance_checks):
                    health_status["status"] = HealthStatus.DEGRADED
                else:
                    health_status["status"] = HealthStatus.UNHEALTHY
            else:
                health_status["status"] = HealthStatus.UNHEALTHY

            return health_status

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"Slack integration health check failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    def _calculate_overall_status(self, component_results: Dict[str, Any]) -> str:
        """Calculate overall health status from component results"""
        statuses = [
            result.get("status", HealthStatus.UNKNOWN) for result in component_results.values()
        ]

        if all(status == HealthStatus.HEALTHY for status in statuses):
            return HealthStatus.HEALTHY
        elif any(status == HealthStatus.UNHEALTHY for status in statuses):
            return HealthStatus.UNHEALTHY
        elif any(status == HealthStatus.DEGRADED for status in statuses):
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.UNKNOWN

    def _generate_health_summary(self, component_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of health check results"""
        total_components = len(component_results)
        healthy_components = sum(
            1
            for result in component_results.values()
            if result.get("status") == HealthStatus.HEALTHY
        )
        degraded_components = sum(
            1
            for result in component_results.values()
            if result.get("status") == HealthStatus.DEGRADED
        )
        unhealthy_components = sum(
            1
            for result in component_results.values()
            if result.get("status") == HealthStatus.UNHEALTHY
        )

        return {
            "total_components": total_components,
            "healthy_components": healthy_components,
            "degraded_components": degraded_components,
            "unhealthy_components": unhealthy_components,
            "health_percentage": (
                round((healthy_components / total_components) * 100, 1)
                if total_components > 0
                else 0
            ),
        }


# Initialize health checker
health_checker = StagingHealthChecker()


@staging_health_router.get("/")
async def basic_health():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": "staging",
    }


@staging_health_router.get("/liveness")
async def liveness_probe():
    """Kubernetes-style liveness probe"""
    return {"status": "alive", "timestamp": datetime.now(timezone.utc).isoformat()}


@staging_health_router.get("/readiness")
async def readiness_probe():
    """Kubernetes-style readiness probe"""
    try:
        # Quick database connectivity check
        async with AsyncSessionFactory.session_scope() as session:
            await session.execute(text("SELECT 1"))

        return {"status": "ready", "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Not ready: {str(e)}"
        )


@staging_health_router.get("/comprehensive")
async def comprehensive_health():
    """Comprehensive health check for all components"""
    try:
        health_result = await health_checker.get_comprehensive_health()

        # Return appropriate HTTP status based on overall health
        if health_result["overall_status"] == HealthStatus.HEALTHY:
            return health_result
        elif health_result["overall_status"] == HealthStatus.DEGRADED:
            # Still return 200 but indicate degraded performance
            return health_result
        else:
            # Return 503 for unhealthy status
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=health_result
            )

    except Exception as e:
        logger.error(f"Comprehensive health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )


@staging_health_router.get("/mcp")
async def mcp_health():
    """Dedicated MCP health check (PM-038 feature)"""
    try:
        mcp_result = await health_checker._check_mcp_health()

        if mcp_result["status"] == HealthStatus.HEALTHY:
            return mcp_result
        elif mcp_result["status"] == HealthStatus.DEGRADED:
            return mcp_result
        else:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=mcp_result)

    except Exception as e:
        logger.error(f"MCP health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MCP health check failed: {str(e)}",
        )


@staging_health_router.get("/slack")
async def slack_integration_health():
    """Dedicated Slack integration health check (PM-078 TDD feature)"""
    try:
        slack_result = await health_checker._check_slack_integration_health()

        if slack_result["status"] == HealthStatus.HEALTHY:
            return slack_result
        elif slack_result["status"] == HealthStatus.DEGRADED:
            return slack_result
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=slack_result
            )

    except Exception as e:
        logger.error(f"Slack integration health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Slack health check failed: {str(e)}",
        )


@staging_health_router.get("/metrics")
async def health_metrics():
    """Prometheus-compatible health metrics"""
    try:
        health_result = await health_checker.get_comprehensive_health()

        # Convert to Prometheus format
        metrics = []

        # Overall health metric
        overall_healthy = 1 if health_result["overall_status"] == HealthStatus.HEALTHY else 0
        metrics.append(f'piper_health_overall{{environment="staging"}} {overall_healthy}')

        # Component health metrics
        for component, result in health_result["components"].items():
            component_healthy = 1 if result.get("status") == HealthStatus.HEALTHY else 0
            metrics.append(
                f'piper_health_component{{component="{component}",environment="staging"}} {component_healthy}'
            )

            # Response time metrics if available
            if "response_time_ms" in result:
                response_time = result["response_time_ms"]
                metrics.append(
                    f'piper_health_response_time_ms{{component="{component}",environment="staging"}} {response_time}'
                )

        # System resource metrics
        if "system_resources" in health_result["components"]:
            sys_res = health_result["components"]["system_resources"]
            if "cpu_percent" in sys_res:
                metrics.append(
                    f'piper_system_cpu_percent{{environment="staging"}} {sys_res["cpu_percent"]}'
                )
            if "memory_percent" in sys_res:
                metrics.append(
                    f'piper_system_memory_percent{{environment="staging"}} {sys_res["memory_percent"]}'
                )
            if "disk_percent" in sys_res:
                metrics.append(
                    f'piper_system_disk_percent{{environment="staging"}} {sys_res["disk_percent"]}'
                )

        # PM-087: Ethics metrics integration
        # #1019 (Path C): adaptive_learning metrics removed — adaptive_boundaries
        # scaffolding was inert (learned patterns never influenced enforcement).
        try:
            from services.ethics.audit_transparency import audit_transparency_system
            from services.infrastructure.monitoring.ethics_metrics import ethics_metrics

            # Core ethics metrics
            ethics_prometheus_metrics = ethics_metrics.get_prometheus_metrics()
            metrics.extend(ethics_prometheus_metrics)

            # Audit transparency metrics
            transparency_stats = audit_transparency_system.get_transparency_statistics()
            metrics.append(
                f'piper_ethics_transparency_requests{{environment="staging"}} {transparency_stats["transparency_statistics"]["transparency_requests"]}'
            )
            metrics.append(
                f'piper_ethics_audit_entries{{environment="staging"}} {transparency_stats["transparency_statistics"]["total_audit_entries"]}'
            )
            metrics.append(
                f'piper_ethics_redactions_made{{environment="staging"}} {transparency_stats["transparency_statistics"]["redactions_made"]}'
            )

        except ImportError as e:
            logger.warning(f"Ethics metrics not available: {e}")
        except Exception as e:
            logger.error(f"Ethics metrics collection failed: {e}")

        return "\n".join(metrics) + "\n"

    except Exception as e:
        logger.error(f"Health metrics generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Metrics generation failed: {str(e)}",
        )


@staging_health_router.get("/ethics-metrics")
async def ethics_metrics_endpoint():
    """PM-087: Dedicated ethics boundary metrics endpoint.

    #1019 (Path C): adaptive_learning section removed — adaptive_boundaries
    scaffolding was inert and has been deleted.
    """
    try:
        from services.ethics.audit_transparency import audit_transparency_system
        from services.infrastructure.monitoring.ethics_metrics import ethics_metrics

        # Get comprehensive ethics metrics
        ethics_summary = ethics_metrics.get_metrics_summary()

        # Get transparency statistics
        transparency_stats = audit_transparency_system.get_transparency_statistics()

        # Return both Prometheus format and summary
        prometheus_metrics = ethics_metrics.get_prometheus_metrics()

        return {
            "prometheus_metrics": "\n".join(prometheus_metrics) + "\n",
            "summary": ethics_summary,
            "audit_transparency": transparency_stats,
            "phase_3_enhancements": {
                "adaptive_boundaries_active": False,  # #1019: removed Path C
                "audit_transparency_active": True,
                "enhanced_pattern_detection": True,
                "metadata_only_learning": False,  # #1019: pattern-learning removed
                "security_redactions_active": True,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": "staging",
        }

    except ImportError as e:
        logger.warning(f"Ethics metrics module not available: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ethics metrics system not available",
        )
    except Exception as e:
        logger.error(f"Ethics metrics endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ethics metrics failed: {str(e)}",
        )


@staging_health_router.get("/ethics-audit")
async def ethics_audit_endpoint(session_id: Optional[str] = None, hours_back: int = 24):
    """PM-087 Phase 3: User-accessible audit transparency endpoint"""
    try:
        from services.ethics.audit_transparency import audit_transparency_system

        # Get user audit log with security redactions
        audit_log = await audit_transparency_system.get_user_audit_log(
            session_id=session_id, hours_back=hours_back, limit=50
        )

        return audit_log

    except ImportError as e:
        logger.warning(f"Audit transparency module not available: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Audit transparency system not available",
        )
    except Exception as e:
        logger.error(f"Ethics audit endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ethics audit failed: {str(e)}",
        )


@staging_health_router.get("/ethics-summary")
async def ethics_summary_endpoint(session_id: Optional[str] = None):
    """PM-087 Phase 3: High-level ethics summary for users"""
    try:
        from services.ethics.audit_transparency import audit_transparency_system

        # Get audit summary
        summary = await audit_transparency_system.get_audit_summary(session_id=session_id)

        return summary

    except ImportError as e:
        logger.warning(f"Audit transparency module not available: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Audit transparency system not available",
        )
    except Exception as e:
        logger.error(f"Ethics summary endpoint failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ethics summary failed: {str(e)}",
        )


@staging_health_router.get("/ethics-learning")
async def ethics_learning_endpoint():
    """PM-087: adaptive learning system status — DEPRECATED.

    #1019 (Path C, May 2026): adaptive_boundaries scaffolding removed (learned
    patterns never influenced enforcement). Any future learning loop will be
    built on the #1004 semantic-detector substrate under #1016 (LLM-touch
    boundary principle epic). Endpoint retained returning 410 GONE so the
    deprecation is discoverable rather than mysterious.
    """
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail=(
            "Adaptive learning system removed per #1019 Path C. "
            "Future learning loop will be built on semantic-detector confidence under #1016."
        ),
    )
