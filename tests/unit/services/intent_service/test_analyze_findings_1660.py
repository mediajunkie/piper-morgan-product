"""#1660 — handle_analyze_document returns the REAL key_findings.

The silent data drop (found during #1657, made user-visible by #1659):
``handle_analyze_document``'s upload branch returned
``"key_findings": analysis_result.recommendations or []`` — but
``DocumentAnalyzer.analyze()`` constructs every happy-path AnalysisResult with
``key_findings=key_points, recommendations=[]``. The real findings were always
dropped; the ``format=detailed`` summarize path then rendered a "Key Findings:"
header with nothing under it.

What this file pins:
  1. Planted-marker content flow (the #1659/#1661 idiom) at the HANDLER
     boundary: a real .txt on disk, real analyzer, mocked LLM — the handler's
     response carries the LLM's actual findings, not [].
  2. Both fields surface under honest names: ``recommendations`` is its own
     key (non-empty only on the analyzer's honest-failure paths, where it
     carries the actionable next step — previously that guidance was the only
     thing ever shown, mislabeled as findings).
  3. #1648 honesty contract in the ``detailed`` render: findings present →
     a real "Key Findings:" section; findings genuinely empty → the response
     SAYS so, never an empty header dressed as content; failure-path
     recommendations render under their own header instead of being dropped.
"""

from contextlib import ExitStack, asynccontextmanager
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.analysis.document_analyzer import DocumentAnalyzer

_OWNER = "3f7b8a52-1660-4b00-9e00-000000001660"
_FILE_ID = "aa11bb22-1660-4c00-9e00-000000001660"

MARKER_1660 = "The quarterly zorbit quota is exactly 17 units"


@asynccontextmanager
async def _fake_scope():
    yield MagicMock()


def _upload_record(storage_path: str) -> SimpleNamespace:
    return SimpleNamespace(
        id=_FILE_ID,
        filename="notes.txt",
        file_type="text/plain",
        storage_path=storage_path,
    )


def _upload_branch_patches(record, analyzer):
    from services.intent_service import document_handlers

    return (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            _fake_scope,
        ),
        patch(
            "services.intent_service.document_handlers._get_uploaded_file",
            AsyncMock(return_value=record),
        ),
        patch.object(document_handlers, "_doc_analyzer", analyzer),
    )


class TestUploadBranchReturnsRealFindings:
    @pytest.mark.asyncio
    async def test_planted_marker_findings_reach_the_handler_response(self, tmp_path):
        """THE #1660 shape: real file, real analyzer, mocked LLM emitting a
        finding — pre-fix the response's key_findings was [] regardless."""
        from services.intent_service import document_handlers

        p = tmp_path / "20260830_120000_abc1660_notes.txt"
        p.write_text(f"Team planning notes.\n{MARKER_1660}\nEnd.\n", encoding="utf-8")

        mock_llm = AsyncMock()
        mock_llm.complete.return_value = (
            '{"summary": "Notes about the zorbit quota.", "key_findings": ["Quota is 17"]}'
        )
        analyzer = DocumentAnalyzer(llm_client=mock_llm)

        with ExitStack() as stack:
            for p_ctx in _upload_branch_patches(_upload_record(str(p)), analyzer):
                stack.enter_context(p_ctx)
            result = await document_handlers.handle_analyze_document(
                file_id=_FILE_ID, user_id=_OWNER
            )

        # Real content reached the LLM (the #1659 idiom, one boundary up).
        assert MARKER_1660 in mock_llm.complete.await_args.kwargs["prompt"]
        # And the LLM's real finding reached the handler's response.
        assert result["key_findings"] == ["Quota is 17"]
        # Happy path: recommendations honestly empty under its own name.
        assert result["recommendations"] == []
        assert result["filename"] == "notes.txt"
        assert result["file_id"] == _FILE_ID

    @pytest.mark.asyncio
    async def test_failure_path_surfaces_both_fields_under_honest_names(self, tmp_path):
        """Unsupported type: the analyzer's honest limit is the FINDING and
        the convert-and-reupload guidance is the RECOMMENDATION. Pre-fix the
        guidance was shown mislabeled as findings and the finding was lost."""
        from services.intent_service import document_handlers

        p = tmp_path / "20260830_120000_def1660_archive.zip"
        p.write_bytes(b"PK\x03\x04 not analyzable binary")
        record = SimpleNamespace(
            id=_FILE_ID,
            filename="archive.zip",
            file_type="application/zip",
            storage_path=str(p),
        )

        analyzer = DocumentAnalyzer(llm_client=AsyncMock())

        with ExitStack() as stack:
            for p_ctx in _upload_branch_patches(record, analyzer):
                stack.enter_context(p_ctx)
            result = await document_handlers.handle_analyze_document(
                file_id=_FILE_ID, user_id=_OWNER
            )

        assert any("not supported" in f for f in result["key_findings"])
        assert any("re-upload" in r for r in result["recommendations"])
        # Neither field is the other, and neither was dropped.
        assert result["key_findings"] != result["recommendations"]

    @pytest.mark.asyncio
    async def test_artifact_branch_has_the_same_response_shape(self):
        """#1657's artifact branch and the upload branch return the same keys
        — one /files id space, one response contract."""
        from services.intent_service import document_handlers

        artifact = SimpleNamespace(
            id=_FILE_ID, content="# Plan\n\nShip it.", payload={}, owner_id=_OWNER
        )
        analysis = SimpleNamespace(
            summary="Ship it.",
            key_findings=["Shipping"],
            recommendations=[],
            generated_at=datetime(2026, 8, 30, 12, 0, 0),
        )
        with (
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
                _fake_scope,
            ),
            patch(
                "services.intent_service.document_handlers._get_uploaded_file",
                AsyncMock(return_value=None),
            ),
            patch(
                "services.intent_service.document_handlers._get_owned_artifact",
                AsyncMock(return_value=artifact),
            ),
            patch.object(
                document_handlers._doc_analyzer,
                "analyze_text",
                AsyncMock(return_value=analysis),
            ),
        ):
            result = await document_handlers.handle_analyze_document(
                file_id=_FILE_ID, user_id=_OWNER
            )

        assert result["key_findings"] == ["Shipping"]
        assert result["recommendations"] == []


class TestDetailedRenderHonesty:
    """handle_summarize_document format=detailed — the render both the REST
    summarize route and the #1624 chat rail hand to the user."""

    @staticmethod
    def _analysis(key_findings, recommendations=None, summary="A summary."):
        analysis = {
            "file_id": _FILE_ID,
            "filename": "notes.txt",
            "summary": summary,
            "key_findings": key_findings,
            "analyzed_at": "2026-08-30T12:00:00",
        }
        if recommendations is not None:
            analysis["recommendations"] = recommendations
        return analysis

    async def _detailed(self, analysis):
        from services.intent_service import document_handlers

        with patch(
            "services.intent_service.document_handlers.handle_analyze_document",
            AsyncMock(return_value=analysis),
        ):
            return await document_handlers.handle_summarize_document(
                file_id=_FILE_ID, format="detailed", user_id=_OWNER
            )

    @pytest.mark.asyncio
    async def test_real_findings_render_under_the_header(self):
        result = await self._detailed(
            self._analysis(["Quota is 17", "Deadline is Friday"], recommendations=[])
        )
        assert "Key Findings:" in result["summary"]
        assert "- Quota is 17" in result["summary"]
        assert "- Deadline is Friday" in result["summary"]

    @pytest.mark.asyncio
    async def test_empty_findings_say_so_instead_of_an_empty_header(self):
        """The user-visible #1660 symptom: 'Key Findings:' with nothing under
        it. #1648: an empty list never renders dressed as content."""
        result = await self._detailed(self._analysis([], recommendations=[]))
        assert "Key Findings:" not in result["summary"]
        assert "No key findings were extracted" in result["summary"]

    @pytest.mark.asyncio
    async def test_failure_path_recommendations_render_under_their_own_header(self):
        result = await self._detailed(
            self._analysis(
                ["File type .zip is not supported for analysis"],
                recommendations=["Convert the file to PDF and re-upload"],
            )
        )
        assert "Key Findings:" in result["summary"]
        assert "Recommendations:" in result["summary"]
        assert "- Convert the file to PDF and re-upload" in result["summary"]

    @pytest.mark.asyncio
    async def test_analysis_dict_without_recommendations_key_still_renders(self):
        """Pre-#1660 callers/mocks hand a dict without the key — the render
        must not KeyError and must not invent a Recommendations section."""
        result = await self._detailed(self._analysis(["One finding"]))
        assert "- One finding" in result["summary"]
        assert "Recommendations:" not in result["summary"]
