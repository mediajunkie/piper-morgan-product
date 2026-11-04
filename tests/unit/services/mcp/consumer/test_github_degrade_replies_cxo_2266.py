"""CXO 2026-11-04 13:26 (#2266, #2188): the two GitHub degrades a person may read ALONE
each name the way on. The store-failed line changed in place (nothing composes with
it); the stale line is a standalone constant rendered through ``github_degrade_reply``
by the five chat sites and the Settings error, while the sentences that compose with
the short stale phrase (standup, Radar, the default-repo check) are unchanged.
"""

import ast
from pathlib import Path

from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import (
    CREDENTIAL_STORE_FAILED_MESSAGE,
    GITHUB_STALE_TOKEN_REPLY,
    GitHubMCPSpatialAdapter,
    github_degrade_reply,
)

REPO = Path(__file__).resolve().parents[5]


class TestCxosTwoLines:
    def test_the_store_failed_line_by_text(self):
        assert CREDENTIAL_STORE_FAILED_MESSAGE == (
            "I couldn't read your GitHub connection just now, so I haven't checked GitHub. "
            "Try again in a moment. If it keeps failing, reconnect GitHub in Settings, under Integrations."
        )

    def test_the_stale_line_by_text(self):
        assert GITHUB_STALE_TOKEN_REPLY == (
            "Your GitHub connection needs re-authorizing. Reconnect GitHub in Settings, under Integrations."
        )

    async def test_a_stale_degrade_read_alone_gets_the_way_on(self):
        d = await GitHubMCPSpatialAdapter().degrade(DegradationReason.STALE_TOKEN)
        assert (
            d.user_message == "Your GitHub connection needs re-authorizing."
        )  # the composable phrase
        assert github_degrade_reply(d) == GITHUB_STALE_TOKEN_REPLY

    async def test_other_reasons_keep_their_message(self):
        for reason in (DegradationReason.CONNECT_REQUIRED, DegradationReason.MISCONFIGURED):
            d = await GitHubMCPSpatialAdapter().degrade(reason)
            assert github_degrade_reply(d) == d.user_message

    def test_the_store_failed_degrade_reads_the_new_line_unchanged(self):
        d = DegradationResponse(
            reason=DegradationReason.UNREACHABLE, user_message=CREDENTIAL_STORE_FAILED_MESSAGE
        )
        assert github_degrade_reply(d) == CREDENTIAL_STORE_FAILED_MESSAGE


class TestTheStandaloneRendersUseTheHelper:
    def test_no_chat_site_renders_a_github_degrade_message_raw(self):
        src = (REPO / "services/intent/intent_service.py").read_text()
        assert "message=connector_result.degradation.user_message" not in src
        assert src.count("github_degrade_reply(connector_result.degradation)") == 5

    def test_the_settings_repositories_error_uses_the_helper(self):
        src = (REPO / "web/api/routes/settings_integrations.py").read_text()
        assert "detail=github_degrade_reply(connector_result.degradation)" in src
        assert "detail=connector_result.degradation.user_message" not in src

    def test_the_composers_still_take_the_short_phrase(self):
        """The default-repo check composes its own sentence from the short phrase; it is
        not routed through the helper and its wording is CXO's 10-30 line."""
        src = (REPO / "services/intent/intent_service.py").read_text()
        assert "Your GitHub connection needs re-authorizing, so I couldn't check" in src
        tree = ast.parse(src)
        assert tree  # parses: the sed left the module whole
