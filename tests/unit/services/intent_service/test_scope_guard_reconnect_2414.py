"""Issue 2414: the scope guard keeps a sentence the turn's own context makes true.

Arch 2026-11-22 (mail 01M82F5PKR), after a local replay of two served status turns
showed the guard dropping a sentence in 9 of 12 replies, and the dropped sentences
were true: the context told the floor GitHub needs reconnecting, the reply said so,
and the guard read "GitHub … unavailable" as a failure claim about an unarmed source.
What was left pointed at the missing sentence ("You can fix that in Settings…").

The rule: when the floor's context says GitHub needs reconnecting, the guard's
``GitHub`` check_name counts as licensed. It only takes drops away. The prompt does
not change, no scan starts because of it, and the fallback never names it.

Layer: the guard as a function, and the floor's ``respond`` seam with a stub model.
The three kept sentences are quoted from the replay's recorded replies.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.intent_service.conversational_floor import ConversationalFloor, FloorContext
from services.intent_service.scope_guard import apply_scope_guard, build_fallback_sentence

#: What a status turn arms when GitHub's reads fail (the replay's armed set).
ARMED = ("open issues", "blocked items", "recent repository activity")

REPLAY_SENTENCES = [
    "Harbor Survey is one of the projects I'm tracking for you, but I wasn't able to pull "
    "up open issues or recent activity this turn — GitHub needs reconnecting before I can "
    "get into that detail (Settings → Integrations → GitHub).",
    "Worth noting: GitHub also needs reconnecting (Settings → Integrations → GitHub), so "
    "any issues or PRs tied to that project are unavailable until that's sorted.",
    "Also worth flagging: GitHub needs reconnecting, so issue and PR data is unavailable "
    "until you do that (Settings → Integrations → GitHub).",
]
SECOND_PARAGRAPH = "Once that's back, I can give you a real picture of where things stand."


@pytest.mark.parametrize("sentence", REPLAY_SENTENCES)
def test_the_replays_sentences_are_dropped_today_without_the_context_fact(sentence):
    """The premise, pinned: with only the failed reads armed, each one is dropped."""
    _, dropped = apply_scope_guard(f"{sentence}\n\n{SECOND_PARAGRAPH}", ARMED)
    assert dropped == 1


@pytest.mark.parametrize("sentence", REPLAY_SENTENCES)
def test_they_are_kept_when_the_context_says_github_needs_reconnecting(sentence):
    reply = f"{sentence}\n\n{SECOND_PARAGRAPH}"
    filtered, dropped = apply_scope_guard(reply, ARMED, context_true_check_names=("GitHub",))
    assert dropped == 0
    assert filtered == reply


def test_the_context_fact_alone_starts_no_scan():
    """Nothing armed means no scan, as before: the new argument only removes drops."""
    reply = "I don't have your todos or your calendar in front of me this turn."
    filtered, dropped = apply_scope_guard(reply, (), context_true_check_names=("GitHub",))
    assert (filtered, dropped) == (reply, 0)


def test_a_claim_about_another_unarmed_source_is_still_dropped():
    reply = (
        "GitHub needs reconnecting, so issue data is unavailable. "
        "I also couldn't check your calendar this turn."
    )
    filtered, dropped = apply_scope_guard(reply, ARMED, context_true_check_names=("GitHub",))
    assert dropped == 1
    assert "calendar" not in filtered and "GitHub needs reconnecting" in filtered


def test_the_fallback_never_names_the_context_fact():
    """A reply emptied by real drops falls back to the armed names only."""
    reply = "I couldn't check your calendar this turn."
    filtered, dropped = apply_scope_guard(reply, ARMED, context_true_check_names=("GitHub",))
    assert dropped == 1
    assert filtered == build_fallback_sentence(ARMED)
    assert "GitHub" not in filtered


def _floor_returning(text):
    llm = MagicMock()
    llm.complete = AsyncMock(return_value=text)
    return ConversationalFloor(llm_client=llm, system_prompt_base="You are Piper Morgan (test).")


def _status_context(**github):
    return {
        "projects": [{"name": "Harbor Survey", "status": "active"}],
        "open_issues_source_failed": True,
        "blocked_items_source_failed": True,
        "github_activity_source_failed": True,
        **github,
    }


@pytest.mark.asyncio
class TestAtTheRespondSeam:
    REPLY = f"{REPLAY_SENTENCES[0]}\n\n{SECOND_PARAGRAPH}"

    async def _respond(self, **github):
        floor = _floor_returning(self.REPLY)
        return await floor.respond(
            FloorContext(
                user_message="how is the Harbor Survey project going?",
                session_id="s2414",
                intent_category="STATUS",
                intent_action="get_project_status",
                domain_context=_status_context(**github),
            )
        )

    async def test_reconnect_true_keeps_the_opening_sentence(self):
        resp = await self._respond(github_connected=True, github_needs_reconnecting=True)
        assert resp.scope_guard_dropped == 0
        assert resp.message.startswith("Harbor Survey is one of the projects")

    async def test_reconnect_false_still_drops_a_github_unavailable_claim(self):
        """Arch's second test: connected and healthy, so the claim has no licence."""
        resp = await self._respond(github_connected=True, github_needs_reconnecting=False)
        assert resp.scope_guard_dropped == 1
        assert "GitHub needs reconnecting" not in resp.message

    async def test_not_connected_keeps_the_sentence_too(self):
        """Arch 01M82G948F: the prompt says "GitHub: not connected (issue/PR data
        unavailable until connected)", so a reply repeating that is true as well. This is
        what a new tester's account reaches."""
        resp = await self._respond(github_connected=False)
        assert resp.scope_guard_dropped == 0
        assert resp.message.startswith("Harbor Survey is one of the projects")

    async def test_no_github_key_in_the_context_licenses_nothing(self):
        """The fact is read from the keys the prompt renders its GitHub line from. With
        no such key the prompt said nothing about GitHub, so the claim has no licence."""
        resp = await self._respond()
        assert resp.scope_guard_dropped == 1


# -- the shape for a right drop: (a), a leading connective is removed ---------------

FALSE_OPENING = "I couldn't check your calendar this turn."


@pytest.mark.parametrize(
    "second, expected_start",
    [
        ("Also, your GitHub issues didn't load.", "Your GitHub issues didn't load."),
        ("And your open issues didn't load.", "Your open issues didn't load."),
        ("But your open issues didn't load.", "Your open issues didn't load."),
        ("So your open issues didn't load.", "Your open issues didn't load."),
        ("Plus, your open issues didn't load.", "Your open issues didn't load."),
        ("That said, your open issues didn't load.", "Your open issues didn't load."),
    ],
)
def test_a_right_drop_of_the_opening_leaves_a_reply_that_opens_on_a_full_sentence(
    second, expected_start
):
    """PPM's acceptance (01M82FWZ30): a false claim about an unarmed source opens the
    reply, an "Also, …" sentence follows, and the reply then opens "Your …"."""
    reply = f"{FALSE_OPENING} {second} Here is what I do have for the project."
    filtered, dropped = apply_scope_guard(reply, ARMED)
    assert dropped == 1
    assert filtered.startswith(expected_start)
    assert filtered.endswith("Here is what I do have for the project.")


def test_a_connective_is_left_alone_when_the_opening_was_not_dropped():
    reply = "So here is where things stand. I couldn't check your calendar this turn."
    filtered, dropped = apply_scope_guard(reply, ARMED)
    assert dropped == 1
    assert filtered == "So here is where things stand."


def test_words_that_only_begin_like_a_connective_are_left_alone():
    reply = f"{FALSE_OPENING} Sometimes the open issues load slowly, and Android is one of them."
    filtered, _ = apply_scope_guard(reply, ARMED)
    assert filtered.startswith("Sometimes the open issues")


def test_the_connective_list_is_closed():
    from services.intent_service.scope_guard import LEADING_CONNECTIVES

    assert LEADING_CONNECTIVES == ("Also", "And", "But", "So", "Plus", "That said")
