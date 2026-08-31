from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pypdf

from services.analysis.base_analyzer import BaseAnalyzer
from services.analysis.summary_parser import SummaryParser
from services.domain.models import AnalysisResult, AnalysisType
from services.prompts import get_json_summary_prompt
from services.shared_types import TaskType

# ---------------------------------------------------------------------------
# #1659: type-dispatched analysis. Before this, analyze() ran pypdf on EVERY
# file type, so a healthy .txt/.md upload "summarized" as 'Unable to analyze
# PDF document' — the wrong-error class the issue names. Dispatch keys, in
# precedence order:
#   1. MIME type — `uploaded_files.file_type` stores the upload request's
#      Content-Type verbatim (web/api/routes/files.py: file_type=
#      file.content_type, gated by ALLOWED_MIME_TYPES), so it is the primary
#      signal when the caller has the DB row.
#   2. Filename extension — the upload route's storage filename is
#      "{timestamp}_{file_id}_{original_filename}", so the original extension
#      survives in storage_path; this also keeps bare analyze(path) callers
#      (existing tests, fixtures) working with no new arguments.
#   3. %PDF magic-byte sniff — last resort when neither is recognized.
# Unknown/binary types get an HONEST message naming the actual type (#1648
# honesty contract) — never a claimed analysis, never a wrong-format claim.
# ---------------------------------------------------------------------------

_PDF_MIME_TYPES = {"application/pdf"}
_PLAIN_TEXT_MIME_TYPES = {
    "text/plain",
    "text/markdown",
    "text/csv",
    "application/json",
}
_PDF_EXTENSIONS = {".pdf"}
_PLAIN_TEXT_EXTENSIONS = {".txt", ".text", ".md", ".markdown", ".csv", ".json", ".log"}


def _unsupported_message(display_type: str) -> str:
    """The honest unsupported-type summary (#1648: name the REAL type)."""
    if display_type:
        return f"I can't analyze {display_type} files yet"
    return "I can't analyze this file type yet"


class UnsupportedDocumentTypeError(Exception):
    """A stored document whose type we can't extract text from (#1659).

    The message names the actual type ('.zip', 'application/zip') — callers
    that surface it to users surface an honest limitation, never the old
    wrong-format 'corrupted PDF' claim.
    """

    def __init__(self, display_type: str):
        self.display_type = display_type
        super().__init__(_unsupported_message(display_type))


def classify_document_type(
    file_type: Optional[str] = None,
    filename: Optional[str] = None,
    data: Optional[bytes] = None,
) -> Tuple[str, str]:
    """Classify a stored document for analysis dispatch (#1659).

    Args:
        file_type: stored MIME Content-Type (uploaded_files.file_type), if known
        filename: original filename OR storage path (extension fallback)
        data: raw bytes for the magic-byte sniff, if already in hand

    Returns:
        (kind, display) — kind is "pdf" | "text" | "unknown"; display is what
        an honest unsupported-type message should call the file (extension if
        known, else the MIME type, else "").
    """
    mime = (file_type or "").split(";")[0].strip().lower()
    suffix = Path(filename).suffix.lower() if filename else ""
    display = suffix or mime

    if mime in _PDF_MIME_TYPES:
        return "pdf", display
    if mime in _PLAIN_TEXT_MIME_TYPES or mime.startswith("text/"):
        return "text", display
    if suffix in _PDF_EXTENSIONS:
        return "pdf", display
    if suffix in _PLAIN_TEXT_EXTENSIONS:
        return "text", display
    if data is not None and data[:4] == b"%PDF":
        return "pdf", display
    return "unknown", display


def extract_document_text(
    data: bytes,
    file_type: Optional[str] = None,
    filename: Optional[str] = None,
    max_pages: Optional[int] = None,
) -> str:
    """Type-dispatched raw text extraction (#1659).

    The shared extraction for document_handlers' question/compare/reference
    sites, which previously ran pypdf on every file type inline. Plain-text
    bytes decode directly; PDFs go through pypdf (optionally truncated to
    max_pages); anything else raises UnsupportedDocumentTypeError whose
    message names the real type.
    """
    import io as _io

    kind, display = classify_document_type(file_type=file_type, filename=filename, data=data)
    if kind == "text":
        return data.decode("utf-8", errors="replace")
    if kind == "pdf":
        reader = pypdf.PdfReader(_io.BytesIO(data))
        pages = reader.pages[:max_pages] if max_pages is not None else reader.pages
        text = ""
        for page in pages:
            text += page.extract_text() or ""
        return text
    raise UnsupportedDocumentTypeError(display)


class DocumentAnalyzer(BaseAnalyzer):
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.summary_parser = SummaryParser()

    async def analyze(
        self,
        file_path: str,
        file_type: Optional[str] = None,
        filename: Optional[str] = None,
        **kwargs,
    ) -> AnalysisResult:
        """Analyze a stored document, dispatched on file type (#1659).

        Args:
            file_path: Path to the document (read via the #1306 decrypt seam)
            file_type: Stored MIME type (uploaded_files.file_type), if known
            filename: Original filename, if known (extension-fallback dispatch;
                the storage path itself preserves the original extension, so
                bare analyze(path) callers still dispatch correctly)
            **kwargs: Additional optional parameters (not used currently)
        """
        try:
            # #1306: bytes via the decrypt seam, never a raw open()
            import io as _io

            from services.file_context.storage import read_file_from_storage

            data = read_file_from_storage(file_path)
            kind, display = classify_document_type(
                file_type=file_type, filename=filename or file_path, data=data
            )

            if kind == "text":
                return await self._analyze_plain_text_bytes(data, file_path)

            if kind == "unknown":
                # #1648 honesty contract: no claimed analysis without real
                # content, and the failure names itself accurately — the
                # actual type, never the old wrong-format 'corrupted PDF'.
                message = _unsupported_message(display)
                return AnalysisResult(
                    file_id=file_path,
                    analysis_type=AnalysisType.DOCUMENT,
                    summary=message,
                    key_findings=[
                        f"File type {display or 'unknown'} is not supported for "
                        "analysis (supported: PDF and plain-text formats such as "
                        ".txt, .md, .csv, .json)"
                    ],
                    recommendations=[
                        "Convert the file to PDF or a plain-text format and re-upload"
                    ],
                    generated_at=datetime.now(),
                    metadata={
                        "error": message,
                        "file_type": file_type,
                        "detected_kind": "unsupported",
                    },
                )

            # kind == "pdf": the pre-#1659 pypdf path, unchanged.
            reader = pypdf.PdfReader(_io.BytesIO(data))
            page_count = len(reader.pages)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            metadata = {"page_count": page_count, "text": text}
            # Empty PDF: summary should be empty string if no text and at least one page
            if not text and page_count > 0:
                summary = ""
                metadata["summary"] = summary
                metadata["key_points"] = []
            elif text:
                # Use LLM for summary and key points with JSON mode
                import structlog

                logger = structlog.get_logger()
                if self.llm_client is not None:
                    try:
                        # Use JSON mode for structured output
                        json_prompt = get_json_summary_prompt()
                        json_response = await self.llm_client.complete(
                            task_type=TaskType.SUMMARIZE.value,
                            prompt=json_prompt.format(content=text[:3000]),
                            response_format={"type": "json_object"},
                        )

                        # Parse JSON into domain model
                        document_summary = self.summary_parser.parse_json(json_response)

                        # Generate clean markdown from domain model
                        summary = document_summary.to_markdown()
                        key_points = document_summary.key_findings

                    except Exception as e:
                        logger.error(f"LLM analysis failed: {e}")
                        summary = (
                            f"Summary generation failed. Document contains {len(text)} characters."
                        )
                        key_points = []
                else:
                    summary = f"PDF with {page_count} pages and {len(text)} characters of text."
                    key_points = []
                metadata["summary"] = summary
                metadata["key_points"] = key_points
            else:
                summary = f"PDF with {page_count} pages and {len(text)} characters of text."
                metadata["summary"] = summary
                metadata["key_points"] = []
            # NOTE: key_points kept in metadata for backward compatibility.
            # Low-priority domain model alignment — not blocking any feature.
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DOCUMENT,
                summary=summary,
                key_findings=key_points,
                recommendations=[],
                generated_at=datetime.now(),
                metadata=metadata,
            )
        except pypdf.errors.PdfReadError:
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DOCUMENT,
                summary="Unable to analyze PDF document",
                key_findings=["PDF file could not be read - file may be corrupted"],
                metadata={"error": "Unable to read PDF file - file may be corrupted"},
                recommendations=[
                    "Verify the PDF file is not corrupted",
                    "Try re-saving or re-exporting the PDF",
                ],
                generated_at=datetime.now(),
            )

    async def analyze_text(self, text: str, source_id: str = "inline-text") -> AnalysisResult:
        """Analyze already-extracted text through the SAME LLM-summary path
        ``analyze()`` uses for PDF text (#1657).

        Exists for content that lives in the database rather than file storage
        — a saved artifact's markdown (the /files view's second half, #355) has
        no storage_path and nothing for pypdf to parse. Mirrors ``analyze()``'s
        text branch verbatim (JSON-mode summary, SummaryParser, markdown
        render, the same honest fallbacks) so both content sources produce the
        same summary shape.
        """
        metadata: Dict[str, Any] = {"text": text}
        summary, key_points = await self._summarize_text(text)
        metadata["summary"] = summary
        metadata["key_points"] = key_points
        return AnalysisResult(
            file_id=source_id,
            analysis_type=AnalysisType.TEXT,
            summary=summary,
            key_findings=key_points,
            recommendations=[],
            generated_at=datetime.now(),
            metadata=metadata,
        )

    async def _analyze_plain_text_bytes(self, data: bytes, file_path: str) -> AnalysisResult:
        """analyze()'s plain-text branch (#1659): decode the stored bytes and
        run them through the same LLM-summary path the PDF branch uses for
        extracted text. Result shape mirrors the PDF branch (DOCUMENT type,
        file_id = storage path, text + summary + key_points in metadata)."""
        text = data.decode("utf-8", errors="replace")
        metadata: Dict[str, Any] = {"text": text}
        summary, key_points = await self._summarize_text(text)
        metadata["summary"] = summary
        metadata["key_points"] = key_points
        return AnalysisResult(
            file_id=file_path,
            analysis_type=AnalysisType.DOCUMENT,
            summary=summary,
            key_findings=key_points,
            recommendations=[],
            generated_at=datetime.now(),
            metadata=metadata,
        )

    async def _summarize_text(self, text: str) -> Tuple[str, List[str]]:
        """Shared LLM-summarize step for the text paths (#1657 analyze_text +
        #1659 plain-text uploads): JSON-mode summary via SummaryParser, with
        the same honest fallbacks analyze_text always had. The PDF branch in
        analyze() keeps its own (byte-identical) copy of this logic — its
        no-LLM fallback message differs ('PDF with N pages...')."""
        if not text:
            return "", []
        if self.llm_client is not None:
            import structlog

            logger = structlog.get_logger()
            try:
                json_prompt = get_json_summary_prompt()
                json_response = await self.llm_client.complete(
                    task_type=TaskType.SUMMARIZE.value,
                    prompt=json_prompt.format(content=text[:3000]),
                    response_format={"type": "json_object"},
                )
                document_summary = self.summary_parser.parse_json(json_response)
                return document_summary.to_markdown(), document_summary.key_findings
            except Exception as e:
                logger.error(f"LLM analysis failed: {e}")
                return (
                    f"Summary generation failed. Document contains {len(text)} characters.",
                    [],
                )
        return f"Document with {len(text)} characters of text.", []
