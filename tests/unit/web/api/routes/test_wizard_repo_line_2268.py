"""#2268: the setup wizard never implies Piper can read a repo it isn't connected to.

Beta session 11-04: the wizard recorded a repo for a project without connecting
GitHub, and Piper then spoke as if it could reach it. Arch's rule (11-04): a repo
name on a project is not a connection. CXO's words (11-04): the not-connected line,
until the wizard itself leads into connect; the linked line when GitHub is connected.

LAYER: the line builder with the status read replaced at its one seam, and the route
function with the database and the builder replaced. Not a render: the wizard page
showing the line is Web's served quote.
DENOMINATOR: the five connection states, a repo given or not, the script's source pin.
"""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from web.api.routes import setup

pytestmark = pytest.mark.unit

REPO = "owner/backend-api"
NOT_CONNECTED = (
    "I've noted owner/backend-api for this project. GitHub isn't connected yet, so I can't "
    "read it. Connect GitHub in Settings, under Integrations."
)
LINKED = "owner/backend-api is linked to this project."


def _status(**over):
    base = {
        "configured": False,
        "check_failed": False,
        "via": None,
        "healthy": None,
        "last_check": None,
        "last_error": None,
    }
    return {**base, **over}


async def _line(state=None, raises=False):
    target = "services.integrations.integration_status_service.IntegrationStatusService.get_status"
    mock = AsyncMock(side_effect=RuntimeError("down")) if raises else AsyncMock(return_value=state)
    with patch(target, mock):
        line = await setup._wizard_repo_line("user-1", REPO)
    assert mock.await_args.args[-2:] == ("user-1", "github")
    return line


class TestTheLineFollowsTheConnection:
    async def test_not_connected_says_cxos_line(self):
        assert await _line(_status()) == NOT_CONNECTED

    async def test_connected_says_it_is_linked(self):
        state = _status(configured=True, via="oauth_binding", healthy=True)
        assert await _line(state) == LINKED

    async def test_connected_and_never_tested_still_reads_as_linked(self):
        assert await _line(_status(configured=True, via="pat", healthy=None)) == LINKED

    async def test_a_rejected_grant_says_nothing(self):
        """Connected but GitHub has rejected it: "isn't connected yet" and "is linked"
        would both be untrue, so the wizard says neither."""
        state = _status(configured=True, via="oauth_binding_stale", healthy=False)
        assert await _line(state) == ""

    async def test_a_failed_check_says_nothing(self):
        assert await _line(_status(check_failed=True)) == ""
        assert await _line(raises=True) == ""


def _claims(user_id):
    return SimpleNamespace(sub=user_id)


async def _create(github_repo, line="LINE"):
    user_id = str(uuid4())
    project = MagicMock()
    project.id = str(uuid4())
    builder = AsyncMock(return_value=line)
    with (
        patch("web.api.routes.setup.AsyncSessionFactory") as factory,
        patch("services.database.repositories.ProjectRepository") as project_repo,
        patch("services.database.repositories.RepositoryRepository") as repo_repo,
        patch("services.connectors.config_service.ConnectorConfigService") as cfg,
        patch(
            "services.infrastructure.github_repo_validator.validate_github_repo_for_account",
            AsyncMock(return_value=SimpleNamespace(validated=False, exists=False, error=None)),
        ),
        patch("services.infrastructure.github_repo_validator.apply_validation_metadata"),
        patch("web.api.routes.setup._wizard_repo_line", builder),
    ):
        ctx = AsyncMock()
        ctx.__aenter__ = AsyncMock(return_value=AsyncMock())
        ctx.__aexit__ = AsyncMock(return_value=None)
        factory.session_scope_fresh.return_value = ctx
        project_repo.return_value.create = AsyncMock(return_value=project)
        repo_repo.return_value.create_repository = AsyncMock(return_value=MagicMock(id="r1"))
        repo_repo.return_value.link_to_project = AsyncMock()
        cfg.return_value.get_default_repo_source = AsyncMock(return_value=None)
        cfg.return_value.set_default_repo = AsyncMock()
        req = setup.SetupProjectRequest(
            user_id=user_id, project_name="Backend", github_repo=github_repo
        )
        result = await setup.create_setup_project(req, _claims(user_id))
    return result, builder, user_id


class TestTheRouteCarriesTheLine:
    async def test_a_project_with_a_repo_returns_the_line_for_that_person(self):
        result, builder, user_id = await _create(f"  {REPO} ")
        assert result.success is True
        assert result.repo_line == "LINE"
        builder.assert_awaited_once_with(user_id, REPO)

    async def test_a_project_with_no_repo_has_no_line_and_reads_no_status(self):
        result, builder, _ = await _create(None)
        assert result.success is True
        assert result.repo_line == ""
        builder.assert_not_awaited()


def test_the_wizard_shows_the_line_as_text_under_the_project():
    src = (Path(__file__).resolve().parents[5] / "web/static/js/setup.js").read_text()
    assert "repoLine: data.repo_line || ''" in src
    assert "${escapeText(p.repoLine)}" in src
    # What the person typed is shown as text, never as markup.
    assert "<strong>${escapeText(p.name)}</strong>" in src
    assert "${escapeText(p.repo)}</span>" in src


def test_copy_rules_hold():
    for line in (NOT_CONNECTED, LINKED):
        assert "alpha" not in line.lower() and "#" not in line
