"""#2236: the capability answer is rendered in code from the #1428 ledger and the
#1547 status read; the floor model contributes at most one guarded opener."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.intent_service.capability_answer import (
    COULDNT_CHECK_LINE,
    compose_capability_reply,
    render_capability_block,
    sanitize_opener,
)
from services.intent_service.capability_legibility import (
    capability_answer_lines_with_outwardness,
)
from services.intent_service.conversational_floor import ConversationalFloor, FloorContext

LEDGER = capability_answer_lines_with_outwardness()


def _ctx(integrations=None, failed=False):
    dc = {"capabilities": list(LEDGER)}
    if integrations is not None:
        dc["integrations"] = integrations
    if failed:
        dc["integrations_source_failed"] = True
    return dc


CONNECTED = [
    {"name": "github", "status": "active"},
    {"name": "calendar", "status": "inactive"},
    {"name": "slack", "status": "inactive"},
    {"name": "notion", "status": "inactive"},
]
NONE_CONNECTED = [
    {"name": n, "status": "inactive"} for n in ("github", "calendar", "slack", "notion")
]


async def _serve(model_text, domain_context, category="DISCOVERY", action="get_capabilities"):
    llm = MagicMock()
    llm.complete = AsyncMock(return_value=model_text)
    floor = ConversationalFloor(llm_client=llm, system_prompt_base="You are Piper.")
    ctx = FloorContext(
        user_message="What can you help me with?",
        session_id="s",
        user_id=None,
        intent_category=category,
        intent_action=action,
        intent_confidence=0.99,
        domain_context=domain_context,
    )
    resp = await floor.respond(ctx)
    return resp.message, llm


class TestLedgerRendered:
    @pytest.mark.asyncio
    async def test_ledger_lines_verbatim_and_in_order(self):
        msg, _ = await _serve("NONE", _ctx(CONNECTED))
        pos = -1
        for line in LEDGER:
            nxt = msg.find(line, pos + 1)
            assert nxt > pos, f"ledger line missing or out of order: {line!r}"
            pos = nxt

    @pytest.mark.asyncio
    async def test_model_cannot_add_a_capability_sentence(self):
        said = "I'll surface things proactively and remind you when something is due."
        msg, _ = await _serve(said, _ctx(CONNECTED))
        assert "proactively" not in msg and "remind you" not in msg
        assert LEDGER[0] in msg

    @pytest.mark.asyncio
    async def test_model_is_not_given_the_ledger_or_connection_state(self):
        _, llm = await _serve("NONE", _ctx(CONNECTED))
        prompt = llm.complete.call_args.kwargs["prompt"]
        assert LEDGER[-1] not in prompt
        assert "Connected integrations" not in prompt
        assert "Capability turn" in prompt

    @pytest.mark.asyncio
    async def test_bare_block_without_opener_is_valid(self):
        msg, _ = await _serve("NONE", _ctx(CONNECTED))
        assert msg.startswith("What I can do today:")

    @pytest.mark.asyncio
    async def test_clean_opener_rides_above_the_block(self):
        msg, _ = await _serve("You're mid-way through the Q4 planning project.", _ctx(CONNECTED))
        assert msg.startswith("You're mid-way through the Q4 planning project.\n\n")


class TestIdentityUnchanged:
    @pytest.mark.asyncio
    async def test_get_identity_turn_serves_the_models_answer_and_no_block(self):
        said = "I'm Piper Morgan, your PM assistant."
        msg, llm = await _serve(said, _ctx(CONNECTED), category="IDENTITY", action="get_identity")
        assert msg == said
        assert "Here is what you can ask me for" not in msg
        prompt = llm.complete.call_args.kwargs["prompt"]
        assert "Capability turn" not in prompt
        assert LEDGER[-1] in prompt  # the model still sees the ledger, as on main


class TestConnectionState:
    def test_connected_account_names_its_tools_from_the_status_read(self):
        block = render_capability_block(_ctx(CONNECTED))
        assert "- GitHub: chat reads" in block
        assert "Not connected, so I'm not using them" in block
        assert (
            "Not connected, so I'm not using them (connect in Settings → Integrations): Google Calendar"
            in block
        )
        assert "Slack" not in block and "Notion" not in block

    def test_nothing_connected_says_so_and_implies_no_source_in_use(self):
        block = render_capability_block(_ctx(NONE_CONNECTED))
        assert "None of your tools are connected yet, so I'm not reading from any of them." in block
        assert "You can connect GitHub or Google Calendar in Settings → Integrations." in block
        assert "Not connected" not in block
        assert "what I read from each" not in block
        assert COULDNT_CHECK_LINE not in block

    def test_failed_read_says_exactly_couldnt_check_and_no_connection_facts(self):
        for dc in (_ctx(CONNECTED, failed=True), _ctx(None, failed=True), _ctx(None), _ctx([])):
            block = render_capability_block(dc)
            assert COULDNT_CHECK_LINE == "I couldn't check which tools you've connected just now."
            assert block.endswith(COULDNT_CHECK_LINE)
            for banned in ("Not connected", "not connected", "Connected", "GitHub", "Settings"):
                assert banned not in block.split("\n\n")[-1].replace(COULDNT_CHECK_LINE, "")

    def test_needs_reconnecting_is_not_called_connected(self):
        block = render_capability_block(_ctx([{"name": "github", "status": "needs_reconnecting"}]))
        assert "Needs reconnecting" in block and "GitHub" in block
        assert "Connected, and what I read" not in block

    def test_not_connected_list_names_only_beta_connectors(self):
        payload = [
            {"name": "slack", "status": "active"},
            {"name": "github", "status": "inactive"},
            {"name": "calendar", "status": "inactive"},
            {"name": "notion", "status": "inactive"},
        ]
        block = render_capability_block(_ctx(payload))
        assert block.endswith(
            "Not connected, so I'm not using them (connect in Settings → Integrations): "
            "GitHub, Google Calendar"
        )
        assert "Notion" not in block
        assert "- Slack: " in block  # a connected tool may still be listed

    def test_offered_connectors_is_exactly_github_and_calendar(self):
        from services.integrations.integration_status_service import BETA_OFFERED_CONNECTORS

        assert BETA_OFFERED_CONNECTORS == {"github": "GitHub", "calendar": "Google Calendar"}

    def test_not_connected_list_is_the_constant_minus_connected(self):
        from services.integrations.integration_status_service import BETA_OFFERED_CONNECTORS

        payload = [{"name": k, "status": "inactive"} for k in BETA_OFFERED_CONNECTORS]
        payload[0] = {"name": payload[0]["name"], "status": "active"}
        block = render_capability_block(_ctx(payload))
        remaining = [v for k, v in BETA_OFFERED_CONNECTORS.items() if k != payload[0]["name"]]
        assert block.endswith(": " + ", ".join(remaining))

    def test_block_reads_the_shared_constant_not_a_copy(self, monkeypatch):
        import services.integrations.integration_status_service as svc

        monkeypatch.setattr(svc, "BETA_OFFERED_CONNECTORS", {"notion": "Notion X"})
        payload = [
            {"name": "github", "status": "active"},
            {"name": "notion", "status": "inactive"},
            {"name": "calendar", "status": "inactive"},
        ]
        block = render_capability_block(_ctx(payload))
        assert block.endswith(": Notion X")


class TestOpenerGuard:
    @pytest.mark.parametrize(
        "opener",
        [
            "I'll learn how you work over time.",
            "I remember what you told me last week.",
            "I can remind you about your due items.",
            "I'll be proactive about your projects.",
            "Here's the honest picture of what I do.",
            "Good timing to ask.",
        ],
    )
    def test_drops_claims_and_filler(self, opener):
        assert sanitize_opener(opener) is None

    def test_drops_multi_line_and_none_token(self):
        assert sanitize_opener("one\ntwo") is None
        assert sanitize_opener("NONE") is None
        assert sanitize_opener("") is None and sanitize_opener(None) is None

    def test_keeps_a_plain_opener_tied_to_the_users_data(self):
        assert sanitize_opener("Your launch project is the open thread today.")

    def test_compose_without_opener_is_the_bare_block(self):
        dc = _ctx(CONNECTED)
        assert compose_capability_reply(None, dc) == render_capability_block(dc)


class TestPullInsightsRowStaysHonest:
    """Arch ruling 1 (2236): the ledger row "what have you learned about my work style?"
    stays only while an empty or failed insights read cannot be voiced as a learned
    pattern. LAYER: the floor prompt the model is handed (served prose is model-composed
    and not measured here)."""

    def _prompt(self, domain_context):
        floor = ConversationalFloor(llm_client=MagicMock(), system_prompt_base="x")
        return floor._format_domain_context(domain_context)

    def test_empty_repository_says_nothing_yet_and_implies_no_pattern(self):
        out = self._prompt({"insights": {"is_empty": True, "total_count": 0}})
        assert "NONE YET" in out
        assert "you have not yet learned patterns" in out
        assert "Do not fabricate" in out
        assert "HIGH CONFIDENCE" not in out

    def test_empty_state_makes_no_forward_looking_promise(self):
        out = self._prompt({"insights": {"is_empty": True, "total_count": 0}}).lower()
        for promise in ("will emerge", "as you work together", "over time", "insight journal"):
            assert promise not in out

    def test_failed_read_takes_the_could_not_check_path_never_nothing_yet(self):
        from services.intent_service.rail_read_failure import RAIL_READ_SOURCES

        assert "pull_insights" in RAIL_READ_SOURCES
        out = self._prompt({"insights_source_failed": True})
        assert "could not check: insights" in out
        assert "NONE YET" not in out
