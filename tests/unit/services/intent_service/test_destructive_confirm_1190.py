"""#1190 [MVP] — multi-turn confirmation gate for destructive issue mutations.

PM ruling (decisions.log 2026-08-10 ~10:55): close_issue / reopen_issue are
DESTRUCTIVE — the point is BLAST-RADIUS protection (a closed Beta Blocker
disappears from every board/query that filters on open state, and the 2026-07
auto-close incident closed a live Beta Blocker from a commit message).
Recoverability ("reversible via reopen") was the old WRITE rationale and is
explicitly retired by the ruling.

These are the FIRST DESTRUCTIVE rail entries — the tier goes from
tests-only (synthetic entries in test_workflow_dispatcher.py) to live.

Layer honesty (m-43): the end-to-end classes drive the REAL entry the web
route calls (``IntentService.process_intent``, the #1411-test idiom), mocked
ONLY at the LLM boundary (explosive — deterministic pre-classification must
carry every turn) and the GitHub-router boundary (explosive wherever nothing
should fire; deterministic stubs on the confirmed-execution turn).
"""

from unittest.mock import AsyncMock

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingError, IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
    build_confirmation_offer,
    detect_bare_exit,
)
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import (
    register_default_workflows,
    run_confirm_pending_action_workflow,
)
from services.shared_types import EffectClass, IntentCategory

CLOSE_ALIASES = ("close_issue", "close_issue_query")
REOPEN_ALIASES = ("reopen_issue", "reopen_issue_query")
# #1666: delete_todo joined the destructive tier (its own ruling — the
# consent-gate coverage gap Arch found; suite: test_delete_todo_confirm_1666).
DELETE_TODO_ALIASES = ("delete_todo", "remove_todo", "cancel_todo")

_USER = "3f7b8a52-1190-4b00-9e00-000000001190"  # valid UUID: survives principal parsing


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every turn in
    these tests must resolve deterministically (pre-classifier or the
    pending-offer seam, which runs before classification)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1190 turns must resolve "
            "deterministically"
        )


def _close_intent(message="close issue #108", action="close_issue_query", context=None):
    ctx = {"original_message": message}
    if context:
        ctx.update(context)
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        context=ctx,
        confidence=0.95,
        original_message=message,
    )


class TestDestructiveEnumFlips1190:
    """Part 1: the enum flips. RED while close/reopen are still WRITE."""

    def test_close_issue_entries_are_destructive(self):
        register_default_workflows()
        wf = get_action_workflows()
        for alias in CLOSE_ALIASES:
            assert wf[alias].effect == EffectClass.DESTRUCTIVE, (
                f"{alias} must be DESTRUCTIVE (PM ruling 2026-08-10: "
                "blast-radius protection, not recoverability)"
            )

    def test_reopen_issue_entries_are_destructive(self):
        register_default_workflows()
        wf = get_action_workflows()
        for alias in REOPEN_ALIASES:
            assert wf[alias].effect == EffectClass.DESTRUCTIVE, (
                f"{alias} must be DESTRUCTIVE (PM ruling 2026-08-10)"
            )

    def test_destructive_entries_derive_needs_confirm(self):
        """The #1190 gate keys off needs_confirm — the flip must make the
        derived predicate true (never a re-derivation from names)."""
        register_default_workflows()
        wf = get_action_workflows()
        for alias in CLOSE_ALIASES + REOPEN_ALIASES:
            assert wf[alias].needs_confirm is True
            assert wf[alias].destructive_hint is True
            assert wf[alias].needs_consent is True  # destructive ⊂ write

    def test_destructive_tier_scope_with_denominator(self):
        """m-44: state the denominator. Exactly close/reopen (2 entries,
        4 alias keys — PM ruling 2026-08-10) plus delete_todo (1 entry,
        3 alias keys — #1666: the consent-gate coverage gap; deletion is
        unrecoverable, so DESTRUCTIVE needs no blast-radius reframing) is
        DESTRUCTIVE on the action rail today. If a new action legitimately
        joins the tier, update this set in the same commit that flips its
        entry."""
        register_default_workflows()
        wf = get_action_workflows()
        destructive_keys = {
            key for key, entry in wf.items() if entry.effect == EffectClass.DESTRUCTIVE
        }
        assert destructive_keys == (
            set(CLOSE_ALIASES) | set(REOPEN_ALIASES) | set(DELETE_TODO_ALIASES)
        ), (
            f"Destructive rail keys drifted: {sorted(destructive_keys)}. "
            "The tier is exactly close/reopen (PM ruling 2026-08-10) + the "
            "delete_todo family (#1666); a new destructive entry needs its "
            "own ruling + this set updated."
        )


class TestConfirmationOfferBuilder:
    """Part 2 machinery: the gate's question + pending-action record."""

    def test_numbered_close_builds_question_and_record(self):
        offer = build_confirmation_offer(_close_intent())
        assert offer is not None
        assert offer.question == "Close issue #108? (yes/no)"
        record = offer.offer
        # The documented generic-carrier shape (module docstring):
        assert record["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        pa = record["pending_action"]
        assert pa["action"] == "close_issue_query"
        assert isinstance(pa["intent"], Intent)
        assert pa["intent"].context["original_message"] == "close issue #108"
        assert pa["summary"] == "close issue #108"
        assert "won't close issue #108" in record["decline_message"]

    def test_title_included_only_when_already_on_the_path(self):
        """#1190 spec: title only from a read ALREADY available (no new call).
        No context title → number-only question; stashed title → included."""
        bare = build_confirmation_offer(_close_intent())
        assert "'" not in bare.question
        titled = build_confirmation_offer(
            _close_intent(context={"issue_title": "Login button unresponsive"})
        )
        assert titled.question == (
            "Close issue #108 'Login button unresponsive'? (yes/no)"
        )

    def test_reopen_question(self):
        intent = _close_intent(
            message="reopen issue #42", action="reopen_issue_query"
        )
        offer = build_confirmation_offer(intent)
        assert offer.question == "Reopen issue #42? (yes/no)"

    def test_no_issue_number_passes_through(self):
        """Close/reopen with no parseable number is the verified read-only
        clarification shape — the gate defers to the handler's 'which
        issue?' turn instead of confirming an unnamed blast radius."""
        intent = _close_intent(message="close the login bug")
        assert build_confirmation_offer(intent) is None

    def test_unknown_destructive_action_always_defers(self):
        """Safe default for future tier members (generic carrier): an
        unconfirmed destructive write must never fire, even before a
        per-action summary exists."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="purge_archive",
            context={"original_message": "purge the archive"},
        )
        offer = build_confirmation_offer(intent)
        assert offer is not None
        assert "(yes/no)" in offer.question
        assert offer.offer["pending_action"]["action"] == "purge_archive"

    @pytest.mark.parametrize(
        "message", ["cancel", "stop", "forget it", "Never mind.", "abort", "STOP IT"]
    )
    def test_bare_exit_commands_detected(self, message):
        assert detect_bare_exit(message) is True

    @pytest.mark.parametrize("message", ["yes", "close it", "what about #109?"])
    def test_non_exits_not_detected(self, message):
        assert detect_bare_exit(message) is False


class TestConfirmEntryPoint:
    """Part 2 machinery: 'yes' executes the ORIGINAL handler path with the
    ORIGINAL resolved parameters via the existing dispatch rail — never a
    re-classification of the 'yes'."""

    class _StubIntentService:
        def __init__(self):
            self.calls = []

        async def _handle_close_issue_query(self, intent, workflow_id, session_id=None):
            self.calls.append((intent, workflow_id))
            result = AsyncMock()
            result.message = "Closed issue #108: Test"
            result.intent_data = {"action": "close_issue_query"}
            return result

    @pytest.mark.asyncio
    async def test_confirmed_dispatch_runs_original_action_with_original_intent(self):
        register_default_workflows()
        stub = self._StubIntentService()
        original = _close_intent()
        result = await run_confirm_pending_action_workflow(
            session_id="sess-1190",
            user_id=_USER,
            context={
                "pending_action": {
                    "action": "close_issue_query",
                    "intent": original,
                    "summary": "close issue #108",
                },
                "intent_service": stub,
            },
        )
        assert len(stub.calls) == 1
        called_intent, workflow_id = stub.calls[0]
        assert called_intent is original  # ORIGINAL params, no re-resolution
        assert workflow_id is None
        # The confirmed marker lets the handler's #902 in-message check
        # execute in one turn instead of re-asking.
        assert called_intent.context["destructive_confirmed"] is True
        # Acceptance-seam shape: {"message", "intent_data"}.
        assert result["message"] == "Closed issue #108: Test"
        assert result["intent_data"] == {"action": "close_issue_query"}

    @pytest.mark.asyncio
    async def test_missing_context_returns_none_never_fires(self):
        assert await run_confirm_pending_action_workflow(
            session_id="s", context={}
        ) is None
        assert await run_confirm_pending_action_workflow(
            session_id="s", context={"pending_action": {}, "intent_service": object()}
        ) is None

    def test_confirm_workflow_is_not_rail_reachable(self):
        """action_triggered=False: a classifier emission can never fire the
        deferred-action executor directly."""
        register_default_workflows()
        assert CONFIRM_PENDING_ACTION_WORKFLOW not in get_action_workflows()


# ---------------------------------------------------------------------------
# End-to-end through the REAL process_intent (the #1411-test idiom)
# ---------------------------------------------------------------------------


def _explosive_router(monkeypatch, allow_update=False, update_result=None):
    """Mock at the GitHub-router boundary. Everything explosive except what a
    given turn legitimately needs; update_issue is THE write under test."""
    from services.integrations.github.github_integration_router import (
        GitHubIntegrationRouter,
    )

    async def _noop_init(self, user_id=None):
        return None

    async def _available(self):
        return True

    async def _explosive_get_issue(self, *a, **k):
        raise AssertionError(
            "github_router.get_issue called — the confirmation turn must not "
            "issue new reads, and a confirmed close skips the #902 preview"
        )

    monkeypatch.setattr(GitHubIntegrationRouter, "initialize", _noop_init)
    monkeypatch.setattr(GitHubIntegrationRouter, "is_available", _available)
    monkeypatch.setattr(GitHubIntegrationRouter, "get_issue", _explosive_get_issue)

    if allow_update:
        update_mock = AsyncMock(
            return_value=update_result
            or {"title": "Test issue", "html_url": "https://github.com/x/y/issues/108"}
        )
        monkeypatch.setattr(GitHubIntegrationRouter, "update_issue", update_mock)
        return update_mock

    async def _explosive_update(self, *a, **k):
        raise AssertionError(
            "github_router.update_issue FIRED — a destructive mutation "
            "executed without a confirmed yes (#1190 gate breach)"
        )

    monkeypatch.setattr(GitHubIntegrationRouter, "update_issue", _explosive_update)
    return None


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


class TestEndToEndConfirmationTurn:
    pytestmark = pytest.mark.asyncio

    async def test_close_issue_defers_asks_and_stores_pending_action(
        self, live_service, monkeypatch
    ):
        """RED before the gate: 'close issue #108' reached the handler (the
        explosive get_issue blew on the #902 preview fetch). GREEN: no GitHub
        call of any kind, one clear question, pending action stored."""
        _explosive_router(monkeypatch, allow_update=False)
        sid = "e2e-1190-confirm"
        result = await live_service.process_intent(
            message="close issue #108", session_id=sid, user_id=_USER
        )
        assert "#108" in result.message
        assert "(yes/no)" in result.message
        assert result.intent_data.get("destructive_confirmation_pending") is True
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert stored["pending_action"]["action"] in CLOSE_ALIASES

    async def test_yes_fires_the_write_with_original_params(
        self, live_service, monkeypatch
    ):
        """'yes' executes the stored action — original issue number, original
        handler path (github_router.update_issue(108, state='closed')) — and
        never re-classifies (explosive LLM carries the turn). The explosive
        get_issue also pins single-turn execution: a confirmed close must not
        re-ask #902's preview question."""
        _explosive_router(monkeypatch, allow_update=False)
        sid = "e2e-1190-yes"
        await live_service.process_intent(
            message="close issue #108", session_id=sid, user_id=_USER
        )
        update_mock = _explosive_router(monkeypatch, allow_update=True)

        # #1529 ordering: the pending offer must claim the turn before the
        # resume check can — make any resume-check touch explosive.
        async def _explosive_resume(*a, **k):
            raise AssertionError(
                "_check_pending_resume_offer reached — pending offer must "
                "bind the affirmative first (#1529 ordering)"
            )

        monkeypatch.setattr(
            live_service, "_check_pending_resume_offer", _explosive_resume
        )

        result = await live_service.process_intent(
            message="yes", session_id=sid, user_id=_USER
        )
        update_mock.assert_awaited_once_with(108, state="closed")
        assert "Closed issue #108" in result.message
        assert _pending_offers(live_service).get(sid) is None  # consumed

    async def test_no_cancels_honestly_and_nothing_fires(
        self, live_service, monkeypatch
    ):
        _explosive_router(monkeypatch, allow_update=False)
        sid = "e2e-1190-no"
        await live_service.process_intent(
            message="close issue #108", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message="no", session_id=sid, user_id=_USER
        )
        assert "won't close issue #108" in result.message
        assert "Nothing has been changed" in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_bare_cancel_declines_via_escape_tier(
        self, live_service, monkeypatch
    ):
        """#1529 exit tier at the offer seam: a bare 'cancel' (not in the
        soft-offer DECLINE_PATTERNS) still cancels honestly instead of
        silently dropping the offer."""
        _explosive_router(monkeypatch, allow_update=False)
        sid = "e2e-1190-cancel"
        await live_service.process_intent(
            message="close issue #108", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message="cancel", session_id=sid, user_id=_USER
        )
        assert "won't close issue #108" in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_off_intent_abandons_and_new_request_gets_fresh_confirmation(
        self, live_service, monkeypatch
    ):
        """Off-intent next turn (#1529 off_intent tier): the pending #108
        action is cancelled by the pop — and the new message is processed
        normally. Using 'close issue #109' as the off-intent message pins
        both halves: the stored action is REPLACED (never merged), and a
        later 'yes' fires 109, not 108."""
        _explosive_router(monkeypatch, allow_update=False)
        sid = "e2e-1190-offintent"
        await live_service.process_intent(
            message="close issue #108", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message="close issue #109", session_id=sid, user_id=_USER
        )
        assert "#109" in result.message and "(yes/no)" in result.message
        stored = _pending_offers(live_service).get(sid)
        assert "#109" in stored["pending_action"]["summary"]
        assert "#108" not in stored["pending_action"]["summary"]

        update_mock = _explosive_router(monkeypatch, allow_update=True)
        await live_service.process_intent(
            message="yes", session_id=sid, user_id=_USER
        )
        update_mock.assert_awaited_once_with(109, state="closed")

    async def test_long_prose_reply_neither_fires_nor_declines_1631(
        self, live_service, monkeypatch
    ):
        """#1631: a long free-text reply to an armed destructive confirm must
        not be claimed by the greedy accept row ("Please …" prefix) or the
        unanchored decline row ("not today" substring). RED pre-fix: the
        accept-greed prose ACCEPTED the confirm and update_issue fired; the
        decline-greed prose returned the honest-cancel copy. GREEN: prose is
        the off-intent tier — the pop cancels the pending action, nothing
        fires, and the turn falls through to normal processing (here the
        explosive LLM boundary, proving no offer seam claimed it)."""
        cases = (
            (
                "accept-greed",
                "Please note that we should not close this yet, not today "
                "anyway, because the migration is still running and three "
                "boards reference this issue while it stays open — let's "
                "revisit once the cutover is verified and announced.",
            ),
            (
                "decline-greed",
                "The migration is still running so I would rather we leave "
                "it alone, not today at least — three boards reference this "
                "issue and closing it would break them; we can revisit after "
                "the cutover is verified and announced to the team.",
            ),
        )
        for label, prose in cases:
            assert len(prose) >= 160 and "\n" not in prose, label
            update_mock = _explosive_router(monkeypatch, allow_update=True)
            sid = f"e2e-1631-{label}"
            await live_service.process_intent(
                message="close issue #108", session_id=sid, user_id=_USER
            )
            try:
                result = await live_service.process_intent(
                    message=prose, session_id=sid, user_id=_USER
                )
                # However the prose turn resolves downstream, it must not be
                # the decline copy — declining was never what the user said.
                assert "won't close issue #108" not in result.message, label
            except IntentProcessingError as exc:
                # Off-intent fell through to normal classification and hit
                # the explosive LLM boundary (which the classifier wraps as
                # INTENT_CLASSIFICATION_FAILED) — exactly the point: neither
                # accept nor decline claimed the turn at the offer seam.
                assert (
                    "LLM boundary touched" in str(exc)
                    or "INTENT_CLASSIFICATION_FAILED" in str(exc)
                ), (label, str(exc))
            update_mock.assert_not_awaited()  # the write never fired
            assert _pending_offers(live_service).get(sid) is None  # popped

    async def test_reopen_defers_then_fires_open_state(
        self, live_service, monkeypatch
    ):
        _explosive_router(monkeypatch, allow_update=False)
        sid = "e2e-1190-reopen"
        result = await live_service.process_intent(
            message="reopen issue #42", session_id=sid, user_id=_USER
        )
        assert "#42" in result.message and "(yes/no)" in result.message
        update_mock = _explosive_router(monkeypatch, allow_update=True)
        await live_service.process_intent(
            message="yes", session_id=sid, user_id=_USER
        )
        update_mock.assert_awaited_once_with(42, state="open")
