"""mail4.py reads every message in one `git cat-file --batch` process, and `inbox --ids` takes
several roles in one call. Before 2026-11-23 it ran one `git show` per message: 55 s per inbox call
at 2,145 messages, and Pard's mail-wake pass took about 17 minutes (Pard's memo, 11-23)."""

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture
def repo(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("mail4", ROOT / "scripts" / "mail4.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    g = lambda *a: subprocess.run(["git", "-C", str(tmp_path), *a], check=True, capture_output=True)  # noqa: E731
    g("init", "-q")
    g("config", "user.email", "t@example.invalid")
    g("config", "user.name", "t")
    files = {
        "messages/2026/11/23/A1.md": "---\nid: A1\nfrom: lead\nto: [cio]\ncc: [arch]\nsent_at: '2026-11-23T10:00:00-08:00'\n---\nBody one.\n",
        "messages/2026/11/23/B2.md": "---\nid: B2\nfrom: arch\nto: [lead]\ncc: []\nsent_at: '2026-11-23T10:01:00-08:00'\n---\nÜnïcode body\n\nwith a blank line and no final newline",
        "messages/2026/11/23/notes.txt": "not a message",
        "acks/arch.log": "A1 2026-11-23T10:05 read\n",
    }
    for p, t in files.items():
        f = tmp_path / p
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(t)
    g("add", "-A")
    g("commit", "-q", "-m", "seed")
    monkeypatch.setattr(mod, "REPO", tmp_path)
    tip = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    monkeypatch.setattr(mod, "fetch_tip", lambda: tip)
    return mod, tip


def test_batch_read_matches_git_show_byte_for_byte(repo):
    mod, tip = repo
    paths = ["messages/2026/11/23/A1.md", "messages/2026/11/23/B2.md", "messages/nope.md"]
    got = mod.show_many(tip, paths)
    assert got["messages/nope.md"] is None
    for p in paths[:2]:
        assert got[p] == mod.show(tip, p)


def test_all_messages_reads_only_md_files_with_an_id(repo):
    mod, tip = repo
    msgs = mod.all_messages(tip)
    assert sorted(m["id"] for m in msgs) == ["A1", "B2"]
    assert next(m for m in msgs if m["id"] == "B2")["_body"].startswith("Ünïcode body")


def test_inbox_ids_for_several_roles_prints_role_and_id(repo, capsys):
    mod, _ = repo
    a = mod.build_parser().parse_args(["inbox", "--role", "cio,arch,lead", "--ids"])
    assert mod.cmd_inbox(a) == 0
    # arch acked A1; cio has A1; lead has B2
    assert capsys.readouterr().out.splitlines() == ["cio A1", "lead B2"]


def test_several_roles_without_ids_is_refused(repo, capsys):
    mod, _ = repo
    a = mod.build_parser().parse_args(["inbox", "--role", "cio,arch"])
    assert mod.cmd_inbox(a) == 2


def test_one_role_ids_output_is_unchanged(repo, capsys):
    mod, _ = repo
    a = mod.build_parser().parse_args(["inbox", "--role", "lead", "--ids"])
    assert mod.cmd_inbox(a) == 0
    assert capsys.readouterr().out.splitlines() == ["B2"]
