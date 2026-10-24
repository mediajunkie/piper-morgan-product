"""#2151: local_git_status_query declines on a hosted server and when the read fails.

The handler reads the SERVER's working tree. On a hosted deployment that is the host's
repository presented as the user's (a substituted read); alpha's image has no ``.git``
(``.dockerignore``), so alpha only ever served the raw error line ("I couldn't read the
local git state: … the server's working directory …"), code vocabulary. CXO (10-23 18:12):
decline plainly and offer GitHub. Arch (18:23): decide "hosted" by the deployment signal,
never by probing for a tree (a probe fails open).

LAYER: unit, the real handler with the deployment signal and the inspector controlled.
DENOMINATOR: hosted, local-unreadable, local-readable, and the signal's three inputs.
"""

from unittest.mock import patch

import pytest

from services.infrastructure.deployment import is_hosted_deployment
from services.intent.intent_service import LOCAL_GIT_DECLINE_LINE


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def service():
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier

    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _intent():
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    return Intent(category=IntentCategory.QUERY, action="local_git_status_query", confidence=1.0)


def _status(**kw):
    from services.integrations.local_git.inspector import LocalGitStatus

    base = dict(current_branch="main", is_clean=True, uncommitted_files_count=0)
    base.update(kw)
    return LocalGitStatus(**base)


@pytest.mark.asyncio
async def test_hosted_declines_without_reading_the_servers_tree(service):
    with (
        patch("services.infrastructure.deployment.is_hosted_deployment", return_value=True),
        patch("services.integrations.local_git.LocalGitInspector.get_status") as read,
    ):
        result = await service._handle_local_git_status_query(_intent(), "wf")
    assert result.message == LOCAL_GIT_DECLINE_LINE
    read.assert_not_called()
    assert "server" not in result.message


@pytest.mark.asyncio
async def test_a_local_install_whose_read_fails_gets_the_plain_decline(service):
    with (
        patch("services.infrastructure.deployment.is_hosted_deployment", return_value=False),
        patch(
            "services.integrations.local_git.LocalGitInspector.get_status",
            return_value=_status(error="not a git repository"),
        ),
    ):
        result = await service._handle_local_git_status_query(_intent(), "wf")
    assert result.message == LOCAL_GIT_DECLINE_LINE
    assert "not a git repository" not in result.message


@pytest.mark.asyncio
async def test_a_local_checkout_still_reports_its_branch(service):
    with (
        patch("services.infrastructure.deployment.is_hosted_deployment", return_value=False),
        patch(
            "services.integrations.local_git.LocalGitInspector.get_status",
            return_value=_status(),
        ),
    ):
        result = await service._handle_local_git_status_query(_intent(), "wf")
    assert "You're on **`main`**" in result.message


def test_the_hosted_signal_reads_fly_and_production(monkeypatch):
    monkeypatch.delenv("FLY_APP_NAME", raising=False)
    monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)
    with patch("services.infrastructure.deployment.os.path.exists", return_value=False):
        assert is_hosted_deployment() is False
        monkeypatch.setenv("FLY_APP_NAME", "piper-morgan")
        assert is_hosted_deployment() is True
        monkeypatch.delenv("FLY_APP_NAME")
        monkeypatch.setenv("PIPER_ENVIRONMENT", "production")
        assert is_hosted_deployment() is True
    with patch("services.infrastructure.deployment.os.path.exists", return_value=True):
        monkeypatch.delenv("PIPER_ENVIRONMENT")
        assert is_hosted_deployment() is True
