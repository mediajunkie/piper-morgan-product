"""#2342 (ADR-081 D3): where the published GitHub App is installed for a person.

In App mode a person's grant reaches only the repositories they installed the App on.
``list_installed_repositories`` reads that set from GitHub's REST API with the person's
own access token (``GET /user/installations``, then each installation's repositories),
so the Settings list shows what Piper can actually use, and a person who has authorized
but installed the App nowhere gets a named state with CXO's words, never an empty list.

A read that fails raises ``InstallationReadFailed``. It is never reported as "not
installed": a failed read is not absence (#2151).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import aiohttp
import structlog

logger = structlog.get_logger(__name__)

_API = "https://api.github.com"
_PER_PAGE = 100
_TIMEOUT_SECONDS = 10

#: The ``detail`` a REPO_UNRESOLVED degrade carries when the App is installed nowhere.
DETAIL_APP_NOT_INSTALLED = "app_not_installed"
#: The same state when no install link can be given (``GITHUB_APP_SLUG`` unset).
DETAIL_APP_INSTALL_LINK_MISSING = "app_install_link_missing"


class InstallationReadFailed(Exception):
    """GitHub did not answer the installation read. Carries the HTTP status, if any."""

    def __init__(self, status: Optional[int] = None, error: str = ""):
        super().__init__(f"installation read failed (status={status}, error={error})")
        self.status = status


@dataclass(frozen=True)
class InstalledRepositories:
    """The repositories the App is installed on for this person, normalized to the
    ``GitHubRepositoryInfo`` shape, and how many installations there are."""

    installations: int
    repositories: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def installed_nowhere(self) -> bool:
        return not self.repositories


def _headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


async def _get_json(session, url: str, token: str, params: Dict[str, Any]) -> Dict[str, Any]:
    async with session.get(url, headers=_headers(token), params=params) as response:
        if response.status != 200:
            raise InstallationReadFailed(response.status)
        data = await response.json(content_type=None)
    if not isinstance(data, dict):
        raise InstallationReadFailed(200, "unexpected_body")
    return data


#: A bound on pages per listing, so a reply that never ends can't hold a request. At 100
#: per page this is 10,000 repositories; reaching it fails the read rather than showing
#: part of a list as if it were complete (Arch 2026-11-12 07:35).
_MAX_PAGES = 100


async def list_installed_repositories(token: str) -> InstalledRepositories:
    """Every repository the App is installed on for the token's person, following
    pagination to the end (Arch 2026-11-12 07:35). With a user token GitHub returns the
    overlap of the person's access and the installation's repositories, which is the set
    Piper can act on; it is not intersected with any search.

    A partial read is a failed read: if any page of any installation can't be read,
    ``InstallationReadFailed`` is raised and nothing is returned. Never logs the token."""
    if not token:
        raise InstallationReadFailed(None, "no_token")
    repositories: List[Dict[str, Any]] = []
    seen = set()
    try:
        timeout = aiohttp.ClientTimeout(total=_TIMEOUT_SECONDS)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            installations: List[Dict[str, Any]] = []
            page = 1
            while True:
                listing = await _get_json(
                    session,
                    f"{_API}/user/installations",
                    token,
                    {"per_page": _PER_PAGE, "page": page},
                )
                batch = listing.get("installations") or []
                installations.extend(batch)
                if len(batch) < _PER_PAGE:
                    break
                page += 1
                if page > _MAX_PAGES:
                    raise InstallationReadFailed(None, "too_many_pages")
            for installation in installations:
                installation_id = installation.get("id")
                if installation_id is None:
                    raise InstallationReadFailed(200, "installation_without_id")
                page = 1
                while True:
                    data = await _get_json(
                        session,
                        f"{_API}/user/installations/{installation_id}/repositories",
                        token,
                        {"per_page": _PER_PAGE, "page": page},
                    )
                    batch = data.get("repositories") or []
                    for repo in batch:
                        full_name = repo.get("full_name") or ""
                        if not full_name or full_name in seen:
                            continue
                        seen.add(full_name)
                        repositories.append(
                            {
                                "id": repo.get("id", 0),
                                "name": repo.get("name", ""),
                                "full_name": full_name,
                                "description": repo.get("description") or "",
                            }
                        )
                    if len(batch) < _PER_PAGE:
                        break
                    page += 1
                    if page > _MAX_PAGES:
                        raise InstallationReadFailed(None, "too_many_pages")
    except InstallationReadFailed:
        raise
    except Exception as e:  # timeout, connection failure, a body that isn't JSON
        logger.warning("github_app_installation_read_failed", error=type(e).__name__)
        raise InstallationReadFailed(None, type(e).__name__) from e
    return InstalledRepositories(installations=len(installations), repositories=repositories)
