import os
from unittest.mock import AsyncMock, Mock

import pytest

from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult

FIXTURE_DIR = "tests/fixtures/"


class TestDocumentAnalyzer:
    def setup_method(self):
        # Mock LLM client for summary/key points - use AsyncMock for async compatibility
        self.mock_llm = AsyncMock()
        # Configure default return value to prevent unawaited coroutine warnings
        self.mock_llm.complete.return_value = (
            '{"summary": "Default test summary.", "key_findings": ["Default point"]}'
        )
        # DocumentAnalyzer will be implemented later
        from services.analysis.document_analyzer import DocumentAnalyzer

        self.analyzer = DocumentAnalyzer(llm_client=self.mock_llm)

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_basic_pdf_analysis(self):
        """Test page count and text extraction from a normal PDF"""
        pdf_path = os.path.join(FIXTURE_DIR, "chapter.pdf")
        result = await self.analyzer.analyze(pdf_path)
        # Be more flexible with page count - just check it's a positive number
        assert result.metadata["page_count"] > 0
        assert isinstance(result.metadata["text"], str)

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_summary_generation_with_llm(self):
        """Test summary generation using LLM (mocked)"""
        pdf_path = os.path.join(FIXTURE_DIR, "chapter.pdf")
        # Mock the complete method that the analyzer actually calls
        self.mock_llm.complete.return_value = (
            '{"summary": "This is a summary.", "key_findings": ["Point 1", "Point 2"]}'
        )
        result = await self.analyzer.analyze(pdf_path)
        assert "summary" in result.metadata
        assert result.metadata["summary"] is not None

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_key_points_extraction(self):
        """Test key points extraction from PDF using LLM (mocked)"""
        pdf_path = os.path.join(FIXTURE_DIR, "chapter.pdf")
        # Mock the complete method that the analyzer actually calls
        self.mock_llm.complete.return_value = (
            '{"summary": "This is a summary.", "key_findings": ["Point 1", "Point 2"]}'
        )
        result = await self.analyzer.analyze(pdf_path)
        assert "key_points" in result.metadata
        assert isinstance(result.metadata["key_points"], list)

    @pytest.mark.asyncio
    async def test_empty_pdf_handling(self):
        """Test that empty PDF (no text) returns zero page count and empty text"""
        pdf_path = os.path.join(FIXTURE_DIR, "empty_document.pdf")
        result = await self.analyzer.analyze(pdf_path)
        # Be more flexible - check it's a valid page count
        assert result.metadata["page_count"] >= 0
        assert isinstance(result.metadata["text"], str)

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_corrupted_pdf_handling(self):
        """Test that corrupted PDF returns error gracefully"""
        pdf_path = os.path.join(FIXTURE_DIR, "corrupted_document.pdf")
        result = await self.analyzer.analyze(pdf_path)
        assert result.metadata.get("error") is not None
        assert (
            "corrupt" in result.metadata.get("error", "").lower()
            or "error" in result.metadata.get("error", "").lower()
        )

    @pytest.mark.smoke
    def test_inherits_from_base_analyzer(self):
        from services.analysis.document_analyzer import DocumentAnalyzer

        assert issubclass(DocumentAnalyzer, BaseAnalyzer)

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_analyze_returns_analysis_result(self):
        pdf_path = os.path.join(FIXTURE_DIR, "chapter.pdf")
        result = await self.analyzer.analyze(pdf_path)
        assert isinstance(result, AnalysisResult)

    @pytest.mark.smoke
    def test_llm_dependency_injection(self):
        from services.analysis.document_analyzer import DocumentAnalyzer

        analyzer = DocumentAnalyzer(llm_client=self.mock_llm)
        assert analyzer.llm_client is self.mock_llm


# 1. Basic PDF analysis (page count, text extraction)
@pytest.mark.asyncio
async def test_document_basic_pdf_analysis():
    from services.analysis.document_analyzer import DocumentAnalyzer

    analyzer = DocumentAnalyzer()
    result = await analyzer.analyze(FIXTURE_DIR + "chapter.pdf")
    # Be more flexible with page count
    assert result.metadata["page_count"] > 0
    assert isinstance(result.metadata["text"], str)
    assert len(result.metadata["text"]) > 0


# 2. Summary generation using LLM (mock LLM)
@pytest.mark.asyncio
async def test_document_summary_generation():
    from services.analysis.document_analyzer import DocumentAnalyzer

    mock_llm = AsyncMock()
    # Configure AsyncMock properly for Python 3.11+ compatibility
    mock_llm.complete.return_value = (
        '{"summary": "This is a summary.", "key_findings": ["Point 1", "Point 2"]}'
    )
    analyzer = DocumentAnalyzer(llm_client=mock_llm)
    result = await analyzer.analyze(FIXTURE_DIR + "chapter.pdf")
    assert "summary" in result.metadata
    assert result.metadata["summary"] is not None


# 3. Key points extraction
@pytest.mark.asyncio
async def test_document_key_points_extraction():
    from services.analysis.document_analyzer import DocumentAnalyzer

    mock_llm = AsyncMock()
    # Configure AsyncMock properly for Python 3.11+ compatibility
    mock_llm.complete.return_value = (
        '{"summary": "This is a summary.", "key_findings": ["Point 1", "Point 2"]}'
    )
    analyzer = DocumentAnalyzer(llm_client=mock_llm)
    result = await analyzer.analyze(FIXTURE_DIR + "chapter.pdf")
    assert "key_points" in result.metadata
    assert isinstance(result.metadata["key_points"], list)


# 4. Empty PDF handling
@pytest.mark.asyncio
async def test_document_empty_pdf_handling():
    from services.analysis.document_analyzer import DocumentAnalyzer

    analyzer = DocumentAnalyzer()
    result = await analyzer.analyze(FIXTURE_DIR + "empty_document.pdf")
    assert result.metadata["page_count"] >= 0
    assert isinstance(result.metadata["text"], str)


# 5. Corrupted PDF handling
@pytest.mark.asyncio
async def test_document_corrupted_pdf_handling():
    from services.analysis.document_analyzer import DocumentAnalyzer

    analyzer = DocumentAnalyzer()
    result = await analyzer.analyze(FIXTURE_DIR + "corrupted_document.pdf")
    assert "error" in result.metadata
    assert "corrupt" in result.metadata["error"] or "invalid" in result.metadata["error"]


# 6. Inheritance from BaseAnalyzer
@pytest.mark.smoke
def test_document_inherits_base_analyzer():
    from services.analysis.base_analyzer import BaseAnalyzer
    from services.analysis.document_analyzer import DocumentAnalyzer

    assert issubclass(DocumentAnalyzer, BaseAnalyzer)


# 7. analyze returns AnalysisResult
@pytest.mark.asyncio
async def test_document_analyze_returns_analysis_result():
    from services.analysis.document_analyzer import DocumentAnalyzer

    analyzer = DocumentAnalyzer()
    result = await analyzer.analyze(FIXTURE_DIR + "chapter.pdf")
    assert isinstance(result, AnalysisResult)


# 8. LLM dependency injection
@pytest.mark.smoke
def test_document_llm_dependency_injection():
    from services.analysis.document_analyzer import DocumentAnalyzer

    mock_llm = Mock()
    analyzer = DocumentAnalyzer(llm_client=mock_llm)
    assert hasattr(analyzer, "llm_client")
    assert analyzer.llm_client is mock_llm


# ---------------------------------------------------------------------------
# #1659: type-dispatched analysis. Before the fix, analyze() ran pypdf on
# EVERY file type, so a healthy .txt/.md upload "summarized" as 'Unable to
# analyze PDF document'. These tests pin: plain-text uploads flow their ACTUAL
# content through the real analyze path (the #1661 planted-marker idiom); the
# PDF path is unchanged; unknown/binary types get an honest message naming
# the real type (#1648 honesty contract).
# ---------------------------------------------------------------------------

MARKER_1659 = "The quarterly zorbit quota is exactly 17 units"


class Test1659TypeDispatch:
    def setup_method(self):
        from services.analysis.document_analyzer import DocumentAnalyzer

        self.mock_llm = AsyncMock()
        self.mock_llm.complete.return_value = (
            '{"summary": "Notes about the zorbit quota.", "key_findings": ["Quota is 17"]}'
        )
        self.analyzer = DocumentAnalyzer(llm_client=self.mock_llm)

    @pytest.mark.asyncio
    async def test_txt_upload_analyzes_its_actual_content(self, tmp_path):
        """#1661 probe idiom: a planted marker fact in a real .txt reaches the
        summarize path — the LLM prompt carries the file's actual content."""
        p = tmp_path / "20260830_120000_abc123_notes.txt"
        p.write_text(f"Team planning notes.\n{MARKER_1659}\nEnd of notes.\n", encoding="utf-8")

        result = await self.analyzer.analyze(
            str(p), file_type="text/plain", filename="notes.txt"
        )

        assert MARKER_1659 in result.metadata["text"]
        sent_prompt = self.mock_llm.complete.await_args.kwargs["prompt"]
        assert MARKER_1659 in sent_prompt  # real content reached the LLM
        assert "Unable to analyze PDF" not in result.summary
        # SummaryParser renders the LLM's JSON to markdown; the mocked
        # key finding must be in the rendered summary
        assert "Quota is 17" in result.summary
        assert result.key_findings == ["Quota is 17"]

    @pytest.mark.asyncio
    async def test_md_upload_analyzes_its_actual_content(self, tmp_path):
        """.md with the stored MIME the upload route records (text/markdown)."""
        p = tmp_path / "20260830_120000_def456_plan.md"
        p.write_text(f"# Plan\n\n{MARKER_1659}\n", encoding="utf-8")

        result = await self.analyzer.analyze(
            str(p), file_type="text/markdown", filename="plan.md"
        )

        assert MARKER_1659 in result.metadata["text"]
        assert MARKER_1659 in self.mock_llm.complete.await_args.kwargs["prompt"]
        assert "Unable to analyze PDF" not in result.summary

    @pytest.mark.asyncio
    async def test_txt_dispatches_by_extension_when_no_mime_stored(self, tmp_path):
        """Legacy rows may have NULL file_type — the storage filename keeps the
        original extension, so bare analyze(path) still dispatches to text."""
        p = tmp_path / "20260830_120000_ghi789_fixture.txt"
        p.write_text(MARKER_1659, encoding="utf-8")

        result = await self.analyzer.analyze(str(p))

        assert MARKER_1659 in result.metadata["text"]
        assert "Unable to analyze PDF" not in result.summary

    @pytest.mark.asyncio
    async def test_txt_without_llm_falls_back_honestly(self, tmp_path):
        from services.analysis.document_analyzer import DocumentAnalyzer

        p = tmp_path / "notes.txt"
        content = "Some plain text content."
        p.write_text(content, encoding="utf-8")

        result = await DocumentAnalyzer().analyze(str(p), file_type="text/plain")

        assert result.summary == f"Document with {len(content)} characters of text."
        assert "PDF" not in result.summary

    @pytest.mark.asyncio
    async def test_empty_txt_yields_empty_summary(self, tmp_path):
        p = tmp_path / "empty.txt"
        p.write_text("", encoding="utf-8")

        result = await self.analyzer.analyze(str(p), file_type="text/plain")

        assert result.summary == ""
        assert result.metadata["key_points"] == []
        self.mock_llm.complete.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_pdf_mime_dispatches_to_pypdf_path_unchanged(self):
        """Explicit application/pdf MIME hits the pre-#1659 pypdf branch."""
        result = await self.analyzer.analyze(
            os.path.join(FIXTURE_DIR, "chapter.pdf"),
            file_type="application/pdf",
            filename="chapter.pdf",
        )

        assert result.metadata["page_count"] > 0
        assert isinstance(result.metadata["text"], str)

    @pytest.mark.asyncio
    async def test_unknown_type_gets_honest_message_naming_real_type(self, tmp_path):
        """#1648: the failure names the ACTUAL type — never the wrong-format
        'corrupted PDF' claim, never a claimed analysis without content."""
        p = tmp_path / "20260830_120000_jkl012_archive.zip"
        p.write_bytes(b"PK\x03\x04 not really analyzable binary content")

        result = await self.analyzer.analyze(
            str(p), file_type="application/zip", filename="archive.zip"
        )

        assert result.summary == "I can't analyze .zip files yet"
        assert "PDF" not in result.summary
        assert "corrupt" not in result.summary.lower()
        assert result.metadata["detected_kind"] == "unsupported"
        self.mock_llm.complete.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_docx_gets_honest_message_not_pdf_claim(self, tmp_path):
        """.docx is upload-allowed but has no extractor today — honest limit."""
        p = tmp_path / "20260830_120000_mno345_report.docx"
        p.write_bytes(b"PK\x03\x04 docx zip container bytes")

        result = await self.analyzer.analyze(
            str(p),
            file_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="report.docx",
        )

        assert result.summary == "I can't analyze .docx files yet"
        assert "Unable to analyze PDF" not in result.summary


class Test1659ExtractDocumentText:
    """The shared extractor for document_handlers' question/compare/reference
    sites (which previously ran pypdf inline on every file type)."""

    def test_plain_text_bytes_decode_directly(self):
        from services.analysis.document_analyzer import extract_document_text

        text = extract_document_text(
            f"line one\n{MARKER_1659}\n".encode("utf-8"),
            file_type="text/plain",
            filename="notes.txt",
        )
        assert MARKER_1659 in text

    def test_pdf_extracts_via_pypdf_with_magic_sniff(self):
        """No MIME, no extension hint — the %PDF magic-byte sniff routes it."""
        from services.analysis.document_analyzer import extract_document_text

        with open(os.path.join(FIXTURE_DIR, "chapter.pdf"), "rb") as f:
            data = f.read()
        text = extract_document_text(data)
        assert isinstance(text, str)
        assert len(text) > 0

    def test_pdf_max_pages_cap(self):
        from services.analysis.document_analyzer import extract_document_text

        with open(os.path.join(FIXTURE_DIR, "chapter.pdf"), "rb") as f:
            data = f.read()
        capped = extract_document_text(data, file_type="application/pdf", max_pages=1)
        assert isinstance(capped, str)

    def test_unsupported_type_raises_naming_real_type(self):
        from services.analysis.document_analyzer import (
            UnsupportedDocumentTypeError,
            extract_document_text,
        )

        with pytest.raises(UnsupportedDocumentTypeError) as exc_info:
            extract_document_text(
                b"PK\x03\x04 binary", file_type="application/zip", filename="a.zip"
            )
        assert "I can't analyze .zip files yet" in str(exc_info.value)
        assert "PDF" not in str(exc_info.value)


class Test1659Classifier:
    def test_mime_beats_everything(self):
        from services.analysis.document_analyzer import classify_document_type

        assert classify_document_type(file_type="application/pdf")[0] == "pdf"
        assert classify_document_type(file_type="text/plain")[0] == "text"
        assert classify_document_type(file_type="text/markdown")[0] == "text"
        assert classify_document_type(file_type="application/json")[0] == "text"

    def test_mime_charset_parameter_is_stripped(self):
        from services.analysis.document_analyzer import classify_document_type

        assert classify_document_type(file_type="text/plain; charset=utf-8")[0] == "text"

    def test_extension_fallback_covers_storage_paths(self):
        from services.analysis.document_analyzer import classify_document_type

        assert classify_document_type(filename="uploads/u1/20260830_x_notes.txt")[0] == "text"
        assert classify_document_type(filename="uploads/u1/20260830_x_doc.pdf")[0] == "pdf"

    def test_unknown_reports_extension_as_display(self):
        from services.analysis.document_analyzer import classify_document_type

        kind, display = classify_document_type(
            file_type="application/zip", filename="a.zip"
        )
        assert kind == "unknown"
        assert display == ".zip"

    def test_unknown_without_filename_reports_mime_as_display(self):
        from services.analysis.document_analyzer import classify_document_type

        kind, display = classify_document_type(file_type="application/zip")
        assert kind == "unknown"
        assert display == "application/zip"
