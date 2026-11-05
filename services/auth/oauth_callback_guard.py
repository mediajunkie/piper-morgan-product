"""#2283 (Arch 2026-11-04 21:11; P0 tenancy under xian's 19:31 rule) and #2281: an OAuth
callback stores a provider grant only for the browser that is signed in as the account the
``state`` names.

The gap this closes: each callback bound the grant to the user the ``state`` names and
never compared that with the browser's own signed-in user, so a Connect started by one
account and completed in another person's browser stored the second person's grant on the
first account. The check runs AFTER the state is verified and consumed (single-use) and
BEFORE the authorization code is exchanged, so a refused callback stores nothing at all:
CXO's "Nothing was connected yet" is true by construction.

Every handler's ``handle_oauth_callback`` takes ``session_user_id`` as a required keyword
and calls ``require_session_matches_state`` before its exchange; the routes pass the
browser's session user (or None) and turn the refusal into an HTML redirect, never JSON.
"""

from __future__ import annotations

from typing import Optional
from urllib.parse import quote

# CXO 2026-11-04 (#2281 page words), above the sign-in form; {name} is the connector.
SIGN_IN_TO_FINISH_LINE = (
    "Sign in to finish connecting {name}. Nothing was connected yet. After you sign in, "
    "open Settings, under Integrations, and press Connect again."
)
# Lead's draft for the signed-in-as-someone-else case, for CXO to rule (11-05).
WRONG_ACCOUNT_LINE = (
    "This connection was started from a different Piper account, so nothing was connected. "
    "Sign in as the account you want to connect, then press Connect again."
)

CONNECTOR_NAMES = {"github": "GitHub", "calendar": "Google Calendar", "slack": "Slack"}


class OAuthCallbackSessionMismatch(ValueError):
    """The callback's browser is not signed in as the state's account. ``signed_in`` says
    which case: False for no session, True for a different account."""

    def __init__(self, signed_in: bool):
        self.signed_in = signed_in
        super().__init__(
            "OAuth callback refused: "
            + ("signed in as a different account" if signed_in else "no session")
        )


def require_session_matches_state(
    state_user_id: Optional[str], session_user_id: Optional[str]
) -> None:
    """Raise unless the browser's session user is the state's user. Call it after the
    state is verified (and consumed) and before the code exchange."""
    if not session_user_id:
        raise OAuthCallbackSessionMismatch(signed_in=False)
    if str(session_user_id) != str(state_user_id):
        raise OAuthCallbackSessionMismatch(signed_in=True)


def refusal_redirect_url(
    connector: str, exc: OAuthCallbackSessionMismatch, *, wizard: bool = False
) -> str:
    """Where a refused callback sends the browser: an HTML page, never JSON."""
    if not exc.signed_in:
        back = "/setup" if wizard else "/settings/integrations"
        return f"/login?connect={quote(connector)}&next={quote(back, safe='')}"
    if wizard:
        return f"/setup?{connector}_error=wrong_account#step-2"
    return f"/settings/integrations?{connector}_error=wrong_account"


def sign_in_to_finish_line(connector: Optional[str]) -> Optional[str]:
    """The login page's notice for ``/login?connect=<connector>``, or None."""
    name = CONNECTOR_NAMES.get((connector or "").strip().lower())
    return SIGN_IN_TO_FINISH_LINE.format(name=name) if name else None


def host_switch_url(request, redirect_uri: Optional[str], page_path: str) -> Optional[str]:
    """#2281 (b), required by #2283: the provider returns the browser to ``redirect_uri``'s
    host, and the callback needs a session THERE. When the Connect was started from another
    host (``beta.`` or ``.fly.dev`` against an ``alpha.`` callback), the page is sent to the
    callback's host first, where the person signs in once and presses Connect. None when the
    hosts already agree, or when either can't be read (a direct call in a test)."""
    from urllib.parse import urlsplit

    if request is None or not redirect_uri:
        return None
    try:
        here = (request.url.hostname or "").lower()
        target = urlsplit(redirect_uri)
    except Exception:  # silent-ok: an unreadable host never blocks a Connect
        return None
    there = (target.hostname or "").lower()
    if not here or not there or here == there:
        return None
    port = f":{target.port}" if target.port else ""
    return f"{target.scheme}://{there}{port}{page_path}"
