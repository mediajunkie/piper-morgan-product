"""#1269: deterministic standup-query routing.

The LLM classifier conflates "give me my standup" with action `get_project_status`
(verified live 2026-06-18: all standup phrasings → get_project_status, conf 1.0), so
standup-query phrasings never reached `_handle_standup_query` and the chat improvised a
fabricated standup. `IntentService._is_standup_query` routes them deterministically to the
derived standup BEFORE classification — and is unit-testable, closing the gap where green
handler/registration unit tests hid a broken end-to-end chain.
"""

from services.intent.intent_service import IntentService


class TestStandupQueryDetection:
    def test_matches_request_phrasings(self):
        for m in [
            "please give me my standup",  # PM's exact prompt (2026-06-18)
            "give me my standup",
            "what's my standup?",
            "what is my standup",
            "show my standup",
            "Show me my standup",
            "my standup please",
            "give me the standup for today",
            "today's standup",
        ]:
            assert IntentService._is_standup_query(m), m

    def test_does_not_match_command_or_incidental(self):
        for m in [
            "/standup",  # interactive capture command — handled separately (#585)
            "how do I run a standup meeting?",
            "schedule a standup",
            "what's my project status",  # the action the classifier conflates standup with
            "give me a status update",
            "remind me about the standup feature",
        ]:
            assert not IntentService._is_standup_query(m), m
