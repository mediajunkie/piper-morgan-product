"""#2258 — the "what changed" Actions block names what Piper did, in the person's terms.

Alpha (2026-11-02, #1680's rows): the block grouped audit rows by ``event_type`` and
printed "consequential: 2". The landed shape (CXO's words 18:59, 21:4x, 21:48, 22:01;
Arch's rulings 19:3x, 21:46, 21:58):

- ONE predicate picks the rows, successes and attempts alike
  (``consequential_sites.person_visible_action``): the #1680 writer's rows (event type
  consequential, a registered site key), not nested in another site's call, and the
  site ``user_visible``. A login, an API-key event or an admin mint never reads as a
  change Piper made; an outer action is never counted twice; the Slack "thinking"
  placeholder is housekeeping and is hidden from both halves (the admin read still
  counts it: tests/unit/web/api/routes/test_admin_consequential_1680.py).
- Every line is the registry's phrase for the row's site (``phrase`` after "I tried
  to", ``done`` for the success list) with the row's ``resource_id`` in its slot; the
  row's ``message`` is never printed or parsed.
- Successes first under "Piper made N changes for you." (N counts rows), then the
  attempts that did not go through (#2151: never listed as done, never counted), no
  status word, no cause, no parenthetical. Identical rendered lines group with a
  count, CXO's no-bracket form; a group of one prints no count.

Same no-LLM, no-database harness as #2140.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from services.intent import intent_service as mod
from services.security.audit_logger import EventType
from services.security.consequential_sites import (
    CONSEQUENTIAL_EVENT_TYPE,
    CONSEQUENTIAL_SITES,
    SLACK,
)
from tests.unit.services.intent_service.test_changes_query_fail_closed_2140 import (  # noqa: F401
    NOTHING_NEW,
    _intent,
    _run,
    intent_service,
)

CHANNEL = "C0AB12CD34"
_STATUS_WORDS = ("success", "failed", "unconfirmed", "error")
_NEVER = ("consequential", "event_type", "auth", "(", ")", CHANNEL) + _STATUS_WORDS
_SITE_KEYS = tuple(CONSEQUENTIAL_SITES)
_VISIBLE = tuple(k for k, s in CONSEQUENTIAL_SITES.items() if s.user_visible)


def _audit(
    site,
    status="success",
    resource_id=None,
    minutes_ago=5,
    event_type=CONSEQUENTIAL_EVENT_TYPE,
    message="internal log label",
    nested_in=None,
):
    row = MagicMock()
    row.status = status
    row.action = site
    row.event_type = event_type
    row.message = message
    row.resource_id = resource_id
    row.details = {"nested_in": nested_in} if nested_in else None
    row.created_at = datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)
    return row


def _resource_for(site):
    """A resource of the kind the site's writer stores (Lead's read of the writers)."""
    entry = CONSEQUENTIAL_SITES[site]
    if entry.family == SLACK:
        return CHANNEL
    return "owner/repo" if "create_issue" in site else "38"


def _assert_no_internal_labels(message):
    low = message.lower()
    for word in _NEVER + _SITE_KEYS:
        assert word.lower() not in low, f"{word!r} leaked into the reply: {message!r}"


def _after_opener(message):
    """The reply's lines after the opener sentence and its blank line, for order
    assertions (the Tasks and Projects blocks are absent in these fixtures)."""
    lines = message.split("\n")[1:]
    while lines and lines[0] == "":
        lines.pop(0)
    return lines


# ── CXO's words, pinned by text ─────────────────────────────────────────────────


def test_constants_are_cxos_words():
    assert mod.CHANGES_ACTIONS_HEADLINE == "Piper made {count} change{s} for you."
    assert mod.CHANGES_ACTION_DONE_REPEATED == "{line}, {n} times"
    assert mod.CHANGES_ACTION_FAILED == "I tried to {phrase}, but it didn't go through."
    assert (
        mod.CHANGES_ACTION_FAILED_REPEATED
        == "I tried to {phrase} {n} times, but it didn't go through."
    )
    assert mod.CHANGES_ACTION_UNCONFIRMED == (
        "I tried to {phrase}, but I couldn't confirm it went through. "
        "Check before you rely on it."
    )
    assert mod.CHANGES_ACTION_UNCONFIRMED_REPEATED == (
        "I tried to {phrase} {n} times, but I couldn't confirm it went through. "
        "Check before you rely on it."
    )


def test_the_registry_event_type_is_the_audit_loggers():
    assert CONSEQUENTIAL_EVENT_TYPE == EventType.CONSEQUENTIAL == "consequential"


# ── CXO's pin: one success, one failed, one unconfirmed ─────────────────────────


@pytest.mark.asyncio
async def test_one_success_one_failed_one_unconfirmed(intent_service):
    rows = [
        _audit("github.chat.close_issue", "success", "38", 2),
        _audit("github.chat.comment_issue", "failed", "40", 4),
        _audit("slack.socket.reply", "unconfirmed", CHANNEL, 6),
    ]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert result.success is True
    assert _after_opener(result.message) == [
        "Piper made 1 change for you.",
        "  - Closed issue #38",
        "I tried to comment on issue #40, but it didn't go through.",
        "I tried to reply in Slack, but I couldn't confirm it went through. "
        "Check before you rely on it.",
    ]
    assert "internal log label" not in result.message
    _assert_no_internal_labels(result.message)


# ── Arch's render pin: every site's row, every outcome, no label ever ───────────


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["success", "failed", "unconfirmed"])
@pytest.mark.parametrize("site", _SITE_KEYS)
async def test_every_sites_row_renders_the_registry_phrase_and_no_label(
    intent_service, site, status
):
    entry = CONSEQUENTIAL_SITES[site]
    row = _audit(site, status, _resource_for(site), message=f"label for {site}")
    result, _ = await _run(intent_service, _intent(), [row], [], [])
    message = result.message
    _assert_no_internal_labels(message)
    assert f"label for {site}" not in message
    if not entry.user_visible:
        # hidden from both halves: the window reads as nothing new
        assert message == NOTHING_NEW.format(window="since yesterday")
        return
    done = entry.done.replace("{resource}", _resource_for(site))
    phrase = entry.phrase.replace("{resource}", _resource_for(site))
    if status == "success":
        assert "Piper made 1 change for you." in message
        assert f"  - {done}" in message
        assert "I tried to" not in message
    elif status == "failed":
        assert "Piper made" not in message
        assert f"I tried to {phrase}, but it didn't go through." in message
    else:
        assert "Piper made" not in message
        assert (
            f"I tried to {phrase}, but I couldn't confirm it went through. "
            "Check before you rely on it."
        ) in message
    assert "times" not in message


# ── The resource slot: #number for issue rows, owner/repo for creates, none for Slack ──


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "site, resource, done_line",
    [
        ("github.chat.close_issue", "38", "Closed issue #38"),
        ("github.chat.reopen_issue", "38", "Reopened issue #38"),
        ("github.chat.comment_issue", "38", "Commented on issue #38"),
        ("github.chat.update_issue", "38", "Updated issue #38"),
        ("github.domain.update_issue", "38", "Updated issue #38"),
        ("github.chat.create_issue", "owner/repo", "Created an issue in owner/repo"),
        ("github.command.create_issue", "owner/repo", "Created an issue in owner/repo"),
        ("github.domain.create_issue", "owner/repo", "Created an issue in owner/repo"),
        (
            "github.standup.create_issue",
            "owner/repo",
            "Created an issue in owner/repo from your standup",
        ),
        ("slack.domain.post_message", CHANNEL, "Posted to Slack"),
        ("slack.standup.post", CHANNEL, "Posted your standup to Slack"),
        ("slack.socket.slash_reply", CHANNEL, "Replied to a Slack command"),
    ],
)
async def test_resource_slot_renders_from_the_stored_resource(
    intent_service, site, resource, done_line
):
    result, _ = await _run(intent_service, _intent(), [_audit(site, "success", resource)], [], [])
    assert f"  - {done_line}" in result.message
    assert "##" not in result.message
    _assert_no_internal_labels(result.message)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "site, done_line, tried_line",
    [
        ("github.chat.close_issue", "Closed that issue", "close that issue"),
        ("github.chat.reopen_issue", "Reopened that issue", "reopen that issue"),
        ("github.chat.comment_issue", "Commented on that issue", "comment on that issue"),
        ("github.chat.update_issue", "Updated that issue", "update that issue"),
        ("github.domain.update_issue", "Updated that issue", "update that issue"),
        ("github.chat.create_issue", "Created an issue", "create an issue"),
        ("github.command.create_issue", "Created an issue", "create an issue"),
        ("github.domain.create_issue", "Created an issue", "create an issue"),
        (
            "github.standup.create_issue",
            "Created an issue from your standup",
            "create an issue from your standup",
        ),
    ],
)
@pytest.mark.parametrize("missing", [None, "", "  "])
async def test_a_row_with_no_resource_renders_a_whole_sentence(
    intent_service, site, done_line, tried_line, missing
):
    rows = [_audit(site, "success", missing, 1), _audit(site, "failed", missing, 2)]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert f"  - {done_line}\n" in result.message + "\n"
    assert f"I tried to {tried_line}, but it didn't go through." in result.message
    assert "{" not in result.message and "issue ." not in result.message
    _assert_no_internal_labels(result.message)


# ── The one predicate: other audit rows, nested rows and the placeholder ────────


@pytest.mark.asyncio
async def test_other_audit_rows_are_neither_listed_nor_counted(intent_service):
    """A successful login (or any non-consequential row) is not a change Piper made,
    even with a message on it; a window of only such rows is nothing new."""
    others = [
        _audit("login", "success", None, 1, event_type="auth", message="Login succeeded"),
        _audit("api_key_created", "success", None, 2, event_type="api_key", message="Key"),
        _audit("github.chat.close_issue", "success", "9", 3, event_type="data"),
        _audit("github_create_issue", "failed", None, 4, event_type="data", message="Create"),
    ]
    result, _ = await _run(intent_service, _intent(), others, [], [])
    assert result.message == NOTHING_NEW.format(window="since yesterday")
    assert result.intent_data["total_activities"] == 0

    rows = others + [_audit("github.chat.close_issue", "success", "38", 5)]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert _after_opener(result.message) == [
        "Piper made 1 change for you.",
        "  - Closed issue #38",
    ]
    assert "Login" not in result.message and "#9" not in result.message
    _assert_no_internal_labels(result.message)


@pytest.mark.asyncio
async def test_a_nested_row_is_the_same_action_and_is_left_out(intent_service):
    rows = [
        _audit("github.standup.create_issue", "success", "owner/repo", 1),
        _audit(
            "github.domain.create_issue",
            "success",
            "owner/repo",
            1,
            nested_in="github.standup.create_issue",
        ),
    ]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert _after_opener(result.message) == [
        "Piper made 1 change for you.",
        "  - Created an issue in owner/repo from your standup",
    ]


@pytest.mark.asyncio
async def test_the_placeholder_is_hidden_from_both_halves(intent_service):
    assert _VISIBLE == tuple(k for k in _SITE_KEYS if k != "slack.socket.placeholder")
    rows = [
        _audit("slack.socket.placeholder", "success", CHANNEL, 1),
        _audit("slack.socket.reply", "success", CHANNEL, 2),
        _audit("slack.socket.placeholder", "failed", CHANNEL, 3),
        _audit("slack.socket.placeholder", "unconfirmed", CHANNEL, 4),
    ]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert _after_opener(result.message) == [
        "Piper made 1 change for you.",
        "  - Replied in Slack",
    ]
    assert "holding" not in result.message
    only = [row for row in rows if row.action == "slack.socket.placeholder"]
    result, _ = await _run(intent_service, _intent(), only, [], [])
    assert result.message == NOTHING_NEW.format(window="since yesterday")


# ── Grouping on the rendered line, CXO's count form, the cap ───────────────────


@pytest.mark.asyncio
async def test_identical_rendered_lines_group_with_a_count_and_rows_still_count(
    intent_service,
):
    rows = [
        _audit("slack.response.individual", "success", CHANNEL, 1),
        _audit("github.chat.close_issue", "success", "38", 2),
        _audit("slack.response.consolidated", "success", CHANNEL, 3),
        _audit("slack.socket.reply", "success", CHANNEL, 4),
        _audit("github.chat.close_issue", "success", "40", 5),
        _audit("slack.socket.reply", "failed", CHANNEL, 6),
        _audit("slack.response.individual", "failed", CHANNEL, 7),
        _audit("github.chat.comment_issue", "unconfirmed", "38", 8),
        _audit("github.chat.comment_issue", "unconfirmed", "38", 9),
    ]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert _after_opener(result.message) == [
        "Piper made 5 changes for you.",
        "  - Replied in Slack, 3 times",
        "  - Closed issue #38",
        "  - Closed issue #40",
        "I tried to reply in Slack 2 times, but it didn't go through.",
        "I tried to comment on issue #38 2 times, but I couldn't confirm it went through. "
        "Check before you rely on it.",
    ]
    _assert_no_internal_labels(result.message)


@pytest.mark.asyncio
async def test_more_than_five_groups_lists_the_five_most_recent_and_counts_the_rest(
    intent_service,
):
    rows = [_audit("github.chat.close_issue", "success", str(n), n) for n in range(1, 8)]
    rows.append(_audit("github.chat.close_issue", "success", "1", 8))
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert _after_opener(result.message) == [
        "Piper made 8 changes for you.",
        "  - Closed issue #1, 2 times",
        "  - Closed issue #2",
        "  - Closed issue #3",
        "  - Closed issue #4",
        "  - Closed issue #5",
        "  - and 2 more",
    ]
    _assert_no_internal_labels(result.message)


@pytest.mark.asyncio
async def test_only_attempts_render_no_headline(intent_service):
    rows = [
        _audit("github.chat.create_issue", "failed", "owner/repo", 1),
        _audit("slack.standup.post", "unconfirmed", CHANNEL, 2),
    ]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert _after_opener(result.message) == [
        "I tried to create an issue in owner/repo, but it didn't go through.",
        "I tried to post your standup to Slack, but I couldn't confirm it went through. "
        "Check before you rely on it.",
    ]
    assert "Piper made" not in result.message
    _assert_no_internal_labels(result.message)


@pytest.mark.asyncio
async def test_failed_read_beside_actions_still_named(intent_service):
    """#2140's fail-closed line stays beside the rows the other reads found."""
    result, _ = await _run(
        intent_service,
        _intent(),
        [_audit("github.chat.comment_issue", "success", "38")],
        RuntimeError("todo"),
        [],
    )
    assert "  - Commented on issue #38" in result.message
    assert result.message.endswith(
        "I couldn't read your Piper tasks just now, so the list above doesn't include it. "
        "Try again in a moment; if it keeps failing, tell us."
    )
    _assert_no_internal_labels(result.message)
