"""#1870 (follow-up 3 of 3 from #1718) — two classifiers exist for the same LLM
failure family and can drift:

  - `services/intent_service/conversational_floor.py::_classify_llm_error`
    (#1824's five/six-bucket RUNTIME classifier — picks a FLOOR_FALLBACK_*
    chat message)
  - `services/ui_messages/user_friendly_errors.py::make_error_user_friendly`
    (the translator #1718 reuses at key-VALIDATION time, and the route's
    degradation extractor reuses at runtime)

Per the issue: do NOT merge them blindly. This file (a) documents the full
bucket table for both (below), (b) implements the ONE safe delegation found —
quota detection, where the floor had NO bucket at all and the translator's
judgment is already ratified copy (see conversational_floor.py's
FLOOR_FALLBACK_QUOTA / `_QUOTA_PATTERN` import, #1870) — and (c) for every
other case, PINS the actual observed (dis)agreement here as ground truth, so
any future change to either classifier that shifts a fixture's bucket without
updating this file fails loudly (drift protection), instead of silently
re-diverging. Where they disagree, this file reports it — it does not pick a
winner; several of the disagreements below are their own finding for CXO/PM,
not a defect this issue asked this Agent to resolve.

================================================================================
BUCKET TABLE (as of #1870, both classifiers read verbatim from source)
================================================================================

_classify_llm_error (conversational_floor.py) — checked in this order:
  1. consent_unreadable   — isinstance ConsentUnreadableError (TYPE match, #1816)
  2. quota_exhausted       — re.search(QUOTA_PATTERN) [NEW, #1870, delegates]
  3. no_provider           — "not configured" or "no llm provider" in text
  4. not_configured        — "not initialized" in text
  5. insufficient_permission — "403" or "forbidden" in text
  6. rejected_credential   — "401"/"unauthorized"/"invalid api key"/
                              "invalid_api_key"/"authentication" in text
  7. config_endpoint       — "model"+("not found"|"does not exist"), or "404"
  8. transient             — catch-all

make_error_user_friendly (user_friendly_errors.py) — first regex match wins,
case-insensitive, in dict-declaration order (LLM-relevant entries only):
  1. llm_key (quota)      — QUOTA_PATTERN (same regex #1870 now shares)
  2. llm_key (invalid)    — invalid_api_key|incorrect api key|invalid.*x-api-key
                             |authentication_error|invalid api key provided
  3. llm_key (permission) — permission_error|permission denied.*model|
                             does not have access to model
  4. llm_key (no-key)     — has no llm key of their own|user llm key required|
                             no llm key configured|no api key configured
  5. llm (all failed)     — all configured llm providers failed
  6-14. generic HTTP/db/file/timeout/validation buckets (401/403/404/429/500,
        "Not Found", "Forbidden", "Unauthorized", relation-does-not-exist, ...)
  15. unknown              — fallback, "Something unexpected happened."

================================================================================
FINDINGS (live-computed, see the PINNED table below for exact fixture->bucket)
================================================================================

FIXED (this issue): quota-shaped errors (#1718's real OpenAI 429/Anthropic 400
no-credits bodies) previously classified "transient" in the floor (-> "try
again in a moment", wrong advice for a permanent billing problem) while the
translator already correctly said "llm_key"/quota. Now both agree via shared
QUOTA_PATTERN.

REPORTED, NOT FIXED (CXO/PM copy call, per the issue's own instruction not to
pick a winner):

  (a) STANDOUT — the floor's OWN real production trigger string doesn't hit
      its OWN "no_provider" bucket. `no_provider` requires "not configured" or
      "no llm provider" in the text; the actual message raised elsewhere in
      this codebase is "All configured LLM providers failed." (confirmed via
      grep — services/llm/clients.py:442 raises it verbatim, and #1824's own
      TestDoubleWrapPropagation fixture reuses it as PROVIDER_401's prefix) —
      which contains NEITHER substring. It falls through everything to
      "transient" ("try again in a moment"), even though nothing is transient
      about zero configured providers. The translator, by contrast, DOES
      recognize this exact string via its dedicated "all configured llm
      providers failed" pattern -> "I couldn't reach a language model just
      now." This is a latent bug in the floor's own classifier against its
      own documented trigger, independent of any merge decision — flagging
      for Lead/CXO as the single most actionable finding in this file.

  (b) Bare status-word messages ("Unauthorized" with no other text, "Error
      code: 403" with no other text) — the floor's substring checks are loose
      enough to catch these ("401"/"403" alone), correctly bucketing
      rejected_credential / insufficient_permission. The translator's llm_key
      patterns require more specific substrings (e.g. "invalid_api_key",
      "authentication_error") that a BARE status code/word doesn't carry, so
      these fall through to the translator's GENERIC "auth" category, whose
      copy ("check your login status", "contact your administrator") is
      actively wrong for an LLM-key scenario (there is no "administrator" for
      a personal API key). The floor's copy is correct here; the translator's
      generic fallback is not LLM-aware. Not fixed — changing the translator's
      generic-auth copy or pattern set is a CXO call, and it's used for
      non-LLM auth failures too (GitHub, DB, etc.) so tightening it isn't free.

  (c) config_endpoint (model-not-found/404) messages mostly fall to the
      translator's generic "unknown" or "api" (couldn't-find-what-you're-
      looking-for) buckets — neither of which fits an operator-side stale
      model ID. The floor's copy ("I'm set up to use a model that isn't
      available. That's ours to fix.") is the more honest one. Not fixed for
      the same reason as (b).

  (d) Gemini's real invalid-key body ("API key not valid... API_KEY_INVALID",
      live-verified #1870) matches NEITHER classifier's invalid-key pattern —
      a SHARED gap, not a disagreement between them (both silently miss it).
      See tests/config/test_llm_key_validation_reasons_1870.py for the pinned
      evidence; not fixed here (pattern-authoring is the CXO-copy-call class
      of change this issue asks NOT to make unilaterally).

LAYER (m-43): pure-unit, both classifiers called directly with real fixture
strings — no network, no LLM call. DENOMINATOR: all 14 distinct #1824 test
fixtures (the parametrized message strings from
tests/unit/services/intent_service/test_llm_error_buckets_1824.py) + the 4
#1718 real provider bodies (OpenAI 401/429, Anthropic 401/400) + the 3 #1870
live-verified provider bodies (Gemini 400/403, Perplexity 401) + the one real
production "no_provider" trigger string. 22 fixtures total, all pinned below.
"""

import pytest

from services.intent_service.conversational_floor import _classify_llm_error
from services.ui_messages.user_friendly_errors import make_error_user_friendly

# Fixture name -> (message, expected_floor_bucket, expected_translator_category)
# PINNED from an actual run against both classifiers on 2026-09-24 (#1870) —
# NOT hand-derived. A change to either classifier that shifts any of these
# must update this table explicitly (drift protection), not silently pass.
PINNED_FIXTURES = {
    # --- #1824 fixtures: rejected_credential family (AGREE: both llm-key/invalid) ---
    "1824_401_auth_err": (
        "Error code: 401 - authentication_error: API key is invalid",
        "rejected_credential",
        "llm_key",
    ),
    "1824_invalid_api_key": ("invalid_api_key", "rejected_credential", "llm_key"),
    "1824_invalid_key_provided": (
        "Invalid API key provided",
        "rejected_credential",
        "llm_key",
    ),
    # --- #1824: bare status text — DISAGREE, finding (b) above ---
    "1824_unauthorized_bare": ("Unauthorized", "rejected_credential", "auth"),
    "1824_403_bare": ("Error code: 403", "insufficient_permission", "unknown"),
    # --- #1824: insufficient_permission with descriptive text — DISAGREE (generic auth) ---
    "1824_forbidden_model": (
        "Forbidden: your account does not allow this model",
        "insufficient_permission",
        "auth",
    ),
    # --- #1824: not_configured — DISAGREE (translator has no equivalent bucket) ---
    "1824_not_initialized": (
        "Anthropic client not initialized",
        "not_configured",
        "unknown",
    ),
    # --- #1824: config_endpoint family — DISAGREE, finding (c) above ---
    "1824_model_not_found": (
        "The model claude-old-1 was not found",
        "config_endpoint",
        "api",
    ),
    "1824_model_does_not_exist": (
        "model gpt-x does not exist",
        "config_endpoint",
        "unknown",
    ),
    "1824_404_not_found_err": (
        "Error code: 404 - not_found_error",
        "config_endpoint",
        "unknown",
    ),
    # --- #1824: no_provider (synthetic test fixture) — DISAGREE ---
    "1824_no_provider_synthetic": (
        "No LLM provider not configured",
        "no_provider",
        "unknown",
    ),
    # --- REAL production no_provider trigger — STANDOUT finding (a) above ---
    "real_all_providers_failed": (
        "All configured LLM providers failed.",
        "transient",  # <- the floor's OWN bug against its OWN real trigger
        "llm",
    ),
    # --- #1824: transient (AGREE: both recognize non-LLM-specific timeout) ---
    "1824_read_timeout": ("Read timed out", "transient", "timeout"),
    # --- #1718 real provider bodies: rejected_credential (AGREE) ---
    "1718_openai_401": (
        'Invalid API key: 401 Unauthorized {"error": {"message": "Incorrect API '
        'key provided", "type": "invalid_request_error", "param": null, "code": '
        '"invalid_api_key"}}',
        "rejected_credential",
        "llm_key",
    ),
    "1718_anthropic_401": (
        'Invalid API key: 401 Unauthorized {"type":"error","error":{"type":'
        '"authentication_error","message":"invalid x-api-key"}}',
        "rejected_credential",
        "llm_key",
    ),
    # --- #1718 real provider bodies: quota — FIXED by #1870 (now AGREE) ---
    "1718_openai_429_quota": (
        "Validation failed: 429 Too Many Requests {'error': {'message': 'You "
        "have no credits remaining. Add credits to continue using the API at "
        "https://platform.openai.com/settings/organization/billing/.', 'type': "
        "'insufficient_quota', 'param': None, 'code': 'credit_balance_exhausted'}}",
        "quota_exhausted",
        "llm_key",
    ),
    "1718_anthropic_400_nocredit": (
        'Validation failed: 400 Bad Request {"type":"error","error":{"type":'
        '"invalid_request_error","message":"Your credit balance is too low to '
        "access the Claude API. Please go to Plans \\u0026 Billing to upgrade or "
        'purchase credits."}}',
        "quota_exhausted",
        "llm_key",
    ),
    # --- #1870 live-verified: Perplexity 401 (AGREE) ---
    "1870_perplexity_401": (
        'Invalid API key: 401 Unauthorized {"error":{"message":"Invalid API key '
        'provided. You can find your API key at https://console.perplexity.ai.",'
        '"type":"invalid_api_key","code":401}}',
        "rejected_credential",
        "llm_key",
    ),
    # --- #1870 live-verified: Gemini invalid-key body — SHARED GAP, finding (d) ---
    "1870_gemini_400_invalid": (
        'Validation failed: 400 {"error": {"code": 400, "message": "API key not '
        'valid. Please pass a valid API key.", "status": "INVALID_ARGUMENT", '
        '"details": [{"reason": "API_KEY_INVALID"}]}}',
        "transient",  # neither classifier's patterns match Gemini's real wording
        "unknown",
    ),
    # --- #1870 live-verified: Gemini no-key-at-all 403 (loosely agree: both LLM-ish) ---
    "1870_gemini_403_nokey": (
        'Invalid API key: 403 {"error": {"code": 403, "message": "Method does '
        "not allow unregistered callers (callers without established identity). "
        "Please use API Key or other form of API consumer identity to call this "
        'API.", "status": "PERMISSION_DENIED"}}',
        "insufficient_permission",
        "unknown",  # translator's generic 403 pattern requires literal "HTTP"/"Forbidden"
    ),
}


class TestClassifierAgreementPinned:
    """Every fixture's (floor_bucket, translator_category) pair is asserted
    exactly as pinned above — this catches BOTH new disagreements (a fixture
    that used to agree starts disagreeing) AND silent re-divergence (a fixture
    whose disagreement was known drifts to a DIFFERENT disagreement) without
    this file being updated."""

    @pytest.mark.parametrize("name", list(PINNED_FIXTURES.keys()))
    def test_pinned_bucket_pair(self, name):
        message, expected_floor, expected_translator_category = PINNED_FIXTURES[name]
        floor_bucket = _classify_llm_error(Exception(message))
        translator_category = make_error_user_friendly(Exception(message))["category"]

        assert floor_bucket == expected_floor, (
            f"{name}: floor bucket drifted — was {expected_floor!r}, now "
            f"{floor_bucket!r}. Update PINNED_FIXTURES deliberately if this is "
            f"an intended change, don't just relax the assertion."
        )
        assert translator_category == expected_translator_category, (
            f"{name}: translator category drifted — was "
            f"{expected_translator_category!r}, now {translator_category!r}. "
            f"Update PINNED_FIXTURES deliberately if this is an intended change."
        )


class TestQuotaDelegationClosesTheGap:
    """#1870's one implemented delegation: quota detection now agrees because
    the floor imports the SAME regex, not because it independently arrived at
    the same judgment — a future edit to QUOTA_PATTERN in
    user_friendly_errors.py changes both classifiers' quota detection at once."""

    @pytest.mark.parametrize(
        "name",
        ["1718_openai_429_quota", "1718_anthropic_400_nocredit"],
    )
    def test_quota_fixtures_agree_after_1870(self, name):
        message, expected_floor, expected_translator_category = PINNED_FIXTURES[name]
        assert expected_floor == "quota_exhausted"
        assert expected_translator_category == "llm_key"
        assert _classify_llm_error(Exception(message)) == "quota_exhausted"
        friendly = make_error_user_friendly(Exception(message))
        assert friendly["category"] == "llm_key"
        assert "quota" in friendly["message"].lower() or "billing" in friendly["message"].lower()

    def test_shared_quota_pattern_is_the_single_source(self):
        """Both modules import/reference the SAME compiled pattern text — not
        two hand-copied regexes that can silently diverge."""
        from services.intent_service.conversational_floor import _QUOTA_PATTERN
        from services.ui_messages.user_friendly_errors import QUOTA_PATTERN

        assert _QUOTA_PATTERN is QUOTA_PATTERN
