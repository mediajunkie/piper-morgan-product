"""
Integration Health Monitor
Foundation Repair: Centralized component health tracking and graceful degradation
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger()


class ComponentStatus(Enum):
    """Component health status"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class ComponentHealth:
    """Health information for a system component"""

    name: str
    status: ComponentStatus
    last_check: float
    error_count: int
    last_error: Optional[str]
    success_rate: float
    average_latency_ms: float
    metadata: Dict[str, Any]


class IntegrationHealthMonitor:
    """
    Centralized health monitoring for integration components.

    Provides:
    - Component health tracking
    - Error aggregation and analysis
    - Graceful degradation decisions
    - Clear failure visibility
    """

    def __init__(self):
        self.components: Dict[str, ComponentHealth] = {}
        self.error_history: List[Dict[str, Any]] = []
        self.max_error_history = 1000
        self.health_check_interval = 30.0  # seconds

        logger.info("Integration Health Monitor initialized")

    def register_component(
        self, name: str, initial_status: ComponentStatus = ComponentStatus.UNKNOWN
    ) -> None:
        """Register a component for health tracking"""
        self.components[name] = ComponentHealth(
            name=name,
            status=initial_status,
            last_check=time.time(),
            error_count=0,
            last_error=None,
            success_rate=1.0,
            average_latency_ms=0.0,
            metadata={},
        )
        logger.info(f"Registered component for health monitoring: {name}")

    def record_success(
        self, component_name: str, latency_ms: float, metadata: Optional[Dict] = None
    ) -> None:
        """Record successful operation for a component"""
        if component_name not in self.components:
            self.register_component(component_name)

        component = self.components[component_name]
        component.status = ComponentStatus.HEALTHY
        component.last_check = time.time()
        component.average_latency_ms = self._update_average(
            component.average_latency_ms,
            latency_ms,
            0.1,  # Moving average factor
        )

        if metadata:
            component.metadata.update(metadata)

        logger.debug(f"Recorded success for {component_name}: {latency_ms:.1f}ms")

    def record_failure(
        self, component_name: str, error: str, metadata: Optional[Dict] = None
    ) -> None:
        """Record failure for a component"""
        if component_name not in self.components:
            self.register_component(component_name)

        component = self.components[component_name]
        component.error_count += 1
        component.last_error = error
        component.last_check = time.time()

        # Update status based on failure patterns
        if component.error_count > 10:
            component.status = ComponentStatus.FAILED
        elif component.error_count > 3:
            component.status = ComponentStatus.DEGRADED

        # Add to error history
        error_entry = {
            "timestamp": time.time(),
            "component": component_name,
            "error": error,
            "metadata": metadata or {},
            "total_errors": component.error_count,
        }
        self.error_history.append(error_entry)

        # Trim error history if too long
        if len(self.error_history) > self.max_error_history:
            self.error_history = self.error_history[-self.max_error_history :]

        logger.warning(f"Recorded failure for {component_name}: {error}")

    def get_component_health(self, component_name: str) -> Optional[ComponentHealth]:
        """Get health information for a specific component"""
        return self.components.get(component_name)

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health summary"""
        if not self.components:
            return {
                "overall_status": "unknown",
                "healthy_components": 0,
                "total_components": 0,
                "health_percentage": 0,
                "components": {},
            }

        healthy_count = sum(
            1 for c in self.components.values() if c.status == ComponentStatus.HEALTHY
        )
        total_count = len(self.components)
        health_percentage = (healthy_count / total_count) * 100 if total_count > 0 else 0

        # Determine overall status
        if health_percentage >= 80:
            overall_status = "healthy"
        elif health_percentage >= 50:
            overall_status = "degraded"
        else:
            overall_status = "unhealthy"

        return {
            "overall_status": overall_status,
            "healthy_components": healthy_count,
            "total_components": total_count,
            "health_percentage": health_percentage,
            "components": {
                name: {
                    "status": comp.status.value,
                    "error_count": comp.error_count,
                    "success_rate": comp.success_rate,
                    "average_latency_ms": comp.average_latency_ms,
                    "last_error": comp.last_error,
                    "last_check": comp.last_check,
                }
                for name, comp in self.components.items()
            },
        }

    def should_degrade_gracefully(self, component_name: str) -> bool:
        """Determine if a component should use graceful degradation"""
        component = self.components.get(component_name)
        if not component:
            return False

        # Use graceful degradation if component is degraded or failed
        return component.status in [ComponentStatus.DEGRADED, ComponentStatus.FAILED]

    def get_degradation_strategy(self, component_name: str) -> Dict[str, Any]:
        """Get recommended degradation strategy for a component"""
        component = self.components.get(component_name)
        if not component:
            return {"strategy": "unknown", "reason": "component not registered"}

        if component.status == ComponentStatus.FAILED:
            return {
                "strategy": "circuit_breaker",
                "reason": f"Component failed with {component.error_count} errors",
                "fallback": "static_response",
                "retry_after": 300,  # 5 minutes
            }
        elif component.status == ComponentStatus.DEGRADED:
            return {
                "strategy": "limited_functionality",
                "reason": f"Component degraded with {component.error_count} errors",
                "fallback": "simplified_response",
                "retry_after": 60,  # 1 minute
            }
        else:
            return {
                "strategy": "normal_operation",
                "reason": "component healthy",
                "fallback": None,
                "retry_after": 0,
            }

    def get_error_analysis(
        self, component_name: Optional[str] = None, last_n_errors: int = 10
    ) -> Dict[str, Any]:
        """Get error analysis for troubleshooting"""
        # Filter errors by component if specified
        errors = self.error_history
        if component_name:
            errors = [e for e in errors if e["component"] == component_name]

        # Get recent errors
        recent_errors = errors[-last_n_errors:] if errors else []

        # Error pattern analysis
        error_patterns = {}
        for error in recent_errors:
            error_msg = error["error"]
            if error_msg in error_patterns:
                error_patterns[error_msg] += 1
            else:
                error_patterns[error_msg] = 1

        return {
            "total_errors": len(errors),
            "recent_errors": len(recent_errors),
            "error_patterns": error_patterns,
            "most_common_error": (
                max(error_patterns.items(), key=lambda x: x[1]) if error_patterns else None
            ),
            "recent_error_details": recent_errors,
        }

    def reset_component_health(self, component_name: str) -> bool:
        """Reset health status for a component (for manual recovery)"""
        if component_name not in self.components:
            return False

        component = self.components[component_name]
        component.status = ComponentStatus.UNKNOWN
        component.error_count = 0
        component.last_error = None
        component.success_rate = 1.0
        component.last_check = time.time()

        logger.info(f"Reset health status for component: {component_name}")
        return True

    def _update_average(self, current_avg: float, new_value: float, factor: float) -> float:
        """Update moving average"""
        return current_avg * (1 - factor) + new_value * factor


# Global health monitor instance
health_monitor = IntegrationHealthMonitor()

# Register core components
health_monitor.register_component("database_connection")
health_monitor.register_component("slack_integration")
health_monitor.register_component("query_response_formatter")
health_monitor.register_component("type_system")
