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
  counts it: tests/unit/web/api/routes/test_admin_consequential_1680.py). Its parts
  run in the SQL (Arch 2026-11-03 07:10), grouped and counted by (site, resource,
  status) with no row limit, so hidden rows can never push a visible action out of
  the window; the handler's rows are those groups.
- Every line is the registry's phrase for the row's site (``phrase`` after "I tried
  to", ``done`` for the success list) with the row's ``resource_id`` in its slot; the
  row's ``message`` is never printed or parsed.
- Successes first under "Piper made N changes for you." (N counts rows), then the
  attempts that did not go through (#2151: never listed as done, never counted), no
  status word, no cause, no parenthetical. Identical rendered lines group with a
  count, CXO's no-bracket form; a group of one prints no count.

Same no-LLM, no-database harness as #2140.
"""

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import text
from sqlalchemy.dialects import postgresql

from services.intent import intent_service as mod
from services.security import audit_logger as al
from services.security.audit_logger import EventType
from services.security.consequential_sites import (
    CONSEQUENTIAL_EVENT_TYPE,
    CONSEQUENTIAL_SITES,
    SLACK,
    outer_site,
    person_visible_action,
    person_visible_site_keys,
)
from tests.unit.services.intent_service.test_changes_query_fail_closed_2140 import (  # noqa: F401
    _USER,
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

# #2265: the window words are rendered from the bounds, so the pins compute them the
# same way, in the patched zone (a fixed non-UTC zone, so a UTC mix-up near midnight
# would print the wrong day and fail here).
_ZONE = "America/Los_Angeles"
_TZ_PATCH = "services.intent.intent_service.user_timezone_name"


def _since_yesterday_words():
    from zoneinfo import ZoneInfo

    start = datetime.now(ZoneInfo(_ZONE)) - timedelta(days=1)
    return f"since the start of yesterday, {start:%A}, {start:%B} {start.day}"


YD = _since_yesterday_words()


@pytest.fixture(autouse=True)
def _fixed_zone():
    with patch(_TZ_PATCH, new=AsyncMock(return_value=_ZONE)):
        yield


def _audit(site, status="success", resource_id=None, minutes_ago=5, n=1):
    """One grouped row as ``_visible_actions_statement`` returns it: the SQL already
    applied the predicate, so every row here is an action Piper took."""
    row = MagicMock()
    row.action = site
    row.status = status
    row.resource_id = resource_id
    row.n = n
    row.last_at = datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)
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
@pytest.mark.parametrize("site", _VISIBLE)
async def test_every_sites_row_renders_the_registry_phrase_and_no_label(
    intent_service, site, status
):
    """Every user-visible site (the SQL admits no other; the statement pin holds the
    key set), each outcome: the registry's line and nothing else."""
    entry = CONSEQUENTIAL_SITES[site]
    row = _audit(site, status, _resource_for(site))
    result, _ = await _run(intent_service, _intent(), [row], [], [])
    message = result.message
    _assert_no_internal_labels(message)
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


# ── The one predicate, in Python and in the SQL (Arch 2026-11-03 07:10) ────────


def test_the_predicate_admits_only_visible_consequential_unnested_rows():
    assert person_visible_action("consequential", "github.chat.close_issue", None)
    assert person_visible_action("consequential", "github.chat.close_issue", {})
    assert not person_visible_action("auth", "login", None)
    assert not person_visible_action("api_key", "api_key_created", None)
    assert not person_visible_action("data", "github.chat.close_issue", None)
    assert not person_visible_action("consequential", "github_create_issue", None)
    assert not person_visible_action("consequential", None, None)
    assert not person_visible_action(
        "consequential", "github.domain.create_issue", {"nested_in": "github.standup.create_issue"}
    )
    assert not person_visible_action("consequential", "slack.socket.placeholder", None)


def test_the_sql_key_set_is_the_predicates():
    """Derived from the registry, never a second list; equal to what the predicate
    admits for an unnested consequential row."""
    admitted = {k for k in CONSEQUENTIAL_SITES if person_visible_action("consequential", k, None)}
    assert person_visible_site_keys() == admitted
    assert _VISIBLE == tuple(k for k in _SITE_KEYS if k != "slack.socket.placeholder")
    assert set(_VISIBLE) == admitted and len(admitted) == 15


def test_the_statement_filters_groups_and_counts_in_sql_with_no_limit():
    owner = uuid.UUID(_USER)
    since = datetime.now(timezone.utc) - timedelta(days=1)
    stmt = mod._visible_actions_statement(owner, since)
    compiled = stmt.compile(
        dialect=postgresql.dialect(), compile_kwargs={"render_postcompile": True}
    )
    sql = " ".join(str(compiled).split())
    params = compiled.params
    assert "audit_logs.user_id = %(user_id_1)s" in sql and params["user_id_1"] == owner
    assert "audit_logs.created_at >= %(created_at_1)s" in sql and params["created_at_1"] == since
    assert "audit_logs.event_type = %(event_type_1)s" in sql
    assert params["event_type_1"] == CONSEQUENTIAL_EVENT_TYPE
    assert "audit_logs.action IN (" in sql
    assert {v for k, v in params.items() if k.startswith("action_1_")} == set(
        person_visible_site_keys()
    )
    assert "(audit_logs.details ->> %(details_1)s)" in sql and params["details_1"] == "nested_in"
    assert sql.count("IS NULL") == 1
    assert "GROUP BY audit_logs.action, audit_logs.resource_id, audit_logs.status" in sql
    assert "ORDER BY max(audit_logs.created_at) DESC" in sql
    assert "count(*) AS n" in sql and "max(audit_logs.created_at) AS last_at" in sql
    # the row's message is an internal label: never selected, so never printed
    assert "audit_logs.message" not in sql and "audit_logs.event_type," not in sql
    assert "LIMIT" not in sql.upper()


@pytest.mark.asyncio
async def test_the_handler_reads_through_the_statement_once(intent_service):
    with patch.object(
        mod, "_visible_actions_statement", wraps=mod._visible_actions_statement
    ) as seen:
        result, made = await _run(
            intent_service, _intent(), [_audit("github.chat.close_issue", "success", "38")], [], []
        )
    assert len(made) == 3
    seen.assert_called_once()
    owner, since = seen.call_args[0]
    assert str(owner) == _USER
    assert since < datetime.now(timezone.utc)
    assert "  - Closed issue #38" in result.message
    assert result.intent_data["total_activities"] == 1


# ── CXO 2026-11-03 07:3x (on Arch 07:27): the empty reply names no "activity log" and
# claims only what the census audits (Slack, GitHub), never "anything"; the count is exact ──


def test_the_nothing_new_line_is_cxos_three_sentences():
    assert mod.CHANGES_NOTHING_NEW == (
        "I don't see anything new in your Piper tasks or projects {window}. "
        "Piper hasn't posted to Slack or written to GitHub for you in that time. "
        "I haven't looked at anything done in GitHub outside Piper."
    )


@pytest.mark.asyncio
async def test_an_empty_window_names_no_activity_log_and_claims_only_the_audited(
    intent_service,
):
    result, _ = await _run(intent_service, _intent(), [], [], [])
    assert result.message == (
        f"I don't see anything new in your Piper tasks or projects {YD}. "
        "Piper hasn't posted to Slack or written to GitHub for you in that time. "
        "I haven't looked at anything done in GitHub outside Piper."
    )
    assert "activity log" not in result.message
    # Arch 07:27: "I haven't changed anything" spoke for Notion writes the audit
    # never sees (#2151's false empty in the wording).
    assert not ("anything" in result.message and "changed" in result.message)


def test_the_opener_and_failed_read_constants_are_cxos_words():
    assert mod.CHANGES_FOUND_OPENER == (
        "Here's what changed in your Piper {sources} {window}, and what Piper did for you. "
        "I haven't looked at anything done in GitHub outside Piper."
    )
    assert mod.CHANGES_FOUND_OPENER_ACTIONS_READ_FAILED == (
        "Here's what changed in your Piper {sources} {window}. I haven't looked at anything "
        "done in GitHub outside Piper."
    )
    assert mod.CHANGES_FOUND_OPENER_ACTIONS_ONLY == (
        "Here's what Piper did for you {window}. I haven't looked at anything done in GitHub "
        "outside Piper."
    )
    assert mod.CHANGES_ACTIONS_READ_FAILED_BESIDE_ROWS == (
        "I couldn't read what Piper did for you just now, so the list above doesn't include "
        "it. Try again in a moment; if it keeps failing, tell us."
    )
    assert mod.CHANGES_ACTIONS_SOURCE_SHOWN == "what Piper did for you"


@pytest.mark.asyncio
async def test_rows_with_every_read_ok_open_with_cxos_opener(intent_service):
    rows = [_audit("github.chat.close_issue", "success", "38")]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert result.message.startswith(
        f"Here's what changed in your Piper tasks and projects {YD}, and what "
        "Piper did for you. I haven't looked at anything done in GitHub outside Piper.\n"
    )
    assert "activity log" not in result.message and "checked GitHub" not in result.message


@pytest.mark.asyncio
async def test_only_the_actions_read_ok_opens_with_what_piper_did(intent_service):
    rows = [_audit("github.chat.close_issue", "success", "38")]
    boom = RuntimeError("down")
    result, _ = await _run(intent_service, _intent(), rows, boom, boom)
    assert _after_opener(result.message)[:2] == [
        "Piper made 1 change for you.",
        "  - Closed issue #38",
    ]
    assert result.message.startswith(
        f"Here's what Piper did for you {YD}. I haven't looked at anything done in "
        "GitHub outside Piper.\n"
    )
    assert result.message.endswith(
        "I couldn't read your Piper tasks just now, so the list above doesn't include it. "
        "Try again in a moment; if it keeps failing, tell us.\n"
        "I couldn't read your Piper projects just now, so the list above doesn't include it. "
        "Try again in a moment; if it keeps failing, tell us."
    )
    assert "activity log" not in result.message


# ── CXO 2026-11-03 08:2x: the seven failure-path strings, read and landed with one edit ──

_TRY = " Try again in a moment; if it keeps failing, tell us."
_BOOM = RuntimeError("read failed")
_SEVEN = {
    # (audit, tasks, projects) read specs → the whole reply
    ("ok", "fail", "ok"): (
        f"I don't see anything new in your Piper projects {YD}, and Piper hasn't "
        "posted to Slack or written to GitHub for you in that time. I couldn't read your Piper "
        "tasks just now, so I can't say what changed there." + _TRY
    ),
    ("ok", "ok", "fail"): (
        f"I don't see anything new in your Piper tasks {YD}, and Piper hasn't posted "
        "to Slack or written to GitHub for you in that time. I couldn't read your Piper projects "
        "just now, so I can't say what changed there." + _TRY
    ),
    ("fail", "ok", "ok"): (
        f"I don't see anything new in your Piper tasks or projects {YD}. I couldn't "
        f"read what Piper did for you just now, so I can't say what it did {YD}." + _TRY
    ),
    ("ok", "fail", "fail"): (
        f"Piper hasn't posted to Slack or written to GitHub for you {YD}. I couldn't "
        "read your Piper tasks or projects just now, so I can't say what changed there." + _TRY
    ),
    ("fail", "fail", "ok"): (
        f"I don't see anything new in your Piper projects {YD}. I couldn't read your "
        "Piper tasks or what Piper did for you just now, so I can't say what changed there." + _TRY
    ),
    ("fail", "ok", "fail"): (
        f"I don't see anything new in your Piper tasks {YD}. I couldn't read your "
        "Piper projects or what Piper did for you just now, so I can't say what changed there."
        + _TRY
    ),
    ("fail", "fail", "fail"): (
        "I couldn't read your Piper tasks or projects, or what Piper did for you, just now, so "
        f"I can't say what changed {YD}." + _TRY
    ),
}


@pytest.mark.asyncio
@pytest.mark.parametrize("spec", sorted(_SEVEN))
async def test_the_seven_failure_path_strings_are_cxos(intent_service, spec):
    reads = [_BOOM if r == "fail" else [] for r in spec]
    result, _ = await _run(intent_service, _intent(), *reads)
    assert result.message == _SEVEN[spec]
    assert result.success is (spec != ("fail", "fail", "fail"))
    assert "activity log" not in result.message


def test_the_slack_github_claim_is_one_stem_shared_with_the_nothing_new_line():
    assert mod.CHANGES_SLACK_GITHUB_CLAIM == (
        "Piper hasn't posted to Slack or written to GitHub for you"
    )
    assert f"{mod.CHANGES_SLACK_GITHUB_CLAIM} in that time." in mod.CHANGES_NOTHING_NEW


@pytest.mark.asyncio
@pytest.mark.parametrize("spec", sorted(_SEVEN) + [("ok", "ok", "ok")])
@pytest.mark.parametrize("with_rows", [False, True])
async def test_no_branch_names_an_activity_log(intent_service, spec, with_rows):
    rows = [_audit("github.chat.close_issue", "success", "38")] if with_rows else []
    reads = [_BOOM if r == "fail" else (rows if i == 0 else []) for i, r in enumerate(spec)]
    result, _ = await _run(intent_service, _intent(), *reads)
    assert "activity log" not in result.message
    assert "checked GitHub" not in result.message


@pytest.mark.asyncio
@pytest.mark.parametrize("rows", [49, 60, 250])
async def test_the_headline_count_is_exact_never_at_least(intent_service, rows):
    """CXO's "at least {N}" words are never needed: the read has no row limit and
    counts in SQL, so the headline is the exact number of rows."""
    groups = [_audit("github.chat.close_issue", "success", str(i), i, n=1) for i in range(rows)]
    result, _ = await _run(intent_service, _intent(), groups, [], [])
    assert f"Piper made {rows} changes for you." in result.message
    assert "at least" not in result.message
    assert f"  - and {rows - 5} more" in result.message
    assert result.intent_data["total_activities"] == rows


@pytest.mark.asyncio
async def test_grouped_rows_count_their_rows_in_total_activities(intent_service):
    rows = [
        _audit("github.chat.close_issue", "success", "38", 1, n=3),
        _audit("slack.socket.reply", "failed", CHANNEL, 2, n=2),
    ]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert result.intent_data["total_activities"] == 5
    assert _after_opener(result.message) == [
        "Piper made 3 changes for you.",
        "  - Closed issue #38, 3 times",
        "I tried to reply in Slack 2 times, but it didn't go through.",
    ]


# ── Grouping on the rendered line, CXO's count form, the cap ───────────────────


@pytest.mark.asyncio
async def test_identical_rendered_lines_group_with_a_count_and_rows_still_count(
    intent_service,
):
    """The SQL groups by (site, resource, status); the render merges groups whose
    rendered line is the same (three Slack reply sites), and the headline counts rows."""
    rows = [
        _audit("slack.response.individual", "success", CHANNEL, 1),
        _audit("github.chat.close_issue", "success", "38", 2),
        _audit("slack.response.consolidated", "success", CHANNEL, 3),
        _audit("slack.socket.reply", "success", CHANNEL, 4),
        _audit("github.chat.close_issue", "success", "40", 5),
        _audit("slack.socket.reply", "failed", CHANNEL, 6),
        _audit("slack.response.individual", "failed", CHANNEL, 7),
        _audit("github.chat.comment_issue", "unconfirmed", "38", 8, n=2),
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
    rows[0].n = 2
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


# ── Arch's 07:10 pin, against the scratch database: hidden rows never push a visible
# action out of the window, because the filter runs in the SQL, not after a limit. ──


@pytest.mark.consequential_audit_db
class TestHiddenRowsNeverHideAVisibleAction:
    async def test_sixty_placeholders_over_an_older_close_still_render_the_close(
        self, intent_service, create_test_user
    ):
        from services.database.session_factory import AsyncSessionFactory
        from tests.unit.web.api.routes.test_admin_consequential_1680 import _db_ready

        await _db_ready()
        user_id = str(uuid.uuid4())
        async with AsyncSessionFactory.session_scope_fresh() as s:
            await create_test_user(s, user_id)
        try:
            # the older visible action first, then sixty hidden rows and a nested pair
            log = await al.audit_logger.log_consequential_action(
                site="github.chat.close_issue",
                status="success",
                user_id=user_id,
                message="Close issue #2258",
                credits_spent=False,
                resource_type="github_issue",
                resource_id="2258",
            )
            assert log is not None
            for _ in range(60):
                assert (
                    await al.audit_logger.log_consequential_action(
                        site="slack.socket.placeholder",
                        status="success",
                        user_id=user_id,
                        message="Slack thinking placeholder",
                        credits_spent=False,
                        resource_type="slack_channel",
                        resource_id=CHANNEL,
                    )
                    is not None
                )
            with outer_site("github.standup.create_issue"):
                assert (
                    await al.audit_logger.log_consequential_action(
                        site="github.domain.create_issue",
                        status="success",
                        user_id=user_id,
                        message="Create issue in owner/repo (domain service)",
                        credits_spent=False,
                        resource_type="github_repository",
                        resource_id="owner/repo",
                    )
                    is not None
                )
                assert (
                    await al.audit_logger.log_consequential_action(
                        site="github.standup.create_issue",
                        status="failed",
                        user_id=user_id,
                        message="Standup item filed as an issue in owner/repo",
                        credits_spent=False,
                        resource_type="github_repository",
                        resource_id="owner/repo",
                    )
                    is not None
                )
            result = await intent_service._handle_changes_query(
                _intent(user_id=user_id), "wf", "session-not-a-user"
            )
        finally:
            async with AsyncSessionFactory.session_scope_fresh() as s:
                await s.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
                await s.commit()
        assert result.success is True
        assert _after_opener(result.message) == [
            "Piper made 1 change for you.",
            "  - Closed issue #2258",
            "I tried to create an issue in owner/repo from your standup, but it didn't go "
            "through.",
        ]
        assert "holding" not in result.message
        assert result.intent_data["total_activities"] == 2
        _assert_no_internal_labels(result.message)
