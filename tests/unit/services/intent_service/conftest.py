"""Shared fixtures for the intent_service unit suite.

#1819: the floor-mechanics tests here (offer/continuation/reminder/standup suites)
drive the REAL conversational floor, whose prose turn reaches the REAL LLM client.
Post-#1809/#1819 every provider leg REFUSES an unbound spend, and the floor re-raises
the refusal family (refusals must reach the boundary) — so on a machine whose
env/keychain holds live keys, these tests started erroring where they previously made
a (silent, real-money) provider call.

The autouse fixture below binds the explicit designated-operator form for every test
in this directory, which restores the exact pre-#1819 behavior on BOTH worlds:
  - keyed developer machine: the server clients exist and are operator-entitled →
    the same live call as before (the developer's own machine, own keys);
  - keyless CI: entitled but no clients → the same "not initialized"/"no providers"
    failure the floor already degrades around.

What these suites pin is offer/floor STATE mechanics, not spend policy — the refusal
semantics themselves are pinned in tests/unit/services/llm/ (the #1809 and #1819
suites), which do NOT inherit this conftest.

Discovered-work note (#1819 census): that these unit tests reach a live LLM at all —
billed to whatever key the machine holds — predates this change; tracked separately.
"""

import pytest

from services.llm.request_key import OPERATOR_SERVER_KEY_ENV, request_api_key


@pytest.fixture(autouse=True)
def _operator_spend_binding_for_floor_suites(monkeypatch):
    monkeypatch.setenv(OPERATOR_SERVER_KEY_ENV, "1")
    with request_api_key(None):
        yield
