"""
Ethics Boundary Metrics Monitoring for PM-087
Tracks ethics decision points, boundary enforcement, and audit transparency
"""

import threading
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class EthicsDecisionType(Enum):
    """Types of ethics decisions tracked"""

    BOUNDARY_ENFORCEMENT = "boundary_enforcement"
    AUDIT_LOGGING = "audit_logging"
    # #1019 (Path C): PATTERN_LEARNING enum value removed with adaptive_boundaries scaffolding
    TRANSPARENCY_REQUEST = "transparency_request"
    PROFESSIONAL_BOUNDARY = "professional_boundary"


class EthicsViolationType(Enum):
    """Types of ethics boundary violations"""

    HARASSMENT_ATTEMPT = "harassment_attempt"
    PERSONAL_BOUNDARY_CROSS = "personal_boundary_cross"
    INAPPROPRIATE_REQUEST = "inappropriate_request"
    DATA_PRIVACY_VIOLATION = "data_privacy_violation"
    PROFESSIONAL_BOUNDARY_VIOLATION = "professional_boundary_violation"


class EthicsMetrics:
    """Singleton for tracking PM-087 ethics boundary metrics"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_metrics()
            return cls._instance

    def _init_metrics(self):
        # Boundary violation tracking
        self.boundary_violations_total = 0
        self.boundary_violations_by_type = defaultdict(int)
        self.boundary_violations_recent = []  # Last 24 hours

        # Ethics decision tracking
        self.ethics_decisions_total = 0
        self.ethics_decisions_by_type = defaultdict(int)
        self.ethics_decisions_recent = []  # Last 24 hours

        # Audit trail tracking
        self.audit_trail_entries_total = 0
        self.audit_trail_failures_total = 0
        self.audit_transparency_requests = 0

        # Professional boundary tracking
        self.professional_boundaries_enforced = 0
        self.professional_guidance_provided = 0

        # Transparency and user trust metrics
        self.transparency_explanations_provided = 0
        self.user_ethics_inquiries = 0

        # Performance metrics
        self.ethics_check_latencies = []  # Response times for ethics checks
        self.last_ethics_check = None

        # Compliance and reporting
        self.compliance_reports_generated = 0
        self.ethics_health_checks = 0

    def record_boundary_violation(
        self,
        violation_type: EthicsViolationType,
        context: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        """Record a boundary violation event"""
        self.boundary_violations_total += 1
        self.boundary_violations_by_type[violation_type.value] += 1

        # Store recent violation for trend analysis (no personal data)
        self.boundary_violations_recent.append(
            {
                "timestamp": datetime.now(timezone.utc),
                "type": violation_type.value,
                "context_hash": hash(context) if context else None,  # Hash only, no actual content
                "session_hash": hash(session_id) if session_id else None,  # Hash only
            }
        )

        # Keep only last 24 hours
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        self.boundary_violations_recent = [
            v for v in self.boundary_violations_recent if v["timestamp"] > cutoff
        ]

    def record_ethics_decision(
        self,
        decision_type: EthicsDecisionType,
        decision_made: str,
        response_time_ms: float,
        session_id: Optional[str] = None,
    ):
        """Record an ethics decision point"""
        self.ethics_decisions_total += 1
        self.ethics_decisions_by_type[decision_type.value] += 1

        # Store recent decision for analysis (no personal data)
        self.ethics_decisions_recent.append(
            {
                "timestamp": datetime.now(timezone.utc),
                "type": decision_type.value,
                "decision_hash": hash(decision_made),  # Hash only
                "response_time_ms": response_time_ms,
                "session_hash": hash(session_id) if session_id else None,
            }
        )

        # Track performance
        self.ethics_check_latencies.append(response_time_ms)
        if len(self.ethics_check_latencies) > 1000:
            self.ethics_check_latencies = self.ethics_check_latencies[-1000:]

        # Keep only last 24 hours
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        self.ethics_decisions_recent = [
            d for d in self.ethics_decisions_recent if d["timestamp"] > cutoff
        ]

    def record_audit_trail_entry(self, success: bool = True):
        """Record audit trail logging attempt"""
        self.audit_trail_entries_total += 1
        if not success:
            self.audit_trail_failures_total += 1

    def record_professional_boundary_enforcement(self):
        """Record professional boundary being enforced"""
        self.professional_boundaries_enforced += 1

    def record_professional_guidance(self):
        """Record professional guidance being provided"""
        self.professional_guidance_provided += 1

    def record_transparency_explanation(self):
        """Record transparency explanation provided to user"""
        self.transparency_explanations_provided += 1

    def record_user_ethics_inquiry(self):
        """Record user asking about ethics/behavior"""
        self.user_ethics_inquiries += 1

    def record_compliance_report(self):
        """Record compliance report generation"""
        self.compliance_reports_generated += 1

    def perform_ethics_health_check(self) -> Dict[str, Any]:
        """Perform ethics system health check"""
        self.ethics_health_checks += 1
        self.last_ethics_check = datetime.now(timezone.utc)

        # Calculate recent violation rate (per hour)
        recent_violations = len(self.boundary_violations_recent)
        hours_tracked = min(
            24,
            (
                datetime.now(timezone.utc)
                - (
                    self.boundary_violations_recent[0]["timestamp"]
                    if self.boundary_violations_recent
                    else datetime.now(timezone.utc)
                )
            ).total_seconds()
            / 3600,
        )
        violation_rate_per_hour = recent_violations / max(hours_tracked, 1)

        # Calculate audit trail success rate
        audit_success_rate = (
            self.audit_trail_entries_total - self.audit_trail_failures_total
        ) / max(self.audit_trail_entries_total, 1)

        # Calculate ethics response performance
        avg_ethics_response_time = (
            sum(self.ethics_check_latencies) / len(self.ethics_check_latencies)
            if self.ethics_check_latencies
            else 0
        )

        return {
            "violation_rate_per_hour": round(violation_rate_per_hour, 3),
            "audit_success_rate": round(audit_success_rate, 3),
            "avg_ethics_response_time_ms": round(avg_ethics_response_time, 2),
            "transparency_engagement_rate": (
                self.user_ethics_inquiries / max(self.ethics_decisions_total, 1)
            ),
            "professional_boundary_effectiveness": (
                self.professional_boundaries_enforced
                / max(
                    self.professional_boundaries_enforced
                    + self.boundary_violations_by_type.get("professional_boundary_violation", 0),
                    1,
                )
            ),
        }

    def get_prometheus_metrics(self) -> List[str]:
        """Generate Prometheus-formatted metrics for PM-087"""
        metrics = []

        # Boundary violation metrics
        metrics.append(
            f'piper_ethics_boundary_violations_total {{environment="staging"}} {self.boundary_violations_total}'
        )

        for violation_type, count in self.boundary_violations_by_type.items():
            metrics.append(
                f'piper_ethics_boundary_violations_by_type{{type="{violation_type}",environment="staging"}} {count}'
            )

        # Ethics decision metrics
        metrics.append(
            f'piper_ethics_decisions_total{{environment="staging"}} {self.ethics_decisions_total}'
        )

        for decision_type, count in self.ethics_decisions_by_type.items():
            metrics.append(
                f'piper_ethics_decisions_by_type{{type="{decision_type}",environment="staging"}} {count}'
            )

        # Audit trail metrics
        metrics.append(
            f'piper_ethics_audit_trail_entries_total{{environment="staging"}} {self.audit_trail_entries_total}'
        )
        metrics.append(
            f'piper_ethics_audit_trail_failures_total{{environment="staging"}} {self.audit_trail_failures_total}'
        )
        metrics.append(
            f'piper_ethics_audit_transparency_requests{{environment="staging"}} {self.audit_transparency_requests}'
        )

        # Professional boundary metrics
        metrics.append(
            f'piper_ethics_professional_boundaries_enforced{{environment="staging"}} {self.professional_boundaries_enforced}'
        )
        metrics.append(
            f'piper_ethics_professional_guidance_provided{{environment="staging"}} {self.professional_guidance_provided}'
        )

        # Transparency metrics
        metrics.append(
            f'piper_ethics_transparency_explanations{{environment="staging"}} {self.transparency_explanations_provided}'
        )
        metrics.append(
            f'piper_ethics_user_inquiries{{environment="staging"}} {self.user_ethics_inquiries}'
        )

        # Performance metrics
        if self.ethics_check_latencies:
            avg_latency = sum(self.ethics_check_latencies) / len(self.ethics_check_latencies)
            metrics.append(
                f'piper_ethics_check_response_time_ms{{environment="staging"}} {avg_latency:.2f}'
            )

        # Health metrics
        metrics.append(
            f'piper_ethics_health_checks_total{{environment="staging"}} {self.ethics_health_checks}'
        )
        metrics.append(
            f'piper_ethics_compliance_reports_total{{environment="staging"}} {self.compliance_reports_generated}'
        )

        # Recent activity metrics (last 24 hours)
        recent_violations = len(self.boundary_violations_recent)
        recent_decisions = len(self.ethics_decisions_recent)
        metrics.append(
            f'piper_ethics_recent_violations_24h{{environment="staging"}} {recent_violations}'
        )
        metrics.append(
            f'piper_ethics_recent_decisions_24h{{environment="staging"}} {recent_decisions}'
        )

        return metrics

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive ethics metrics summary"""
        health_check = self.perform_ethics_health_check()

        return {
            "boundary_violations": {
                "total": self.boundary_violations_total,
                "by_type": dict(self.boundary_violations_by_type),
                "recent_24h": len(self.boundary_violations_recent),
                "rate_per_hour": health_check["violation_rate_per_hour"],
            },
            "ethics_decisions": {
                "total": self.ethics_decisions_total,
                "by_type": dict(self.ethics_decisions_by_type),
                "recent_24h": len(self.ethics_decisions_recent),
                "avg_response_time_ms": health_check["avg_ethics_response_time_ms"],
            },
            "audit_trail": {
                "entries_total": self.audit_trail_entries_total,
                "failures_total": self.audit_trail_failures_total,
                "success_rate": health_check["audit_success_rate"],
                "transparency_requests": self.audit_transparency_requests,
            },
            "professional_boundaries": {
                "enforced": self.professional_boundaries_enforced,
                "guidance_provided": self.professional_guidance_provided,
                "effectiveness": health_check["professional_boundary_effectiveness"],
            },
            "transparency": {
                "explanations_provided": self.transparency_explanations_provided,
                "user_inquiries": self.user_ethics_inquiries,
                "engagement_rate": health_check["transparency_engagement_rate"],
            },
            "system_health": health_check,
            "last_health_check": (
                self.last_ethics_check.isoformat() if self.last_ethics_check else None
            ),
        }


# Singleton instance for global access
ethics_metrics = EthicsMetrics()
