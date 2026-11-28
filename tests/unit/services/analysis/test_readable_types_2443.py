"""Issues 2443 and 2444 (Arch's conditions 2026-11-26; CXO's words 2026-11-27 and
01M8H9Z1PP; PPM's rows 01M8HA6Z5J; Web's served reads 01M8H9J72V).

2443: one table of what Piper can read feeds the upload allow-list, the reader, the
page's hint and every refusal. A .docx is read, with the unzip bounded before parsing.
A file that was not read gets one plain sentence, never a summary heading or bullets,
in both summary replies. The Remove dialog names the file.

2444: a summary that read only the start of the text says so, in the reply itself, in
both replies; the key findings appear once.

Layers: the analyzer, the handlers and the two reply builders called directly, with
the model and the file store stubbed. Not served, and not a browser.
"""

import io
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import docx
import pytest

from services.analysis import document_analyzer as da
from services.domain.models import Intent
from services.intent_service import document_handlers
from services.shared_types import IntentCategory
from web.api.routes import files as files_routes

ROOT = Path(__file__).resolve().parents[4]
_USER = "3f7b8a52-2443-4b00-9e00-000000002443"
SUMMARY_JSON = (
    '{"title": "Garden notes", "document_type": "notes", '
    '"key_findings": ["Beds are planted", "Water on Mondays"], "sections": []}'
)


def _docx_bytes(build) -> bytes:
    document = docx.Document()
    build(document)
    out = io.BytesIO()
    document.save(out)
    return out.getvalue()


def _garden(document) -> None:
    document.add_paragraph("Garden club notes for spring.")
    table = document.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "Bed"
    table.cell(0, 1).text = "Crop"
    table.cell(1, 0).text = "North"
    table.cell(1, 1).text = "Beans"
    document.add_paragraph("Water on Mondays.")


# --- 2443: one table ------------------------------------------------------------------


def test_the_upload_lists_are_the_readers_table():
    """PPM's first row: a test that fails if they differ in either direction."""
    assert files_routes.ALLOWED_EXTENSIONS == da.readable_extensions()
    assert files_routes.ALLOWED_MIME_TYPES == da.readable_mime_types()
    source = (ROOT / "web/api/routes/files.py").read_text()
    for typed in ('".docx"', '".pdf"', '"application/pdf"', '"text/plain"'):
        assert typed not in source, f"{typed} is typed into the upload route"


def test_every_type_the_upload_offers_is_one_the_reader_reads():
    for kind, (extensions, mimes) in da.READABLE_KINDS.items():
        for ext in extensions:
            assert da.classify_document_type(filename=f"a{ext}")[0] == kind
        for mime in mimes:
            assert da.classify_document_type(file_type=mime)[0] == kind
    assert {".docx", ".csv", ".log"} <= da.readable_extensions()


def test_the_reader_reads_nothing_by_extension_that_the_upload_refuses():
    for ext in (".text", ".markdown", ".doc", ".rtf", ".xlsx", ".zip", ""):
        assert ext not in da.readable_extensions()
        assert da.classify_document_type(filename=f"a{ext}")[0] == "unknown"


DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


@pytest.mark.parametrize(
    "content_type,name,allowed",
    [
        ("text/plain", "a.txt", True),
        ("text/csv", "a.csv", True),
        ("application/vnd.ms-excel", "a.csv", False),  # a named type outside the kind
        ("", "a.log", True),  # Arch: a browser that does not know the type
        ("application/octet-stream", "a.md", True),
        ("text/x-log", "a.log", True),
        ("text/x-markdown", "a.md", True),  # Arch: any text/* for a text-kind extension
        ("application/pdf", "a.pdf", True),
        (DOCX_MIME, "a.docx", True),
        ("application/pdf", "a.docx", False),  # Arch: the reader would send it to pypdf
        ("text/plain", "a.docx", False),  # Arch: the reader would decode it as text
        ("text/plain", "a.pdf", False),
        (DOCX_MIME, "a.txt", False),
        ("application/json", "a.txt", True),  # both are the text kind
        ("application/pdf", "a.exe", False),  # the extension must be in the table
        ("application/zip", "a.zip", False),
        ("text/plain", "a", False),
    ],
)
def test_the_upload_gate(content_type, name, allowed):
    suffix = Path(name).suffix.lower()
    assert files_routes._upload_type_allowed(content_type, suffix) is allowed


@pytest.mark.parametrize(
    "content_type,name",
    [
        ("text/plain", "a.txt"),
        ("", "a.log"),
        ("application/octet-stream", "a.docx"),
        ("text/x-markdown", "a.md"),
        (DOCX_MIME, "a.docx"),
        ("application/pdf", "a.pdf"),
        ("application/json", "a.csv"),
    ],
)
def test_every_file_the_upload_stores_is_the_same_kind_to_the_reader(content_type, name):
    """Arch's condition: the reader decides by MIME type first, the upload by
    extension; for anything the upload lets in, the two must agree."""
    suffix = Path(name).suffix.lower()
    assert files_routes._upload_type_allowed(content_type, suffix)
    by_extension = da.classify_document_type(filename=name)[0]
    as_stored = da.classify_document_type(file_type=content_type, filename=name)[0]
    assert as_stored == by_extension != "unknown"


# --- 2443: CXO's lines, built from the table -------------------------------------------


def test_the_types_phrase_is_sorted_with_and_before_the_last():
    assert da.readable_types_phrase() == ".csv, .docx, .json, .log, .md, .pdf and .txt"
    assert da.readable_types_hint() == (
        "Piper can read .csv, .docx, .json, .log, .md, .pdf and .txt files."
    )


def test_the_refusal_names_the_persons_extension_and_the_table():
    types = da.readable_types_phrase()
    assert da.cant_read_line(".zip") == f"Piper can't read .zip files. It can read {types} files."
    assert da.cant_read_line(".XLSX").startswith("Piper can't read .xlsx files.")
    no_ext = f"Piper can't read that kind of file. It can read {types} files."
    for odd in ("", "application/zip", ".<b>x</b>", ".averyveryverylongextension", ".a b", "."):
        assert da.cant_read_line(odd) == no_ext
    assert files_routes.FILE_KIND_NOT_USABLE_LINE == no_ext


def test_the_page_hint_and_picker_come_from_the_table_and_the_remove_dialog_names_the_file():
    page = (ROOT / "templates/files.html").read_text()
    assert "{{ readable_types_hint }}" in page and 'accept="{{ readable_accept }}"' in page
    assert "Word (.docx)" not in page and "Allowed: Text" not in page
    assert "Remove this file?" not in page and "Remove this artifact?" not in page
    assert "title: `Remove ${name || fallback}?`" in page
    assert "I'll remove this from your documents. This can't be undone." in page
    route = (ROOT / "web/api/routes/ui.py").read_text()
    assert '"readable_types_hint": readable_types_hint()' in route


# --- 2443: a .docx is read, bounded ---------------------------------------------------


def test_a_docx_gives_paragraph_and_table_text_in_document_order():
    text = da.extract_docx_text(_docx_bytes(_garden))
    assert text.split("\n") == [
        "Garden club notes for spring.",
        "Bed",
        "Crop",
        "North",
        "Beans",
        "Water on Mondays.",
    ]
    assert da.extract_document_text(_docx_bytes(_garden), filename="notes.docx") == text


def test_a_docx_past_the_bound_is_refused_before_anything_is_parsed(monkeypatch):
    data = _docx_bytes(_garden)
    monkeypatch.setattr(da, "MAX_DOCX_PACKAGE_BYTES", 10)
    with patch("docx.Document") as opened:
        with pytest.raises(da.DocxUnreadableError) as refused:
            da.extract_docx_text(data)
    opened.assert_not_called()  # the reader catches every error, so a raise proves nothing
    assert (
        str(refused.value)
        == "That file is too large or isn't a valid .docx, so I couldn't read it."
    )


def test_the_bound_reads_the_declared_size_from_the_zips_directory():
    """A small file whose main part declares 60 MB: refused, and never decompressed."""
    big = io.BytesIO()
    with zipfile.ZipFile(big, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", b"\0" * (60 * 1024 * 1024))
    data = big.getvalue()
    assert len(data) < 1024 * 1024  # it would pass the 10 MB upload cap
    with patch("docx.Document") as opened:
        with pytest.raises(da.DocxUnreadableError):
            da.extract_docx_text(data)
    opened.assert_not_called()


def _with_extra_part(data: bytes, name: str, payload: bytes, relate: bool) -> bytes:
    """A valid .docx with one more part added. ``relate`` links it from the document's
    relationships as an image, which is what makes python-docx load it."""
    out = io.BytesIO()
    with (
        zipfile.ZipFile(io.BytesIO(data)) as src,
        zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst,
    ):
        for entry in src.infolist():
            body = src.read(entry.filename)
            if relate and entry.filename == "word/_rels/document.xml.rels":
                link = (
                    b'<Relationship Id="rIdBig" Type="http://schemas.openxmlformats.org/'
                    b'officeDocument/2006/relationships/image" Target="media/big.png"/>'
                )
                body = body.replace(b"</Relationships>", link + b"</Relationships>")
            if (
                relate
                and entry.filename == "[Content_Types].xml"
                and b'Extension="png"' not in body
            ):
                body = body.replace(
                    b"</Types>", b'<Default Extension="png" ContentType="image/png"/></Types>'
                )
            dst.writestr(entry, body)
        dst.writestr(name, payload)
    return out.getvalue()


@pytest.mark.parametrize("relate", [True, False])
def test_the_bound_is_on_the_whole_package_not_one_part(relate):
    """HOST's finding (01M8HETS9W), confirmed by Arch from python-docx's source: every
    part a relationship reaches is decompressed. A small document.xml beside a linked
    part that declares 60 MB is refused from the directory, and never opened."""
    data = _with_extra_part(
        _docx_bytes(_garden), "word/media/big.png", b"\0" * (60 * 1024 * 1024), relate
    )
    assert len(data) < 1024 * 1024  # it would pass the 10 MB upload cap
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        assert archive.getinfo("word/document.xml").file_size < 100_000
    with patch("docx.Document") as opened:
        with pytest.raises(da.DocxUnreadableError) as refused:
            da.extract_docx_text(data)
    opened.assert_not_called()  # the reader catches every error, so a raise proves nothing
    assert str(refused.value) == da.DOCX_UNREADABLE_LINE


def test_a_linked_part_under_the_bound_is_still_read():
    data = _with_extra_part(_docx_bytes(_garden), "word/media/big.png", b"\0" * 1024, True)
    assert "Garden club notes for spring." in da.extract_docx_text(data)


def test_an_entity_bomb_in_the_document_part_expands_nothing():
    """python-docx builds its parser with ``resolve_entities=False`` (Arch read
    ``docx/oxml/parser.py``). If a version bump changes that, this fails here, not on
    the server: the text stays small, or the file is refused; it never grows."""
    bomb = (
        b'<?xml version="1.0"?><!DOCTYPE w [<!ENTITY a "' + b"A" * 1000 + b'">'
        b'<!ENTITY b "&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;">'
        b'<!ENTITY c "&b;&b;&b;&b;&b;&b;&b;&b;&b;&b;">'
        b'<!ENTITY d "&c;&c;&c;&c;&c;&c;&c;&c;&c;&c;">]>'
        b'<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        b"<w:body><w:p><w:r><w:t>&d;&d;&d;&d;&d;&d;&d;&d;&d;&d;</w:t></w:r></w:p></w:body>"
        b"</w:document>"
    )
    out = io.BytesIO()
    with (
        zipfile.ZipFile(io.BytesIO(_docx_bytes(_garden))) as src,
        zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst,
    ):
        for entry in src.infolist():
            body = bomb if entry.filename == "word/document.xml" else src.read(entry.filename)
            dst.writestr(entry, body)
    try:
        text = da.extract_docx_text(out.getvalue())
    except da.DocxUnreadableError:
        return
    assert len(text) < 10_000  # fully expanded it would be 10,000,000 characters


@pytest.mark.parametrize("label", ["not_a_zip", "zip_without_the_part", "part_is_not_word"])
def test_a_bad_docx_is_the_one_line_never_an_error(label):
    if label == "not_a_zip":
        data = b"\xd0\xcf\x11\xe0 an encrypted or old-format file"
    else:
        raw = io.BytesIO()
        with zipfile.ZipFile(raw, "w") as archive:
            name = "word/document.xml" if label == "part_is_not_word" else "other.txt"
            archive.writestr(name, "not a word document")
        data = raw.getvalue()
    with pytest.raises(da.DocxUnreadableError):
        da.extract_docx_text(data)
    assert issubclass(da.DocxUnreadableError, da.UnsupportedDocumentTypeError)


def test_the_text_kept_from_a_docx_is_capped(monkeypatch):
    monkeypatch.setattr(da, "MAX_DOCX_TEXT_CHARS", 50)

    def long(document):
        for _ in range(20):
            document.add_paragraph("twenty characters ..")

    assert len(da.extract_docx_text(_docx_bytes(long))) <= 50


# --- the analyzer's results -----------------------------------------------------------


def _analyzer(reply=SUMMARY_JSON):
    llm = AsyncMock()
    llm.complete.return_value = reply
    return da.DocumentAnalyzer(llm_client=llm), llm


async def _analyze(tmp_path, name, data, file_type=None):
    path = tmp_path / name
    path.write_bytes(data)
    analyzer, llm = _analyzer()
    with patch("services.file_context.storage.read_file_from_storage", return_value=data):
        result = await analyzer.analyze(str(path), file_type=file_type, filename=name, user_id=None)
    return result, llm


@pytest.mark.asyncio
async def test_a_docx_is_summarized_from_its_text(tmp_path):
    result, llm = await _analyze(tmp_path, "garden-notes.docx", _docx_bytes(_garden))
    prompt = llm.complete.await_args.kwargs["prompt"]
    assert "Garden club notes for spring." in prompt and "Beans" in prompt
    assert not result.metadata.get("refusal")
    assert "Beds are planted" in result.summary
    assert result.key_findings == ["Beds are planted", "Water on Mondays"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,data,line",
    [
        ("a.docx", b"not a zip", da.DOCX_UNREADABLE_LINE),
        ("empty.docx", None, da.NO_TEXT_LINE),
        ("blank.txt", b"  \n ", da.NO_TEXT_LINE),
        ("archive.zip", b"PK\x03\x04", None),
    ],
)
async def test_a_file_that_was_not_read_is_one_sentence_and_marked(tmp_path, name, data, line):
    if data is None:
        data = _docx_bytes(lambda document: None)
    result, llm = await _analyze(tmp_path, name, data)
    assert result.summary == (line or da.cant_read_line(".zip"))
    assert result.metadata["refusal"] is True
    assert result.key_findings == [] and result.recommendations == []
    llm.complete.assert_not_awaited()


@pytest.mark.asyncio
async def test_a_pdf_with_pages_and_no_text_says_so(tmp_path):
    """A scanned PDF: a page, and no text on it (built here; the repo's
    ``empty_document.pdf`` fixture does carry text)."""
    import pypdf

    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=200, height=200)
    path = tmp_path / "scan.pdf"
    with open(path, "wb") as out:
        writer.write(out)
    analyzer, llm = _analyzer()
    result = await analyzer.analyze(str(path), user_id=None)
    assert result.summary == "I opened the file but found no text in it."
    assert result.metadata["refusal"] is True and result.metadata["page_count"] > 0
    llm.complete.assert_not_awaited()


@pytest.mark.asyncio
async def test_a_pdf_that_cannot_be_opened_is_marked_too():
    analyzer, _ = _analyzer()
    result = await analyzer.analyze("tests/fixtures/corrupted_document.pdf", user_id=None)
    assert result.summary == (
        "Piper couldn't open that PDF. Paste its text here and Piper will work with it."
    )
    assert result.metadata["refusal"] is True
    assert result.key_findings == [] and result.recommendations == []
    assert "Unable to analyze" not in result.summary


# --- 2444: the coverage sentence -------------------------------------------------------


def test_the_sentence_is_built_from_the_cut_and_shown_only_past_it():
    cut = da.SUMMARY_READ_CHARS
    assert da.summary_coverage_line(cut) is None and da.summary_coverage_line(0) is None
    assert da.summary_coverage_line(41250) == (
        "This summary covers the first 3,000 characters of a document of 41,250 characters."
    )
    assert f"{cut:,}" in da.summary_coverage_line(cut + 1)


def test_one_constant_makes_the_slice_and_no_3000_is_typed_elsewhere():
    source = (ROOT / "services/analysis/document_analyzer.py").read_text()
    assert source.count("3000") == 1 and "SUMMARY_READ_CHARS = 3000" in source
    assert "text[:SUMMARY_READ_CHARS]" in source


@pytest.mark.asyncio
@pytest.mark.parametrize("length,covered", [(7486, True), (3000, False), (12, False)])
async def test_the_model_gets_the_cut_and_the_result_carries_the_sentence(
    tmp_path, length, covered
):
    text = ("harbor " * 2000)[:length]
    result, llm = await _analyze(tmp_path, "harbor-report.txt", text.encode())
    sent = llm.complete.await_args.kwargs["prompt"]
    assert text[: da.SUMMARY_READ_CHARS] in sent
    assert (text[: da.SUMMARY_READ_CHARS] + "h") not in sent or length <= da.SUMMARY_READ_CHARS
    line = result.metadata.get("summary_coverage")
    if covered:
        assert line == (
            "This summary covers the first 3,000 characters of a document of 7,486 characters."
        )
    else:
        assert line is None


@pytest.mark.asyncio
async def test_no_sentence_when_the_model_made_no_summary(tmp_path):
    path = tmp_path / "long.txt"
    data = b"x" * 9000
    path.write_bytes(data)
    with patch("services.file_context.storage.read_file_from_storage", return_value=data):
        offline = await da.DocumentAnalyzer(llm_client=None).analyze(str(path), user_id=None)
        failing = AsyncMock()
        failing.complete.side_effect = RuntimeError("down")
        failed = await da.DocumentAnalyzer(llm_client=failing).analyze(str(path), user_id=None)
    assert "summary_coverage" not in offline.metadata
    assert "summary_coverage" not in failed.metadata


def test_the_prompt_tells_the_model_not_to_describe_the_whole():
    from services.prompts import get_json_summary_prompt

    prompt = get_json_summary_prompt()
    assert "may be only the first part of a longer document" in prompt
    assert "total length, size, page count or number of sections" in prompt


# --- the handlers ----------------------------------------------------------------------

REFUSED = {
    "file_id": "f-1",
    "filename": "garden-notes.docx",
    "summary": da.DOCX_UNREADABLE_LINE,
    "key_findings": [],
    "recommendations": [],
    "refusal": True,
    "coverage": None,
}
MARKDOWN = (
    "# Harbor Cleanup Report\n\n**Document Type:** report\n\n## Key Findings\n\n"
    "- Volunteers logged each bag\n- Totals rose by section\n\n"
)
COVERAGE = "This summary covers the first 3,000 characters of a document of 7,486 characters."
READ = {
    "file_id": "f-2",
    "filename": "harbor-report.pdf",
    "summary": MARKDOWN,
    "key_findings": ["Volunteers logged each bag", "Totals rose by section"],
    "recommendations": [],
    "refusal": False,
    "coverage": COVERAGE,
}
_ANALYZE = "services.intent_service.document_handlers.handle_analyze_document"


@pytest.mark.asyncio
@pytest.mark.parametrize("fmt", ["bullet", "paragraph", "detailed"])
async def test_summarize_hands_a_refusal_back_untouched(fmt):
    """On beta the old line was split at its full stop into two bullets."""
    with patch(_ANALYZE, AsyncMock(return_value=dict(REFUSED))):
        out = await document_handlers.handle_summarize_document("f-1", fmt, _USER)
    assert out["summary"] == da.DOCX_UNREADABLE_LINE and out["refusal"] is True
    assert "- " not in out["summary"] and "Key Findings" not in out["summary"]


@pytest.mark.asyncio
@pytest.mark.parametrize("fmt", ["bullet", "paragraph", "detailed"])
async def test_summarize_puts_the_sentence_above_and_the_findings_once(fmt):
    with patch(_ANALYZE, AsyncMock(return_value=dict(READ))):
        out = await document_handlers.handle_summarize_document("f-2", fmt, _USER)
    assert out["summary"].startswith(COVERAGE + "\n\n# Harbor Cleanup Report")
    assert out["summary"].count("Volunteers logged each bag") == 1
    assert out["refusal"] is False


def test_findings_are_added_only_when_the_summary_does_not_hold_them():
    keep = document_handlers.findings_not_already_in
    assert keep(MARKDOWN, READ["key_findings"]) == []
    assert keep("Plain prose summary.", ["A finding"]) == ["A finding"]
    assert keep(MARKDOWN, ["Volunteers logged each bag", "Something else"]) == [
        "Volunteers logged each bag",
        "Something else",
    ]
    assert keep("", []) == []


@pytest.mark.asyncio
async def test_the_handler_passes_the_analyzers_notes_through():
    result = MagicMock()
    result.summary, result.key_findings, result.recommendations = "s", [], []
    result.generated_at.isoformat.return_value = "t"
    result.metadata = {"refusal": True, "summary_coverage": COVERAGE}
    assert document_handlers._reading_notes(result) == {"refusal": True, "coverage": COVERAGE}
    result.metadata = {"text": "x"}
    assert document_handlers._reading_notes(result) == {"refusal": False, "coverage": None}


# --- the two replies -------------------------------------------------------------------


@asynccontextmanager
async def _fake_scope():
    yield MagicMock()


async def _summarize_reply(analysis):
    from services.file_context.file_resolver import FileResolver as real
    from services.intent_service.workflow_entries import run_summarize_document_workflow

    resolver = MagicMock()
    resolver.is_temporal_reference = real.is_temporal_reference
    resolver.temporal_window_days = real.temporal_window_days
    resolver.return_value.list_owner_documents = AsyncMock(return_value=[])
    resolver.return_value.resolve_file_reference = AsyncMock(return_value=("f-1", 0.95))
    intent = Intent(
        category=IntentCategory.SYNTHESIS,
        action="summarize_document",
        original_message="summarize it",
        confidence=0.9,
        context={"original_message": "summarize it", "source_type": "document"},
    )
    with (
        patch("services.database.session_factory.AsyncSessionFactory.session_scope", _fake_scope),
        patch("services.repositories.file_repository.FileRepository", MagicMock()),
        patch("services.file_context.file_resolver.FileResolver", resolver),
        patch(_ANALYZE, AsyncMock(return_value=dict(analysis))),
    ):
        return await run_summarize_document_workflow(
            session_id="s", user_id=_USER, context={"intent": intent}
        )


@pytest.mark.asyncio
async def test_the_summarize_reply_for_a_file_not_read_is_the_sentence_alone():
    result = await _summarize_reply(REFUSED)
    assert result.message == da.DOCX_UNREADABLE_LINE
    assert "Here's my summary" not in result.message and "\n" not in result.message
    assert result.success is False
    assert result.intent_data["context"]["reason"] == "document_not_readable"


@pytest.mark.asyncio
async def test_the_summarize_reply_says_what_part_it_read():
    result = await _summarize_reply(READ)
    assert result.message.startswith(f"Here's my summary of harbor-report.pdf:\n\n{COVERAGE}\n\n")
    assert result.message.count("Volunteers logged each bag") == 1


@pytest.fixture
def intent_service():
    from services.intent.intent_service import IntentService

    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


async def _analyze_reply(intent_service, analysis):
    message = "Analyze harbor-report.pdf"
    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_document",
        original_message=message,
        context={"original_message": message, "user_id": _USER},
    )
    held = AsyncMock(return_value=[{"file_id": analysis["file_id"], "filename": None}])
    with (
        patch("services.intent_service.document_handlers.resolve_held_files", held),
        patch(_ANALYZE, AsyncMock(return_value=dict(analysis))),
    ):
        return await intent_service._analyze_bound_held_file(intent, "wf")


@pytest.mark.asyncio
async def test_the_analyze_reply_for_a_file_not_read_is_the_sentence_alone(intent_service):
    result = await _analyze_reply(intent_service, REFUSED)
    assert result.message == da.DOCX_UNREADABLE_LINE
    assert "I read" not in result.message and result.success is False


@pytest.mark.asyncio
async def test_the_analyze_reply_says_what_part_it_read_and_lists_findings_once(intent_service):
    result = await _analyze_reply(intent_service, READ)
    assert result.message.startswith(
        f"I read 'harbor-report.pdf' from your files.\n\n{COVERAGE}\n\n**Summary:**\n"
    )
    assert result.message.count("Volunteers logged each bag") == 1
    assert "**Key findings:**" not in result.message
    assert result.success is True


@pytest.mark.asyncio
async def test_the_analyze_reply_still_lists_findings_the_summary_lacks(intent_service):
    plain = {**READ, "summary": "A short prose summary.", "coverage": None}
    result = await _analyze_reply(intent_service, plain)
    assert "**Key findings:**\n- Volunteers logged each bag" in result.message
    assert COVERAGE not in result.message
