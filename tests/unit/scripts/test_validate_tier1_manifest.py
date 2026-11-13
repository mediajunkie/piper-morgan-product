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
