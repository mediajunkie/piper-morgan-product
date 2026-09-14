"""#1807 — the one surviving server-key path, and the two default-OFF gates on it.

After #1807 the resolver has no "any authenticated user" rung. What remains is a
DESIGNATED OPERATOR PRINCIPAL, and this file pins that it is narrow, config-named, and
off unless someone explicitly turned it on.

TWO GATES, ON PURPOSE (both must hold):
  1. ``PIPER_OPERATOR_SERVER_KEY`` opted in — env, absent ⇒ off (the #1690
     ``PIPER_DEMO_PLUGIN`` operator-opt-in idiom). This is the "default OFF in hosted"
     half of AC 2.
  2. the caller IS the configured PM/operator, resolved through the EXISTING convention
     (``resolve_pm_owner_id``: env ``PIPER_PM_USER_ID`` → the "PM Identity" section of
     ``config/PIPER.user.md``; #1260 / ADR-071 D7). No new identity concept invented.

Gate 1 is not redundant with gate 2. ``PIPER_PM_USER_ID`` exists today to mark *document
provenance*. Without gate 1, any deployment that named its PM for ingest would silently
acquire a billable server-key path — config for one purpose quietly granting authority
for another. Gate 1 also guarantees the hosted default regardless of what identity config
happens to be present.

LAYER (m-43). ``resolve_pm_owner_id`` runs FOR REAL here, including its real env-override
branch and its real UUID parsing; only ``AsyncSessionFactory.session_scope_fresh`` is
stubbed, and the env-override branch returns before ever touching the session it is
handed. ``operator_server_key_opted_in`` is never stubbed — it reads the real env.

DENOMINATOR. Covered: the opt-in gate (off / on / truthy spellings), the identity gate
(match / mismatch / unconfigured / non-UUID caller), fail-closed on a resolution error,
and the resolver's own fail-closed default when no checker is injected at all. NOT
covered here: ``resolve_pm_owner_id``'s *username → users.id* DB branch (needs a real
database; it is #1260's own tested surface), and the route-level surfaces, which are
pinned in tests/unit/web/test_authenticated_keyless_server_key_1807.py and
tests/unit/web/api/routes/test_documents_keyless_refusal_1807.py.
"""

import contextlib
import uuid
from unittest.mock import patch

import pytest

from services.llm.request_key import (
    AnonymousLLMKeyRequiredError,
    UserLLMKeyRequiredError,
    operator_server_key_opted_in,
    resolve_request_api_key,
)
from web.utils.llm_key import is_designated_operator

OPERATOR_ID = "11111111-1111-4111-8111-111111111111"
SOMEONE_ELSE = "22222222-2222-4222-8222-222222222222"


@contextlib.asynccontextmanager
async def _fake_session():
    yield object()


@contextlib.contextmanager
def _no_database():
    """Stub only the session factory. `resolve_pm_owner_id` itself runs for real."""
    with patch(
        "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
        lambda *a, **k: _fake_session(),
    ):
        yield


async def _fetch_no_stored_key(uid):
    return None


async def _fetch_boom(uid):  # pragma: no cover - asserts it is never called
    raise AssertionError("stored-key lookup should not have been reached")


class TestTheOptInGate:
    """Gate 1: the operator's key is spendable only when someone typed the flag."""

    def test_absent_env_is_off(self, monkeypatch):
        monkeypatch.delenv("PIPER_OPERATOR_SERVER_KEY", raising=False)
        assert operator_server_key_opted_in() is False

    @pytest.mark.parametrize("value", ["1", "true", "TRUE", "yes", "on", " true "])
    def test_truthy_spellings_opt_in(self, monkeypatch, value):
        monkeypatch.setenv("PIPER_OPERATOR_SERVER_KEY", value)
        assert operator_server_key_opted_in() is True

    @pytest.mark.parametrize("value", ["", "0", "false", "no", "off", "maybe"])
    def test_everything_else_is_off(self, monkeypatch, value):
        monkeypatch.setenv("PIPER_OPERATOR_SERVER_KEY", value)
        assert operator_server_key_opted_in() is False

    @pytest.mark.asyncio
    async def test_operator_identity_alone_does_not_grant_spending(self, monkeypatch):
        """The point of having two gates: the configured PM, correctly identified, is
        still refused while the opt-in flag is off. Naming your PM for document
        provenance must never hand out a billable path."""
        monkeypatch.delenv("PIPER_OPERATOR_SERVER_KEY", raising=False)
        monkeypatch.setenv("PIPER_PM_USER_ID", OPERATOR_ID)

        with _no_database():
            assert await is_designated_operator(OPERATOR_ID) is False


class TestTheIdentityGate:
    """Gate 2: with the flag on, only the configured principal qualifies."""

    @pytest.mark.asyncio
    async def test_the_configured_operator_qualifies(self, monkeypatch):
        monkeypatch.setenv("PIPER_OPERATOR_SERVER_KEY", "1")
        monkeypatch.setenv("PIPER_PM_USER_ID", OPERATOR_ID)

        with _no_database():
            assert await is_designated_operator(OPERATOR_ID) is True

    @pytest.mark.asyncio
    async def test_a_different_authenticated_user_does_not(self, monkeypatch):
        """The alpha tester. Authenticated, real account, flag on — still not the
        operator, so still refused."""
        monkeypatch.setenv("PIPER_OPERATOR_SERVER_KEY", "1")
        monkeypatch.setenv("PIPER_PM_USER_ID", OPERATOR_ID)

        with _no_database():
            assert await is_designated_operator(SOMEONE_ELSE) is False

    @pytest.mark.asyncio
    async def test_no_operator_configured_qualifies_nobody(self, monkeypatch):
        """Flag on but no principal named (no env override, no PM Identity section —
        the shape of a stock hosted deployment): nobody gets the server key."""
        monkeypatch.setenv("PIPER_OPERATOR_SERVER_KEY", "1")
        monkeypatch.delenv("PIPER_PM_USER_ID", raising=False)

        with (
            _no_database(),
            patch(
                "services.configuration.piper_config_loader.PiperConfigLoader.load_pm_identity_config",
                return_value=None,
            ),
        ):
            assert await is_designated_operator(OPERATOR_ID) is False

    @pytest.mark.asyncio
    async def test_non_uuid_caller_never_matches(self, monkeypatch):
        monkeypatch.setenv("PIPER_OPERATOR_SERVER_KEY", "1")
        monkeypatch.setenv("PIPER_PM_USER_ID", OPERATOR_ID)

        with _no_database():
            assert await is_designated_operator("not-a-uuid") is False

    @pytest.mark.asyncio
    async def test_resolution_failure_refuses_never_allows(self, monkeypatch):
        """Fail-closed, the #1485/#1792 posture: if we cannot establish that the caller
        IS the operator, the answer is no. A store outage must not open a billing path."""
        monkeypatch.setenv("PIPER_OPERATOR_SERVER_KEY", "1")
        monkeypatch.setenv("PIPER_PM_USER_ID", OPERATOR_ID)

        def _explode(*a, **k):
            raise RuntimeError("database is down")

        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            _explode,
        ):
            assert await is_designated_operator(OPERATOR_ID) is False


class TestResolverContract:
    """What the resolver does with the operator verdict — including when it has none."""

    @pytest.mark.asyncio
    async def test_operator_true_yields_none_meaning_server_key(self):
        async def _is_operator(uid):
            return True

        resolved = await resolve_request_api_key(
            None, str(uuid.uuid4()), _fetch_no_stored_key, _is_operator
        )
        assert resolved is None  # None ⇒ anthropic_client_for_request returns the server client

    @pytest.mark.asyncio
    async def test_operator_false_refuses(self):
        async def _is_operator(uid):
            return False

        with pytest.raises(UserLLMKeyRequiredError):
            await resolve_request_api_key(
                None, str(uuid.uuid4()), _fetch_no_stored_key, _is_operator
            )

    @pytest.mark.asyncio
    async def test_no_checker_injected_refuses_fail_closed(self):
        """The default. A caller that has not deliberately wired the operator path
        cannot accidentally reopen it — omission refuses rather than falling back."""
        with pytest.raises(UserLLMKeyRequiredError):
            await resolve_request_api_key(None, str(uuid.uuid4()), _fetch_no_stored_key)

    @pytest.mark.asyncio
    async def test_stored_key_short_circuits_the_operator_check(self):
        """A user with their own key never reaches the operator question — the paying
        path stays the cheap path."""

        async def _fetch_key(uid):
            return "sk-their-own"

        async def _is_operator(uid):  # pragma: no cover - asserts it is never called
            raise AssertionError("operator check reached despite a stored key")

        assert await resolve_request_api_key(None, "u1", _fetch_key, _is_operator) == "sk-their-own"

    @pytest.mark.asyncio
    async def test_header_key_short_circuits_everything(self):
        """#1162 no-regress: BYOC wins, no DB, no operator question, login optional."""

        async def _is_operator(uid):  # pragma: no cover - asserts it is never called
            raise AssertionError("operator check reached despite a header key")

        assert (
            await resolve_request_api_key("sk-byoc", "u1", _fetch_boom, _is_operator) == "sk-byoc"
        )
        assert (
            await resolve_request_api_key("sk-byoc", None, _fetch_boom, _is_operator) == "sk-byoc"
        )

    @pytest.mark.asyncio
    async def test_no_regress_1320_anonymous_still_raises_its_own_error(self):
        """The anonymous refusal keeps its own type. The two are siblings, not one
        error with a flag — the remediations differ and #1520 is what conflating them
        costs."""

        async def _is_operator(uid):  # pragma: no cover - asserts it is never called
            raise AssertionError("operator check reached for an anonymous caller")

        with pytest.raises(AnonymousLLMKeyRequiredError):
            await resolve_request_api_key(None, None, _fetch_boom, _is_operator)
        with pytest.raises(AnonymousLLMKeyRequiredError):
            await resolve_request_api_key("", None, _fetch_boom, _is_operator)
