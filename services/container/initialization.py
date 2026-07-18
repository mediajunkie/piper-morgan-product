"""Service initialization logic."""

import logging
from typing import Optional

from services.container.exceptions import ServiceInitializationError
from services.container.service_registry import ServiceRegistry

logger = logging.getLogger(__name__)


class ServiceInitializer:
    """Handles service initialization in correct order."""

    def __init__(self, registry: ServiceRegistry):
        self.registry = registry

    async def initialize_all(self) -> None:
        """
        Initialize all services in correct dependency order.

        Order:
        1. LLM service (no dependencies)
        2. Intent service (depends on LLM; dispatch via task_type registry, #1094)
        """
        logger.info("Starting service initialization sequence")

        await self._initialize_llm_service()
        self._initialize_intent_service()
        self._initialize_process_registry()

        logger.info("Service initialization sequence complete")

    async def _initialize_llm_service(self) -> None:
        """Initialize LLM service."""
        try:
            logger.info("Initializing LLM service")

            # Import here to avoid circular imports
            from services.domain.llm_domain_service import LLMDomainService

            # Create LLM service
            llm_service = LLMDomainService()

            # Initialize (async validation)
            await llm_service.initialize()

            # Register
            self.registry.register(
                "llm", llm_service, metadata={"version": "1.0", "dependencies": []}
            )

            logger.info("LLM service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {e}", exc_info=True)
            raise ServiceInitializationError("llm", e)

    def _initialize_intent_service(self) -> None:
        """Initialize Intent service (depends on LLM)."""
        try:
            logger.info("Initializing Intent service")

            from services.intent.intent_service import IntentService
            from services.intent_service.classifier import IntentClassifier

            # Get LLM service from registry (Issue #322: proper DI for classifier)
            llm_service = self.registry.get("llm")

            # Issue #560: Create classifier with LLM service properly injected
            intent_classifier = IntentClassifier(llm_service=llm_service)

            # Issue #563: Create ConversationManager for turn persistence
            from services.conversation.conversation_manager import ConversationManager

            conversation_manager = ConversationManager()

            intent_service = IntentService(
                intent_classifier=intent_classifier,
                conversation_manager=conversation_manager,  # Issue #563
            )

            self.registry.register(
                "intent",
                intent_service,
                metadata={"version": "1.0", "dependencies": ["llm"]},
            )

            logger.info("Intent service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Intent service: {e}", exc_info=True)
            raise ServiceInitializationError("intent", e)

    def _initialize_process_registry(self) -> None:
        """
        Initialize ProcessRegistry for guided processes (ADR-049).

        Registers default guided process adapters (onboarding, standup).
        Must be called after intent service initialization.
        """
        try:
            logger.info("Initializing ProcessRegistry (ADR-049)")

            # Import here to avoid circular imports
            from services.process import register_default_processes

            # Register default guided processes (standup; onboarding on ice per ADR-059)
            register_default_processes()

            # ADR-059: Register workflow dispatcher entry points
            from services.intent_service.workflow_entries import register_default_workflows

            register_default_workflows()

            # Validate workflow registry at startup
            from services.intent_service.workflow_dispatcher import validate_registry

            errors = validate_registry()
            if errors:
                for err in errors:
                    logger.error(f"workflow_registry_validation_error: {err}")  # #1436: stdlib logger
            else:
                logger.info("WorkflowDispatcher validated successfully")

            logger.info("ProcessRegistry initialized successfully")

        except Exception as e:
            # Non-fatal: log warning but don't fail startup
            # The old check methods still exist as fallback
            logger.warning(f"Failed to initialize ProcessRegistry: {e}", exc_info=True)
