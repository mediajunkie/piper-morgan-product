"""#1436 Tier-2: the /piper calendar|status|priority subcommands build REAL Intents.

Regression: all three constructed a pre-refactor Intent shape
(``raw_input=``/``classification=`` — fields the dataclass has never had) —
TypeError on every invocation, caught by each handler's except, so every
subcommand answered with the generic "having trouble" copy since the Intent
refactor. The canonical handlers themselves were fine; the glue was dead.
"""

from unittest.mock import AsyncMock, patch

from services.integrations.slack.webhook_router import SlackWebhookRouter
from services.shared_types import IntentCategory


def _router():
    return SlackWebhookRouter.__new__(SlackWebhookRouter)  # subcommands need no init state


CASES = [
    ("_handle_calendar_subcommand", "_handle_temporal_query",
     IntentCategory.TEMPORAL, "get_current_time"),
    ("_handle_status_subcommand", "_handle_status_query",
     IntentCategory.STATUS, "get_project_status"),
    ("_handle_priority_subcommand", "_handle_priority_query",
     IntentCategory.PRIORITY, "get_top_priority"),
]


async def test_subcommands_reach_their_canonical_handlers_with_valid_intents():
    for sub_name, handler_name, category, action in CASES:
        captured = {}

        async def fake_handler(intent, session_id, user_id=None, _c=captured):
            _c["intent"], _c["session_id"], _c["user_id"] = intent, session_id, user_id
            return {"message": f"real answer via {intent.action}"}

        with patch(
            f"services.intent_service.canonical_handlers.CanonicalHandlers.{handler_name}",
            new=AsyncMock(side_effect=fake_handler),
        ):
            out = await getattr(_router(), sub_name)(user_id="U123", channel_id="C1")

        intent = captured["intent"]
        assert intent.category == category, sub_name
        assert intent.action == action, sub_name
        assert intent.original_message  # detect-helpers read this
        assert captured["user_id"] == "U123"
        assert captured["session_id"] == "slack_U123"
        # The handler's real message reaches Slack (old code: generic failure copy)
        assert out["text"] == f"real answer via {action}", sub_name
        assert "having trouble" not in out["text"]
