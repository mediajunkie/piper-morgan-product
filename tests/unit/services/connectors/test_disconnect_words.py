"""CXO and Arch 2026-11-18 (the disconnect unit): one map of what a disconnect says, keyed by
connector and leg; the "stays valid" words on exactly the legs where something stays, and
an ``unknown`` GitHub leg that claims nothing one leg would make false.

Layer: the map, the routes' replies, and the card's leg from the resolver's answer.
"""

from __future__ import annotations

import json
import re
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from services.connectors.disconnect import DisconnectResult
from services.connectors.disconnect_words import (
    DISCONNECT_WORDS,
    MAY,
    PLAIN,
    all_closing_line,
    all_closing_table,
    all_incomplete_line,
    all_revoke_failed_line,
    closing_key,
    disconnect_words,
    page_all_words,
    revoke_failed_line,
)

#: Where Lead's facts (from disconnect.py) say something stays valid at the provider.
STAYS = {("github", "app"), ("github", "token"), ("notion", None)}


def _sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.])\s+", text.strip()) if s]


def test_the_stays_valid_words_are_on_exactly_the_legs_where_something_stays():
    for key, words in DISCONNECT_WORDS.items():
        if key == ("github", "unknown"):
            continue
        says_stays = "stays" in words.dialog or "stays" in words.cleared
        assert says_stays is (key in STAYS), key
        assert words.stays is (key in STAYS), key
        assert (words.all_note == PLAIN) is (key in STAYS), key


def test_the_revoking_legs_say_so_and_claim_nothing_stays():
    for key in [("slack", None), ("calendar", None), ("github", "oauth")]:
        words = DISCONNECT_WORDS[key]
        assert "revoke Piper's access there" in words.dialog
        assert words.cleared.endswith("disconnected.") and words.all_note is None


#: Sentences in the unknown entry that are true whichever leg is connected.
_TRUE_FOR_EVERY_LEG = {
    "I'll disconnect GitHub.",
    "You can connect it again anytime.",
    "GitHub disconnected.",
}


def test_the_unknown_github_entry_asserts_nothing_one_leg_would_make_false():
    words = DISCONNECT_WORDS[("github", "unknown")]
    closing_with = all_closing_line({"Notion": PLAIN, "GitHub": MAY})
    closing_alone = all_closing_line({"GitHub": MAY})
    texts = [words.dialog, words.cleared, closing_alone]
    # The All line with Notion: Notion's clause is plain (Notion always stays); GitHub's
    # part comes after "and" and must be conditional.
    notion_part, github_part = closing_with.split(", and ", 1)
    assert notion_part == "Notion also needs you to remove Piper in its settings"
    texts.append(github_part)
    for text in texts:
        for sentence in _sentences(text):
            if sentence in _TRUE_FOR_EVERY_LEG:
                continue
            conditional = sentence.startswith("If you connected it with") or " may " in (
                f" {sentence} "
            )
            assert conditional, sentence
            # ... and the condition names the legs it applies to.
            assert "app" in sentence and "token" in sentence, sentence
    assert words.stays is True and words.all_note == MAY


def test_github_with_no_leg_or_a_leg_the_map_lacks_is_unknown_never_a_guess():
    unknown = DISCONNECT_WORDS[("github", "unknown")]
    assert disconnect_words("github") is unknown
    assert disconnect_words("github", "pat") is unknown
    assert disconnect_words("github", "app") is DISCONNECT_WORDS[("github", "app")]


def test_the_revoke_line_names_a_place_a_person_can_find():
    assert "I couldn't revoke it at Google, so" in revoke_failed_line("Google Calendar")
    assert revoke_failed_line("Google Calendar").endswith(
        "until you remove Piper in your Google account's settings."
    )
    assert revoke_failed_line("Slack").endswith("until you remove Piper in Slack's settings.")
    assert all_revoke_failed_line("Google Calendar").endswith(
        "until you remove Piper in your Google account's settings."
    )


@pytest.mark.parametrize(
    "notes,line",
    [
        (
            {"GitHub": PLAIN, "Notion": PLAIN},
            "GitHub and Notion also need you to remove Piper in their own settings.",
        ),
        ({"Notion": PLAIN}, "Notion also needs you to remove Piper in its settings."),
        (
            {"Notion": PLAIN, "GitHub": MAY},
            "Notion also needs you to remove Piper in its settings, and GitHub may too if you "
            "connected it with the app or a token.",
        ),
        (
            {"GitHub": MAY},
            "GitHub may need you to remove Piper in its settings if you connected it with the "
            "app or a token.",
        ),
        ({}, None),
    ],
)
def test_the_closing_lines_are_cxos(notes, line):
    assert all_closing_line(notes) == line
    if line:
        assert all_closing_table()[closing_key(notes)] == line


def test_the_page_gets_every_closing_line_and_the_incomplete_line_from_the_map():
    words = page_all_words()
    assert words["closing"] == all_closing_table()
    assert words["incomplete"].replace("{service}", "Slack") == all_incomplete_line("Slack")
    # Only GitHub and Notion are ever named; Slack and Calendar never stay.
    assert all(
        set(re.findall(r"[A-Za-z]+(?=:)", key)) <= {"GitHub", "Notion"} for key in words["closing"]
    )


# --- the routes' replies -------------------------------------------------------------

ROUTES = {
    "slack": ("disconnect_slack", "Slack"),
    "calendar": ("disconnect_calendar", "Google Calendar"),
    "notion": ("disconnect_notion", "Notion"),
    "github": ("disconnect_github", "GitHub"),
}


async def _reply(card, clearing):
    from web.api.routes import settings_integrations as routes

    with patch("services.connectors.disconnect.disconnect_connector", new=clearing):
        reply = await getattr(routes, ROUTES[card][0])(current_user=SimpleNamespace(sub="u-1"))
    if hasattr(reply, "body"):
        return json.loads(reply.body)
    return reply


@pytest.mark.asyncio
@pytest.mark.parametrize("card", sorted(ROUTES))
async def test_each_reply_carries_the_line_disconnect_all_shows(card):
    async def revoke_failed(user, connector):
        return DisconnectResult(connector, (), True)

    async def incomplete(user, connector):
        return DisconnectResult(connector, ("a stored copy",), False)

    async def cleared(user, connector):
        return DisconnectResult(connector, (), False)

    service = ROUTES[card][1]
    assert (await _reply(card, revoke_failed))["all_line"] == all_revoke_failed_line(service)
    assert (await _reply(card, incomplete))["all_line"] == all_incomplete_line(service)
    assert (await _reply(card, cleared))["all_line"] is None


# --- the card's leg, from the resolver's own answer ----------------------------------


def test_the_card_leg_comes_from_the_resolvers_answer():
    from services.mcp.consumer.connector import DegradationReason, DegradationResponse
    from web.api.routes.integrations import _github_disconnect_leg

    def cred(**kw):
        return SimpleNamespace(
            **{"leg": None, "app_grant": False, "stale_oauth_reason": None, **kw}
        )

    assert _github_disconnect_leg(cred(leg="oauth", app_grant=True)) == "app"
    assert _github_disconnect_leg(cred(leg="oauth")) == "oauth"
    assert _github_disconnect_leg(cred(leg="pat")) == "token"
    # A token covering for a stale grant is two legs at once: unknown, never a guess.
    stale = DegradationReason.STALE_TOKEN
    assert _github_disconnect_leg(cred(leg="pat", stale_oauth_reason=stale)) == "unknown"
    degraded = DegradationResponse(reason=DegradationReason.UNREACHABLE, user_message="x")
    assert _github_disconnect_leg(degraded) == "unknown"


# --- a grant and a token at once (Arch 01M7T6ZN3C) -----------------------------------

META = {"display_name": "GitHub", "configure_url": "/settings/integrations/github"}


async def _leg_with(credential, held):
    from web.api.routes import integrations as routes

    async def resolve(*args, **kwargs):
        return credential

    async def token_held(user_id):
        if isinstance(held, Exception):
            raise held
        return held

    async def login(*args, **kwargs):
        return "octo-example"

    with (
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential",
            new=resolve,
        ),
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.account_login",
            new=login,
        ),
        patch.object(routes, "_github_token_held", new=token_held),
    ):
        _card, leg = await routes._github_card_and_leg(META, "u-1")
    return leg


def _grant(app_grant):
    return SimpleNamespace(leg="oauth", app_grant=app_grant, stale_oauth_reason=None, token="t")


@pytest.mark.asyncio
@pytest.mark.parametrize("app_grant", [True, False])
async def test_a_grant_plus_a_saved_token_is_the_unknown_leg(app_grant):
    assert await _leg_with(_grant(app_grant), held=True) == "unknown"


@pytest.mark.asyncio
@pytest.mark.parametrize("app_grant,leg", [(True, "app"), (False, "oauth")])
async def test_a_grant_with_no_token_keeps_its_leg(app_grant, leg):
    assert await _leg_with(_grant(app_grant), held=False) == leg


@pytest.mark.asyncio
async def test_a_failed_presence_read_is_the_unknown_leg():
    """The read itself answers True on any failure, so the leg is unknown."""
    from web.api.routes import integrations as routes

    with patch(
        "services.infrastructure.keychain_service.KeychainService.aread_secret",
        side_effect=RuntimeError("store down"),
    ):
        assert await routes._github_token_held("u-1") is True
