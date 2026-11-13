"""#2362 (Arch's ruling, 2026-11-12): the URL redaction filter lives on handlers.

A filter on a logger applies only to records logged on that logger. Until this fix the
filter sat on the root logger alone, so a line from any other logger reached the root's
handler with its ``key=`` value intact. Measured on 2026-11-12; that measurement is the
first test here.
"""

from __future__ import annotations

import io
import json
import logging
import subprocess
import sys
from pathlib import Path

import pytest

from services.infrastructure.logging import url_redaction as ur

ROOT = Path(__file__).resolve().parents[4]
LINE = "GET https://example.invalid/v1?key=NOT-A-REAL-VALUE-123&plain=ok done"


@pytest.fixture(autouse=True)
def _leave_other_handlers_as_found():
    """These tests install the filter on every handler that exists, pytest's own
    capture handlers included. Take off whatever was added, so the rest of the run
    sees the handlers it had."""
    before = {id(h): list(h.filters) for _owner, h in ur._all_handlers()}
    root_filters = list(logging.getLogger().filters)
    yield
    for _owner, handler in ur._all_handlers():
        if id(handler) in before:
            handler.filters[:] = before[id(handler)]
    logging.getLogger().filters[:] = root_filters


@pytest.fixture
def root_stream():
    """A fresh handler on the root, removed afterwards."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(name)s %(message)s"))
    root = logging.getLogger()
    root.addHandler(handler)
    yield stream, handler
    root.removeHandler(handler)


def test_a_child_loggers_line_is_redacted_in_the_root_handlers_output(root_stream):
    stream, _handler = root_stream
    ur.install_root_redaction_filter()
    logging.getLogger("some.library.2362").warning(LINE)
    logging.getLogger().warning(LINE)
    text = stream.getvalue()
    assert "NOT-A-REAL-VALUE-123" not in text
    assert text.count("key=[REDACTED]") == 2 and "plain=ok" in text


def test_the_old_shape_really_did_leak():
    """The defect, kept as a test so the reason for the handler filter stays visible:
    with the filter on a parent LOGGER only, a child logger's line is not redacted.
    A private parent stands in for the root, so no other handler in this test run
    (which may carry the filter and redacts the shared record in place) takes part."""
    parent = logging.getLogger("oldshape2362")
    parent.propagate = False
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    parent.addHandler(handler)
    parent.addFilter(ur.URLRedactionFilter())
    try:
        logging.getLogger("oldshape2362.child").warning(LINE)
        parent.warning(LINE)
    finally:
        parent.removeHandler(handler)
    lines = stream.getvalue().splitlines()
    assert "NOT-A-REAL-VALUE-123" in lines[0]  # the child's line: the filter never ran
    assert "NOT-A-REAL-VALUE-123" not in lines[1]  # the parent's own line: it did


def test_every_handler_carries_the_filter_after_install_including_non_propagating_ones():
    lonely = logging.getLogger("non.propagating.2362")
    lonely.propagate = False
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    lonely.addHandler(handler)
    try:
        assert "non.propagating.2362" in ur.handlers_without_redaction()
        ur.install_handler_redaction_filter()
        assert ur.handlers_without_redaction() == []
        lonely.warning(LINE)
        assert "NOT-A-REAL-VALUE-123" not in stream.getvalue()
        # idempotent: a second install adds nothing
        assert ur.install_handler_redaction_filter() == []
        assert len([f for f in handler.filters if isinstance(f, ur.URLRedactionFilter)]) == 1
    finally:
        lonely.removeHandler(handler)


def _run(code: str) -> dict:
    out = subprocess.run(
        [sys.executable, "-c", code], cwd=str(ROOT), capture_output=True, text=True, timeout=120
    )
    assert out.returncode == 0, out.stderr[-800:]
    marker = [ln for ln in out.stdout.splitlines() if ln.startswith("RESULT ")]
    assert marker, (out.stdout[-400:], out.stderr[-400:])
    result = json.loads(marker[-1][len("RESULT ") :])
    result["all_output"] = out.stdout + out.stderr
    return result


_AFTER_UVICORN = """
import io, json, logging
import uvicorn
from services.infrastructure.logging.url_redaction import (
    handlers_without_redaction, install_handler_redaction_filter,
    install_root_redaction_filter, install_url_redaction_filter,
)
logging.basicConfig(level=logging.WARNING, format="%(message)s")
install_url_redaction_filter()
install_root_redaction_filter()
import services.infrastructure.logging.evidence  # the evidence logger's own handler
async def app(scope, receive, send):
    pass
config = uvicorn.Config(app, host="127.0.0.1", port=0, log_level="info")
before = handlers_without_redaction()
install_handler_redaction_filter()
after = handlers_without_redaction()
owners = sorted({n for n, o in logging.root.manager.loggerDict.items()
                 if isinstance(o, logging.Logger) and o.handlers})
logging.getLogger("uvicorn.access").info(
    '%s - "%s %s HTTP/%s" %d', "127.0.0.1:1", "GET",
    "/cb?key=NOT-A-REAL-VALUE-123&plain=ok", "1.1", 200)
logging.getLogger("uvicorn.error").info("started https://example.invalid/?token=NOT-A-REAL-VALUE-456")
print("RESULT " + json.dumps({"before": before, "after": after, "owners": owners}))
"""


def test_a_process_set_up_like_the_hosts_has_no_unfiltered_handler():
    """The order both entry points use: basicConfig, the two installs, uvicorn.Config
    (which builds the uvicorn and uvicorn.access handlers), then the handler install."""
    result = _run(_AFTER_UVICORN)
    assert result["after"] == [], result
    # uvicorn's handlers exist and were the unfiltered ones before the install
    assert "uvicorn" in result["owners"] and "uvicorn.access" in result["owners"], result
    assert "uvicorn.access" in result["before"], result
    assert "piper.evidence" in result["owners"] and "piper.evidence" not in result["before"]
    assert "NOT-A-REAL-VALUE-123" not in result["all_output"]
    assert "NOT-A-REAL-VALUE-456" not in result["all_output"]
    assert "key=[REDACTED]" in result["all_output"]


def test_both_entry_points_install_on_handlers_after_building_the_server_config():
    for name, config_call in (
        ("main.py", "config = uvicorn.Config("),
        ("main_mcp.py", "config = uvicorn.Config("),
    ):
        src = (ROOT / name).read_text()
        assert config_call in src, name
        after_config = src[src.index(config_call) :]
        assert "install_handler_redaction_filter()" in after_config, name
        serve = "server.serve()" if name == "main.py" else "uvicorn.Server(config).run()"
        assert after_config.index("install_handler_redaction_filter()") < after_config.index(
            serve
        ), name
    mcp = (ROOT / "main_mcp.py").read_text()
    assert "install_root_redaction_filter()" in mcp and "install_url_redaction_filter()" in mcp
    assert "uvicorn.run(" not in mcp  # uvicorn.run would build the handlers out of reach


def test_the_docstring_says_what_the_function_guarantees():
    doc = ur.install_root_redaction_filter.__doc__
    assert "ensures ALL log messages" not in doc
    assert "handler" in doc
