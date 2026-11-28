"""Issue 2470: `add pipermorgan/piper-test-2` gets a specific decline, never the
generic "I didn't recognize that".

Served on beta 2026-11-27 (Web): the model offered "I can link them up", and taking the
offer was named ``add_github_repo``, an action no handler takes, so the person read the
generic decline with "I may have misread the ask" although the ask was recognised.

LAYER: unit, the decline function the unwired-execution branch calls. DENOMINATOR: this
one action. Not covered: that the classifier names ``add_github_repo`` for a given
sentence (a model's choice), the model's own offer sentence (issue 2463's prompt pass),
and anything served.
"""

from services.intent_service.unwired_writes import (
    UNWIRED_WRITE_DECLINES,
    generic_unwired_write_decline,
    get_unwired_write_decline,
)

# CXO, 2026-11-27 (issue 2470); this pin makes a change of words a diff.
WORDS = (
    "I can't add a repository from chat. Add it at GitHub (the Piper GitHub app's "
    "installed repositories), then press Refresh List in Settings → Integrations → GitHub."
)
ASK = "add pipermorgan/piper-test-2"


def test_the_words():
    assert UNWIRED_WRITE_DECLINES["add_github_repo"] == WORDS


def test_the_served_ask_gets_the_specific_decline():
    reply = get_unwired_write_decline("add_github_repo", original_message=ASK)
    assert reply == WORDS


def test_it_is_not_the_generic_decline_and_claims_no_misreading():
    reply = get_unwired_write_decline("add_github_repo", original_message=ASK)
    assert reply != generic_unwired_write_decline(ASK)
    assert "I didn't recognize" not in reply
    assert "misread" not in reply


def test_it_promises_nothing_and_names_where_it_is_done():
    reply = get_unwired_write_decline("add_github_repo", original_message=ASK)
    for promise in ("I'll", "I can link", "on the way", "yet"):
        assert promise not in reply
    # Arch's condition (2026-11-27): the line names the places it points to.
    assert "Add it at GitHub" in reply
    assert "Settings → Integrations → GitHub" in reply


def test_a_repo_pair_in_the_ask_adds_no_create_issue_hint():
    """The files-family hint (#1571) appends on an owner/repo pair only for a
    files-family action; this action is not one."""
    reply = get_unwired_write_decline("add_github_repo", original_message=ASK)
    assert "issue filed" not in reply
