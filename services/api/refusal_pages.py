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

Issue 2433 (Arch, mail 01M880KDHY): the link under the line is a ``WayOut``, a closed set
of two. ``RELOAD`` (the default) reloads the same address, for a refusal that may pass on
a retry. ``SETTINGS`` goes back to Settings, for a refusal a retry cannot change (a
non-admin opening an admin-only page). A caller names a member and never passes an address
or a label; the same guard holds each call to ``WayOut.<MEMBER>``. A third member is a
diff Arch reads.
"""

import html
from enum import Enum
from typing import Optional

from starlette.requests import Request
from starlette.responses import HTMLResponse

_MESSAGE_SLOT = "__PIPER_REFUSAL_MESSAGE__"
_LINK_ADDRESS_SLOT = "__PIPER_REFUSAL_LINK_ADDRESS__"
_LINK_TEXT_SLOT = "__PIPER_REFUSAL_LINK_TEXT__"

# Issue 2433 (CXO, mail 01M87ZZX8Q): what a non-admin reads on opening an admin-only page.
# Not the gate's JSON line ("... Nothing was changed."): on a page load nothing was tried.
ADMIN_PAGE_NEEDS_ADMIN_LINE = "This page needs an admin account."

TRY_AGAIN_LINK_TEXT = "Try again"
BACK_TO_SETTINGS_LINK_TEXT = "Back to Settings"
SAME_ADDRESS = ""
SETTINGS_ADDRESS = "/settings"


class WayOut(Enum):
    """The link under a refusal page's line: (its text, its address). Closed set."""

    RELOAD = (TRY_AGAIN_LINK_TEXT, SAME_ADDRESS)
    SETTINGS = (BACK_TO_SETTINGS_LINK_TEXT, SETTINGS_ADDRESS)


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
<p><a href="__PIPER_REFUSAL_LINK_ADDRESS__">__PIPER_REFUSAL_LINK_TEXT__</a></p>
</main>
</body>
</html>
"""


def wants_a_page(request: Request) -> bool:
    """True when the request is a page load: not under ``/api/``, and it accepts HTML.

    A missing ``Accept`` header is not a page load (``fetch`` sends ``*/*``)."""
    accept = request.headers.get("accept", "") or ""
    return not request.url.path.startswith("/api/") and "text/html" in accept


def refusal_page(
    message: str,
    status_code: int,
    retry_after_seconds: Optional[int],
    way_out: WayOut = WayOut.RELOAD,
) -> HTMLResponse:
    """A plain page with the line and one link: by default, one that reloads the same address.

    Keeps the refusal's status. ``Retry-After`` is sent when ``retry_after_seconds`` is a
    number and left out when it is None (a 403 has nothing to wait for). Uses nothing but
    this module's constants."""
    if not isinstance(way_out, WayOut):
        raise TypeError("way_out must be a member of WayOut")
    link_text, link_address = way_out.value
    content = (
        REFUSAL_PAGE_HTML.replace(_MESSAGE_SLOT, html.escape(message))
        .replace(_LINK_ADDRESS_SLOT, html.escape(link_address, quote=True))
        .replace(_LINK_TEXT_SLOT, html.escape(link_text))
    )
    headers = {}
    if retry_after_seconds is not None:
        headers["Retry-After"] = str(int(retry_after_seconds))
    return HTMLResponse(content=content, status_code=status_code, headers=headers)
