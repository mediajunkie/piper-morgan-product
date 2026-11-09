"""
Integration test for Service Container (Phase 1.5)

Tests the complete service container flow with real service initialization.
This verifies the DDD pattern works end-to-end.

Note: Requires LLM API keys in environment for full test coverage.
"""

import pytest

from services.container import ServiceContainer


@pytest.mark.asyncio
async def test_service_container_full_lifecycle():
    """
    Integration test: Full service container lifecycle.

    Tests:
    1. Container initialization
    2. Service registration (LLM, Intent)
    3. Service retrieval
    4. Service functionality
    5. Container shutdown
    """
    # Reset container to clean state
    ServiceContainer.reset()

    # Create container
    container = ServiceContainer()

    # Verify not initialized yet
    assert not container.is_initialized()
    assert container.list_services() == []

    # Initialize container (async)
    await container.initialize()

    # Verify initialized
    assert container.is_initialized()

    # Verify expected services registered
    services = container.list_services()
    assert "llm" in services, "LLM service should be registered"
    assert "intent" in services, "Intent service should be registered"

    # Get LLM service
    llm_service = container.get_service("llm")
    assert llm_service is not None
    assert hasattr(llm_service, "initialize")

    # Get Intent service
    intent_service = container.get_service("intent")
    assert intent_service is not None
    assert hasattr(intent_service, "process_intent")

    # Verify has_service works
    assert container.has_service("llm")
    assert container.has_service("intent")
    assert not container.has_service("nonexistent")

    # Verify idempotent initialization
    await container.initialize()  # Should not re-initialize
    assert container.is_initialized()
    assert len(container.list_services()) == 2  # Still just 2 services

    # Shutdown
    container.shutdown()

    # Verify shutdown
    assert not container.is_initialized()
    assert container.list_services() == []

    # Clean up
    ServiceContainer.reset()


# test_multiple_containers_are_singleton asserted the singleton that #322 removed on
# purpose (one container per app via the lifespan; the unit tier pins that).
# Removed 2026-11-09 off the full-suite backlog (1452).


@pytest.mark.asyncio
async def test_service_container_with_missing_api_keys():
    """
    Integration test: Container initialization gracefully handles missing API keys.

    Note: This test may fail if API keys are present in environment.
    """
    import os

    # Save original keys
    original_anthropic = os.environ.get("ANTHROPIC_API_KEY")
    original_openai = os.environ.get("OPENAI_API_KEY")

    try:
        # Remove API keys temporarily
        if "ANTHROPIC_API_KEY" in os.environ:
            del os.environ["ANTHROPIC_API_KEY"]
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        # Reset container
        ServiceContainer.reset()

        # Create container
        container = ServiceContainer()

        # Initialize should handle missing keys gracefully
        # (LLMDomainService should initialize but providers_initialized = False)
        await container.initialize()

        # Container should still be initialized
        assert container.is_initialized()

        # Services should be registered
        assert container.has_service("llm")
        assert container.has_service("intent")

        # LLM service should exist
        llm_service = container.get_service("llm")
        assert hasattr(llm_service, "is_initialized")
        # Note: LLM service may still initialize successfully with default config

        # Clean up
        ServiceContainer.reset()

    finally:
        # Restore original keys
        if original_anthropic is not None:
            os.environ["ANTHROPIC_API_KEY"] = original_anthropic
        if original_openai is not None:
            os.environ["OPENAI_API_KEY"] = original_openai


@pytest.mark.asyncio
async def test_container_survives_service_access_before_init():
    """
    Integration test: Accessing services before initialization raises proper error.
    """
    # Reset container
    ServiceContainer.reset()

    # Create container
    container = ServiceContainer()

    # Try to access service before initialization
    from services.container.exceptions import ContainerNotInitializedError

    with pytest.raises(ContainerNotInitializedError):
        container.get_service("llm")

    # Now initialize
    await container.initialize()

    # Now service access should work
    llm_service = container.get_service("llm")
    assert llm_service is not None

    # Clean up
    ServiceContainer.reset()


@pytest.mark.asyncio
async def test_container_service_not_found_error():
    """
    Integration test: Requesting non-existent service raises proper error.
    """
    # Reset and initialize container
    ServiceContainer.reset()
    container = ServiceContainer()
    await container.initialize()

    # Request non-existent service
    from services.container.exceptions import ServiceNotFoundError

    with pytest.raises(ServiceNotFoundError) as exc_info:
        container.get_service("nonexistent_service")

    # Verify error message includes available services
    error_msg = str(exc_info.value)
    assert "nonexistent_service" in error_msg
    assert "llm" in error_msg  # Should list available services
    assert "intent" in error_msg

    # Clean up
    ServiceContainer.reset()
