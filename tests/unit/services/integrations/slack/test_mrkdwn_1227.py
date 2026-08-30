"""#1227 — GitHub-flavored markdown → Slack mrkdwn converter tests."""

from __future__ import annotations

from services.integrations.slack.mrkdwn import markdown_to_mrkdwn


class TestBold:
    def test_double_star_bold(self):
        assert markdown_to_mrkdwn("**bold**") == "*bold*"

    def test_double_underscore_bold(self):
        assert markdown_to_mrkdwn("__bold__") == "*bold*"

    def test_bold_inline_in_sentence(self):
        assert markdown_to_mrkdwn("a **b** c") == "a *b* c"


class TestItalic:
    def test_single_star_italic_to_underscore(self):
        assert markdown_to_mrkdwn("*italic*") == "_italic_"

    def test_underscore_italic_unchanged(self):
        assert markdown_to_mrkdwn("_italic_") == "_italic_"

    def test_bold_and_italic_same_line_no_crosstalk(self):
        # The ordering hazard: bold must not become italic, italic must not stay starred.
        assert markdown_to_mrkdwn("**b** and *i*") == "*b* and _i_"


class TestHeaders:
    def test_h1_to_bold_line(self):
        assert markdown_to_mrkdwn("# Title") == "*Title*"

    def test_h3_to_bold_line(self):
        assert markdown_to_mrkdwn("### Sub") == "*Sub*"

    def test_header_not_reconverted_to_italic(self):
        # header → *Title* must NOT then be turned into _Title_ by the italic pass
        assert markdown_to_mrkdwn("## Status") == "*Status*"


class TestLists:
    def test_dash_bullet(self):
        assert markdown_to_mrkdwn("- one") == "• one"

    def test_star_bullet_not_italic(self):
        # a list `* item` must become a bullet, not be read as emphasis
        assert markdown_to_mrkdwn("* one") == "• one"

    def test_plus_bullet(self):
        assert markdown_to_mrkdwn("+ one") == "• one"

    def test_indented_bullet_preserves_indent(self):
        assert markdown_to_mrkdwn("  - nested") == "  • nested"


class TestLinks:
    def test_link_to_slack_format(self):
        assert markdown_to_mrkdwn("[Piper](https://x.io)") == "<https://x.io|Piper>"


class TestCodePreserved:
    def test_inline_code_untouched(self):
        # markdown chars inside inline code must NOT be converted
        assert markdown_to_mrkdwn("use `**not bold**` here") == "use `**not bold**` here"

    def test_code_block_untouched(self):
        src = "```\n# not a header\n**not bold**\n```"
        assert markdown_to_mrkdwn(src) == src


class TestSafeOnPlainText:
    def test_plain_unchanged(self):
        assert markdown_to_mrkdwn("just some words") == "just some words"

    def test_empty(self):
        assert markdown_to_mrkdwn("") == ""

    def test_already_mrkdwn_bullets_and_links_stable(self):
        # bullets/links/italic are stable on re-apply (only bold *x* is not, by design)
        s = "• one\n<https://x.io|Piper>\n_italic_"
        assert markdown_to_mrkdwn(s) == s


class TestIssueExample:
    def test_full_example(self):
        src = "**Top priority:** finish #1227\n# Sprint status\n- item one"
        out = markdown_to_mrkdwn(src)
        assert out == "*Top priority:* finish #1227\n*Sprint status*\n• item one"


class TestSendMessageSeamConverts:
    """#1227 Phase 2: slack_client.send_message normalizes text to mrkdwn — the
    single chokepoint response_handler routes through (simple_response_handler
    did too, until its disposal — 2026-08-30 census disposal Batch 3).
    Outgoing Slack text must contain mrkdwn (*bold*), not raw markdown (**bold**)."""

    async def test_send_message_converts_text_to_mrkdwn(self):
        from unittest.mock import MagicMock

        from services.integrations.slack.slack_client import SlackClient

        captured: dict = {}

        async def _capture(method, endpoint, data):
            captured["data"] = data
            return MagicMock(success=True)

        client = SlackClient(config_service=MagicMock(), user_id="u1")
        client._make_request = _capture

        await client.send_message(channel="C1", text="**bold** and *i*\n# H")

        # the payload posted to chat.postMessage carries converted mrkdwn
        assert captured["data"]["text"] == "*bold* and _i_\n*H*"
        assert "**" not in captured["data"]["text"]
