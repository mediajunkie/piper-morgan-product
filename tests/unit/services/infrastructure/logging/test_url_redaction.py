"""
Unit tests for URL parameter redaction filter.

Tests that sensitive URL parameters are properly redacted from log messages.
"""

import logging

import pytest

from services.infrastructure.logging.url_redaction import (
    URLRedactionFilter,
    install_root_redaction_filter,
    install_url_redaction_filter,
)


class TestURLRedactionFilter:
    """Tests for the URLRedactionFilter class."""

    @pytest.fixture
    def redaction_filter(self):
        """Create a fresh redaction filter for each test."""
        return URLRedactionFilter()

    def test_redacts_key_parameter(self, redaction_filter):
        """Test that key= parameter is redacted (Gemini API pattern)."""
        message = "https://generativelanguage.googleapis.com/v1/models?key=AIzaSyD123abc456"
        result = redaction_filter.redact_message(message)
        assert result == "https://generativelanguage.googleapis.com/v1/models?key=[REDACTED]"
        assert "AIzaSyD123abc456" not in result

    def test_redacts_api_key_parameter(self, redaction_filter):
        """Test that api_key= parameter is redacted."""
        message = "GET https://api.example.com/data?api_key=sk-secret123&format=json"
        result = redaction_filter.redact_message(message)
        assert "api_key=[REDACTED]" in result
        assert "sk-secret123" not in result
        assert "format=json" in result  # Non-sensitive param preserved

    def test_redacts_token_parameter(self, redaction_filter):
        """Test that token= parameter is redacted."""
        message = "URL: https://api.slack.com/api?token=xoxb-123-456-abc"
        result = redaction_filter.redact_message(message)
        assert "token=[REDACTED]" in result
        assert "xoxb-123-456-abc" not in result

    def test_redacts_access_token_parameter(self, redaction_filter):
        """Test that access_token= parameter is redacted."""
        message = "https://graph.facebook.com/me?access_token=EAABsbCS123"
        result = redaction_filter.redact_message(message)
        assert "access_token=[REDACTED]" in result
        assert "EAABsbCS123" not in result

    def test_redacts_secret_parameter(self, redaction_filter):
        """Test that secret= parameter is redacted."""
        message = "Webhook: https://hooks.example.com?secret=whsec_abc123"
        result = redaction_filter.redact_message(message)
        assert "secret=[REDACTED]" in result
        assert "whsec_abc123" not in result

    def test_redacts_client_secret_parameter(self, redaction_filter):
        """Test that client_secret= parameter is redacted."""
        message = "OAuth: https://oauth.example.com?client_id=abc&client_secret=xyz789"
        result = redaction_filter.redact_message(message)
        assert "client_secret=[REDACTED]" in result
        assert "xyz789" not in result
        assert "client_id=abc" in result  # client_id is not sensitive

    def test_redacts_password_parameter(self, redaction_filter):
        """Test that password= parameter is redacted."""
        message = "https://example.com/login?user=admin&password=hunter2"
        result = redaction_filter.redact_message(message)
        assert "password=[REDACTED]" in result
        assert "hunter2" not in result
        assert "user=admin" in result

    def test_redacts_multiple_sensitive_params(self, redaction_filter):
        """Test that multiple sensitive parameters are all redacted."""
        message = "https://api.example.com?key=key1&api_key=key2&token=tok3"
        result = redaction_filter.redact_message(message)
        assert "key=[REDACTED]" in result
        assert "api_key=[REDACTED]" in result
        assert "token=[REDACTED]" in result
        assert "key1" not in result
        assert "key2" not in result
        assert "tok3" not in result

    def test_case_insensitive_redaction(self, redaction_filter):
        """Test that parameter matching is case-insensitive."""
        message = "https://api.example.com?KEY=secret1&Api_Key=secret2&TOKEN=secret3"
        result = redaction_filter.redact_message(message)
        assert "secret1" not in result
        assert "secret2" not in result
        assert "secret3" not in result

    def test_preserves_non_sensitive_params(self, redaction_filter):
        """Test that non-sensitive parameters are not modified."""
        message = "https://api.example.com?format=json&limit=100&page=2"
        result = redaction_filter.redact_message(message)
        assert result == message  # Unchanged

    def test_handles_empty_message(self, redaction_filter):
        """Test that empty messages are handled gracefully."""
        assert redaction_filter.redact_message("") == ""
        assert redaction_filter.redact_message(None) is None

    def test_handles_message_without_urls(self, redaction_filter):
        """Test that messages without URLs are unchanged."""
        message = "This is a regular log message without any URLs"
        result = redaction_filter.redact_message(message)
        assert result == message

    def test_filter_modifies_log_record(self, redaction_filter):
        """Test that the filter modifies log records in place."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Request to https://api.example.com?key=secret123",
            args=(),
            exc_info=None,
        )

        result = redaction_filter.filter(record)

        assert result is True  # Filter allows record through
        assert "key=[REDACTED]" in record.msg
        assert "secret123" not in record.msg

    def test_filter_handles_args_tuple(self, redaction_filter):
        """Test that filter redacts sensitive data in args tuple."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Request: %s",
            args=("https://api.example.com?token=abc123",),
            exc_info=None,
        )

        redaction_filter.filter(record)

        # 2026-11-13: a string argument is redacted in place and the arguments are kept,
        # so a formatter that reads them still works.
        assert record.args == ("https://api.example.com?token=[REDACTED]",)
        assert "abc123" not in record.getMessage()
        assert record.getMessage() == "Request: https://api.example.com?token=[REDACTED]"

    def test_filter_handles_args_dict(self, redaction_filter):
        """Test that filter redacts sensitive data in args dict."""
        # Create record with empty args first, then set args manually
        # (LogRecord constructor has special handling for dict args)
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Request: %(url)s",
            args=None,
            exc_info=None,
        )
        # Manually set args as dict after construction
        record.args = {"url": "https://api.example.com?api_key=secret"}

        redaction_filter.filter(record)

        assert record.args == {"url": "https://api.example.com?api_key=[REDACTED]"}
        assert record.getMessage() == "Request: https://api.example.com?api_key=[REDACTED]"

    def test_a_format_string_with_a_sensitive_looking_placeholder_still_formats(
        self, redaction_filter
    ):
        """#2362, the defect found when the filter went onto handlers: redacting the
        format string turned ``key=%s`` into ``key=[REDACTED]``, the placeholder was
        gone, and merging the arguments raised TypeError, losing the line."""
        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="test.py",
            lineno=1,
            msg="readback_failed user_id=%s key=%s error=%s",
            args=("u-1", "theme", "db down"),
            exc_info=None,
        )
        assert redaction_filter.filter(record) is True
        message = record.getMessage()  # must not raise
        assert message.startswith("readback_failed user_id=u-1 key=[REDACTED] error=db down")

    def test_a_value_split_between_format_string_and_argument_is_redacted(self, redaction_filter):
        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="test.py",
            lineno=1,
            msg="calling https://example.invalid/v1?token=%s now",
            args=("NOT-A-REAL-VALUE-789",),
            exc_info=None,
        )
        redaction_filter.filter(record)
        assert "NOT-A-REAL-VALUE-789" not in record.getMessage()

    def test_a_malformed_record_is_written_redacted_not_left_raw(self, redaction_filter):
        """Arch, 2026-11-12: when the arguments cannot be merged, the handler would
        print the raw message and arguments in its error report. The filter builds one
        line from both, redacts it and clears the arguments, and never raises."""
        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="test.py",
            lineno=1,
            msg="two placeholders %s %s",
            args=("https://example.invalid/v1?token=NOT-A-REAL-VALUE-321",),
            exc_info=None,
        )
        assert redaction_filter.filter(record) is True
        assert record.args is None
        message = record.getMessage()  # no longer raises
        assert "NOT-A-REAL-VALUE-321" not in message
        assert "two placeholders" in message and "could not be merged" in message

    def test_oauth_code_and_state_are_redacted_as_query_parameters_only(self, redaction_filter):
        """Arch, 2026-11-12: only straight after ``?`` or ``&``, so an ordinary
        ``status_code=200`` or ``state=ready`` survives."""
        line = 'GET /cb?code=NOT-A-CODE-1&state=NOT-A-STATE-2&plain=ok HTTP/1.1" 200'
        out = redaction_filter.redact_message(line)
        assert "NOT-A-CODE-1" not in out and "NOT-A-STATE-2" not in out
        assert out == 'GET /cb?code=[REDACTED]&state=[REDACTED]&plain=ok HTTP/1.1" 200'
        plain = "status_code=200 state=ready code=7 exit_code=0"
        assert redaction_filter.redact_message(plain) == plain

    def test_a_record_with_nothing_to_redact_and_no_arguments_is_untouched(self, redaction_filter):
        payload = {"event": "x"}
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg=payload,
            args=None,
            exc_info=None,
        )
        redaction_filter.filter(record)
        assert record.msg is payload


class TestArgumentsSurviveForFormattersThatReadThem:
    """2026-11-13, served on beta from d5905b6946: the filter set ``record.args`` to
    ``None`` on every record that had arguments. uvicorn's access formatter unpacks
    five arguments, so each request wrote a logging-error traceback where its access
    line should be. No test used that formatter."""

    @pytest.fixture
    def redaction_filter(self):
        return URLRedactionFilter()

    @staticmethod
    def _access_record(path):
        return logging.LogRecord(
            name="uvicorn.access",
            level=logging.INFO,
            pathname="h11_impl.py",
            lineno=1,
            msg='%s - "%s %s HTTP/%s" %d',
            args=("127.0.0.1:50546", "GET", path, "1.1", 200),
            exc_info=None,
        )

    def test_uvicorn_access_formatter_formats_a_filtered_record(self, redaction_filter):
        from uvicorn.logging import AccessFormatter

        record = self._access_record("/health?code=NOT-A-1&state=NOT-A-2&token=NOT-A-3&x=1")
        assert redaction_filter.filter(record) is True
        line = AccessFormatter(
            fmt='%(client_addr)s - "%(request_line)s" %(status_code)s', use_colors=False
        ).format(record)
        assert "NOT-A-" not in line
        assert (
            '"GET /health?code=[REDACTED]&state=[REDACTED]&token=[REDACTED]&x=1 HTTP/1.1" 200'
            in line
        )

    def test_a_record_passing_two_filters_still_formats(self, redaction_filter):
        # The logger's filter and the handler's filter both run on one record.
        from uvicorn.logging import AccessFormatter

        record = self._access_record("/cb?code=NOT-A-1")
        redaction_filter.filter(record)
        URLRedactionFilter().filter(record)
        assert len(record.args) == 5
        line = AccessFormatter(
            fmt='%(client_addr)s - "%(request_line)s" %(status_code)s', use_colors=False
        ).format(record)
        assert "/cb?code=[REDACTED] HTTP/1.1" in line

    def test_an_access_line_with_nothing_sensitive_keeps_its_arguments_untouched(
        self, redaction_filter
    ):
        record = self._access_record("/health")
        before = record.args
        redaction_filter.filter(record)
        assert record.args == before

    def test_a_split_value_is_still_merged(self, redaction_filter):
        record = logging.LogRecord("t", logging.INFO, "t.py", 1, "token=%s", ("NOT-A-1",), None)
        redaction_filter.filter(record)
        assert record.args is None
        assert record.getMessage() == "token=[REDACTED]"

    def test_a_value_in_a_non_string_argument_is_still_merged(self, redaction_filter):
        class Url:
            def __str__(self):
                return "https://x.invalid/v1?key=NOT-A-1"

        record = logging.LogRecord("t", logging.INFO, "t.py", 1, "GET %s", (Url(),), None)
        redaction_filter.filter(record)
        assert record.args is None
        assert record.getMessage() == "GET https://x.invalid/v1?key=[REDACTED]"

    def test_non_string_arguments_are_kept_as_they_were(self, redaction_filter):
        record = logging.LogRecord("t", logging.INFO, "t.py", 1, "%s took %d ms", ("a", 12), None)
        redaction_filter.filter(record)
        assert record.args == ("a", 12)


class TestRedactionIsIdempotent:
    """#2350 (Arch, 2026-11-13): a line can pass through redaction more than once
    (a value redacted before ``json.dumps``, then the logger's and the handler's
    filters over the finished line). A second pass must change nothing."""

    CASES = [
        "https://api.example.com/v1?key=NOT-A-VALUE-1&other=value",
        "https://api.example.com/v1?other=value&api_key=NOT-A-VALUE-1",
        "POST https://x.invalid/t?client_secret=NOT-A-VALUE-1&access_token=NOT-A-VALUE-2 200",
        "https://x.invalid/cb?code=NOT-A-VALUE-1&state=NOT-A-VALUE-2",
        "https://x.invalid/cb?state=NOT-A-VALUE-2",
        'key="NOT-A-VALUE-1"',
        "lookup key=NOT-A-VALUE-1 failed",
        "TOKEN=NOT-A-VALUE-1",
        "status_code=200 and nothing sensitive",
        "",
    ]

    @pytest.mark.parametrize("message", CASES)
    def test_a_second_pass_changes_nothing(self, message):
        f = URLRedactionFilter()
        once = f.redact_message(message)
        assert "NOT-A-VALUE" not in once
        assert f.redact_message(once) == once

    def test_a_json_line_ending_a_string_in_a_redacted_parameter_keeps_its_quote(self):
        import json

        f = URLRedactionFilter()
        line = json.dumps(
            {
                "reason": f.redact_message("https://x.invalid/y?code=NOT-A-1&state=NOT-A-2"),
                "count": 3,
            }
        )
        again = f.redact_message(line)
        assert again == line
        assert json.loads(again)["count"] == 3

    def test_a_quoted_value_is_still_redacted(self):
        # Arch's point 2: ``"`` is not an excluded value character.
        assert "NOT-A-VALUE-1" not in URLRedactionFilter().redact_message('key="NOT-A-VALUE-1"')

    def test_a_parameter_after_a_redacted_one_is_still_redacted(self):
        out = URLRedactionFilter().redact_message("u?key=[REDACTED]&token=NOT-A-VALUE-1&x=1")
        assert out == "u?key=[REDACTED]&token=[REDACTED]&x=1"

    @pytest.mark.parametrize(
        "message",
        [
            "key=[REDACTED]NOT-A-VALUE-1",
            "u?token=[REDACTED]NOT-A-VALUE-1&x=1",
            "https://x.invalid/cb?code=[REDACTED]NOT-A-VALUE-1",
        ],
    )
    def test_a_value_that_only_begins_with_the_marker_is_redacted_whole(self, message):
        # Arch, 2026-11-13: the marker is "already redacted" only before a delimiter
        # or the end of the text.
        f = URLRedactionFilter()
        once = f.redact_message(message)
        assert "NOT-A-VALUE" not in once
        assert f.redact_message(once) == once

    @pytest.mark.parametrize(
        "tail", ["", "&x=1", " next", '"', "',", ",", ";", ")", "]", "}", '\\"']
    )
    def test_the_marker_before_a_delimiter_is_left_alone(self, tail):
        line = "key=[REDACTED]" + tail
        assert URLRedactionFilter().redact_message(line) == line


class TestInstallFunctions:
    """Tests for the filter installation functions."""

    def test_install_url_redaction_filter_adds_to_httpx(self):
        """Test that install function adds filter to httpx logger."""
        # Start from an httpx logger with no redaction filter. An app startup earlier in
        # the same test run installs one (#2362: the install runs at the end of startup),
        # and this test then saw nothing to add: main went red on 875c051bee for it.
        httpx_logger = logging.getLogger("httpx")
        before = list(httpx_logger.filters)
        httpx_logger.filters[:] = [f for f in before if not isinstance(f, URLRedactionFilter)]
        initial_filter_count = len(httpx_logger.filters)
        try:
            # Install the filter
            install_url_redaction_filter(["httpx"])

            # Verify filter was added: exactly one, and still exactly one after a
            # second install (Arch, 2026-11-12: the install is idempotent).
            def carried():
                return [f for f in httpx_logger.filters if isinstance(f, URLRedactionFilter)]

            assert len(httpx_logger.filters) == initial_filter_count + 1
            assert len(carried()) == 1
            install_url_redaction_filter(["httpx"])
            assert len(carried()) == 1
        finally:
            httpx_logger.filters[:] = before

    def test_install_does_not_duplicate_filters(self):
        """Test that installing multiple times doesn't duplicate filters."""
        test_logger = logging.getLogger("test_no_duplicate")

        # Install multiple times
        install_url_redaction_filter(["test_no_duplicate"])
        install_url_redaction_filter(["test_no_duplicate"])
        install_url_redaction_filter(["test_no_duplicate"])

        # Count URLRedactionFilter instances
        filter_count = sum(1 for f in test_logger.filters if isinstance(f, URLRedactionFilter))
        assert filter_count == 1

    def test_install_root_redaction_filter(self):
        """Test that root filter installation works."""
        root_logger = logging.getLogger()
        initial_filter_count = len(root_logger.filters)

        install_root_redaction_filter()

        # Should have at least one URLRedactionFilter
        assert any(isinstance(f, URLRedactionFilter) for f in root_logger.filters)


class TestIntegrationWithLogging:
    """Integration tests with Python's logging system."""

    def test_httpx_style_log_is_redacted(self, caplog):
        """Test that httpx-style log messages are redacted."""
        # Create a logger that simulates httpx behavior
        test_logger = logging.getLogger("httpx_simulation")
        test_logger.setLevel(logging.DEBUG)

        # Add our filter
        redaction_filter = URLRedactionFilter()
        test_logger.addFilter(redaction_filter)

        # Log a message similar to what httpx produces
        with caplog.at_level(logging.DEBUG, logger="httpx_simulation"):
            test_logger.info(
                "HTTP Request: GET https://generativelanguage.googleapis.com/v1/models?key=AIzaSyD123abc"
            )

        # Check the captured log
        assert len(caplog.records) == 1
        assert "key=[REDACTED]" in caplog.records[0].message
        assert "AIzaSyD123abc" not in caplog.records[0].message

    def test_gemini_api_url_redaction(self, caplog):
        """Specific test for the Gemini API URL pattern that caused the incident."""
        test_logger = logging.getLogger("gemini_test")
        test_logger.setLevel(logging.DEBUG)
        redaction_filter = URLRedactionFilter()
        test_logger.addFilter(redaction_filter)

        # Exact pattern from the security incident
        gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDfakekey123456789"

        with caplog.at_level(logging.DEBUG, logger="gemini_test"):
            test_logger.info(f"Making request to {gemini_url}")

        assert "AIzaSyDfakekey123456789" not in caplog.text
        assert "key=[REDACTED]" in caplog.text


def test_every_installed_handler_formats_a_filtered_record_with_arguments():
    """Arch's ratchet, 2026-11-13. In an app-shaped setup (``logging.basicConfig``,
    then ``uvicorn.Config`` as ``main.py`` builds it, then the handler install), every
    handler's own formatter must format a record with arguments after the handler's
    filters have run. The next formatter that reads ``record.args`` fails here, not
    on a host. Run in a bare subprocess so no logging state leaks into this one."""
    import json
    import subprocess
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[5]
    code = r"""
import json, logging, sys
import uvicorn
from services.infrastructure.logging.url_redaction import (
    _all_handlers, handlers_without_redaction, install_handler_redaction_filter,
)

async def app(scope, receive, send):
    return None

logging.basicConfig(level=logging.INFO)
uvicorn.Config(app, log_level="info")
install_handler_redaction_filter()
out = {"without": handlers_without_redaction(), "handlers": []}
for owner, handler in _all_handlers():
    if owner == "uvicorn.access":
        record = logging.LogRecord(owner, logging.INFO, "x.py", 1, '%s - "%s %s HTTP/%s" %d',
            ("127.0.0.1:1", "GET", "/health?code=NOT-A-1&state=NOT-A-2&token=NOT-A-3", "1.1", 200), None)
    else:
        record = logging.LogRecord(owner, logging.INFO, "x.py", 1, "%s took %d ms",
            ("https://x.invalid/v1?key=NOT-A-1", 12), None)
    entry = {"owner": owner, "formatter": type(handler.formatter).__name__}
    try:
        handler.filter(record)
        entry["line"] = handler.format(record)
    except Exception as exc:
        entry["error"] = repr(exc)
    out["handlers"].append(entry)
print("RESULT " + json.dumps(out))
"""
    run = subprocess.run(
        [sys.executable, "-c", code], cwd=str(root), capture_output=True, text=True, timeout=120
    )
    assert run.returncode == 0, run.stderr[-800:]
    result = json.loads(
        [ln for ln in run.stdout.splitlines() if ln.startswith("RESULT ")][0][len("RESULT ") :]
    )
    assert result["without"] == []
    owners = {h["owner"] for h in result["handlers"]}
    assert {"root", "uvicorn", "uvicorn.access"} <= owners, owners
    for h in result["handlers"]:
        assert "error" not in h, h
        assert "NOT-A-" not in h["line"], h
    access = [h for h in result["handlers"] if h["owner"] == "uvicorn.access"][0]
    assert access["formatter"] == "AccessFormatter"
    assert access["line"].count("[REDACTED]") == 3
