"""
Startup Phase Manager for web/app.py

Purpose: Extract lifespan startup/shutdown logic into separate, testable phases.
This follows DDD pattern with each phase handling a single responsibility.

Status: Phase 2 of web/app.py refactoring (Issue #385 - INFR-MAINT-REFACTOR)
Impact: Reduces lifespan from 200+ lines to 25 lines, makes startup testable
"""

from contextlib import asynccontextmanager
from typing import Optional

import structlog

logger = structlog.get_logger()


class ServiceContainerPhase:
    """Phase 1.5: ServiceContainer initialization (DDD pattern)"""

    @staticmethod
    async def startup(app) -> None:
        """Initialize ServiceContainer and store in app state"""
        print("\n" + "=" * 60)
        print("🔧 Phase 1.5: Initializing ServiceContainer (DDD pattern)")
        print("=" * 60)

        from services.container import ServiceContainer

        container = ServiceContainer()

        if not container.is_initialized():
            logger.info("Container not initialized, initializing now...")
            await container.initialize()
            print("✅ Phase 1.5: ServiceContainer initialized successfully")
            print(f"   Services available: {container.list_services()}")
        else:
            logger.info("Container already initialized (started via main.py)")
            print("✅ Phase 1.5: ServiceContainer already initialized")
            print(f"   Services available: {container.list_services()}")

        # Store container in app state for access
        app.state.service_container = container

    @staticmethod
    async def shutdown(app) -> None:
        """Shutdown ServiceContainer"""
        print("\n🔧 Shutting down ServiceContainer...")
        if hasattr(app.state, "service_container") and app.state.service_container:
            try:
                app.state.service_container.shutdown()
                print("✅ ServiceContainer shutdown successful")
            except Exception as e:
                print(f"⚠️ ServiceContainer shutdown error: {e}")


class ConfigValidationPhase:
    """GREAT-2D: Configuration validation at startup"""

    @staticmethod
    async def startup(app) -> None:
        """Validate configuration and store results in app state"""
        print("\n" + "=" * 60)
        print("🔍 CORE-GREAT-2D: Configuration Validation")
        print("=" * 60)

        try:
            from services.infrastructure.config.config_validator import ConfigValidator

            validator = ConfigValidator()
            validator.validate_all()
            validator.print_summary()

            # Store validation results in app state
            app.state.config_validation = validator.get_summary()

            # Warning for invalid configurations (but don't fail startup)
            if not validator.is_all_valid():
                invalid_services = validator.get_invalid_services()
                print("\n⚠️ WARNING: Some service configurations are invalid")
                print("Services will operate in degraded mode\n")
            else:
                print("✅ All service configurations valid\n")

        except Exception as e:
            print(f"❌ Configuration validation failed: {e}")
            print("⚠️ Continuing startup without validation\n")
            app.state.config_validation = {"error": str(e)}


class SchemaValidationPhase:
    """Issue #484: Schema validation at startup

    Validates that SQLAlchemy models match actual database schema.
    Catches model/schema drift before runtime failures occur.

    Can be disabled via PIPER_SKIP_SCHEMA_VALIDATION=1 env var.
    """

    @staticmethod
    async def startup(app) -> None:
        """Validate database schema against models"""
        from services.infrastructure.schema_validator import SchemaValidator, is_validation_disabled

        print("\n" + "=" * 60)
        print("🔍 Issue #484: Database Schema Validation")
        print("=" * 60)

        if is_validation_disabled():
            print("⏭️ Schema validation skipped (PIPER_SKIP_SCHEMA_VALIDATION=1)")
            app.state.schema_validation = {"skipped": True}
            return

        try:
            validator = SchemaValidator()
            result = await validator.validate()
            validator.print_report()

            # Store validation results in app state
            app.state.schema_validation = {
                "is_valid": result.is_valid,
                "tables_checked": result.tables_checked,
                "columns_checked": result.columns_checked,
                "mismatches": len(result.mismatches),
            }

            if not result.is_valid:
                # Log mismatches but don't fail startup (yet)
                # In future, could make this configurable to fail-fast
                print("\n⚠️ WARNING: Schema drift detected!")
                print("Database may not match models. Check logs for details.")
                print("This could cause runtime errors.\n")
            else:
                print("✅ All models match database schema\n")

        except Exception as e:
            print(f"❌ Schema validation failed: {e}")
            print("⚠️ Continuing startup without schema validation\n")
            app.state.schema_validation = {"error": str(e)}


class ServiceRetrievalPhase:
    """Phase 1.5: Get services from ServiceContainer"""

    @staticmethod
    async def startup(app) -> None:
        """Retrieve services from container and store in app state.

        #1116 fix 2026-05-25: orchestration service was deleted in #1094 but
        this phase still hard-required it. The outer except was clobbering
        the successfully-set intent_service + llm_service when orchestration
        get_service raised. Now orchestration is in its own nested try since
        it's expected-absent post-#1094, and the outer except only nulls
        attrs that weren't successfully set.
        """
        # Default to None so the except path doesn't clobber valid attrs
        if not hasattr(app.state, "intent_service"):
            app.state.intent_service = None
        if not hasattr(app.state, "llm_service"):
            app.state.llm_service = None
        if not hasattr(app.state, "orchestration_engine"):
            app.state.orchestration_engine = None

        try:
            print("\n🔧 Phase 1.5: Getting services from ServiceContainer...")

            container = app.state.service_container

            # Get IntentService from container
            intent_service = container.get_service("intent")
            app.state.intent_service = intent_service
            print(f"✅ IntentService retrieved from container")

            # Get LLM service from container (for backward compatibility)
            llm_service = container.get_service("llm")
            app.state.llm_service = llm_service
            print(f"✅ LLM service retrieved from container")

            # Get OrchestrationEngine from container — expected-absent post-#1094
            # (γ-preserve deletion of OrchestrationEngine + WorkflowFactory).
            # Don't let its absence clobber the successfully-retrieved intent +
            # llm services above.
            try:
                orchestration_engine = container.get_service("orchestration")
                app.state.orchestration_engine = orchestration_engine
                print(f"✅ OrchestrationEngine retrieved from container")
            except Exception as oe:
                app.state.orchestration_engine = None
                print(f"⚠️  OrchestrationEngine not in container (expected post-#1094): {oe}")

            print("✅ Phase 1.5: All services retrieved from ServiceContainer\n")

        except Exception as e:
            print(f"❌ Phase 1.5: Failed to get services from container: {e}")
            print("⚠️ Continuing with degraded service availability\n")
            # Only null services we didn't successfully set above (preserves
            # any successful retrievals before the exception).
            if not getattr(app.state, "intent_service", None):
                app.state.intent_service = None
            if not getattr(app.state, "llm_service", None):
                app.state.llm_service = None
            if not getattr(app.state, "orchestration_engine", None):
                app.state.orchestration_engine = None


class WebComponentsInitializationPhase:
    """Phase 4: Web component initialization (templates, parsers, enhancers)"""

    @staticmethod
    async def startup(app) -> None:
        """Initialize web-specific components and store in app state"""
        print("\n" + "=" * 60)
        print("🎨 Phase 4: Initializing Web Components")
        print("=" * 60)

        try:
            from pathlib import Path

            from fastapi.templating import Jinja2Templates

            from web.personality_integration import PersonalityResponseEnhancer, PiperConfigParser

            # Get project root for template path
            project_root = Path(__file__).parent.parent

            # Initialize Jinja2Templates
            templates = Jinja2Templates(directory=str(project_root / "templates"))
            app.state.templates = templates
            print("✅ Jinja2Templates initialized")

            # Initialize PiperConfigParser
            config_parser = PiperConfigParser()
            app.state.config_parser = config_parser
            print("✅ PiperConfigParser initialized")

            # Initialize PersonalityResponseEnhancer
            personality_enhancer = PersonalityResponseEnhancer()
            app.state.personality_enhancer = personality_enhancer
            print("✅ PersonalityResponseEnhancer initialized")

            # Get port configuration (for reference - used in __main__)
            from services.configuration.port_configuration_service import get_port_configuration

            port_config = get_port_configuration()
            app.state.port_config = port_config
            print("✅ Port configuration loaded")

            print("✅ Phase 4: Web Components initialized successfully\n")

        except Exception as e:
            print(f"❌ Phase 4: Failed to initialize web components: {e}")
            print("⚠️ Continuing without full web component initialization\n")
            # Set to None so routes can detect missing components
            app.state.templates = None
            app.state.config_parser = None
            app.state.personality_enhancer = None
            app.state.port_config = None


class PluginInitializationPhase:
    """Phase 3B: Plugin system initialization"""

    @staticmethod
    async def startup(app) -> None:
        """Initialize plugin system and mount plugin routers"""
        print("\n🔌 Phase 3B: Initializing Plugin System...")

        try:
            from services.plugins import get_plugin_registry

            registry = get_plugin_registry()

            # Discover and load enabled plugins from config
            load_results = registry.load_enabled_plugins()

            success_count = sum(1 for success in load_results.values() if success)
            total_count = len(load_results)

            if total_count == 0:
                print("  ⚠️  No plugins enabled in configuration")
            else:
                print(f"  📦 Loaded {success_count}/{total_count} plugin(s)")
                for name, success in load_results.items():
                    status = "✅" if success else "❌"
                    print(f"    {status} {name}")

            # Initialize all registered plugins
            init_results = await registry.initialize_all()

            success_count = sum(1 for success in init_results.values() if success)
            total_count = len(init_results)

            print(f"  ✅ Initialized {success_count}/{total_count} plugin(s)")

            # Mount plugin routers
            routers = registry.get_routers()
            for router in routers:
                app.include_router(router)

            print(f"  ✅ Mounted {len(routers)} router(s)")

            # Store registry in app state for access
            app.state.plugin_registry = registry

            print(f"✅ Plugin system initialized\n")

        except Exception as e:
            print(f"⚠️ Plugin system initialization failed: {e}")
            print("   Continuing without plugin system\n")
            # Don't fail startup if plugin system has issues
            app.state.plugin_registry = None

    @staticmethod
    async def shutdown(app) -> None:
        """Shutdown plugin system"""
        print("\n🔌 Shutting down Plugin System...")

        if hasattr(app.state, "plugin_registry") and app.state.plugin_registry:
            try:
                shutdown_results = await app.state.plugin_registry.shutdown_all()
                success_count = sum(1 for success in shutdown_results.values() if success)
                print(f"✅ Plugin shutdown: {success_count}/{len(shutdown_results)} successful")
            except Exception as e:
                print(f"⚠️ Plugin shutdown error: {e}")

        print("🛑 Plugin system shutdown complete")


class APIRouterMountingPhase:
    """Phase 1.6: Mount API routers using factory pattern"""

    @staticmethod
    async def startup(app) -> None:
        """Mount all configured API routers"""
        # Phase 1.6: Mount API Routers using factory pattern (Issue #385 - INFR-MAINT-REFACTOR)
        # This replaces 100+ lines of duplicate try/catch boilerplate
        from web.router_initializer import RouterInitializer

        RouterInitializer.mount_router(app, "web.api.routes.standup", "router", "Standup API")
        RouterInitializer.mount_router(app, "web.api.routes.learning", "router", "Learning API")
        RouterInitializer.mount_router(app, "web.api.routes.health", "router", "Health API")
        RouterInitializer.mount_router(app, "web.api.routes.api_keys", "router", "API Keys API")


class BackgroundCleanupPhase:
    """Background cleanup job for token blacklist (Issue #227 - CORE-USERS-JWT)"""

    @staticmethod
    async def startup(app) -> None:
        """Start background cleanup job for token blacklist"""
        print("\n🧹 Starting Background Cleanup Job...")
        try:
            import asyncio

            from services.scheduler.blacklist_cleanup_job import BlacklistCleanupJob

            cleanup_job = BlacklistCleanupJob(interval_hours=24)
            cleanup_task = asyncio.create_task(cleanup_job.start())

            # Store in app state for shutdown
            app.state.blacklist_cleanup_job = cleanup_job
            app.state.blacklist_cleanup_task = cleanup_task

            print("✅ Blacklist cleanup job started (runs every 24 hours)")
        except Exception as e:
            print(f"⚠️ Failed to start blacklist cleanup job: {e}")
            print("   Continuing without background cleanup\n")

    @staticmethod
    async def shutdown(app) -> None:
        """Shutdown background cleanup job"""
        print("\n🧹 Shutting down Background Cleanup Job...")
        if hasattr(app.state, "blacklist_cleanup_job") and app.state.blacklist_cleanup_job:
            try:
                await app.state.blacklist_cleanup_job.stop()
                print("✅ Blacklist cleanup job stopped")
            except Exception as e:
                print(f"⚠️ Cleanup job shutdown error: {e}")

        print("🛑 Background cleanup shutdown complete")


class AttentionDecayPhase:
    """Background job for attention decay updates (Issue #365 - SLACK-ATTENTION-DECAY)

    Implements Pattern-048: Periodic Background Job
    """

    @staticmethod
    async def startup(app) -> None:
        """Start attention decay background job"""
        print("\n⏱️ Starting Attention Decay Job...")
        try:
            import asyncio

            from services.integrations.slack.attention_model import AttentionModel
            from services.scheduler.attention_decay_job import AttentionDecayJob

            # Create attention model for decay tracking
            # Note: This creates a dedicated model instance for the decay job
            # In production, this could be shared via ServiceContainer
            attention_model = AttentionModel()

            decay_job = AttentionDecayJob(
                attention_model=attention_model,
                interval_minutes=5,  # Default, can be configured
            )
            decay_task = asyncio.create_task(decay_job.start())

            # Store in app state for shutdown
            app.state.attention_decay_job = decay_job
            app.state.attention_decay_task = decay_task

            print("✅ Attention decay job started (runs every 5 minutes)")
        except Exception as e:
            print(f"⚠️ Failed to start attention decay job: {e}")
            print("   Continuing without attention decay updates\n")

    @staticmethod
    async def shutdown(app) -> None:
        """Shutdown attention decay job"""
        print("\n⏱️ Shutting down Attention Decay Job...")
        if hasattr(app.state, "attention_decay_job") and app.state.attention_decay_job:
            try:
                await app.state.attention_decay_job.stop()
                print("✅ Attention decay job stopped")
            except Exception as e:
                print(f"⚠️ Attention decay job shutdown error: {e}")

        print("🛑 Attention decay shutdown complete")


class EthicsAuditCleanupPhase:
    """Issue #1018 Phase 2: scheduled retention sweep for ethics_audit_log table.

    Sibling pattern to BackgroundCleanupPhase + AttentionDecayPhase.
    Includes the post-#948 task-cancellation hygiene (start() captures
    asyncio.current_task(); stop() cancels-and-awaits) so shutdown is
    sub-second on Ctrl-C.
    """

    @staticmethod
    async def startup(app) -> None:
        print("\n📜 Starting Ethics Audit Cleanup Job...")
        try:
            import asyncio

            from services.scheduler.ethics_audit_cleanup_job import EthicsAuditCleanupJob

            cleanup_job = EthicsAuditCleanupJob(interval_hours=24, retention_days=90)
            cleanup_task = asyncio.create_task(cleanup_job.start())
            app.state.ethics_audit_cleanup_job = cleanup_job
            app.state.ethics_audit_cleanup_task = cleanup_task

            print("✅ Ethics audit cleanup job started (runs every 24 hours; 90-day retention)")
        except Exception as e:
            print(f"⚠️ Failed to start ethics audit cleanup job: {e}")
            print("   Continuing without scheduled retention sweep\n")

    @staticmethod
    async def shutdown(app) -> None:
        print("\n📜 Shutting down Ethics Audit Cleanup Job...")
        if hasattr(app.state, "ethics_audit_cleanup_job") and app.state.ethics_audit_cleanup_job:
            try:
                await app.state.ethics_audit_cleanup_job.stop()
                print("✅ Ethics audit cleanup job stopped")
            except Exception as e:
                print(f"⚠️ Ethics audit cleanup shutdown error: {e}")
        print("🛑 Ethics audit cleanup shutdown complete")


class OutputFilterWiringPhase:
    """Issue #1017 Phase 2.3: attach the OutputFilter to the module-level LLMClient.

    Output filtering can't construct at module-import time because
    BoundaryEnforcer pulls in config + audit_transparency dependencies
    that aren't ready at import. Doing it in a startup phase keeps the
    eager-import surface clean while still wiring before the first
    LLM call.

    On wiring failure the LLM client continues to operate WITHOUT
    filtering (graceful degradation). The failure is logged loudly so
    operators see the gap; the alternative — failing startup entirely
    — would be a worse outage shape for a defense-in-depth layer.
    """

    @staticmethod
    async def startup(app) -> None:
        print("\n🛡  Wiring OutputFilter into LLMClient...")
        try:
            from services.ethics.output_filter import build_default_output_filter
            from services.llm.clients import llm_client

            output_filter = build_default_output_filter()
            llm_client.set_output_filter(output_filter)

            app.state.output_filter = output_filter
            print("✅ OutputFilter wired (PII + secrets + boundary categories)")
        except Exception as e:
            print(f"⚠️ Failed to wire OutputFilter: {e}")
            print("   LLM outputs will pass through UNFILTERED until the next startup\n")

    @staticmethod
    async def shutdown(app) -> None:
        # No teardown needed — filter is stateless aside from the
        # BoundaryEnforcer reference, which has its own lifecycle.
        pass


class CompostingSchedulerPhase:
    """Issue #1035 Phase 5: scheduled composting cycle ("filing dreams").

    Wraps `services.mux.composting_scheduler.CompostingScheduler` in
    `services.scheduler.composting_scheduler_job.CompostingSchedulerJob` and
    runs it as a startup-managed lifecycle task. The scheduler ticks every
    hour by default; `maybe_run()` decides whether the tick actually runs a
    composting cycle (quiet-hours + min_pending + min_interval gates per
    `composting-experience-design.md`).

    Sibling pattern to `EthicsAuditCleanupPhase` (#1018 Phase 2). Includes
    post-#948 task-cancellation hygiene so shutdown is sub-second.

    Each instance constructs its own CompostBin + CompostingPipeline +
    CompostingScheduler. CompostBin is in-memory and starts empty on each
    boot — per audit Q1 (May 3) the queue is rebuilt from candidate-objects
    on demand rather than persisted across restarts. Insights themselves
    persist via the InsightJournal repository (#1035 Phase 4).
    """

    @staticmethod
    async def startup(app) -> None:
        print("\n🌱 Starting Composting Scheduler Job...")
        try:
            import asyncio

            from services.mux.compost_bin import CompostBin
            from services.mux.composting_pipeline import (
                CompostingPipeline,
                InsightJournal,
            )
            from services.mux.composting_scheduler import (
                CompostingSchedule,
                CompostingScheduler,
            )
            from services.scheduler.composting_scheduler_job import (
                CompostingSchedulerJob,
            )

            # Build the domain stack
            compost_bin = CompostBin()
            journal = InsightJournal()  # repository-backed (#1035 Phase 4)
            pipeline = CompostingPipeline(journal=journal)
            schedule = CompostingSchedule()  # quiet_hours=[2,3,4] default per spec
            scheduler = CompostingScheduler(
                compost_bin=compost_bin,
                pipeline=pipeline,
                schedule=schedule,
            )

            # Wrap in the runtime job
            job = CompostingSchedulerJob(
                scheduler=scheduler,
                interval_seconds=3600,  # tick every hour; gates decide whether to run
            )
            task = asyncio.create_task(job.start())
            app.state.composting_scheduler_job = job
            app.state.composting_scheduler_task = task
            # Expose the bin so callers (object-archival paths, etc.) can add
            # candidate objects later. Kept on app.state for now until a more
            # formal contributor surface is designed.
            app.state.compost_bin = compost_bin

            print(
                "✅ Composting scheduler started "
                "(ticks hourly; quiet-hours composting per spec)"
            )
        except Exception as e:
            print(f"⚠️ Failed to start composting scheduler: {e}")
            print("   Continuing without scheduled composting\n")

    @staticmethod
    async def shutdown(app) -> None:
        print("\n🌱 Shutting down Composting Scheduler Job...")
        if (
            hasattr(app.state, "composting_scheduler_job")
            and app.state.composting_scheduler_job
        ):
            try:
                await app.state.composting_scheduler_job.stop()
                print("✅ Composting scheduler stopped")
            except Exception as e:
                print(f"⚠️ Composting scheduler shutdown error: {e}")
        print("🛑 Composting scheduler shutdown complete")


class StartupManager:
    """Orchestrates all startup phases in sequence"""

    def __init__(self, app):
        """Initialize startup manager"""
        self.app = app
        self.phases = [
            ServiceContainerPhase,
            ConfigValidationPhase,
            SchemaValidationPhase,  # Issue #484: Validate models match DB schema
            ServiceRetrievalPhase,
            WebComponentsInitializationPhase,
            PluginInitializationPhase,
            APIRouterMountingPhase,
            BackgroundCleanupPhase,
            AttentionDecayPhase,  # Issue #365: SLACK-ATTENTION-DECAY
            EthicsAuditCleanupPhase,  # Issue #1018 Phase 2: ethics_audit_log retention sweep
            OutputFilterWiringPhase,  # Issue #1017 Phase 2.3: attach OutputFilter to LLMClient
            CompostingSchedulerPhase,  # Issue #1035 Phase 5: insight composting cycle
        ]

    async def startup(self) -> None:
        """Execute all startup phases"""
        for phase_class in self.phases:
            await phase_class.startup(self.app)

        print("🚀 Web server startup complete")

    async def shutdown(self) -> None:
        """Execute all shutdown phases in reverse order"""
        # Shutdown in reverse order of startup
        for phase_class in reversed(self.phases):
            if hasattr(phase_class, "shutdown"):
                await phase_class.shutdown(self.app)

        print("🛑 Web server shutdown complete")

    @asynccontextmanager
    async def lifespan_context(self):
        """Context manager for FastAPI lifespan"""
        await self.startup()
        yield
        await self.shutdown()


@asynccontextmanager
async def lifespan(app):
    """
    FastAPI lifespan context manager for startup/shutdown events
    Delegates to StartupManager for orchestration of startup phases
    """
    manager = StartupManager(app)
    async with manager.lifespan_context():
        yield
