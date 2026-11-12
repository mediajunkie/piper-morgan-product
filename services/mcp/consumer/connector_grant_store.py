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

from .github_app_grant import GitHubAppGrant


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

    async def get_strict(
        self, session: AsyncSession, user_id: str, connector: str
    ) -> Optional[str]:
        """#2266: the grant, or None ONLY when no grant row exists. A row whose secret
        cannot be read raises ``UserKeyReadFailed`` (#2151's contract), so a caller can
        tell absence from failure and never treats either as "connect without a token"."""
        return await self._service.retrieve_user_key_strict(session, user_id, _provider(connector))

    async def store_app_grant(
        self, session: AsyncSession, user_id: str, connector: str, grant: GitHubAppGrant
    ) -> None:
        """#2342: persist a GitHub App grant record: both tokens and both expiries in ONE
        row, so a refresh rewrites the pair in one write (the refresh token just used is
        already spent at GitHub).

        ``security_check=False`` (on #1982's closed list): the record was issued by
        GitHub's token endpoint in the same call, and the #268 validator can never accept
        it. Its fake-key rule refuses any value with under 30% distinct characters, which
        every record of this length is; a refused write here would lose a spent refresh
        token and force a reconnect.

        Arch 2026-11-12 06:53: the bypass covers this function only, and only a
        ``GitHubAppGrant`` passes through it. The record is built here, never handed in
        as a string, and the write is refused unless both tokens and both expiries are
        present, so no caller can put an arbitrary value through the bypass. Callers:
        the connect callback and the refresh (per request and background), each holding
        a reply GitHub issued in the same call."""
        if not isinstance(grant, GitHubAppGrant):
            raise TypeError("store_app_grant takes a GitHubAppGrant, never a raw value")
        tokens_ok = all(
            isinstance(v, str) and v.strip() for v in (grant.access_token, grant.refresh_token)
        )
        expiries_ok = all(
            isinstance(v, int) and not isinstance(v, bool) and v > 0
            for v in (grant.access_expires_at, grant.refresh_expires_at)
        )
        if not (tokens_ok and expiries_ok):
            raise ValueError("App grant record is incomplete; refusing to store it")
        await self._service.store_user_key(
            session,
            user_id,
            _provider(connector),
            grant.encode(),
            validate=False,
            security_check=False,
        )

    async def get_encrypted_strict(
        self, session: AsyncSession, user_id: str, connector: str
    ) -> Optional[str]:
        """#2342: the stored value from the encrypted row ONLY (no keychain copy), or None
        when no grant row exists. Raises ``UserKeyReadFailed`` when a row can't be read.
        App mode reads the grant here, because a keychain copy can hold a spent pair."""
        return await self._service.retrieve_encrypted_secret_strict(
            session, user_id, _provider(connector)
        )

    async def delete(self, session: AsyncSession, user_id: str, connector: str) -> bool:
        """Revoke (delete) the user's stored OAuth grant for ``connector`` — the disconnect
        inverse of ``store`` (#1330). Idempotent: returns ``False`` if no grant was stored."""
        return await self._service.delete_user_key(session, user_id, _provider(connector))
