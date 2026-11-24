"""Whether a request wants a page, and the plain page a refusal answers it with (issue 2431).

Arch's ruling on issue 2431 (2026-11-24): "a page is wanted" means the path does not start
with ``/api/`` and the ``Accept`` header contains ``text/html``. That rule had two copies
(``AuthMiddleware._unauthorized_response``'s redirect to ``/login`` and the negotiated 404 in
``web/app.py``, issue 2039); both now call ``wants_a_page``. A test fails on any other
``"text/html" in ...`` check or ``Accept`` read under ``services/`` or ``web/``
(``tests/unit/web/test_outage_replies_2431.py``).

``refusal_page`` answers a page load that a middleware refuses before the route runs: the
capacity guard's three refusals and the auth middleware's session 503. It is built from one
constant with ``str.replace``: no template engine, no session, no database and no Redis,
because it renders during exactly the outage that broke those. It never redirects.

Its ``message`` is a fixed line: a literal, an UPPER_CASE constant, or (Arch, mail 01M87EY4N7)
``UPPER_CASE_TEMPLATE.format(<name>=int(<expr>))``, the 429's whole number of seconds. The guard
in ``tests/unit/web/test_setup_lines_reach_the_page_2428.py`` reads each call.
"""

import html

from starlette.requests import Request
from starlette.responses import HTMLResponse

_MESSAGE_SLOT = "__PIPER_REFUSAL_MESSAGE__"

REFUSAL_PAGE_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Piper Morgan</title>
<style>
body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; color: #1f2937;
  background: #ffffff; max-width: 32rem; margin: 4rem auto; padding: 0 1rem; line-height: 1.5; }
a { color: #1d4ed8; }
</style>
</head>
<body>
<main>
<p>__PIPER_REFUSAL_MESSAGE__</p>
<p><a href="">Try again</a></p>
</main>
</body>
</html>
"""


def wants_a_page(request: Request) -> bool:
    """True when the request is a page load: not under ``/api/``, and it accepts HTML.

    A missing ``Accept`` header is not a page load (``fetch`` sends ``*/*``)."""
    accept = request.headers.get("accept", "") or ""
    return not request.url.path.startswith("/api/") and "text/html" in accept


def refusal_page(message: str, status_code: int, retry_after_seconds: int) -> HTMLResponse:
    """A plain page with the line and a link that reloads the same address.

    Keeps the refusal's status and ``Retry-After``. Uses nothing but this module's constant."""
    text = html.escape(message)
    return HTMLResponse(
        content=REFUSAL_PAGE_HTML.replace(_MESSAGE_SLOT, text),
        status_code=status_code,
        headers={"Retry-After": str(int(retry_after_seconds))},
    )
