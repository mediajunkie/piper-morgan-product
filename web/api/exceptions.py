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

# Issue 2429: the class moved to services/api/errors.py so a services/ gate can raise it;
# re-exported here so existing importers keep working.
from services.api.errors import UserFacingHTTPException  # noqa: F401
from services.domain.models import ShareRole

# Issue 2432 (CXO, comment 7144095698): the one role refusal the list, todo and project
# share routes give. The roles are computed once here from ``ShareRole``, in its declared
# order, and the line never echoes the role the person sent.
SHARE_ROLES = tuple(role.value for role in ShareRole)
ROLE_NOT_RECOGNISED_LINE = (
    "That isn't a role I recognise. Choose one of: " + ", ".join(SHARE_ROLES) + "."
)


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
