"""#313: drag & drop upload — files.html markup contract.

Live behavior (drop → POST /upload → list refresh) verified via browser UAT;
these guard the template wiring (overlay, handlers, shared upload helper).
"""

from pathlib import Path

import pytest


@pytest.fixture
def files_html() -> str:
    return (Path(__file__).resolve().parents[3] / "templates" / "files.html").read_text()


def test_drop_overlay_present(files_html):
    assert 'id="drop-overlay"' in files_html
    assert "Drop files to upload" in files_html


def test_dragdrop_handlers_wired(files_html):
    assert "function initDragDropUpload(" in files_html
    assert "initDragDropUpload();" in files_html  # called on DOMContentLoaded
    for evt in ("dragenter", "dragover", "dragleave", "drop"):
        assert f"addEventListener('{evt}'" in files_html


def test_shared_upload_helper_used_by_dialog_and_drop(files_html):
    assert "async function uploadOneFile(" in files_html
    # Both call sites use it.
    assert files_html.count("uploadOneFile(") >= 3  # def + dialog + drop loop
