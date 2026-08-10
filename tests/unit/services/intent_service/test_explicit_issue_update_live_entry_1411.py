"""#1411 follow-up (2026-08-10) — the LIVE entry must route explicit issue
updates to update_issue, hash and no-hash alike.

PM's production transcript (2026-08-10, deployed cut containing the 08-09
Stage-0 work):

- "change the status of issue #108 to in progress" → the DOCUMENT handler's
  "which document to update?" copy.
- "change the title of issue 108" → update_issue (asked for the repository).

The 08-09 fix was on the live path all along (classify_multiple's Stage 0 runs
first at the real entry) — but its detector's field vocabulary
(``_ISSUE_FIELD_WORDS``) had no "status", so PM's status phrasing missed
Stage 0 in BOTH forms. From there the two forms DIVERGED (keyless live-entry
repro, 2026-08-10):

- no-hash: surface 1's ``change … to`` document pattern claimed it →
  ``update_document_query`` @ 1.0, deterministically;
- hash: the '#' breaks that pattern's ``[\\w\\s]+`` span, so every
  deterministic surface passed and the LLM classifier (surface 2) decided —
  in production it chose the document lane. The hash-form misroute is the LLM
  leg and does NOT reproduce keylessly (keyless run raises
  INTENT_CLASSIFICATION_FAILED at the same fork).

So the asymmetry PM hit was "status" vs "title" (vocabulary), surfaced as
hash vs no-hash (which downstream surface claimed the fallthrough). These
tests drive the REAL entry the web route calls —
``IntentService.process_intent`` (web/api/routes/intent.py → POST /intent) —
mocked only at the LLM and GitHub-API boundaries, and pin:

1. PM's exact production sentence routes to update_issue with the LLM
   structurally unreachable (deterministic reachability, not corpus);
2. AGREEMENT: hash and no-hash forms of the same sentence route identically
   (the asymmetry becomes unrepresentable);
3. the no-hash form is never document-claimed again.
"""

import pytest

from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier

# PM's verbatim production phrasings (2026-08-10).
PM_STATUS_HASH = "change the status of issue #108 to in progress"
PM_STATUS_NO_HASH = "change the status of issue 108 to in progress"
# The 08-09 retest pair, driven through the same live entry for agreement.
PM_TITLE_HASH = "change the title of issue #108 to test new regressions"
PM_TITLE_NO_HASH = "change the title of issue 108 to test new regressions"

_USER = "3f7b8a52-1411-4b00-9e00-000000001411"  # valid UUID: survives principal parsing


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Explicit-#N
    updates must be deterministically routed; reachability is not corpus."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — explicit issue updates must "
            "resolve deterministically at Stage 0, never via the LLM classifier"
        )


@pytest.fixture
def live_service(monkeypatch):
    """The real IntentService + real IntentClassifier, mocked ONLY at the two
    external boundaries: the LLM (explosive — must never be reached) and the
    GitHub API (deterministic not-connected — a unit test must never attempt a
    live API call; the handler's not-connected reply still carries the routed
    intent_data, which is what these tests assert on)."""
    from services.integrations.github.github_integration_router import (
        GitHubIntegrationRouter,
    )

    async def _noop_init(self, user_id=None):
        return None

    async def _unavailable(self):
        return False

    monkeypatch.setattr(GitHubIntegrationRouter, "initialize", _noop_init)
    monkeypatch.setattr(GitHubIntegrationRouter, "is_available", _unavailable)

    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _routed_action(result):
    return (result.intent_data or {}).get("action")


class TestLiveEntryRouting:
    pytestmark = pytest.mark.asyncio

    async def test_pm_production_sentence_reaches_update_issue(self, live_service):
        """PM's exact 2026-08-10 sentence through the real entry: update_issue,
        LLM structurally unreachable. Red before the vocabulary fix: the hash
        form fell through Stage 0 AND surface 1 to the LLM classifier."""
        result = await live_service.process_intent(
            message=PM_STATUS_HASH, session_id="live-1411b-s1", user_id=_USER
        )
        assert _routed_action(result) == "update_issue"

    async def test_no_hash_form_is_not_document_claimed(self, live_service):
        """Red before the fix: surface 1's document pattern claimed this
        deterministically (update_document_query @ 1.0) — the keyless repro of
        the misroute lane PM saw."""
        result = await live_service.process_intent(
            message=PM_STATUS_NO_HASH, session_id="live-1411b-s2", user_id=_USER
        )
        assert _routed_action(result) != "update_document_query"
        assert _routed_action(result) == "update_issue"

    @pytest.mark.parametrize(
        "hash_form,no_hash_form,sid",
        [
            (PM_STATUS_HASH, PM_STATUS_NO_HASH, "live-1411b-agree-status"),
            (PM_TITLE_HASH, PM_TITLE_NO_HASH, "live-1411b-agree-title"),
        ],
    )
    async def test_agreement_hash_and_no_hash_route_identically(
        self, live_service, hash_form, no_hash_form, sid
    ):
        """The asymmetry PM hit (one form issue-routed, the other
        document-claimed) becomes unrepresentable: both forms of the same
        sentence must route to the same action, and that action is
        update_issue."""
        r_hash = await live_service.process_intent(
            message=hash_form, session_id=f"{sid}-h", user_id=_USER
        )
        r_no_hash = await live_service.process_intent(
            message=no_hash_form, session_id=f"{sid}-n", user_id=_USER
        )
        assert _routed_action(r_hash) == _routed_action(r_no_hash)
        assert _routed_action(r_hash) == "update_issue"
