"""Connector-config service (RECONNECT WS-1, #1226 / #1199).

The single connector-config interface over `connector_configs` (ADR-070 D4) — the home
that supersedes the three scattered stores in P3:
  - `UserPreferenceManager` (in-memory default-repo)
  - the flat `data/github_preferences.json` file (the settings-UI bridge)
  - the github `config_service` default-repository accessor

The github default-repo accessors below mirror `UserPreferenceManager.get/set_default_repo`'s
signature exactly (owner_id in, "owner/name" out) so P3 can swap callers without shape
changes. Like the repository, this layer flushes but does NOT commit — the caller owns the
transaction boundary (request handler / workflow), which P3 reconciles per-caller.
"""
from __future__ import annotations

from typing import Optional, Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from services.connectors.config_repository import ConnectorConfigRepository

GITHUB = "github"
DEFAULT_REPO_KEY = "default_repository"


class ConnectorConfigService:
    """WS-1 connector-config interface (ADR-070 D4). Owner-scoped; credential-free (D3)."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ConnectorConfigRepository(session)

    async def get_config(self, owner_id: Union[str, UUID, None], connector: str) -> dict:
        """The connector's config blob for the owner — a COPY (empty dict if unset/graceful-miss)."""
        row = await self.repo.get(owner_id, connector)
        return dict(row.config) if row and row.config else {}

    async def set_config(
        self, owner_id: Union[str, UUID, None], connector: str, config: dict
    ) -> None:
        """Replace the connector's config blob for the owner (write is strict on owner_id)."""
        await self.repo.upsert(owner_id, connector, config)

    # --- github default-repo: drop-in for UserPreferenceManager.get/set_default_repo ---

    async def get_default_repo(self, owner_id: Union[str, UUID, None]) -> Optional[str]:
        """The owner's default GitHub repo as 'owner/name', or None if unset."""
        return (await self.get_config(owner_id, GITHUB)).get(DEFAULT_REPO_KEY)

    async def set_default_repo(
        self, owner_id: Union[str, UUID, None], value: Optional[str]
    ) -> None:
        """Set (value) or clear (None) the owner's default GitHub repo, preserving other keys."""
        config = await self.get_config(owner_id, GITHUB)
        if value is None:
            config.pop(DEFAULT_REPO_KEY, None)
        else:
            config[DEFAULT_REPO_KEY] = value
        await self.set_config(owner_id, GITHUB, config)
