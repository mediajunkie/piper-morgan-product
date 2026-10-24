"""#2151 step 3, ISS-STATUS: a connection check that couldn't run is not "not connected".

Before: ``get_config_status`` swallowed each user-scoped credential lookup's exception
(``except Exception: pass``) and fell through to ``("not_configured", None)``, and the
GitHub binding check returned None (= "no binding") when it raised. So a failed check
read as "not connected" on every surface: the capabilities reply ("No, GitHub isn't
connected"), the floor ("GitHub: not connected", "Connected integrations: none") and the
Settings card ("Not configured"). Arch's ruling (#2151, 6377720778): ``unknown`` is not
``not_configured``. CXO's words (10-23 17:55): the couldn't-check template; the checks
that worked are still shown.

LAYER: unit. The service with the keychain / session forced to raise; the capabilities
handler, the floor renderer and the /health card from the service's result.
DENOMINATOR: the 4 integrations' lookups, the binding check, and the 4 consuming surfaces
(capabilities asked + list, floor identity + GitHub line, /health card).
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.integrations import integration_status_service as iss

_USER = "5a2c9d10-2151-4b00-9e00-00000000bbbb"


def _raise(*a, **k):
    raise RuntimeError("keychain unavailable")


@pytest.fixture(autouse=True)
def _no_env_credentials(monkeypatch):
    for name in (
        "GITHUB_TOKEN",
        "GITHUB_ACCESS_TOKEN",
        "SLACK_BOT_TOKEN",
        "NOTION_API_KEY",
        "NOTION_API_TOKEN",
        "GOOGLE_CALENDAR_CREDENTIALS",
        "MCP_ENABLED",
    ):
        monkeypatch.delenv(name, raising=False)


@pytest.mark.asyncio
class TestTheServiceSaysUnknown:
    @pytest.mark.parametrize("integration", ["github", "slack", "calendar"])
    async def test_a_raising_keychain_lookup_is_unknown(self, integration):
        with patch(
            "services.infrastructure.keychain_service.KeychainService.aread_secret",
            AsyncMock(side_effect=RuntimeError("keychain unavailable")),
        ):
            assert await iss.get_config_status(integration, user_id=_USER) == ("unknown", None)

    @pytest.mark.parametrize("integration", ["github", "slack", "calendar"])
    async def test_a_store_that_failed_to_answer_is_unknown(self, integration):
        """The swallow under the swallow: get_api_key returns None when the store fails
        (timeout, backend error), the same as "absent", so a failed lookup read as "Not
        configured". read_secret's STORE_FAILED says which."""
        from services.infrastructure.keychain_service import SecretProvenance, SecretRead

        with patch(
            "services.infrastructure.keychain_service.KeychainService.aread_secret",
            AsyncMock(return_value=SecretRead(SecretProvenance.STORE_FAILED, error="timeout")),
        ):
            assert await iss.get_config_status(integration, user_id=_USER) == ("unknown", None)

    async def test_a_raising_notion_store_is_unknown(self):
        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            _raise,
        ):
            assert await iss.get_config_status("notion", user_id=_USER) == ("unknown", None)

    async def test_a_lookup_that_ran_and_found_nothing_is_still_not_configured(self):
        from services.infrastructure.keychain_service import SecretProvenance, SecretRead

        with patch(
            "services.infrastructure.keychain_service.KeychainService.aread_secret",
            AsyncMock(return_value=SecretRead(SecretProvenance.VERIFIED_ABSENT)),
        ):
            assert await iss.get_config_status("slack", user_id=_USER) == ("not_configured", None)

    async def test_a_raising_binding_check_is_check_failed_not_no_binding(self):
        with patch("services.database.session_factory.AsyncSessionFactory.session_scope", _raise):
            state = await iss.github_oauth_binding_state(_USER)
        assert state == iss.BINDING_CHECK_FAILED
        with patch.object(iss, "github_oauth_binding_state", AsyncMock(return_value=state)):
            assert await iss.github_oauth_bound(_USER) is False
            assert await iss.github_needs_reconnecting(_USER) is False

    async def test_get_status_carries_check_failed(self):
        with (
            patch.object(
                iss, "github_oauth_binding_state", AsyncMock(return_value=iss.BINDING_CHECK_FAILED)
            ),
            patch.object(
                iss, "get_config_status", AsyncMock(return_value=("not_configured", None))
            ),
        ):
            st = await iss.IntegrationStatusService().get_status(_USER, "github")
        assert st["configured"] is False and st["check_failed"] is True

    async def test_a_verified_absence_is_not_check_failed(self):
        with patch.object(
            iss, "get_config_status", AsyncMock(return_value=("not_configured", None))
        ):
            st = await iss.IntegrationStatusService().get_status(_USER, "slack")
        assert st["configured"] is False and st["check_failed"] is False


def _statuses(**failed):
    out = {}
    for name in iss.KNOWN_INTEGRATIONS:
        if failed.get(name):
            out[name] = {"configured": False, "check_failed": True, "via": None, "healthy": None}
        elif name == "github":
            out[name] = {
                "configured": True,
                "check_failed": False,
                "via": "keychain",
                "healthy": True,
            }
        else:
            out[name] = {"configured": False, "check_failed": False, "via": None, "healthy": None}
    return out


@pytest.mark.asyncio
class TestTheCapabilitiesReply:
    async def _reply(self, message, statuses):
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handlers = CanonicalHandlers()
        with patch.object(
            iss.IntegrationStatusService, "get_all", AsyncMock(return_value=statuses)
        ):
            out = await handlers._format_integration_setup_guidance(
                user_id=_USER, original_message=message
            )
        return out["message"]

    async def test_asked_about_an_unchecked_integration_says_it_couldnt_check(self):
        msg = await self._reply("is slack connected?", _statuses(slack=True))
        assert "I couldn't check Slack just now, so I can't say whether it's connected." in msg
        assert "isn't connected" not in msg

    async def test_the_list_keeps_what_worked_and_names_what_didnt(self):
        msg = await self._reply("what integrations do I have?", _statuses(slack=True))
        assert "GitHub" in msg.split("I couldn't check")[0]  # the working check is shown
        assert "I couldn't check Slack just now, so the list above doesn't include it." in msg
        not_connected = msg.split("Not connected yet:")[-1] if "Not connected yet:" in msg else ""
        assert "Slack" not in not_connected


class TestTheFloorNeverSaysNotConnected:
    def _render(self, ctx):
        from unittest.mock import MagicMock

        from services.intent_service.conversational_floor import ConversationalFloor

        return ConversationalFloor(llm_client=MagicMock())._format_domain_context(ctx)

    def test_an_unchecked_integration_is_not_listed_as_not_connected_and_arms_the_aggregate(self):
        out = self._render(
            {
                "integrations": [
                    {"name": "github", "status": "active"},
                    {"name": "slack", "status": "check_failed"},
                ],
                "integrations_source_failed": True,
            }
        )
        assert "could not check: integrations" in out
        assert "Not connected (available in Settings): Slack" not in out
        assert "- Connected integrations: GitHub" in out

    def test_with_nothing_confirmed_the_floor_never_says_none(self):
        out = self._render(
            {
                "integrations": [{"name": "slack", "status": "check_failed"}],
                "integrations_source_failed": True,
            }
        )
        assert "Connected integrations: none" not in out
        assert "could not check: integrations" in out

    def test_a_failed_github_check_renders_no_not_connected_line(self):
        out = self._render({"integrations_source_failed": True})
        assert "GitHub: not connected" not in out
        assert "could not check: integrations" in out


@pytest.mark.asyncio
async def test_the_health_card_says_the_check_failed_not_not_configured():
    from web.api.routes import integrations as routes

    with patch.object(routes, "_get_integration_config_status", AsyncMock(return_value="unknown")):
        card = await routes._check_integration_health(
            "slack", routes.INTEGRATION_REGISTRY["slack"], user_id=_USER
        )
    assert card.status == "unknown"
    assert card.status_message == routes.CHECK_FAILED_MESSAGE
