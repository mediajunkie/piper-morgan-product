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

FIXED (#1870): quota-shaped errors (#1718's real OpenAI 429/Anthropic 400
no-credits bodies) previously classified "transient" in the floor (-> "try
again in a moment", wrong advice for a permanent billing problem) while the
translator already correctly said "llm_key"/quota. Now both agree via shared
QUOTA_PATTERN.

FIXED (#1872 — this issue):

  (a) STANDOUT, RESOLVED FOR THE TYPED PATH — the floor's OWN real production
      trigger string didn't hit its OWN "no_provider" bucket: `no_provider`
      required "not configured" or "no llm provider" in the text, and the
      actual message raised at services/llm/clients.py — "All configured LLM
      providers failed. Details: ..." — contains NEITHER substring, so it fell
      through everything to "transient" regardless of cause (zero providers,
      a rejected credential, a connection blip — one string, one wrong
      answer). Fixed AT THE PRODUCER, not with a smarter string pattern (the
      issue's own point: a one-line pattern can't be honest for three
      different causes behind one string): `clients.py` now raises a typed
      `AllProvidersFailed(attempts=[(provider, reason), ...])`; the floor's
      `_classify_llm_error` classifies from the TYPE first — `no_providers`
      (an honest fact read off `attempts`, never inferred from text) ->
      `no_provider`, otherwise the PRIMARY provider's own `reason` classified
      through the shared `classify_llm_error_text`. See
      `TestTypedExceptionResolvesStandoutFinding` below — four fixtures
      constructed via the REAL producer type, all previously-transient,
      now bucketed honestly. The UNTYPED bare-string fixture
      (`real_all_providers_failed` below) is DELIBERATELY left unresolved —
      text alone still can't disambiguate the three causes, which is exactly
      why the fix had to be type-based, not pattern-based.

  (d) Gemini's real invalid-key body ("API key not valid... API_KEY_INVALID",
      live-verified #1870) — previously matched NEITHER classifier's
      invalid-key pattern (a SHARED gap, not a disagreement). #1872 item 3
      adds it to both via the named `GEMINI_INVALID_KEY_PATTERN` /
      `INVALID_KEY_PATTERN` constants in user_friendly_errors.py — both now
      agree (rejected_credential / llm_key). See the updated
      `1870_gemini_400_invalid` row below; See also
      tests/config/test_llm_key_validation_reasons_1870.py for the original
      pinned evidence of the gap.

REPORTED, NOT FIXED (CXO/PM copy call, per the issue's own instruction not to
pick a winner — #1872 explicitly did not touch these):

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

LAYER (m-43): pure-unit, both classifiers called directly with real fixture
strings — no network, no LLM call. DENOMINATOR: all 14 distinct #1824 test
fixtures (the parametrized message strings from
tests/unit/services/intent_service/test_llm_error_buckets_1824.py) + the 4
#1718 real provider bodies (OpenAI 401/429, Anthropic 401/400) + the 3 #1870
live-verified provider bodies (Gemini 400/403, Perplexity 401) + the one real
production "no_provider" trigger string. 22 string fixtures total, all pinned
below in PINNED_FIXTURES. #1872 adds 4 more fixtures in PINNED_TYPED_FIXTURES,
constructed via the REAL `AllProvidersFailed` producer type rather than a
hand-written string — the fix this issue makes is dispatched on TYPE, not on
any string pattern, so a string-only denominator can't exercise it. 26
fixtures total across both tables.
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
    # --- #1870 live-verified: Gemini invalid-key body — FIXED by #1872 item 3
    # (was: SHARED GAP, finding (d) — neither classifier's patterns matched
    # Gemini's real wording). Both now recognize it via the shared
    # `GEMINI_INVALID_KEY_PATTERN`/`INVALID_KEY_PATTERN` in
    # user_friendly_errors.py (AGREE, both llm-key/invalid) ---
    "1870_gemini_400_invalid": (
        'Validation failed: 400 {"error": {"code": 400, "message": "API key not '
        'valid. Please pass a valid API key.", "status": "INVALID_ARGUMENT", '
        '"details": [{"reason": "API_KEY_INVALID"}]}}',
        "rejected_credential",
        "llm_key",
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


# #1872: fixtures constructed via the REAL `AllProvidersFailed` producer type
# (services/llm/clients.py) rather than a hand-written string — the fix this
# issue makes is dispatched on the exception's TYPE (`isinstance`,
# `.no_providers`, `.primary_reason`), so only a typed fixture can exercise
# it. Name -> (attempts, expected_floor_bucket, expected_translator_category).
PINNED_TYPED_FIXTURES = {
    # STANDOUT finding (a), invalid-key leg — the issue's own illustrative
    # example (`Details: anthropic: invalid x-api-key`): a primary reason
    # carrying NONE of the "401"/"authentication_error" wrapper a raw
    # provider exception usually includes. Needed INVALID_KEY_PATTERN's
    # `invalid.*x-api-key` clause OR'd into classify_llm_error_text's
    # rejected_credential check (#1872), not just the typed dispatch alone.
    "1872_typed_invalid_key": (
        [("anthropic", "invalid x-api-key")],
        "rejected_credential",
        "llm_key",
    ),
    # STANDOUT finding (a), connection leg — the issue's other example
    # (`Details: anthropic: Connection error.`, the CLAUDE.md env-var-
    # shadowing symptom). Genuinely transient: the fix is that this is now an
    # HONEST transient (classified from the actual primary reason), not an
    # ACCIDENTAL one (pre-#1872, EVERY cause fell here).
    "1872_typed_connection_error": (
        [("anthropic", "Connection error.")],
        "transient",
        "llm",
    ),
    # STANDOUT finding (a), quota leg.
    "1872_typed_quota": (
        [("openai", "insufficient_quota: You have no credits remaining")],
        "quota_exhausted",
        "llm_key",
    ),
    # STANDOUT finding (a), the zero-providers leg itself — the floor's OWN
    # no_provider bucket now fires from the typed `.no_providers` fact
    # instead of falling through to transient. (Note: the real producer's
    # only call site never actually constructs zero attempts — primary_exc is
    # always attempts[0] — so this exercises the property for correctness/
    # future call sites, per the issue's "derived honestly" requirement, not
    # a scenario clients.py currently reaches.)
    "1872_typed_zero_providers": (
        [],
        "no_provider",
        "llm",
    ),
}


class TestTypedExceptionResolvesStandoutFinding:
    """#1872: finding (a) — the floor's OWN real production trigger not
    hitting its OWN no_provider bucket — is resolved for the TYPED exception
    path (the real producer, `AllProvidersFailed` in services/llm/clients.py).
    The untyped bare-string fixture (`real_all_providers_failed` above) is
    DELIBERATELY left classifying "transient": text alone can't disambiguate
    the three causes the issue describes, and a one-line string pattern would
    be dishonest for two of them (the issue's own reasoning) — only the TYPE
    closes the gap, which is why the fix lives in the producer, not in a
    smarter regex."""

    @pytest.mark.parametrize("name", list(PINNED_TYPED_FIXTURES.keys()))
    def test_typed_fixture_resolves(self, name):
        from services.llm.clients import AllProvidersFailed

        attempts, expected_floor, expected_translator_category = PINNED_TYPED_FIXTURES[name]
        exc = AllProvidersFailed(attempts)

        floor_bucket = _classify_llm_error(exc)
        translator_category = make_error_user_friendly(exc)["category"]

        assert floor_bucket == expected_floor, (
            f"{name}: resolved typed-exception bucket regressed — a "
            f"previously-fixed case fell back to a different bucket. Expected "
            f"{expected_floor!r}, got {floor_bucket!r}."
        )
        assert translator_category == expected_translator_category, (
            f"{name}: translator category regressed — expected "
            f"{expected_translator_category!r}, got {translator_category!r}."
        )

    def test_none_fall_to_transient_unless_genuinely_transient(self):
        """The issue's own acceptance bar: none of the resolved cases read
        'try again in a moment' unless the cause really is transient (the
        connection-error leg only)."""
        from services.llm.clients import AllProvidersFailed

        for name, (attempts, _expected_floor, _cat) in PINNED_TYPED_FIXTURES.items():
            bucket = _classify_llm_error(AllProvidersFailed(attempts))
            if name == "1872_typed_connection_error":
                assert bucket == "transient"
            else:
                assert bucket != "transient", f"{name} incorrectly fell to transient"

    def test_str_stays_byte_identical_to_pre_1872_message(self):
        """The producer's promise (#1872 AC): AllProvidersFailed's str() is
        unchanged so every existing string-matching consumer — the web
        route's degradation extractor, the translator's own pattern table,
        and every pre-#1872 test that greps this literal text — keeps
        working unchanged."""
        from services.llm.clients import AllProvidersFailed

        exc = AllProvidersFailed(
            [("anthropic", "invalid x-api-key"), ("openai", "429 rate limited")]
        )
        assert str(exc) == (
            "All configured LLM providers failed. Details: "
            "anthropic: invalid x-api-key; openai: 429 rate limited"
        )

    def test_no_providers_is_read_from_attempts_not_text(self):
        """`.no_providers` is an honest structural fact, not a string guess —
        it stays correct even fed a reason string that itself contains
        provider-sounding text, and correctly False the moment any attempt
        exists (the real producer's only call site: primary_exc is always
        attempts[0], so it can never construct a zero-attempt instance —
        this fixture exists for the property, not that scenario)."""
        from services.llm.clients import AllProvidersFailed

        assert AllProvidersFailed([]).no_providers is True
        assert AllProvidersFailed([("anthropic", "no llm provider configured")]).no_providers is (
            False
        )
