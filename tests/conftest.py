"""
conftest.py — Minimal test infrastructure for Piper Morgan
"""

import os
import sys
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


# Basic fixtures that don't depend on services that may not exist
@pytest.fixture
def mock_session():
    """Provide a mock session for tests that need it"""
    return Mock()


@pytest.fixture
def mock_async_session():
    """Provide a mock async session for tests that need it"""
    return AsyncMock()


# GREAT-5 Phase 1.5: IntentService test fixtures
# Updated in #212 Phase 0 to add ServiceRegistry initialization (required after #217 refactoring)
@pytest.fixture
async def intent_service():
    """
    Provide properly initialized IntentService for testing.

    This fixture ensures IntentService is available with all required dependencies:
    - ServiceRegistry with LLM service (#217 refactoring requirement)
    - OrchestrationEngine (None for tests)
    - Intent classifier
    - Conversation handler

    Created in GREAT-5 Phase 1.5 to fix initialization issues revealed by
    stricter test assertions in Phase 1.
    Updated in #212 Phase 0 for #217 ServiceRegistry pattern.
    """
    import sys

    from services.conversation.conversation_handler import ConversationHandler
    from services.domain.llm_domain_service import LLMDomainService
    from services.intent.intent_service import IntentService
    from services.intent_service import classifier
    from services.service_registry import ServiceRegistry

    print("[FIXTURE DEBUG] Starting fixture setup", file=sys.stderr)

    # Initialize ServiceRegistry with LLM domain service (required after #217)
    llm_domain_service = LLMDomainService()
    await llm_domain_service.initialize()  # Must initialize before use

    print(
        f"[FIXTURE DEBUG] Before register. Registry: {list(ServiceRegistry._services.keys())}",
        file=sys.stderr,
    )
    ServiceRegistry.register("llm", llm_domain_service)
    print(
        f"[FIXTURE DEBUG] After register. Registry: {list(ServiceRegistry._services.keys())}",
        file=sys.stderr,
    )

    # Initialize IntentService with test configuration
    service = IntentService(
        orchestration_engine=None,  # Tests don't need real orchestration
        intent_classifier=classifier,
        conversation_handler=ConversationHandler(session_manager=None),
    )

    yield service

    # Cleanup: Reset classifier's cached LLM and clear ServiceRegistry
    # The classifier singleton caches the LLM reference, which becomes stale
    # when we clear the registry. Must reset it for next test.
    classifier._llm = None
    ServiceRegistry._services.clear()


@pytest.fixture
def client_with_intent():
    """
    FastAPI TestClient with IntentService properly initialized in app.state.

    This ensures tests using the web API have access to a working IntentService,
    preventing "IntentService not available - initialization failed" errors.

    Created in GREAT-5 Phase 1.5.
    """
    from fastapi.testclient import TestClient

    from services.conversation.conversation_handler import ConversationHandler
    from services.intent.intent_service import IntentService
    from services.intent_service import classifier
    from web.app import app

    # Ensure IntentService is initialized in app.state
    if not hasattr(app.state, "intent_service") or app.state.intent_service is None:
        app.state.intent_service = IntentService(
            orchestration_engine=None,
            intent_classifier=classifier,
            conversation_handler=ConversationHandler(session_manager=None),
        )

    client = TestClient(app)
    return client
