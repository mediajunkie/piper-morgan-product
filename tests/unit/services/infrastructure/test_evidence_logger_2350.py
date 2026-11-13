"""#2350 (Arch's ruling, 2026-11-12): operational evidence has its own logger.

The hosts keep the root at WARNING. ``piper.evidence`` is INFO whatever the root is,
writes through its own handler, redacts URLs itself, and its event list is pinned so
moving a line back to a plain logger fails.
"""

from __future__ import annotations

import ast
import io
import logging
from pathlib import Path

import pytest

import services.infrastructure.logging.config  # noqa: F401  (structlog on stdlib, as the app)
from services.infrastructure.logging import evidence as ev

ROOT = Path(__file__).resolve().parents[4]
SCAN = ("services", "web", "cli", "scripts", "main.py", "main_mcp.py")


@pytest.fixture
def captured(monkeypatch):
    """The evidence logger's output, with the root at WARNING as on a host."""
    monkeypatch.setattr(logging.getLogger(), "level", logging.WARNING)
    log = ev.configure_evidence_logger()
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(handler)
    yield stream
    log.removeHandler(handler)


def _py_files():
    for entry in SCAN:
        path = ROOT / entry
        if path.is_file():
            yield path
        else:
            yield from path.rglob("*.py")


def _calls(func_names):
    """(file, lineno, first-arg literal or None, callee text) for matching calls."""
    out = []
    for path in _py_files():
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            callee = ast.unparse(node.func)
            if callee not in func_names:
                continue
            first = node.args[0] if node.args else None
            literal = first.value if isinstance(first, ast.Constant) else None
            out.append((path.relative_to(ROOT).as_posix(), node.lineno, literal, callee))
    return out


def test_evidence_is_info_and_emitted_while_the_root_drops_info(captured, caplog):
    root_stream = io.StringIO()
    root_handler = logging.StreamHandler(root_stream)
    logging.getLogger().addHandler(root_handler)
    try:
        ev.evidence("github_app_background_refresh_pass", seen=3, refreshed=1)
        logging.getLogger("some.library").info("an info line a host would drop")
        logging.getLogger().info("a root info line a host would drop")
    finally:
        logging.getLogger().removeHandler(root_handler)
    assert logging.getLogger(ev.EVIDENCE_LOGGER_NAME).level == logging.INFO
    assert "github_app_background_refresh_pass" in captured.getvalue()
    assert '"seen": 3' in captured.getvalue()
    assert "would drop" not in root_stream.getvalue()
    # written once: it does not also travel to the root's handlers
    assert "github_app_background_refresh_pass" not in root_stream.getvalue()


def test_it_has_its_own_handler_so_an_unconfigured_process_still_writes():
    log = ev.configure_evidence_logger()
    own = [h for h in log.handlers if getattr(h, "piper_evidence_handler", False)]
    assert len(own) == 1 and own[0].level == logging.INFO and log.propagate is False
    ev.configure_evidence_logger()  # idempotent
    assert len([h for h in log.handlers if getattr(h, "piper_evidence_handler", False)]) == 1


def test_a_url_in_an_evidence_line_is_redacted(captured):
    ev.evidence(
        "mcp_rate_limit_backend_active", backend="https://example.invalid/x?key=NOT-A-VALUE-1"
    )
    assert "NOT-A-VALUE-1" not in captured.getvalue()
    assert "key=[REDACTED]" in captured.getvalue()


def test_a_field_named_like_a_value_is_dropped_and_the_drop_is_said(captured):
    ev.evidence(
        "github_app_grant_refreshed",
        owner_id="owner-1",
        access_token="fake-value-not-token-shaped",
        redis_url="redis://example.invalid",
        key_count=2,
    )
    text = captured.getvalue()
    assert "fake-value-not-token-shaped" not in text and "example.invalid" not in text
    assert "owner-1" in text and '"key_count": 2' in text
    assert "evidence_fields_dropped" in text and "access_token" in text


def test_an_unlisted_event_is_still_written_and_flagged(captured):
    ev.evidence("something_new_happened", count=1)
    text = captured.getvalue()
    assert "something_new_happened" in text and "evidence_event_unlisted" in text


def test_it_never_raises(monkeypatch):
    monkeypatch.setattr(ev, "configure_evidence_logger", lambda: 1 / 0)
    ev.evidence("github_app_grant_refreshed", owner_id="x")


def test_the_line_is_valid_json_with_the_event_and_fields(captured):
    import json

    ev.evidence("TokenBlacklist: Redis available", seeded_entries=4)
    line = json.loads(captured.getvalue().strip().splitlines()[-1])
    assert line["event"] == "TokenBlacklist: Redis available" and line["seeded_entries"] == 4
    assert line["logger"] == "piper.evidence" and line["level"] == "info"
    assert line["timestamp"].endswith("Z")


def test_it_does_not_go_through_structlog():
    """Arch, 2026-11-12: the path to the filter and handler must not depend on
    structlog.configure having run first."""
    src = Path(ev.__file__).read_text()
    assert "import structlog" not in src and "structlog.get_logger" not in src


def test_a_bare_process_redacts_a_url_in_an_allowed_field():
    """Arch's test: no logging setup, no structlog configuration, nothing imported
    first. The line is written, and a ``key=`` value in an allowed field is not."""
    import json
    import subprocess
    import sys

    code = (
        "from services.infrastructure.logging.evidence import evidence\n"
        "evidence('mcp_rate_limit_backend_active', "
        "backend='https://example.invalid/x?key=NOT-A-VALUE-1&plain=ok')\n"
    )
    out = subprocess.run(
        [sys.executable, "-c", code], cwd=str(ROOT), capture_output=True, text=True, timeout=60
    )
    assert out.returncode == 0, out.stderr[-500:]
    text = out.stdout + out.stderr
    assert "NOT-A-VALUE-1" not in text
    lines = [ln for ln in text.splitlines() if "mcp_rate_limit_backend_active" in ln]
    assert len(lines) == 1, text[-500:]
    line = json.loads(lines[0])
    assert line["backend"] == "https://example.invalid/x?key=[REDACTED]&plain=ok"


def test_every_evidence_call_uses_a_listed_literal_and_every_listed_event_has_a_site():
    calls = _calls({"evidence"})
    assert calls, "no evidence() call found"
    not_literal = [c for c in calls if c[2] is None]
    assert not_literal == [], f"evidence() needs a literal event name: {not_literal}"
    unlisted = [c for c in calls if c[2] not in ev.EVIDENCE_EVENTS]
    assert unlisted == [], f"add the event to EVIDENCE_EVENTS: {unlisted}"
    used = {c[2] for c in calls}
    assert used == set(ev.EVIDENCE_EVENTS), sorted(set(ev.EVIDENCE_EVENTS) - used)


def test_no_listed_event_is_logged_on_a_plain_logger():
    """Moving an evidence line back to ``logger.info`` puts it under the root's
    WARNING again, where a host drops it."""
    plain = _calls(
        {"logger.info", "logger.debug", "self.logger.info", "log.info", "self.logger.debug"}
    )
    back = [c for c in plain if c[2] in ev.EVIDENCE_EVENTS]
    assert back == [], back


def test_the_host_level_is_an_explicit_setting():
    main = (ROOT / "main.py").read_text()
    assert 'os.getenv("LOG_LEVEL")' in main and '"WARNING"' in main
    fly = (ROOT / "fly.toml").read_text()
    assert 'LOG_LEVEL = "WARNING"' in fly
