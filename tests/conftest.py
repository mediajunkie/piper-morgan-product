"""
conftest.py — Minimal test infrastructure for Piper Morgan
"""

import asyncio
import os
import sys
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# ============================================================================
# UUID Test Fixtures (Issue #262 - UUID Migration)
# ============================================================================
# Reusable UUIDs for tests - use these instead of hardcoded strings
TEST_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
TEST_USER_ID_2 = UUID("22222222-2222-2222-2222-222222222222")
TEST_SESSION_ID = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
TEST_WORKFLOW_ID = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")

# For xian's actual UUID from migration
XIAN_USER_ID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")


# ============================================================================
# Load API keys from macOS Keychain for LLM tests (#742)
# ============================================================================
def pytest_configure(config):
    """
    Load API keys from macOS Keychain before test collection.

    This allows LLM and GitHub integration tests to run when keys are stored
    securely in keychain rather than requiring them to be exported to shell
    environment.

    Keys are loaded from the "piper-morgan" keychain service.

    Issue #914: Added GitHub token loading from keychain.
    """
    try:
        # Import here to avoid dependency issues if keyring not installed
        from services.infrastructure.keychain_service import get_keychain_service

        keychain = get_keychain_service()

        # Try to load OpenAI key (skip if already in environment)
        if not os.environ.get("OPENAI_API_KEY"):
            openai_key = keychain.get_api_key("openai")
            if openai_key:
                os.environ["OPENAI_API_KEY"] = openai_key
                print("  [conftest] Loaded OPENAI_API_KEY from keychain")

        # Try to load Anthropic key (skip if already in environment)
        if not os.environ.get("ANTHROPIC_API_KEY"):
            anthropic_key = keychain.get_api_key("anthropic")
            if anthropic_key:
                os.environ["ANTHROPIC_API_KEY"] = anthropic_key
                print("  [conftest] Loaded ANTHROPIC_API_KEY from keychain")

        # Try to load GitHub token (Issue #914)
        # The keychain stores it as "github_token" (via save_github_token route).
        # The codebase reads it from GITHUB_TOKEN env var (get_github_token()).
        if not os.environ.get("GITHUB_TOKEN"):
            github_key = keychain.get_api_key("github_token")
            if github_key:
                os.environ["GITHUB_TOKEN"] = github_key
                print("  [conftest] Loaded GITHUB_TOKEN from keychain")

    except ImportError:
        # keyring or keychain_service not available - skip silently
        pass
    except Exception as e:
        # Log but don't fail - tests will just skip when keys unavailable
        print(f"  [conftest] Warning: Could not load API keys from keychain: {e}")

    # Fallback: try `gh auth token` if GITHUB_TOKEN still not set (Issue #914)
    # The gh CLI stores its own auth token — reuse it for integration tests.
    if not os.environ.get("GITHUB_TOKEN"):
        try:
            import subprocess

            result = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                os.environ["GITHUB_TOKEN"] = result.stdout.strip()
                print("  [conftest] Loaded GITHUB_TOKEN from gh CLI")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass  # gh not installed or timed out - skip silently


# ============================================================================
# Auto-skip tests when required credentials not available
# ============================================================================
def pytest_collection_modifyitems(config, items):
    """
    Auto-skip tests marked with @pytest.mark.llm or @pytest.mark.github
    when the required API keys are not available.

    This prevents test failures in CI/local environments without credentials.
    Tests will show as 'skipped' rather than 'failed'.

    Issue #914: Added GitHub token auto-skip support.
    """
    # Check for LLM API keys
    has_openai = bool(os.environ.get("OPENAI_API_KEY"))
    has_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_llm_keys = has_openai or has_anthropic

    # Check for GitHub token
    has_github = bool(os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"))

    for item in items:
        # Skip LLM tests if no LLM keys
        if not has_llm_keys and "llm" in item.keywords:
            item.add_marker(
                pytest.mark.skip(
                    reason="LLM API keys not available (OPENAI_API_KEY or ANTHROPIC_API_KEY)"
                )
            )

        # Skip GitHub tests if no GitHub token (Issue #914)
        if not has_github and "github" in item.keywords:
            item.add_marker(
                pytest.mark.skip(
                    reason="GitHub token not available (GITHUB_TOKEN or GH_TOKEN). "
                    "Store via: keychain.store_api_key('github_token', 'ghp_...')"
                )
            )


# Session-scoped event loop for async integration tests (Issue #290)
# This ensures all tests in a session share the same event loop, preventing
# "Task attached to different loop" errors when database connections are reused
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the entire test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# Basic fixtures that don't depend on services that may not exist
@pytest.fixture
def mock_session():
    """Provide a mock session for tests that need it"""
    return Mock()


@pytest.fixture(autouse=True)
def mock_token_blacklist(request):
    """
    Auto-mock TokenBlacklist for unit tests to prevent database session conflicts.

    Investigation (2025-11-20 SLACK-SPATIAL Phase 1.2):
    Confirmed this auto-mock serves its purpose without hiding bugs. All auth tests
    use @pytest.mark.integration and bypass this mock. See investigation report:
    dev/2025/11/20/token-blacklist-investigation-results.md

    WHY THIS EXISTS:
    Issue #281: TokenBlacklist.is_blacklisted() gets async context manager from
    overridden db.get_session() in tests, causing '_AsyncGeneratorContextManager'
    has no attribute 'execute' errors in unit tests that don't properly configure
    database session mocks.

    WHAT IT DOES:
    - Automatically mocks is_blacklisted() to return False for unit tests
    - Allows unit tests to run without complex database session setup
    - Does NOT affect integration tests (they bypass this mock)

    WHEN IT APPLIES:
    - Unit tests (no @pytest.mark.integration marker)
    - Tests that indirectly call TokenBlacklist through JWT validation

    WHEN IT DOESN'T APPLY:
    - Integration tests (marked with @pytest.mark.integration)
    - Tests in tests/unit/services/auth/ (all use integration marker)

    TO DISABLE FOR INVESTIGATION:
    Change autouse=True to autouse=False and run your tests. Remember to re-enable
    after investigation to maintain unit test stability.

    Related Issues: #281 (original issue), #292 (integration test behavior)
    Investigation: piper-morgan-otf (SLACK-SPATIAL Phase 1.2)
    """
    from unittest.mock import AsyncMock, patch

    # Skip mock for integration and performance tests - they use real database/Redis
    if "integration" in request.keywords or "performance" in request.keywords:
        yield
        return

    # Import the module first to ensure it exists before patching
    # This avoids "module has no attribute" errors during patch()
    try:
        from services.auth import token_blacklist  # noqa: F401
    except ImportError:
        # If module doesn't exist, skip the mock
        yield
        return

    # Patch the service class at its module definition location
    with patch(
        "services.auth.token_blacklist.TokenBlacklist.is_blacklisted",
        new=AsyncMock(return_value=False),
    ):
        yield


@pytest.fixture
def mock_async_session():
    """Provide a mock async session for tests that need it"""
    return AsyncMock()


class _PermissiveFakeRedis:
    """A fake Redis client that always lets requests through cleanly.

    Supports exactly the commands UsageCapMiddleware (ADR-076) uses. Reads
    always report "nothing counted yet" so no test unexpectedly hits the
    rate limit or concurrency cap; writes are no-ops. This is deliberately
    permissive, not a behavioral simulation — tests that need to exercise
    the middleware's actual rate-limit/concurrency-cap/fail-closed logic
    use their own precise fake (see test_usage_cap_middleware_1370.py),
    which patches the same target and takes precedence during those tests.
    """

    async def incr(self, key):
        return 1

    async def expire(self, key, seconds):
        return True

    async def ttl(self, key):
        return -1

    async def zadd(self, key, mapping):
        return len(mapping)

    async def zscore(self, key, member):
        return None

    async def zcard(self, key):
        return 0

    async def zremrangebyscore(self, key, min_score, max_score):
        return 0

    async def close(self):
        pass


@pytest.fixture(autouse=True)
def mock_usage_cap_redis(request):
    """
    Auto-mock Redis for UsageCapMiddleware (ADR-076) so unit/route tests that
    exercise the real FastAPI app (`from web.app import app` + `TestClient`)
    don't fail with 503s when no local Redis is running.

    Investigation (2026-07-06, ADR-076 build): confirmed no Redis service is
    provisioned in this repo's gating CI (`ci.yml` runs bare `pytest tests/`
    with no `services:` block — only pm034-llm/e2e-aaxt workflows provision
    Redis) and none is running in a plain local dev shell without
    `docker compose up -d`. UsageCapMiddleware fails closed (ADR-076 D4) when
    Redis is unavailable, meaning EVERY request through the real app — not
    just usage-cap-specific tests — would get a 503 instead of its expected
    response. Confirmed by running tests/auth/test_auth_endpoints.py before
    this fixture existed: test_login_success failed with
    {"error":"capacity_check_unavailable",...} instead of 200.

    Same shape as mock_token_blacklist above: skip for integration/performance
    tests (they should exercise real infra deliberately), patch for everything
    else. The patch target (`RedisFactory.redis_scope`, a classmethod) is the
    same object regardless of which module's import path names it, so this
    also covers other code that happens to call it during the same test —
    intentional, not a side effect to guard against.

    TO DISABLE FOR INVESTIGATION: add your test's ID to a `-k not` filter, or
    temporarily change autouse=True to autouse=False.
    """
    if "integration" in request.keywords or "performance" in request.keywords:
        yield
        return

    from contextlib import asynccontextmanager

    # Import the module first to ensure it exists before patching (same
    # discipline as mock_token_blacklist above) — mock.patch's dotted-string
    # target resolution needs `services.cache` to already be an attribute of
    # `services`, which isn't guaranteed for every test file's import chain
    # (found via tests/integration/test_route_prefixes_1075.py: "AttributeError:
    # module 'services' has no attribute 'cache'" when nothing else in that
    # file's imports had pulled in services.cache.redis_factory first).
    try:
        from services.cache import redis_factory  # noqa: F401
    except ImportError:
        yield
        return

    fake = _PermissiveFakeRedis()

    @asynccontextmanager
    async def _scope():
        yield fake

    with patch(
        "services.cache.redis_factory.RedisFactory.redis_scope",
        side_effect=_scope,
    ):
        yield


# GREAT-5 Phase 1.5: IntentService test fixtures
# Updated in #212 Phase 0 to add ServiceRegistry initialization (required after #217 refactoring)
@pytest.fixture
async def intent_service():
    """
    Provide properly initialized IntentService for testing.

    This fixture ensures IntentService is available with all required dependencies:
    - ServiceRegistry with LLM service (#217 refactoring requirement)
    - Intent classifier
    - Conversation handler

    Created in GREAT-5 Phase 1.5 to fix initialization issues revealed by
    stricter test assertions in Phase 1.
    Updated in #212 Phase 0 for #217 ServiceRegistry pattern.
    """
    import sys

    from services.container import ServiceContainer
    from services.container.service_registry import ServiceRegistry
    from services.conversation.conversation_handler import ConversationHandler
    from services.domain.llm_domain_service import LLMDomainService
    from services.intent.intent_service import IntentService
    from services.intent_service import classifier

    print("[FIXTURE DEBUG] Starting fixture setup", file=sys.stderr)

    # Initialize ServiceRegistry with LLM domain service (Phase 1.6: Updated to use container pattern)
    llm_domain_service = LLMDomainService()
    await llm_domain_service.initialize()  # Must initialize before use

    # Get container instance and access internal registry for test setup
    container = ServiceContainer()
    print(
        f"[FIXTURE DEBUG] Before register. Registry: {list(container._registry._services.keys())}",
        file=sys.stderr,
    )
    container._registry.register("llm", llm_domain_service)
    container._initialized = True  # Mark as initialized for tests
    print(
        f"[FIXTURE DEBUG] After register. Registry: {list(container._registry._services.keys())}",
        file=sys.stderr,
    )

    # Initialize IntentService with test configuration
    service = IntentService(
        intent_classifier=classifier,
        conversation_handler=ConversationHandler(session_manager=None),
    )

    yield service

    # Cleanup: Reset classifier's cached LLM and ServiceContainer (Phase 1.6)
    # The classifier singleton caches the LLM reference, which becomes stale
    # when we clear the container. Must reset it for next test.
    classifier._llm = None
    ServiceContainer.reset()


@pytest_asyncio.fixture
async def initialized_container():
    """
    Initialize ServiceContainer with LLM service for tests that need container setup.

    This fixture provides a minimal container initialization for tests that directly
    instantiate IntentClassifier or LLMIntentClassifier without going through IntentService.

    Created to fix piper-morgan-8oz and piper-morgan-ss0 (container initialization bugs).

    Usage:
        @pytest.mark.asyncio
        async def test_classifier(initialized_container):
            classifier = IntentClassifier()  # Now works - container is initialized
            intent = await classifier.classify("message")
    """
    from services.container import ServiceContainer
    from services.domain.llm_domain_service import LLMDomainService

    # Initialize LLM domain service
    llm_domain_service = LLMDomainService()
    await llm_domain_service.initialize()

    # Get container instance and register LLM service
    container = ServiceContainer()
    container._registry.register("llm", llm_domain_service)
    container._initialized = True

    yield container

    # Cleanup: Reset container for next test
    ServiceContainer.reset()


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
            intent_classifier=classifier,
            conversation_handler=ConversationHandler(session_manager=None),
        )

    client = TestClient(app)
    return client


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    """
    Create fresh async database engine per test.

    Using function scope ensures each test gets a new engine in a fresh event loop,
    avoiding "Future attached to different loop" errors when tests run together.

    Issue #281: Fix async test isolation
    """
    from services.database.connection import db

    # Initialize global db connection if not already done
    if not db._initialized:
        await db.initialize()

    # Build database URL (same as db.initialize() does)
    db_url = db._build_database_url()

    # Create fresh engine for this test
    engine = create_async_engine(
        db_url,
        echo=False,  # Reduce log noise in tests
        pool_pre_ping=True,  # Verify connections are alive
        pool_recycle=3600,
    )

    yield engine

    # Proper cleanup: dispose engine and its connection pool
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    """
    Create fresh async database session per test.

    Each test gets a new session from a new engine, ensuring proper event loop isolation.
    The session is automatically cleaned up by the context manager.

    Issue #281: Fix async test isolation
    """
    # Create fresh sessionmaker for this test
    async_session_factory = async_sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False,  # Allow access to objects after commit
    )

    # Create session and yield it
    async with async_session_factory() as session:
        yield session
        # Session cleanup happens automatically via context manager


# ============================================================================
# State Transition Testing Fixtures (Issue #485)
# ============================================================================
# These fixtures support testing state transitions like fresh-install flows,
# catching temporal/ordering bugs that steady-state tests miss.


@pytest_asyncio.fixture(scope="function")
async def fresh_database(db_session):
    """
    Provides a database with schema but NO user data.
    Use for testing fresh-install flows where no users exist yet.

    Unlike other fixtures, this does NOT create test users.
    This catches temporal bugs where operations assume users exist.

    Issue #485: Created to test setup wizard FK violation bug
    """
    from sqlalchemy import text

    # Clear all user-related data to simulate fresh install
    # Order matters due to FK constraints - clear child tables first.
    # #1452: the original 4-table list predated half the schema (the bare
    # users delete FK-failed on personalization_contexts in CI). Full child
    # set, information_schema-derived — same order as delete_test_user_fully.
    for _tbl_stmt in (
        "DELETE FROM conversation_turns",
        "DELETE FROM conversations",
        "DELETE FROM session_activity",
        "DELETE FROM token_blacklist",
        "DELETE FROM password_reset_tokens",
        "DELETE FROM user_api_keys",
        "DELETE FROM audit_logs",
        "DELETE FROM learned_patterns",
        "DELETE FROM learning_settings",
        "DELETE FROM user_trust_profiles",
        "DELETE FROM personality_profiles",
        "DELETE FROM personalization_contexts",
        "DELETE FROM feedback",
        "DELETE FROM invite_tokens",
        "DELETE FROM uploaded_files",
        "DELETE FROM documents",
        "DELETE FROM knowledge_edges",
        "DELETE FROM knowledge_nodes",
        "DELETE FROM list_items",
        "DELETE FROM list_memberships",
        "WITH del AS (DELETE FROM todo_items RETURNING id) DELETE FROM items WHERE id IN (SELECT id FROM del)",
        "DELETE FROM lists",
        "DELETE FROM project_integrations",
        "DELETE FROM repositories",
        "DELETE FROM projects",
        "DELETE FROM connector_bindings",
        "DELETE FROM connector_configs",
        "DELETE FROM users",
    ):
        try:
            await db_session.execute(text(_tbl_stmt))
        except Exception:
            pass
    await db_session.commit()

    yield db_session


class TransitionState:
    """
    Helper for testing state transitions.
    Tracks before/after state for assertions about database changes.

    Usage:
        async def test_something(fresh_database, transition_state):
            await transition_state.capture_before(fresh_database)
            # ... do some operations ...
            await transition_state.capture_after(fresh_database)
            transition_state.assert_no_new_records('user_api_keys')

    Issue #485: Created for state transition testing
    """

    def __init__(self):
        self.before_counts = {}
        self.after_counts = {}

    async def capture_before(self, session):
        """Capture table row counts before the operation under test."""
        self.before_counts = await self._get_counts(session)

    async def capture_after(self, session):
        """Capture table row counts after the operation under test."""
        self.after_counts = await self._get_counts(session)

    async def _get_counts(self, session):
        """Get row counts for key tables."""
        from sqlalchemy import text

        counts = {}
        tables = ["users", "user_api_keys", "audit_logs", "learned_patterns"]
        for table in tables:
            result = await session.execute(text(f"SELECT COUNT(*) FROM {table}"))
            counts[table] = result.scalar()
        return counts

    def assert_no_new_records(self, *tables):
        """Assert that no new records were created in the specified tables."""
        for table in tables:
            before = self.before_counts.get(table, 0)
            after = self.after_counts.get(table, 0)
            assert before == after, (
                f"Unexpected records created in {table}: " f"before={before}, after={after}"
            )

    def assert_new_records(self, table, count=1):
        """Assert that exactly N new records were created in the table."""
        before = self.before_counts.get(table, 0)
        after = self.after_counts.get(table, 0)
        actual_new = after - before
        assert actual_new == count, (
            f"Expected {count} new record(s) in {table}, "
            f"got {actual_new} (before={before}, after={after})"
        )


@pytest.fixture
def transition_state():
    """
    Provide a TransitionState helper for tests.

    Issue #485: Created for state transition testing
    """
    return TransitionState()


# ---------------------------------------------------------------------------
# #1452 root cure for the poisoned-pool pathology: the app's global
# AsyncSessionFactory keeps a shared engine whose pool accumulates loop-bound
# connections across a full sweep; any later fixture/route/service borrowing
# from it hits `asyncpg: another operation is in progress` (or cross-loop
# futures). Three per-file cures showed the pattern (fresh-engine fixtures,
# NullPool scope patches); this is the systemic version: every test sees a
# session_scope backed by a NullPool engine — no pooled connections exist, so
# nothing can carry a stale loop binding. Semantics mirror the real
# session_scope contract EXACTLY (#1193: commit on clean exit, rollback on
# exception, close always). session_scope_fresh is untouched (already
# per-loop-fresh). Tests that monkeypatch session_scope themselves layer on
# top harmlessly. LIVE code is unaffected — this is test-scope only.
# ---------------------------------------------------------------------------
from contextlib import asynccontextmanager as _1452_acm

from sqlalchemy.pool import NullPool as _1452_NullPool


def _1452_db_url() -> str:
    user = os.getenv("POSTGRES_USER", "piper")
    pw = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "piper_morgan")
    return f"postgresql+asyncpg://{user}:{pw}@{host}:{port}/{db}"


@pytest.fixture(scope="session")
def _1452_nullpool_engine():
    engine = create_async_engine(_1452_db_url(), poolclass=_1452_NullPool)
    yield engine


@pytest_asyncio.fixture(autouse=True)
async def _1452_session_scope_nullpool(_1452_nullpool_engine, monkeypatch):
    from services.database.session_factory import AsyncSessionFactory as _ASF

    maker = async_sessionmaker(
        _1452_nullpool_engine, class_=AsyncSession, expire_on_commit=False
    )

    @_1452_acm
    async def _scope():
        session = maker()
        try:
            yield session
            await session.commit()
        except Exception:
            try:
                await session.rollback()
            except Exception:
                pass
            raise
        finally:
            try:
                await session.close()
            except Exception:
                pass

    monkeypatch.setattr(_ASF, "session_scope", staticmethod(_scope))
    yield


# ---------------------------------------------------------------------------
# #1452: THE one test-user cascade delete. 26 FK references from 24 tables
# point at users (information_schema-derived 2026-07-21); per-site cleanup
# lists drift every time a table lands (personalization_contexts bit three
# helper files + both e2e conftests in one week). Order matters: grandchild →
# child → users. On a new FK violation here, re-derive the list (query in the
# #1452 thread) and extend THIS function only.
# ---------------------------------------------------------------------------
async def delete_test_user_fully(session, user_id: str) -> None:
    from sqlalchemy import text as _text

    uid = {"u": str(user_id)}
    for stmt in (
        "DELETE FROM conversation_turns WHERE conversation_id IN (SELECT id FROM conversations WHERE user_id = :u)",
        "DELETE FROM conversations WHERE user_id = :u",
        "DELETE FROM session_activity WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM token_blacklist WHERE user_id = CAST(:u AS uuid)",
        "DELETE FROM password_reset_tokens WHERE user_id = :u",
        "DELETE FROM user_api_keys WHERE user_id = :u",
        "DELETE FROM audit_logs WHERE user_id = :u",
        "DELETE FROM learned_patterns WHERE user_id = CAST(:u AS uuid)",
        "DELETE FROM learning_settings WHERE user_id = CAST(:u AS uuid)",
        "DELETE FROM user_trust_profiles WHERE user_id = :u",
        "DELETE FROM personality_profiles WHERE user_id = :u OR owner_id = CAST(:u AS uuid)",
        "DELETE FROM personalization_contexts WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM feedback WHERE user_id = CAST(:u AS uuid) OR owner_id = CAST(:u AS uuid)",
        "UPDATE invite_tokens SET used_by_user_id = NULL WHERE used_by_user_id = :u",
        "DELETE FROM uploaded_files WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM documents WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM knowledge_edges WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM knowledge_nodes WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM list_items WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM list_memberships WHERE owner_id = CAST(:u AS uuid)",
        "WITH del AS (DELETE FROM todo_items WHERE owner_id = CAST(:u AS uuid) RETURNING id) "
        "DELETE FROM items WHERE id IN (SELECT id FROM del)",
        "DELETE FROM lists WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM project_integrations WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM repositories WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM projects WHERE owner_id = :u",
        "DELETE FROM connector_bindings WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM connector_configs WHERE owner_id = CAST(:u AS uuid)",
        "DELETE FROM users WHERE id = :u",
    ):
        try:
            await session.execute(_text(stmt), uid)
        except Exception:
            # a table absent in this schema build or a type-cast miss must not
            # strand the rest of the cascade; the final users delete surfaces
            # any REAL leftover-FK problem loudly
            pass
    await session.commit()


@pytest.fixture(autouse=True)
def _1452_usage_cap_headroom(monkeypatch):
    """#1452: the instance-wide concurrency cap (10) is an OPS guard, not
    test-subject behavior — sweep residue in the shared dev Redis fills the
    gauge and 503s unrelated endpoint tests. Patch the limits AND clear the
    gauge key (the middleware may capture values before this runs; the key
    clear is the order-proof leg). Dedicated usage-cap tests layer their own."""
    try:
        import web.middleware.usage_cap_middleware as _ucm

        monkeypatch.setattr(_ucm, "MAX_CONCURRENT_SESSIONS", 1000)
        monkeypatch.setattr(_ucm, "RATE_LIMIT_PER_MINUTE", 100000)
    except Exception:
        pass
    try:
        import redis as _redis

        r = _redis.Redis(host="localhost", port=6379, socket_connect_timeout=1)
        r.delete("usage_cap:active_sessions")
        r.close()
    except Exception:
        pass
