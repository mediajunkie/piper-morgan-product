"""Settings "Connected apps" API routes (#1918).

Backend half of #1918 only — see the issue for the UI card (CXO-designed,
built separately) and #1911 (consent-copy update, gated on this shipping).

Lets a signed-in alpha user see which MCP OAuth clients (ChatGPT, Claude,
etc.) hold access to their Piper account, and revoke any of them
immediately. Business logic lives in ``services/mcp/server/connections.py``
(owner-scoped by construction); this router's only job is auth +
HTTP shape — it never accepts a user id from the request, only from the
authenticated session (``get_current_user``), matching every other
settings route on this app (see ``web/api/routes/settings_integrations.py``).
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.session_factory import AsyncSessionFactory
from services.mcp.server.connections import list_user_connections, revoke_oauth_connection

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/settings/mcp-connections", tags=["settings-mcp-connections"])


class OAuthConnectionResponse(BaseModel):
    client_id: str
    client_name: Optional[str] = None
    connected_at: datetime
    last_used_at: Optional[datetime] = None
    active: bool


class ManualTokenResponse(BaseModel):
    label: str
    connected_at: datetime
    last_used_at: Optional[datetime] = None
    active: bool


class MCPConnectionsResponse(BaseModel):
    oauth_connections: List[OAuthConnectionResponse]
    manual_tokens: List[ManualTokenResponse]


class MCPConnectionRevokeResponse(BaseModel):
    revoked: bool
    client_id: str


@router.get("", response_model=MCPConnectionsResponse)
async def list_mcp_connections(
    current_user: JWTClaims = Depends(get_current_user),
) -> MCPConnectionsResponse:
    """The caller's MCP grants: OAuth clients grouped by ``client_id``, plus
    manually-minted bearer tokens by label. Never returns a token hash or
    raw token."""
    try:
        async with AsyncSessionFactory.session_scope() as session:
            connections = await list_user_connections(session, current_user.user_id)
    except Exception as e:
        logger.error("mcp_connections_list_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load MCP connections",
        )

    return MCPConnectionsResponse(
        oauth_connections=[
            OAuthConnectionResponse(
                client_id=c.client_id,
                client_name=c.client_name,
                connected_at=c.connected_at,
                last_used_at=c.last_used_at,
                active=c.active,
            )
            for c in connections.oauth_connections
        ],
        manual_tokens=[
            ManualTokenResponse(
                label=t.label,
                connected_at=t.connected_at,
                last_used_at=t.last_used_at,
                active=t.active,
            )
            for t in connections.manual_tokens
        ],
    )


@router.post("/{client_id}/revoke", response_model=MCPConnectionRevokeResponse)
async def revoke_mcp_connection(
    client_id: str,
    current_user: JWTClaims = Depends(get_current_user),
) -> MCPConnectionRevokeResponse:
    """Revoke every one of the CALLER's access + refresh tokens for
    ``client_id``, in one transaction. Idempotent (a second call on an
    already-revoked connection still returns 200/revoked=true). 404s for a
    ``client_id`` this user never held a credential for — never reveals
    whether it exists for a different user."""
    try:
        async with AsyncSessionFactory.session_scope() as session:
            found = await revoke_oauth_connection(session, current_user.user_id, client_id)
    except Exception as e:
        logger.error(
            "mcp_connection_revoke_failed", client_id=client_id, error=str(e), exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke MCP connection",
        )

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such connection")

    logger.info("mcp_connection_revoked", user_id=str(current_user.user_id), client_id=client_id)
    return MCPConnectionRevokeResponse(revoked=True, client_id=client_id)
