"""#2100 — what chat can read from each connector is declared by code, rendered on the
floor's integration lines, and the floor is told never to promise a read not listed.

Web, #1386 scenario C3 on alpha e801b1a309: "what CAN you actually do right now?" offered
"Connect my Notion" as what "would solve" summarizing Notion docs; no chat path reads Notion.
Arch's ruling (issue 2100): a CHAT_READS map beside the readers, rendered per integration
line, an empty entry renders the can't-read sentence, one NEVER rule in the floor addendum.

LAYER: the declaration, the renderer (ConversationalFloor._format_domain_context) and the
addendum text. DENOMINATOR: every connector in the display set; every declared reader symbol.
"""

from unittest.mock import MagicMock

from services.intent_service import capability_legibility as cl
from services.intent_service.conversational_floor import (
    FLOOR_SYSTEM_PROMPT_ADDENDUM,
    ConversationalFloor,
)


def _lines(integrations):
    out = ConversationalFloor(llm_client=MagicMock())._format_domain_context(
        {"integrations": integrations}
    )
    return [line.strip() for line in out.splitlines()]


class TestDeclaration:
    def test_keys_equal_the_integration_display_set(self):
        # A new connector without a declaration fails the build.
        assert set(cl.CHAT_READS) == set(cl.INTEGRATION_DISPLAY)

    def test_every_declared_reader_symbol_resolves(self):
        for key, reads in cl.CHAT_READS.items():
            for read in reads:
                assert cl.reader_symbol_resolves(read.reader), f"{key}: {read.reader}"

    def test_a_bad_symbol_does_not_resolve(self):
        assert (
            cl.reader_symbol_resolves("services.intent_service.capability_legibility:Nope") is False
        )

    def test_notion_declares_no_read(self):
        assert cl.CHAT_READS["notion"] == ()
        assert cl.chat_reads_line("notion") == "connects, but chat can't read your Notion pages yet"


class TestRendering:
    def test_notion_renders_the_cannot_read_line_connected_or_not(self, monkeypatch):
        """Connected or not, where the host offers Notion (staging). On a host that
        doesn't offer it (beta), only an existing binding keeps the line: "connects"
        is false there (Arch 01M8350YSD, issue 2419's class)."""
        from services.integrations.integration_status_service import STAGING_APP_NAME

        line = "- Notion: connects, but chat can't read your Notion pages yet"
        monkeypatch.setenv("FLY_APP_NAME", STAGING_APP_NAME)
        for status in ("active", "inactive"):
            assert line in _lines([{"name": "notion", "status": status}])
        monkeypatch.delenv("FLY_APP_NAME")
        assert line in _lines([{"name": "notion", "status": "active"}])
        assert line not in _lines([{"name": "notion", "status": "inactive"}])

    def test_github_renders_its_reads(self):
        lines = _lines([{"name": "github", "status": "active"}])
        assert "- GitHub: chat reads open issues and their status, one issue by number" in lines
        assert "- Connected integrations: GitHub" in lines  # the #1547 line is unchanged

    def test_summarize_notion_context_carries_the_cannot_read_line(self):
        # The C3 shape: Notion connected, the question is about its content.
        out = ConversationalFloor(llm_client=MagicMock())._format_domain_context(
            {
                "integrations": [
                    {"name": "notion", "status": "active"},
                    {"name": "github", "status": "active"},
                ],
            }
        )
        assert "Notion: connects, but chat can't read your Notion pages yet" in out


class TestPromptRule:
    def test_addendum_carries_the_never_rule(self):
        assert "NEVER suggest connecting" in FLOOR_SYSTEM_PROMPT_ADDENDUM
        assert "unless that" in FLOOR_SYSTEM_PROMPT_ADDENDUM
        assert "What chat reads from each integration" in FLOOR_SYSTEM_PROMPT_ADDENDUM
