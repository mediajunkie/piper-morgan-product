"""
Unit tests for canonical_handlers.py

Tests for CanonicalHandlers class, focusing on:
- _get_dynamic_capabilities() method (Issue #493)
- Plugin registry integration
- Error handling for registry failures
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.plugins.plugin_interface import PluginMetadata


@pytest.fixture
def canonical_handlers():
    """Fixture to create CanonicalHandlers instance"""
    return CanonicalHandlers()


@pytest.fixture
def mock_plugin_registry():
    """Fixture to create a mock PluginRegistry"""
    registry = MagicMock()

    # Mock get_status_all to return status for configured plugins
    registry.get_status_all.return_value = {
        "slack": {"configured": True, "active": True, "status": "active"},
        "github": {"configured": True, "active": False, "status": "inactive"},
        "notion": {"configured": False, "active": False, "status": "not_configured"},
    }

    # Mock get_plugin to return plugin instances with metadata
    def get_plugin_side_effect(name):
        if name == "slack":
            plugin = MagicMock()
            plugin.get_metadata.return_value = PluginMetadata(
                name="slack",
                version="1.0.0",
                description="Slack integration for team communication",
                author="Piper Team",
                capabilities=["channels", "messages", "spatial"],
            )
            return plugin
        elif name == "github":
            plugin = MagicMock()
            plugin.get_metadata.return_value = PluginMetadata(
                name="github",
                version="1.0.0",
                description="GitHub integration for issue tracking",
                author="Piper Team",
                capabilities=["issues", "pull_requests", "webhooks"],
            )
            return plugin
        else:
            return None

    registry.get_plugin.side_effect = get_plugin_side_effect

    return registry


class TestGetDynamicCapabilities:
    """Test suite for _get_dynamic_capabilities() method"""

    @pytest.fixture(autouse=True)
    def _isolate_workflow_registry(self):
        """#923: Isolate from workflow registry side effects in other tests."""
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value={},
        ):
            yield

    def test_returns_expected_structure(self, canonical_handlers, mock_plugin_registry):
        """
        Test that _get_dynamic_capabilities() returns the expected dict structure
        with 'core', 'integrations', and 'capabilities_list' keys.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert
        assert isinstance(result, dict)
        assert "core" in result
        assert "integrations" in result
        assert "capabilities_list" in result

        # Verify structure types
        assert isinstance(result["core"], list)
        assert isinstance(result["integrations"], list)
        assert isinstance(result["capabilities_list"], list)

    def test_core_capabilities_always_present(self, canonical_handlers, mock_plugin_registry):
        """
        Test that core PM capabilities are always included regardless of plugin state.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Core capabilities should be present (#923: now conversational)
        core = result["core"]
        assert "conversational PM guidance" in core
        assert "strategic thinking and prioritization" in core
        assert len(core) == 2

    def test_includes_active_plugins(self, canonical_handlers, mock_plugin_registry):
        """
        Test that active and configured plugins are included in integrations list.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Should include slack (active) and github (configured)
        integrations = result["integrations"]
        assert len(integrations) == 2

        # Check slack integration
        slack_integration = next((i for i in integrations if i["name"] == "slack"), None)
        assert slack_integration is not None
        assert slack_integration["description"] == "Slack integration for team communication"
        assert "channels" in slack_integration["capabilities"]

        # Check github integration
        github_integration = next((i for i in integrations if i["name"] == "github"), None)
        assert github_integration is not None
        assert github_integration["description"] == "GitHub integration for issue tracking"
        assert "issues" in github_integration["capabilities"]

    def test_excludes_unconfigured_plugins(self, canonical_handlers, mock_plugin_registry):
        """
        Test that unconfigured and inactive plugins are excluded from integrations.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Notion should NOT be included (not configured, not active)
        integrations = result["integrations"]
        notion_names = [i["name"] for i in integrations]
        assert "notion" not in notion_names

    def test_capabilities_list_includes_all(self, canonical_handlers, mock_plugin_registry):
        """
        Test that capabilities_list includes core capabilities plus integration names.
        #923: Also includes workflow capabilities from dispatcher registry.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert
        capabilities_list = result["capabilities_list"]

        # #923: Should contain core conversational capabilities
        assert "conversational PM guidance" in capabilities_list
        assert "strategic thinking and prioritization" in capabilities_list

        # Should contain integration summaries
        assert "slack integration" in capabilities_list
        assert "github integration" in capabilities_list

        # Total should be 2 core + 0 workflows + 2 integrations = 4
        assert len(capabilities_list) == 4

    def test_handles_registry_unavailable(self, canonical_handlers):
        """
        Test that method gracefully handles PluginRegistry being unavailable.
        Should return core capabilities only without raising exception.
        """
        # Arrange - Mock get_plugin_registry to raise exception
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry"
        ) as mock_get_registry:
            mock_get_registry.side_effect = Exception("Registry not available")

            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Should still return valid structure with core capabilities
        assert isinstance(result, dict)
        assert "core" in result
        assert "integrations" in result
        assert "capabilities_list" in result

        # #923: Core conversational capabilities should be present
        assert len(result["core"]) == 2

        # Integrations should be empty list (not None)
        assert result["integrations"] == []

        # Capabilities list should only have core (no workflows, no integrations)
        assert len(result["capabilities_list"]) == 2

    def test_handles_plugin_metadata_error(self, canonical_handlers, mock_plugin_registry):
        """
        Test that method handles errors when getting plugin metadata.
        Current implementation: entire plugin processing aborts on first error.
        Returns core capabilities only.
        """

        # Arrange - Make slack plugin raise error on get_metadata
        def get_plugin_error_side_effect(name):
            if name == "slack":
                plugin = MagicMock()
                plugin.get_metadata.side_effect = Exception("Metadata error")
                return plugin
            elif name == "github":
                plugin = MagicMock()
                plugin.get_metadata.return_value = PluginMetadata(
                    name="github",
                    version="1.0.0",
                    description="GitHub integration for issue tracking",
                    author="Piper Team",
                    capabilities=["issues", "pull_requests"],
                )
                return plugin
            return None

        mock_plugin_registry.get_plugin.side_effect = get_plugin_error_side_effect

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Current implementation: entire loop aborts on error
        # So no integrations are returned (caught by broad exception handler)
        integrations = result["integrations"]
        assert len(integrations) == 0  # No plugins included due to error

        # #923: Core conversational capabilities should still be present
        assert len(result["core"]) == 2
        assert len(result["capabilities_list"]) == 2

    def test_empty_plugin_registry(self, canonical_handlers):
        """
        Test behavior when plugin registry has no plugins registered.
        Should return only core capabilities.
        """
        # Arrange
        empty_registry = MagicMock()
        empty_registry.get_status_all.return_value = {}

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=empty_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert — #923: core is now 2 conversational capabilities
        assert len(result["core"]) == 2
        assert len(result["integrations"]) == 0
        assert len(result["capabilities_list"]) == 2

    def test_plugin_returns_none(self, canonical_handlers):
        """
        Test that method handles when get_plugin returns None for a plugin.
        Should skip that plugin gracefully.
        """
        # Arrange - Create fresh mock with get_plugin returning None
        registry = MagicMock()
        registry.get_status_all.return_value = {
            "slack": {"configured": True, "active": True},
            "github": {"configured": True, "active": False},
        }
        # All get_plugin calls return None
        registry.get_plugin.return_value = None

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry", return_value=registry
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Should have core but no integrations (plugins returned None)
        # #923: core is now 2 conversational capabilities
        assert len(result["core"]) == 2
        assert len(result["integrations"]) == 0
        assert len(result["capabilities_list"]) == 2


class TestLastActivityDetection:
    """Test suite for _detect_last_activity_request() method (Issue #504)"""

    def test_detects_last_time_worked_on_pattern(self, canonical_handlers):
        """Test detection of 'last time we worked on X' pattern."""
        # Arrange
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="When was the last time we worked on project alpha?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_last_activity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert
        assert result == "project alpha"

    def test_detects_when_did_we_work_on_pattern(self, canonical_handlers):
        """Test detection of 'when did we work on X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="When did we work on HealthTrack?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_last_activity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert (note: detection returns lowercase from regex)
        assert result == "healthtrack"

    def test_detects_last_worked_on_pattern(self, canonical_handlers):
        """Test detection of 'last worked on X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="When was the last worked on the backend?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_last_activity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert
        assert result == "the backend"

    def test_detects_last_touched_pattern(self, canonical_handlers):
        """Test detection of 'last touched X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="When was the last time we touched the API?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_last_activity",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert (note: detection returns lowercase from regex)
        assert result == "the api"

    def test_returns_none_for_non_matching_query(self, canonical_handlers):
        """Test that non-matching queries return None."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What day is it?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_current_time",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert
        assert result is None

    def test_returns_none_for_empty_message(self, canonical_handlers):
        """Test that empty messages return None."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_time",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_last_activity_request(intent)

        # Assert
        assert result is None


class TestProjectDurationDetection:
    """Test suite for _detect_duration_request() method (Issue #505)"""

    def test_detects_how_long_working_on_pattern(self, canonical_handlers):
        """Test detection of 'how long have we been working on X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How long have we been working on project alpha?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_project_duration",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result == "project alpha"

    def test_detects_how_long_been_on_pattern(self, canonical_handlers):
        """Test detection of 'how long have we been on X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How long have we been on HealthTrack?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_project_duration",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result == "healthtrack"

    def test_detects_when_did_we_start_pattern(self, canonical_handlers):
        """Test detection of 'when did we start X' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="When did we start the backend project?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_project_duration",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result == "the backend project"

    def test_detects_this_project_pattern(self, canonical_handlers):
        """Test detection of 'how long this project' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How long have we been on this project?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_project_duration",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result == "this project"

    def test_returns_none_for_non_matching_query(self, canonical_handlers):
        """Test that non-matching queries return None."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What is the project status?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result is None

    def test_returns_none_for_empty_message(self, canonical_handlers):
        """Test that empty messages return None."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_time",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_duration_request(intent)

        # Assert
        assert result is None


class TestPriorityRecommendationDetection:
    """Test suite for _detect_priority_recommendation_request() method (Issue #511)"""

    def test_detects_which_project_focus_pattern(self, canonical_handlers):
        """Test detection of 'which project should I focus on' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Which project should I focus on?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is True

    def test_detects_what_project_work_pattern(self, canonical_handlers):
        """Test detection of 'what project should I work on' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What project should I work on next?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is True

    def test_detects_what_should_prioritize_pattern(self, canonical_handlers):
        """Test detection of 'what should I prioritize' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What should I prioritize this week?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is True

    def test_detects_most_important_pattern(self, canonical_handlers):
        """Test detection of 'what's most important' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's most important to work on?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is True

    def test_detects_focus_on_pattern(self, canonical_handlers):
        """Test detection of 'what should I focus on' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What should I focus on right now?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is True

    def test_returns_false_for_non_matching_query(self, canonical_handlers):
        """Test that non-matching queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What are my priorities?",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_empty_message(self, canonical_handlers):
        """Test that empty messages return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.PRIORITY,
            action="query_priority",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_priority_recommendation_request(intent)

        # Assert
        assert result is False


class TestPriorityScoreCalculation:
    """Test suite for _calculate_priority_score() method (Issue #511)"""

    def test_calculates_score_with_staleness(self, canonical_handlers):
        """Test priority score calculation with staleness factor."""
        from datetime import datetime, timedelta

        # Arrange - Project inactive for 20 days
        last_update = (datetime.now() - timedelta(days=20)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 5}

        # Act
        result = canonical_handlers._calculate_priority_score("TestProject", github_data)

        # Assert
        assert result["score"] >= 20  # Should have staleness points
        assert result["breakdown"]["staleness"] == 20
        assert "days since last activity" in result["top_reason"]

    def test_calculates_score_with_many_issues(self, canonical_handlers):
        """Test priority score calculation with high issue count."""
        from datetime import datetime, timedelta

        # Arrange - Recent activity but many issues
        last_update = (datetime.now() - timedelta(days=5)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 15}

        # Act
        result = canonical_handlers._calculate_priority_score("TestProject", github_data)

        # Assert
        assert result["score"] > 0
        assert result["breakdown"]["issue_count"] > 0
        assert "open issues" in result["top_reason"]

    def test_calculates_score_with_urgency(self, canonical_handlers):
        """Test priority score calculation with high-priority issues."""
        from datetime import datetime, timedelta

        # Arrange - Project with high-priority issues
        last_update = (datetime.now() - timedelta(days=10)).isoformat()
        github_data = {
            "updated_at": last_update,
            "open_issues_count": 8,
            "issues_preview": [
                {
                    "number": 1,
                    "title": "Critical bug",
                    "labels": [{"name": "critical"}],
                },
                {
                    "number": 2,
                    "title": "High priority feature",
                    "labels": [{"name": "high-priority"}],
                },
            ],
        }

        # Act
        result = canonical_handlers._calculate_priority_score("TestProject", github_data)

        # Assert
        assert result["breakdown"]["urgency"] > 0
        # Top reason will be first reason added (issue count in this case)
        assert "open issues" in result["top_reason"]

    def test_handles_missing_github_data(self, canonical_handlers):
        """Test priority score calculation with no GitHub data."""
        # Act
        result = canonical_handlers._calculate_priority_score("TestProject", None)

        # Assert
        assert result["score"] == 0
        assert result["top_reason"] == "No GitHub data available"

    def test_handles_active_project_low_issues(self, canonical_handlers):
        """Test priority score for active project with few issues."""
        from datetime import datetime, timedelta

        # Arrange - Recent activity, few issues
        last_update = (datetime.now() - timedelta(days=3)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 2}

        # Act
        result = canonical_handlers._calculate_priority_score("TestProject", github_data)

        # Assert
        assert result["score"] < 20  # Should have low score
        # With 2 issues, we get "2 open issues" as reason
        assert "2 open issues" in result["top_reason"]


class TestPriorityRecommendationFormatting:
    """Test suite for priority recommendation formatting methods (Issue #511)"""

    def test_format_embedded_with_projects(self, canonical_handlers):
        """Test EMBEDDED format with ranked projects."""
        # Arrange
        ranked_projects = [
            {
                "name": "HighPriority",
                "score": 80,
                "top_reason": "30 days since last activity",
                "breakdown": {"staleness": 30, "issue_count": 30, "urgency": 20},
            },
            {
                "name": "LowPriority",
                "score": 10,
                "top_reason": "Active and low issue count",
                "breakdown": {"staleness": 0, "issue_count": 10, "urgency": 0},
            },
        ]

        # Act
        result = canonical_handlers._format_priority_embedded(ranked_projects)

        # Assert
        assert result == "Focus on: HighPriority"

    def test_format_embedded_no_projects(self, canonical_handlers):
        """Test EMBEDDED format with no projects."""
        # Act
        result = canonical_handlers._format_priority_embedded([])

        # Assert
        assert result == "No projects to prioritize"

    def test_format_standard_with_projects(self, canonical_handlers):
        """Test STANDARD format with ranked projects."""
        # Arrange
        ranked_projects = [
            {
                "name": "Project1",
                "score": 70,
                "top_reason": "25 days since last activity",
                "breakdown": {"staleness": 25, "issue_count": 30, "urgency": 15},
            },
            {
                "name": "Project2",
                "score": 50,
                "top_reason": "15 open issues",
                "breakdown": {"staleness": 0, "issue_count": 30, "urgency": 20},
            },
            {
                "name": "Project3",
                "score": 30,
                "top_reason": "10 open issues",
                "breakdown": {"staleness": 0, "issue_count": 30, "urgency": 0},
            },
        ]

        # Act
        result = canonical_handlers._format_priority_standard(ranked_projects)

        # Assert
        assert "Priority Recommendation" in result
        assert "1. **Project1**" in result
        assert "2. **Project2**" in result
        assert "3. **Project3**" in result
        assert "(Score: 70)" in result
        assert "25 days since last activity" in result

    def test_format_standard_with_many_projects(self, canonical_handlers):
        """Test STANDARD format shows only top 3 plus count."""
        # Arrange
        ranked_projects = [
            {
                "name": f"Project{i}",
                "score": 100 - i * 10,
                "top_reason": "Test reason",
                "breakdown": {},
            }
            for i in range(5)
        ]

        # Act
        result = canonical_handlers._format_priority_standard(ranked_projects)

        # Assert
        assert "Plus 2 more projects" in result

    def test_format_granular_with_projects(self, canonical_handlers):
        """Test GRANULAR format with full details."""
        # Arrange
        ranked_projects = [
            {
                "name": "DetailedProject",
                "score": 90,
                "top_reason": "35 days since last activity",
                "breakdown": {"staleness": 35, "issue_count": 30, "urgency": 25},
                "github_data": {
                    "open_issues_count": 12,
                    "updated_at": "2025-11-15T10:00:00Z",
                },
            }
        ]

        # Act
        result = canonical_handlers._format_priority_granular(ranked_projects)

        # Assert
        assert "Full Priority Analysis" in result
        assert "DetailedProject" in result
        assert "Priority Score**: 90/100" in result
        assert "Staleness: 35/40 points" in result
        assert "Issue Count: 30/30 points" in result
        assert "Urgency: 25/30 points" in result
        assert "Open Issues: 12" in result


class TestProjectDurationCalculation:
    """Test suite for project duration calculation (Issue #505)"""

    def test_calculate_duration_with_valid_date(self, canonical_handlers):
        """Test duration calculation with a valid ISO date string."""
        from datetime import datetime, timedelta

        # Arrange - 45 days ago
        start_date = datetime.now() - timedelta(days=45)
        created_at = start_date.isoformat()

        # Act
        result = canonical_handlers._calculate_duration(created_at)

        # Assert
        assert result is not None
        assert result["total_days"] == 45
        assert result["months"] == 1  # 45 // 30 = 1
        assert result["weeks"] == 2  # (45 % 30) // 7 = 2
        assert result["days"] == 1  # ((45 % 30) % 7) = 1

    def test_calculate_duration_with_datetime_object(self, canonical_handlers):
        """Test duration calculation with a datetime object."""
        from datetime import datetime, timedelta

        # Arrange - 10 days ago
        start_date = datetime.now() - timedelta(days=10)

        # Act
        result = canonical_handlers._calculate_duration(start_date)

        # Assert
        assert result is not None
        assert result["total_days"] == 10
        assert result["months"] == 0
        assert result["weeks"] == 1
        assert result["days"] == 3

    def test_calculate_duration_with_recent_start(self, canonical_handlers):
        """Test duration calculation with very recent start date."""
        from datetime import datetime, timedelta

        # Arrange - 2 days ago
        start_date = datetime.now() - timedelta(days=2)
        created_at = start_date.isoformat()

        # Act
        result = canonical_handlers._calculate_duration(created_at)

        # Assert
        assert result is not None
        assert result["total_days"] == 2
        assert result["months"] == 0
        assert result["weeks"] == 0
        assert result["days"] == 2

    def test_calculate_duration_handles_invalid_date(self, canonical_handlers):
        """Test that invalid dates return None."""
        # Act
        result = canonical_handlers._calculate_duration("not-a-date")

        # Assert
        assert result is None


class TestProjectDurationFormatting:
    """Test suite for project duration formatting methods (Issue #505)"""

    def test_format_embedded_with_months(self, canonical_handlers):
        """Test EMBEDDED format with duration in months."""
        # Arrange
        duration = {"total_days": 90, "months": 3, "weeks": 0, "days": 0}

        # Act
        result = canonical_handlers._format_duration_embedded("TestProject", duration)

        # Assert
        assert result == "TestProject: 3 months"

    def test_format_embedded_with_single_month(self, canonical_handlers):
        """Test EMBEDDED format with single month (no 's')."""
        # Arrange
        duration = {"total_days": 30, "months": 1, "weeks": 0, "days": 0}

        # Act
        result = canonical_handlers._format_duration_embedded("TestProject", duration)

        # Assert
        assert result == "TestProject: 1 month"

    def test_format_embedded_with_days(self, canonical_handlers):
        """Test EMBEDDED format with duration in days only."""
        # Arrange
        duration = {"total_days": 15, "months": 0, "weeks": 2, "days": 1}

        # Act
        result = canonical_handlers._format_duration_embedded("TestProject", duration)

        # Assert
        assert result == "TestProject: 15 days"

    def test_format_embedded_without_duration(self, canonical_handlers):
        """Test EMBEDDED format with no duration data."""
        # Act
        result = canonical_handlers._format_duration_embedded("TestProject", None)

        # Assert
        assert result == "TestProject: unknown duration"

    def test_format_standard_with_duration(self, canonical_handlers):
        """Test STANDARD format with duration data."""
        from datetime import datetime

        # Arrange
        start_date = datetime(2025, 11, 1)
        duration = {
            "total_days": 51,
            "months": 1,
            "weeks": 3,
            "days": 0,
            "start_date": start_date,
        }

        # Act
        result = canonical_handlers._format_duration_standard("TestProject", duration, None)

        # Assert
        assert "You've been working on **TestProject**" in result
        assert "1 month and 3 weeks" in result
        assert "started November 01, 2025" in result

    def test_format_standard_without_duration(self, canonical_handlers):
        """Test STANDARD format with no duration data."""
        # Act
        result = canonical_handlers._format_duration_standard("TestProject", None, None)

        # Assert
        assert "I don't have start date information for **TestProject**" in result
        assert "Check if the project is configured" in result

    def test_format_granular_with_duration(self, canonical_handlers):
        """Test GRANULAR format with duration data."""
        from datetime import datetime

        # Arrange
        start_date = datetime(2025, 10, 15)
        duration = {
            "total_days": 68,
            "months": 2,
            "weeks": 1,
            "days": 1,
            "start_date": start_date,
        }

        # Act
        result = canonical_handlers._format_duration_granular("TestProject", duration, None)

        # Assert
        assert "**Project Duration: TestProject**" in result
        assert "**Started**: Wednesday, October 15, 2025" in result
        assert "**Total Days**: 68" in result
        assert "**Breakdown**:" in result
        assert "- Months: 2" in result
        assert "- Weeks: 1" in result
        assert "- Days: 1" in result

    def test_format_granular_without_duration(self, canonical_handlers):
        """Test GRANULAR format with no duration data."""
        # Act
        result = canonical_handlers._format_duration_granular("TestProject", None, None)

        # Assert
        assert "**TestProject** duration unknown" in result
        assert "may not be configured with a start date" in result
        assert "Check Settings → Projects" in result


class TestLastActivityFormatting:
    """Test suite for last activity formatting methods (Issue #504)"""

    def test_format_embedded_with_activity_today(self, canonical_handlers):
        """Test EMBEDDED format with activity from today."""
        from datetime import datetime

        # Arrange
        activity = {
            "type": "commit",
            "date": datetime.now().isoformat(),
            "title": "Fix bug in handler",
        }

        # Act
        result = canonical_handlers._format_last_activity_embedded("TestProject", activity)

        # Assert
        assert "TestProject: today" == result

    def test_format_embedded_with_activity_yesterday(self, canonical_handlers):
        """Test EMBEDDED format with activity from yesterday."""
        from datetime import datetime, timedelta

        # Arrange
        yesterday = datetime.now() - timedelta(days=1)
        activity = {
            "type": "commit",
            "date": yesterday.isoformat(),
            "title": "Update documentation",
        }

        # Act
        result = canonical_handlers._format_last_activity_embedded("TestProject", activity)

        # Assert
        assert "TestProject: yesterday" == result

    def test_format_embedded_with_activity_days_ago(self, canonical_handlers):
        """Test EMBEDDED format with activity from several days ago."""
        from datetime import datetime, timedelta

        # Arrange
        five_days_ago = datetime.now() - timedelta(days=5)
        activity = {"type": "commit", "date": five_days_ago.isoformat(), "title": "Refactor code"}

        # Act
        result = canonical_handlers._format_last_activity_embedded("TestProject", activity)

        # Assert
        assert "TestProject: 5 days ago" == result

    def test_format_embedded_without_activity(self, canonical_handlers):
        """Test EMBEDDED format with no activity data."""
        # Act
        result = canonical_handlers._format_last_activity_embedded("TestProject", None)

        # Assert
        assert result == "TestProject: no recent activity"

    def test_format_standard_with_activity(self, canonical_handlers):
        """Test STANDARD format with activity data."""
        from datetime import datetime

        # Arrange
        activity = {
            "type": "pull_request",
            "date": "2025-12-21T10:30:00Z",
            "title": "Add new feature for user authentication",
        }

        # Act
        result = canonical_handlers._format_last_activity_standard("TestProject", activity)

        # Assert
        assert "Last activity on **TestProject**" in result
        assert "pull_request" in result
        assert "December 21, 2025" in result
        assert "Add new feature for user authentication" in result

    def test_format_standard_without_activity(self, canonical_handlers):
        """Test STANDARD format with no activity data."""
        # Act
        result = canonical_handlers._format_last_activity_standard("TestProject", None)

        # Assert
        assert "I don't have recent activity data for TestProject" in result
        assert "GitHub integration may need to be configured" in result

    def test_format_granular_with_activity(self, canonical_handlers):
        """Test GRANULAR format with activity data."""
        from datetime import datetime

        # Arrange
        activity = {
            "type": "issue",
            "date": "2025-12-20T15:45:00Z",
            "title": "Bug: Application crashes on startup",
        }

        # Act
        result = canonical_handlers._format_last_activity_granular("TestProject", activity)

        # Assert
        assert "**Last Activity on TestProject**" in result
        assert "**Date**:" in result
        assert "**Time Since**:" in result
        assert "**Type**: issue" in result
        assert "**Description**: Bug: Application crashes on startup" in result

    def test_format_granular_without_activity(self, canonical_handlers):
        """Test GRANULAR format with no activity data."""
        # Act
        result = canonical_handlers._format_last_activity_granular("TestProject", None)

        # Assert
        assert "No recent activity found for **TestProject**" in result
        assert "No commits, issues, or PRs in the last 30 days" in result
        assert "GitHub integration not configured" in result


class TestSetupRequestDetection:
    """Tests for _detect_setup_request() method - Issue #498."""

    def test_detects_project_setup(self, canonical_handlers):
        """Detects 'set up my projects' as projects setup."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Help me set up my projects",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result == "projects"

    def test_detects_configure_projects(self, canonical_handlers):
        """Detects 'configure my projects' as projects setup."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="I want to configure my project portfolio",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result == "projects"

    def test_detects_integration_setup(self, canonical_handlers):
        """Detects 'set up integrations' as integrations setup."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Help me set up my integrations",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result == "integrations"

    def test_detects_connect_github(self, canonical_handlers):
        """Detects 'connect github' as integrations setup."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="I want to connect my GitHub account",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result == "integrations"

    def test_detects_general_setup(self, canonical_handlers):
        """Detects 'get started with piper' as general setup."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How do I get started with Piper?",
            category=IntentCategoryEnum.GUIDANCE,
            action="request_setup_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result == "general"

    def test_returns_none_for_non_setup(self, canonical_handlers):
        """Returns None for non-setup queries."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's on my agenda today?",
            category=IntentCategoryEnum.QUERY,
            action="query_agenda",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result is None

    def test_handles_empty_intent(self, canonical_handlers):
        """Returns None for empty/None intent."""
        result = canonical_handlers._detect_setup_request(None)
        assert result is None

    def test_handles_missing_message(self, canonical_handlers):
        """Returns None for intent without message."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message=None,
            category=IntentCategoryEnum.GUIDANCE,
            action="request_guidance",
            confidence=0.9,
        )

        result = canonical_handlers._detect_setup_request(intent)
        assert result is None


class TestSetupGuidanceFormatting:
    """Tests for setup guidance formatting methods - Issue #498."""

    def test_project_setup_no_existing_projects(self, canonical_handlers):
        """Project setup guidance when user has no projects."""
        result = canonical_handlers._format_project_setup_guidance(None)

        assert "message" in result
        assert "set up your projects" in result["message"].lower()
        assert "/settings/projects" in result["message"]
        assert result["intent"]["action"] == "provide_setup_guidance"
        assert result["setup_type"] == "projects"

    def test_project_setup_with_existing_projects(self, canonical_handlers):
        """Project setup guidance when user has projects."""
        user_context = MagicMock()
        user_context.projects = ["Project A", "Project B"]

        result = canonical_handlers._format_project_setup_guidance(user_context)

        assert "message" in result
        assert "2 project(s)" in result["message"]
        assert "Project A" in result["message"]
        assert "/settings/projects" in result["message"]

    def test_integration_setup_guidance(self, canonical_handlers):
        """Integration setup guidance."""
        result = canonical_handlers._format_integration_setup_guidance()

        assert "message" in result
        assert result["setup_type"] == "integrations"

    def test_general_setup_guidance(self, canonical_handlers):
        """General setup guidance."""
        result = canonical_handlers._format_general_setup_guidance()

        assert "message" in result
        assert result["setup_type"] == "general"


class TestProjectListDetection:
    """Test suite for _detect_project_list_request() method (Issue #509)"""

    def test_detects_what_projects_pattern(self, canonical_handlers):
        """Test detection of 'what projects' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What projects are we working on?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        result = canonical_handlers._detect_project_list_request(intent)
        assert result is True

    def test_detects_list_projects_pattern(self, canonical_handlers):
        """Test detection of 'list projects' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="List all projects",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        result = canonical_handlers._detect_project_list_request(intent)
        assert result is True

    def test_detects_show_projects_pattern(self, canonical_handlers):
        """Test detection of 'show projects' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Show me my projects",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        result = canonical_handlers._detect_project_list_request(intent)
        assert result is True

    def test_returns_false_for_non_list_query(self, canonical_handlers):
        """Test that non-list queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's the status of HealthTrack?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        result = canonical_handlers._detect_project_list_request(intent)
        assert result is False


class TestProjectListFormatting:
    """Test suite for project list formatting methods (Issue #509)"""

    def test_format_embedded_with_projects(self, canonical_handlers):
        """Test EMBEDDED format with project list."""
        projects = ["HealthTrack", "MediHub", "CarePro"]

        result = canonical_handlers._format_project_list_embedded(projects, {})

        assert result == "You have 3 active projects: HealthTrack, MediHub, CarePro"

    def test_format_embedded_no_projects(self, canonical_handlers):
        """Test EMBEDDED format with no projects."""
        result = canonical_handlers._format_project_list_embedded([], {})

        assert result == "No active projects"

    def test_format_standard_with_github(self, canonical_handlers):
        """Test STANDARD format with GitHub metadata."""
        projects = ["HealthTrack", "MediHub"]
        metadata = {
            "HealthTrack": {
                "has_github": True,
                "open_issues_count": 12,
                "recent_issues": [
                    {"number": 123, "title": "Fix authentication bug"},
                    {"number": 124, "title": "Add user settings page"},
                ],
            },
            "MediHub": {"has_github": False},
        }

        result = canonical_handlers._format_project_list_standard(projects, metadata)

        # Verify key content elements are present
        assert "active projects" in result.lower()
        assert "HealthTrack" in result
        assert "MediHub" in result
        assert "12 open issues" in result

    def test_format_granular_without_github(self, canonical_handlers):
        """Test GRANULAR format without GitHub connection."""
        # Arrange
        projects = ["HealthTrack"]
        metadata = {"HealthTrack": {"has_github": False}}

        # Act
        result = canonical_handlers._format_project_list_granular(projects, metadata)

        # Assert - verify key content is present
        assert "HealthTrack" in result
        assert "active project" in result.lower() or "project" in result.lower()


class TestLandscapeDetection:
    """Test suite for _detect_landscape_request() method (Issue #510)"""

    def test_detects_project_landscape_pattern(self, canonical_handlers):
        """Test detection of 'project landscape' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Show me the project landscape",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is True

    def test_detects_portfolio_pattern(self, canonical_handlers):
        """Test detection of 'portfolio' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's my portfolio looking like?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is True

    def test_detects_project_overview_pattern(self, canonical_handlers):
        """Test detection of 'project overview' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Give me a project overview",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is True

    def test_detects_portfolio_health_pattern(self, canonical_handlers):
        """Test detection of 'portfolio health' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Show me portfolio health",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is True

    def test_detects_all_projects_health_pattern(self, canonical_handlers):
        """Test detection of 'all projects health' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How are all projects health?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is True

    def test_returns_false_for_non_landscape_query(self, canonical_handlers):
        """Test that non-landscape queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What am I working on?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_empty_message(self, canonical_handlers):
        """Test that empty messages return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_landscape_request(intent)

        # Assert
        assert result is False


class TestProjectHealthCalculation:
    """Test suite for _calculate_project_health() method (Issue #510)"""

    def test_calculates_healthy_status(self, canonical_handlers):
        """Test health calculation for recently active project."""
        from datetime import datetime, timedelta

        # Arrange - Project active 7 days ago
        last_update = (datetime.now() - timedelta(days=7)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 5}

        # Act
        result = canonical_handlers._calculate_project_health("TestProject", github_data)

        # Assert
        assert result["status"] == "healthy"
        assert "7 days" in result["reason"]

    def test_calculates_at_risk_status_by_time(self, canonical_handlers):
        """Test health calculation for project at risk due to time."""
        from datetime import datetime, timedelta

        # Arrange - Project active 20 days ago
        last_update = (datetime.now() - timedelta(days=20)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 5}

        # Act
        result = canonical_handlers._calculate_project_health("TestProject", github_data)

        # Assert
        assert result["status"] == "at-risk"
        assert "20 days" in result["reason"]

    def test_calculates_at_risk_status_by_issues(self, canonical_handlers):
        """Test health calculation for project at risk due to open issues."""
        from datetime import datetime, timedelta

        # Arrange - Project active recently but many issues
        last_update = (datetime.now() - timedelta(days=5)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 25}

        # Act
        result = canonical_handlers._calculate_project_health("TestProject", github_data)

        # Assert
        assert result["status"] == "at-risk"
        assert "25 open issues" in result["reason"]

    def test_calculates_stalled_status(self, canonical_handlers):
        """Test health calculation for stalled project."""
        from datetime import datetime, timedelta

        # Arrange - Project inactive for 45 days
        last_update = (datetime.now() - timedelta(days=45)).isoformat()
        github_data = {"updated_at": last_update, "open_issues_count": 3}

        # Act
        result = canonical_handlers._calculate_project_health("TestProject", github_data)

        # Assert
        assert result["status"] == "stalled"
        assert "45 days" in result["reason"]

    def test_handles_missing_github_data(self, canonical_handlers):
        """Test health calculation with no GitHub data."""
        # Act
        result = canonical_handlers._calculate_project_health("TestProject", None)

        # Assert
        assert result["status"] == "unknown"
        assert "No GitHub data" in result["reason"]

    def test_handles_missing_updated_at(self, canonical_handlers):
        """Test health calculation with missing updated_at field."""
        # Arrange
        github_data = {"open_issues_count": 15}

        # Act
        result = canonical_handlers._calculate_project_health("TestProject", github_data)

        # Assert - Should fall back to issue count
        assert result["status"] == "healthy"


class TestLandscapeFormatting:
    """Test suite for landscape formatting methods (Issue #510)"""

    def test_format_embedded_with_all_statuses(self, canonical_handlers):
        """Test EMBEDDED format with projects in all health categories."""
        # Arrange
        health_groups = {
            "healthy": [{"name": "Project A"}],
            "at-risk": [{"name": "Project B"}, {"name": "Project C"}],
            "stalled": [{"name": "Project D"}],
            "unknown": [],
        }

        # Act
        result = canonical_handlers._format_landscape_embedded(health_groups)

        # Assert
        assert "1 healthy" in result
        assert "2 at-risk" in result
        assert "1 stalled" in result

    def test_format_embedded_healthy_only(self, canonical_handlers):
        """Test EMBEDDED format with only healthy projects."""
        # Arrange
        health_groups = {
            "healthy": [{"name": "Project A"}, {"name": "Project B"}],
            "at-risk": [],
            "stalled": [],
            "unknown": [],
        }

        # Act
        result = canonical_handlers._format_landscape_embedded(health_groups)

        # Assert
        assert result == "Portfolio: 2 healthy"

    def test_format_embedded_no_projects(self, canonical_handlers):
        """Test EMBEDDED format with no projects."""
        # Arrange
        health_groups = {"healthy": [], "at-risk": [], "stalled": [], "unknown": []}

        # Act
        result = canonical_handlers._format_landscape_embedded(health_groups)

        # Assert
        assert "No projects configured" in result

    def test_format_standard_includes_project_names(self, canonical_handlers):
        """Test STANDARD format includes project names."""
        # Arrange
        health_groups = {
            "healthy": [{"name": "HealthyProject", "reason": "Active within 5 days"}],
            "at-risk": [
                {"name": "RiskyProject", "reason": "20 days since last activity"},
            ],
            "stalled": [
                {"name": "StalledProject", "reason": "45 days since last activity"},
            ],
            "unknown": [{"name": "UnknownProject", "reason": "No GitHub data"}],
        }

        # Act
        result = canonical_handlers._format_landscape_standard(health_groups)

        # Assert
        assert "Portfolio Health Overview" in result
        assert "HealthyProject" in result
        assert "RiskyProject" in result
        assert "StalledProject" in result
        assert "UnknownProject" in result
        assert "20 days since last activity" in result
        assert "45 days since last activity" in result

    def test_format_granular_includes_github_data(self, canonical_handlers):
        """Test GRANULAR format includes GitHub metadata."""
        # Arrange
        health_groups = {
            "healthy": [
                {
                    "name": "HealthyProject",
                    "reason": "Active within 5 days",
                    "github_data": {
                        "open_issues_count": 3,
                        "updated_at": "2025-12-20T10:00:00Z",
                    },
                }
            ],
            "at-risk": [],
            "stalled": [],
            "unknown": [],
        }

        # Act
        result = canonical_handlers._format_landscape_granular(health_groups)

        # Assert
        assert "Full Health Analysis" in result
        assert "HealthyProject" in result
        assert "Open Issues: 3" in result
        assert "Last Updated:" in result


class TestStatusReportDetection:
    """Test suite for _detect_status_report_request() method (Issue #513)"""

    def test_detects_status_report_pattern(self, canonical_handlers):
        """Test detection of 'status report' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Give me a status report",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_status_report_request(intent)

        # Assert
        assert result is True

    def test_detects_give_me_status_pattern(self, canonical_handlers):
        """Test detection of 'give me status' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Give me a status",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_status_report_request(intent)

        # Assert
        assert result is True

    def test_detects_project_status_pattern(self, canonical_handlers):
        """Test detection of 'project status' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's the project status?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_status_report_request(intent)

        # Assert
        assert result is True

    def test_detects_current_status_pattern(self, canonical_handlers):
        """Test detection of 'current status' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's the current status?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_status_report_request(intent)

        # Assert
        assert result is True

    def test_detects_how_are_things_going_pattern(self, canonical_handlers):
        """Test detection of 'how are things going' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How are things going?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_status_report_request(intent)

        # Assert
        assert result is True

    def test_returns_false_for_non_status_report_query(self, canonical_handlers):
        """Test that non-status-report queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Show me my projects",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_status_report_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_none_intent(self, canonical_handlers):
        """Test that None intent returns False."""
        # Act
        result = canonical_handlers._detect_status_report_request(None)

        # Assert
        assert result is False

    def test_returns_false_for_empty_message(self, canonical_handlers):
        """Test that empty message returns False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_status_report_request(intent)

        # Assert
        assert result is False


class TestRetrospectiveQuery:
    """Test suite for retrospective query detection and handling (Issue #501)"""

    def test_detects_what_did_we_accomplish_yesterday(self, canonical_handlers):
        """Test detection of 'what did we accomplish yesterday' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What did we accomplish yesterday?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_retrospective_request(intent)

        # Assert
        assert result is True

    def test_detects_what_did_we_do_yesterday(self, canonical_handlers):
        """Test detection of 'what did we do yesterday' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What did we do yesterday?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_retrospective_request(intent)

        # Assert
        assert result is True

    def test_detects_what_got_done_yesterday(self, canonical_handlers):
        """Test detection of 'what got done yesterday' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What got done yesterday?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_retrospective_request(intent)

        # Assert
        assert result is True

    def test_detects_finished_yesterday(self, canonical_handlers):
        """Test detection of 'finished yesterday' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What tasks finished yesterday?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_retrospective_request(intent)

        # Assert
        assert result is True

    def test_detects_completed_yesterday(self, canonical_handlers):
        """Test detection of 'completed yesterday' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What tasks were completed yesterday?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_retrospective_request(intent)

        # Assert
        assert result is True

    def test_detects_yesterdays_accomplishments(self, canonical_handlers):
        """Test detection of 'yesterday's accomplishments' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Show me yesterday's accomplishments",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_retrospective_request(intent)

        # Assert
        assert result is True

    def test_detects_yesterdays_progress(self, canonical_handlers):
        """Test detection of 'yesterday's progress' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What was yesterday's progress?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_retrospective_request(intent)

        # Assert
        assert result is True

    def test_detects_what_happened_yesterday(self, canonical_handlers):
        """Test detection of 'what happened yesterday' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What happened yesterday?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_retrospective_request(intent)

        # Assert
        assert result is True

    def test_returns_false_for_non_retrospective_query(self, canonical_handlers):
        """Test that non-retrospective queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's on my agenda today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_retrospective_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_empty_message(self, canonical_handlers):
        """Test that empty messages return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = canonical_handlers._detect_retrospective_request(intent)

        # Assert
        assert result is False

    def test_returns_false_for_none_intent(self, canonical_handlers):
        """Test that None intent returns False."""
        # Act
        result = canonical_handlers._detect_retrospective_request(None)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_handler_returns_correct_structure(self, canonical_handlers):
        """Test handler returns expected response structure."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What did we accomplish yesterday?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = await canonical_handlers._handle_retrospective_query(intent, "test_session")

        # Assert structure
        assert "message" in result
        assert "intent" in result
        assert result["intent"]["category"] == "temporal"
        assert result["intent"]["action"] == "provide_retrospective"
        assert result["intent"]["confidence"] == 1.0
        assert "retrospective" in result
        assert "completed_tasks" in result["retrospective"]
        assert result["requires_clarification"] is False

    @pytest.mark.asyncio
    async def test_handler_respects_spatial_pattern_embedded(self, canonical_handlers):
        """Test handler uses EMBEDDED format for embedded spatial pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What did we accomplish yesterday?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )
        intent.spatial_context = {"pattern": "EMBEDDED"}

        # Act
        result = await canonical_handlers._handle_retrospective_query(intent, "test_session")

        # Assert - EMBEDDED format should be brief
        assert result["spatial_pattern"] == "EMBEDDED"
        # Should match format: "Month Day: N tasks completed"
        assert "tasks completed" in result["message"] or "No completed tasks" in result["message"]
        assert len(result["message"]) < 100  # Brief format

    @pytest.mark.asyncio
    async def test_handler_respects_spatial_pattern_granular(self, canonical_handlers):
        """Test handler uses GRANULAR format for granular spatial pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What did we accomplish yesterday?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )
        intent.spatial_context = {"pattern": "GRANULAR"}

        # Act
        result = await canonical_handlers._handle_retrospective_query(intent, "test_session")

        # Assert - GRANULAR format should be detailed
        assert result["spatial_pattern"] == "GRANULAR"
        # Should match format: "# Yesterday's Accomplishments"
        assert "Yesterday's Accomplishments" in result["message"]

    @pytest.mark.asyncio
    async def test_handler_uses_standard_format_by_default(self, canonical_handlers):
        """Test handler uses STANDARD format when no spatial pattern is set."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What did we accomplish yesterday?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_retrospective",
            confidence=0.9,
        )

        # Act
        result = await canonical_handlers._handle_retrospective_query(intent, "test_session")

        # Assert - STANDARD format should be used
        assert result["spatial_pattern"] is None
        # Should match format: "**Yesterday's Accomplishments**"
        assert "Yesterday's Accomplishments" in result["message"]

    def test_format_embedded_with_tasks(self, canonical_handlers):
        """Test EMBEDDED format with completed tasks."""
        from datetime import datetime

        # Arrange
        target_date = datetime(2025, 12, 21)
        completed_todos = [
            {"title": "Task 1", "priority": "high"},
            {"title": "Task 2", "priority": "medium"},
            {"title": "Task 3", "priority": "low"},
        ]

        # Act
        result = canonical_handlers._format_retrospective_embedded(completed_todos, target_date)

        # Assert
        assert result == "December 21: 3 tasks completed"

    def test_format_embedded_no_tasks(self, canonical_handlers):
        """Test EMBEDDED format with no completed tasks."""
        from datetime import datetime

        # Arrange
        target_date = datetime(2025, 12, 21)
        completed_todos = []

        # Act
        result = canonical_handlers._format_retrospective_embedded(completed_todos, target_date)

        # Assert
        assert result == "December 21: No completed tasks"

    def test_format_standard_with_tasks(self, canonical_handlers):
        """Test STANDARD format with completed tasks."""
        from datetime import datetime

        # Arrange
        target_date = datetime(2025, 12, 21)
        completed_todos = [
            {"title": "Fix authentication bug", "priority": "high"},
            {"title": "Update documentation", "priority": "medium"},
            {"title": "Review PR #42", "priority": "low"},
        ]

        # Act
        result = canonical_handlers._format_retrospective_standard(completed_todos, target_date)

        # Assert
        assert "Yesterday's Accomplishments" in result
        assert "Sunday, December 21, 2025" in result
        assert "Completed Tasks" in result
        assert "3" in result
        assert "Fix authentication bug" in result
        assert "Update documentation" in result
        assert "Review PR #42" in result
        assert "Productive day" in result

    def test_format_standard_no_tasks(self, canonical_handlers):
        """Test STANDARD format with no completed tasks."""
        from datetime import datetime

        # Arrange
        target_date = datetime(2025, 12, 21)
        completed_todos = []

        # Act
        result = canonical_handlers._format_retrospective_standard(completed_todos, target_date)

        # Assert
        assert "Yesterday's Accomplishments" in result
        assert "Sunday, December 21, 2025" in result
        assert "No completed tasks found" in result

    def test_format_standard_with_many_tasks(self, canonical_handlers):
        """Test STANDARD format with more than 8 tasks."""
        from datetime import datetime

        # Arrange
        target_date = datetime(2025, 12, 21)
        completed_todos = [{"title": f"Task {i}", "priority": "medium"} for i in range(12)]

        # Act
        result = canonical_handlers._format_retrospective_standard(completed_todos, target_date)

        # Assert
        assert "Yesterday's Accomplishments" in result
        assert "12" in result
        assert "and 4 more" in result

    def test_format_granular_with_tasks_grouped_by_priority(self, canonical_handlers):
        """Test GRANULAR format groups tasks by priority."""
        from datetime import datetime

        # Arrange
        target_date = datetime(2025, 12, 21)
        completed_todos = [
            {"title": "Critical fix", "priority": "high"},
            {"title": "Important feature", "priority": "high"},
            {"title": "Documentation update", "priority": "medium"},
            {"title": "Code cleanup", "priority": "low"},
        ]

        # Act
        result = canonical_handlers._format_retrospective_granular(completed_todos, target_date)

        # Assert
        assert "# Yesterday's Accomplishments" in result
        assert "Sunday, December 21, 2025" in result
        assert "## 🔴 High Priority Completed" in result
        assert "Critical fix" in result
        assert "Important feature" in result
        assert "## 🟡 Medium Priority Completed" in result
        assert "Documentation update" in result
        assert "## 🟢 Low Priority Completed" in result
        assert "Code cleanup" in result
        assert "## 📊 Summary" in result
        assert "**Total Completed**: 4 tasks" in result
        assert "**High Priority**: 2 tasks" in result
        assert "**Medium Priority**: 1 tasks" in result
        assert "**Low Priority**: 1 tasks" in result

    def test_format_granular_no_tasks(self, canonical_handlers):
        """Test GRANULAR format with no completed tasks."""
        from datetime import datetime

        # Arrange
        target_date = datetime(2025, 12, 21)
        completed_todos = []

        # Act
        result = canonical_handlers._format_retrospective_granular(completed_todos, target_date)

        # Assert
        assert "# Yesterday's Accomplishments" in result
        assert "Sunday, December 21, 2025" in result
        assert "📋 No completed tasks found" in result
        assert "Consider reviewing your task list" in result


class TestStatusReportFormatting:
    """Test suite for status report formatting methods (Issue #513)"""

    def test_format_embedded_with_all_data(self, canonical_handlers):
        """Test EMBEDDED format with projects and todos."""
        # Arrange
        report_data = {
            "total_projects": 3,
            "health_summary": {
                "healthy": 2,
                "at-risk": 1,
                "stalled": 0,
                "unknown": 0,
            },
            "open_todos": 5,
        }

        # Act
        result = canonical_handlers._format_status_report_embedded(report_data)

        # Assert
        assert "2 healthy" in result
        assert "1 at-risk" in result
        assert "5 open todos" in result

    def test_format_embedded_no_data(self, canonical_handlers):
        """Test EMBEDDED format with no projects or todos."""
        # Arrange
        report_data = {
            "total_projects": 0,
            "health_summary": {
                "healthy": 0,
                "at-risk": 0,
                "stalled": 0,
                "unknown": 0,
            },
            "open_todos": 0,
        }

        # Act
        result = canonical_handlers._format_status_report_embedded(report_data)

        # Assert
        assert "No projects or todos" in result

    def test_format_standard_includes_sections(self, canonical_handlers):
        """Test STANDARD format includes all sections."""
        # Arrange
        report_data = {
            "total_projects": 3,
            "health_summary": {
                "healthy": 1,
                "at-risk": 1,
                "stalled": 1,
                "unknown": 0,
            },
            "open_todos": 7,
        }

        # Act
        result = canonical_handlers._format_status_report_standard(report_data)

        # Assert
        assert "Status Report" in result
        assert "Projects" in result
        assert "3 total" in result
        assert "Healthy: 1" in result
        assert "At Risk: 1" in result
        assert "Stalled: 1" in result
        assert "Open Todos**: 7" in result

    def test_format_granular_includes_breakdown(self, canonical_handlers):
        """Test GRANULAR format includes detailed breakdown."""
        # Arrange
        report_data = {
            "total_projects": 4,
            "health_summary": {
                "healthy": 2,
                "at-risk": 1,
                "stalled": 1,
                "unknown": 0,
            },
            "open_todos": 10,
        }

        # Act
        result = canonical_handlers._format_status_report_granular(report_data)

        # Assert
        assert "Detailed Status Report" in result
        assert "Overview" in result
        assert "Total Projects**: 4" in result
        assert "Open Todos**: 10" in result
        assert "Project Health Breakdown" in result
        assert "Healthy**: 2 projects" in result
        assert "At Risk**: 1 projects" in result
        assert "Stalled**: 1 projects" in result
        assert "Summary" in result

    def test_format_granular_all_healthy(self, canonical_handlers):
        """Test GRANULAR format when all projects are healthy."""
        # Arrange
        report_data = {
            "total_projects": 3,
            "health_summary": {
                "healthy": 3,
                "at-risk": 0,
                "stalled": 0,
                "unknown": 0,
            },
            "open_todos": 2,
        }

        # Act
        result = canonical_handlers._format_status_report_granular(report_data)

        # Assert
        assert "All projects are healthy!" in result

    def test_format_granular_with_stalled(self, canonical_handlers):
        """Test GRANULAR format shows attention needed for stalled projects."""
        # Arrange
        report_data = {
            "total_projects": 3,
            "health_summary": {
                "healthy": 1,
                "at-risk": 0,
                "stalled": 2,
                "unknown": 0,
            },
            "open_todos": 5,
        }

        # Act
        result = canonical_handlers._format_status_report_granular(report_data)

        # Assert
        assert "Attention needed" in result
        assert "2 stalled project(s)" in result

    def test_format_standard_only_healthy(self, canonical_handlers):
        """Test STANDARD format with only healthy projects."""
        # Arrange
        report_data = {
            "total_projects": 2,
            "health_summary": {
                "healthy": 2,
                "at-risk": 0,
                "stalled": 0,
                "unknown": 0,
            },
            "open_todos": 3,
        }

        # Act
        result = canonical_handlers._format_status_report_standard(report_data)

        # Assert
        assert "Healthy: 2" in result
        assert "At Risk" not in result or "At Risk: 0" not in result  # Should not show 0 counts


class TestProjectSpecificQuery:
    """Test suite for project-specific query detection and formatting (Issue #500)"""

    def test_detects_status_of_pattern(self, canonical_handlers):
        """Test detection of 'status of ProjectName' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's the status of HealthTrack?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result == "HealthTrack"

    def test_detects_how_is_project_going_pattern(self, canonical_handlers):
        """Test detection of 'how is project going' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How is the MediHub project going?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result == "MediHub"

    def test_detects_how_is_project_doing_pattern(self, canonical_handlers):
        """Test detection of 'how is project doing' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="How is CarePro doing?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result == "CarePro"

    def test_detects_tell_me_about_pattern(self, canonical_handlers):
        """Test detection of 'tell me about' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Tell me about HealthTrack",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result == "HealthTrack"

    def test_detects_update_on_pattern(self, canonical_handlers):
        """Test detection of 'update on' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Give me an update on MediHub?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result == "MediHub"

    def test_detects_project_status_pattern(self, canonical_handlers):
        """Test detection of 'ProjectName status' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="CarePro status?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result == "CarePro"

    def test_detects_what_about_pattern(self, canonical_handlers):
        """Test detection of 'what about' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What about HealthTrack?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result == "HealthTrack"

    def test_case_insensitive_exact_match(self, canonical_handlers):
        """Test case-insensitive exact match for project names."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's the status of healthtrack?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert - Should match HealthTrack despite case difference
        assert result == "HealthTrack"

    def test_fuzzy_match_project_contains_query(self, canonical_handlers):
        """Test fuzzy match when project name contains query term."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's the status of Health?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert - Should match HealthTrack (contains "health")
        assert result == "HealthTrack"

    def test_fuzzy_match_query_contains_project(self, canonical_handlers):
        """Test fuzzy match when query contains project name."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's the status of MediHub platform?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert - Should match MediHub
        assert result == "MediHub"

    def test_returns_none_for_unknown_project(self, canonical_handlers):
        """Test returns None when project name is not recognized."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's the status of UnknownProject?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result is None

    def test_returns_none_for_empty_projects_list(self, canonical_handlers):
        """Test returns None when projects list is empty."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's the status of HealthTrack?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = []

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result is None

    def test_returns_none_for_none_intent(self, canonical_handlers):
        """Test returns None when intent is None."""
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(None, projects)

        # Assert
        assert result is None

    def test_returns_none_for_empty_message(self, canonical_handlers):
        """Test returns None when message is empty."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result is None

    def test_returns_none_for_non_project_specific_query(self, canonical_handlers):
        """Test returns None for general status queries."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What am I working on?",
            category=IntentCategoryEnum.STATUS,
            action="query_status",
            confidence=0.9,
        )
        projects = ["HealthTrack", "MediHub", "CarePro"]

        # Act
        result = canonical_handlers._detect_project_specific_query(intent, projects)

        # Assert
        assert result is None

    def test_format_embedded_with_github_metadata(self, canonical_handlers):
        """Test EMBEDDED format with GitHub metadata."""
        # Arrange
        metadata = {"has_github": True, "open_issues_count": 12}

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, None, spatial_pattern="EMBEDDED"
        )

        # Assert
        assert result == "HealthTrack: 12 open issues"

    def test_format_embedded_without_issues_count(self, canonical_handlers):
        """Test EMBEDDED format without issues count."""
        # Arrange
        metadata = {"has_github": True}

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, None, spatial_pattern="EMBEDDED"
        )

        # Assert
        assert result == "HealthTrack: Active"

    def test_format_embedded_no_github(self, canonical_handlers):
        """Test EMBEDDED format without GitHub connection."""
        # Arrange
        metadata = {"has_github": False}

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, None, spatial_pattern="EMBEDDED"
        )

        # Assert
        assert result == "HealthTrack: Active"

    def test_format_standard_with_github_metadata(self, canonical_handlers):
        """Test STANDARD format with GitHub metadata."""
        # Arrange
        metadata = {
            "has_github": True,
            "open_issues_count": 8,
            "issues_preview": [
                {"number": 101, "title": "Fix authentication bug"},
                {"number": 102, "title": "Add user settings page"},
                {"number": 103, "title": "Update documentation"},
            ],
            "repository": "https://github.com/org/healthtrack",
        }

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, None, spatial_pattern="STANDARD"
        )

        # Assert
        assert "**HealthTrack Status**" in result
        assert "📋 **Open Issues**: 8" in result
        assert "#101: Fix authentication bug" in result
        assert "#102: Add user settings page" in result
        assert "#103: Update documentation" in result
        assert "🔗 **Repository**: https://github.com/org/healthtrack" in result

    def test_format_standard_without_github(self, canonical_handlers):
        """Test STANDARD format without GitHub connection."""
        # Arrange
        metadata = {"has_github": False}

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, None, spatial_pattern="STANDARD"
        )

        # Assert
        assert "**HealthTrack Status**" in result
        assert "📊 **Status**: Active development" in result
        assert "ℹ️ No GitHub repository linked - add one in Settings → Projects" in result

    def test_format_granular_with_full_metadata(self, canonical_handlers):
        """Test GRANULAR format with full metadata and user context."""
        # Arrange
        metadata = {
            "has_github": True,
            "open_issues_count": 15,
            "issues_preview": [
                {"number": 201, "title": "Critical: Database connection fails on startup"},
                {"number": 202, "title": "Feature: Add export functionality"},
                {"number": 203, "title": "Bug: UI glitch in settings page"},
                {"number": 204, "title": "Enhancement: Improve search performance"},
                {"number": 205, "title": "Documentation: Update API reference"},
                {"number": 206, "title": "Refactor: Simplify authentication flow"},
            ],
            "repository": "https://github.com/org/healthtrack",
        }
        user_context = MagicMock()
        user_context.organization = "HealthCare Inc."
        user_context.priorities = ["Q1 Launch", "Security Audit", "Performance Optimization"]

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, user_context, spatial_pattern="GRANULAR"
        )

        # Assert
        assert "**HealthTrack Status**" in result
        assert "📋 **Open Issues**: 15" in result
        # GRANULAR should show 5 issues
        assert "#201:" in result
        assert "#202:" in result
        assert "#203:" in result
        assert "#204:" in result
        assert "#205:" in result
        assert "🔗 **Repository**: https://github.com/org/healthtrack" in result
        assert "🏢 **Organization**: HealthCare Inc." in result
        assert "🎯 **Current Priorities**:" in result
        assert "Q1 Launch" in result
        assert "Security Audit" in result
        assert "Performance Optimization" in result

    def test_format_granular_limits_issue_preview_to_five(self, canonical_handlers):
        """Test GRANULAR format shows maximum 5 issue previews."""
        # Arrange
        metadata = {
            "has_github": True,
            "open_issues_count": 10,
            "issues_preview": [{"number": i, "title": f"Issue {i}"} for i in range(1, 11)],
            "repository": "https://github.com/org/healthtrack",
        }

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, None, spatial_pattern="GRANULAR"
        )

        # Assert - Should only show first 5 issues
        assert "#1:" in result
        assert "#2:" in result
        assert "#3:" in result
        assert "#4:" in result
        assert "#5:" in result
        assert "#6:" not in result

    def test_format_standard_limits_issue_preview_to_three(self, canonical_handlers):
        """Test STANDARD format shows maximum 3 issue previews."""
        # Arrange
        metadata = {
            "has_github": True,
            "open_issues_count": 10,
            "issues_preview": [{"number": i, "title": f"Issue {i}"} for i in range(1, 11)],
            "repository": "https://github.com/org/healthtrack",
        }

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, None, spatial_pattern="STANDARD"
        )

        # Assert - Should only show first 3 issues
        assert "#1:" in result
        assert "#2:" in result
        assert "#3:" in result
        assert "#4:" not in result

    def test_format_truncates_long_issue_titles(self, canonical_handlers):
        """Test that issue titles longer than 60 chars are truncated."""
        # Arrange
        long_title = "This is a very long issue title that should definitely be truncated because it exceeds sixty characters"
        metadata = {
            "has_github": True,
            "open_issues_count": 1,
            "issues_preview": [
                {"number": 999, "title": long_title},
            ],
            "repository": "https://github.com/org/healthtrack",
        }

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, None, spatial_pattern="STANDARD"
        )

        # Assert - Title should be truncated to 60 chars
        assert "#999:" in result
        # The title in result should be truncated
        truncated_title = long_title[:60]
        assert truncated_title in result
        assert long_title not in result

    def test_format_handles_missing_issue_title(self, canonical_handlers):
        """Test format handles missing issue title gracefully."""
        # Arrange
        metadata = {
            "has_github": True,
            "open_issues_count": 1,
            "issues_preview": [
                {"number": 999},  # No title field
            ],
            "repository": "https://github.com/org/healthtrack",
        }

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, None, spatial_pattern="STANDARD"
        )

        # Assert
        assert "#999: Untitled" in result

    def test_format_without_user_context_organization(self, canonical_handlers):
        """Test format without organization in user context."""
        # Arrange
        metadata = {"has_github": True, "open_issues_count": 5}
        user_context = MagicMock()
        user_context.organization = None

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, user_context, spatial_pattern="STANDARD"
        )

        # Assert - Should not include organization section
        assert "🏢 **Organization**:" not in result

    def test_format_without_user_context_priorities(self, canonical_handlers):
        """Test GRANULAR format without priorities in user context."""
        # Arrange
        metadata = {"has_github": True, "open_issues_count": 5}
        user_context = MagicMock()
        user_context.priorities = None

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, user_context, spatial_pattern="GRANULAR"
        )

        # Assert - Should not include priorities section
        assert "🎯 **Current Priorities**:" not in result

    def test_format_standard_does_not_show_priorities(self, canonical_handlers):
        """Test STANDARD format does not show priorities even if available."""
        # Arrange
        metadata = {"has_github": True, "open_issues_count": 5}
        user_context = MagicMock()
        user_context.priorities = ["Priority 1", "Priority 2"]

        # Act
        result = canonical_handlers._format_project_specific_status(
            "HealthTrack", metadata, user_context, spatial_pattern="STANDARD"
        )

        # Assert - STANDARD should not show priorities (only GRANULAR does)
        assert "🎯 **Current Priorities**:" not in result


class TestIntegrationTipLogic847:
    """
    Issue #847: Verify tip logic uses config_service.is_configured(user_id)
    instead of plugin.is_configured() which always returns False.
    """

    def test_tip_not_shown_when_calendar_configured(self, canonical_handlers):
        """Calendar configured → no 'Connect your calendar' tip."""
        # calendar_context with has_calendar=True means config check passed
        calendar_context = {"has_calendar": True}
        project_metadata = {"some_project": {"has_github": True}}
        priority_metadata = {"has_github": True, "high_priority_issues": []}

        user_context = MagicMock()
        user_context.projects = ["MyProject"]
        user_context.priorities = []

        result = canonical_handlers._synthesize_focus_recommendation(
            current_hour=10,
            user_context=user_context,
            calendar_context=calendar_context,
            project_metadata=project_metadata,
            priority_metadata=priority_metadata,
        )

        assert "calendar" not in result["missing_integrations"]
        # Should not suggest connecting calendar
        for suggestion in result["suggestions"]:
            assert "Connect your calendar" not in suggestion

    def test_tip_shown_when_calendar_not_configured(self, canonical_handlers):
        """Calendar not configured → 'Connect your calendar' tip shown."""
        result = canonical_handlers._synthesize_focus_recommendation(
            current_hour=10,
            user_context=MagicMock(projects=[], priorities=[]),
            calendar_context=None,
            project_metadata={},
            priority_metadata={},
        )

        assert "calendar" in result["missing_integrations"]

    def test_tip_not_shown_when_github_configured(self, canonical_handlers):
        """GitHub configured → no 'Connect GitHub' tip."""
        priority_metadata = {"has_github": True, "high_priority_issues": []}
        project_metadata = {"proj": {"has_github": True}}

        result = canonical_handlers._synthesize_focus_recommendation(
            current_hour=10,
            user_context=MagicMock(projects=["proj"], priorities=[]),
            calendar_context=None,
            project_metadata=project_metadata,
            priority_metadata=priority_metadata,
        )

        assert "github" not in result["missing_integrations"]

    def test_tip_shown_when_github_not_configured(self, canonical_handlers):
        """GitHub not configured → 'Connect GitHub' tip shown."""
        result = canonical_handlers._synthesize_focus_recommendation(
            current_hour=10,
            user_context=MagicMock(projects=[], priorities=[]),
            calendar_context=None,
            project_metadata={},
            priority_metadata={},
        )

        assert "github" in result["missing_integrations"]

    def test_context_level_rich_when_all_configured(self, canonical_handlers):
        """All integrations configured → context_level is 'rich'."""
        result = canonical_handlers._synthesize_focus_recommendation(
            current_hour=10,
            user_context=MagicMock(projects=["proj"], priorities=["p1"]),
            calendar_context={"has_calendar": True},
            project_metadata={"proj": {}},
            priority_metadata={"has_github": True},
        )

        assert result["context_level"] == "rich"

    @pytest.mark.asyncio
    async def test_get_calendar_context_uses_config_service(self, canonical_handlers):
        """_get_calendar_context checks config_service, not plugin.is_configured()."""
        with patch(
            "services.integrations.calendar.config_service.CalendarConfigService"
        ) as MockConfigService:
            mock_config = MagicMock()
            mock_config.is_configured.return_value = False
            MockConfigService.return_value = mock_config

            result = await canonical_handlers._get_calendar_context(user_id="test-user")

            # Should have checked config service with user_id
            mock_config.is_configured.assert_called_once_with("test-user")
            # Config says not configured → should return None
            assert result is None

    @pytest.mark.asyncio
    async def test_get_priority_metadata_uses_config_service(self, canonical_handlers):
        """_get_priority_metadata checks config_service, not plugin.is_configured()."""
        with patch(
            "services.integrations.github.config_service.GitHubConfigService"
        ) as MockConfigService:
            mock_config = MagicMock()
            mock_config.is_configured.return_value = False
            MockConfigService.return_value = mock_config

            result = await canonical_handlers._get_priority_metadata(user_id="test-user")

            # Should have checked config service with user_id
            mock_config.is_configured.assert_called_once_with("test-user")
            # Config says not configured → #1231 honest-degrade marker (was silent {})
            assert result == {"github_unavailable": "not_configured"}

    @pytest.mark.asyncio
    async def test_get_calendar_context_returns_none_without_user_id(self, canonical_handlers):
        """_get_calendar_context returns None when no user_id provided."""
        result = await canonical_handlers._get_calendar_context(user_id=None)
        assert result is None

    @pytest.mark.asyncio
    async def test_get_priority_metadata_returns_empty_without_user_id(self, canonical_handlers):
        """_get_priority_metadata returns empty dict when no user_id provided."""
        result = await canonical_handlers._get_priority_metadata(user_id=None)
        assert result == {}


class TestGuidanceQuerySynthesisSeam497:
    """Issue #497: guard the
    _handle_guidance_query -> _synthesize_focus_recommendation -> response seam.

    The synthesis helper has branch-level coverage (TestIntegrationTipLogic847),
    but nothing previously verified that the *full handler* threads the synthesized
    recommendation (and its derived context_level) all the way into the response
    payload. A regression in the handler's wiring would compute the synthesis and
    silently discard it (Pattern-073 doc-vs-actual drift). These tests lock the seam.
    """

    @pytest.mark.asyncio
    async def test_handler_threads_rich_synthesis_into_response(self, canonical_handlers):
        """Calendar + projects + priorities all present -> 'rich' context_level, and
        the focus_recommendation (incl. urgent counts + primary_focus) rides through
        to the response context."""
        intent = MagicMock()
        intent.spatial_context = None  # -> standard formatter path

        user_ctx = MagicMock()
        user_ctx.projects = ["proj"]
        user_ctx.priorities = ["Ship alpha testing"]
        user_ctx.organization = "Piper Morgan"

        with (
            patch.object(canonical_handlers, "_detect_setup_request", return_value=None),
            patch(
                "services.intent_service.canonical_handlers.user_context_service.get_user_context",
                new=AsyncMock(return_value=user_ctx),
            ),
            patch.object(
                canonical_handlers,
                "_get_calendar_context",
                new=AsyncMock(return_value={"has_calendar": True, "next_meeting": None}),
            ),
            patch.object(
                canonical_handlers,
                "_get_project_metadata",
                new=AsyncMock(return_value={"proj": {"has_github": True}}),
            ),
            patch.object(
                canonical_handlers,
                "_get_priority_metadata",
                new=AsyncMock(
                    return_value={
                        "has_github": True,
                        "high_priority_issues": [{"number": 1}],
                        "total_open_issues": 5,
                    }
                ),
            ),
        ):
            result = await canonical_handlers._handle_guidance_query(
                intent, session_id="s-test", user_id="u-test"
            )

        # Seam 1: top-level signals reflect the synthesis
        assert result["context_level"] == "rich"
        assert result["calendar_aware"] is True
        assert result["personalized"] is True

        # Seam 2: the full synthesis dict rides through in the response context
        fr = result["intent"]["context"]["focus_recommendation"]
        assert fr["context_level"] == "rich"
        assert fr["urgent_items"] == 1
        assert fr["open_issues"] == 5
        # urgent path -> primary_focus is urgent-issues, surfaced in suggestions
        assert fr["primary_focus"] == "urgent-issues"
        assert any("urgent" in s.lower() for s in fr["suggestions"])

    @pytest.mark.asyncio
    async def test_handler_minimal_and_suggests_setup_when_no_integrations(
        self, canonical_handlers
    ):
        """No calendar / projects / priorities -> 'minimal' context_level with both
        setup tips, and the handler still returns a well-formed payload (graceful
        degradation, not an exception)."""
        intent = MagicMock()
        intent.spatial_context = None

        user_ctx = MagicMock()
        user_ctx.projects = []
        user_ctx.priorities = []
        user_ctx.organization = None

        with (
            patch.object(canonical_handlers, "_detect_setup_request", return_value=None),
            patch(
                "services.intent_service.canonical_handlers.user_context_service.get_user_context",
                new=AsyncMock(return_value=user_ctx),
            ),
            patch.object(
                canonical_handlers,
                "_get_calendar_context",
                new=AsyncMock(return_value=None),
            ),
            patch.object(
                canonical_handlers,
                "_get_priority_metadata",
                new=AsyncMock(return_value={}),
            ),
        ):
            result = await canonical_handlers._handle_guidance_query(
                intent, session_id="s-test", user_id="u-test"
            )

        assert result["context_level"] == "minimal"
        fr = result["intent"]["context"]["focus_recommendation"]
        assert "calendar" in fr["missing_integrations"]
        assert "github" in fr["missing_integrations"]
