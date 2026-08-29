"""#1657 live — 'summarize <the document the Files page shows>' works for AGED rows.

WHAT LAYER THIS VERIFIES (m-43): real-turn HTTP. A real server process, a real
login, and the exact turn PM typed on 2026-08-18 — driven against rows seeded
the way PM's actual data looks, which is the shape every fresh fixture misses
(the m-44 education in the issue):

  - The artifact row is a YEAR-OLD generated artifact with NO title and
    PLAINTEXT content (pre-#358-B legacy passthrough shape) — its /files name
    is the id projection ('artifact-XXXXXXXX.md'), which is what the user
    types back at the chat.
  - The uploaded_files row is a YEAR-OLD upload whose storage file is
    PLAINTEXT on disk (pre-#1306, no PMENC1 marker — the legacy read-through
    branch), reference_count 0, last_referenced NULL.

Pre-fix, the artifact turn answered "I don't see any uploaded documents I can
summarize" while the Files listing showed the document — table divergence: the
listing reads uploaded_files ∪ generated artifacts, the resolver read
uploaded_files alone.

LLM marking: chat summarize is LLM-lane only (the pre-classifier declines
summarize phrasings — action_registry.py #1624 note), so these turns REQUIRE a
real classifier credential in the server. Marked @llm accordingly; they run
where KeychainService has a real Anthropic key (dev laptop), and are excluded
from -m "not llm" runs by construction.

USAGE (evidence runs):
    PIPER_LIVE=1 POSTGRES_PORT=5433 venv/bin/python -m pytest \
        tests/live/test_summarize_files_view_1657_live.py -v -s \
        -o addopts="--import-mode=importlib"

Issue: #1657
"""

import io
import os
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from sqlalchemy import text

pytestmark = [pytest.mark.live, pytest.mark.llm]

_HONEST_EMPTY = "I don't see any uploaded documents"


def _year_ago() -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=365)


def _make_text_pdf(path: Path) -> int:
    """Write a REAL one-page PDF with extractable text — plaintext on disk
    (no PMENC1 marker), i.e. the pre-#1306 legacy storage shape the seam's
    read side passes through unchanged."""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    y = 700
    for line in (
        "Q3 Roadmap 2025",
        "Phase one hardens authentication and session ownership.",
        "Phase two ships the beta to alpha testers.",
        "Phase three collects feedback and cuts the production release.",
        "Primary risk: credential provisioning drift between hosts.",
    ):
        c.drawString(72, y, line)
        y -= 24
    c.showPage()
    c.save()
    data = buf.getvalue()
    path.write_bytes(data)  # deliberate raw write: seeding legacy plaintext
    return len(data)


async def _seed_aged_artifact(db, owner_id: str) -> str:
    """A year-old generated artifact, no title, plaintext content — PM's row
    shape. Returns the artifact id (the /files filename derives from it)."""
    artifact_id = str(uuid.uuid4())
    await db.execute(
        text(
            """
            INSERT INTO artifacts
                (id, owner_id, content, source_type, lifecycle_state,
                 source_conversation_id, payload, created_at, updated_at)
            VALUES
                (:id, :owner, :content, 'generated', NULL, NULL, NULL, :old, :old)
            """
        ),
        {
            "id": artifact_id,
            "owner": owner_id,
            "content": (
                "# Beta launch notes\n\n"
                "The beta gates on live verification of the summarize rail, "
                "credential provisioning on the always-on host, and honest "
                "degradation copy for every empty state.\n"
            ),
            "old": _year_ago(),
        },
    )
    await db.commit()
    return artifact_id


async def _seed_aged_upload(db, owner_id: str, storage_path: Path, size: int) -> str:
    """A year-old uploaded_files row: reference_count 0, last_referenced NULL,
    plaintext storage file — the aged-survivor shape fresh fixtures never take."""
    file_id = str(uuid.uuid4())
    await db.execute(
        text(
            """
            INSERT INTO uploaded_files
                (id, filename, file_type, file_size, storage_path, upload_time,
                 last_referenced, reference_count, file_metadata, owner_id)
            VALUES
                (:id, :fn, 'application/pdf', :size, :path, :old,
                 NULL, 0, NULL, CAST(:owner AS uuid))
            """
        ),
        {
            "id": file_id,
            "fn": "q3-roadmap-2025.pdf",
            "size": size,
            "path": str(storage_path),
            "old": _year_ago(),
            "owner": owner_id,
        },
    )
    await db.commit()
    return file_id


@pytest.mark.live
class TestSummarizeSeesTheFilesView1657:
    async def test_aged_untitled_artifact_summarizes_by_its_listed_name(
        self, turn_driver, live_db_session
    ):
        """THE #1657 repro: the account's only document is a year-old untitled
        artifact. The Files listing shows 'artifact-XXXXXXXX.md'; typing
        'summarize artifact-XXXXXXXX.md' must summarize it — not honest-empty."""
        artifact_id = await _seed_aged_artifact(live_db_session, turn_driver.user.user_id)
        filename = f"artifact-{artifact_id[:8]}.md"

        # The listing half of the divergence, measured live first: the /files
        # endpoint must show exactly this document for this account.
        listing = turn_driver.get("/api/v1/files/list").json()
        listed_names = [f["filename"] for f in listing.get("files", [])]
        assert filename in listed_names, (
            f"Precondition failed: /files does not list {filename} "
            f"(got {listed_names}) — the seeded row doesn't reproduce the "
            "listing half of the #1657 divergence."
        )

        body = turn_driver.turn(f"summarize {filename}")
        msg = body.get("message", "")
        assert _HONEST_EMPTY not in msg, (
            f"WRONG-EMPTY still live: the Files listing shows {filename} but "
            f"the summarize turn answered {msg[:200]!r} — the #1657 divergence "
            "is not fixed."
        )
        assert (
            f"Here's my summary of {filename}" in msg
        ), f"Turn did not reach the summarize rail for {filename}: {msg[:300]!r}"
        # A summary of THIS artifact, not boilerplate: the content is about a
        # beta launch; the summary must carry some of it.
        assert len(msg) > len(f"Here's my summary of {filename}:") + 20

    async def test_aged_plaintext_upload_summarizes_via_the_real_handler(
        self, turn_driver, live_db_session
    ):
        """A year-old uploaded_files row (plaintext storage, never referenced)
        must resolve by its exact filename and summarize through the REAL
        handle_summarize_document → DocumentAnalyzer path."""
        tmp_dir = Path(tempfile.mkdtemp(prefix="piper-1657-"))
        pdf_path = tmp_dir / f"{uuid.uuid4()}.pdf"
        size = _make_text_pdf(pdf_path)
        try:
            await _seed_aged_upload(live_db_session, turn_driver.user.user_id, pdf_path, size)

            body = turn_driver.turn("summarize q3-roadmap-2025.pdf")
            msg = body.get("message", "")
            assert _HONEST_EMPTY not in msg, (
                "WRONG-EMPTY on an aged uploaded_files row: " f"{msg[:200]!r}"
            )
            assert (
                "Here's my summary of q3-roadmap-2025.pdf" in msg
            ), f"Turn did not summarize the aged upload: {msg[:300]!r}"
            # The analyzer read the real bytes (legacy plaintext read-through):
            # a failed read produces the corrupted-PDF copy, which must not pass.
            assert "Unable to analyze PDF document" not in msg
            assert "Summary generation failed" not in msg
        finally:
            try:
                os.unlink(pdf_path)
                os.rmdir(tmp_dir)
            except OSError:
                pass
