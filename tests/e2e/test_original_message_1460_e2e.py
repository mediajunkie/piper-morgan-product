"""
#1460 runtime verification: original_message instance fix, end-to-end.

Drives the REAL app in-process (ASGI transport, POST /api/v1/intent) — not
unit mocks — to pin the two user-visible outcomes the #1459 trace showed
were broken:

1. 'help me setup my projects' reaches the #814 setup flow
   (``provide_setup_guidance``) instead of being silently floor-routed.
   Pre-fix: ``detect_multiple_intents`` produced dict-only Intents, the
   attribute-only ``_detect_setup_request`` gate never fired, and the setup
   flow was skipped on the dominant chat path (#1417's mis-route resurfaced).
2. A multi-intent turn whose TEMPORAL half asks for the day's schedule
   reaches the agenda aggregation path (``provide_agenda``) via the
   orchestrator route. Pre-fix: the orchestrator calls CanonicalHandlers
   directly (no backfill), all four temporal detectors read the attribute
   only, and the turn got the bare date template.

NOTE on the pinned multi-intent message: the #1460 AC's exemplar
("What's my schedule today and show my todos") cannot reach the TEMPORAL
handler at all — "my schedule today" matches CALENDAR_QUERY_PATTERNS, the
subsumption filter drops TEMPORAL, and the orchestrator has no QUERY handler,
so BOTH halves fail regardless of original_message plumbing. That is a
pre-existing pre-classifier taxonomy gap (same shape as #1084), out of scope
for this wiring-only fix and tracked separately (see the #1460 discovered-work
note). The pinned message below genuinely takes the TEMPORAL multi-intent
path: it matches TEMPORAL (``\\bmy schedule\\b``) without matching any
calendar pattern, and carries the agenda keywords ("schedule" + "today") the
detector gates on.

Both queries are fully pre-classified (deterministic) and the responses are
canonical-handler built — no LLM classification or floor call — so this
module is keyless-safe.

Fixtures mirror tests/e2e/test_canonical_conversations.py's module-scoped
boot-once pattern (#1165). Requires PostgreSQL on 5433.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from uuid import uuid4

import httpx
import pytest
import pytest_asyncio
from httpx import ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"

SETUP_MESSAGE = "help me setup my projects"
AGENDA_MULTI_INTENT_MESSAGE = "What does my schedule look like today and show my todos"


@pytest_asyncio.fixture(scope="module")
async def e2e_client():
    """Module-scoped: boot the real app once (see #1165 rationale)."""
    from web.app import app

    @asynccontextmanager
    async def _lifespan():
        async with app.router.lifespan_context(app):
            yield

    async with _lifespan():
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest_asyncio.fixture(scope="module")
async def e2e_auth_headers(e2e_client):
    """Module-scoped shared test user (mirrors the canonical suite fixture)."""
    from services.auth.password_service import PasswordService

    user_id = str(uuid4())
    username = f"om1460_e2e_{user_id[:8]}"
    password = "testpass123"
    password_hash = PasswordService().hash_password(password)

    engine = create_async_engine(_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        await s.execute(
            text(
                "INSERT INTO users (id, username, email, password_hash, is_active, "
                "is_verified, created_at, updated_at, role, is_alpha) "
                "VALUES (:id, :u, :e, :ph, true, true, :now, :now, 'user', true)"
            ),
            {
                "id": user_id,
                "u": username,
                "e": f"{username}@test.example.com",
                "ph": password_hash,
                "now": datetime.now(timezone.utc),
            },
        )
        await s.commit()

    login = await e2e_client.post(
        "/api/v1/auth/login", data={"username": username, "password": password}
    )
    assert login.status_code == 200, f"login failed: {login.text}"
    yield {"cookies": login.cookies}

    from tests.conftest import delete_test_user_fully

    async with async_session() as s:
        await delete_test_user_fully(s, user_id)
        await s.commit()
    await engine.dispose()


async def _post_intent(client, message, auth):
    response = await client.post(
        "/api/v1/intent",
        json={"message": message, "session_id": str(uuid4())},
        **auth,
    )
    assert response.status_code == 200, f"HTTP {response.status_code}: {response.text[:200]}"
    return response.json()


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_setup_request_reaches_setup_flow(e2e_client, e2e_auth_headers):
    """#1460 AC-1: setup request reaches the #814 setup flow, not the floor."""
    data = await _post_intent(e2e_client, SETUP_MESSAGE, e2e_auth_headers)

    intent = data.get("intent", {}) or {}
    assert intent.get("floor_hit") is not True, (
        f"setup request was floor-routed (the pre-#1460 mis-route): {intent}"
    )
    assert intent.get("action") == "provide_setup_guidance", (
        "setup request did not reach the #814 setup flow "
        f"(action={intent.get('action')!r}, category={intent.get('category')!r}); "
        f"message head: {str(data.get('message'))[:120]!r}"
    )
    # The setup-flow response is substantive guidance, not the bare fallback.
    assert data.get("message"), "empty message from setup flow"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_multi_intent_schedule_turn_reaches_agenda_aggregation(
    e2e_client, e2e_auth_headers
):
    """#1460 AC-2: multi-intent schedule turn hits agenda aggregation (orchestrator)."""
    data = await _post_intent(e2e_client, AGENDA_MULTI_INTENT_MESSAGE, e2e_auth_headers)

    intent = data.get("intent", {}) or {}
    assert intent.get("floor_hit") is not True, f"unexpected floor route: {intent}"
    assert intent.get("action") == "provide_agenda", (
        "multi-intent schedule turn did not reach the agenda aggregation path "
        "(pre-#1460 this was the bare date template from _handle_temporal_query) "
        f"(action={intent.get('action')!r}, category={intent.get('category')!r}); "
        f"message head: {str(data.get('message'))[:120]!r}"
    )
    message = data.get("message") or ""
    assert "agenda" in message.lower() or "Today is" not in message, (
        f"agenda aggregation produced a bare date template: {message[:160]!r}"
    )
