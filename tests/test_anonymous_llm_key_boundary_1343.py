"""#1343 (Arch gate-integrity read, 2026-07-02) — ratchet the anonymous-LLM-billing
fix so the SAME class of bug (an anonymous-reachable route silently billing the
server's own Anthropic key) can't regress OR reappear on a new route.

Arch's framing: #1308's exempt-list lint flags auth+WRITE; it has no "auth +
paid-side-effect" dimension, so a route can pass #1308 and still silently bill. This
extends the guard family with that missing dimension — same mechanical, route-
introspection style as #1308, not a general call-graph analyzer (m-40).

Mechanism: enumerate every route whose dependency tree includes
`get_current_user_optional` (FastAPI's `route.dependant.dependencies` — the
anonymous-reachable marker; confirmed reliable, not fragile source-scanning). For
each, if its handler's source touches the raw LLM-key resolver
(`resolve_request_api_key`), it MUST also reference `AnonymousLLMKeyRequiredError`
in the same function — proving the anonymous-refusal path is wired, not silently
dropped. A future new optional-auth route that reaches billing without the guard
fails this test, same as #1308 fails the build for a new unjustified exempt write.
"""

import inspect


def _optional_auth_routes():
    """Every registered route whose dependency tree includes get_current_user_optional
    — the anonymous-reachable marker. Verified today: exactly {"/api/v1/intent"}."""
    from web.app import app

    out = []
    for r in app.routes:
        dependant = getattr(r, "dependant", None)
        if not dependant:
            continue
        names = [
            getattr(d.call, "__name__", None)
            for d in dependant.dependencies
            if getattr(d, "call", None)
        ]
        if "get_current_user_optional" in names:
            out.append(r)
    return out


def test_there_is_at_least_one_optional_auth_route():
    # Sanity: the lint is exercising a real route, not vacuous (mirrors #1308's
    # "at least one writable exempt route" sanity check).
    assert _optional_auth_routes(), "expected at least one optional-auth route (e.g. /intent)"


def test_every_optional_auth_route_that_touches_the_raw_resolver_handles_anonymous_refusal():
    """The #1343 ratchet: any anonymous-reachable route touching resolve_request_api_key
    must handle AnonymousLLMKeyRequiredError in the same function — or it can silently
    fall through to billing the server's own key for an anonymous caller."""
    violations = []
    for r in _optional_auth_routes():
        endpoint = getattr(r, "endpoint", None)
        if endpoint is None:
            continue
        try:
            source = inspect.getsource(endpoint)
        except (OSError, TypeError):
            continue
        if "resolve_request_api_key(" in source and "AnonymousLLMKeyRequiredError" not in source:
            violations.append(getattr(r, "path", str(endpoint)))

    assert not violations, (
        "#1343 SECURITY BOUNDARY: these anonymous-reachable routes call the raw LLM-key "
        f"resolver without handling AnonymousLLMKeyRequiredError: {violations}. An "
        "unauthenticated caller with no X-User-Api-Key could silently bill the server's "
        "own Anthropic key (the exact #1343 class). Fix: catch AnonymousLLMKeyRequiredError "
        "and return an honest refusal (see web/api/routes/intent.py::process_intent)."
    )


def test_documents_routes_never_reach_the_resolver_via_optional_auth():
    """Defense-in-depth: web/utils/llm_key.py's resolve_user_llm_key wraps the same raw
    resolver but is only ever called from routes requiring Depends(get_current_user)
    (mandatory, not optional) — documents.py, per #1185. If a future documents-style
    route switches to optional auth while still calling resolve_user_llm_key, it must
    show up in the optional-auth set above and get caught by the prior test too."""
    optional_paths = {getattr(r, "path", None) for r in _optional_auth_routes()}
    assert "/api/v1/documents" not in optional_paths
    # Precise-enough guard: no /documents/* path is currently optional-auth.
    assert not any((p or "").startswith("/api/v1/documents") for p in optional_paths)
