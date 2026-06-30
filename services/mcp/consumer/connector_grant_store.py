"""Per-user connector OAuth-grant storage (#1317 inc.2 slice B; ADR-070 C / D3).

Stores a connector's user OAuth grant in the #358 encrypted user-secret store
(``user_api_keys``, encrypted-at-rest), keyed ``(user_id, "<connector>_mcp_oauth")``.
The #1229 ``ConnectorBinding`` references this by the ``(owner, connector)`` convention —
the binding row holds NO token (ADR-070 D3 precise: no raw vendor PAT; scoped/revocable
OAuth grants permitted, encrypted-at-rest, binding = pointer).

``validate=False`` on store: the grant is an OAuth token forwarded to the self-hosted
``github-mcp-server``, not a provider API key to validate against a vendor endpoint.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from services.security.user_api_key_service import UserAPIKeyService


def _provider(connector: str) -> str:
    """The user_api_keys provider key for a connector's OAuth grant."""
    return f"{connector}_mcp_oauth"


class ConnectorGrantStore:
    """Thin store for per-user connector OAuth grants over the #358 user-secret store."""

    def __init__(self, service: Optional[UserAPIKeyService] = None) -> None:
        self._service = service or UserAPIKeyService()

    async def store(
        self, session: AsyncSession, user_id: str, connector: str, access_token: str
    ) -> None:
        """Persist the user's OAuth grant for ``connector`` (encrypted-at-rest)."""
        await self._service.store_user_key(
            session, user_id, _provider(connector), access_token, validate=False
        )

    async def get(self, session: AsyncSession, user_id: str, connector: str) -> Optional[str]:
        """Return the user's stored OAuth grant for ``connector``, or ``None``."""
        return await self._service.retrieve_user_key(session, user_id, _provider(connector))

    async def delete(self, session: AsyncSession, user_id: str, connector: str) -> bool:
        """Revoke (delete) the user's stored OAuth grant for ``connector`` — the disconnect
        inverse of ``store`` (#1330). Idempotent: returns ``False`` if no grant was stored."""
        return await self._service.delete_user_key(session, user_id, _provider(connector))
