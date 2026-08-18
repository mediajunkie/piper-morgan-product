"""#1656 — /files upload must work end-to-end on the real server.

WHAT THIS VERIFIES (m-43 — name the layer):
  Real-server HTTP layer, the same surface files.html's uploadOneFile() JS
  drives: a real multipart POST to /api/v1/files/upload with the real
  auth_token cookie from a real login, through every middleware, the auth
  dependency, the #1306 encrypt seam, and the uploaded_files DB write.
  Then the read side: /list shows the row, /{id}/preview returns the exact
  content (decrypt seam), and a SECOND upload works (PM's report was "error
  on EVERY attempt" — one success is not the fix's bar).

WHAT IT DOES NOT VERIFY:
  - The browser JS itself (FormData construction, toast rendering) — this
    harness drives HTTP, it does not execute JS. The request shape below is
    a faithful copy of uploadOneFile()'s (multipart field named "file",
    cookie auth, no extra headers).
  - Fly-environment realities (the /data volume mount, UPLOAD_DIR
    resolution on the machine) — local UPLOAD_DIR default is `uploads/`.
    A prod-only mount failure needs a prod check.

Context: this path had ZERO live coverage before #1656 — which is how it
rotted unnoticed. This file is the permanent tripwire.

Issue: #1656
"""

import uuid

import pytest

UPLOAD_PATH = "/api/v1/files/upload"
LIST_PATH = "/api/v1/files/list"


def _upload(driver, filename: str, content: bytes, content_type: str):
    """Multipart POST shaped exactly like files.html uploadOneFile():
    one field named "file", cookie auth, nothing else."""
    return driver.post(
        UPLOAD_PATH,
        files={"file": (filename, content, content_type)},
        timeout=30.0,
    )


@pytest.mark.live
class TestFilesUploadLive:
    def test_upload_lands_row_listing_shows_it_and_second_upload_works(self, turn_driver):
        """The #1656 repro-then-proof: upload → 200 + row; listing shows it;
        preview returns the exact bytes back (decrypt seam); second upload
        also succeeds; delete cleans up (row AND bytes)."""
        marker = uuid.uuid4().hex[:8]
        name_1 = f"live-1656-{marker}-first.md"
        body_1 = f"# live 1656 upload {marker}\n\nfirst file content.\n".encode()

        # --- Upload 1: the failing assertion IS the repro ---
        resp = _upload(turn_driver, name_1, body_1, "text/markdown")
        assert resp.status_code == 200, (
            f"POST {UPLOAD_PATH} returned HTTP {resp.status_code} — this is "
            f"the #1656 defect surface (PM: error on every attempt). "
            f"Body: {resp.text[:800]}"
        )
        uploaded = resp.json()
        file_id_1 = uploaded.get("file_id")
        assert file_id_1, f"200 but no file_id in body: {resp.text[:500]}"
        assert uploaded.get("filename") == name_1
        assert uploaded.get("size") == len(body_1)

        # --- Listing shows the row (what the Files page renders from) ---
        listing = turn_driver.get(LIST_PATH, timeout=30.0)
        assert listing.status_code == 200, (
            f"GET {LIST_PATH} returned HTTP {listing.status_code}: " f"{listing.text[:500]}"
        )
        files = listing.json().get("files", [])
        match = [f for f in files if f.get("file_id") == file_id_1]
        assert match, (
            f"Uploaded file {file_id_1} absent from {LIST_PATH} " f"({len(files)} entries returned)"
        )
        assert match[0]["filename"] == name_1

        # --- Content is retrievable and EXACT (through the decrypt seam) ---
        preview = turn_driver.get(f"/api/v1/files/{file_id_1}/preview", timeout=30.0)
        assert (
            preview.status_code == 200
        ), f"Preview returned HTTP {preview.status_code}: {preview.text[:500]}"
        pbody = preview.json()
        assert pbody.get("previewable") is True, f"not previewable: {pbody}"
        assert (
            pbody.get("content") == body_1.decode()
        ), "Preview content does not round-trip the uploaded bytes"

        # --- Upload 2: 'every attempt' means the SECOND one must work too ---
        name_2 = f"live-1656-{marker}-second.txt"
        body_2 = f"second live-1656 file {marker}\n".encode()
        resp2 = _upload(turn_driver, name_2, body_2, "text/plain")
        assert (
            resp2.status_code == 200
        ), f"Second upload returned HTTP {resp2.status_code}: {resp2.text[:800]}"
        file_id_2 = resp2.json().get("file_id")
        assert file_id_2 and file_id_2 != file_id_1

        listing2 = turn_driver.get(LIST_PATH, timeout=30.0)
        ids = {f.get("file_id") for f in listing2.json().get("files", [])}
        assert {file_id_1, file_id_2} <= ids, f"Listing after second upload missing rows: has {ids}"

        # --- Delete both via the API (removes bytes from disk too; the
        #     count-verified user teardown then proves the rows are gone) ---
        for fid in (file_id_1, file_id_2):
            deleted = turn_driver.delete(f"/api/v1/files/{fid}", timeout=30.0)
            assert deleted.status_code == 200, (
                f"DELETE /api/v1/files/{fid} returned "
                f"HTTP {deleted.status_code}: {deleted.text[:500]}"
            )
