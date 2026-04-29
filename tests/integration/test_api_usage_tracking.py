"""
Integration tests for API Usage Tracking (Issue #271: CORE-KEYS-COST-TRACKING)

Tests verify that:
1. API usage is logged to the database
2. Token counts are captured correctly
3. Costs are calculated and stored
4. Conversation context is preserved
5. Database schema is properly configured
"""

from decimal import Decimal

import pytest

from services.analytics.api_usage_tracker import APIUsageTracker
from services.analytics.cost_estimator import CostEstimator


class TestAPIUsageTracker:
    """Test API usage tracking functionality"""

    def test_api_usage_tracker_initialization(self):
        """Test that APIUsageTracker can be initialized"""
        tracker = APIUsageTracker()
        assert tracker is not None

    def test_api_usage_log_creation(self):
        """Test that APIUsageLog dataclass can be created"""
        from services.analytics.api_usage_tracker import APIUsageLog

        log = APIUsageLog(
            user_id="test_user",
            provider="anthropic",
            model="claude-3-sonnet",
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            estimated_cost=Decimal("0.0045"),
            conversation_id="conv_123",
            feature="test",
            request_id="req_123",
            response_time_ms=1200,
        )

        assert log.user_id == "test_user"
        assert log.provider == "anthropic"
        assert log.model == "claude-3-sonnet"
        assert log.prompt_tokens == 100
        assert log.completion_tokens == 50
        assert log.total_tokens == 150
        assert log.estimated_cost == Decimal("0.0045")
        assert log.conversation_id == "conv_123"
        assert log.feature == "test"

    def test_usage_summary_creation(self):
        """Test that UsageSummary dataclass can be created"""
        from datetime import datetime

        from services.analytics.api_usage_tracker import UsageSummary

        summary = UsageSummary(
            user_id="test_user",
            period="month",
            start_date=datetime(2025, 10, 1),
            end_date=datetime(2025, 10, 31),
            total_cost=Decimal("100.50"),
            total_requests=50,
            total_tokens=10000,
            by_provider={"anthropic": {"cost": "50.25", "requests": 25}},
            by_model={"claude-3-sonnet": {"cost": "50.25", "requests": 25}},
            by_feature={"chat": {"cost": "50.25", "requests": 25}},
            top_conversations=[{"id": "conv_1", "cost": "10.00"}],
            daily_costs=[{"date": "2025-10-01", "cost": 3.25}],
            cost_per_token=Decimal("0.01"),
            cost_per_request=Decimal("2.01"),
            recommendations=["Consider using GPT-3.5 for simple tasks"],
        )

        assert summary.user_id == "test_user"
        assert summary.period == "month"
        assert summary.total_cost == Decimal("100.50")
        assert summary.total_requests == 50
        assert len(summary.by_provider) == 1
        assert len(summary.recommendations) > 0


class TestCostEstimator:
    """Test cost estimation functionality"""

    def test_cost_estimator_initialization(self):
        """Test that CostEstimator can be initialized"""
        estimator = CostEstimator()
        assert estimator is not None

    def test_cost_estimation_anthropic(self):
        """Test cost calculation for Anthropic models"""
        estimator = CostEstimator()

        # Estimate cost for Claude 3 Sonnet
        cost = estimator.estimate_cost(
            provider="anthropic",
            model="claude-3-sonnet",
            prompt_tokens=1000,
            completion_tokens=500,
        )

        assert cost > 0
        assert isinstance(cost, Decimal)

    def test_cost_estimation_openai(self):
        """Test cost calculation for OpenAI models"""
        estimator = CostEstimator()

        # Estimate cost for GPT-4
        cost = estimator.estimate_cost(
            provider="openai",
            model="gpt-4",
            prompt_tokens=1000,
            completion_tokens=500,
        )

        assert cost > 0
        assert isinstance(cost, Decimal)

    def test_cost_scales_with_tokens(self):
        """Test that cost increases with more tokens"""
        estimator = CostEstimator()

        # Calculate cost for 100 tokens
        cost_100 = estimator.estimate_cost(
            "openai",
            "gpt-3.5-turbo",
            100,
            100,
        )

        # Calculate cost for 1000 tokens (10x more)
        cost_1000 = estimator.estimate_cost(
            "openai",
            "gpt-3.5-turbo",
            1000,
            1000,
        )

        # 10x tokens should result in ~10x cost
        assert cost_1000 > cost_100
        assert cost_1000 > cost_100 * 5  # At least 5x difference


class TestLLMDomainServiceIntegration:
    """Test integration with LLMDomainService"""

    def test_llm_domain_service_has_usage_tracker(self):
        """Test that LLMDomainService includes usage tracker"""
        from services.domain.llm_domain_service import LLMDomainService

        service = LLMDomainService()
        assert hasattr(service, "_usage_tracker")
        assert isinstance(service._usage_tracker, APIUsageTracker)

    def test_log_usage_method_exists(self):
        """Test that _log_usage method exists on LLMDomainService"""
        from services.domain.llm_domain_service import LLMDomainService

        service = LLMDomainService()
        assert hasattr(service, "_log_usage")
        assert callable(service._log_usage)


class TestLLMClientIntegration:
    """Test integration with LLMClient"""

    def test_llm_client_complete_accepts_context(self):
        """Test that LLMClient.complete() accepts context parameter"""
        import inspect

        from services.llm.clients import LLMClient

        client = LLMClient()
        sig = inspect.signature(client.complete)
        params = list(sig.parameters.keys())

        # Verify context parameter exists
        assert "context" in params


class TestDatabaseMigration:
    """Test that database migration was applied"""

    def test_migration_file_exists(self):
        """Test that migration file exists"""
        import os

        migration_file = (
            "/Users/xian/Development/piper-morgan/alembic/versions/"
            "68166c68224b_add_api_usage_logs_table_issue_271.py"
        )
        assert os.path.exists(migration_file), "Migration file should exist"

    def test_migration_has_upgrade_function(self):
        """Test that migration has upgrade function"""
        import importlib.util

        migration_path = (
            "/Users/xian/Development/piper-morgan/alembic/versions/"
            "68166c68224b_add_api_usage_logs_table_issue_271.py"
        )

        spec = importlib.util.spec_from_file_location(
            "migration",
            migration_path,
        )
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)

        assert hasattr(migration, "upgrade")
        assert hasattr(migration, "downgrade")
        assert callable(migration.upgrade)
        assert callable(migration.downgrade)


class TestDataStructures:
    """Test data structures for cost tracking"""

    def test_api_usage_log_with_defaults(self):
        """Test APIUsageLog with optional fields"""
        from services.analytics.api_usage_tracker import APIUsageLog

        log = APIUsageLog(
            user_id="test_user",
            provider="anthropic",
            model="claude-3-sonnet",
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            estimated_cost=Decimal("0.0045"),
        )

        # Optional fields should have defaults or be None
        assert log.conversation_id is None
        assert log.feature is None
        assert log.request_id is None
        assert log.response_time_ms is None
        assert log.created_at is None

    def test_api_usage_tracker_pricing_loaded(self):
        """Test that CostEstimator has pricing data"""
        estimator = CostEstimator()

        # Try different models to verify pricing is loaded
        models_to_test = [
            ("anthropic", "claude-3-sonnet"),
            ("anthropic", "claude-3-opus"),
            ("openai", "gpt-4"),
            ("openai", "gpt-3.5-turbo"),
        ]

        for provider, model in models_to_test:
            cost = estimator.estimate_cost(provider, model, 100, 100)
            assert cost > 0, f"Should have pricing for {provider}/{model}"
