"""#2284 (Arch 2026-11-05 06:28): a host that doesn't offer a connector reads no stored
credential for it on any use path, so every reader sees "not connected".

Slack is gated once, at ``SlackConfigService.get_config``; the socket runner's start and
the Settings "Test" button are gated through the same offered check. Notion's two
user-secret reads (the async key read and the keychain fallback) check the offered set
too. The slot ratchet pins which modules may name the Slack slots in a call at all.
"""

import ast
import asyncio
import subprocess
from pathlib import Path

import pytest

from services.integrations import integration_status_service as iss
from services.integrations.slack.config_service import SlackConfig, SlackConfigService

REPO = Path(__file__).resolve().parents[4]


@pytest.fixture
def slack_offered(monkeypatch):
    monkeypatch.setitem(iss.BETA_OFFERED_CONNECTORS, "slack", "Slack")


@pytest.fixture
def not_staging(monkeypatch):
    monkeypatch.delenv("FLY_APP_NAME", raising=False)


def _service_with(bot="xoxb-stored", user="xoxp-stored"):
    svc = SlackConfigService()
    svc._config_cache["u1"] = SlackConfig(bot_token=bot, user_token=user)
    return svc


class TestSlackGetConfigGate:
    def test_not_offered_returns_no_tokens(self, not_staging):
        assert not iss.connector_offered("slack")
        cfg = _service_with().get_config("u1")
        assert cfg.bot_token == "" and cfg.user_token == ""

    def test_not_offered_leaves_the_cache_intact(self, not_staging):
        svc = _service_with()
        svc.get_config("u1")
        assert svc._config_cache["u1"].bot_token == "xoxb-stored"

    def test_offered_returns_the_stored_tokens(self, slack_offered):
        cfg = _service_with().get_config("u1")
        assert cfg.bot_token == "xoxb-stored" and cfg.user_token == "xoxp-stored"


class TestSocketRunnerStartGate:
    def test_not_offered_builds_no_runner(self, monkeypatch, not_staging):
        from services.integrations.slack import socket_mode_runner as smr

        monkeypatch.setenv("PIPER_SLACK_INBOUND_ENABLED", "true")
        monkeypatch.setenv("SLACK_APP_TOKEN", "xapp-test")

        async def _boom():
            raise AssertionError("bound-user lookup ran on a host that doesn't offer Slack")

        monkeypatch.setattr(smr, "_resolve_bound_user", _boom)
        assert asyncio.run(smr.build_runner(intent_service=None)) is None


class TestSlackTestButton:
    def test_not_offered_reads_as_not_connected(self, monkeypatch, not_staging):
        from services.infrastructure import keychain_service as kc
        from web.api.routes import integrations as routes

        slot_reads = []

        def _record(self, name, *a, **k):
            slot_reads.append(name)
            return ""

        monkeypatch.setattr(kc.KeychainService, "get_api_key", _record)
        monkeypatch.setattr(
            SlackConfigService,
            "_load_config",
            lambda self, user_id: SlackConfig(bot_token="xoxb-stored"),
        )
        out = asyncio.run(routes._test_slack(user_id="u1"))
        assert out["success"] is False and out["error_type"] == "not_configured"
        assert "slack_bot" not in slot_reads, "the Test button read the slot directly"


class _KeyService:
    def __init__(self):
        self.calls = 0

    async def retrieve_user_key(self, session, user_id, provider):
        self.calls += 1
        return "secret_notion"


class _Scope:
    def __call__(self):
        return self

    async def __aenter__(self):
        return object()

    async def __aexit__(self, *a):
        return False


def _notion(key_service):
    from services.integrations.notion.config_service import NotionConfigService

    svc = NotionConfigService()
    svc._user_key_service = key_service
    svc._session_scope = _Scope()
    return svc


class TestNotionUserKeyGate:
    def test_not_offered_reads_nothing(self, not_staging):
        ks = _KeyService()
        assert asyncio.run(_notion(ks).aget_user_api_key("u1")) is None
        assert ks.calls == 0

    def test_offered_on_staging_reads_the_key(self, monkeypatch):
        monkeypatch.setenv("FLY_APP_NAME", iss.STAGING_APP_NAME)
        ks = _KeyService()
        assert asyncio.run(_notion(ks).aget_user_api_key("u1")) == "secret_notion"
        assert ks.calls == 1

    def test_not_offered_skips_the_keychain_fallback(self, monkeypatch, not_staging):
        from services.infrastructure import keychain_service as kc
        from services.integrations.notion import config_service as ncs

        monkeypatch.delenv("NOTION_API_KEY", raising=False)
        reads = []

        # Record rather than raise: the fallback swallows any exception it hits.
        def _record(self, name, *a, **k):
            reads.append(name)
            return "secret_from_keychain"

        monkeypatch.setattr(kc.KeychainService, "get_api_key", _record)
        monkeypatch.setattr(ncs, "_hosted", lambda: False)
        svc = ncs.NotionConfigService()
        monkeypatch.setattr(svc, "_load_from_user_config", lambda: {})
        assert svc._load_config("u1").api_key == ""
        assert "notion" not in reads


#: Every module that may name a Slack credential slot in a call. Use-path readers go
#: through SlackConfigService.get_config; the rest are Arch's named exceptions.
ALLOWED_SLACK_SLOT_MODULES = {
    "services/integrations/slack/config_service.py",  # the one gated use-path read
    "services/integrations/slack/oauth_handler.py",  # the writer
    "services/connectors/disconnect.py",  # revoke and clear
    "services/integrations/integration_status_service.py",  # existence only
    "services/integrations/slack/socket_mode_runner.py",  # start gated on the offered set
}
SLACK_SLOTS = {"slack_bot", "slack_user"}


def _modules_naming_a_slack_slot():
    files = subprocess.run(
        ["git", "ls-files", "services", "web", "cli"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    found = set()
    for rel in files:
        if not rel.endswith(".py"):
            continue
        tree = ast.parse((REPO / rel).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                args = list(node.args) + [k.value for k in node.keywords]
                if any(isinstance(a, ast.Constant) and a.value in SLACK_SLOTS for a in args):
                    found.add(rel)
            elif isinstance(node, (ast.Tuple, ast.List)) and any(
                isinstance(e, ast.Constant) and e.value in SLACK_SLOTS for e in node.elts
            ):
                found.add(rel)
    return found


class TestSlackSlotRatchet:
    def test_no_new_module_reads_the_slack_slots(self):
        extra = _modules_naming_a_slack_slot() - ALLOWED_SLACK_SLOT_MODULES
        assert not extra, (
            f"{sorted(extra)} name a Slack credential slot. Read the token through "
            "SlackConfigService.get_config, which is gated on the offered set (#2284)."
        )

    def test_the_allow_list_holds_no_stale_entries(self):
        stale = ALLOWED_SLACK_SLOT_MODULES - _modules_naming_a_slack_slot()
        assert not stale, f"{sorted(stale)} no longer name a slot; drop them from the list."
