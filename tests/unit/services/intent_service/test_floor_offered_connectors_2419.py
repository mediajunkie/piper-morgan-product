"""Issue 2419 (Arch 01M832SQEC, CXO 01M8331YXP): the floor's context calls available
only what this host offers.

Served on beta 948af3a198: "Slack, Google Calendar, and Notion are available there too"
with an offer to set them up, while Settings says Slack and Notion are not in this beta.
The floor repeated a line code gave it ("- Not connected (available in Settings): ...").
The fix removes the false fact: that list and the per-connector connect sentences are
filtered through ``offered_connectors()``, read at call time. No prompt rule.
"""

from services.integrations.integration_status_service import STAGING_APP_NAME
from services.intent_service.conversational_floor import ConversationalFloor

WEB_SEED = [
    {"name": "github", "status": "needs_reconnecting"},
    {"name": "calendar", "status": "inactive"},
    {"name": "slack", "status": "inactive"},
    {"name": "notion", "status": "inactive"},
]


def _block(integrations):
    return ConversationalFloor(system_prompt_base="x")._format_domain_context(
        {"integrations": integrations}
    )


def _available_lines(block):
    """The not-connected line and the connect sentences under it."""
    out, inside = [], False
    for line in block.splitlines():
        if line.startswith("- Not connected (available in Settings)"):
            inside = True
            out.append(line)
        elif inside and line.startswith("  - "):
            out.append(line)
        else:
            inside = False
    return out


def test_beta_never_calls_slack_or_notion_available(monkeypatch):
    monkeypatch.delenv("FLY_APP_NAME", raising=False)
    lines = _available_lines(_block(WEB_SEED))
    assert lines[0] == "- Not connected (available in Settings): Google Calendar"
    text = "\n".join(lines)
    assert "Slack" not in text and "Notion" not in text


def test_beta_with_only_unoffered_inactive_has_no_available_line(monkeypatch):
    monkeypatch.delenv("FLY_APP_NAME", raising=False)
    block = _block(
        [
            {"name": "github", "status": "active"},
            {"name": "calendar", "status": "active"},
            {"name": "slack", "status": "inactive"},
            {"name": "notion", "status": "inactive"},
        ]
    )
    assert "available in Settings" not in block


def test_staging_still_lists_notion(monkeypatch):
    monkeypatch.setenv("FLY_APP_NAME", STAGING_APP_NAME)
    lines = _available_lines(_block(WEB_SEED))
    assert lines[0] == "- Not connected (available in Settings): Google Calendar, Notion"
    assert "Slack" not in "\n".join(lines)


def test_the_reconnect_line_is_untouched(monkeypatch):
    monkeypatch.delenv("FLY_APP_NAME", raising=False)
    assert "- Needs reconnecting (reconnect in Settings → Integrations): GitHub" in _block(WEB_SEED)
