"""v4_route_hint.py: since 2026-11-23 a v3 memo whose every party is a mail v4 seat is refused
(exit 2), unless PIPER_V3_FALLBACK names why v4 can't be used. The v4 review:
dev/2026/11/23/mail-v4-review-2026-11-23.md."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
V4 = {"exec", "cio", "lead", "arch", "cxo", "ppm", "comms", "host", "docs", "pa", "web"}


@pytest.fixture
def hint(monkeypatch, tmp_path):
    spec = importlib.util.spec_from_file_location(
        "v4_route_hint", ROOT / "scripts" / "v4_route_hint.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "pilots", lambda: set(V4))
    monkeypatch.delenv("PIPER_V3_FALLBACK", raising=False)
    monkeypatch.chdir(tmp_path)
    return mod


def memo(role, name, front):
    p = Path("mailboxes") / role / "inbox" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"---\n{front}\n---\n\nBody.\n")
    return str(p)


def test_an_all_v4_memo_is_refused(hint, capsys):
    path = memo("lead", "m.md", "from: CIO\nto: Lead\ncc: [arch, exec]")
    assert hint.main([path]) == 2
    assert "REFUSED" in capsys.readouterr().err


def test_the_fallback_reason_lets_it_through_and_prints_the_reason(hint, capsys, monkeypatch):
    monkeypatch.setenv("PIPER_V3_FALLBACK", "mail repo fetch failing")
    path = memo("lead", "m.md", "from: cio\nto: lead")
    assert hint.main([path]) == 0
    err = capsys.readouterr().err
    assert "REFUSED" not in err and "mail repo fetch failing" in err


@pytest.mark.parametrize(
    "front",
    [
        "from: Pard\nto: CIO",  # an agent outside this repo writing in
        "from: cio\nto: spec",  # Spec has no v4 seat
        "from: cio\nto: lead\ncc: janus",  # one outside party is enough
    ],
)
def test_a_memo_with_any_party_off_v4_goes_through(hint, capsys, front):
    assert hint.main([memo("cio", "m.md", front)]) == 0
    assert capsys.readouterr().err == ""


def test_filing_a_read_memo_is_not_checked(hint):
    p = Path("mailboxes/cio/read/m.md")
    p.parent.mkdir(parents=True)
    p.write_text("---\nfrom: lead\nto: cio\n---\n")
    assert hint.main(["mailboxes/cio/inbox/m.md", str(p)]) == 0


def test_no_roles_file_fails_open(hint, monkeypatch):
    monkeypatch.setattr(hint, "pilots", lambda: set())
    assert hint.main([memo("lead", "m.md", "from: cio\nto: lead")]) == 0


def test_mail_send_stops_only_on_exit_2():
    text = (ROOT / "scripts" / "mail-send.sh").read_text()
    at = text.index("v4_route_hint.py")
    block = text[at : at + 200]
    assert "|| V4_RC=$?" in block and '[ "$V4_RC" -eq 2 ]' in block and "exit 2" in block
