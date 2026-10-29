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
# #2205 (Arch 2026-10-29 13:48): who designated the default. "user" = set in Settings or
# chat, answered to the write-time ask, or chosen in the setup wizard; "auto" = code picked
# it (#1314's rule at OAuth first-run or #1590's read-time recovery). A default with no
# source predates this key and counts as NOT user for writes (asked once). A sibling key in
# the same JSON blob: no schema change.
DEFAULT_REPO_SOURCE_KEY = "default_repository_source"
SOURCE_USER = "user"
SOURCE_AUTO = "auto"


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

    async def get_default_repo_source(self, owner_id: Union[str, UUID, None]) -> Optional[str]:
        """#2205: who designated the default ("user" | "auto"), or None (unset or legacy)."""
        return (await self.get_config(owner_id, GITHUB)).get(DEFAULT_REPO_SOURCE_KEY)

    async def set_default_repo(
        self,
        owner_id: Union[str, UUID, None],
        value: Optional[str],
        *,
        source: str,
    ) -> None:
        """Set (value) or clear (None) the owner's default GitHub repo, preserving other keys.
        #2205: ``source`` records who designated it (``user`` or ``auto``). REQUIRED, no
        default (Arch 14:39, condition 2): a permission-bearing value fails closed, so a
        caller that forgets it fails at call time instead of minting a write target."""
        if source not in (SOURCE_USER, SOURCE_AUTO):
            raise ValueError(f"default repo source must be 'user' or 'auto', not {source!r}")
        config = await self.get_config(owner_id, GITHUB)
        if value is None:
            config.pop(DEFAULT_REPO_KEY, None)
            config.pop(DEFAULT_REPO_SOURCE_KEY, None)
        else:
            config[DEFAULT_REPO_KEY] = value
            config[DEFAULT_REPO_SOURCE_KEY] = source
        await self.set_config(owner_id, GITHUB, config)
