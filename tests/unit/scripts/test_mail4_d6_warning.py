"""mail4.py's ADR-084 D6 warning: a ruling-relay that puts a step on xian names the standing
access that would remove it. The check warns; it never stops a send."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture(scope="module")
def mail4():
    spec = importlib.util.spec_from_file_location("mail4", ROOT / "scripts" / "mail4.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize(
    "body",
    [
        "xian pastes one line in Terminal, then Lead checks.",
        "Step D is one paste, after HOST's read.",
        "This stays his hand until the key exists.",
        "Xian runs `scripts/redis_password_rotate.py` once.",
        "The connect is xian's console.",
        # the v4 review's misses and hits (2026-11-23)
        "The OpenAI run or the beta key read. That step is xian's.",
        "Exec (copied): that is the one step here that needs xian.",
        "Before the first chat turn, xian confirms on his console that the key sits there.",
    ],
)
def test_a_relay_with_a_step_for_xian_and_no_standing_access_line_warns(mail4, body):
    warning = mail4.d6_warning("ruling-relay", body)
    assert warning and "D6" in warning and "Sent anyway" in warning


@pytest.mark.parametrize(
    "kind, body",
    [
        (
            "ruling-relay",
            "xian pastes one line. The standing access that would end it: a seat key.",
        ),
        (
            "ruling-relay",
            "xian runs it once (D6: none exists, because it changes a production secret).",
        ),
        ("ruling-relay", "xian said yes to the ADR and the budget."),  # a ruling, no step
        ("ruling-relay", "Lead builds it; HOST reads it; no step for anyone else."),
        # the v4 review's false hits (2026-11-23): a verb near xian is not a step on him
        ("ruling-relay", "That comes under xian's 11-13 yes for 2364's runs."),
        ("ruling-relay", "That includes xian's own edits to his PIPER.md context."),
        ("ruling-relay", "Figures as Janus transcribed them from his console screenshots."),
        (
            "ruling-relay",
            "xian said yes to the promote-gate change, and gave a standing word for edits.",
        ),
        ("task", "xian pastes one line in Terminal."),  # only relays are checked
        ("fyi", "This stays his hand."),
    ],
)
def test_no_warning_when_the_line_is_there_or_nothing_is_asked_of_xian(mail4, kind, body):
    assert mail4.d6_warning(kind, body) is None


def test_the_warning_never_stops_the_send(mail4):
    text = (ROOT / "scripts" / "mail4.py").read_text()
    at = text.index("warning = d6_warning(a.type, body)")
    following = text[at : at + 200]
    assert "print(warning, file=sys.stderr)" in following and "return" not in following
