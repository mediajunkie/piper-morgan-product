"""
GitHub Repository Validator — soft validation via GitHub REST API.

Issue #867: Optionally validate repos exist and pull metadata when linking.
Soft validation: if token unavailable or API fails, warn but don't block.
"""

import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp
import structlog

logger = structlog.get_logger()

GITHUB_API_BASE = "https://api.github.com"


@dataclass
class RepoValidationResult:
    """Result of a GitHub API repo validation attempt."""

    validated: bool  # True if API call was attempted
    exists: bool  # True if repo was found (HTTP 200)
    accessible: bool  # True if token has read access
    error: Optional[str] = None
    # Metadata — populated only on success
    description: Optional[str] = None
    language: Optional[str] = None
    visibility: Optional[str] = None  # "public", "private", "internal"
    default_branch: Optional[str] = None
    # HTTP status GitHub answered with; None when no response was read (no token, network
    # error). Lets a caller tell 404 (not found) from 401/403 (no access) from other statuses
    # without parsing ``error`` text (#2230).
    status_code: Optional[int] = None
    # Why the check did not run or settle: "no_credential" (no token for the account),
    # "network" (connection or timeout), "error" (unexpected exception or status). None when
    # GitHub gave a definite answer (200, 404, 401, 403). Callers that ignore it are unaffected.
    not_checked_reason: Optional[str] = None

    @property
    def metadata_available(self) -> bool:
        """True if we got metadata from the API."""
        return self.validated and self.exists and self.accessible


def get_github_token() -> Optional[str]:
    """The deployment's GitHub token, LOCAL INSTALLS ONLY (ADR-081 D2): None on a hosted
    deploy. An alias of ``GitHubConfigService().get_authentication_token("system")``, the
    one local-only reader of the env token names. A caller acting for an account should
    use ``validate_github_repo_for_account`` (ADR-081 D1)."""
    from services.integrations.github.config_service import GitHubConfigService

    return GitHubConfigService().get_authentication_token("system")


async def validate_github_repo(
    full_name: str,
    token: Optional[str] = None,
    *,
    headers: Optional[dict] = None,
) -> RepoValidationResult:
    """Validate a GitHub repo exists and pull metadata.

    Args:
        full_name: Repository in "owner/repo" format.
        token: the requesting account's own GitHub token. None returns the
               unvalidated result, which means "not checked", never "doesn't exist".
               ADR-081 D1 (Arch 10-24 18:45): never the deployment's env token, which
               can see repos the account can't. A caller acting for an account uses
               ``validate_github_repo_for_account``.

    Returns:
        RepoValidationResult with validation status and optional metadata.
    """
    # #2235: ``headers`` is the account's own Authorization as the connector's one
    # credential resolver built it (``GitHubMCPSpatialAdapter._grant_headers_or_raise``:
    # the OAuth grant or the PAT, as ``Bearer``). ``token`` remains for the local
    # deployment-token path only; never both.
    if not headers and not token:
        logger.info("github_repo_validation_skipped", full_name=full_name, reason="no_token")
        return RepoValidationResult(
            validated=False, exists=False, accessible=False, not_checked_reason="no_credential"
        )
    url = f"{GITHUB_API_BASE}/repos/{full_name}"
    authorization = dict(headers) if headers else {"Authorization": f"token {token}"}
    headers = {
        **authorization,
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "piper-morgan",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(
                        "github_repo_validation_success",
                        full_name=full_name,
                        visibility=data.get("visibility"),
                    )
                    return RepoValidationResult(
                        validated=True,
                        exists=True,
                        accessible=True,
                        description=data.get("description"),
                        language=data.get("language"),
                        visibility=data.get("visibility"),
                        default_branch=data.get("default_branch"),
                        status_code=200,
                    )
                elif resp.status == 404:
                    logger.warning("github_repo_validation_not_found", full_name=full_name)
                    return RepoValidationResult(
                        validated=True,
                        exists=False,
                        accessible=False,
                        error=f"Repository '{full_name}' not found on GitHub",
                        status_code=404,
                    )
                elif resp.status == 401:
                    logger.warning("github_repo_validation_auth_failed", full_name=full_name)
                    return RepoValidationResult(
                        validated=True,
                        exists=False,
                        accessible=False,
                        error="GitHub token is invalid or expired",
                        status_code=401,
                    )
                elif resp.status == 403:
                    logger.warning(
                        "github_repo_validation_forbidden",
                        full_name=full_name,
                        status=403,
                    )
                    return RepoValidationResult(
                        validated=True,
                        exists=True,
                        accessible=False,
                        error="GitHub API rate limit or insufficient permissions",
                        status_code=403,
                    )
                else:
                    logger.warning(
                        "github_repo_validation_unexpected_status",
                        full_name=full_name,
                        status=resp.status,
                    )
                    return RepoValidationResult(
                        validated=True,
                        exists=False,
                        accessible=False,
                        error=f"GitHub API returned status {resp.status}",
                        status_code=resp.status,
                        not_checked_reason="error",
                    )

    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logger.warning("github_repo_validation_network_error", full_name=full_name, error=str(e))
        return RepoValidationResult(
            validated=False,
            exists=False,
            accessible=False,
            error=f"Network error: {e}",
            not_checked_reason="network",
        )
    except Exception as e:
        logger.error("github_repo_validation_unexpected_error", full_name=full_name, error=str(e))
        return RepoValidationResult(
            validated=False,
            exists=False,
            accessible=False,
            error=f"Unexpected error: {e}",
            not_checked_reason="error",
        )


async def _account_authorization(
    user_id: Optional[str],
) -> tuple[Optional[dict], Optional[str], Optional[str]]:
    """``(headers, not_checked_reason, error)`` for the requesting account (#2235).

    The credential comes from the connector's ONE resolver,
    ``GitHubMCPSpatialAdapter.resolve_credential`` via ``_grant_headers_or_raise``:
    the BOUND OAuth grant first, the account's own PAT second (ADR-081 D1, #1965).
    Before #2235 this read only the PAT, so an account connected by "Connect with
    GitHub" alone was never validated ("not checked" on every repo).

    A refusal keeps its reason, and a failed read is never "not found" (#2151):
    ``no_account`` (no principal), ``no_credential`` (neither leg: CONNECT_REQUIRED),
    ``credential_failed`` (a leg exists but failed: stale token, unreachable store,
    missing grant; the detail rides in ``error``).
    """
    if not user_id:
        return None, "no_account", None
    try:
        from services.integrations.github.read_failed import GitHubReadFailed
        from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

        try:
            headers = await GitHubMCPSpatialAdapter()._grant_headers_or_raise(user_id)
        except GitHubReadFailed as e:
            if e.detail == "no_credential":
                return None, "no_credential", None
            logger.warning(
                "github_repo_validation_credential_failed",
                user_id=str(user_id),
                reason=e.reason_code,
                detail=e.detail,
            )
            return (
                None,
                "credential_failed",
                f"GitHub credential failed: {e.detail or e.reason_code}",
            )
        return headers, None, None
    except Exception as e:  # silent-ok: LOGGED; the pre-2235 catch, kept: a validator fault is "not checked", never a dead wizard turn
        logger.warning(
            "github_repo_validation_token_unreadable", error=type(e).__name__, exc_info=True
        )
        return None, "error", f"Credential read error: {type(e).__name__}"


async def validate_github_repo_for_account(
    full_name: str, user_id: Optional[str]
) -> RepoValidationResult:
    """ADR-081 D1: validate ``full_name`` as the requesting account, with its own
    credential, resolved by the connector's one resolver (#2235: the OAuth leg or the
    PAT leg). No credential, or one that couldn't be read, returns ``validated=False``
    with a stated ``not_checked_reason``; it is never read as "not found"."""
    headers, reason, error = await _account_authorization(user_id)
    if headers is None:
        return RepoValidationResult(
            validated=False,
            exists=False,
            accessible=False,
            error=error,
            not_checked_reason=reason,
        )
    return await validate_github_repo(full_name, headers=headers)


def apply_validation_metadata(repo, result: RepoValidationResult):
    """Merge validated metadata into a Repository domain entity.

    Modifies the repo in place. Only applies metadata if the validation succeeded.
    """
    if result.metadata_available:
        repo.description = result.description
        repo.language = result.language
        repo.visibility = result.visibility
        repo.default_branch = result.default_branch
