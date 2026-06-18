"""Dev-route gate — the canonical way to make a route dev-only (#1149).

A dev/debug route must not be reachable in production. The convention: mount the
router normally, but hang ``Depends(require_dev_environment)`` on it so every route
**404s in production** — invisible, not merely forbidden (don't disclose the route
exists). Default environment is "development" (the #1087 pattern), so a route is
open in dev and closed in prod without any per-deploy config.

This consolidates the gate that ``web/routers/dev_trust.py`` and
``web/routers/dev_composting.py`` each hand-rolled. New dev routes should depend on
``require_dev_environment`` from here rather than copy the check. (Migrating those two
to this helper is a small follow-up — tracked, not done in #1149's scope.)

Env resolution mirrors ``services/auth/jwt_service.py`` (#1087): ``PIPER_ENVIRONMENT``
is canonical, ``ENVIRONMENT`` is the older fallback.
"""
from __future__ import annotations

import os

from fastapi import HTTPException


def is_production() -> bool:
    """True only when the environment explicitly resolves to production."""
    env = (os.getenv("PIPER_ENVIRONMENT") or os.getenv("ENVIRONMENT") or "development").lower()
    return env == "production"


def require_dev_environment() -> None:
    """FastAPI route dependency: hide a dev-only route entirely in production.

    Raises 404 (not 403) so production does not even disclose the route exists.
    """
    if is_production():
        raise HTTPException(status_code=404, detail="Not Found")
