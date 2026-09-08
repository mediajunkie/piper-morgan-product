"""#1730 Gap 1 — the GENERIC unwired-write decline speaks in uncertainty, never
asserts absence, and echoes what it heard (CXO copy, 2026-09-08).

The defect: `GENERIC_UNWIRED_WRITE_DECLINE` fires for ANY unmapped emission —
including one where the CLASSIFIER misread a request for a capability that IS
wired — and the old copy said "that capability is still on the way". The system
knows "I have no mapping for this emission"; it published "that capability
doesn't exist yet". Two different claims, and the second is the one the user
acts on (PM hit a false denial for a shipped capability).

Scope (CXO, binding): ONLY the generic. The per-action `UNWIRED_WRITE_DECLINES`
map stays DEFINITE — for a mapped action we genuinely know it's unwired, so
asserting absence is honest there.

Fixture note: PM's #1527 probe phrasings ("delete the reminder…") ROUTE
correctly since the alias fix and never reach this decline — so the generic is
pinned here via a genuinely-unmapped emission (`archive_repository`, the same
by-construction-unwired fixture test_unwired_execution_derived_decline_1333
uses), not via phrasings that no longer hit the branch.

Echo safety (layer named): the chat frontend renders bot messages as markdown
with NO sanitizer (web/bot-message-renderer.js: marked.parse() → innerHTML),
and there is no server-side escaping on the reply path — so the echo is
markdown-escaped (backslash before every ASCII punctuation char: literal
render, no raw HTML, no re-parse — the #1729 family concern) and capped with
an honest ellipsis.
"""

from unittest.mock import patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.unwired_writes import (
    _ECHO_MAX_CHARS,
    GENERIC_UNWIRED_WRITE_DECLINE,
    UNWIRED_WRITE_DECLINES,
    generic_unwired_write_decline,
    get_unwired_write_decline,
)
from services.shared_types import IntentCategory

# The old false-absence claims — pinned ABSENT from the generic (and ONLY the
# generic: the per-action declines are licensed to assert absence).
_OLD_FALSE_CLAIM_FRAGMENTS = ["still on the way", "can't do that from chat yet"]


class TestGenericCopyIsUncertainNotAbsent:
    """The new copy's key fragments present; the old absence claims gone."""

    def test_new_copy_key_fragments_present(self):
        assert "I didn't recognize" in GENERIC_UNWIRED_WRITE_DECLINE
        assert "may have misread" in GENERIC_UNWIRED_WRITE_DECLINE
        # #1426 census-D3 preserved verbatim in intent: both surfaces, presuming neither.
        assert "Settings, Files, Lists" in GENERIC_UNWIRED_WRITE_DECLINE
        assert "GitHub" in GENERIC_UNWIRED_WRITE_DECLINE

    def test_old_false_claims_absent_from_generic(self):
        for fragment in _OLD_FALSE_CLAIM_FRAGMENTS:
            assert fragment not in GENERIC_UNWIRED_WRITE_DECLINE
            assert fragment not in generic_unwired_write_decline("archive my old repo")

    def test_no_apology_no_unfortunately(self):
        # CXO: the product isn't broken; it misheard.
        low = GENERIC_UNWIRED_WRITE_DECLINE.lower()
        assert "sorry" not in low
        assert "unfortunately" not in low

    def test_per_action_declines_stay_definite_and_untouched(self):
        """Exclusion pin: for mapped actions we genuinely KNOW unwiring, so their
        definite copy ("can't … yet") is honest and stays."""
        assert UNWIRED_WRITE_DECLINES  # the curated map still exists
        for action, copy in UNWIRED_WRITE_DECLINES.items():
            low = copy.lower()
            assert "can't" in low, f"{action}: curated copy must stay definite"
            assert "yet" in low, f"{action}: curated copy must stay definite"
        # A message passed alongside a curated action changes nothing (#1730 is
        # generic-only; no echo on the definite declines).
        assert (
            get_unwired_write_decline("create_milestone", original_message="add a milestone")
            == UNWIRED_WRITE_DECLINES["create_milestone"]
        )


class TestEchoRecoveryAffordance:
    """'What I heard was: …' — inserted after the first sentence, verbatim words."""

    def test_echo_renders_the_users_message(self):
        msg = generic_unwired_write_decline("archive my old repo")
        assert 'What I heard was: "archive my old repo."' in msg

    def test_echo_inserted_after_first_sentence(self):
        msg = generic_unwired_write_decline("archive my old repo")
        first = msg.index("I didn't recognize")
        echo = msg.index("What I heard was")
        recovery = msg.index("If I misread it")
        assert first < echo < recovery
        # The first sentence ends before the echo begins.
        assert "being unable to do it." in msg[:echo]

    def test_no_message_means_no_echo_sentence(self):
        assert "What I heard was" not in generic_unwired_write_decline(None)
        assert "What I heard was" not in generic_unwired_write_decline("")
        assert "What I heard was" not in generic_unwired_write_decline("   \n  ")
        assert generic_unwired_write_decline(None) == GENERIC_UNWIRED_WRITE_DECLINE

    def test_single_arg_call_shape_is_the_base_form(self):
        # The dispatcher's pre-#1571 call shape stays the echo-less base copy.
        assert get_unwired_write_decline("archive_repository") == GENERIC_UNWIRED_WRITE_DECLINE


class TestEchoCap:
    """A pasted-in paragraph must not swamp the reply; truncation is honest."""

    def test_long_message_is_capped_with_honest_ellipsis(self):
        long_message = "archive the repo because " + "reasons " * 70  # ~585 chars
        assert len(long_message) > 500
        msg = generic_unwired_write_decline(long_message)
        assert long_message not in msg  # never renders whole
        assert '…"' in msg  # ellipsis (inside the quote) marks the truncation
        # The echoed portion is the message's own prefix, capped.
        assert 'What I heard was: "archive the repo because reasons' in msg
        echo_start = msg.index('What I heard was: "') + len('What I heard was: "')
        echoed = msg[echo_start : msg.index('…"')]
        assert len(echoed) <= _ECHO_MAX_CHARS

    def test_short_message_renders_whole_with_terminal_period(self):
        msg = generic_unwired_write_decline("archive my old repo")
        assert 'What I heard was: "archive my old repo."' in msg
        assert "…" not in msg


class TestEchoEscaping:
    """USER CONTENT interpolated into a marked.parse()→innerHTML surface, two
    layers: & < > entity-escaped (no raw tag reaches innerHTML — holds even in
    the renderer's no-marked degraded fallback), remaining ASCII punctuation
    backslash-escaped (marked renders it literally — no re-parse of the user's
    words, the #1729 family concern)."""

    def test_html_is_neutralized(self):
        msg = generic_unwired_write_decline('do it <script>alert("x")</script> now')
        assert "<script>" not in msg  # raw HTML never survives
        assert "&lt;script&gt;" in msg  # entity-escaped: renders as literal text
        assert "&amp;" not in msg  # no double-escape of the entities themselves

    def test_ampersand_is_entity_escaped_once(self):
        msg = generic_unwired_write_decline("this & that")
        assert "this &amp; that" in msg

    def test_markdown_is_not_reparsed(self):
        msg = generic_unwired_write_decline("make it *bold* and `coded` [now](x)")
        assert "\\*bold\\*" in msg
        assert "\\`coded\\`" in msg
        assert "\\[now\\]\\(x\\)" in msg

    def test_autolink_defeated(self):
        # GFM autolinks bare URLs/www; escaped punctuation renders them as text.
        msg = generic_unwired_write_decline("archive https://example.com please")
        assert "https\\:\\/\\/example\\.com" in msg

    def test_user_backslashes_are_escaped_too(self):
        msg = generic_unwired_write_decline("literal \\* stays")
        assert "\\\\\\*" in msg  # user's \ then * → \\ then \*

    def test_newlines_collapse_so_echo_cannot_open_block_structure(self):
        msg = generic_unwired_write_decline("first line\n\n# heading\n- item")
        assert "\n" not in msg
        assert "first line \\# heading \\- item" in msg

    def test_plain_words_pass_through_verbatim(self):
        msg = generic_unwired_write_decline("archive my old repo")
        assert "\\" not in msg  # nothing to escape → no backslash noise


@pytest.mark.asyncio
class TestGenericPinnedViaUnmappedEmission:
    """The generic reaches the user through `_handle_execution_intent`'s
    else-branch for a genuinely-unmapped emission — pin the copy THERE."""

    @pytest.fixture
    def intent_service(self):
        with patch("services.intent.intent_service.LearningHandler"):
            with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
                return IntentService()

    async def test_unmapped_emission_gets_uncertain_copy_with_echo(self, intent_service):
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="archive_repository",  # by construction unwired (no handler, no mapping)
            original_message="please archive my old repo",
        )

        result = await intent_service._handle_execution_intent(
            intent, workflow=None, session_id="s-1730", user_id="u-1730"
        )

        assert result.success is True
        assert result.intent_data.get("unwired_action") is True
        assert "I didn't recognize" in result.message
        assert "may have misread" in result.message
        assert 'What I heard was: "please archive my old repo."' in result.message
        for fragment in _OLD_FALSE_CLAIM_FRAGMENTS:
            assert fragment not in result.message
