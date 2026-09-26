"""#1772 residual — the post-compose SCOPE GUARD.

CXO ruled build (not accept the 10% residual), Arch ruled the mechanism
sound with one binding condition (an adversarial over-trigger pass). This
file carries both halves as separate, both-required corpora:

- ``TestOverTriggerCorpus``: >= 12 hand-written LEGITIMATE sentences that
  name an unarmed source without claiming a failed/unchecked read (a
  successful read, a reference, or an offer). None of these may be dropped
  — that is Arch's condition, and it is a floor, not a suggestion.
- ``TestUnderTriggerCorpus``: every leaking reply, VERBATIM, from the three
  #1772 measurement documents (``dev/2026/09/15/1772-scope-leak-measurement.md``,
  ``dev/2026/09/24/1772-candidate-measurement-2026-09-24.md``,
  ``dev/2026/09/25/1772-landed-string-measurement-2026-09-25.md``) — 8
  distinct replies. Each must have its offending sentence dropped.

Layer honesty (m-43): all tests in this file are PURE-FUNCTION or
STUBBED-LLM tests against ``apply_scope_guard`` / ``ConversationalFloor.respond()``
with a fixed model string. They measure the deterministic post-compose
filter, not a live model — the live leak rate under the guard is a separate
measurement (the Lead is scheduling it), not something this file claims.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from structlog.testing import capture_logs

from services.intent_service.conversational_floor import ConversationalFloor, FloorContext
from services.intent_service.scope_guard import apply_scope_guard, build_fallback_sentence

# ---------------------------------------------------------------------------
# (a) The over-trigger corpus — Arch's binding condition.
#
# Each sentence names an UNARMED source (reminders is the only armed check
# in these tests) via a successful read, a reference, or an offer — never a
# claim that the source failed/was unchecked. None may be dropped.
# ---------------------------------------------------------------------------

LEGITIMATE_UNARMED_MENTIONS = [
    "Your calendar shows a 3pm meeting with the design team.",  # successful read
    "You asked about your todos earlier — here's what I found.",  # reference
    "I can check your calendar if you like.",  # offer
    "Want me to check your calendar this afternoon?",  # offer, question form
    "Your project board looks busy this week.",  # successful read
    "I see three open issues on GitHub tagged for this sprint.",  # successful read
    "Let me know if you want me to open a repo for that.",  # offer
    "The project updates from last week are still relevant.",  # reference
    "You mentioned your todo list needs pruning.",  # reference
    "I noticed your GitHub repository has a new pull request.",  # successful read
    "If you want, I can pull up your meetings for today.",  # offer
    "Your todos are looking manageable today.",  # successful read
    "Should I check your project updates before we continue?",  # offer, question form
]

assert len(LEGITIMATE_UNARMED_MENTIONS) >= 12


class TestOverTriggerCorpus:
    """Arch's condition: a sentence merely naming/quoting/offering an
    unarmed source must survive untouched."""

    @pytest.mark.parametrize("sentence", LEGITIMATE_UNARMED_MENTIONS)
    def test_legitimate_mention_is_never_dropped(self, sentence):
        filtered, dropped = apply_scope_guard(sentence, ("reminders",))
        assert dropped == 0, f"false positive on legitimate sentence: {sentence!r}"
        assert filtered == sentence

    def test_legitimate_mentions_survive_together_in_one_reply(self):
        reply = " ".join(LEGITIMATE_UNARMED_MENTIONS)
        filtered, dropped = apply_scope_guard(reply, ("reminders",))
        assert dropped == 0
        assert filtered == reply


# ---------------------------------------------------------------------------
# (b) The under-trigger corpus — every leaking reply, verbatim, from the
# three measurement documents. 8 distinct replies.
# ---------------------------------------------------------------------------

# 09-15 measurement doc, anthropic N=1, idx 1/2/3/7/8 (5 leaks).
LEAK_09_15_IDX1 = (
    "Morning! I wasn't able to pull up your reminders just now, so I can't "
    "give you a full picture on that front — worth trying again in a moment.\n\n"
    "For the rest of your status, I don't have your todos, calendar, or "
    "project updates in front of me this turn. Want me to check any of those "
    'specifically? Something like "show my todos" or "what\'s on my calendar '
    'this week" should get you a clean snapshot of whichever you need most.'
)

LEAK_09_15_IDX2 = (
    "Morning! I wasn't able to pull up your reminders just now, so I can't "
    "give you a full picture on that front — worth a quick retry if you're "
    "expecting anything time-sensitive today.\n\n"
    "For the rest of your status — I don't have your todos, calendar, or "
    "project updates loaded in front of me this turn. Want me to check any "
    'of those specifically? A quick "show my todos" or "what\'s on my '
    'calendar this week" should get you what you need.'
)

LEAK_09_15_IDX3 = (
    "Good morning! I wasn't able to pull up your reminders just now, so I "
    "can't give you a full picture on that front — worth a retry if you're "
    "expecting anything time-sensitive.\n\n"
    "For the rest of your status — I don't have your todos, calendar, or "
    "project updates in front of me this turn. Want me to pull a standup "
    'view or check what\'s on your plate? Something like "show my standup" '
    'or "what are my open todos" would get me the specifics.\n\n'
    "What's the most pressing thing on your mind this morning?"
)

LEAK_09_15_IDX7 = (
    "Good morning! I wasn't able to pull up your reminders just now, so I "
    "can't give you a full picture on that front — worth restating that ask "
    "if anything time-sensitive is on your mind.\n\n"
    "For the rest of your status — I don't have your todos, calendar, or "
    "project updates in front of me this turn. Want me to pull any of those "
    'specifically? Something like "show my todos" or "what\'s on my calendar '
    'this week" would get you a real answer fast.\n\n'
    "What's the most pressing thing on your plate this morning?"
)

LEAK_09_15_IDX8 = (
    "Good morning! I wasn't able to pull up your reminders just now, so I "
    "can't give you a full picture on that front — worth a retry if you're "
    "expecting anything time-sensitive there.\n\n"
    "For the rest of your status — I don't have your todos, calendar, or "
    "project board in front of me this turn. Want me to check any of those "
    'specifically? Something like "show my todos" or "what\'s on my calendar '
    'this week" would get you a concrete answer right away.'
)

# 09-24 candidate-measurement doc, anthropic verbatim-directive re-baseline,
# idx 5/6 (2 leaks).
LEAK_09_24_IDX5 = (
    "Good morning! I wasn't able to pull up your reminders just now — worth "
    "trying again if you're expecting anything time-sensitive there.\n\n"
    "For the rest of your status, I don't have your projects or todos in "
    "front of me this turn. Want me to pull up your open issues, todo list, "
    "or anything specific — sprint board, recent PRs, what shipped this "
    "week? Just tell me where to look first."
)

LEAK_09_24_IDX6 = (
    "Morning! I wasn't able to pull your reminders just now, so I can't give "
    "you a full picture on that front — worth restating that ask if "
    "anything time-sensitive is on your mind.\n\n"
    "For the rest of your status — I don't have your todos, projects, or "
    "calendar in front of me this turn. Want me to pull up your open "
    "issues, check what's due today, or run a standup summary? Just say the "
    "word and I'll grab whichever slice is most useful to start your day."
)

# 09-25 landed-string-measurement doc, anthropic, idx 6 (1 leak).
LEAK_09_25_IDX6 = (
    "Good morning! I wasn't able to pull up your reminders just now, so "
    "that piece of your status is missing from this picture.\n\n"
    "For the rest — I don't have your todos, project board, or calendar in "
    "front of me this turn either. Want me to run a proper status check? If "
    "you tell me where to start (open issues, this week's priorities, "
    "sprint board), I can dig in right away."
)

# The exact offending clause per reply — the sentence the guard must drop.
# Kept separate from the full reply so the test can assert its ABSENCE
# precisely, rather than a blanket word-absence that would also catch the
# legitimate trailing offer sentence's quoted examples ("show my todos").
LEAK_CORPUS = [
    (
        "09-15-idx1",
        LEAK_09_15_IDX1,
        "For the rest of your status, I don't have your todos, calendar, or "
        "project updates in front of me this turn.",
    ),
    (
        "09-15-idx2",
        LEAK_09_15_IDX2,
        "For the rest of your status — I don't have your todos, calendar, or "
        "project updates loaded in front of me this turn.",
    ),
    (
        "09-15-idx3",
        LEAK_09_15_IDX3,
        "For the rest of your status — I don't have your todos, calendar, or "
        "project updates in front of me this turn.",
    ),
    (
        "09-15-idx7",
        LEAK_09_15_IDX7,
        "For the rest of your status — I don't have your todos, calendar, or "
        "project updates in front of me this turn.",
    ),
    (
        "09-15-idx8",
        LEAK_09_15_IDX8,
        "For the rest of your status — I don't have your todos, calendar, or "
        "project board in front of me this turn.",
    ),
    (
        "09-24-idx5",
        LEAK_09_24_IDX5,
        "For the rest of your status, I don't have your projects or todos in "
        "front of me this turn.",
    ),
    (
        "09-24-idx6",
        LEAK_09_24_IDX6,
        "For the rest of your status — I don't have your todos, projects, or "
        "calendar in front of me this turn.",
    ),
    (
        "09-25-idx6",
        LEAK_09_25_IDX6,
        "For the rest — I don't have your todos, project board, or calendar "
        "in front of me this turn either.",
    ),
]

assert len(LEAK_CORPUS) == 8


class TestUnderTriggerCorpus:
    """Every leaking reply verbatim from the three measurement docs must
    have its offending sentence dropped, while the true armed-source claim
    (about reminders) and the trailing offer survive."""

    @pytest.mark.parametrize("name,reply,offending", LEAK_CORPUS, ids=[c[0] for c in LEAK_CORPUS])
    def test_leak_sentence_dropped_armed_claim_kept(self, name, reply, offending):
        filtered, dropped = apply_scope_guard(reply, ("reminders",))
        assert dropped >= 1, f"{name}: guard did not fire on a known leak"
        assert offending not in filtered, f"{name}: offending clause survived"
        # The true claim about the ARMED source survives — "reminders" only
        # ever appears in the retained leading sentence in this corpus (the
        # offending clause names only unarmed sources).
        assert "reminders" in filtered

    @pytest.mark.parametrize("name,reply,offending", LEAK_CORPUS, ids=[c[0] for c in LEAK_CORPUS])
    def test_leak_logs_dropped_sentence_count_never_reply_text(self, name, reply, offending):
        with capture_logs() as events:
            apply_scope_guard(reply, ("reminders",), session_id="s1772")

        hits = [e for e in events if e.get("event") == "floor_scope_guard_dropped"]
        assert len(hits) == 1
        assert hits[0]["dropped_sentences"] >= 1
        assert hits[0]["session_id"] == "s1772"
        # The unarmed sources named are logged; the reply text itself is not
        # a field on the event.
        assert "unarmed_sources" in hits[0]
        for key, value in hits[0].items():
            if isinstance(value, str):
                assert "in front of me" not in value


# ---------------------------------------------------------------------------
# (c) Fallback when dropping empties the reply (or leaves a fragment).
# ---------------------------------------------------------------------------


class TestFallback:
    def test_fully_dropped_reply_falls_back_to_armed_honest_sentence(self):
        reply = "I don't have your todos, calendar, or project updates in front of me this turn."
        filtered, dropped = apply_scope_guard(reply, ("reminders",))
        assert dropped == 1
        assert filtered == build_fallback_sentence(("reminders",))
        assert filtered == "I couldn't check reminders this turn."

    def test_fragment_after_drop_falls_back(self):
        # Two sentences: the second is a bare fragment once the first (the
        # only substantive content) is dropped for claiming an unarmed
        # source.
        reply = "I don't have your calendar in front of me this turn. Okay."
        filtered, dropped = apply_scope_guard(reply, ("reminders",))
        assert dropped == 1
        assert filtered == "I couldn't check reminders this turn."

    def test_fallback_names_every_armed_check_in_registry_order(self):
        fallback = build_fallback_sentence(("reminders", "projects"))
        assert fallback == "I couldn't check reminders, projects this turn."


# ---------------------------------------------------------------------------
# (d) No armed flag => no scan at all.
# ---------------------------------------------------------------------------


class TestNoArmedFlagNoScan:
    def test_empty_armed_set_returns_input_unchanged_and_does_not_log(self):
        reply = "I don't have your todos, calendar, or project updates in front of me this turn."
        with capture_logs() as events:
            filtered, dropped = apply_scope_guard(reply, ())
        assert filtered == reply
        assert dropped == 0
        assert not [e for e in events if e.get("event") == "floor_scope_guard_dropped"]

    def test_empty_text_is_a_noop(self):
        filtered, dropped = apply_scope_guard("", ("reminders",))
        assert filtered == ""
        assert dropped == 0


# ---------------------------------------------------------------------------
# (e) The N>=2 case: a sentence naming BOTH an armed and an unarmed source.
#
# Decision (documented in scope_guard.py's module docstring and pinned
# here): KEEP the sentence. It contains a TRUE claim about the armed
# source, and dropping the whole sentence would lose that true claim in
# order to filter the false half. This is a deliberate asymmetry from the
# single-unarmed-source case, not an oversight.
# ---------------------------------------------------------------------------


class TestArmedPlusUnarmedSentence:
    def test_sentence_naming_armed_and_unarmed_source_is_kept(self):
        sentence = "I couldn't check your reminders or your calendar this turn."
        filtered, dropped = apply_scope_guard(sentence, ("reminders",))
        assert dropped == 0
        assert filtered == sentence

    def test_two_armed_sources_named_together_is_never_flagged(self):
        # The 2-flag control shape from the #1772 measurement docs: both
        # named sources are armed, so nothing here is a leak at all.
        sentence = "I ran into a snag pulling up your reminders and projects just now."
        filtered, dropped = apply_scope_guard(sentence, ("reminders", "projects"))
        assert dropped == 0
        assert filtered == sentence


# ---------------------------------------------------------------------------
# (f) Metadata flag on FloorResponse, at the respond() seam.
# ---------------------------------------------------------------------------


def _floor_returning(text):
    llm = MagicMock()
    llm.complete = AsyncMock(return_value=text)
    return ConversationalFloor(
        llm_client=llm,
        system_prompt_base="You are Piper Morgan (test base).",
    )


class TestRespondSeamMetadata:
    @pytest.mark.asyncio
    async def test_scope_guard_dropped_flag_set_when_armed_and_leaking(self):
        floor = _floor_returning(LEAK_09_15_IDX1)
        resp = await floor.respond(
            FloorContext(
                user_message="good morning, what's my status?",
                session_id="s1772",
                domain_context={"source_failed": True},
            )
        )
        assert resp.scope_guard_dropped >= 1
        assert (
            "For the rest of your status, I don't have your todos, calendar, or "
            "project updates in front of me this turn."
        ) not in resp.message
        assert "wasn't able to pull up your reminders" in resp.message

    @pytest.mark.asyncio
    async def test_scope_guard_dropped_flag_zero_when_nothing_armed(self):
        clean_reply = "Good morning! Anything specific you'd like to focus on today?"
        floor = _floor_returning(clean_reply)
        resp = await floor.respond(
            FloorContext(
                user_message="good morning",
                session_id="s1772",
                domain_context={},
            )
        )
        assert resp.scope_guard_dropped == 0
        assert resp.message == clean_reply

    @pytest.mark.asyncio
    async def test_scope_guard_dropped_flag_zero_when_armed_but_reply_clean(self):
        clean_reply = "I wasn't able to pull up your reminders just now — want me to try again?"
        floor = _floor_returning(clean_reply)
        resp = await floor.respond(
            FloorContext(
                user_message="good morning, what's my status?",
                session_id="s1772",
                domain_context={"source_failed": True},
            )
        )
        assert resp.scope_guard_dropped == 0
        assert resp.message == clean_reply
