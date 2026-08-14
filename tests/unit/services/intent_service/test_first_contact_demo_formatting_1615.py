"""#1615 (formatting half): the first-contact demo block must render as a
real list, not a run-on line.

PM's 08-13 retest screenshot: the demo rendered as one paragraph —
``"95 open items, most recently active: • #109 … • #108 …"`` — literal
bullet glyphs inside flowing prose.

Root cause, layer named: the chat frontend renders success messages through
``marked.parse`` (``web/assets/bot-message-renderer.js:66``) with default
options, so a single ``\\n`` inside a paragraph collapses to a space.
``render_first_contact_block`` joined ``•``-prefixed lines with single
newlines — markdown-invisible line breaks. The fix emits actual markdown
list syntax (``- `` items, blank line before the list) that marked turns
into ``<ul><li>`` rows.

Two surfaces pinned here:
1. ``render_first_contact_block`` — the deterministic canonical-greeting
   block (the surface in PM's screenshot).
2. ``ConversationalFloor._format_domain_context`` — the floor path hands the
   same items to the LLM; its directive must tell the model to present them
   as a markdown bullet list so the composed reply doesn't recreate the
   run-on.

The day-part / elapsed-focus-time half of #1615 is NOT covered here — it is
#1572-gated (needs the user's clock) and deliberately not built.
"""

import re

from services.intent_service.conversational_floor import ConversationalFloor
from services.intent_service.first_contact import render_first_contact_block

DEMO_PAYLOAD = {
    "connector": "github",
    "repo": "acme/rocket",
    "items": [
        {
            "number": 123,
            "title": "Fix the login flow",
            "type": "issue",
            "recency": "updated today",
            "url": "https://github.com/acme/rocket/issues/123",
        },
        {
            "number": 456,
            "title": "Add CSV export",
            "type": "pr",
            "recency": "updated 3 days ago",
            "url": "https://github.com/acme/rocket/pull/456",
        },
    ],
    "open_count": 12,
}


class TestRenderedBlockIsMarkdownList:
    def test_exact_markdown_block_for_known_payload(self):
        """The input→output pin: known items produce this exact markdown."""
        block = render_first_contact_block(DEMO_PAYLOAD)
        assert block == (
            "Here's what I can already see in acme/rocket — the GitHub repo "
            "you've connected: 12 open items, most recently active:\n"
            "\n"
            '- #123 "Fix the login flow" (issue, updated today)\n'
            '- #456 "Add CSV export" (PR, updated 3 days ago)\n'
            "\n"
            "Want me to dig into any of these?"
        )

    def test_no_bullet_glyphs_anywhere(self):
        """The literal ``•`` glyph is what survived into PM's screenshot —
        it must not appear in the rendered block at all."""
        assert "•" not in render_first_contact_block(DEMO_PAYLOAD)

    def test_each_item_is_its_own_markdown_list_line(self):
        block = render_first_contact_block(DEMO_PAYLOAD)
        item_lines = [ln for ln in block.split("\n") if ln.startswith("- ")]
        assert len(item_lines) == len(DEMO_PAYLOAD["items"])
        for it in DEMO_PAYLOAD["items"]:
            assert any(f"#{it['number']}" in ln for ln in item_lines)

    def test_blank_line_precedes_list_so_marked_breaks_it_out(self):
        """Markdown only starts a list after a paragraph break. Without the
        blank line, marked folds the ``- `` lines back into the intro
        paragraph — the exact run-on being fixed. Layer named: this test
        asserts the markdown SOURCE shape; the HTML render is marked's
        contract, exercised by the frontend, not simulated here."""
        block = render_first_contact_block(DEMO_PAYLOAD)
        first_item = block.index("- #")
        assert "\n\n" in block[:first_item], (
            "no paragraph break before the list — marked will render a run-on"
        )
        # And the closing question must not glue onto the last list item.
        assert re.search(r"\n\nWant me to dig", block)

    def test_single_item_uses_singular_noun_and_still_lists(self):
        payload = {
            "repo": "acme/rocket",
            "items": [DEMO_PAYLOAD["items"][0]],
            "open_count": 1,
        }
        block = render_first_contact_block(payload)
        assert "1 open item," in block
        assert "\n- #123" in block

    def test_empty_payload_still_renders_nothing(self):
        assert render_first_contact_block(None) == ""
        assert render_first_contact_block({}) == ""
        assert render_first_contact_block({"repo": "r", "items": []}) == ""


class TestFloorDirectiveAsksForAList:
    def test_directive_instructs_markdown_bullet_list(self):
        """The floor reply is LLM-composed; the directive (the only lever at
        this layer) must tell the model to present the items as a bullet
        list, one per line — otherwise it mirrors the prompt's inline shape
        into the same run-on."""
        block = ConversationalFloor()._format_domain_context(
            {"first_contact_demo": DEMO_PAYLOAD}
        )
        assert "bullet list" in block.lower()
        assert "one item per line" in block.lower()

    def test_directive_and_entities_still_present(self):
        """The #1536 guarantees this rides on are untouched."""
        block = ConversationalFloor()._format_domain_context(
            {"first_contact_demo": DEMO_PAYLOAD}
        )
        assert "acme/rocket" in block
        assert "#123" in block and "#456" in block
        assert "ONLY" in block
