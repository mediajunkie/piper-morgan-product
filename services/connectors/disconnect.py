"""Uniform connector-disconnect helper (#1334 Part 2, Arch-ruled 2026-06-30).

A single call surface — `disconnect_connector(user_id, connector)` — with per-model
dispatch behind it. The value (Arch ②): symmetric-by-construction disconnect that
recurrence-proofs #1330 (github disconnect that leaked the OAuth binding/grant). The
call surface is uniform regardless of the connector's credential model; the *impl*
per connector is swappable (m-40 layer-then-migrate — when a keychain connector
migrates onto the ADR-070 binding model under the (B)→(A) trigger, only the impl
behind this interface changes, not the call sites).

Per-connector clearing (each best-effort — a missing credential never fails the
disconnect; the point is to leave NO usable credential behind):
- **github** (ADR-070 binding): keychain PAT + config-cache + binding→UNBOUND +
  #358 grant revoke (the #1330 fix).
- **slack** (ADR-058 keychain): bot+user keychain tokens + Slack-side OAuth revoke
  (the #1334-P1 fix).

#1558 (mirror of #1507): this module must NEVER mutate `os.environ`. The old
github/slack clears popped GITHUB_TOKEN/GH_TOKEN/SLACK_BOT_TOKEN etc. — a
process-wide ambient-credential mutation: one user's disconnect deleted the
SYSTEM/deployment credential for every env-reading path in the process. And it
protected no user path: since #1461(a) the env fallback is system-only
(GitHubConfigService gates it on `not is_real_user`), so a real user's reads
never touch env. User disconnect touches only user-scoped stores. AST pin:
tests/unit/services/connectors/test_disconnect_no_env_mutation_1558.py.
- **calendar** (keychain): user-scoped refresh token + Google-side OAuth revoke
  (the #542 fix — previously local-clear only, never actually revoked).
- **notion** (keychain + #358 store): keychain key (legacy) AND the user-scoped
  UserAPIKeyService store where `save_notion_key` actually writes (#1337) — clearing
  only the keychain left the real token behind.

#2172 (Arch 2026-10-25, ADR-080 / #2151): a disconnect that SAYS it worked must have
verified it. Every clear is attempted (one failure never stops the rest), then each
copy is read back with provenance: a copy still there, or a read that failed, is
"remaining". ``disconnect_connector`` returns a ``DisconnectResult``; the routes say
"disconnected" only when ``remaining`` is empty. "Already absent" counts as gone. A
provider-side revoke (Slack, Google) that fails is not remaining: Piper holds no copy
once the local clears verify. It sets ``provider_revoke_failed`` and the success
message says the access stays valid at the provider (CXO 10-25).
"""

from __future__ import annotations

from dataclasses import dataclass

import structlog

logger = structlog.get_logger(__name__)

SUPPORTED_CONNECTORS = ("github", "slack", "calendar", "notion")


@dataclass(frozen=True)
class DisconnectResult:
    """What a disconnect verified (#2172). ``remaining`` names each copy that is still
    stored or couldn't be read back; empty means every copy is verifiably gone."""

    connector: str
    remaining: tuple[str, ...] = ()
    # The provider-side revoke (Slack, Google) failed: Piper holds no copy, but the
    # access stays valid at the provider until the person removes Piper there. Not
    # "remaining"; the success message says so (CXO 10-25).
    provider_revoke_failed: bool = False

    @property
    def cleared(self) -> bool:
        return not self.remaining


async def disconnect_connector(user_id: str, connector: str) -> DisconnectResult:
    """Clear whatever credential/binding the given connector holds for this user, then
    verify each copy is gone (#2172).

    Uniform interface; per-model dispatch below. Raises ValueError for an unknown
    connector (a programming error — callers pass a fixed literal). A merely-absent
    credential is cleared; a failed clear or a failed read-back is ``remaining``.
    """
    revoke_failed = False
    if connector == "github":
        remaining = await _disconnect_github(user_id)
    elif connector == "slack":
        remaining, revoke_failed = await _disconnect_slack(user_id)
    elif connector == "calendar":
        remaining, revoke_failed = await _disconnect_calendar(user_id)
    elif connector == "notion":
        remaining = await _disconnect_notion(user_id)
    else:
        raise ValueError(
            f"disconnect_connector: unknown connector {connector!r} "
            f"(supported: {', '.join(SUPPORTED_CONNECTORS)})"
        )
    result = DisconnectResult(connector, tuple(remaining), revoke_failed)
    if not result.cleared:
        logger.warning(
            "connector_disconnect_incomplete", connector=connector, remaining=result.remaining
        )
    return result


async def _keychain_copy_gone(keychain, provider: str, username: str | None) -> bool:
    """Delete one keychain copy, then read it back with provenance (#2172).

    ``delete_api_key`` answers False for both "not found" and "failed", so its answer
    can't tell gone from stuck; the read-back can. Only VERIFIED_ABSENT is gone.
    ``username`` has no default on purpose: check_unscoped_reads.py can't see through
    this helper, so each caller names its principal (or None, with the reason)."""
    from services.infrastructure.keychain_service import SecretProvenance

    try:
        await keychain.adelete_api_key(provider, username)
    except Exception:
        pass
    read = await keychain.aread_secret(provider, username)
    return read.provenance is SecretProvenance.VERIFIED_ABSENT


async def _disconnect_github(user_id: str) -> list[str]:
    from services.infrastructure.keychain_service import KeychainService

    remaining: list[str] = []
    keychain = KeychainService()
    if not await _keychain_copy_gone(keychain, "github_token", user_id):  # #849 user-scoped
        remaining.append("keychain_pat")
    # #1558: NO os.environ.pop here — env tokens are system/deployment
    # credentials (#1461(a): env fallback is system-only); a user-scoped
    # disconnect mutating them was process-wide cross-tenant damage.
    try:
        from services.integrations.github.config_service import GitHubConfigService

        GitHubConfigService().clear_cache()
    except Exception as e:
        logger.warning("github_config_cache_clear_failed", error=str(e))
        remaining.append("config_cache")
    # #1330: clear the OAuth binding + revoke the #358 grant (the inverse of
    # persist_github_connection) — else badge/health/reads still read "Connected".
    try:
        from services.connectors.binding_repository import ConnectorBindingRepository
        from services.database.session_factory import AsyncSessionFactory
        from services.mcp.consumer.connector import ConnectorStatusState
        from services.mcp.consumer.connector_grant_store import ConnectorGrantStore

        async with AsyncSessionFactory.session_scope() as session:
            await ConnectorBindingRepository(session).set_status(
                user_id, "github", ConnectorStatusState.UNBOUND.value
            )
            await ConnectorGrantStore().delete(session, user_id, "github")
    except Exception as e:
        logger.warning("github_oauth_binding_clear_failed", error=str(e))
        remaining.append("oauth_binding_and_grant")
    # The grant's keychain copy (#2172, Arch): ConnectorGrantStore.delete removes the
    # row, then this copy best-effort, so read it back here.
    if not await _keychain_copy_gone(keychain, "github_mcp_oauth", user_id):
        remaining.append("oauth_grant_keychain")
    # #1982: the at-rest PAT row (the dual write's second copy) goes too, so a
    # revoke leaves no row the MCP app's GitHub subkey could still read.
    try:
        from services.connectors.github_pat_store import delete_user_pat_at_rest
        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope() as session:
            await delete_user_pat_at_rest(session, user_id)
    except Exception as e:
        logger.warning("github_pat_at_rest_clear_failed", error=str(e))
        remaining.append("pat_at_rest")
    # The key service's own keychain copy (provider "github", #1982's dual write);
    # delete_user_pat_at_rest removes it best-effort, so read it back here.
    if not await _keychain_copy_gone(keychain, "github", user_id):
        remaining.append("keychain_pat_key_service")
    # The read-back is THE resolver (ADR-081 D1): gone means it finds no credential on
    # either leg and degrades CONNECT_REQUIRED. A leg it still serves, or a store that
    # didn't answer (UNREACHABLE), is not verified gone.
    try:
        from services.mcp.consumer.connector import DegradationReason
        from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

        resolved = await GitHubMCPSpatialAdapter().resolve_credential(user_id)
        leg = getattr(resolved, "leg", None)
        if leg is not None:
            remaining.append(f"credential_still_resolves:{leg}")
        elif getattr(resolved, "reason", None) is not DegradationReason.CONNECT_REQUIRED:
            remaining.append("credential_unverified")
    except Exception as e:
        logger.warning("github_disconnect_readback_failed", error=str(e))
        remaining.append("credential_unverified")
    return remaining


async def _disconnect_slack(user_id: str) -> tuple[list[str], bool]:
    from services.infrastructure.keychain_service import KeychainService

    remaining: list[str] = []
    revoke_failed = False
    keychain = KeychainService()

    # #1334-P1 / #542: revoke on Slack's side BEFORE clearing the keychain -- the
    # revoke call reads the live token via SlackConfigService, which reads the same
    # keychain entries deleted below. Revoking after deletion would always find
    # nothing to revoke (a real ordering bug, fixed 2026-07-06).
    try:
        from services.integrations.slack.config_service import SlackConfigService
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        oauth_handler = SlackOAuthHandler(SlackConfigService())
        revoke_failed = not await oauth_handler.revoke_workspace_access(user_id)
    except Exception as revoke_error:
        revoke_failed = True
        logger.warning(
            "slack_revoke_warning",
            error=str(revoke_error),
            message="Could not revoke via Slack API; clearing local creds anyway",
        )

    for provider in ("slack_bot", "slack_user"):
        if not await _keychain_copy_gone(keychain, provider, user_id):
            remaining.append(provider)
    # #1558: NO os.environ.pop here — same class as the github clear above
    # (SLACK_BOT_TOKEN env is deployment config, not a user credential).
    return remaining, revoke_failed


async def _disconnect_calendar(user_id: str) -> tuple[list[str], bool]:
    from services.infrastructure.keychain_service import KeychainService

    remaining: list[str] = []
    revoke_failed = False
    keychain = KeychainService()
    key_name = f"google_calendar_{user_id}"  # #839 user-scoped key

    # #542: revoke on Google's side before clearing locally (best-effort -- a
    # revoke failure must never leave the disconnect incomplete).
    try:
        refresh_token = await keychain.aget_api_key(key_name)
        if refresh_token:
            from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

            revoke_failed = not await GoogleCalendarOAuthHandler().revoke_token(refresh_token)
    except Exception as e:
        revoke_failed = True
        logger.warning("calendar_revoke_attempt_failed", error=str(e))

    # username None: the key name itself carries the user id (#839).
    if not await _keychain_copy_gone(keychain, key_name, None):
        remaining.append("calendar_refresh_token")
    return remaining, revoke_failed


async def _disconnect_notion(user_id: str) -> list[str]:
    from services.infrastructure.keychain_service import KeychainService

    remaining: list[str] = []
    keychain = KeychainService()
    # #1337/#1334-P2: the real token lives in the user-scoped #358 store (save_notion_key
    # writes there via UserAPIKeyService) — clearing only the keychain left it behind.
    try:
        from services.database.session_factory import AsyncSessionFactory
        from services.security.user_api_key_service import UserAPIKeyService

        async with AsyncSessionFactory.session_scope_fresh() as session:
            await UserAPIKeyService().delete_user_key(session, user_id, "notion")
    except Exception as e:
        logger.warning("notion_user_key_clear_failed", error=str(e))
        remaining.append("notion_user_key")
    # The keychain copy last: delete_user_key's own keychain delete is best-effort, and
    # the #849 legacy key shares the slot; the read-back covers both.
    if not await _keychain_copy_gone(keychain, "notion", user_id):  # #849 legacy keychain
        remaining.append("notion_keychain")
    return remaining
