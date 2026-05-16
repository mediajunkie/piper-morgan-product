"""RequestContext enforcement tests (Phase 3 of #734 Multi-Tenancy Isolation).

These tests verify that:
1. Authenticated routes create RequestContext at boundary
2. RequestContext is passed to services (not reconstructed)
3. Unauthenticated requests are rejected

TDD: Write tests first, then implement.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTClaims
from services.domain.models import RequestContext


def make_jwt_claims(
    sub: str = None,
    user_email: str = "test@example.com",
    username: str = "testuser",
    workspace_id: str = None,
    use_empty_sub: bool = False,
) -> JWTClaims:
    """Helper to create JWTClaims with all required fields.

    Args:
        sub: Subject (user ID as string). If None, generates one.
        user_email: User email
        username: Username
        workspace_id: Optional workspace ID
        use_empty_sub: If True, sets sub to empty string (for testing validation)
    """
    user_id = uuid4()
    effective_sub = "" if use_empty_sub else (sub or str(user_id))
    return JWTClaims(
        iss="piper-morgan",
        aud="piper-morgan-api",
        sub=effective_sub,
        exp=int(datetime.now(timezone.utc).timestamp()) + 3600,
        iat=int(datetime.now(timezone.utc).timestamp()),
        jti=str(uuid4()),
        user_id=user_id,
        user_email=user_email,
        username=username,
        scopes=["user"],
        token_type="access",
        workspace_id=workspace_id,
    )


class TestRequestContextFactory:
    """Test RequestContext.from_jwt_and_request() factory."""

    def test_creates_context_from_valid_claims(self):
        """Factory creates context with correct values from JWT claims."""
        claims = make_jwt_claims()
        conversation_id = str(uuid4())

        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=conversation_id,
        )

        assert ctx.user_id == UUID(claims.sub)
        assert ctx.conversation_id == UUID(conversation_id)
        assert ctx.user_email == claims.user_email
        assert ctx.request_id is not None  # Auto-generated
        assert ctx.timestamp is not None

    def test_rejects_missing_sub(self):
        """Factory rejects claims without 'sub' field."""
        claims = make_jwt_claims(use_empty_sub=True)  # Empty sub

        with pytest.raises(ValueError, match="missing 'sub' field"):
            RequestContext.from_jwt_and_request(
                claims=claims,
                conversation_id=str(uuid4()),
            )

    def test_rejects_missing_conversation_id(self):
        """Factory rejects missing conversation_id."""
        claims = make_jwt_claims()

        with pytest.raises(ValueError, match="conversation_id is required"):
            RequestContext.from_jwt_and_request(
                claims=claims,
                conversation_id="",  # Empty
            )

    def test_accepts_custom_request_id(self):
        """Factory accepts custom request_id for tracing."""
        claims = make_jwt_claims()
        custom_request_id = uuid4()

        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=str(uuid4()),
            request_id=custom_request_id,
        )

        assert ctx.request_id == custom_request_id

    def test_includes_workspace_id_when_provided(self):
        """Factory includes workspace_id when present in claims."""
        workspace_id = uuid4()
        claims = make_jwt_claims(workspace_id=str(workspace_id))

        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=str(uuid4()),
        )

        assert ctx.workspace_id == workspace_id


# Note: TestRequireRequestContext class removed 2026-05-16 per #1015 Phase 2
# (ADR-051 amendment). The `require_request_context` dependency it tested was
# deleted as part of the same amendment; tests deleted alongside.


class TestContextImmutability:
    """Test that RequestContext is immutable."""

    def test_context_is_frozen(self):
        """RequestContext should be immutable (frozen dataclass)."""
        claims = make_jwt_claims()

        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=str(uuid4()),
        )

        # Attempting to modify should raise
        with pytest.raises(Exception):  # FrozenInstanceError
            ctx.user_id = uuid4()
