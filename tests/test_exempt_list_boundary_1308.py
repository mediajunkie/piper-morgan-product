"""#1308 (m-41) — the auth-exempt list is a security boundary.

Once the Caddy perimeter gate is removed (#1162), `AuthMiddleware`'s exempt list
(`DEFAULT_EXCLUDE_PATHS`) is the entire attack surface. This lint fails the build if
any exempt route has a WRITE method (POST/PUT/PATCH/DELETE) without a justified entry
in `AUTH_EXEMPT_JUSTIFIED` — the #1307 class (exempt + writable + prod-reachable) made
impossible-by-construction. Read-only exempt routes need no entry.
"""

WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def _exempt_writable_routes():
    """Registered routes that are under an exempt prefix AND expose a write method."""
    from services.auth.auth_middleware import DEFAULT_EXCLUDE_PATHS
    from web.app import app

    out = []
    for r in app.routes:
        path = getattr(r, "path", None)
        methods = getattr(r, "methods", None) or set()
        if path is None:
            continue
        exempt = any(
            path == ex or path.startswith(ex.rstrip("/") + "/") for ex in DEFAULT_EXCLUDE_PATHS
        )
        if exempt and (WRITE_METHODS & set(methods)):
            out.append((path, sorted(WRITE_METHODS & set(methods))))
    return out


def _is_justified(path, justified):
    """A justified key is an exact path or a trailing-'/' prefix."""
    return any(path == key or (key.endswith("/") and path.startswith(key)) for key in justified)


def test_every_writable_exempt_route_is_justified():
    from services.auth.auth_middleware import AUTH_EXEMPT_JUSTIFIED

    unjustified = [
        (p, m) for p, m in _exempt_writable_routes() if not _is_justified(p, AUTH_EXEMPT_JUSTIFIED)
    ]
    assert not unjustified, (
        "#1308 SECURITY BOUNDARY: these auth-exempt routes have WRITE methods but no "
        f"AUTH_EXEMPT_JUSTIFIED entry: {unjustified}. This is the #1307 class (exempt + "
        "writable + prod-reachable). Fix one of: make it read-only, env-gate it (404 in "
        "prod), remove it from the exempt list (require auth), or add an "
        "AUTH_EXEMPT_JUSTIFIED entry with a one-line reason if the exemption is deliberate."
    )


def test_there_is_at_least_one_writable_exempt_route():
    # Sanity: the lint is exercising real routes (auth bootstrap exists), not vacuous.
    assert _exempt_writable_routes(), "expected writable exempt routes (auth bootstrap) to exist"


def test_justified_allowlist_has_no_stale_entries():
    """Every AUTH_EXEMPT_JUSTIFIED key must match a real writable exempt route (no rot —
    cf. admin_compose #1307, which a stale entry would have masked)."""
    from services.auth.auth_middleware import AUTH_EXEMPT_JUSTIFIED

    writable_paths = [p for p, _ in _exempt_writable_routes()]
    stale = [
        key
        for key in AUTH_EXEMPT_JUSTIFIED
        if not any(p == key or (key.endswith("/") and p.startswith(key)) for p in writable_paths)
    ]
    assert not stale, (
        f"AUTH_EXEMPT_JUSTIFIED has stale entries (no matching writable exempt route): {stale}. "
        "Remove them so the allowlist stays a true reflection of the boundary."
    )


def test_matcher_flags_unjustified_and_accepts_justified():
    justified = {"/api/v1/auth/login": "ok", "/api/v1/setup/": "wizard"}
    assert not _is_justified("/api/v1/admin/danger", justified)
    assert _is_justified("/api/v1/auth/login", justified)
    assert _is_justified("/api/v1/setup/complete", justified)  # prefix match
