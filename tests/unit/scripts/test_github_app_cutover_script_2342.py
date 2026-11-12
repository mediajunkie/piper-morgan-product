"""#2342: ``scripts/github_app_cutover.py`` is a thin command over ``run_cutover``: a dry
run unless ``--apply``, counts only, and distinct exit codes for done, refused, error."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from services.connectors import github_app_cutover as cut

_SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "github_app_cutover.py"
_COUNTS = {key: 0 for key in cut.COUNT_KEYS}


@pytest.fixture
def script():
    spec = importlib.util.spec_from_file_location("github_app_cutover_script", _SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_flag_is_a_dry_run(script, monkeypatch, capsys):
    run = AsyncMock(return_value=dict(_COUNTS, seen=2, marked=2))
    monkeypatch.setattr(cut, "run_cutover", run)
    assert script.main([]) == 0
    run.assert_awaited_once_with(apply=False)
    out = capsys.readouterr().out
    assert "DRY RUN" in out and "classic grants found" in out


def test_apply_is_passed_through(script, monkeypatch, capsys):
    run = AsyncMock(return_value=dict(_COUNTS, seen=1, deleted=1, revoke_failed=1))
    monkeypatch.setattr(cut, "run_cutover", run)
    assert script.main(["--apply"]) == 0
    run.assert_awaited_once_with(apply=True)
    assert "APPLIED" in capsys.readouterr().out


def test_a_refusal_exits_2_and_says_nothing_changed(script, monkeypatch, capsys):
    monkeypatch.setattr(
        cut, "run_cutover", AsyncMock(side_effect=cut.CutoverRefused("App mode is off."))
    )
    assert script.main(["--apply"]) == 2
    assert "REFUSED" in capsys.readouterr().out


def test_an_error_exits_1_and_prints_only_its_type(script, monkeypatch, capsys):
    monkeypatch.setattr(
        cut, "run_cutover", AsyncMock(side_effect=RuntimeError("a-value-that-must-not-print"))
    )
    assert script.main([]) == 1
    out = capsys.readouterr().out
    assert "RuntimeError" in out and "a-value-that-must-not-print" not in out
