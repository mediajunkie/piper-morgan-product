"""#1184: /files artifact rename UI wiring (content assertions).

The rename affordance is artifacts-only, owner-gated, and uses the design-floor
Dialog form-mode (NOT native prompt — #1170 retires those) → owner-scoped
PATCH /api/v1/artifacts/{id}. The PATCH behavior itself is covered by the route
tests (test_artifacts_355) + repo tests (test_artifact_repository_952); these
guard the template wiring so a future edit can't silently drop it.
"""
from pathlib import Path

import pytest


@pytest.fixture
def files_html() -> str:
    return (Path(__file__).resolve().parents[3] / "templates" / "files.html").read_text()


def _rename_handler(files_html: str) -> str:
    assert "function renameArtifact(" in files_html, "renameArtifact handler missing"
    return files_html.split("function renameArtifact(")[1].split("// Utility functions")[0]


def test_rename_button_is_artifacts_only_and_owner_gated(files_html):
    assert "renameArtifact(" in files_html
    # artifacts only (the PATCH endpoint is /api/v1/artifacts) + owner/admin gate
    assert "kind === 'artifact' && (isOwner(file)" in files_html


def test_rename_handler_uses_dialog_form_mode_not_native_prompt(files_html):
    seg = _rename_handler(files_html)
    assert "Dialog.show(" in seg          # design-floor Dialog component...
    assert "mode: 'form'" in seg          # ...in form mode (text input), not native prompt()
    assert "prompt(" not in seg           # explicitly NOT a native prompt (#1170)


def test_rename_patches_owner_scoped_artifacts_endpoint(files_html):
    seg = _rename_handler(files_html)
    assert "method: 'PATCH'" in seg
    assert "/api/v1/artifacts/${artifactId}" in seg
    assert "credentials: 'include'" in seg     # owner cookie travels
    assert "loadFiles()" in seg                # refresh after a successful rename


def test_rename_validates_empty_title(files_html):
    seg = _rename_handler(files_html)
    # empty name keeps the dialog open (returns false), doesn't fire a bad PATCH
    assert "return false" in seg


def test_rename_toast_key_registered():
    toast = (Path(__file__).resolve().parents[3] / "web" / "static" / "js" / "toast-messages.js").read_text()
    assert "file_renamed" in toast
