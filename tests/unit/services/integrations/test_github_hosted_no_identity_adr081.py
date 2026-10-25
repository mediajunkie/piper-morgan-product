"""ADR-081 D2: a hosted deploy has no GitHub identity of its own.

On a hosted deploy ``get_authentication_token("system")`` answers None by construction,
whatever the env token names or a "system" keychain row hold. A local install keeps them
(the operator is the user). A real user's own token is untouched by the gate.
"""

from unittest.mock import MagicMock, patch

from services.infrastructure.keychain_service import SecretProvenance, SecretRead
from services.integrations.github.config_service import GitHubConfigService

HOSTED = "services.infrastructure.deployment.is_hosted_deployment"


def _keychain(value):
    kc = MagicMock()
    kc.get_api_key.return_value = value
    kc.read_secret.return_value = (
        SecretRead(SecretProvenance.PRESENT, value=value)
        if value
        else SecretRead(SecretProvenance.VERIFIED_ABSENT)
    )
    return patch("services.infrastructure.keychain_service.KeychainService", return_value=kc)


def test_hosted_system_gets_no_token_from_env_or_keychain():
    with (
        patch(HOSTED, return_value=True),
        patch.dict("os.environ", {"GITHUB_TOKEN": "fake-token-env"}, clear=False),
        _keychain("fake-token-system-row"),
    ):
        svc = GitHubConfigService()
        assert svc.get_authentication_token("system") is None
        assert svc.is_configured("system") is False


def test_local_system_keeps_the_env_token():
    with (
        patch(HOSTED, return_value=False),
        patch.dict("os.environ", {"GITHUB_TOKEN": "fake-token-env"}, clear=False),
        _keychain(None),
    ):
        assert GitHubConfigService().get_authentication_token("system") == "fake-token-env"


def test_the_hosted_gate_is_read_at_call_time_not_cached():
    svc = GitHubConfigService()
    with (
        patch.dict("os.environ", {"GITHUB_TOKEN": "fake-token-env"}, clear=False),
        _keychain(None),
    ):
        with patch(HOSTED, return_value=True):
            assert svc.get_authentication_token("system") is None
        with patch(HOSTED, return_value=False):
            assert svc.get_authentication_token("system") == "fake-token-env"


def test_a_real_users_own_token_is_untouched_by_the_gate():
    with (
        patch(HOSTED, return_value=True),
        patch.dict("os.environ", {"GITHUB_TOKEN": "fake-token-env"}, clear=False),
        _keychain("fake-token-user"),
    ):
        uid = "694d8f4e-0000-0000-0000-000000000042"
        assert GitHubConfigService().get_authentication_token(uid) == "fake-token-user"
