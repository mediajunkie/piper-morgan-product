"""
Slack Pipeline Inspector

Comprehensive debugging and inspection utilities for Slack integration pipeline.
Provides real-time monitoring, trace analysis, and event replay capabilities
to eliminate silent failures through complete observability.

This module enables interactive debugging of pipeline executions with detailed
trace analysis and replay capabilities for failed events.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, patch

from services.infrastructure.task_manager import task_manager
from services.observability.slack_monitor import (
    ACTIVE_PIPELINES,
    ProcessingStage,
    SlackPipelineMetrics,
)

logger = logging.getLogger(__name__)


class SlackPipelineInspector:
    """
    Tools for debugging silent failures and analyzing pipeline execution.

    Provides comprehensive inspection capabilities for active and completed
    pipelines, enabling detailed trace analysis and event replay for debugging.
    """

    @staticmethod
    def get_active_pipelines() -> List[SlackPipelineMetrics]:
        """Get all currently active pipeline executions"""
        return list(ACTIVE_PIPELINES.values())

    @staticmethod
    def get_pipeline_by_correlation_id(correlation_id: str) -> Optional[SlackPipelineMetrics]:
        """Find pipeline metrics by correlation ID"""
        return ACTIVE_PIPELINES.get(correlation_id)

    @staticmethod
    def get_pipeline_by_event_id(event_id: str) -> Optional[SlackPipelineMetrics]:
        """Find pipeline metrics by Slack event ID"""
        for metrics in ACTIVE_PIPELINES.values():
            if metrics.slack_event_id == event_id:
                return metrics
        return None

    @staticmethod
    def get_recent_pipelines(minutes: int = 30) -> List[SlackPipelineMetrics]:
        """Get pipelines from the last N minutes"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=minutes)

        recent_pipelines = []
        for pipeline in ACTIVE_PIPELINES.values():
            if pipeline.started_at >= cutoff_time:
                recent_pipelines.append(pipeline)

        # Sort by start time, most recent first
        return sorted(recent_pipelines, key=lambda p: p.started_at, reverse=True)

    @staticmethod
    def get_failed_pipelines(minutes: int = 60) -> List[SlackPipelineMetrics]:
        """Get all failed pipelines from the last N minutes"""
        recent_pipelines = SlackPipelineInspector.get_recent_pipelines(minutes)

        failed_pipelines = []
        for pipeline in recent_pipelines:
            if (
                pipeline.final_status == "failed"
                or ProcessingStage.PIPELINE_FAILED in pipeline.stages
                or pipeline.error_details
            ):
                failed_pipelines.append(pipeline)

        return failed_pipelines

    @staticmethod
    def print_pipeline_trace(correlation_id: str) -> bool:
        """
        Print detailed trace of a pipeline execution.

        Args:
            correlation_id: The correlation ID to trace

        Returns:
            True if pipeline was found and traced, False otherwise
        """
        metrics = ACTIVE_PIPELINES.get(correlation_id)
        if not metrics:
            print(f"❌ No pipeline found for correlation ID: {correlation_id}")
            return False

        print(f"\n{'='*60}")
        print(f"🔍 Pipeline Trace: {correlation_id}")
        print(f"{'='*60}")
        print(f"📧 Event ID: {metrics.slack_event_id or 'N/A'}")
        print(f"⏱️  Started: {metrics.started_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")

        if metrics.completed_at:
            print(f"✅ Completed: {metrics.completed_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"⚡ Total Duration: {metrics.total_duration_ms:.2f}ms")
            print(f"🎯 Final Status: {metrics.final_status or 'unknown'}")
        else:
            print(
                f"🔄 Status: RUNNING (duration: {(datetime.now(timezone.utc) - metrics.started_at).total_seconds() * 1000:.2f}ms)"
            )

        if metrics.error_details:
            print(f"❌ Error: {metrics.error_details}")

        print(f"\n📊 Stage Progression:")
        print(f"{'Stage':<25} {'Status':<10} {'Duration':<12} {'Started At':<20}")
        print(f"{'-'*70}")

        for stage_enum, stage_metrics in metrics.stages.items():
            status = (
                "✅ SUCCESS"
                if stage_metrics.success
                else "❌ FAILED"
                if stage_metrics.success is False
                else "🔄 RUNNING"
            )
            duration = f"{stage_metrics.duration_ms:.2f}ms" if stage_metrics.duration_ms else "N/A"
            started = (
                stage_metrics.started_at.strftime("%H:%M:%S") if stage_metrics.started_at else "N/A"
            )

            print(f"{stage_enum.value:<25} {status:<10} {duration:<12} {started:<20}")

            if stage_metrics.error:
                print(f"  💥 Error: {stage_metrics.error}")

            if stage_metrics.metadata:
                print(f"  📝 Metadata: {json.dumps(stage_metrics.metadata, indent=2)}")

        print(f"\n📦 Webhook Data:")
        if metrics.webhook_data:
            print(json.dumps(metrics.webhook_data, indent=2))
        else:
            print("No webhook data available")

        return True

    @staticmethod
    def print_active_pipelines_summary():
        """Print summary of all active pipelines"""
        active_pipelines = SlackPipelineInspector.get_active_pipelines()

        if not active_pipelines:
            print("✅ No active pipelines")
            return

        print(f"\n🔄 Active Pipelines: {len(active_pipelines)}")
        print(f"{'Correlation ID':<40} {'Event ID':<20} {'Duration':<12} {'Stage':<25}")
        print(f"{'-'*100}")

        for pipeline in sorted(active_pipelines, key=lambda p: p.started_at):
            duration = (datetime.now(timezone.utc) - pipeline.started_at).total_seconds() * 1000
            current_stage = "unknown"

            # Find the most recent stage
            if pipeline.stages:
                latest_stage = max(pipeline.stages.items(), key=lambda x: x[1].started_at)
                current_stage = latest_stage[0].value

            print(
                f"{pipeline.correlation_id:<40} {pipeline.slack_event_id or 'N/A':<20} {duration:.0f}ms{'':<7} {current_stage:<25}"
            )

    @staticmethod
    def print_failure_analysis(minutes: int = 60):
        """Print analysis of recent failures"""
        failed_pipelines = SlackPipelineInspector.get_failed_pipelines(minutes)

        if not failed_pipelines:
            print(f"✅ No failed pipelines in the last {minutes} minutes")
            return

        print(f"\n❌ Failed Pipelines ({minutes} minutes): {len(failed_pipelines)}")
        print(f"{'Correlation ID':<40} {'Failed Stage':<25} {'Error':<30}")
        print(f"{'-'*100}")

        for pipeline in failed_pipelines:
            failed_stage = "unknown"
            error_msg = pipeline.error_details or "Unknown error"

            # Find the failed stage
            for stage_enum, stage_metrics in pipeline.stages.items():
                if stage_metrics.success is False:
                    failed_stage = stage_enum.value
                    if stage_metrics.error:
                        error_msg = stage_metrics.error[:30]
                    break

            print(f"{pipeline.correlation_id:<40} {failed_stage:<25} {error_msg:<30}")

    @staticmethod
    async def replay_event(
        event: Dict[str, Any], mock_api_calls: bool = True
    ) -> Optional[SlackPipelineMetrics]:
        """
        Replay a Slack event through the pipeline for debugging.

        Args:
            event: The Slack event to replay
            mock_api_calls: Whether to mock external API calls to prevent side effects

        Returns:
            The pipeline metrics for the replayed event, or None if replay failed
        """
        print(f"🔄 Replaying event: {event.get('event_ts', event.get('ts', 'unknown'))}")
        print(f"📝 Event type: {event.get('type', 'unknown')}")

        try:
            if mock_api_calls:
                # Mock external calls to prevent side effects
                with patch("services.integrations.slack.client.slack_client") as mock_client:
                    mock_client.chat_postMessage = AsyncMock(
                        return_value={"ok": True, "ts": "mock_response"}
                    )
                    mock_client.auth_test = AsyncMock(
                        return_value={"ok": True, "team": "mock_team"}
                    )

                    # Import and call the webhook handler
                    from services.integrations.slack.webhook_router import handle_event_callback

                    result = await handle_event_callback(event)
            else:
                print("⚠️  WARNING: Using real API calls - this may have side effects!")
                from services.integrations.slack.webhook_router import handle_event_callback

                result = await handle_event_callback(event)

            # Wait for background processing to complete
            print("⏳ Waiting for background processing...")
            await asyncio.sleep(2.0)

            # Find the most recent pipeline (should be our replay)
            recent_pipelines = SlackPipelineInspector.get_recent_pipelines(1)  # Last 1 minute
            if recent_pipelines:
                latest_pipeline = recent_pipelines[0]
                print(f"✅ Replay completed - Pipeline: {latest_pipeline.correlation_id}")

                # Print the trace automatically
                SlackPipelineInspector.print_pipeline_trace(latest_pipeline.correlation_id)

                return latest_pipeline
            else:
                print("❌ No pipeline found after replay - check logs for errors")
                return None

        except Exception as e:
            print(f"❌ Replay failed with exception: {e}")
            logger.error(f"Event replay failed: {e}", exc_info=True)
            return None

    @staticmethod
    def calculate_success_rate(minutes: int = 60) -> Dict[str, Any]:
        """Calculate success rate for recent pipelines"""
        recent_pipelines = SlackPipelineInspector.get_recent_pipelines(minutes)

        if not recent_pipelines:
            return {
                "total_pipelines": 0,
                "successful_pipelines": 0,
                "failed_pipelines": 0,
                "success_rate": 0.0,
                "avg_duration_ms": 0.0,
            }

        successful = 0
        failed = 0
        total_duration = 0.0
        completed_count = 0

        for pipeline in recent_pipelines:
            if pipeline.final_status == "success":
                successful += 1
            elif pipeline.final_status == "failed":
                failed += 1

            if pipeline.total_duration_ms:
                total_duration += pipeline.total_duration_ms
                completed_count += 1

        return {
            "total_pipelines": len(recent_pipelines),
            "successful_pipelines": successful,
            "failed_pipelines": failed,
            "success_rate": successful / len(recent_pipelines) if recent_pipelines else 0.0,
            "avg_duration_ms": total_duration / completed_count if completed_count > 0 else 0.0,
        }

    @staticmethod
    def get_pipeline_health() -> Dict[str, Any]:
        """Get comprehensive pipeline health metrics"""
        active_pipelines = SlackPipelineInspector.get_active_pipelines()
        recent_stats = SlackPipelineInspector.calculate_success_rate(60)
        task_summary = task_manager.get_active_tasks_summary()

        # Check for stuck pipelines (running > 5 minutes)
        stuck_pipelines = []
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=5)

        for pipeline in active_pipelines:
            if pipeline.started_at < cutoff_time and not pipeline.completed_at:
                stuck_pipelines.append(
                    {
                        "correlation_id": pipeline.correlation_id,
                        "duration_minutes": (
                            datetime.now(timezone.utc) - pipeline.started_at
                        ).total_seconds()
                        / 60,
                    }
                )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_pipelines": len(active_pipelines),
            "stuck_pipelines": len(stuck_pipelines),
            "stuck_pipeline_details": stuck_pipelines,
            "recent_success_rate": recent_stats["success_rate"],
            "avg_processing_time_ms": recent_stats["avg_duration_ms"],
            "background_tasks": {
                "active": task_summary["active_tasks"],
                "total_created": task_summary["total_tasks_created"],
                "success_rate": task_summary["success_rate"],
            },
            "health_status": (
                "healthy"
                if (
                    recent_stats["success_rate"] > 0.8
                    and len(stuck_pipelines) == 0
                    and task_summary["success_rate"] > 0.8
                )
                else "degraded"
                if recent_stats["success_rate"] > 0.5
                else "unhealthy"
            ),
        }


class PipelineDebugger:
    """Interactive debugging session manager"""

    def __init__(self):
        self.inspector = SlackPipelineInspector()

    async def start_debug_session(self):
        """Start an interactive debugging session"""
        print("🔧 Slack Pipeline Debugger")
        print("=" * 50)
        print("Available commands:")
        print("  trace <correlation_id>     - Show detailed pipeline trace")
        print("  event <event_id>          - Find pipeline by Slack event ID")
        print("  active                    - Show active pipelines")
        print("  failures [minutes]        - Show recent failures (default: 60 min)")
        print("  health                    - Show pipeline health status")
        print("  replay <event_json>       - Replay event for debugging")
        print("  stats [minutes]           - Show success rate stats (default: 60 min)")
        print("  cleanup                   - Clean up old pipeline data")
        print("  help                      - Show this help message")
        print("  exit                      - Exit debugger")
        print("=" * 50)

        while True:
            try:
                command_line = input("\n🔍 > ").strip()
                if not command_line:
                    continue

                command_parts = command_line.split(None, 1)
                command = command_parts[0].lower()
                args = command_parts[1] if len(command_parts) > 1 else ""

                if command == "trace":
                    if args:
                        self.inspector.print_pipeline_trace(args)
                    else:
                        print("❌ Usage: trace <correlation_id>")

                elif command == "event":
                    if args:
                        pipeline = self.inspector.get_pipeline_by_event_id(args)
                        if pipeline:
                            self.inspector.print_pipeline_trace(pipeline.correlation_id)
                        else:
                            print(f"❌ No pipeline found for event ID: {args}")
                    else:
                        print("❌ Usage: event <event_id>")

                elif command == "active":
                    self.inspector.print_active_pipelines_summary()

                elif command == "failures":
                    minutes = 60
                    if args:
                        try:
                            minutes = int(args)
                        except ValueError:
                            print(f"❌ Invalid minutes value: {args}")
                            continue
                    self.inspector.print_failure_analysis(minutes)

                elif command == "health":
                    health = self.inspector.get_pipeline_health()
                    print(f"\n🏥 Pipeline Health Status: {health['health_status'].upper()}")
                    print(f"📊 Active Pipelines: {health['active_pipelines']}")
                    print(f"🔄 Success Rate: {health['recent_success_rate']:.1%}")
                    print(f"⚡ Avg Processing Time: {health['avg_processing_time_ms']:.1f}ms")
                    print(f"🔒 Stuck Pipelines: {health['stuck_pipelines']}")
                    print(f"🎯 Background Tasks: {health['background_tasks']['active']} active")

                elif command == "replay":
                    if args:
                        try:
                            event_data = json.loads(args)
                            await self.inspector.replay_event(event_data, mock_api_calls=True)
                        except json.JSONDecodeError:
                            print("❌ Invalid JSON format for event data")
                        except Exception as e:
                            print(f"❌ Replay failed: {e}")
                    else:
                        print("❌ Usage: replay <event_json>")

                elif command == "stats":
                    minutes = 60
                    if args:
                        try:
                            minutes = int(args)
                        except ValueError:
                            print(f"❌ Invalid minutes value: {args}")
                            continue

                    stats = self.inspector.calculate_success_rate(minutes)
                    print(f"\n📈 Pipeline Statistics ({minutes} minutes):")
                    print(f"  Total Pipelines: {stats['total_pipelines']}")
                    print(f"  Successful: {stats['successful_pipelines']}")
                    print(f"  Failed: {stats['failed_pipelines']}")
                    print(f"  Success Rate: {stats['success_rate']:.1%}")
                    print(f"  Avg Duration: {stats['avg_duration_ms']:.1f}ms")

                elif command == "cleanup":
                    from services.observability.slack_monitor import SlackPipelineMonitor

                    monitor = SlackPipelineMonitor()
                    monitor.cleanup_stale_pipelines(max_age_minutes=30)
                    task_manager.cleanup_completed_tasks(max_age_minutes=60)
                    print("✅ Cleanup completed")

                elif command == "help":
                    print("\n🔧 Available commands:")
                    print("  trace <correlation_id>     - Show detailed pipeline trace")
                    print("  event <event_id>          - Find pipeline by Slack event ID")
                    print("  active                    - Show active pipelines")
                    print("  failures [minutes]        - Show recent failures")
                    print("  health                    - Show pipeline health status")
                    print("  replay <event_json>       - Replay event for debugging")
                    print("  stats [minutes]           - Show success rate stats")
                    print("  cleanup                   - Clean up old pipeline data")
                    print("  exit                      - Exit debugger")

                elif command == "exit":
                    print("👋 Exiting Slack Pipeline Debugger")
                    break

                else:
                    print(f"❌ Unknown command: {command}. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\n👋 Exiting Slack Pipeline Debugger")
                break
            except Exception as e:
                print(f"❌ Command failed: {e}")
                logger.error(f"Debug command failed: {e}", exc_info=True)
