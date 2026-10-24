"""#2151 (Arch 10-24 12:32, gap 2): Slack's one credential resolver reads the user's
tokens with provenance, and the host's env/PIPER.user.md layers never override a user's
own token on a hosted deploy.

- a credential store that failed to answer RAISES (it read as an empty token, so "not
  connected", and the recent-activity Slack legs took it as not performed);
- hosted: SLACK_BOT_TOKEN / SLACK_USER_TOKEN env are ignored; only the user's own
  keychain token counts; local installs keep all four layers.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from services.infrastructure.keychain_service import SecretProvenance, SecretRead
from services.integrations.slack.config_service import (
    SlackConfigService,
    SlackCredentialReadFailed,
)

USER = "u-slack-2151"


def _keychain(reads):
    kc = MagicMock()
    kc.read_secret = lambda provider, username=None: reads.get(
        provider, SecretRead(SecretProvenance.VERIFIED_ABSENT)
    )
    kc.get_api_key = MagicMock(return_value=None)  # app credentials (client id/secret)
    return kc


def _config(reads, *, env=None, hosted=False):
    with (
        patch.dict(os.environ, env or {}, clear=True),
        patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=_keychain(reads),
        ),
        patch("services.infrastructure.deployment.is_hosted_deployment", return_value=hosted),
        patch.object(SlackConfigService, "_load_from_user_config", return_value={}),
    ):
        return SlackConfigService().get_config(user_id=USER)


def test_a_store_that_failed_raises_never_an_empty_token():
    reads = {"slack_bot": SecretRead(SecretProvenance.STORE_FAILED, error="timeout")}
    with pytest.raises(SlackCredentialReadFailed):
        _config(reads)


def test_hosted_ignores_the_host_env_token():
    cfg = _config(
        {},
        env={"SLACK_BOT_TOKEN": "fake-host-bot", "SLACK_USER_TOKEN": "fake-host-user"},
        hosted=True,
    )
    assert cfg.bot_token == "" and cfg.user_token == ""


def test_hosted_uses_the_users_own_keychain_token():
    reads = {"slack_bot": SecretRead(SecretProvenance.PRESENT, value="fake-user-bot")}
    cfg = _config(reads, env={"SLACK_BOT_TOKEN": "fake-host-bot"}, hosted=True)
    assert cfg.bot_token == "fake-user-bot"


def test_local_keeps_the_env_layer():
    cfg = _config({}, env={"SLACK_BOT_TOKEN": "fake-local-bot"}, hosted=False)
    assert cfg.bot_token == "fake-local-bot"


@pytest.mark.asyncio
async def test_a_store_failure_arms_the_activity_flag_not_not_performed():
    """The DM leg's no-token guard used to read a store failure as "not connected"."""
    from services.intent_service.context_assembler import (
        ContextAssembler,
        _SlackReadFailed,
    )

    service = MagicMock()
    service.get_config = MagicMock(side_effect=SlackCredentialReadFailed("fake"))
    with patch(
        "services.integrations.slack.config_service.SlackConfigService", return_value=service
    ):
        with pytest.raises(_SlackReadFailed):
            await ContextAssembler()._fetch_slack_activity_items(USER)
