"""#1601 — `effective_user_id` must not stringify a None `ctx.user_id` into
the literal string "None".

``services/intent/intent_service.py`` (``process_intent``) used to compute:

    effective_user_id = str(ctx.user_id) if ctx else user_id

``RequestContext.user_id`` is typed ``UUID`` (non-Optional), and its own
factory (``RequestContext.from_jwt_and_request``) refuses to build one
without a real ``claims.sub`` — but nothing at *runtime* stops a hand-built
(or future) context from carrying ``user_id=None``, since the dataclass has
no ``__post_init__`` guard. When that happened, ``str(None)`` produced the
THREE-CHARACTER STRING ``"None"`` rather than the value ``None``.

That was harmless while nothing consumed it as an identity. #1532 now uses
``effective_user_id`` as the ownership principal for conversation access —
so a ctx with a missing user_id and a ctx belonging to a real (if
improbably-named) user could collide on the string ``"None"``. The direction
is fail-closed (denies rather than leaks), but the sharp edge is real and
latent. Pinned here per #1601's acceptance criteria: a ctx with
``user_id=None`` must yield ``None``, never the string ``"None"``; a ctx with
a real UUID must still stringify normally.

Technique: ``_process_intent_internal`` is the very next call after
``effective_user_id`` is computed, and — unlike the #913 instrumentation
block just above it — is NOT wrapped in a swallowing ``except Exception:
pass``, so patching it to raise lets us inspect the call args it was invoked
with (i.e. the actual ``effective_user_id`` value) without needing to mock
the rest of the intent-processing pipeline.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from uuid import UUID, uuid4

import pytest

from services.domain.models import RequestContext
from services.intent.intent_service import IntentService


class _StopAtInternal(Exception):
    """Raised by the patched ``_process_intent_internal`` so the test can
    inspect its call args without running the real pipeline."""


def _ctx(user_id):
    """A RequestContext built directly (bypassing from_jwt_and_request's
    validation) — the exact shape #1601 says nothing at runtime prevents."""
    return RequestContext(
        user_id=user_id,
        conversation_id=uuid4(),
        request_id=uuid4(),
        user_email="user@example.com",
        timestamp=datetime.now(timezone.utc),
    )


@pytest.fixture
def service():
    return IntentService()


@pytest.mark.asyncio
async def test_ctx_with_none_user_id_yields_none_principal_not_the_string_none(service):
    ctx = _ctx(user_id=None)

    with patch.object(
        service, "_process_intent_internal", AsyncMock(side_effect=_StopAtInternal)
    ) as mock_internal:
        with pytest.raises(_StopAtInternal):
            await service.process_intent("hello", session_id="s1", ctx=ctx)

    effective_user_id = mock_internal.call_args.kwargs["user_id"]
    assert (
        effective_user_id is None
    ), f"ctx.user_id=None must yield a None principal, got {effective_user_id!r}"
    assert effective_user_id != "None"


@pytest.mark.asyncio
async def test_ctx_with_real_uuid_still_stringifies(service):
    real_id = UUID("11111111-2222-3333-4444-555555555555")
    ctx = _ctx(user_id=real_id)

    with patch.object(
        service, "_process_intent_internal", AsyncMock(side_effect=_StopAtInternal)
    ) as mock_internal:
        with pytest.raises(_StopAtInternal):
            await service.process_intent("hello", session_id="s1", ctx=ctx)

    assert mock_internal.call_args.kwargs["user_id"] == str(real_id)


@pytest.mark.asyncio
async def test_no_ctx_falls_back_to_the_legacy_user_id_param(service):
    """Unchanged behavior: with no ctx at all, the legacy `user_id` kwarg is
    used as-is (including a caller-supplied literal None)."""
    with patch.object(
        service, "_process_intent_internal", AsyncMock(side_effect=_StopAtInternal)
    ) as mock_internal:
        with pytest.raises(_StopAtInternal):
            await service.process_intent("hello", session_id="s1", user_id="legacy-id")

    assert mock_internal.call_args.kwargs["user_id"] == "legacy-id"
