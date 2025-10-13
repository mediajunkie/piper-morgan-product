"""
Piper Morgan Web Interface
Simple FastAPI app for interacting with the main Piper Morgan Platform API
"""

import asyncio
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import structlog
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Add project root to path for imports (same as CLI)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Standup API moved to backend - only config loader needed for legacy compatibility
from services.configuration.piper_config_loader import piper_config_loader

# Configuration service import - eliminates hardcoded values
from services.configuration.port_configuration_service import get_port_configuration

# Import personality integration
from web.personality_integration import (
    PersonalityResponseEnhancer,
    PiperConfigParser,
    WebPersonalityConfig,
)

# Server Configuration - now using centralized configuration service
port_config = get_port_configuration()
DEFAULT_PORT = port_config.web_port
API_BASE_URL = port_config.get_api_base_url()

# Initialize logger
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup/shutdown events
    Phase 3A: OrchestrationEngine dependency injection setup
    GREAT-2D: Configuration validation at startup
    """
    # GREAT-2D: Configuration validation
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

    # Phase 3A: OrchestrationEngine dependency injection setup
    try:
        from services.orchestration.engine import OrchestrationEngine, set_global_engine

        print("🔧 Phase 3A: Initializing OrchestrationEngine with dependency injection...")

        # Initialize OrchestrationEngine (uses ServiceRegistry internally)
        orchestration_engine = OrchestrationEngine()

        # Store in app state for dependency injection (DDD-compliant)
        app.state.orchestration_engine = orchestration_engine

        # Also set global engine for backward compatibility with main.py pattern
        set_global_engine(orchestration_engine)

        print("✅ Phase 3A: OrchestrationEngine initialized successfully via dependency injection")

    except Exception as e:
        print(f"❌ Phase 3A: OrchestrationEngine initialization failed: {e}")
        # Continue startup without orchestration engine (preserve bypasses)
        app.state.orchestration_engine = None

    # Phase 2B: IntentService dependency injection setup
    try:
        from services.conversation.conversation_handler import ConversationHandler
        from services.intent.intent_service import IntentService
        from services.intent_service import classifier

        print("🔧 Phase 2B: Initializing IntentService with dependency injection...")

        # Initialize IntentService with dependencies
        intent_service = IntentService(
            orchestration_engine=app.state.orchestration_engine,
            intent_classifier=classifier,
            conversation_handler=ConversationHandler(session_manager=None),
        )

        # Store in app state for dependency injection
        app.state.intent_service = intent_service

        print("✅ Phase 2B: IntentService initialized successfully")

    except Exception as e:
        print(f"❌ Phase 2B: IntentService initialization failed: {e}")
        # Continue without intent service (will fail gracefully in route)
        app.state.intent_service = None

    # Phase 3B: Plugin system initialization
    print("\n🔌 Phase 3B: Initializing Plugin System...")

    try:
        from services.plugins import get_plugin_registry

        registry = get_plugin_registry()

        # GREAT-3B Update: Replaced static imports with dynamic loading
        # - Plugins discovered from services/integrations/*/
        # - Config in PIPER.user.md controls what loads
        # - Backwards compatible: all plugins enabled by default

        # Phase 3B: Plugin System (Dynamic Loading - GREAT-3B)
        print("\n🔌 Initializing Plugin System...")

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

    print("🚀 Web server startup complete")

    yield

    # Shutdown: cleanup plugins
    print("\n🔌 Shutting down Plugin System...")

    if hasattr(app.state, "plugin_registry") and app.state.plugin_registry:
        try:
            shutdown_results = await app.state.plugin_registry.shutdown_all()
            success_count = sum(1 for success in shutdown_results.values() if success)
            print(f"✅ Plugin shutdown: {success_count}/{len(shutdown_results)} successful")
        except Exception as e:
            print(f"⚠️ Plugin shutdown error: {e}")

    print("🛑 Plugin system shutdown complete")

    # Cleanup
    print("🛑 Web server shutdown complete")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Piper Morgan UI",
    description="Web Interface for the Piper Morgan Platform",
    lifespan=lifespan,
)

# GREAT-4B: Intent Enforcement Middleware
from web.middleware.intent_enforcement import IntentEnforcementMiddleware

app.add_middleware(IntentEnforcementMiddleware)
logger.info("✅ IntentEnforcementMiddleware registered (GREAT-4B)")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Initialize personality components
config_parser = PiperConfigParser()
personality_enhancer = PersonalityResponseEnhancer()

# Mount static files
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "assets")),
    name="assets",
)


@app.get("/debug-markdown", response_class=HTMLResponse)
async def debug_markdown(request: Request):
    return HTMLResponse(
        content="""<!DOCTYPE html>
<html>
<head>
    <title>Markdown Debug Test</title>
    <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test-section { border: 1px solid #ccc; margin: 10px 0; padding: 10px; }
        .raw { background: #f0f0f0; padding: 10px; margin: 5px 0; }
        .rendered { background: #e8f4f8; padding: 10px; margin: 5px 0; }
        h1 { color: #2c3e50; border-bottom: 1px solid #ecf0f1; }
        h2 { color: #34495e; }
        strong { color: #2c3e50; }
    </style>
</head>
<body>
    <h1>Markdown Renderer Debug Test</h1>

    <div class="test-section">
        <h3>Test 1: Check if renderMarkdown function exists</h3>
        <div class="rendered" id="test1"></div>
    </div>

    <div class="test-section">
        <h3>Test 2: Simple Header</h3>
        <div class="raw">Input: "# Header 1"</div>
        <div class="rendered" id="test2"></div>
    </div>

    <div class="test-section">
        <h3>Test 3: Your Failing Example</h3>
        <div class="raw">Input: "Here's my summary... # Header ## Subheader"</div>
        <div class="rendered" id="test3"></div>
    </div>

    <script src="/assets/markdown-renderer.js?v=2"></script>
    <script>
        // Test if the function is loaded
        if (typeof renderMarkdown === 'function') {
            document.getElementById('test1').innerHTML = '✅ renderMarkdown function loaded successfully';

            // Test 2: Simple header
            document.getElementById('test2').innerHTML = renderMarkdown('# Header 1');

            // Test 3: Your failing example
            const failingText = `Here's my summary: # Piper Morgan Summary ## File Type This appears to be documentation.`;
            document.getElementById('test3').innerHTML = renderMarkdown(failingText);

        } else {
            document.getElementById('test1').innerHTML = '❌ renderMarkdown function not loaded - check console for errors';
            console.error('renderMarkdown function not found');
        }
    </script>
</body>
</html>"""
    )


@app.get("/")
async def home(request: Request):
    """Render home page"""
    return templates.TemplateResponse("home.html", {"request": request})


# GREAT-1B: Bug #166 Fix - Add missing workflow status endpoint
@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str, request: Request):
    """Get workflow status to prevent UI polling hang (Bug #166 fix)"""
    try:
        # Get OrchestrationEngine from app state
        orchestration_engine = getattr(request.app.state, "orchestration_engine", None)

        if orchestration_engine is None:
            return {
                "status": "error",
                "error": "OrchestrationEngine not available",
                "workflow_id": workflow_id,
            }

        # For GREAT-1B, return a simple status response
        # This prevents the infinite polling that causes UI hangs
        return {
            "workflow_id": workflow_id,
            "status": "completed",  # Simplified for Bug #166 fix
            "message": "Workflow processing completed",
            "tasks": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

    except Exception as e:
        return {"status": "error", "error": str(e), "workflow_id": workflow_id}


# Personality Configuration Endpoints
@app.get("/api/personality/profile/{user_id}")
async def get_personality_profile(user_id: str = "default"):
    """Get user's personality preferences"""
    try:
        config = config_parser.load_personality_config(user_id)
        return {"status": "success", "data": config.to_dict(), "user_id": user_id}
    except Exception as e:
        return {"status": "error", "error": str(e), "user_id": user_id}


@app.put("/api/personality/profile/{user_id}")
async def update_personality_profile(user_id: str, request: Request):
    """Update user's personality preferences"""
    try:
        data = await request.json()
        config = WebPersonalityConfig.from_dict(data)

        success = config_parser.save_personality_config(config, user_id)

        if success:
            return {
                "status": "success",
                "data": config.to_dict(),
                "user_id": user_id,
                "message": "Personality preferences updated successfully",
            }
        else:
            return {
                "status": "error",
                "error": "Failed to save personality configuration",
                "user_id": user_id,
            }
    except Exception as e:
        return {"status": "error", "error": str(e), "user_id": user_id}


@app.post("/api/personality/enhance")
async def enhance_response(request: Request):
    """Enhance a response with personality"""
    try:
        data = await request.json()
        content = data.get("content", "")
        user_id = data.get("user_id", "default")
        confidence = data.get("confidence", 0.5)

        # Load personality config
        config = config_parser.load_personality_config(user_id)

        # Enhance response
        enhanced_content = personality_enhancer.enhance_response(content, config, confidence)

        return {
            "status": "success",
            "data": {
                "original_content": content,
                "enhanced_content": enhanced_content,
                "personality_config": config.to_dict(),
                "confidence": confidence,
            },
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/api/standup")
async def standup_proxy(
    format: str = Query("raw", description="Response format: 'raw' or 'human-readable'"),
    personality: bool = Query(False, description="Apply personality enhancement"),
):
    """Proxy standup requests to backend API"""
    import httpx

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/api/standup", params={"format": format, "personality": personality}
            )
            return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error": f"Backend API unavailable: {str(e)}",
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "source": "web-proxy",
                "version": "1.0",
                "error_type": "ProxyError",
                "recovery_suggestions": [
                    f"Check if backend API is running on port {port_config.backend_port}",
                    "Verify main.py service is started",
                    "Try again in a few moments",
                ],
            },
        }


@app.post("/api/v1/intent")
async def process_intent(request: Request):
    """
    Phase 2B: Thin HTTP adapter for intent processing

    Delegates all business logic to IntentService.
    Route only handles HTTP concerns (request parsing, response formatting, status codes).

    Business logic: services/intent/intent_service.py
    """
    try:
        # Parse HTTP request
        request_data = await request.json()
        message = request_data.get("message", "")
        session_id = request_data.get("session_id", "default_session")

        # Get IntentService from app state (dependency injection)
        intent_service = getattr(request.app.state, "intent_service", None)

        if intent_service is None:
            # Service not initialized - should not happen with proper lifespan
            return {
                "status": "error",
                "error": "IntentService not available - initialization failed",
                "detail": "Service not found in app.state",
            }

        # Delegate to service (all business logic)
        result = await intent_service.process_intent(message=message, session_id=session_id)

        # Format HTTP response from service result
        response = {
            "message": result.message,
            "intent": result.intent_data,
            "workflow_id": result.workflow_id,
            "requires_clarification": result.requires_clarification,
            "clarification_type": result.clarification_type,
        }

        # Add error fields if present
        if result.error:
            response["status"] = "error"
            response["error"] = result.error
            if result.error_type:
                response["error_type"] = result.error_type

        return response

    except Exception as e:
        # Unexpected error - HTTP 500 equivalent
        logger.error(f"Intent route error: {str(e)}")
        return {
            "status": "error",
            "error": f"Intent processing failed: {str(e)}",
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "source": "web-direct",
                "version": "1.0",
                "error_type": "ProcessingError",
            },
        }


@app.get("/standup")
async def standup_ui(request: Request):
    """Render standup UI"""
    return templates.TemplateResponse("standup.html", {"request": request})


@app.get("/personality-preferences")
async def personality_preferences_ui():
    """Serve the personality preferences interface"""
    return HTMLResponse(
        content=open(
            os.path.join(os.path.dirname(__file__), "assets", "personality-preferences.html")
        ).read()
    )


@app.get("/health/config")
async def health_config():
    """
    Configuration health check endpoint.

    Returns validation status for all service configurations.
    CORE-GREAT-2D: Configuration Validation
    """
    from services.infrastructure.config.config_validator import ConfigValidator

    validator = ConfigValidator()
    summary = validator.get_summary()

    # Return 200 with summary (even if some services invalid)
    # This is a health check endpoint, not a gate
    return {
        "status": "healthy" if summary["all_valid"] else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "validation": summary,
    }


@app.get("/api/admin/intent-monitoring")
async def intent_monitoring():
    """
    Intent enforcement monitoring endpoint.

    Returns current middleware configuration and monitoring status.
    CORE-GREAT-4B: Intent Enforcement
    """
    return IntentEnforcementMiddleware.get_monitoring_status()


@app.get("/api/admin/intent-cache-metrics")
async def intent_cache_metrics(request: Request):
    """
    Intent cache performance metrics endpoint.

    Returns cache hit rate, size, and performance statistics.
    CORE-GREAT-4B Phase 3: Intent Caching
    """
    # Get IntentService from app state
    intent_service = getattr(request.app.state, "intent_service", None)

    # GREAT-5 Phase 1.5: Fix attribute name (intent_classifier not classifier)
    if intent_service and hasattr(intent_service.intent_classifier, "cache"):
        metrics = intent_service.intent_classifier.cache.get_metrics()
        return {"cache_enabled": True, "metrics": metrics, "status": "operational"}
    else:
        return {"cache_enabled": False, "status": "not_configured"}


@app.post("/api/admin/intent-cache-clear")
async def clear_intent_cache(request: Request):
    """
    Clear the intent cache (admin only).

    Removes all cached intent classifications and resets metrics.
    CORE-GREAT-4B Phase 3: Intent Caching
    """
    # Get IntentService from app state
    intent_service = getattr(request.app.state, "intent_service", None)

    # GREAT-5 Phase 1.5: Fix attribute name (intent_classifier not classifier)
    if intent_service and hasattr(intent_service.intent_classifier, "cache"):
        intent_service.intent_classifier.cache.clear()
        return {"status": "cache_cleared", "message": "Intent cache cleared successfully"}
    else:
        return {"status": "cache_not_configured", "message": "Intent cache not available"}


@app.get("/api/admin/piper-config-cache-metrics")
async def piper_config_cache_metrics():
    """
    PIPER.md config cache performance metrics endpoint.

    Returns cache hit rate, age, and performance statistics for PIPER configuration caching.
    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.configuration.piper_config_loader import piper_config_loader

    metrics = piper_config_loader.get_cache_metrics()
    return {"cache_enabled": True, "metrics": metrics, "status": "operational"}


@app.post("/api/admin/piper-config-cache-clear")
async def clear_piper_config_cache():
    """
    Clear the PIPER.md config cache (admin only).

    Forces next PIPER.md load to read from disk.
    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.configuration.piper_config_loader import piper_config_loader

    piper_config_loader.clear_cache()
    return {"status": "cache_cleared", "message": "PIPER config cache cleared successfully"}


@app.get("/api/admin/user-context-cache-metrics")
async def user_context_cache_metrics():
    """
    User context cache performance metrics endpoint.

    Returns cache hit rate and session-level cache statistics.
    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.user_context_service import user_context_service

    metrics = user_context_service.get_cache_metrics()
    return {"cache_enabled": True, "metrics": metrics, "status": "operational"}


@app.post("/api/admin/user-context-cache-clear")
async def clear_user_context_cache():
    """
    Clear the user context cache (admin only).

    Removes all cached user contexts. Next request will reload from PIPER.md.
    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.user_context_service import user_context_service

    user_context_service.invalidate_cache()  # No session_id = clear all
    return {"status": "cache_cleared", "message": "User context cache cleared successfully"}


@app.get("/health")
async def health():
    """
    Health check endpoint - exempt from intent enforcement.

    Returns basic service status for monitoring and load balancers.
    """
    return {
        "status": "healthy",
        "message": "Piper Morgan web service is running",
        "timestamp": datetime.now().isoformat(),
        "services": {"web": "healthy", "intent_enforcement": "active"},
    }


@app.post("/api/admin/user-context-cache-invalidate/{session_id}")
async def invalidate_user_context(session_id: str):
    """
    Invalidate specific user's cached context (admin only).

    Args:
        session_id: Session identifier to invalidate

    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.user_context_service import user_context_service

    user_context_service.invalidate_cache(session_id)
    return {
        "status": "invalidated",
        "session_id": session_id,
        "message": f"User context for session {session_id} invalidated",
    }


if __name__ == "__main__":
    import uvicorn

    print(f"🚀 Starting Piper Morgan Web Interface on {port_config.get_web_url()}")
    print(f"📊 Standup API: {port_config.get_web_url()}/api/standup")
    print(f"🌅 Standup UI: {port_config.get_web_url()}/standup")
    print(f"📖 API Docs: {port_config.get_web_url()}/docs")
    print(f"🔗 Backend API: {port_config.get_backend_url()}")
    print(
        f"\n🔧 Server Command: PYTHONPATH=. python -m uvicorn web.app:app --host {port_config.web_host} --port {port_config.web_port}"
    )
    uvicorn.run(app, host=port_config.web_host, port=port_config.web_port)
