"""#1729 — chat document-summarize: nested "Key Findings" list rendered as ONE
run-on bullet with literal "• -" sequences inside it, instead of a real list.

What PM saw (2026-09-08, `summarize <doc>.md` on the default `format=bullet`
path):

    • Issue #1608's liveness check structurally cannot catch #1713's failure
    mode; the two must remain separate checks • - #1608 is a chronic-
    staleness detector ... • - GitHub documents that scheduled workflow runs
    are best-effort ...

Root cause (services/intent_service/document_handlers.py,
``handle_summarize_document``'s ``format == "bullet"`` branch):
``analysis["summary"]`` is always ``DocumentSummary.to_markdown()``'s output
(services/domain/models.py) — it ALWAYS starts with ``"# {title}\\n\\n"``, so
the "already bulleted" guard (``.startswith("•") or .startswith("-")``) never
matched. Every summary — including a fully-formed
``"## Key Findings\\n\\n- item\\n  - subitem\\n"`` — fell through to the
naive re-bulletizer, which splits the WHOLE markdown blob on "." (periods)
with zero regard for block/list boundaries. A nested list item's own newline
and indent survive as literal text mid period-chunk, and get an errant
``"• "`` glued on front — producing exactly the "• -" run-on PM saw.

The fix: use ``has_markdown_formatting`` (services/utils/markdown_formatter.py
— previously written, never wired to a caller) to detect ANY markdown
structure anywhere in the text (not just a leading glyph) and leave already-
structured markdown untouched. The genuine plain-prose fallback (no-LLM /
failure-path summaries like "PDF with N pages...") still gets bulletized, but
now with a REAL markdown "- " marker instead of the Unicode "•" glyph — marked
.parse (web/assets/bot-message-renderer.js) does not recognize "•" as list
syntax, so "•"-prefixed lines were never a list to the renderer: they're
plain text joined by CommonMark soft breaks, which collapse to spaces inside
one paragraph (the same mechanism #1615 fixed at the first-contact demo
site).
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.intent_service import document_handlers

_OWNER = "3f7b8a52-1729-4b00-9e00-000000001729"
_FILE_ID = "aa11bb22-1729-4c00-9e00-000000001729"

# The smallest reproduction: a 2-level markdown list under "Key Findings",
# exactly as DocumentSummary.to_markdown() emits it.
NESTED_FINDINGS_MARKDOWN = (
    "# cio-mechanism-half-recurring-duty-2026-09-04\n\n"
    "**Document Type:** Markdown\n\n"
    "## Key Findings\n\n"
    "- Issue #1608's liveness check structurally cannot catch #1713's "
    "failure mode; the two must remain separate checks.\n"
    "  - #1608 is a chronic-staleness detector for workflows with no "
    "successful run.\n"
    "  - GitHub documents that scheduled workflow runs are best-effort.\n"
    "- Second top-level finding with its own detail.\n"
)


async def _summarize(analysis_summary: str, *, format: str = "bullet"):
    analysis = {
        "file_id": _FILE_ID,
        "filename": "cio-mechanism-half-recurring-duty-2026-09-04.md",
        "summary": analysis_summary,
        "key_findings": [],
        "analyzed_at": "2026-09-08T05:14:00",
    }
    with patch(
        "services.intent_service.document_handlers.handle_analyze_document",
        AsyncMock(return_value=analysis),
    ):
        return await document_handlers.handle_summarize_document(
            file_id=_FILE_ID, format=format, user_id=_OWNER
        )


class TestBulletFormatPreservesStructuredMarkdown:
    @pytest.mark.asyncio
    async def test_nested_key_findings_list_survives_unmangled(self):
        """THE #1729 shape: a real DocumentSummary.to_markdown() summary with
        a nested list under Key Findings must NOT be run through the
        period-split bulletizer at all."""
        result = await _summarize(NESTED_FINDINGS_MARKDOWN)

        # Pre-fix symptom: literal "• -" sequences from a mangled nested item.
        assert "• -" not in result["summary"]
        # The markdown is passed through untouched — headers, structure, and
        # both nested sub-items survive as real list items, not flattened
        # into one paragraph.
        assert result["summary"] == NESTED_FINDINGS_MARKDOWN
        assert "  - #1608 is a chronic-staleness detector" in result["summary"]
        assert "  - GitHub documents that scheduled workflow runs" in result["summary"]
        assert "- Second top-level finding with its own detail." in result["summary"]

    @pytest.mark.asyncio
    async def test_flat_markdown_list_also_survives_unmangled(self):
        """Non-nested case: a flat "## Key Findings\\n- a\\n- b" list must
        also be left alone (regression guard against a fix that only
        special-cases nesting)."""
        flat = "# Doc\n\n## Key Findings\n\n- First finding.\n- Second finding.\n"
        result = await _summarize(flat)
        assert result["summary"] == flat
        assert "•" not in result["summary"]


class TestBulletFormatFallbackUsesRealMarkdown:
    @pytest.mark.asyncio
    async def test_plain_prose_fallback_uses_dash_not_glyph(self):
        """The genuine fallback case (no-LLM / failure-path summaries have no
        markdown at all) still gets bulletized — but with "- " (real
        CommonMark list syntax) instead of the "•" glyph, which marked.parse
        does not recognize as a list marker."""
        result = await _summarize("PDF with 3 pages and 240 characters of text")
        assert result["summary"].startswith("- ")
        assert "•" not in result["summary"]

    @pytest.mark.asyncio
    async def test_plain_prose_multi_sentence_becomes_real_list_items(self):
        result = await _summarize("The roadmap covers Q3. It has three phases. Risks are listed")
        lines = [ln for ln in result["summary"].split("\n") if ln.strip()]
        assert lines[0] == "- The roadmap covers Q3"
        assert all(ln.startswith("- ") for ln in lines)
        assert "•" not in result["summary"]
