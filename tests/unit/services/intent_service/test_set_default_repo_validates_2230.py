"""#2230: the chat setter validates owner/name against the user's own GitHub account
before it writes the default. One pin per outcome; a failed read is never "not found"
(#2151) and nothing is written on any non-"exists" outcome.

Layer: the handler with the validator and the config writer mocked. No live GitHub call.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.infrastructure.github_repo_validator import RepoValidationResult
from services.intent.intent_service import IntentService
from services.shared_types import IntentCategory

_MSG = "set my default repo to mediajunkie/piper-morgan-product"
_VALIDATOR = "services.infrastructure.github_repo_validator.validate_github_repo_for_account"


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


async def _run(intent_service, validator):
    intent = Intent(
        category=IntentCategory.QUERY,
        action="set_default_repo",
        original_message=_MSG,
        context={"original_message": _MSG, "user_id": "user-123"},
    )
    writer = MagicMock()
    writer.set_default_repo = AsyncMock()
    with (
        patch(_VALIDATOR, validator),
        patch("services.connectors.config_service.ConnectorConfigService", return_value=writer),
        patch("services.database.session_factory.AsyncSessionFactory.session_scope") as scope,
    ):
        scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
        scope.return_value.__aexit__ = AsyncMock(return_value=False)
        result = await intent_service._handle_set_default_repo(intent, "wf-1")
    return result, writer


def _res(**kw):
    return AsyncMock(return_value=RepoValidationResult(**kw))


@pytest.mark.asyncio
async def test_exists_writes_and_confirms(intent_service):
    v = _res(validated=True, exists=True, accessible=True, status_code=200)
    result, writer = await _run(intent_service, v)
    v.assert_awaited_once_with("mediajunkie/piper-morgan-product", "user-123")
    writer.set_default_repo.assert_awaited_once()
    assert result.success is True
    assert result.message.startswith(
        "Done — your default repo is now **mediajunkie/piper-morgan-product**."
    )
    assert result.intent_data["validation_outcome"] == "exists"


@pytest.mark.asyncio
async def test_not_found_writes_nothing_and_says_so(intent_service):
    v = _res(
        validated=True,
        exists=False,
        accessible=False,
        status_code=404,
        error="Repository 'x' not found on GitHub",
    )
    result, writer = await _run(intent_service, v)
    writer.set_default_repo.assert_not_awaited()
    assert "couldn't find mediajunkie/piper-morgan-product on GitHub" in result.message
    assert "haven't changed your default" in result.message
    assert result.requires_clarification is True
    assert result.intent_data["validation_outcome"] == "not_found"


@pytest.mark.asyncio
async def test_401_is_no_access_and_writes_nothing(intent_service):
    v = _res(
        validated=True,
        exists=False,
        accessible=False,
        status_code=401,
        error="GitHub token is invalid or expired",
    )
    result, writer = await _run(intent_service, v)
    writer.set_default_repo.assert_not_awaited()
    assert (
        "Your GitHub connection needs re-authorizing, so I couldn't check "
        "mediajunkie/piper-morgan-product and haven't changed your default." in result.message
    )
    assert "Reconnect with GitHub" in result.message
    assert "can't see" not in result.message  # the retired no-access line (CXO 17:4x)
    assert "Settings \u2192 Integrations \u2192 GitHub" in result.message
    assert result.requires_clarification is True
    assert result.intent_data["validation_outcome"] == "no_access"


@pytest.mark.asyncio
async def test_403_writes_nothing_and_says_try_again_not_no_access(intent_service):
    # The validator's 403 branch returns exists=True, accessible=False: never key on exists.
    v = _res(validated=True, exists=True, accessible=False, status_code=403, error="rate limit")
    result, writer = await _run(intent_service, v)
    writer.set_default_repo.assert_not_awaited()
    assert "couldn't check mediajunkie/piper-morgan-product just now" in result.message
    assert "Try again in a moment" in result.message
    assert "needs re-authorizing" not in result.message  # a 403 is not a 401
    assert "can't see" not in result.message
    assert result.success is False
    assert result.intent_data["validation_outcome"] == "not_checked"


@pytest.mark.asyncio
async def test_no_credential_writes_nothing_and_points_to_settings(intent_service):
    v = _res(validated=False, exists=False, accessible=False, not_checked_reason="no_credential")
    result, writer = await _run(intent_service, v)
    writer.set_default_repo.assert_not_awaited()
    assert result.message == (
        "I can't check mediajunkie/piper-morgan-product from here, so I haven't changed "
        "your default. Set it in Settings \u2192 Integrations \u2192 GitHub."
    )
    assert result.intent_data["validation_outcome"] == "no_credential"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "validator",
    [
        _res(validated=False, exists=False, accessible=False, not_checked_reason="network"),
        _res(validated=False, exists=False, accessible=False, not_checked_reason="error"),
        _res(validated=False, exists=False, accessible=False),
        _res(
            validated=True,
            exists=False,
            accessible=False,
            status_code=500,
            error="GitHub API returned status 500",
            not_checked_reason="error",
        ),
        AsyncMock(side_effect=RuntimeError("boom")),
    ],
    ids=["network", "error", "no_reason", "status_500", "exception"],
)
async def test_check_that_did_not_run_writes_nothing_and_says_the_check_failed(
    intent_service, validator
):
    result, writer = await _run(intent_service, validator)
    writer.set_default_repo.assert_not_awaited()
    assert (
        result.message == "I couldn't check mediajunkie/piper-morgan-product just now, so I "
        "haven't changed your default. Try again in a moment."
    )
    assert result.success is False
    assert result.error_type == "set_default_repo_validation_unavailable"
    assert result.intent_data["validation_outcome"] == "not_checked"
