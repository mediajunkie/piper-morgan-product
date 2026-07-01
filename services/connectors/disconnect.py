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
- **github** (ADR-070 binding): keychain PAT + env + config-cache + binding→UNBOUND +
  #358 grant revoke (the #1330 fix).
- **slack** (ADR-058 keychain): bot+user keychain tokens + Slack-side OAuth revoke
  (the #1334-P1 fix) + env.
- **calendar** (keychain): user-scoped refresh token.
- **notion** (keychain + #358 store): keychain key (legacy) AND the user-scoped
  UserAPIKeyService store where `save_notion_key` actually writes (#1337) — clearing
  only the keychain left the real token behind.
"""

from __future__ import annotations

import os

import structlog

logger = structlog.get_logger(__name__)

SUPPORTED_CONNECTORS = ("github", "slack", "calendar", "notion")


async def disconnect_connector(user_id: str, connector: str) -> None:
    """Clear whatever credential/binding the given connector holds for this user.

    Uniform interface; per-model dispatch below. Raises ValueError for an unknown
    connector (a programming error — callers pass a fixed literal). Individual clears
    are best-effort and never raise for a merely-absent credential.
    """
    if connector == "github":
        await _disconnect_github(user_id)
    elif connector == "slack":
        await _disconnect_slack(user_id)
    elif connector == "calendar":
        _disconnect_calendar(user_id)
    elif connector == "notion":
        await _disconnect_notion(user_id)
    else:
        raise ValueError(
            f"disconnect_connector: unknown connector {connector!r} "
            f"(supported: {', '.join(SUPPORTED_CONNECTORS)})"
        )


async def _disconnect_github(user_id: str) -> None:
    from services.infrastructure.keychain_service import KeychainService

    keychain = KeychainService()
    try:
        keychain.delete_api_key("github_token", username=user_id)  # #849 user-scoped
    except Exception:
        pass
    for var in ("GITHUB_TOKEN", "GITHUB_API_TOKEN", "GH_TOKEN"):
        os.environ.pop(var, None)
    try:
        from services.integrations.github.config_service import GitHubConfigService

        GitHubConfigService().clear_cache()
    except Exception:
        pass
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


async def _disconnect_slack(user_id: str) -> None:
    from services.infrastructure.keychain_service import KeychainService

    keychain = KeychainService()
    try:
        keychain.delete_api_key("slack_bot", username=user_id)
        keychain.delete_api_key("slack_user", username=user_id)
    except Exception:
        pass
    # #1334-P1: revoke on Slack's side too (best-effort).
    try:
        from services.integrations.slack.config_service import SlackConfigService
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        workspace_id = os.environ.get("SLACK_TEAM_ID", "default")
        oauth_handler = SlackOAuthHandler(SlackConfigService())
        await oauth_handler.revoke_workspace_access(workspace_id)
    except Exception as revoke_error:
        logger.warning(
            "slack_revoke_warning",
            error=str(revoke_error),
            message="Could not revoke via Slack API; cleared local creds",
        )
    for var in ("SLACK_BOT_TOKEN", "SLACK_TEAM_ID", "SLACK_APP_TOKEN"):
        os.environ.pop(var, None)


def _disconnect_calendar(user_id: str) -> None:
    from services.infrastructure.keychain_service import KeychainService

    keychain = KeychainService()
    try:
        keychain.delete_api_key(f"google_calendar_{user_id}")  # #839 user-scoped key
    except Exception:
        pass


async def _disconnect_notion(user_id: str) -> None:
    from services.infrastructure.keychain_service import KeychainService

    keychain = KeychainService()
    try:
        keychain.delete_api_key("notion", username=user_id)  # #849 legacy keychain
    except Exception:
        pass
    # #1337/#1334-P2: the real token lives in the user-scoped #358 store (save_notion_key
    # writes there via UserAPIKeyService) — clearing only the keychain left it behind.
    try:
        from services.database.session_factory import AsyncSessionFactory
        from services.security.user_api_key_service import UserAPIKeyService

        async with AsyncSessionFactory.session_scope_fresh() as session:
            await UserAPIKeyService().delete_user_key(session, user_id, "notion")
    except Exception as e:
        logger.warning("notion_user_key_clear_failed", error=str(e))
