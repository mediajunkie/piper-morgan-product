"""#1536 FTUX-COLDSTART — the user's own data in the FIRST exchange, unprompted.

Design spec: dev/active/design-spec-first-contact-plugin-surface-2026-07-31.md
§7a (RULED 2026-08-10, the converged three gate items):

1. Cold account + one connector authorized → the user's own data appears in
   the first exchange, unprompted — content naming at least one REAL entity.
2. NO fabricated entities — a named entity is a stored-state claim; entities
   may only come from a read that actually happened this turn. The gather IS
   that read; renderers are pure string formatting over the gathered payload,
   so they are structurally incapable of naming an entity the read didn't
   return.
3. "Only Piper could produce it" is a conformance judgment — reviewed, never
   gated. These tests aim for specificity (real names, real recency) and
   leave the judgment to review.

Plus CXO's flagged item (i): the first reply must NOT ask for scope before
showing data (no "which repo?" first — the #1327 default-repo rail resolves
the bound repo; unresolved → no demo at all, and the normal greeting stands).

Layer honesty (m-43): assembler tests assert on the gathered context dict;
floor tests assert on the `[Available context]` prompt block handed to the
LLM (the final floor reply is LLM-composed and not measured here); the
canonical-greeting tests assert on the FINAL user-facing message, because
that path's demonstration block is deterministic (no LLM between payload and
user copy).

Canaries: warm conversation (a completed turn exists) → no demo re-run;
cold + no connector → current behavior unchanged (no fake demo); failed read
→ honesty flag, never a fabricated demo (#1425).
"""

import re
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversation_context import get_or_create_context
from services.intent_service.conversational_floor import ConversationalFloor

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

DEMO_PAYLOAD = {
    "connector": "github",
    "repo": "acme/rocket",
    "items": [
        {
            "number": 123,
            "title": "Fix the login flow",
            "type": "issue",
            "recency": "updated today",
            "url": "https://github.com/acme/rocket/issues/123",
        },
        {
            "number": 456,
            "title": "Add CSV export",
            "type": "pr",
            "recency": "updated 3 days ago",
            "url": "https://github.com/acme/rocket/pull/456",
        },
    ],
    "open_count": 12,
}


class _PassthroughCache:
    """#984 seam without a Redis dependency: always compute."""

    async def get_or_compute(self, key, ttl_seconds, compute_fn):
        return await compute_fn()


_CATEGORY_GATHERERS = [
    "_gather_identity_context",
    "_gather_trust_context",
    "_gather_insight_pull_context",
    "_gather_memory_context",
    "_gather_temporal_context",
    "_gather_status_priority_context",
]


def _quiet_gatherers():
    """Patch the category gatherers + reminder/time rails to empty so tests
    isolate the first-contact rail (the real gatherers reach DB/GitHub)."""
    patchers = [
        patch.object(ContextAssembler, name, AsyncMock(return_value={}))
        for name in _CATEGORY_GATHERERS
    ]
    patchers.append(
        patch.object(ContextAssembler, "_gather_reminder_context", AsyncMock(return_value={}))
    )
    patchers.append(
        patch(
            "services.intent_service.context_assembler._current_time_for_user",
            AsyncMock(return_value=None),
        )
    )
    return patchers


def _fresh_cold_session(user_id=None):
    """A brand-new conversation with only the in-flight turn recorded —
    exactly the state process_intent leaves at handler time (#1122)."""
    session_id = str(uuid4())
    conv_ctx = get_or_create_context(session_id, user_id=user_id)
    conv_ctx.add_turn(message="hello")  # in-flight: response stays None
    return session_id


def _warm_session(user_id=None):
    """A conversation with one COMPLETED exchange (turn has a response)."""
    session_id = str(uuid4())
    conv_ctx = get_or_create_context(session_id, user_id=user_id)
    conv_ctx.add_turn(message="hello")
    conv_ctx.turns[-1].response = "Hi! What are you working on?"
    conv_ctx.add_turn(message="what can you see?")  # in-flight turn 2
    return session_id


# ---------------------------------------------------------------------------
# is_first_exchange — the honest newness signal
# ---------------------------------------------------------------------------


class TestIsFirstExchange:
    def test_true_on_fresh_session_with_in_flight_turn(self):
        from services.intent_service.first_contact import is_first_exchange

        user_id = str(uuid4())
        session_id = _fresh_cold_session(user_id)
        assert is_first_exchange(session_id, user_id) is True

    def test_true_on_empty_context(self):
        from services.intent_service.first_contact import is_first_exchange

        assert is_first_exchange(str(uuid4()), str(uuid4())) is True

    def test_false_after_completed_exchange(self):
        from services.intent_service.first_contact import is_first_exchange

        user_id = str(uuid4())
        session_id = _warm_session(user_id)
        assert is_first_exchange(session_id, user_id) is False

    def test_false_without_session(self):
        from services.intent_service.first_contact import is_first_exchange

        assert is_first_exchange(None, str(uuid4())) is False


# ---------------------------------------------------------------------------
# gather_first_contact_demo — the read that IS the entity source
# ---------------------------------------------------------------------------


def _status_service(configured: bool):
    inst = MagicMock()
    inst.is_configured = AsyncMock(return_value=configured)
    return patch(
        "services.integrations.integration_status_service.IntegrationStatusService",
        return_value=inst,
    )


def _resolved_repo():
    from services.integrations.github.repo_resolver import ResolvedRepo

    return ResolvedRepo(owner="acme", name="rocket", source="user_default")


def _router_returning(issues, raise_on_read=False):
    inst = MagicMock()
    inst.initialize = AsyncMock(return_value=None)
    inst.close = AsyncMock(return_value=None)
    if raise_on_read:
        inst.get_open_issues = AsyncMock(side_effect=RuntimeError("boom"))
    else:
        inst.get_open_issues = AsyncMock(return_value=issues)
    return patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
        return_value=inst,
    )


GITHUB_ISSUES = [
    {
        "number": 123,
        "title": "Fix the login flow",
        "state": "open",
        "updated_at": "2026-08-10T09:00:00Z",
        "is_pull_request": False,
        "uri": "https://github.com/acme/rocket/issues/123",
    },
    {
        "number": 456,
        "title": "Add CSV export",
        "state": "open",
        "updated_at": "2026-08-07T09:00:00Z",
        "is_pull_request": True,
        "uri": "https://github.com/acme/rocket/pull/456",
    },
]


class TestGatherFirstContactDemo:
    @pytest.mark.asyncio
    async def test_no_user_id_returns_empty(self):
        """Principal-threaded: no authenticated principal → no read, no demo."""
        from services.intent_service.first_contact import gather_first_contact_demo

        assert await gather_first_contact_demo(None, cache=_PassthroughCache()) == {}

    @pytest.mark.asyncio
    async def test_no_connector_returns_empty(self):
        """No-connector canary: cold + nothing configured → nothing injected."""
        from services.intent_service.first_contact import gather_first_contact_demo

        with _status_service(False):
            result = await gather_first_contact_demo(str(uuid4()), cache=_PassthroughCache())
        assert result == {}

    @pytest.mark.asyncio
    async def test_payload_carries_real_entities(self):
        """Gate item 1's source: the gather returns the repo + real items."""
        from services.intent_service.first_contact import gather_first_contact_demo

        with _status_service(True), patch(
            "services.integrations.github.repo_resolver.resolve_repo",
            AsyncMock(return_value=_resolved_repo()),
        ), _router_returning(GITHUB_ISSUES):
            result = await gather_first_contact_demo(str(uuid4()), cache=_PassthroughCache())

        demo = result.get("first_contact_demo")
        assert demo, f"no demo payload gathered (got {result})"
        assert demo["repo"] == "acme/rocket"
        assert demo["open_count"] == 2
        numbers = [i["number"] for i in demo["items"]]
        assert numbers == [123, 456]  # recency order, most recent first
        assert demo["items"][0]["title"] == "Fix the login flow"
        assert demo["items"][1]["type"] == "pr"
        # Real recency: humanized, derived from updated_at — never absent
        assert all(i.get("recency") for i in demo["items"])

    @pytest.mark.asyncio
    async def test_router_failure_is_honest_never_fake(self):
        """#1425: a failed read flags source_failed — never a fabricated demo."""
        from services.intent_service.first_contact import gather_first_contact_demo

        with _status_service(True), patch(
            "services.integrations.github.repo_resolver.resolve_repo",
            AsyncMock(return_value=_resolved_repo()),
        ), _router_returning([], raise_on_read=True):
            result = await gather_first_contact_demo(str(uuid4()), cache=_PassthroughCache())

        assert result == {"first_contact_source_failed": True}
        assert "first_contact_demo" not in result

    @pytest.mark.asyncio
    async def test_unresolved_repo_yields_no_demo_and_no_scope_question(self):
        """CXO item (i): with no resolvable repo there is no data to show —
        nothing is injected (the reply must not ask 'which repo?' first)."""
        from services.integrations.github.repo_resolver import UnresolvedRepoError
        from services.intent_service.first_contact import gather_first_contact_demo

        with _status_service(True), patch(
            "services.integrations.github.repo_resolver.resolve_repo",
            AsyncMock(side_effect=UnresolvedRepoError("no repo")),
        ):
            result = await gather_first_contact_demo(str(uuid4()), cache=_PassthroughCache())
        assert result == {}

    @pytest.mark.asyncio
    async def test_empty_read_yields_no_demo(self):
        """[] conflates adapter-swallowed errors with genuine zero (the MCP
        adapter returns [] on failure) — asserting emptiness would be an
        unverified stored-state claim (m-44). No demo; behavior unchanged."""
        from services.intent_service.first_contact import gather_first_contact_demo

        with _status_service(True), patch(
            "services.integrations.github.repo_resolver.resolve_repo",
            AsyncMock(return_value=_resolved_repo()),
        ), _router_returning([]):
            result = await gather_first_contact_demo(str(uuid4()), cache=_PassthroughCache())
        assert result == {}


# ---------------------------------------------------------------------------
# render_first_contact_block — deterministic user copy (canonical greeting)
# ---------------------------------------------------------------------------


class TestRenderFirstContactBlock:
    def test_block_names_repo_and_entities(self):
        from services.intent_service.first_contact import render_first_contact_block

        block = render_first_contact_block(DEMO_PAYLOAD)
        assert "acme/rocket" in block  # scope named inside the claim
        assert "#123" in block and "Fix the login flow" in block
        assert "#456" in block and "Add CSV export" in block
        assert "12" in block  # open_count, row-derived denominator
        assert "updated today" in block  # real recency
        assert "which repo" not in block.lower()  # CXO item (i)

    def test_no_fabrication_pin_entities_subset_of_payload(self):
        """Hostile pin (gate item 2): every #N in the output exists in the
        payload — the renderer is pure formatting, no extra names possible."""
        from services.intent_service.first_contact import render_first_contact_block

        block = render_first_contact_block(DEMO_PAYLOAD)
        payload_numbers = {str(i["number"]) for i in DEMO_PAYLOAD["items"]}
        rendered_numbers = set(re.findall(r"#(\d+)", block))
        assert rendered_numbers, "no entities rendered at all"
        assert rendered_numbers.issubset(payload_numbers), (
            f"renderer emitted entity numbers not in the payload: "
            f"{rendered_numbers - payload_numbers}"
        )

    def test_empty_or_failed_payload_renders_nothing(self):
        from services.intent_service.first_contact import render_first_contact_block

        assert render_first_contact_block(None) == ""
        assert render_first_contact_block({}) == ""
        assert render_first_contact_block({"repo": "acme/rocket", "items": []}) == ""


# ---------------------------------------------------------------------------
# ContextAssembler — the first-contact rail rides the cold first turn only
# ---------------------------------------------------------------------------


async def _gather_with(category, session_id, user_id, demo_result):
    patchers = _quiet_gatherers()
    for p in patchers:
        p.start()
    try:
        import services.intent_service.first_contact as fc

        with patch.object(
            fc, "gather_first_contact_demo", AsyncMock(return_value=demo_result)
        ) as gather_mock:
            assembler = ContextAssembler(cache=_PassthroughCache())
            context = await assembler.gather_context(
                category, user_id=user_id, session_id=session_id
            )
            return context, gather_mock, assembler
    finally:
        for p in patchers:
            p.stop()


class TestAssemblerFirstContactRail:
    @pytest.mark.asyncio
    async def test_cold_conversation_with_connector_gets_demo(self):
        """RED before #1536: a cold CONVERSATION turn assembled no user data
        at all (the category branch is a deliberate pass)."""
        user_id = str(uuid4())
        session_id = _fresh_cold_session(user_id)
        context, gather_mock, assembler = await _gather_with(
            "CONVERSATION", session_id, user_id, {"first_contact_demo": DEMO_PAYLOAD}
        )
        assert context.get("first_contact_demo") == DEMO_PAYLOAD, (
            f"first-contact demo missing from cold-turn context "
            f"(keys: {list(context.keys())})"
        )
        gather_mock.assert_awaited_once()
        # #1030 R4: the key is provenance-attributed like every gathered key
        assert "first_contact_demo" in assembler.get_last_provenance()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("category", ["UNKNOWN", "STATUS", "IDENTITY"])
    async def test_rail_rides_other_floor_categories_too(self, category):
        """A cold first message needn't be a greeting — any floor-bound first
        turn (e.g. an unrailed QUERY through _handle_unknown_intent) gets it."""
        user_id = str(uuid4())
        session_id = _fresh_cold_session(user_id)
        context, _, _ = await _gather_with(
            category, session_id, user_id, {"first_contact_demo": DEMO_PAYLOAD}
        )
        assert context.get("first_contact_demo") == DEMO_PAYLOAD

    @pytest.mark.asyncio
    async def test_warm_conversation_does_not_rerun_demo(self):
        """Warm canary: a completed exchange exists → no re-demonstration,
        and no read is even attempted."""
        user_id = str(uuid4())
        session_id = _warm_session(user_id)
        context, gather_mock, _ = await _gather_with(
            "CONVERSATION", session_id, user_id, {"first_contact_demo": DEMO_PAYLOAD}
        )
        assert "first_contact_demo" not in context
        gather_mock.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_missing_user_or_session_skips_demo(self):
        context, gather_mock, _ = await _gather_with(
            "CONVERSATION", None, str(uuid4()), {"first_contact_demo": DEMO_PAYLOAD}
        )
        assert "first_contact_demo" not in context
        gather_mock.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_first_contact_failure_never_breaks_the_gather(self):
        """Rail isolation (the #1566 pattern): a first-contact crash degrades
        to the pre-#1536 context, never a dead turn."""
        user_id = str(uuid4())
        session_id = _fresh_cold_session(user_id)
        patchers = _quiet_gatherers()
        for p in patchers:
            p.start()
        try:
            import services.intent_service.first_contact as fc

            with patch.object(
                fc, "gather_first_contact_demo", AsyncMock(side_effect=RuntimeError("boom"))
            ):
                assembler = ContextAssembler(cache=_PassthroughCache())
                context = await assembler.gather_context(
                    "CONVERSATION", user_id=user_id, session_id=session_id
                )
        finally:
            for p in patchers:
                p.stop()
        assert isinstance(context, dict)
        assert "first_contact_demo" not in context

    @pytest.mark.asyncio
    async def test_source_failed_flag_reaches_context(self):
        """#1425 honesty end-to-end: the failure flag rides to the floor."""
        user_id = str(uuid4())
        session_id = _fresh_cold_session(user_id)
        context, _, _ = await _gather_with(
            "CONVERSATION", session_id, user_id, {"first_contact_source_failed": True}
        )
        assert context.get("first_contact_source_failed") is True


# ---------------------------------------------------------------------------
# Floor prompt rendering — entities reach the LLM from the gathered block ONLY
# ---------------------------------------------------------------------------


class TestFloorRendersFirstContactDemo:
    def test_demo_block_rendered_with_entities_and_directive(self):
        floor = ConversationalFloor()
        block = floor._format_domain_context({"first_contact_demo": DEMO_PAYLOAD})
        assert "acme/rocket" in block
        assert "#123" in block and "Fix the login flow" in block
        assert "updated today" in block  # real recency, humanized
        # The no-fabrication directive rides WITH the data
        assert "ONLY" in block
        # CXO item (i): the directive forbids a scope question before data
        assert "scope" in block.lower() or "which repo" in block.lower()

    def test_prompt_entities_subset_of_payload(self):
        """Hostile pin at the prompt layer: every #N the LLM is shown comes
        from the gathered payload."""
        floor = ConversationalFloor()
        block = floor._format_domain_context({"first_contact_demo": DEMO_PAYLOAD})
        payload_numbers = {str(i["number"]) for i in DEMO_PAYLOAD["items"]}
        rendered_numbers = set(re.findall(r"#(\d+)", block))
        assert rendered_numbers, "no entities rendered into the prompt block"
        assert rendered_numbers.issubset(payload_numbers), (
            f"prompt block carries entity numbers not in the payload: "
            f"{rendered_numbers - payload_numbers}"
        )

    def test_source_failed_renders_couldnt_check_never_empty_claim(self):
        floor = ConversationalFloor()
        block = floor._format_domain_context({"first_contact_source_failed": True})
        assert "FAILED" in block
        assert "invent" in block.lower() or "empty" in block.lower()

    def test_no_demo_key_renders_nothing_new(self):
        floor = ConversationalFloor()
        assert floor._format_domain_context({}) == ""


# ---------------------------------------------------------------------------
# Canonical greeting — the deterministic demonstration on "hello"
# ---------------------------------------------------------------------------


def _greeting_intent(user_id):
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    intent = Intent(
        category=IntentCategory.CONVERSATION,
        action="greeting",
        confidence=0.99,
        original_message="hello",
    )
    intent.context = {"user_id": user_id}
    return intent


class TestCanonicalGreetingFirstContact:
    @pytest.mark.asyncio
    async def test_cold_greeting_carries_real_entity(self):
        """Gate item 1 on the pure-'hello' path: the FIRST reply names the
        user's own data, unprompted — deterministic append, no LLM between
        payload and user copy."""
        from services.conversation.conversation_handler import ConversationHandler

        user_id = str(uuid4())
        session_id = _fresh_cold_session(user_id)
        handler = ConversationHandler()

        import services.intent_service.first_contact as fc

        with patch.object(
            handler, "_check_suspended_session_reentry", AsyncMock(return_value=None)
        ), patch.object(
            handler, "_get_calendar_summary", AsyncMock(return_value=None)
        ), patch.object(
            fc, "gather_first_contact_demo", AsyncMock(return_value={"first_contact_demo": DEMO_PAYLOAD})
        ):
            result = await handler._respond_to_greeting(
                _greeting_intent(user_id), session_id, user_id=user_id
            )

        message = result["message"]
        assert "acme/rocket" in message
        assert "#123" in message and "Fix the login flow" in message
        # CXO item (i): no scope request ahead of the data
        assert "which repo" not in message.lower()

    @pytest.mark.asyncio
    async def test_warm_greeting_unchanged(self):
        """Warm canary on the canonical path: no re-demonstration, no read."""
        from services.conversation.conversation_handler import ConversationHandler

        user_id = str(uuid4())
        session_id = _warm_session(user_id)
        handler = ConversationHandler()

        import services.intent_service.first_contact as fc

        with patch.object(
            handler, "_check_suspended_session_reentry", AsyncMock(return_value=None)
        ), patch.object(
            handler, "_get_calendar_summary", AsyncMock(return_value=None)
        ), patch.object(
            fc, "gather_first_contact_demo", AsyncMock(return_value={"first_contact_demo": DEMO_PAYLOAD})
        ) as gather_mock:
            result = await handler._respond_to_greeting(
                _greeting_intent(user_id), session_id, user_id=user_id
            )

        assert "acme/rocket" not in result["message"]
        gather_mock.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_cold_greeting_without_connector_unchanged(self):
        """No-connector canary: the greeting is exactly the pre-#1536 shape —
        no fake demo, no new copy."""
        from services.conversation.conversation_handler import ConversationHandler

        user_id = str(uuid4())
        session_id = _fresh_cold_session(user_id)
        handler = ConversationHandler()

        import services.intent_service.first_contact as fc

        with patch.object(
            handler, "_check_suspended_session_reentry", AsyncMock(return_value=None)
        ), patch.object(
            handler, "_get_calendar_summary", AsyncMock(return_value=None)
        ), patch.object(
            fc, "gather_first_contact_demo", AsyncMock(return_value={})
        ):
            result = await handler._respond_to_greeting(
                _greeting_intent(user_id), session_id, user_id=user_id
            )

        assert "acme/rocket" not in result["message"]
        assert "#123" not in result["message"]

    @pytest.mark.asyncio
    async def test_failed_read_never_fakes_a_demo_in_greeting(self):
        """#1425 on the deterministic path: source_failed appends nothing
        (the deterministic renderer has no honest-failure sentence to add
        without turning the greeting into an error report)."""
        from services.conversation.conversation_handler import ConversationHandler

        user_id = str(uuid4())
        session_id = _fresh_cold_session(user_id)
        handler = ConversationHandler()

        import services.intent_service.first_contact as fc

        with patch.object(
            handler, "_check_suspended_session_reentry", AsyncMock(return_value=None)
        ), patch.object(
            handler, "_get_calendar_summary", AsyncMock(return_value=None)
        ), patch.object(
            fc, "gather_first_contact_demo",
            AsyncMock(return_value={"first_contact_source_failed": True}),
        ):
            result = await handler._respond_to_greeting(
                _greeting_intent(user_id), session_id, user_id=user_id
            )

        assert "acme/rocket" not in result["message"]
        assert "#" not in result["message"]
