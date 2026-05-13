"""
Custom HTTP exceptions for the API layer.

#1078: HTTPExceptionWithCookieClear lets an endpoint communicate
cookie-clearing intent through the #283 friendly-error handler. The
handler rebuilds a fresh JSONResponse, which loses any Set-Cookie
headers set on the dependency-injected Response — so endpoints that
need to clear cookies as part of a 4xx raise this subclass and the
handler applies `delete_cookie` to the rebuilt response.
"""

from typing import List, Optional

from fastapi import HTTPException


class HTTPExceptionWithCookieClear(HTTPException):
    """HTTPException that signals the friendly-error handler to clear named cookies.

    Use when raising a 4xx from inside the API needs to also clear
    auth-related cookies (e.g. invalid refresh token → clear both auth +
    refresh cookies so client falls back to login flow cleanly).

    The #283 friendly-error handler at `web/app.py` checks for this
    subclass and applies `response.delete_cookie(name)` for each entry
    in `clear_cookies` after building the JSONResponse.
    """

    def __init__(
        self,
        *args,
        clear_cookies: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.clear_cookies = clear_cookies or []
