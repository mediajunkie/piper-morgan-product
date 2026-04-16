"""
Slack Pipeline Monitoring API

Real-time monitoring API endpoints for Slack pipeline status, metrics, and debugging.
Provides comprehensive visibility into pipeline health and performance for the
TDD-based Slack integration system.

This module enables real-time monitoring dashboards and automated health checks
for the bulletproof Slack integration infrastructure.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Monitoring router for Slack pipeline
slack_monitoring_router = APIRouter(prefix="/api/v1/slack", tags=["slack-monitoring"])


class PipelineStatusResponse(BaseModel):
    """Response model for pipeline status"""

    active_pipelines: int
    recent_errors: List[Dict[str, Any]]
    performance_metrics: Dict[str, Any]
    health_status: str
    timestamp: str


class PipelineTraceResponse(BaseModel):
    """Response model for pipeline trace"""

    correlation_id: str
    found: bool
    trace_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


def calculate_avg_duration() -> float:
    """Calculate average duration for recent successful pipelines"""
    try:
        from services.debugging.slack_inspector import SlackPipelineInspector

        stats = SlackPipelineInspector.calculate_success_rate(minutes=60)
        return stats.get("avg_duration_ms", 0.0)
    except ImportError:
        return 0.0
    except Exception as e:
        logger.error(f"Failed to calculate average duration: {e}")
        return 0.0


def calculate_success_rate() -> float:
    """Calculate success rate for recent pipelines"""
    try:
        from services.debugging.slack_inspector import SlackPipelineInspector

        stats = SlackPipelineInspector.calculate_success_rate(minutes=60)
        return stats.get("success_rate", 0.0)
    except ImportError:
        return 0.0
    except Exception as e:
        logger.error(f"Failed to calculate success rate: {e}")
        return 0.0


@slack_monitoring_router.get("/pipelines", response_model=PipelineStatusResponse)
async def get_pipeline_status(
    error_limit: int = Query(10, description="Maximum number of recent errors to return"),
    minutes: int = Query(60, description="Time window for metrics in minutes"),
):
    """
    Get current pipeline status for monitoring dashboard.

    Provides real-time visibility into Slack pipeline health including:
    - Active pipeline count
    - Recent error details
    - Performance metrics (success rate, average duration)
    - Overall health status
    """
    try:
        # Import monitoring modules (lazy import to handle missing dependencies)
        try:
            from services.debugging.slack_inspector import SlackPipelineInspector
            from services.observability.slack_monitor import ACTIVE_PIPELINES

            monitoring_available = True
        except ImportError as e:
            return PipelineStatusResponse(
                active_pipelines=0,
                recent_errors=[{"error": f"Monitoring modules not available: {str(e)}"}],
                performance_metrics={"error": "Monitoring infrastructure not initialized"},
                health_status="unknown",
                timestamp=datetime.now(timezone.utc).isoformat(),
            )

        # Get active pipelines count
        active_count = len(ACTIVE_PIPELINES)

        # Get recent failed pipelines
        inspector = SlackPipelineInspector()
        failed_pipelines = inspector.get_failed_pipelines(minutes=minutes)

        recent_errors = []
        for pipeline in failed_pipelines[-error_limit:]:  # Get most recent errors
            error_info = {
                "correlation_id": pipeline.correlation_id[:12] + "...",  # Truncate for security
                "event_id": pipeline.slack_event_id,
                "error_details": pipeline.error_details,
                "failed_stage": "unknown",
                "duration_ms": pipeline.total_duration_ms,
                "timestamp": pipeline.started_at.isoformat() if pipeline.started_at else None,
            }

            # Find the specific stage that failed
            for stage_enum, stage_metrics in pipeline.stages.items():
                if stage_metrics.success is False:
                    error_info["failed_stage"] = stage_enum.value
                    if stage_metrics.error:
                        error_info["stage_error"] = stage_metrics.error
                    break

            recent_errors.append(error_info)

        # Calculate performance metrics
        stats = inspector.calculate_success_rate(minutes)
        performance_metrics = {
            "success_rate": stats["success_rate"],
            "avg_duration_ms": stats["avg_duration_ms"],
            "total_pipelines": stats["total_pipelines"],
            "successful_pipelines": stats["successful_pipelines"],
            "failed_pipelines": stats["failed_pipelines"],
            "time_window_minutes": minutes,
        }

        # Determine overall health status
        if stats["success_rate"] > 0.9 and active_count < 10:  # Healthy thresholds
            health_status = "healthy"
        elif stats["success_rate"] > 0.7:  # Degraded thresholds
            health_status = "degraded"
        else:
            health_status = "unhealthy"

        # Check for stuck pipelines
        stuck_pipelines = []
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=5)

        for pipeline in ACTIVE_PIPELINES.values():
            if pipeline.started_at < cutoff_time and not pipeline.completed_at:
                stuck_pipelines.append(pipeline.correlation_id)

        if stuck_pipelines:
            health_status = "degraded" if health_status == "healthy" else "unhealthy"
            performance_metrics["stuck_pipelines"] = len(stuck_pipelines)

        return PipelineStatusResponse(
            active_pipelines=active_count,
            recent_errors=recent_errors,
            performance_metrics=performance_metrics,
            health_status=health_status,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as e:
        logger.error(f"Failed to get pipeline status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline status check failed: {str(e)}",
        )


@slack_monitoring_router.get(
    "/pipelines/{correlation_id}/trace", response_model=PipelineTraceResponse
)
async def get_pipeline_trace(correlation_id: str):
    """
    Get detailed trace for a specific pipeline execution.

    Provides comprehensive debugging information for a pipeline including:
    - Stage progression with timings
    - Error details at each stage
    - Context data and metadata
    - Webhook payload information
    """
    try:
        from services.debugging.slack_inspector import SlackPipelineInspector

        inspector = SlackPipelineInspector()
        pipeline = inspector.get_pipeline_by_correlation_id(correlation_id)

        if not pipeline:
            return PipelineTraceResponse(
                correlation_id=correlation_id, found=False, error="Pipeline not found"
            )

        # Get pipeline summary for API response
        trace_data = pipeline.get_summary()

        return PipelineTraceResponse(
            correlation_id=correlation_id, found=True, trace_data=trace_data
        )

    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline monitoring not available - modules not loaded",
        )
    except Exception as e:
        logger.error(f"Failed to get pipeline trace for {correlation_id}: {e}")
        return PipelineTraceResponse(correlation_id=correlation_id, found=False, error=str(e))


@slack_monitoring_router.get("/pipelines/active")
async def get_active_pipelines():
    """Get summary of all currently active pipelines"""
    try:
        from services.debugging.slack_inspector import SlackPipelineInspector

        inspector = SlackPipelineInspector()
        active_pipelines = inspector.get_active_pipelines()

        pipeline_summaries = []
        for pipeline in active_pipelines:
            current_duration = (
                datetime.now(timezone.utc) - pipeline.started_at
            ).total_seconds() * 1000

            # Find current stage
            current_stage = "unknown"
            if pipeline.stages:
                # Get the most recent stage that was started
                latest_stage = max(pipeline.stages.items(), key=lambda x: x[1].started_at)
                current_stage = latest_stage[0].value

            pipeline_summaries.append(
                {
                    "correlation_id": pipeline.correlation_id,
                    "event_id": pipeline.slack_event_id,
                    "started_at": pipeline.started_at.isoformat(),
                    "duration_ms": round(current_duration, 2),
                    "current_stage": current_stage,
                    "webhook_type": (
                        pipeline.webhook_data.get("type", "unknown")
                        if pipeline.webhook_data
                        else "unknown"
                    ),
                }
            )

        return {
            "active_count": len(pipeline_summaries),
            "pipelines": pipeline_summaries,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline monitoring not available - modules not loaded",
        )
    except Exception as e:
        logger.error(f"Failed to get active pipelines: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Active pipelines check failed: {str(e)}",
        )


@slack_monitoring_router.get("/health")
async def get_slack_health():
    """
    Get comprehensive Slack integration health status.

    Returns the same data as the general health endpoint but focused specifically
    on Slack integration components for dedicated monitoring.
    """
    try:
        from services.debugging.slack_inspector import SlackPipelineInspector

        inspector = SlackPipelineInspector()
        health_data = inspector.get_pipeline_health()

        return health_data

    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Slack health monitoring not available - modules not loaded",
        )
    except Exception as e:
        logger.error(f"Slack health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Slack health check failed: {str(e)}",
        )


@slack_monitoring_router.get("/stats")
async def get_pipeline_statistics(
    minutes: int = Query(60, description="Time window for statistics in minutes"),
):
    """
    Get detailed pipeline statistics for the specified time window.

    Provides comprehensive metrics for monitoring dashboards and alerting systems.
    """
    try:
        from services.debugging.slack_inspector import SlackPipelineInspector
        from services.infrastructure.task_manager import task_manager

        inspector = SlackPipelineInspector()

        # Get pipeline statistics
        pipeline_stats = inspector.calculate_success_rate(minutes)

        # Get task manager statistics
        task_stats = task_manager.get_active_tasks_summary()

        # Get recent failures analysis
        failed_pipelines = inspector.get_failed_pipelines(minutes)

        # Analyze failure patterns
        failure_stages = {}
        for pipeline in failed_pipelines:
            for stage_enum, stage_metrics in pipeline.stages.items():
                if stage_metrics.success is False:
                    stage_name = stage_enum.value
                    failure_stages[stage_name] = failure_stages.get(stage_name, 0) + 1
                    break

        return {
            "time_window_minutes": minutes,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pipeline_metrics": pipeline_stats,
            "task_metrics": task_stats,
            "failure_analysis": {
                "total_failures": len(failed_pipelines),
                "failure_stages": failure_stages,
                "most_common_failure": (
                    max(failure_stages.items(), key=lambda x: x[1])[0] if failure_stages else None
                ),
            },
            "performance_analysis": {
                "meeting_slack_timeout": (
                    pipeline_stats["avg_duration_ms"] < 3000
                    if pipeline_stats["avg_duration_ms"] > 0
                    else None
                ),
                "avg_duration_status": (
                    (
                        "excellent"
                        if pipeline_stats["avg_duration_ms"] < 1000
                        else (
                            "good"
                            if pipeline_stats["avg_duration_ms"] < 2000
                            else (
                                "warning"
                                if pipeline_stats["avg_duration_ms"] < 3000
                                else "critical"
                            )
                        )
                    )
                    if pipeline_stats["avg_duration_ms"] > 0
                    else "no_data"
                ),
            },
        }

    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline statistics not available - modules not loaded",
        )
    except Exception as e:
        logger.error(f"Failed to get pipeline statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline statistics failed: {str(e)}",
        )


@slack_monitoring_router.post("/pipelines/{correlation_id}/replay")
async def replay_pipeline_event(correlation_id: str, mock_calls: bool = True):
    """
    Replay a pipeline event for debugging purposes.

    Useful for debugging failed pipelines by replaying the original webhook event
    with the same correlation ID for analysis.
    """
    try:
        from services.debugging.slack_inspector import SlackPipelineInspector

        inspector = SlackPipelineInspector()

        # Find the original pipeline
        pipeline = inspector.get_pipeline_by_correlation_id(correlation_id)
        if not pipeline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Pipeline {correlation_id} not found"
            )

        # Extract webhook data for replay
        if not pipeline.webhook_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No webhook data available for replay",
            )

        # Replay the event
        replayed_pipeline = await inspector.replay_event(
            pipeline.webhook_data, mock_api_calls=mock_calls
        )

        if replayed_pipeline:
            return {
                "original_correlation_id": correlation_id,
                "replayed_correlation_id": replayed_pipeline.correlation_id,
                "replay_successful": True,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        else:
            return {
                "original_correlation_id": correlation_id,
                "replayed_correlation_id": None,
                "replay_successful": False,
                "error": "Replay failed - check logs for details",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline replay not available - modules not loaded",
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Failed to replay pipeline {correlation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline replay failed: {str(e)}",
        )


@slack_monitoring_router.post("/cleanup")
async def cleanup_old_pipelines(
    max_age_minutes: int = Query(30, description="Maximum age of pipelines to keep"),
):
    """
    Clean up old pipeline data to prevent memory leaks.

    Removes completed pipelines older than the specified age from the monitoring
    system while preserving recent data for debugging.
    """
    try:
        from services.infrastructure.task_manager import task_manager
        from services.observability.slack_monitor import SlackPipelineMonitor

        # Clean up old pipeline data
        monitor = SlackPipelineMonitor()
        monitor.cleanup_stale_pipelines(max_age_minutes=max_age_minutes)

        # Clean up old task data
        task_manager.cleanup_completed_tasks(
            max_age_minutes=max_age_minutes * 2
        )  # Keep task data longer

        return {
            "cleanup_completed": True,
            "max_age_minutes": max_age_minutes,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline cleanup not available - modules not loaded",
        )
    except Exception as e:
        logger.error(f"Pipeline cleanup failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline cleanup failed: {str(e)}",
        )
