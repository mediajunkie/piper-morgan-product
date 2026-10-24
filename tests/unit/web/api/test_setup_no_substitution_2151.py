"""#2151 route group 3 (Arch 10-24 09:09): the setup wizard never presents someone else's
credential as the visitor's.

- check-keychain / use-keychain on a HOSTED deploy: the "keychain" is the operator's store,
  so the wizard is never offered it (local installs unchanged: the keychain is the user's).
- slack/status with no signed-in user: the "system" principal's token is never this
  visitor's connection.
(calendar/status's no-user case is in test_calendar_status_scoped_key_1434.py.)
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from web.api.routes import setup as setup_routes


@pytest.mark.asyncio
@pytest.mark.parametrize("provider", ["openai", "anthropic", "notion"])
async def test_hosted_check_keychain_never_offers_the_operators_key(provider):
    from services.infrastructure.keychain_service import KeychainService

    with (
        patch("services.infrastructure.deployment.is_hosted_deployment", return_value=True),
        patch.object(KeychainService, "get_api_key", return_value="fake-operator-key") as get_key,
    ):
        out = await setup_routes.check_keychain(provider)
    assert out.exists is False
    assert out.message == setup_routes.HOSTED_NO_KEYCHAIN_MESSAGE
    get_key.assert_not_called()


@pytest.mark.asyncio
async def test_hosted_use_keychain_refuses():
    from services.infrastructure.keychain_service import KeychainService

    with (
        patch("services.infrastructure.deployment.is_hosted_deployment", return_value=True),
        patch.object(KeychainService, "get_api_key", return_value="fake-operator-key") as get_key,
    ):
        out = await setup_routes.use_keychain(setup_routes.KeychainUseRequest(provider="openai"))
    assert (out.success, out.valid) == (False, False)
    get_key.assert_not_called()


@pytest.mark.asyncio
async def test_local_check_keychain_still_reads_the_users_own_keychain():
    from services.infrastructure.keychain_service import KeychainService

    with (
        patch("services.infrastructure.deployment.is_hosted_deployment", return_value=False),
        patch.object(KeychainService, "get_api_key", return_value="fake-local-key"),
    ):
        out = await setup_routes.check_keychain("openai")
    assert out.exists is True


@pytest.mark.asyncio
async def test_slack_status_with_no_user_reads_no_system_token():
    service = MagicMock()
    service.get_config = MagicMock(return_value=MagicMock(bot_token="fake-host-bot-token"))
    with patch(
        "services.integrations.slack.config_service.SlackConfigService", return_value=service
    ):
        out = await setup_routes.get_slack_status(SimpleNamespace(state=SimpleNamespace()))
    assert out == {"configured": False, "message": "Not connected"}
    service.get_config.assert_not_called()


@pytest.mark.asyncio
async def test_slack_status_for_a_signed_in_user_reads_their_own():
    service = MagicMock()
    service.get_config = MagicMock(return_value=MagicMock(bot_token="fake-user-bot-token"))
    with patch(
        "services.integrations.slack.config_service.SlackConfigService", return_value=service
    ):
        out = await setup_routes.get_slack_status(
            SimpleNamespace(state=SimpleNamespace(user_id="u-2151"))
        )
    assert out["configured"] is True
    service.get_config.assert_called_once_with("u-2151")


# ── validate-key's GitHub leg: a real check ──


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,valid,message_name",
    [
        (200, True, "KEY_ACCEPTED_MESSAGE"),
        (401, False, "GITHUB_TOKEN_REFUSED_MESSAGE"),
        (403, False, "GITHUB_TOKEN_REFUSED_MESSAGE"),
        (502, False, "KEY_CHECK_COULD_NOT_RUN_MESSAGE"),
        (None, False, "KEY_CHECK_COULD_NOT_RUN_MESSAGE"),
    ],
)
async def test_the_github_token_is_actually_checked(status, valid, message_name):
    from unittest.mock import AsyncMock

    with patch.object(setup_routes, "_github_token_status", new=AsyncMock(return_value=status)):
        out = await setup_routes.validate_api_key(
            setup_routes.ApiKeyValidateRequest(provider="github", api_key="fake-gh-token")
        )
    assert out.valid is valid
    assert out.message == getattr(setup_routes, message_name)
    assert "saved" not in out.message
