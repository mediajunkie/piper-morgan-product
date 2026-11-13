"""
URL Parameter Redaction Filter for Logging

Security measure to prevent sensitive data (API keys, tokens) from being logged
when passed as URL query parameters.

Created: 2026-01-17
Issue: Security incident - Gemini API key leaked via httpx INFO logs
"""

import logging
import re
from typing import List, Pattern


class URLRedactionFilter(logging.Filter):
    """
    Logging filter that redacts sensitive URL parameters from log messages.

    Redacts query parameters matching patterns like:
    - key=VALUE
    - api_key=VALUE
    - apikey=VALUE
    - token=VALUE
    - secret=VALUE
    - password=VALUE
    - auth=VALUE
    - bearer=VALUE
    - access_token=VALUE
    - client_secret=VALUE

    Example:
        Before: https://api.example.com/v1?key=AIzaSyD123abc&other=value
        After:  https://api.example.com/v1?key=[REDACTED]&other=value
    """

    # Patterns for sensitive URL parameters (case-insensitive)
    SENSITIVE_PARAM_PATTERNS: List[str] = [
        r"key=",
        r"api_key=",
        r"apikey=",
        r"api-key=",
        r"token=",
        r"access_token=",
        r"refresh_token=",
        r"secret=",
        r"client_secret=",
        r"password=",
        r"passwd=",
        r"auth=",
        r"authorization=",
        r"bearer=",
        r"credential=",
        r"credentials=",
    ]

    # #2362 (Arch, 2026-11-12): an OAuth callback's ``code`` and ``state``. Matched only
    # as query parameters (straight after ``?`` or ``&``), so ``status_code=200`` in an
    # ordinary line survives.
    QUERY_ONLY_PARAMS: List[str] = ["code", "state"]

    # Compiled regex pattern for efficient matching
    # Matches: param_name=value (where value continues until & or end of string/whitespace)
    _redaction_pattern: Pattern = None

    def __init__(self, name: str = ""):
        super().__init__(name)
        self._compile_pattern()

    def _compile_pattern(self) -> None:
        """Compile the regex pattern for URL parameter redaction."""
        # Build alternation of all sensitive parameter names
        param_names = "|".join(self.SENSITIVE_PARAM_PATTERNS)
        # Match: (param_name=)(value until & or whitespace or end)
        # The value can contain any characters except & and whitespace
        # #2350 (Arch, 2026-11-13): the lookahead makes redaction idempotent. A line can
        # pass through this more than once (the evidence logger redacts a value, then the
        # logger's and the handler's filters run over the finished JSON line). Without it
        # the second pass matched ``[REDACTED]",`` and ate the closing quote and comma.
        # Do not add ``"`` to the excluded value characters: ``key="abc"`` would then keep
        # its value.
        done = r"(?!\[REDACTED\])"
        self._redaction_pattern = re.compile(rf"({param_names}){done}([^&\s]+)", re.IGNORECASE)
        query_only = "|".join(self.QUERY_ONLY_PARAMS)
        self._query_only_pattern = re.compile(
            rf"([?&](?:{query_only})=){done}([^&\s]+)", re.IGNORECASE
        )

    def redact_message(self, message: str) -> str:
        """
        Redact sensitive URL parameters from a message string.

        Args:
            message: The log message to redact

        Returns:
            Message with sensitive parameter values replaced with [REDACTED]
        """
        if not message:
            return message

        # Replace all matches with param_name=[REDACTED]
        redacted = self._redaction_pattern.sub(r"\1[REDACTED]", str(message))
        return self._query_only_pattern.sub(r"\1[REDACTED]", redacted)

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter method called by logging framework.

        Redacts the FINISHED message: the format string and its arguments are merged
        first, then the result is redacted and stored as the record's message with no
        arguments left. Always returns True (the record goes through, redacted).

        #2362: this used to redact ``record.msg`` and each string argument
        separately. A format string such as ``"lookup key=%s failed"`` then lost its
        placeholder (``key=[REDACTED]``), and merging the arguments raised
        ``TypeError: not all arguments converted``, so the line was lost. It also
        could not redact a value split between the format string and an argument
        (``"token=%s"`` with the value as the argument). Never raises: a filter that
        raised would take the log call's caller down with it.
        """
        try:
            message = record.getMessage()
        except Exception:
            # A malformed format string or arguments. Left alone, the handler would
            # print the raw message and arguments in its formatting-error report,
            # unredacted (Arch, 2026-11-12). So build one line from both, redact it, and
            # clear the arguments: the line is written, redacted, and nothing is lost.
            try:
                raw = f"{record.msg} (log arguments could not be merged: {record.args!r})"
                record.msg = self.redact_message(raw)
                record.args = None
            except Exception:  # pragma: no cover - redaction must never break logging
                record.msg = "[log record could not be rendered or redacted]"
                record.args = None
            return True
        try:
            redacted = self.redact_message(message)
            if redacted != message or record.args:
                record.msg = redacted
                record.args = None
        except Exception:  # pragma: no cover - redaction must never break logging
            pass
        return True


def install_url_redaction_filter(logger_names: List[str] = None) -> None:
    """
    Install the URL redaction filter on specified loggers.

    If no logger names provided, installs on common HTTP client loggers:
    - httpx
    - httpcore
    - urllib3
    - requests
    - aiohttp

    Args:
        logger_names: Optional list of logger names to filter.
                     If None, uses default HTTP client loggers.
    """
    if logger_names is None:
        logger_names = [
            "httpx",
            "httpcore",
            "urllib3",
            "requests",
            "aiohttp",
            "aiohttp.client",
        ]

    redaction_filter = URLRedactionFilter()

    for name in logger_names:
        logger = logging.getLogger(name)
        # Check if filter already installed to avoid duplicates
        if not any(isinstance(f, URLRedactionFilter) for f in logger.filters):
            logger.addFilter(redaction_filter)


def install_root_redaction_filter() -> None:
    """
    Install the URL redaction filter on the root logger AND on every handler.

    A filter on a logger applies only to records logged ON that logger; a record from
    any other logger reaches the root's handlers without passing the root logger's
    filters (#2362: until 2026-11-12 this function attached to the root logger alone,
    and a child logger's line kept its ``key=`` value). A handler's filters see every
    record the handler emits, so the coverage lives there. The root-logger filter is
    kept for records logged directly on the root before any handler exists.
    """
    redaction_filter = URLRedactionFilter()
    root_logger = logging.getLogger()

    # Check if filter already installed to avoid duplicates
    if not any(isinstance(f, URLRedactionFilter) for f in root_logger.filters):
        root_logger.addFilter(redaction_filter)
    install_handler_redaction_filter()


def _all_handlers() -> List[tuple]:
    """(owner name, handler) for the root's handlers and every other logger's own
    handlers (a non-propagating logger such as uvicorn's writes only through its own)."""
    found = [("root", h) for h in logging.getLogger().handlers]
    for name, obj in list(logging.root.manager.loggerDict.items()):
        if isinstance(obj, logging.Logger):
            found.extend((name, h) for h in obj.handlers)
    return found


def install_handler_redaction_filter() -> List[str]:
    """Put the redaction filter on every logging handler that exists right now (#2362).

    Call it after anything that creates handlers: ``logging.basicConfig``, and
    ``uvicorn.Config(...)``, which builds the ``uvicorn`` and ``uvicorn.access``
    handlers. Idempotent. Returns the owner name of each handler it added a filter to.
    """
    added: List[str] = []
    for owner, handler in _all_handlers():
        if not any(isinstance(f, URLRedactionFilter) for f in handler.filters):
            handler.addFilter(URLRedactionFilter())
            added.append(owner)
    return added


def handlers_without_redaction() -> List[str]:
    """Owner names of handlers that do not carry the filter. Empty is the goal."""
    return [
        owner
        for owner, handler in _all_handlers()
        if not any(isinstance(f, URLRedactionFilter) for f in handler.filters)
    ]


class RedactionAtStartup:
    """ASGI wrapper: re-run the handler install once the app's startup has finished.

    #2362 (Arch, 2026-11-12): a handler created during startup, after the entry point's
    own install, would otherwise be left without the filter. The install is idempotent,
    so running it again at the end of startup costs nothing. It runs when the wrapped
    app reports ``lifespan.startup.complete``, and passes every message through.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "lifespan":
            await self.app(scope, receive, send)
            return

        async def send_and_install(message):
            if message.get("type") == "lifespan.startup.complete":
                try:
                    install_handler_redaction_filter()
                except Exception:  # pragma: no cover - never block startup on this
                    pass
            await send(message)

        await self.app(scope, receive, send_and_install)
