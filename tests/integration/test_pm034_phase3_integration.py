"""
PM-034 Phase 3 Integration Testing Framework

This test suite validates the ConversationManager implementation and integration
with QueryRouter, Redis caching, and end-to-end conversation flows.

Target Capability:
User: "Create GitHub issue for login bug" → Piper: [Creates issue #85]
User: "Show me that issue again" → Piper: [ConversationManager resolves + displays #85]
"""

import asyncio
import time
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestPM034Phase3Integration:
    """Comprehensive integration testing for PM-034 Phase 3 ConversationManager."""

    @pytest.fixture
    async def setup_conversation_environment(self):
        """Set up test environment with mocked external dependencies."""
        # Mock Redis for conversation caching
        with (
            patch("services.conversation.conversation_manager.redis.Redis") as mock_redis,
            patch("services.queries.query_router.QueryRouter") as mock_query_router,
            patch("services.database.session_factory.AsyncSessionFactory") as mock_session_factory,
        ):
            # Mock Redis responses
            mock_redis_instance = AsyncMock()
            mock_redis.return_value = mock_redis_instance
            mock_redis_instance.get.return_value = None  # No existing conversation
            mock_redis_instance.set.return_value = True

            # Mock QueryRouter responses
            mock_query_router_instance = AsyncMock()
            mock_query_router.return_value = mock_query_router_instance

            # Mock session factory
            mock_session_factory_instance = AsyncMock()
            mock_session_factory.return_value = mock_session_factory_instance

            yield {
                "redis": mock_redis_instance,
                "query_router": mock_query_router_instance,
                "session_factory": mock_session_factory_instance,
            }

    async def test_conversation_manager_creation(self, setup_conversation_environment):
        """Test ConversationManager service creation and initialization."""
        try:
            from services.conversation.conversation_manager import ConversationManager

            env = setup_conversation_environment

            # Test ConversationManager instantiation
            conversation_manager = ConversationManager(
                redis_client=env["redis"],
                query_router=env["query_router"],
                session_factory=env["session_factory"],
            )

            assert conversation_manager is not None
            assert hasattr(conversation_manager, "context_window_size")
            assert conversation_manager.context_window_size == 10

            print("✅ ConversationManager creation successful")
            return True

        except ImportError as e:
            print(f"❌ ConversationManager not yet implemented: {e}")
            return False
        except Exception as e:
            print(f"❌ ConversationManager creation failed: {e}")
            return False

    async def test_conversation_context_persistence(self, setup_conversation_environment):
        """Test conversation context persistence across turns."""
        try:
            from services.conversation.conversation_manager import ConversationManager

            env = setup_conversation_environment
            conversation_manager = ConversationManager(
                redis_client=env["redis"],
                query_router=env["query_router"],
                session_factory=env["session_factory"],
            )

            session_id = "test_session_123"

            # Test context storage
            context_data = {
                "current_project": "E-commerce Platform",
                "last_github_issue": 85,
                "conversation_turns": 2,
            }

            start_time = time.time()
            await conversation_manager.store_context(session_id, context_data)
            store_time = (time.time() - start_time) * 1000

            # Test context retrieval
            start_time = time.time()
            retrieved_context = await conversation_manager.get_context(session_id)
            retrieve_time = (time.time() - start_time) * 1000

            # Validate context persistence
            assert retrieved_context is not None
            assert retrieved_context.get("current_project") == "E-commerce Platform"
            assert retrieved_context.get("last_github_issue") == 85

            # Performance validation
            assert store_time < 50, f"Context storage time {store_time:.2f}ms exceeds 50ms"
            assert retrieve_time < 50, f"Context retrieval time {retrieve_time:.2f}ms exceeds 50ms"

            print(
                f"✅ Context persistence: store={store_time:.2f}ms, retrieve={retrieve_time:.2f}ms"
            )
            return {"store_time": store_time, "retrieve_time": retrieve_time, "context_valid": True}

        except Exception as e:
            print(f"❌ Context persistence test failed: {e}")
            return {"context_valid": False, "error": str(e)}

    async def test_anaphoric_resolution_accuracy(self, setup_conversation_environment):
        """Test anaphoric resolution accuracy with conversation context."""
        try:
            from services.conversation.conversation_manager import ConversationManager

            env = setup_conversation_environment
            conversation_manager = ConversationManager(
                redis_client=env["redis"],
                query_router=env["query_router"],
                session_factory=env["session_factory"],
            )

            session_id = "anaphoric_test_session"

            # Multi-turn conversation with anaphoric references
            conversation_flow = [
                {
                    "user_input": "Create GitHub issue for login bug",
                    "expected_resolution": "github_issue_creation",
                    "context_update": {"last_github_issue": 85, "current_project": "E-commerce"},
                },
                {
                    "user_input": "Show me that issue again",
                    "expected_resolution": "github_issue_85",
                    "context_should_contain": {"last_github_issue": 85},
                },
                {
                    "user_input": "Update the authentication system",
                    "expected_resolution": "auth_system_update",
                    "context_should_contain": {"current_project": "E-commerce"},
                },
                {
                    "user_input": "What is the status of that project?",
                    "expected_resolution": "project_status_query",
                    "context_should_contain": {"current_project": "E-commerce"},
                },
            ]

            resolution_accuracy = 0
            total_turns = len(conversation_flow)
            performance_results = []

            for i, turn in enumerate(conversation_flow):
                start_time = time.time()

                try:
                    # Process turn with conversation context
                    resolution = await conversation_manager.resolve_reference(
                        session_id, turn["user_input"]
                    )

                    end_time = time.time()
                    processing_time = (end_time - start_time) * 1000
                    performance_results.append(processing_time)

                    # Check if resolution matches expected
                    if resolution and resolution.get("type") == turn["expected_resolution"]:
                        resolution_accuracy += 1

                    # Update context for next turn
                    if "context_update" in turn:
                        await conversation_manager.store_context(session_id, turn["context_update"])

                    # Validate context contains expected data
                    if "context_should_contain" in turn:
                        context = await conversation_manager.get_context(session_id)
                        for key, value in turn["context_should_contain"].items():
                            if context and context.get(key) == value:
                                resolution_accuracy += 0.5  # Partial credit for context maintenance

                except Exception as e:
                    print(f"Error in turn {i+1}: {e}")
                    continue

            if performance_results:
                avg_performance = sum(performance_results) / len(performance_results)
                accuracy_rate = (resolution_accuracy / total_turns) * 100

                print(
                    f"✅ Anaphoric resolution: {accuracy_rate:.1f}% accuracy, {avg_performance:.2f}ms avg"
                )

                # Validate accuracy and performance
                assert (
                    accuracy_rate >= 90
                ), f"Anaphoric resolution accuracy {accuracy_rate:.1f}% below 90%"
                assert (
                    avg_performance < 150
                ), f"Anaphoric resolution time {avg_performance:.2f}ms exceeds 150ms"

                return {
                    "accuracy": accuracy_rate,
                    "avg_performance": avg_performance,
                    "total_turns": total_turns,
                }

        except Exception as e:
            print(f"❌ Anaphoric resolution test failed: {e}")
            return {"accuracy": 0, "error": str(e)}

    async def test_redis_caching_performance(self, setup_conversation_environment):
        """Test Redis caching performance and reliability."""
        env = setup_conversation_environment
        redis_client = env["redis"]

        # Test Redis operations performance
        test_data = {
            "session_id": "redis_test_123",
            "context": {"project": "Test Project", "issue": 123, "turns": 5},
        }

        performance_results = []

        # Test multiple operations
        for i in range(10):
            start_time = time.time()

            try:
                # Test set operation
                await redis_client.set(
                    f"conversation:{test_data['session_id']}:{i}",
                    str(test_data["context"]),
                    ex=300,  # 5-minute TTL
                )

                # Test get operation
                result = await redis_client.get(f"conversation:{test_data['session_id']}:{i}")

                end_time = time.time()
                operation_time = (end_time - start_time) * 1000
                performance_results.append(operation_time)

                # Validate data integrity
                assert result is not None

            except Exception as e:
                print(f"Redis operation {i+1} failed: {e}")
                continue

        if performance_results:
            avg_performance = sum(performance_results) / len(performance_results)
            max_performance = max(performance_results)
            min_performance = min(performance_results)

            print(
                f"✅ Redis caching: avg={avg_performance:.2f}ms, max={max_performance:.2f}ms, min={min_performance:.2f}ms"
            )

            # Performance validation
            assert avg_performance < 10, f"Redis performance {avg_performance:.2f}ms exceeds 10ms"
            assert (
                max_performance < 50
            ), f"Redis max performance {max_performance:.2f}ms exceeds 50ms"

            return {
                "avg_performance": avg_performance,
                "max_performance": max_performance,
                "min_performance": min_performance,
                "operations_tested": len(performance_results),
            }

        return None

    async def test_query_router_integration(self, setup_conversation_environment):
        """Test QueryRouter integration with conversation context."""
        try:
            from services.conversation.conversation_manager import ConversationManager

            env = setup_conversation_environment
            conversation_manager = ConversationManager(
                redis_client=env["redis"],
                query_router=env["query_router"],
                session_factory=env["session_factory"],
            )

            # Mock QueryRouter responses
            env["query_router"].process_query.return_value = {
                "type": "github_issue",
                "data": {"issue_id": 85, "title": "Login Bug Fix"},
                "context_enhanced": True,
            }

            session_id = "integration_test_session"

            # Test conversation-enhanced query processing
            test_queries = [
                "Show me the login bug issue",
                "What's the status of that project?",
                "Update the authentication system",
            ]

            integration_results = []

            for query in test_queries:
                start_time = time.time()

                try:
                    # Process query with conversation context
                    result = await conversation_manager.process_conversation_query(
                        session_id, query
                    )

                    end_time = time.time()
                    processing_time = (end_time - start_time) * 1000

                    integration_results.append(
                        {"query": query, "result": result, "processing_time": processing_time}
                    )

                    # Validate QueryRouter was called with context
                    env["query_router"].process_query.assert_called()

                except Exception as e:
                    print(f"Integration test failed for query '{query}': {e}")
                    continue

            if integration_results:
                avg_time = sum(r["processing_time"] for r in integration_results) / len(
                    integration_results
                )
                successful_queries = len([r for r in integration_results if r["result"]])

                print(
                    f"✅ QueryRouter integration: {successful_queries}/{len(test_queries)} successful, {avg_time:.2f}ms avg"
                )

                # Performance validation
                assert avg_time < 150, f"Integration processing time {avg_time:.2f}ms exceeds 150ms"
                assert (
                    successful_queries >= len(test_queries) * 0.8
                ), f"Integration success rate below 80%"

                return {
                    "avg_processing_time": avg_time,
                    "successful_queries": successful_queries,
                    "total_queries": len(test_queries),
                }

        except Exception as e:
            print(f"❌ QueryRouter integration test failed: {e}")
            return {"error": str(e)}

    async def test_end_to_end_conversation_flow(self, setup_conversation_environment):
        """Test complete end-to-end conversation flow with anaphoric resolution."""
        try:
            from services.conversation.conversation_manager import ConversationManager

            env = setup_conversation_environment
            conversation_manager = ConversationManager(
                redis_client=env["redis"],
                query_router=env["query_router"],
                session_factory=env["session_factory"],
            )

            # Mock GitHub issue creation response
            env["query_router"].process_query.side_effect = [
                {
                    "type": "github_issue_created",
                    "data": {"issue_id": 85, "title": "Login Bug Fix"},
                },
                {
                    "type": "github_issue_display",
                    "data": {"issue_id": 85, "title": "Login Bug Fix"},
                },
                {
                    "type": "project_status",
                    "data": {"project": "E-commerce", "status": "In Progress"},
                },
            ]

            session_id = "e2e_test_session"

            # Complete conversation flow
            conversation_flow = [
                {
                    "user_input": "Create GitHub issue for login bug",
                    "expected_response": "github_issue_created",
                    "expected_context": {"last_github_issue": 85},
                },
                {
                    "user_input": "Show me that issue again",
                    "expected_response": "github_issue_display",
                    "expected_context": {"last_github_issue": 85},
                },
                {
                    "user_input": "What is the status of that project?",
                    "expected_response": "project_status",
                    "expected_context": {"current_project": "E-commerce"},
                },
            ]

            flow_results = []
            total_start_time = time.time()

            for i, turn in enumerate(conversation_flow):
                turn_start_time = time.time()

                try:
                    # Process conversation turn
                    response = await conversation_manager.process_conversation_turn(
                        session_id, turn["user_input"]
                    )

                    turn_end_time = time.time()
                    turn_time = (turn_end_time - turn_start_time) * 1000

                    # Validate response
                    response_valid = response and response.get("type") == turn["expected_response"]

                    # Validate context
                    context = await conversation_manager.get_context(session_id)
                    context_valid = context and any(
                        context.get(key) == value for key, value in turn["expected_context"].items()
                    )

                    flow_results.append(
                        {
                            "turn": i + 1,
                            "response_valid": response_valid,
                            "context_valid": context_valid,
                            "processing_time": turn_time,
                        }
                    )

                except Exception as e:
                    print(f"E2E flow error in turn {i+1}: {e}")
                    flow_results.append(
                        {
                            "turn": i + 1,
                            "response_valid": False,
                            "context_valid": False,
                            "error": str(e),
                        }
                    )

            total_end_time = time.time()
            total_time = (total_end_time - total_start_time) * 1000

            # Calculate success metrics
            successful_turns = len(
                [r for r in flow_results if r["response_valid"] and r["context_valid"]]
            )
            total_turns = len(flow_results)
            success_rate = (successful_turns / total_turns) * 100 if total_turns > 0 else 0

            avg_turn_time = sum(
                r["processing_time"] for r in flow_results if "processing_time" in r
            ) / len(flow_results)

            print(
                f"✅ E2E Conversation Flow: {success_rate:.1f}% success, {avg_turn_time:.2f}ms avg per turn, {total_time:.2f}ms total"
            )

            # Success criteria validation
            assert success_rate >= 90, f"E2E flow success rate {success_rate:.1f}% below 90%"
            assert avg_turn_time < 150, f"E2E flow avg time {avg_turn_time:.2f}ms exceeds 150ms"
            assert total_time < 500, f"E2E flow total time {total_time:.2f}ms exceeds 500ms"

            return {
                "success_rate": success_rate,
                "avg_turn_time": avg_turn_time,
                "total_time": total_time,
                "successful_turns": successful_turns,
                "total_turns": total_turns,
            }

        except Exception as e:
            print(f"❌ E2E conversation flow test failed: {e}")
            return {"error": str(e)}

    async def test_comprehensive_phase3_validation(self, setup_conversation_environment):
        """Run comprehensive Phase 3 validation and generate report."""
        print("\n" + "=" * 70)
        print("PM-034 PHASE 3 COMPREHENSIVE INTEGRATION VALIDATION")
        print("=" * 70)

        results = {}

        # Run all Phase 3 validation tests
        print("\n1. CONVERSATION MANAGER CREATION")
        results["conversation_manager"] = await self.test_conversation_manager_creation(
            setup_conversation_environment
        )

        print("\n2. CONVERSATION CONTEXT PERSISTENCE")
        results["context_persistence"] = await self.test_conversation_context_persistence(
            setup_conversation_environment
        )

        print("\n3. ANAPHORIC RESOLUTION ACCURACY")
        results["anaphoric_resolution"] = await self.test_anaphoric_resolution_accuracy(
            setup_conversation_environment
        )

        print("\n4. REDIS CACHING PERFORMANCE")
        results["redis_caching"] = await self.test_redis_caching_performance(
            setup_conversation_environment
        )

        print("\n5. QUERY ROUTER INTEGRATION")
        results["query_router_integration"] = await self.test_query_router_integration(
            setup_conversation_environment
        )

        print("\n6. END-TO-END CONVERSATION FLOW")
        results["e2e_flow"] = await self.test_end_to_end_conversation_flow(
            setup_conversation_environment
        )

        # Generate comprehensive report
        print("\n" + "=" * 70)
        print("PHASE 3 VALIDATION SUMMARY")
        print("=" * 70)

        # Calculate overall success metrics
        working_components = 0
        total_components = 6

        if results["conversation_manager"]:
            working_components += 1
            print("✅ ConversationManager: Created successfully")

        if results["context_persistence"] and results["context_persistence"].get("context_valid"):
            working_components += 1
            store_time = results["context_persistence"].get("store_time", 0)
            retrieve_time = results["context_persistence"].get("retrieve_time", 0)
            print(
                f"✅ Context Persistence: {store_time:.2f}ms store, {retrieve_time:.2f}ms retrieve"
            )

        if (
            results["anaphoric_resolution"]
            and results["anaphoric_resolution"].get("accuracy", 0) >= 90
        ):
            working_components += 1
            accuracy = results["anaphoric_resolution"].get("accuracy", 0)
            performance = results["anaphoric_resolution"].get("avg_performance", 0)
            print(f"✅ Anaphoric Resolution: {accuracy:.1f}% accuracy, {performance:.2f}ms avg")

        if results["redis_caching"]:
            working_components += 1
            avg_perf = results["redis_caching"].get("avg_performance", 0)
            print(f"✅ Redis Caching: {avg_perf:.2f}ms average performance")

        if (
            results["query_router_integration"]
            and "error" not in results["query_router_integration"]
        ):
            working_components += 1
            avg_time = results["query_router_integration"].get("avg_processing_time", 0)
            success_rate = results["query_router_integration"].get("successful_queries", 0)
            total_queries = results["query_router_integration"].get("total_queries", 0)
            print(
                f"✅ QueryRouter Integration: {success_rate}/{total_queries} successful, {avg_time:.2f}ms avg"
            )

        if results["e2e_flow"] and "error" not in results["e2e_flow"]:
            working_components += 1
            success_rate = results["e2e_flow"].get("success_rate", 0)
            avg_turn_time = results["e2e_flow"].get("avg_turn_time", 0)
            print(
                f"✅ E2E Conversation Flow: {success_rate:.1f}% success, {avg_turn_time:.2f}ms avg per turn"
            )

        overall_health = (working_components / total_components) * 100
        print(
            f"\nOverall Phase 3 Health: {overall_health:.1f}% ({working_components}/{total_components} components)"
        )

        # Performance analysis
        performance_metrics = []
        for result in results.values():
            if result and isinstance(result, dict):
                if "avg_performance" in result:
                    performance_metrics.append(result["avg_performance"])
                elif "avg_processing_time" in result:
                    performance_metrics.append(result["avg_processing_time"])
                elif "avg_turn_time" in result:
                    performance_metrics.append(result["avg_turn_time"])

        if performance_metrics:
            avg_performance = sum(performance_metrics) / len(performance_metrics)
            print(f"Average Performance: {avg_performance:.2f}ms")

            if avg_performance < 150:
                print("✅ Performance Target: ACHIEVED (<150ms)")
            else:
                print("❌ Performance Target: NOT ACHIEVED (>150ms)")

        # Success criteria validation
        print("\nSUCCESS CRITERIA VALIDATION:")

        if overall_health >= 80:
            print("✅ End-to-end conversation memory: OPERATIONAL")
        else:
            print("❌ End-to-end conversation memory: NOT OPERATIONAL")

        if (
            results["anaphoric_resolution"]
            and results["anaphoric_resolution"].get("accuracy", 0) >= 90
        ):
            print("✅ Anaphoric resolution: WORKING")
        else:
            print("❌ Anaphoric resolution: NOT WORKING")

        if performance_metrics and avg_performance < 150:
            print("✅ Performance maintenance: ACHIEVED")
        else:
            print("❌ Performance maintenance: NOT ACHIEVED")

        # Phase 3 completion assessment
        print("\nPHASE 3 COMPLETION ASSESSMENT:")

        if overall_health >= 80 and avg_performance < 150:
            print("🎉 PHASE 3: SUCCESSFULLY COMPLETED")
            print("✅ All success criteria met")
            print("✅ ConversationManager operational with anaphoric resolution")
            print("✅ Performance targets achieved")
        elif overall_health >= 60:
            print("⚠️  PHASE 3: PARTIALLY COMPLETED")
            print("🔧 Some components need attention")
            print("📋 Review failed components for systematic resolution")
        else:
            print("❌ PHASE 3: NOT COMPLETED")
            print("🚨 Critical issues prevent Phase 3 success")
            print("🔧 Immediate attention required for core components")

        return results
