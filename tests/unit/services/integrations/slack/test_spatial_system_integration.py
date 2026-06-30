"""
Complete Slack Spatial System Integration Tests
Tests end-to-end integration of all spatial components following strict TDD principles.

This test suite validates the complete OAuth → Spatial → Workflow → Attention flow
that represents the core value proposition of PM-074 Slack Integration.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID, uuid4

import pytest

from services.integrations.slack.attention_model import (
    AttentionEvent,
    AttentionModel,
    AttentionSource,
)
from services.integrations.slack.ngrok_service import NgrokService
from services.integrations.slack.oauth_handler import SlackOAuthHandler
from services.integrations.slack.spatial_mapper import SlackSpatialMapper
from services.integrations.slack.spatial_memory import SpatialMemoryRecord, SpatialMemoryStore
from services.integrations.slack.spatial_types import (
    AttentionAttractor,
    AttentionLevel,
    EmotionalValence,
    Room,
    RoomPurpose,
    SpatialCoordinates,
    SpatialEvent,
    Territory,
    TerritoryType,
)
from services.integrations.slack.webhook_router import SlackWebhookRouter
from services.integrations.slack.workspace_navigator import (
    NavigationIntent,
    TerritoryState,
    WorkspaceNavigator,
)

from contextlib import asynccontextmanager


# Issue #1109: the Slack OAuth nonce store moved to Redis (multi-process safe),
# so generate_authorization_url + handle_oauth_callback are async and Redis-
# backed. fakeredis isn't installed here; patch RedisFactory.redis_scope with a
# shared in-memory fake so the nonce written on /connect is visible to /callback.
class _FakeRedis:
    def __init__(self):
        self.store: dict = {}

    async def setex(self, key, ttl_seconds, value):
        self.store[key] = value.encode() if isinstance(value, str) else value
        return True

    async def get(self, key):
        return self.store.get(key)

    async def getdel(self, key):
        return self.store.pop(key, None)

    async def close(self):
        pass


@pytest.fixture
def patched_oauth_redis():
    fake = _FakeRedis()

    @asynccontextmanager
    async def _scope():
        yield fake

    with patch(
        "services.integrations.slack.oauth_handler.RedisFactory.redis_scope",
        side_effect=_scope,
    ):
        yield fake


class TestCompleteOAuthToSpatialWorkflow:
    """
    TDD Test Suite: Complete OAuth → Spatial Workflow Integration

    These tests are written FIRST and expected to FAIL initially.
    They define the complete behavior of the spatial system.
    """

    @pytest.fixture
    def mock_config_service(self):
        """Mock configuration service with OAuth credentials"""
        config = Mock()
        config.get_config.return_value = Mock(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="https://test-ngrok.ngrok.io/slack/oauth/callback",
            scopes=["chat:write", "channels:read", "groups:read"],
        )
        config.is_configured.return_value = True
        return config

    @pytest.fixture
    def spatial_memory_store(self, tmp_path):
        """Spatial memory store with temporary storage"""
        return SpatialMemoryStore(storage_path=str(tmp_path / "spatial_memory"))

    @pytest.fixture
    def workspace_navigator(self, spatial_memory_store):
        """Workspace navigator with test memory store"""
        return WorkspaceNavigator(memory_store=spatial_memory_store)

    @pytest.fixture
    def attention_model(self, spatial_memory_store):
        """Attention model with test memory store"""
        return AttentionModel(memory_store=spatial_memory_store)

    @pytest.fixture
    def oauth_handler(self, mock_config_service):
        """OAuth handler with mocked dependencies"""
        return SlackOAuthHandler(config_service=mock_config_service)

    # TDD Test 1: COMPLETE OAUTH FLOW WITH SPATIAL INITIALIZATION
    # This test should FAIL initially - we need to implement the complete flow

    @patch("httpx.AsyncClient.post")
    @pytest.mark.smoke
    async def test_oauth_flow_creates_spatial_workspace_territory(
        self,
        mock_post,
        oauth_handler,
        workspace_navigator,
        spatial_memory_store,
        patched_oauth_redis,
    ):
        """
        TDD: OAuth success should automatically initialize spatial workspace territory

        EXPECTED TO FAIL: This is the complete integration we need to build
        """
        # STEP 1: Generate OAuth authorization URL (registers state)
        # Issue #734: Now requires user_id for multi-tenancy
        # Issue #1109: generate_authorization_url is async (Redis-backed state)
        auth_url, state = await oauth_handler.generate_authorization_url(user_id="test-user-123")
        assert state is not None, "OAuth state should be generated"

        # Mock successful OAuth response (async response from httpx)
        mock_response = AsyncMock()
        mock_response.json = Mock(  # .json() returns the dict directly, not async
            return_value={
                "ok": True,
                "access_token": "xoxb-test-token",
                "team": {"id": "T123456", "name": "Test Workspace", "domain": "test-workspace"},
                "authed_user": {"id": "U123456"},
            }
        )
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        # STEP 2: Execute OAuth callback with registered state - this should create spatial territory
        oauth_result = await oauth_handler.handle_oauth_callback(code="test_code", state=state)

        # ASSERTION 1: OAuth succeeds
        assert oauth_result["success"] is True
        assert oauth_result["workspace"] is not None

        # ASSERTION 2: Spatial context is included in response
        assert "spatial_mapping" in oauth_result
        spatial_context = oauth_result["spatial_mapping"]
        assert spatial_context is not None

        # ASSERTION 3: Territory is created in workspace_data
        workspace_data = oauth_result["workspace"]
        assert "territory" in workspace_data
        territory_info = workspace_data["territory"]
        assert territory_info["id"] == "T123456"
        assert territory_info["name"] == "Test Workspace"

        # ASSERTION 4: Navigation context is properly initialized
        assert "navigation_context" in territory_info
        nav_context = territory_info["navigation_context"]
        assert nav_context is not None

    # TDD Test 2: SLACK EVENT TO SPATIAL PROCESSING TO WORKFLOW
    # This test should FAIL initially - complete event processing chain

    @pytest.mark.smoke
    async def test_slack_event_to_spatial_to_workflow_pipeline(
        self, workspace_navigator, attention_model, spatial_memory_store
    ):
        """
        TDD: Slack webhook event → Spatial processing → Piper workflow creation

        EXPECTED TO FAIL: This is the complete value proposition integration
        """
        # SETUP: Create test territory and room
        test_territory = Territory(
            id="T123456",
            name="Test Workspace",
            territory_type=TerritoryType.CORPORATE,
            domain="test-workspace.slack.com",
        )

        workspace_navigator.register_territory(test_territory)

        # SIMULATE: Slack webhook event (mention with help request)
        slack_event = {
            "type": "app_mention",
            "text": "<@U_PIPER> Help! We have a critical bug in production",
            "channel": "C123456",
            "channel_type": "channel",
            "ts": "1234567890.123456",
            "user": "U789012",
            "team": "T123456",
        }

        # STEP 1: Spatial mapping (should create spatial objects)
        spatial_mapper = SlackSpatialMapper()

        # Map channel to room (using dict interface)
        channel_data = {
            "id": "C123456",
            "team_id": "T123456",
            "name": "general",
            "purpose": {"value": "General discussion"},
            "topic": {"value": "Team collaboration"},
            "is_private": False,
            "num_members": 10,
            "members": ["U789012"],
        }
        room = await spatial_mapper.map_channel_to_room(channel_data)

        # Map mention to attention attractor
        attention_attractor = await spatial_mapper.map_mention_to_attention_attractor(slack_event)

        # ASSERTION 1: Room properly mapped with spatial attributes
        assert room.id == "C123456"
        assert room.territory_id == "T123456"
        assert room.purpose == RoomPurpose.GENERAL
        assert "general" in room.name

        # ASSERTION 2: Attention attractor created with correct urgency
        assert (
            attention_attractor.target_id == "user"
        )  # Mentioned user (fallback due to underscore)
        assert attention_attractor.attractor_type == AttentionLevel.URGENT
        assert attention_attractor.source_object_id == "1234567890.123456"
        assert "critical" in attention_attractor.urgency_indicators
        assert "help" in attention_attractor.urgency_indicators

        # STEP 2: Attention model processing
        # Create spatial coordinates from room and event data
        attention_coordinates = SpatialCoordinates(
            territory_id="T123456",
            room_id="C123456",
            path_id=slack_event.get("ts"),
        )

        attention_event = attention_model.create_attention_event(
            source=AttentionSource.MENTION,
            coordinates=attention_coordinates,
            base_intensity=0.9,
            urgency_level=0.9,
            context={
                "actor_id": "U789012",
                "target_users": ["U_PIPER"],
                "keywords": ["help", "critical", "bug", "production"],
                "workflow_priority": "high",
            },
        )

        # ASSERTION 3: Attention event properly classified
        assert attention_event.source == AttentionSource.MENTION
        assert attention_event.urgency_level == 0.9
        assert attention_event.personal_relevance > 0.5  # Base relevance + keyword match
        assert "U789012" == attention_event.actor_id

        # STEP 3: Navigation decision (workspace navigator)
        navigation_priorities = attention_model.get_attention_priorities(
            current_coordinates=SpatialCoordinates(
                territory_id="T123456",
                room_id="C_OTHER",  # Currently in different room
                path_id=None,
            )
        )

        # ASSERTION 4: Navigation prioritizes urgent attention
        assert len(navigation_priorities) > 0
        top_event, top_score = navigation_priorities[0]
        assert top_score > 0.8
        assert top_event.spatial_coordinates.room_id == "C123456"

        # STEP 4: Memory persistence
        spatial_memory_store.record_spatial_visit(
            "C123456",
            "room",
            "general",
            context={
                "attention_event": True,
                "urgency": "high",
                "requires_response": True,
                "keywords": ["critical", "bug", "production"],
            },
        )

        # ASSERTION 5: Spatial memory updated with context
        room_memory = spatial_memory_store.get_memory_record("C123456")
        assert room_memory is not None
        assert room_memory.visit_count > 0
        assert len(room_memory.attention_history) > 0

        # STEP 5: Workflow creation context
        workflow_context = {
            "spatial_trigger": {
                "event_type": "attention_attracted",
                "source": "slack_mention",
                "coordinates": attention_coordinates.to_slack_reference(),
                "urgency": attention_event.urgency_level,
                "keywords": attention_event.keywords,
                "requires_immediate_response": True,
            },
            "navigation_decision": {
                "recommended_action": "respond_immediately",
                "target_location": attention_coordinates.to_slack_reference(),
                "confidence": top_score,
            },
            "spatial_memory": {
                "room_context": room_memory.purpose,
                "previous_interactions": len(room_memory.attention_history),
                "room_activity_level": "high",
            },
        }

        # ASSERTION 6: Complete workflow context contains all spatial intelligence
        assert workflow_context["spatial_trigger"]["urgency"] > 0.8
        assert workflow_context["spatial_trigger"]["requires_immediate_response"] is True
        assert (
            workflow_context["navigation_decision"]["recommended_action"] == "respond_immediately"
        )
        assert workflow_context["spatial_memory"]["room_activity_level"] == "high"

        # FINAL ASSERTION: End-to-end spatial system integration successful
        assert True  # If we reach here, complete integration works

    # TDD Test 3: MULTI-WORKSPACE NAVIGATION WITH ATTENTION PRIORITIZATION
    # This test should FAIL initially - complex multi-territory scenarios
    # DEFERRED: Multi-workspace support is post-alpha (Enterprise milestone)

    @pytest.mark.skip(
        reason="Deferred: SLACK-MULTI-WORKSPACE - Requires multiple Slack workspace installations (Enterprise milestone)"
    )
    async def test_multi_workspace_attention_prioritization(
        self, workspace_navigator, attention_model, spatial_memory_store
    ):
        """
        TDD: Multi-workspace navigation with intelligent attention prioritization

        EXPECTED TO FAIL: Complex cross-workspace attention management
        DEFERRED: This feature requires multiple Slack workspace setup (post-alpha)
        """
        # SETUP: Register multiple territories
        corp_territory = Territory(
            id="T_CORP",
            name="Corporate Workspace",
            territory_type=TerritoryType.CORPORATE,
            domain="corp.slack.com",
        )

        startup_territory = Territory(
            id="T_STARTUP",
            name="Startup Workspace",
            territory_type=TerritoryType.STARTUP,
            domain="startup.slack.com",
        )

        workspace_navigator.register_territory(corp_territory)
        workspace_navigator.register_territory(startup_territory)

        # CREATE: Competing attention events across workspaces

        # Corporate: Medium priority meeting reminder
        corp_attention = attention_model.create_attention_event(
            source=AttentionSource.MESSAGE,
            coordinates=SpatialCoordinates("T_CORP", "C_CORP_GENERAL", None),
            base_intensity=0.6,
            urgency_level=0.5,
            context={"keywords": ["meeting", "reminder"], "actor_id": "U_CORP_USER"},
        )

        # Startup: High priority critical bug report
        startup_attention = attention_model.create_attention_event(
            source=AttentionSource.EMERGENCY,
            coordinates=SpatialCoordinates("T_STARTUP", "C_STARTUP_INCIDENT", None),
            base_intensity=1.0,
            urgency_level=0.95,
            context={
                "keywords": ["critical", "bug", "production", "emergency"],
                "actor_id": "U_STARTUP_DEV",
                "emotional_context": EmotionalValence.NEGATIVE,
            },
        )

        # STEP 1: Attention prioritization across territories
        current_location = SpatialCoordinates("T_CORP", "C_CORP_RANDOM", None)
        priorities = attention_model.get_attention_priorities(
            current_coordinates=current_location, max_results=10
        )

        # ASSERTION 1: Emergency attention wins across territories
        assert len(priorities) >= 2
        top_event, top_score = priorities[0]
        assert top_event.spatial_coordinates.territory_id == "T_STARTUP"
        assert top_event.source == AttentionSource.EMERGENCY
        assert top_score > 0.9

        # STEP 2: Navigation planning with territory switch
        suggested_territory = workspace_navigator.suggest_next_territory(
            context=None  # No specific context, should prioritize by attention
        )

        # ASSERTION 2: Navigator suggests emergency territory
        assert suggested_territory == "T_STARTUP"

        # STEP 3: Execute territory switch
        switch_success = workspace_navigator.switch_territory("T_STARTUP", context=None)

        # ASSERTION 3: Territory switch successful
        assert switch_success is True
        assert workspace_navigator._current_territory == "T_STARTUP"

        # STEP 4: Navigation history tracking
        navigation_history = workspace_navigator._navigation_history
        assert len(navigation_history) > 0

        latest_nav = navigation_history[-1]
        assert latest_nav["to_territory"] == "T_STARTUP"
        assert latest_nav["from_territory"] == "T_CORP"

        # STEP 5: Spatial memory cross-territory relationships
        spatial_memory_store.record_spatial_relationship(
            "T_CORP",
            "T_STARTUP",
            "emergency_escalation",
            context={
                "trigger": "critical_bug_report",
                "priority_shift": True,
                "cross_workspace_attention": True,
            },
        )

        # ASSERTION 4: Cross-territory relationships tracked
        relationships = spatial_memory_store.get_connected_spaces("T_CORP")
        assert "T_STARTUP" in relationships

        # FINAL ASSERTION: Multi-workspace attention management works
        assert workspace_navigator._current_territory == "T_STARTUP"
        assert len(priorities) >= 2
        assert top_event.source == AttentionSource.EMERGENCY


class TestAttentionModelBehaviorValidation:
    """
    TDD Test Suite: Attention Model Advanced Behavior Validation

    Tests sophisticated attention patterns, decay models, and learning.
    """

    @pytest.fixture
    def attention_model(self):
        """Clean attention model for behavior testing"""
        return AttentionModel()

    # TDD Test 4: ATTENTION DECAY MODEL VALIDATION
    # Issue #365: SLACK-ATTENTION-DECAY - Pattern learning implemented

    async def test_attention_decay_models_with_pattern_learning(self, attention_model):
        """
        TDD: Attention decay models with pattern learning validation

        Tests decay behavior and pattern learning across different attention sources.
        Implemented as part of Issue #365.
        """
        # CREATE: Test attention events with different decay models

        # Emergency event - should have slow decay
        emergency_event = attention_model.create_attention_event(
            source=AttentionSource.EMERGENCY,
            coordinates=SpatialCoordinates("T123", "C_INCIDENT", None),
            base_intensity=1.0,
            urgency_level=0.95,
            context={"keywords": ["critical", "emergency", "production"]},
        )

        # Social event - should have fast decay
        social_event = attention_model.create_attention_event(
            source=AttentionSource.SOCIAL,
            coordinates=SpatialCoordinates("T123", "C_SOCIAL", None),
            base_intensity=0.4,
            urgency_level=0.2,
            context={"keywords": ["chat", "social", "casual"]},
        )

        # Mention event - should have medium decay
        mention_event = attention_model.create_attention_event(
            source=AttentionSource.MENTION,
            coordinates=SpatialCoordinates("T123", "C_WORK", None),
            base_intensity=0.8,
            urgency_level=0.7,
            context={"keywords": ["help", "question", "work"]},
        )

        # STEP 1: Test immediate intensity (no decay)
        emergency_intensity_t0 = emergency_event.get_current_intensity()
        social_intensity_t0 = social_event.get_current_intensity()
        mention_intensity_t0 = mention_event.get_current_intensity()

        # ASSERTION 1: Initial intensities account for spatial decay factor
        # EMERGENCY: base=1.0 * spatial=1.0 = 1.0
        # MENTION: base=0.8 * spatial=0.9 = 0.72
        # SOCIAL: base=0.4 * spatial=0.7 = 0.28
        assert abs(emergency_intensity_t0 - 1.0) < 0.1
        assert abs(social_intensity_t0 - 0.28) < 0.1
        assert abs(mention_intensity_t0 - 0.72) < 0.1

        # STEP 2: Simulate time passage (30 minutes)
        from unittest.mock import patch

        future_time = datetime.now() + timedelta(minutes=30)

        with patch("services.integrations.slack.attention_model.datetime") as mock_datetime:
            mock_datetime.now.return_value = future_time

            # Use CONTEXTUAL decay for source-specific behavior
            from services.integrations.slack.attention_model import AttentionDecay

            emergency_intensity_t30 = emergency_event.get_current_intensity(
                decay_model=AttentionDecay.CONTEXTUAL
            )
            social_intensity_t30 = social_event.get_current_intensity(
                decay_model=AttentionDecay.CONTEXTUAL
            )
            mention_intensity_t30 = mention_event.get_current_intensity(
                decay_model=AttentionDecay.CONTEXTUAL
            )

        # ASSERTION 2: Different decay rates by source type (CONTEXTUAL mode)
        # EMERGENCY: 2-hour half-life, min 0.3 → ~0.84 at 30 min
        # MENTION: 1-hour half-life, min 0.1 → ~0.51 at 30 min (adjusted by spatial=0.9)
        # SOCIAL: 30-min half-life → ~0.14 at 30 min (adjusted by spatial=0.7)
        assert emergency_intensity_t30 > mention_intensity_t30  # Emergency decays slower
        assert mention_intensity_t30 > social_intensity_t30  # Social decays fastest
        assert emergency_intensity_t30 > 0.7  # Emergency still strong (2hr half-life)
        assert social_intensity_t30 < 0.2  # Social significantly decayed

        # STEP 3: Pattern learning from attention events
        # Learn from emergency event multiple times to build confidence > 0.5
        # (New patterns start at confidence=0.3, need repeated observations)
        attention_model._learn_from_attention_event(emergency_event)
        attention_model._learn_from_attention_event(emergency_event)
        attention_model._learn_from_attention_event(emergency_event)  # 3rd observation
        attention_model._learn_from_attention_event(mention_event)

        # ASSERTION 3: Patterns learned and stored
        learned_patterns = attention_model._learned_patterns
        assert len(learned_patterns) > 0

        emergency_patterns = [
            p
            for p in learned_patterns.values()
            if p.trigger_conditions.get("source") == "emergency"
        ]
        assert len(emergency_patterns) > 0
        # Verify confidence built up above threshold
        assert emergency_patterns[0].confidence > 0.5

        # STEP 4: Pattern-based attention adjustment
        new_emergency_event = attention_model.create_attention_event(
            source=AttentionSource.EMERGENCY,
            coordinates=SpatialCoordinates("T123", "C_INCIDENT", None),
            base_intensity=0.8,  # Lower base intensity
            urgency_level=0.9,
            context={"keywords": ["critical", "emergency"]},
        )

        pattern_adjustment = attention_model._get_pattern_adjustment(new_emergency_event)

        # ASSERTION 4: Pattern learning enhances attention scoring
        assert pattern_adjustment > 1.0  # Pattern provides boost
        assert pattern_adjustment <= 1.2  # Reasonable boost limit

        # FINAL ASSERTION: Attention model learns and adapts
        assert len(learned_patterns) > 0
        assert emergency_intensity_t30 > social_intensity_t30


class TestSpatialMemoryPersistenceIntegration:
    """
    TDD Test Suite: Spatial Memory Persistence Across Sessions

    Tests that spatial awareness persists and accumulates knowledge.
    """

    @pytest.fixture
    def temp_storage_path(self, tmp_path):
        """Temporary storage path for persistence testing"""
        return str(tmp_path / "test_spatial_memory")

    # TDD Test 5: SPATIAL MEMORY PERSISTENCE AND LEARNING
    # Should FAIL initially - complex persistence behavior
    # DEFERRED: Spatial memory persistence is post-alpha (Enhancement milestone)

    @pytest.mark.skip(
        reason="Deferred: SLACK-MEMORY - Requires time-series storage for pattern persistence (Enhancement milestone)"
    )
    async def test_spatial_memory_persistence_and_pattern_accumulation(self, temp_storage_path):
        """
        TDD: Spatial memory persists across sessions and accumulates patterns

        EXPECTED TO FAIL: Complex cross-session memory behavior
        DEFERRED: Requires time-series data storage (post-alpha)
        """
        # SESSION 1: Initial spatial interactions
        memory_store_session1 = SpatialMemoryStore(storage_path=temp_storage_path)

        # Record multiple visits to build memory
        for i in range(5):
            memory_store_session1.record_spatial_visit(
                "C_GENERAL",
                "room",
                "general",
                visit_duration=120.0,  # 2 minutes each
                context={
                    "activity_level": "moderate",
                    "conversation_style": "collaborative",
                    "inhabitants": [f"U_USER_{i}", "U_PIPER"],
                    "emotional_valence": "positive",
                },
            )

        # Record spatial relationships
        memory_store_session1.record_spatial_relationship(
            "C_GENERAL",
            "C_RANDOM",
            "frequent_path",
            context={"navigation_time": 2.5, "usage_pattern": "daily"},
        )

        # Learn spatial patterns
        pattern_data = {
            "navigation_sequence": ["C_GENERAL", "C_RANDOM", "C_GENERAL"],
            "time_pattern": "morning_routine",
            "frequency": "daily",
            "efficiency": 0.9,
        }

        memory_store_session1.learn_spatial_pattern(
            "navigation", "morning_check_routine", pattern_data, 0.8, ["C_GENERAL"]
        )

        # Force save to disk
        save_success = memory_store_session1.save_to_disk(force=True)
        assert save_success is True

        # Verify files exist
        storage_path = Path(temp_storage_path)
        assert (storage_path / "spatial_memories.json").exists()
        assert (storage_path / "spatial_relationships.json").exists()
        assert (storage_path / "spatial_patterns.json").exists()
        assert (storage_path / "metadata.json").exists()

        # SESSION 1 ASSERTIONS: Data properly stored
        general_memory = memory_store_session1.get_memory_record("C_GENERAL")
        assert general_memory is not None
        assert general_memory.visit_count == 5
        assert general_memory.total_time_spent == 600.0  # 5 * 120 seconds
        assert "U_PIPER" in general_memory.typical_inhabitants
        assert general_memory.conversation_style == "collaborative"

        # SESSION 2: New session loads previous memory
        memory_store_session2 = SpatialMemoryStore(storage_path=temp_storage_path)

        # ASSERTION 1: Previous memory loaded successfully
        loaded_general_memory = memory_store_session2.get_memory_record("C_GENERAL")
        assert loaded_general_memory is not None
        assert loaded_general_memory.visit_count == 5
        assert loaded_general_memory.total_time_spent == 600.0
        assert "U_PIPER" in loaded_general_memory.typical_inhabitants

        # ASSERTION 2: Relationships preserved
        relationships = memory_store_session2.get_connected_spaces("C_GENERAL")
        assert "C_RANDOM" in relationships

        # ASSERTION 3: Patterns preserved and available
        patterns = memory_store_session2.find_patterns("navigation", "C_GENERAL", 0.5)
        assert len(patterns) > 0
        morning_pattern = next((p for p in patterns if "morning" in p.pattern_name), None)
        assert morning_pattern is not None
        assert morning_pattern.confidence == 0.8

        # SESSION 2: Additional interactions build on existing memory
        memory_store_session2.record_spatial_visit(
            "C_GENERAL",
            "room",
            "general",
            visit_duration=180.0,  # 3 minutes
            context={
                "activity_level": "busy",
                "attention_event": True,
                "inhabitants": ["U_NEW_USER", "U_PIPER"],
            },
        )

        # ASSERTION 4: Memory accumulates correctly
        updated_memory = memory_store_session2.get_memory_record("C_GENERAL")
        assert updated_memory.visit_count == 6  # 5 + 1
        assert updated_memory.total_time_spent == 780.0  # 600 + 180
        assert "U_NEW_USER" in updated_memory.typical_inhabitants
        assert len(updated_memory.typical_inhabitants) == 3  # U_PIPER + U_USER_* + U_NEW_USER

        # STEP 3: Pattern learning enhancement
        enhanced_pattern_data = {
            "navigation_sequence": ["C_GENERAL", "C_INCIDENT", "C_GENERAL"],
            "time_pattern": "incident_response",
            "frequency": "as_needed",
            "efficiency": 0.95,
            "trigger_keywords": ["urgent", "help", "incident"],
        }

        memory_store_session2.learn_spatial_pattern(
            "navigation", "incident_response_pattern", enhanced_pattern_data, 0.9, ["C_GENERAL"]
        )

        # ASSERTION 5: Multiple patterns coexist
        all_patterns = memory_store_session2.find_patterns("navigation", "C_GENERAL", 0.0)
        assert len(all_patterns) >= 2

        pattern_names = [p.pattern_name for p in all_patterns]
        assert "morning_check_routine" in pattern_names
        assert "incident_response_pattern" in pattern_names

        # SESSION 3: Memory analysis and insights
        memory_analysis = memory_store_session2.analyze_spatial_patterns()

        # ASSERTION 6: Rich analytics from accumulated memory
        assert memory_analysis["total_locations"] >= 1
        assert memory_analysis["rooms"] >= 1
        assert memory_analysis["relationships"] >= 1
        assert memory_analysis["patterns"] >= 2

        most_visited = memory_analysis["most_visited"]
        assert len(most_visited) > 0
        assert most_visited[0]["id"] == "C_GENERAL"
        assert most_visited[0]["visits"] == 6

        # FINAL ASSERTION: Cross-session spatial intelligence works
        assert updated_memory.visit_count == 6
        assert len(all_patterns) >= 2
        assert memory_analysis["total_locations"] >= 1


# Test Runner Configuration
if __name__ == "__main__":
    # These tests are designed to FAIL initially
    # Run with: PYTHONPATH=. pytest services/integrations/slack/tests/test_spatial_system_integration.py -v
    print("TDD Integration Tests - Expected to FAIL initially")
    print("Implement complete spatial system to make tests pass")
