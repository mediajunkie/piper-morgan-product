"""#2245: the capability answer suggests no connect prompt for a connector this
beta refuses. The example asks come from the #1428 ledger, filtered by the
same single source the Integrations page, the wizard and the connect routes
read under #2237 (``BETA_OFFERED_CONNECTORS``). Nothing is added in a dropped
line's place, and the ledger itself (the #1433 ratchet's denominator) is
untouched.
"""

from __future__ import annotations

import pytest

from services.integrations import integration_status_service
from services.intent_service import capability_legibility as legibility
from services.intent_service import chat_pointers
from services.intent_service.chat_pointers import (
    CORE_CAPABILITIES,
    POINTER,
    answer_utterances,
    capability_answer_lines,
    connector_of_pointer_key,
    pointer_utterances,
)

SLACK = 'you can ask me: "connect my slack"'
NOTION = 'you can ask me: "connect my notion"'
GITHUB = 'you can ask me: "connect my github"'


def _renderers():
    return (capability_answer_lines(), legibility.capability_answer_lines_with_outwardness())


class TestUnofferedConnectorsAreNotSuggested:
    def test_served_shape_offers_github_and_calendar_only(self):
        """The real ledger against the real offered set: PA's served 10-31 lines are gone."""
        assert set(integration_status_service.BETA_OFFERED_CONNECTORS) == {"github", "calendar"}
        for lines in _renderers():
            assert not any(line.startswith(SLACK) for line in lines)
            assert not any(line.startswith(NOTION) for line in lines)
            assert any(line.startswith(GITHUB) for line in lines)
            assert any("calendar" in line for line in lines)

    def test_the_offered_set_is_the_single_source(self, monkeypatch):
        """Change only BETA_OFFERED_CONNECTORS and the answer follows it, both ways."""
        monkeypatch.setattr(
            integration_status_service,
            "BETA_OFFERED_CONNECTORS",
            {"github": "GitHub", "calendar": "Google Calendar", "slack": "Slack"},
        )
        for lines in _renderers():
            assert any(line.startswith(SLACK) for line in lines)
            assert not any(line.startswith(NOTION) for line in lines)
        monkeypatch.setattr(
            integration_status_service, "BETA_OFFERED_CONNECTORS", {"calendar": "Google Calendar"}
        )
        for lines in _renderers():
            assert not any(line.startswith(SLACK) for line in lines)
        # "connect my github" is also taught by the Integrations PAGE row
        # (page:/settings/integrations), which names no connector, so with the
        # real ledger it survives; without that row it follows the set too.
        ledger = {
            k: v
            for k, v in chat_pointers.CHAT_POINTERS.items()
            if k != "page:/settings/integrations"
        }
        assert "connect my github" not in answer_utterances(ledger)
        assert "connect my github" in answer_utterances()

    def test_nothing_is_added_in_a_dropped_lines_place(self):
        """The answer is CORE_CAPABILITIES plus exactly the offered asks, in ledger order."""
        dropped = {
            row.utterance
            for key, row in chat_pointers.CHAT_POINTERS.items()
            if isinstance(row, POINTER)
            and connector_of_pointer_key(key) is not None
            and connector_of_pointer_key(key)
            not in integration_status_service.BETA_OFFERED_CONNECTORS
        }
        assert {"connect my slack", "connect my notion"} <= dropped
        expected = [u for u in pointer_utterances() if u not in dropped]
        assert answer_utterances() == expected
        assert len(capability_answer_lines()) == len(CORE_CAPABILITIES) + len(expected)

    def test_the_ledger_and_the_ratchets_denominator_are_untouched(self):
        """pointer_utterances() still lists every POINTER: the refusal path stays routable."""
        assert "connect my slack" in pointer_utterances()
        assert "connect my notion" in pointer_utterances()


class TestTheFilterReadsKeysNotWords:
    @pytest.mark.parametrize(
        "key, connector",
        [
            ("integration:slack", "slack"),
            ("integration:github", "github"),
            ("page:/settings/integrations/notion", "notion"),
            ("page:/settings/integrations/calendar", "calendar"),
            ("page:/settings/integrations/calendar/callback", "calendar"),
            ("page:/settings", None),
            ("capability:post_to_slack", None),
            ("pin:anything", None),
        ],
    )
    def test_connector_of_pointer_key(self, key, connector):
        assert connector_of_pointer_key(key) == connector

    def test_a_row_that_names_no_connector_is_never_dropped_for_its_words(self, monkeypatch):
        """A non-connector row whose utterance mentions slack is not a phrase match."""
        ledger = dict(chat_pointers.CHAT_POINTERS)
        ledger["pin:2245_words"] = POINTER(
            "tell me about slack", expects=("guidance", "get_contextual_guidance")
        )
        assert "tell me about slack" in answer_utterances(ledger)

    def test_an_utterance_shared_by_an_offered_row_survives(self, monkeypatch):
        """Dedup follows the ledger: one offered row keeps the utterance in the answer."""
        ledger = dict(chat_pointers.CHAT_POINTERS)
        ledger["page:/settings/integrations/slack"] = POINTER(
            "connect my slack", expects=("guidance", "get_contextual_guidance")
        )
        ledger["pin:2245_shared"] = POINTER(
            "connect my slack", expects=("guidance", "get_contextual_guidance")
        )
        assert "connect my slack" in answer_utterances(ledger)
