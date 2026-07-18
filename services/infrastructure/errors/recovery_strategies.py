import asyncio
import logging
from dataclasses import dataclass
from typing import Any


@dataclass
class SearchResult:
    results: list
    degraded: bool = False
    reason: str = ""


class MCPRecoveryStrategies:
    """Implements graceful degradation and recovery patterns"""

    @staticmethod
    async def fallback_to_filename_search(query: str, error: Exception) -> SearchResult:
        """When content search fails, fall back to filename matching.

        #1436 F4 (Arch: remove-the-lie): the placeholder FABRICATED a result
        ("Matched file for query ..."). A dormant safety scaffold that honestly
        returns nothing is fine; one that invents results is a landmine. Wire a
        real filename search here when this strategy gets a caller.
        """
        logging.warning(f"Fallback to filename search due to error: {error}")
        return SearchResult(results=[], degraded=True, reason="content_search_failed")

    @staticmethod
    async def circuit_breaker_recovery(service_name: str) -> bool:
        """Attempt to recover from circuit breaker open state.

        #1436 F4 (Arch: remove-the-lie): the placeholder fake-slept and
        returned True — a fabricated "recovered" signal. Until a real health
        probe exists, honestly report NOT recovered; callers keep the breaker
        open (the safe state).
        """
        logging.info(f"Circuit breaker recovery for {service_name}: no real probe wired — reporting not-recovered")
        return False

    @staticmethod
    async def performance_degradation_response(current_latency: float) -> dict:
        """Adjust behavior when performance degrades"""
        response = {"mode": "normal"}
        if current_latency > 500:
            response["mode"] = "cache_only"
            response["action"] = "Switching to cache-only mode due to high latency."
        elif current_latency > 400:
            response["mode"] = "limited_concurrency"
            response["action"] = "Limiting concurrent extractions."
        elif current_latency > 200:
            response["mode"] = "no_tfidf"
            response["action"] = "Disabling TF-IDF scoring."
        return response


class AlertThresholds:
    """Define when to alert on various conditions"""

    ERROR_RATE_WARNING = 0.05  # 5% errors
    ERROR_RATE_CRITICAL = 0.10  # 10% errors
    LATENCY_WARNING = 300  # ms
    LATENCY_CRITICAL = 500  # ms
    EXTRACTION_FAILURE_RATE = 0.20  # 20% extraction failures
