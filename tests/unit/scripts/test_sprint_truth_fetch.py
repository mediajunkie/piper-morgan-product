"""sprint-truth.py fetch(): a capped pull is retried once at the board's total; any mismatch after
that is still refused (query-github-board rule 1). Exec's report 2026-11-20: 2,208 items, cap 2,000."""

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "sprint-truth.py"


def load():
    spec = importlib.util.spec_from_file_location("sprint_truth", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def board(total):
    """A fake `gh project item-list`: returns min(limit, total) items and the true total."""
    calls = []

    def run(cmd, **kw):
        limit = int(cmd[cmd.index("--limit") + 1])
        calls.append(limit)
        n = min(limit, total)
        payload = {"items": [{"id": i} for i in range(n)], "totalCount": total}
        return subprocess.CompletedProcess(cmd, 0, json.dumps(payload), "")

    return run, calls


def test_board_under_cap_is_one_pull(monkeypatch):
    mod = load()
    run, calls = board(1500)
    monkeypatch.setattr(mod.subprocess, "run", run)
    assert len(mod.fetch()) == 1500
    assert calls == [2000]


def test_board_over_cap_refetches_once_at_total(monkeypatch, capsys):
    mod = load()
    run, calls = board(2208)
    monkeypatch.setattr(mod.subprocess, "run", run)
    assert len(mod.fetch()) == 2208
    assert calls == [2000, 2208 + mod.REFETCH_MARGIN]
    assert "pull complete: 2208/2208" in capsys.readouterr().out


def test_explicit_limit_is_the_first_pull(monkeypatch):
    mod = load()
    run, calls = board(2208)
    monkeypatch.setattr(mod.subprocess, "run", run)
    assert len(mod.fetch(3000)) == 2208
    assert calls == [3000]


def test_short_pull_under_the_cap_is_still_refused(monkeypatch):
    """Fewer items than the total while UNDER the cap is not a cap problem; no retry, refuse."""
    mod = load()

    def run(cmd, **kw):
        payload = {"items": [{"id": i} for i in range(1200)], "totalCount": 1280}
        return subprocess.CompletedProcess(cmd, 0, json.dumps(payload), "")

    monkeypatch.setattr(mod.subprocess, "run", run)
    with pytest.raises(SystemExit) as e:
        mod.fetch()
    assert "TRUNCATED PULL: fetched 1200 of 1280" in str(e.value)


def test_refetch_still_short_is_refused(monkeypatch):
    """The board keeps growing past the raised limit: refuse, never summarize a subset."""
    mod = load()
    calls = []

    def run(cmd, **kw):
        limit = int(cmd[cmd.index("--limit") + 1])
        calls.append(limit)
        total = 2208 if len(calls) == 1 else 5000
        payload = {"items": [{"id": i} for i in range(min(limit, total))], "totalCount": total}
        return subprocess.CompletedProcess(cmd, 0, json.dumps(payload), "")

    monkeypatch.setattr(mod.subprocess, "run", run)
    with pytest.raises(SystemExit) as e:
        mod.fetch()
    assert len(calls) == 2
    assert "TRUNCATED PULL" in str(e.value)


def test_missing_total_is_refused(monkeypatch):
    mod = load()

    def run(cmd, **kw):
        return subprocess.CompletedProcess(cmd, 0, json.dumps({"items": [{"id": 1}]}), "")

    monkeypatch.setattr(mod.subprocess, "run", run)
    with pytest.raises(SystemExit) as e:
        mod.fetch()
    assert "no totalCount" in str(e.value)
