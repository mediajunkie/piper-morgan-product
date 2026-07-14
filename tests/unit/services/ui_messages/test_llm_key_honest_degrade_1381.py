"""LLM-key failures degrade honestly, not as a transient "try again" (PM 2026-07-14).

The live case: a fresh beta account stored an OpenAI key that later ran out of
quota. Every chat turn failed with `All configured LLM providers failed. Details:
openai: Error code: 429 - insufficient_quota`, and the chat route reported "AI
service is temporarily unavailable. Please try again in a few moments." That is a
lie — the key is dead, retrying never recovers, and the user is given no path to
the actual fix (Settings → LLM API Keys).

These tests pin the two guarantees:
1. The humanizer classifies quota/auth as a PERMANENT key problem (category
   "llm_key") with an actionable Settings recovery — and quota MUST win over the
   generic 429/rate-limit pattern (ordering matters).
2. A genuine transient (connection error) still degrades as a brief outage, NOT a
   key problem.
"""

import pytest

from services.ui_messages.user_friendly_errors import make_error_user_friendly

# The exact string seen in Fly logs during Scenario A.
QUOTA_ERROR = "All configured LLM providers failed. Details: openai: Error code: 429 - insufficient_quota"


class TestQuotaIsPermanentNotTransient:
    def test_insufficient_quota_is_llm_key_category(self):
        f = make_error_user_friendly(RuntimeError(QUOTA_ERROR))
        assert f["category"] == "llm_key"

    def test_quota_wins_over_generic_429_pattern(self):
        """The error string also contains '429'; the quota pattern must match
        FIRST so we don't frame a dead key as a rate-limit 'slow down'."""
        f = make_error_user_friendly(RuntimeError(QUOTA_ERROR))
        assert f["category"] != "rate_limit"

    def test_quota_recovery_points_at_settings(self):
        f = make_error_user_friendly(RuntimeError(QUOTA_ERROR))
        assert "Settings" in f["recovery"]
        assert "LLM API Keys" in f["recovery"]

    def test_quota_message_does_not_promise_transience(self):
        f = make_error_user_friendly(RuntimeError(QUOTA_ERROR))
        text = f"{f['message']} {f['recovery']}".lower()
        assert "temporarily unavailable" not in text


class TestInvalidKey:
    def test_invalid_api_key_is_llm_key_category(self):
        f = make_error_user_friendly(RuntimeError("openai: Error code: 401 - invalid_api_key"))
        assert f["category"] == "llm_key"
        assert "isn't valid" in f["message"]


class TestTransientStillTransient:
    def test_connection_error_is_not_a_key_problem(self):
        """A provider connection blip is a real brief outage — it must NOT claim
        the user's key is bad (which would send them to fix a key that's fine)."""
        f = make_error_user_friendly(
            RuntimeError("All configured LLM providers failed. Details: anthropic: Connection error")
        )
        assert f["category"] == "llm"
        assert "brief outage" in f["recovery"]
