import io
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Tuple

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

# Issue 2443 (Arch's condition 1, 2026-11-26): ONE table of what Piper can read. Each
# kind lists its extensions and its MIME types. ``classify_document_type`` reads it, and
# so do the upload route's allow-lists (``web/api/routes/files.py``), the Documents
# page's hint and every refusal line. A type is offered at upload if and only if the
# reader below can read it; ``tests/unit/services/analysis/test_readable_types_2443.py``
# fails if the two ever differ, in either direction.
READABLE_KINDS: Dict[str, Tuple[FrozenSet[str], FrozenSet[str]]] = {
    "pdf": (frozenset({".pdf"}), frozenset({"application/pdf"})),
    "text": (
        frozenset({".txt", ".md", ".csv", ".json", ".log"}),
        frozenset({"text/plain", "text/markdown", "text/csv", "application/json"}),
    ),
    "docx": (
        frozenset({".docx"}),
        frozenset({"application/vnd.openxmlformats-officedocument.wordprocessingml.document"}),
    ),
}

#: A browser that does not know a file's type sends one of these. They name no kind, so
#: the extension decides (issue 2443: a ``.log`` or ``.csv`` often arrives this way).
GENERIC_MIME_TYPES: FrozenSet[str] = frozenset({"", "application/octet-stream"})

#: Issue 2443 (Arch's condition 3): a .docx is a zip, and the upload cap counts compressed
#: bytes. The declared size of its main part is read before anything is parsed.
MAX_DOCX_XML_BYTES = 50 * 1024 * 1024
#: The most text kept from one .docx. Summarize reads 3,000 characters and a question
#: 4,000, so this is generous.
MAX_DOCX_TEXT_CHARS = 300_000

#: Issue 2444: how much of a document's text the summary call is given. The slice and
#: the sentence that tells the person about it are both built from this one number.
SUMMARY_READ_CHARS = 3000

# CXO's words (issue 2443 comment, 2026-11-27), verbatim. ``{types}`` is always
# ``readable_types_phrase()``; no type is typed into a line by hand.
DOCX_UNREADABLE_LINE = "That file is too large or isn't a valid .docx, so I couldn't read it."
NO_TEXT_LINE = "I opened the file but found no text in it."
READABLE_TYPES_HINT = "Piper can read {types} files."
CANT_READ_TYPE_LINE = "Piper can't read {ext} files. It can read {types} files."
CANT_READ_KIND_LINE = "Piper can't read that kind of file. It can read {types} files."
SUMMARY_COVERAGE_LINE = (
    "This summary covers the first {cut:,} characters of a document of {n:,} characters."
)
#: A PDF pypdf cannot open (CXO 01M8HEQDYD, 2026-11-28). It claims no cause (damaged,
#: password, scanned), because the code does not know which.
PDF_UNREADABLE_LINE = (
    "Piper couldn't open that PDF. Paste its text here and Piper will work with it."
)


def readable_extensions() -> FrozenSet[str]:
    """Every extension in the table."""
    return frozenset(ext for extensions, _ in READABLE_KINDS.values() for ext in extensions)


def readable_mime_types() -> FrozenSet[str]:
    """Every MIME type in the table."""
    return frozenset(mime for _, mimes in READABLE_KINDS.values() for mime in mimes)


def readable_types_phrase() -> str:
    """The table's extensions as CXO wrote them: sorted, commas between, "and" before
    the last (".csv, .docx, .json, .log, .md, .pdf and .txt")."""
    extensions = sorted(readable_extensions())
    if len(extensions) == 1:
        return extensions[0]
    return ", ".join(extensions[:-1]) + " and " + extensions[-1]


def readable_types_hint() -> str:
    return READABLE_TYPES_HINT.format(types=readable_types_phrase())


def _echoable_extension(display_type: str) -> str:
    """The person's own extension, if it is safe and short enough to say back: a dot,
    then letters, digits, ``+``, ``-`` or ``_``. Anything else (a MIME type, a long or
    odd suffix) is not echoed, and the no-extension line is used."""
    ext = (display_type or "").strip().lower()
    body = ext[1:]
    if ext.startswith(".") and 0 < len(body) <= 10 and all(c.isalnum() or c in "+-_" for c in body):
        return ext
    return ""


def cant_read_line(display_type: str = "") -> str:
    """CXO's refusal for a type that is not in the table (issue 2443)."""
    ext = _echoable_extension(display_type)
    types = readable_types_phrase()
    if ext:
        return CANT_READ_TYPE_LINE.format(ext=ext, types=types)
    return CANT_READ_KIND_LINE.format(types=types)


def summary_coverage_line(text_chars: int) -> Optional[str]:
    """Issue 2444: the sentence that says the summary read only the start of the text.
    None when the whole text was read."""
    if text_chars <= SUMMARY_READ_CHARS:
        return None
    return SUMMARY_COVERAGE_LINE.format(cut=SUMMARY_READ_CHARS, n=text_chars)


def _unsupported_message(display_type: str) -> str:
    """The refusal for a type Piper can't read (issue 2443; #1648: name the real type)."""
    return cant_read_line(display_type)


class UnsupportedDocumentTypeError(Exception):
    """A stored document whose type we can't extract text from (#1659).

    The message names the actual type ('.zip', 'application/zip') — callers
    that surface it to users surface an honest limitation, never the old
    wrong-format 'corrupted PDF' claim.
    """

    def __init__(self, display_type: str):
        self.display_type = display_type
        super().__init__(_unsupported_message(display_type))


class DocxUnreadableError(UnsupportedDocumentTypeError):
    """A .docx past the unzip bound, or one that is not a valid .docx (issue 2443).
    A kind of unreadable document, so callers that already handle the parent need no
    new branch; its message is CXO's line, not the type line."""

    def __init__(self) -> None:
        self.display_type = ".docx"
        Exception.__init__(self, DOCX_UNREADABLE_LINE)


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
        (kind, display) — kind is a key of ``READABLE_KINDS`` ("pdf" | "text" |
        "docx") or "unknown"; display is what an honest unsupported-type message
        should call the file (extension if known, else the MIME type, else "").
    """
    mime = (file_type or "").split(";")[0].strip().lower()
    suffix = Path(filename).suffix.lower() if filename else ""
    display = suffix or mime

    # Issue 2443: the one table decides. MIME type first, then extension.
    for kind, (_, mimes) in READABLE_KINDS.items():
        if mime in mimes:
            return kind, display
    if mime.startswith("text/"):
        return "text", display
    for kind, (extensions, _) in READABLE_KINDS.items():
        if suffix in extensions:
            return kind, display
    if data is not None and data[:4] == b"%PDF":
        return "pdf", display
    return "unknown", display


def extract_docx_text(data: bytes) -> str:
    """The text of a .docx: paragraphs and table cells in document order (issue 2443,
    Arch's conditions 2 and 3).

    Raises ``DocxUnreadableError`` when the main part declares more than
    ``MAX_DOCX_XML_BYTES`` (read from the zip's directory, before anything is
    decompressed), and when the bytes are not a .docx python-docx can open (a corrupt
    zip, an encrypted file, a zip that is not a Word document).
    """
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            declared = archive.getinfo("word/document.xml").file_size
    except (zipfile.BadZipFile, KeyError, OSError, ValueError):
        raise DocxUnreadableError() from None
    if declared > MAX_DOCX_XML_BYTES:
        raise DocxUnreadableError()

    import docx  # python-docx, already pinned
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    try:
        document = docx.Document(io.BytesIO(data))
        parts: List[str] = []
        kept = 0

        def keep(text: str) -> bool:
            """Add one piece of text; False once the cap is reached."""
            nonlocal kept
            if text:
                parts.append(text)
                kept += len(text) + 1
            return kept < MAX_DOCX_TEXT_CHARS

        def walk(container: Any) -> bool:
            for block in container.iter_inner_content():
                if isinstance(block, Paragraph):
                    if not keep(block.text):
                        return False
                elif isinstance(block, Table):
                    # A merged cell is returned once per column it spans. The cell
                    # elements themselves are kept (not their ids, which are reused
                    # once a proxy is collected).
                    seen: List[Any] = []
                    for row in block.rows:
                        for cell in row.cells:
                            if any(cell._tc is kept_tc for kept_tc in seen):
                                continue
                            seen.append(cell._tc)
                            if not walk(cell):
                                return False
            return True

        walk(document)
    except DocxUnreadableError:
        raise
    except Exception:  # silent-ok: any parse failure is the one refusal line, never a 500
        raise DocxUnreadableError() from None
    return "\n".join(parts)[:MAX_DOCX_TEXT_CHARS]


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
    max_pages); a .docx goes through ``extract_docx_text`` (issue 2443; it raises
    ``DocxUnreadableError``); anything else raises UnsupportedDocumentTypeError whose
    message names the real type.
    """
    import io as _io

    kind, display = classify_document_type(file_type=file_type, filename=filename, data=data)
    if kind == "text":
        return data.decode("utf-8", errors="replace")
    if kind == "docx":
        return extract_docx_text(data)
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
        *,
        user_id: Optional[str],  # #2131 (Arch): named, keyword-only, no default
        **kwargs,
    ) -> AnalysisResult:
        """Analyze a stored document, dispatched on file type (#1659).

        Args:
            file_path: Path to the document (read via the #1306 decrypt seam)
            file_type: Stored MIME type (uploaded_files.file_type), if known
            filename: Original filename, if known (extension-fallback dispatch;
                the storage path itself preserves the original extension, so
                bare analyze(path) callers still dispatch correctly)
            user_id: the acting principal (#2131: picks the provider); None = a system call
            **kwargs: unused
        """
        try:
            # #1306: bytes via the decrypt seam, never a raw open()
            from services.file_context.storage import read_file_from_storage

            data = read_file_from_storage(file_path)
            kind, display = classify_document_type(
                file_type=file_type, filename=filename or file_path, data=data
            )

            if kind == "text":
                return await self._analyze_plain_text_bytes(data, file_path, user_id=user_id)

            if kind == "docx":
                # Issue 2443: read the .docx, then the same summary path as plain text.
                try:
                    text = extract_docx_text(data)
                except DocxUnreadableError:
                    return self._refusal(file_path, DOCX_UNREADABLE_LINE, file_type, "docx")
                return await self._analyze_text_as_document(text, file_path, user_id=user_id)

            if kind == "unknown":
                # #1648 honesty contract: no claimed analysis without real content.
                # Issue 2443: the line names the person's type and the readable ones
                # from the table; nothing else is said, and no list is typed by hand.
                return self._refusal(
                    file_path, _unsupported_message(display), file_type, "unsupported"
                )

            # kind == "pdf"
            reader = pypdf.PdfReader(io.BytesIO(data))
            page_count = len(reader.pages)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            if not text.strip():
                # Issue 2443 (CXO): a scanned PDF has pages and no text. Say so; never
                # an empty summary under a summary heading.
                refused = self._refusal(file_path, NO_TEXT_LINE, file_type, "no_text")
                refused.metadata["page_count"] = page_count
                return refused
            metadata: Dict[str, Any] = {"page_count": page_count, "text": text}
            summary, key_points, read_by_model = await self._summarize_text(
                text,
                user_id=user_id,
                no_llm_summary=f"PDF with {page_count} pages and {len(text)} characters of text.",
            )
            metadata["summary"] = summary
            metadata["key_points"] = key_points
            self._note_coverage(metadata, text, read_by_model)
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
            # One sentence, alone, like every other file that was not read.
            return self._refusal(file_path, PDF_UNREADABLE_LINE, file_type, "pdf_unreadable")

    @staticmethod
    def _refusal(
        file_path: str, line: str, file_type: Optional[str], detected_kind: str
    ) -> AnalysisResult:
        """A file Piper did not read: one plain sentence, marked ``refusal`` so no
        caller dresses it as a summary (issue 2443: on beta the old line came back as
        two bullets under "Here's my summary of ...")."""
        return AnalysisResult(
            file_id=file_path,
            analysis_type=AnalysisType.DOCUMENT,
            summary=line,
            key_findings=[],
            recommendations=[],
            generated_at=datetime.now(),
            metadata={
                "error": line,
                "refusal": True,
                "file_type": file_type,
                "detected_kind": detected_kind,
            },
        )

    @staticmethod
    def _note_coverage(metadata: Dict[str, Any], text: str, read_by_model: bool) -> None:
        """Issue 2444: when the model summarized only the start of the text, the
        sentence that says so rides in the result. Nothing is added when the whole
        text was read, or when no model summary was made."""
        line = summary_coverage_line(len(text)) if read_by_model else None
        if line:
            metadata["summary_coverage"] = line

    async def analyze_text(
        self, text: str, source_id: str = "inline-text", *, user_id: Optional[str]
    ) -> AnalysisResult:
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
        summary, key_points, read_by_model = await self._summarize_text(text, user_id=user_id)
        metadata["summary"] = summary
        metadata["key_points"] = key_points
        self._note_coverage(metadata, text, read_by_model)
        return AnalysisResult(
            file_id=source_id,
            analysis_type=AnalysisType.TEXT,
            summary=summary,
            key_findings=key_points,
            recommendations=[],
            generated_at=datetime.now(),
            metadata=metadata,
        )

    async def _analyze_plain_text_bytes(
        self, data: bytes, file_path: str, *, user_id: Optional[str]
    ) -> AnalysisResult:
        """analyze()'s plain-text branch (#1659): decode the stored bytes and
        run them through the same LLM-summary path the PDF branch uses for
        extracted text. Result shape mirrors the PDF branch (DOCUMENT type,
        file_id = storage path, text + summary + key_points in metadata)."""
        text = data.decode("utf-8", errors="replace")
        return await self._analyze_text_as_document(text, file_path, user_id=user_id)

    async def _analyze_text_as_document(
        self, text: str, file_path: str, *, user_id: Optional[str]
    ) -> AnalysisResult:
        """Text taken from a stored file (plain text, or a .docx's text, issue 2443),
        summarized. A file with no text in it is said plainly (CXO), never summarized."""
        if not text.strip():
            return self._refusal(file_path, NO_TEXT_LINE, None, "no_text")
        metadata: Dict[str, Any] = {"text": text}
        summary, key_points, read_by_model = await self._summarize_text(text, user_id=user_id)
        metadata["summary"] = summary
        metadata["key_points"] = key_points
        self._note_coverage(metadata, text, read_by_model)
        return AnalysisResult(
            file_id=file_path,
            analysis_type=AnalysisType.DOCUMENT,
            summary=summary,
            key_findings=key_points,
            recommendations=[],
            generated_at=datetime.now(),
            metadata=metadata,
        )

    async def _summarize_text(
        self,
        text: str,
        *,
        user_id: Optional[str],
        no_llm_summary: Optional[str] = None,
    ) -> Tuple[str, List[str], bool]:
        """The one LLM-summarize step for every text source (#1657 artifacts, #1659
        plain text, PDFs, and a .docx's text since issue 2443): JSON-mode summary via
        SummaryParser, with the same honest fallbacks.

        Returns ``(summary, key_findings, read_by_model)``. ``read_by_model`` is True
        only when the model's summary is what came back, so the caller knows whether
        the issue 2444 sentence applies. The model is given the first
        ``SUMMARY_READ_CHARS`` characters and no more.
        """
        if not text:
            return "", [], False
        if self.llm_client is not None:
            import structlog

            logger = structlog.get_logger()
            try:
                json_prompt = get_json_summary_prompt()
                json_response = await self.llm_client.complete(
                    task_type=TaskType.SUMMARIZE.value,
                    prompt=json_prompt.format(content=text[:SUMMARY_READ_CHARS]),
                    response_format={"type": "json_object"},
                    user_id=user_id,
                )
                document_summary = self.summary_parser.parse_json(json_response)
                return document_summary.to_markdown(), document_summary.key_findings, True
            except Exception as e:
                logger.error(f"LLM analysis failed: {e}")
                return (
                    f"Summary generation failed. Document contains {len(text)} characters.",
                    [],
                    False,
                )
        return no_llm_summary or f"Document with {len(text)} characters of text.", [], False
