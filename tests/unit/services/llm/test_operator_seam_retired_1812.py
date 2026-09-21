"""#1812 step 5 — the operator seam is RETIRED, and staying retired is a contract.

This file replaces ``test_operator_server_key_1807.py``. That file pinned the one
surviving server-key path (a designated operator principal behind two default-OFF
gates). PM then ruled their own account has normal-account semantics (decisions.log
2026-09-19), removing the last principal the seam could have served — so #1812
step 5 deleted the seam itself: ``PIPER_OPERATOR_SERVER_KEY``,
``operator_server_key_opted_in``, ``is_designated_operator``, the resolver's
operator rung, and the explicit ``None`` binding are all gone.

What this file pins now is the INVERSE: the seam cannot come back quietly.
  - the deleted symbols stay deleted (a re-import is a regression, not a revival);
  - binding ``None`` raises at bind time — the value that used to MEAN "spend the
    server's key" is unrepresentable, not merely unused;
  - the resolver is header > stored > refuse, unconditionally — no fourth argument,
    no principal that resolves to "someone else pays";
  - the #1807/#1320 refusal types and short-circuit order survive unchanged (the
    KEEP half of the plan's keep-and-invert: refusals got simpler, not weaker).

LAYER (m-43): pure unit — the resolver and binding run for real; only the injected
``fetch_stored`` is faked (that is its designed test seam, not a stub of the code
under test). DENOMINATOR: the resolver's three rungs and both refusal types; the
bind-time guard; symbol absence in the two modules that owned the seam. The spend
chokepoints' unbound refusals live in test_unbound_key_refusal_1809.py /
test_provider_request_key_1819.py.
"""

import uuid

import pytest

from services.llm.request_key import (
    AnonymousLLMKeyRequiredError,
    UserLLMKeyRequiredError,
    request_api_key,
    resolve_request_api_key,
)


async def _fetch_no_stored_key(uid):
    return None


async def _fetch_boom(uid):  # pragma: no cover - asserts it is never called
    raise AssertionError("stored-key lookup should not have been reached")


class TestTheSeamStaysDeleted:
    """The symbols that constituted the seam are gone from both owning modules."""

    def test_request_key_module_has_no_operator_surface(self):
        import services.llm.request_key as rk

        for symbol in ("operator_server_key_opted_in", "OPERATOR_SERVER_KEY_ENV"):
            assert not hasattr(rk, symbol), f"{symbol} came back — the #1812 cut regressed"

    def test_web_llm_key_module_has_no_operator_check(self):
        import web.utils.llm_key as wk

        assert not hasattr(
            wk, "is_designated_operator"
        ), "is_designated_operator came back — the #1812 cut regressed"

    def test_resolver_takes_no_operator_checker(self):
        """The fourth argument WAS the seam's injection point. Its absence is the
        structural guarantee that no caller can wire an operator path back in
        without changing this signature — which is exactly the loud event we want."""
        import inspect

        params = inspect.signature(resolve_request_api_key).parameters
        assert list(params) == ["header_key", "user_id", "fetch_stored"]


class TestNoneBindingIsUnrepresentable:
    """``request_api_key(None)`` used to mean "the operator authorized the server's
    key". It now raises at bind time — bad state unrepresentable, not just unused."""

    def test_binding_none_raises(self):
        with pytest.raises(ValueError, match="1812"):
            with request_api_key(None):  # pragma: no cover - must not enter
                pass

    def test_binding_blank_raises(self):
        with pytest.raises(ValueError, match="1812"):
            with request_api_key(""):  # pragma: no cover - must not enter
                pass


class TestResolverContract:
    """Header > stored > refuse — the KEEP half, simpler with the operator rung gone."""

    @pytest.mark.asyncio
    async def test_authenticated_keyless_refuses_unconditionally(self):
        """The alpha tester AND the PM alike (normal-account ruling): authenticated,
        no key of their own — refused. There is no principal for whom this resolves
        to someone else's credential."""
        with pytest.raises(UserLLMKeyRequiredError):
            await resolve_request_api_key(None, str(uuid.uuid4()), _fetch_no_stored_key)

    @pytest.mark.asyncio
    async def test_no_fetcher_injected_refuses_fail_closed(self):
        with pytest.raises(UserLLMKeyRequiredError):
            await resolve_request_api_key(None, str(uuid.uuid4()), None)

    @pytest.mark.asyncio
    async def test_stored_key_resolves_and_is_returned(self):
        async def _fetch_key(uid):
            return "sk-their-own"

        assert await resolve_request_api_key(None, "u1", _fetch_key) == "sk-their-own"

    @pytest.mark.asyncio
    async def test_header_key_short_circuits_everything(self):
        """#1162 no-regress: BYOC wins, no DB touch, login optional."""
        assert await resolve_request_api_key("sk-byoc", "u1", _fetch_boom) == "sk-byoc"
        assert await resolve_request_api_key("sk-byoc", None, _fetch_boom) == "sk-byoc"

    @pytest.mark.asyncio
    async def test_no_regress_1320_anonymous_keeps_its_own_error(self):
        """The anonymous refusal keeps its own type — the remediations differ and
        #1520 is what conflating them costs."""
        with pytest.raises(AnonymousLLMKeyRequiredError):
            await resolve_request_api_key(None, None, _fetch_boom)
        with pytest.raises(AnonymousLLMKeyRequiredError):
            await resolve_request_api_key("", None, _fetch_boom)

    @pytest.mark.asyncio
    async def test_resolver_never_returns_none(self):
        """The str-or-raise contract: every successful resolution is a real key.
        ``None`` — the value the operator seam used to smuggle out — has no
        producing path left."""

        async def _fetch_key(uid):
            return "sk-real"

        for args in (("sk-byoc", None, _fetch_boom), (None, "u1", _fetch_key)):
            resolved = await resolve_request_api_key(*args)
            assert isinstance(resolved, str) and resolved
