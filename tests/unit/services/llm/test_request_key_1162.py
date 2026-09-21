"""#1162 BYOC per-request LLM key — the credential-handling security logic.

These guard the load-bearing properties: a per-request user key is bound only for
the request, ALWAYS reset afterward (incl. on exception → no cross-request leak),
a blank header falls back to the server key, and the client-selection uses the
user key when bound. The route wiring + the LLM call site consume this module.
"""

import pytest

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


def test_blank_or_none_raises_at_bind_time():
    """AMENDED by #1812 step 5. A blank/None binding used to mean the operator's
    server credential (and before #1809, simply 'nothing bound'). The seam is
    deleted: binding None/blank now raises — an absent header falls through at
    the RESOLVER (which refuses or finds a stored key), never at the binder."""
    with pytest.raises(ValueError, match="1812"):
        with request_api_key(""):  # pragma: no cover - must not enter
            pass
    with pytest.raises(ValueError, match="1812"):
        with request_api_key(None):  # pragma: no cover - must not enter
            pass


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
    # absent → REFUSE (#1809 inversion; this line used to assert the server
    # client — "PM's own use / unauthenticated" — which #1807/#1320 closed at
    # the resolver, #1809 closed at the chokepoint, and #1812 step 5 made
    # unrepresentable: the chokepoint takes no server client at all)
    from services.llm.request_key import UnboundLLMKeyError

    with pytest.raises(UnboundLLMKeyError):
        anthropic_client_for_request()
    # bound → a FRESH client keyed to the user's BYOC key
    with request_api_key("sk-ant-user"):
        client = anthropic_client_for_request()
        assert getattr(client, "api_key", None) == "sk-ant-user"


def test_nested_contexts_restore_outer():
    with request_api_key("outer"):
        with request_api_key("inner"):
            assert get_request_api_key() == "inner"
        assert get_request_api_key() == "outer"
    assert get_request_api_key() is None
