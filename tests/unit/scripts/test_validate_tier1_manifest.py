"""Pins for scripts/validate_tier1_manifest.py (#2355, Tier 1 corpus manifest).

Concept: docs/internal/design/tier1-corpus-manifest.md
"""

import csv
import importlib.util
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts" / "validate_tier1_manifest.py"


@pytest.fixture()
def v(monkeypatch):
    monkeypatch.chdir(ROOT)
    spec = importlib.util.spec_from_file_location("validate_tier1_manifest", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _temp_manifest(mod, edit):
    with open(mod.PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    idx = {n: rows[0].index(n) for n in rows[0]}
    for r in rows[1:]:
        edit(r, idx)
    tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="")
    csv.writer(tmp, lineterminator="\n").writerows(rows)
    tmp.close()
    return tmp.name


def test_real_manifest_passes_deploy_gate(v):
    assert v.main(["--deploy"]) == 0


def test_offered_names_equal_the_imported_dicts(v):
    """Lead's pin: the names the checker reads by ast equal the real dicts' values."""
    svc = pytest.importorskip("services.integrations.integration_status_service")
    expected = set(svc.BETA_OFFERED_CONNECTORS.values()) | set(
        svc.STAGING_ONLY_OFFERED_CONNECTORS.values()
    )
    assert v.offered_names() == expected


def test_stale_verified_row_drops_and_does_not_refuse(v, capsys):
    def edit(r, i):
        if r[i["id"]] == "d-known-limits":
            r[i["status"]], r[i["last_verified"]] = "verified", "2026-01-01"

    v.PATH = _temp_manifest(v, edit)
    assert v.main(["--deploy"]) == 0
    assert "DROP  d-known-limits" in capsys.readouterr().out


def test_indexed_item_on_excluded_path_refuses_deploy(v):
    def edit(r, i):
        if r[i["id"]] == "b-connectors":
            r[i["item"]], r[i["status"]] = "dev/2026/11/13/x.md", "verified"

    v.PATH = _temp_manifest(v, edit)
    assert v.main(["--deploy"]) == 1


def _git(cwd, *args):
    import subprocess

    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_approval_survives_a_deleted_line_but_not_a_new_one(v, tmp_path, monkeypatch):
    """Arch, 11-13: every non-blank line of the current item must appear at the approved sha."""
    _git(tmp_path, "init", "-q")
    item = tmp_path / "item.md"
    item.write_text("# Title\n\nline one\nline two\n")
    _git(tmp_path, "add", "item.md")
    _git(tmp_path, "commit", "-qm", "approved text")
    sha = _git(tmp_path, "rev-parse", "HEAD")
    monkeypatch.chdir(tmp_path)
    assert v.approved_text_ok(sha, "item.md") is True
    item.write_text("# Title\n\nline one\n")  # a deletion keeps the approval
    assert v.approved_text_ok(sha, "item.md") is True
    item.write_text("# Title\n\nline one\nline three\n")  # new words need a new approval
    assert v.approved_text_ok(sha, "item.md") is False
    assert v.approved_text_ok("0" * 40, "item.md") is None  # no history: skipped, not failed


def test_verified_row_without_approval_drops(v, capsys):
    def edit(r, i):
        if r[i["id"]] == "b-connectors":
            r[i["status"]], r[i["last_verified"]], r[i["voice_pass"]] = (
                "verified",
                "2026-11-13",
                "passed",
            )

    v.PATH = _temp_manifest(v, edit)
    assert v.main(["--deploy"]) == 0
    assert "b-connectors: verified but not approved" in capsys.readouterr().out


def test_unreadable_approval_drops_an_item_but_fails_a_stand_in_build(v, capsys):
    """Arch, 11-13: an item with an unreadable approval is a DROP, the stand-ins file is exit 1."""

    def edit_item(r, i):
        if r[i["id"]] == "b-connectors":
            r[i["status"]], r[i["last_verified"]] = "verified", "2026-11-13"
            r[i["voice_pass"]], r[i["approved"]] = "passed", "0" * 40

    v.PATH = _temp_manifest(v, edit_item)
    assert v.main(["--deploy"]) == 0
    assert "b-connectors: approval can't be checked" in capsys.readouterr().out

    def edit_stand_in(r, i):
        if r[i["id"]] == "s-stand-ins":
            r[i["approved"]] = "0" * 40

    v.PATH = _temp_manifest(v, edit_stand_in)
    assert v.main(["--deploy"]) == 1
