"""#1162 BYOC per-request LLM key — the credential-handling security logic.

These guard the load-bearing properties: a per-request user key is bound only for
the request, ALWAYS reset afterward (incl. on exception → no cross-request leak),
a blank header falls back to the server key, and the client-selection uses the
user key when bound. The route wiring + the LLM call site consume this module.
"""
from services.llm.request_key import (
    anthropic_client_for_request,
    get_request_api_key,
    request_api_key,
)


def test_default_is_none():
    """No per-request key bound → None (the LLM client uses the server key)."""
    assert get_request_api_key() is None


def test_binds_then_resets():
    with request_api_key("sk-user-123"):
        assert get_request_api_key() == "sk-user-123"
    # reset in the finally — the key never outlives the request
    assert get_request_api_key() is None


def test_blank_or_none_binds_nothing():
    """An absent/blank X-User-Api-Key header must fall back to the server key."""
    with request_api_key(""):
        assert get_request_api_key() is None
    with request_api_key(None):
        assert get_request_api_key() is None


def test_reset_even_on_exception():
    """The finally must reset even if the wrapped request raises — no leak."""
    try:
        with request_api_key("sk-user-xyz"):
            assert get_request_api_key() == "sk-user-xyz"
            raise ValueError("boom")
    except ValueError:
        pass
    assert get_request_api_key() is None


def test_client_selection_uses_user_key_when_bound():
    server_client = object()  # sentinel for the server's configured client
    # absent → the server client (PM's own use / unauthenticated)
    assert anthropic_client_for_request(server_client) is server_client
    # bound → a FRESH client keyed to the user's BYOC key, not the server client
    with request_api_key("sk-ant-user"):
        client = anthropic_client_for_request(server_client)
        assert client is not server_client
        assert getattr(client, "api_key", None) == "sk-ant-user"


def test_nested_contexts_restore_outer():
    with request_api_key("outer"):
        with request_api_key("inner"):
            assert get_request_api_key() == "inner"
        assert get_request_api_key() == "outer"
    assert get_request_api_key() is None
