"""#1571 — the drafted-issue pending binding (PM live 2026-08-10 + 2026-08-15).

PM's transcript, repro'd live in the 2026-08-15 baseline:

1. The compose flow builds a complete draft; PM: **"Please file it as is"** →
   double-confirm friction ("want me to go ahead?") instead of filing.
2. The floor then FABRICATED success with the template showing: *"Filed!
   Here's what I created… #[issue number]"* — a literal placeholder in
   user-facing copy (self-caught in the same message, but post-hoc means it
   shipped to PM's eyes first).
3. The suggested retry LOST the entire draft ("What should the issue be
   about?").

The fix, at the seam #1190 named for it (destructive_confirm.py's generic
``pending_action`` carrier — "#1571 tracks the named next consumer"):

- The #1510 collaborate turn ARMS a pending action (kind ``drafted_issue``)
  binding the draft.
- "file it" / "file it as is" IS the confirmation — one turn, no second ask;
  acceptance re-dispatches the ORIGINAL intent through the real create rail
  (the #1190 acceptance mirror) with the confirmed marker, which the
  collaborate gate honors as consent-already-given.
- Success copy derives from the ACTUAL tool result (real number).
- Failure keeps the draft bound (re-armed) — retry does not lose it.
- Off-intent abandons per the carrier's rules; declines drop honestly.
- The placeholder-literal CLASS is killed renderer-side: a hash-bracket slot
  in floor output (``#[issue number]``) is machinery grammar, replaced with
  deterministic honesty (``strip_placeholder_slots``).

Layer honesty (m-43): the end-to-end classes drive the REAL
``IntentService.process_intent`` for the confirmation turns (which resolve at
the pending-offer seam, before classification — explosive LLM proves it);
the arming turn drives ``_handle_create_issue`` directly (the compose ask's
classification is LLM-lane, out of scope here — the #1510 suite owns the
gate's reachability).
"""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
    CONFIRMED_CONTEXT_KEY,
)
from services.intent_service.drafted_issue import (
    DRAFTED_ISSUE_KIND,
    build_drafted_issue_offer,
    detect_file_command,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

GATE = "services.intent_service.collaboration_gate"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
RESOLVER = "services.integrations.github.repo_resolver.get_user_default_repo"

# PM's compose shape (the #1510 Jake shape) and PM's verbatim file command.
COMPOSE_ASK = "help me write a ticket about the login timeout on mobile"
PM_FILE_AS_IS = "Please file it as is"

_USER = "3f7b8a52-1571-4b00-9e00-000000001571"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. The
    confirmation turns must resolve at the pending-offer seam, before
    classification — the live theft happened because nothing bound them."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1571 confirmation turns must "
            "resolve deterministically at the offer seam"
        )


def _compose_intent(message=COMPOSE_ASK, action="create_ticket"):
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=0.95,
        original_message=message,
        context={},
    )


# ---------------------------------------------------------------------------
# 1. The file-command detector (deterministic, pure)
# ---------------------------------------------------------------------------


class TestDetectFileCommand:
    @pytest.mark.parametrize(
        "message",
        [
            "file it",
            "file it as is",
            "file it as-is",
            "Please file it as is",
            "please file it as is.",
            "create it",
            "submit it",
            "open it",
            "go ahead and file it",
            "file this",
            "file the issue",
            "create the ticket as is",
            "file the draft",
            "file it, please",
        ],
    )
    def test_file_commands_match(self, message):
        assert detect_file_command(message) is not None

    def test_incident_phrase_with_repo_binds_and_captures_repo(self):
        """The ORIGINAL #1571 phrase — 'file it in owner/repo' — with a draft
        pending is unambiguous: accept, with the named repo overriding."""
        cmd = detect_file_command("file it in mediajunkie/test-piper-morgan")
        assert cmd is not None
        assert cmd["repo"] == "mediajunkie/test-piper-morgan"

    def test_plain_command_has_no_repo_override(self):
        assert detect_file_command("file it as is")["repo"] is None

    @pytest.mark.parametrize(
        "message",
        [
            "file an issue about flaky tests",  # NEW ask, not this draft
            "create an issue in owner/repo about testing",  # canonical NEW ask
            "what should I file it under?",
            "can you file it later if I forget",
            "profile it",
            "no",
            "yes",  # generic accept is the offer seam's business, not this detector's
            "",
        ],
    )
    def test_non_file_commands_do_not_match(self, message):
        assert detect_file_command(message) is None


# ---------------------------------------------------------------------------
# 2. The offer record (the documented generic-carrier shape)
# ---------------------------------------------------------------------------


class TestDraftedIssueOffer:
    def test_record_shape_rides_the_1190_carrier(self):
        intent = _compose_intent()
        offer = build_drafted_issue_offer(
            intent, subject="login timeout on mobile", repository="acme/widgets"
        )
        assert offer["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        pa = offer["pending_action"]
        assert pa["kind"] == DRAFTED_ISSUE_KIND
        assert pa["action"] == "create_ticket"
        assert pa["intent"] is intent
        assert pa["draft"] == {
            "title": "login timeout on mobile",
            "repository": "acme/widgets",
        }
        assert "login timeout on mobile" in pa["summary"]
        # The decline copy is honest about what did NOT happen.
        assert "Nothing was filed" in offer["decline_message"]


# ---------------------------------------------------------------------------
# 3. The collaborate turn ARMS the binding
# ---------------------------------------------------------------------------


@pytest.fixture
def svc():
    register_default_workflows()
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


class TestCollaborateTurnArmsBinding:
    pytestmark = pytest.mark.asyncio

    async def test_draft_turn_stores_drafted_issue_pending_action(self, svc):
        sid = "sess-1571-arm"
        intent = _compose_intent()
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            result = await svc._handle_create_issue(intent, "wf-1", sid, user_id=_USER)

        w.assert_not_awaited()
        assert result.intent_data.get("collaboration_gate") is True
        # The clobber-guard flag (the #1605 belt) is set…
        assert result.intent_data.get("drafted_issue_pending") is True
        # …and the store holds the drafted_issue record for this session.
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == DRAFTED_ISSUE_KIND
        assert "login timeout on mobile" in stored["pending_action"]["draft"]["title"]
        # The copy teaches the phrase that NOW ROUTES — never the unbound lie.
        assert "file it as is" in result.message

    async def test_no_subject_draft_arms_subjectless_but_teaches_no_file_phrase(
        self, svc
    ):
        """PIN FLIPPED BY #1630 (this test used to assert no-subject = no
        arm). A subjectless ask now arms the minimal SUBJECTLESS carrier so
        the #1627 hold covers the "What's it about?" answer — the unarmed
        opening was the exact theft shape, one turn earlier. What #1571
        still requires: the copy must not teach 'file it as is' while the
        draft has no content (teaching a phrase with nothing behind it was
        #1571's original defect)."""
        sid = "sess-1571-nosubj"
        intent = _compose_intent("help me write a ticket")
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()),
        ):
            result = await svc._handle_create_issue(intent, "wf-1", sid, user_id=_USER)
        assert result.intent_data.get("drafted_issue_pending") is True
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == DRAFTED_ISSUE_KIND
        assert stored["pending_action"]["draft"].get("title") is None
        assert "file it as is" not in result.message
        assert "What's it about?" in result.message

    async def test_confirmed_redispatch_skips_the_gate(self, svc):
        """The acceptance re-dispatch carries CONFIRMED_CONTEXT_KEY — the
        compose-framed original message must NOT re-trigger the collaborate
        gate (the double-confirm friction, killed at its root)."""
        intent = _compose_intent()
        intent.context[CONFIRMED_CONTEXT_KEY] = True
        created = {"number": 123, "html_url": "https://x/123", "title": "t"}
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            result = await svc._handle_create_issue(
                intent, "wf-1", "sess-1571-conf", user_id=_USER
            )
        w.assert_awaited_once()
        assert "#123" in result.message


# ---------------------------------------------------------------------------
# 4. End-to-end: PM's transcript sequence through the REAL process_intent
# ---------------------------------------------------------------------------


async def _arm_draft(svc, sid):
    """Turn 1 (the compose/draft turn) at the handler seam — arms the binding."""
    intent = _compose_intent()
    with (
        patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.create_issue", new=AsyncMock()),
    ):
        return await svc._handle_create_issue(intent, "wf-1", sid, user_id=_USER)


class TestPmTranscriptEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def test_file_it_as_is_files_in_one_confirmation_with_real_number(
        self, svc
    ):
        """PM's sequence, fixed: draft → "Please file it as is" → the REAL
        create fires in ONE turn, and the success copy carries the ACTUAL
        issue number from the tool result — no second ask, no placeholder,
        no re-classification (explosive LLM carries the turn)."""
        sid = "e2e-1571-file"
        await _arm_draft(svc, sid)

        created = {
            "number": 123,
            "html_url": "https://github.com/acme/widgets/issues/123",
            "title": "login timeout on mobile",
        }
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            result = await svc.process_intent(
                message=PM_FILE_AS_IS, session_id=sid, user_id=_USER
            )

        w.assert_awaited_once()  # ONE confirmation → the write fired
        # Success copy derives from the actual tool result:
        assert "#123" in result.message
        assert result.intent_data.get("issue_number") == 123
        # Never a template slot, never a re-ask:
        assert "#[" not in result.message
        assert "(yes/no)" not in result.message
        assert "want me to go ahead" not in result.message.lower()
        # The binding is consumed — nothing pending afterward.
        assert _pending_offers(svc) == {}

    async def test_bare_file_it_also_confirms(self, svc):
        """'file it' — the phrase the generic accept detector does NOT know —
        is exactly why the kind-specific seam exists."""
        sid = "e2e-1571-bare"
        await _arm_draft(svc, sid)
        created = {"number": 7, "html_url": "https://x/7", "title": "t"}
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            result = await svc.process_intent(
                message="file it", session_id=sid, user_id=_USER
            )
        w.assert_awaited_once()
        assert "#7" in result.message

    async def test_create_failure_keeps_the_draft_bound_and_retry_works(self, svc):
        """PM's loss, fixed: the create FAILS → honest error, draft still
        bound; the retry files it — never "What should the issue be about?"."""
        sid = "e2e-1571-retry"
        await _arm_draft(svc, sid)

        # Attempt 1: the router blows up.
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(
                f"{ROUTER}.create_issue",
                new=AsyncMock(side_effect=RuntimeError("boom")),
            ),
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            r1 = await svc.process_intent(
                message=PM_FILE_AS_IS, session_id=sid, user_id=_USER
            )

        # Honest: no fabricated success, no placeholder, and the draft LIVES.
        assert "#[" not in r1.message
        assert "Filed!" not in r1.message
        assert "draft" in r1.message.lower()
        assert r1.intent_data.get("drafted_issue_retained") is True
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == DRAFTED_ISSUE_KIND
        # The amnesia line PM hit is exactly what must NOT happen:
        assert "What should the issue be about" not in r1.message

        # Attempt 2: retry files the SAME draft.
        created = {"number": 124, "html_url": "https://x/124", "title": "t"}
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            r2 = await svc.process_intent(
                message="file it", session_id=sid, user_id=_USER
            )
        w.assert_awaited_once()
        assert "#124" in r2.message
        assert _pending_offers(svc) == {}

    async def test_unverified_outcome_also_retains_the_draft(self, svc):
        """A rail answer that did not verifiably create (degraded-connector
        copy) passes through honestly WITH the draft retained."""
        sid = "e2e-1571-degraded"
        await _arm_draft(svc, sid)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=False)),
        ):
            r = await svc.process_intent(
                message=PM_FILE_AS_IS, session_id=sid, user_id=_USER
            )
        assert r.intent_data.get("issue_number") is None
        assert r.intent_data.get("drafted_issue_retained") is True
        assert len(_pending_offers(svc)) == 1

    async def test_off_intent_abandons_and_the_turn_routes_normally(self, svc):
        """The carrier's rules: a different intent abandons the binding (the
        pop already removed it) and routes as its own turn — here the
        deterministic close route, which arms ITS OWN confirmation. Also the
        property the #1509 Jake pin relies on: an explicit imperative after
        the draft turn is never captured by the binding."""
        sid = "e2e-1571-offintent"
        await _arm_draft(svc, sid)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(
                message="close issue #108", session_id=sid, user_id=_USER
            )
        w.assert_not_awaited()  # the draft did NOT file
        # The turn routed normally: the #1190 close confirmation claimed it.
        assert "(yes/no)" in r.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"].get("kind") != DRAFTED_ISSUE_KIND

    async def test_decline_drops_the_draft_honestly(self, svc):
        sid = "e2e-1571-decline"
        await _arm_draft(svc, sid)
        with patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})):
            r = await svc.process_intent(message="no", session_id=sid, user_id=_USER)
        assert "Nothing was filed" in r.message
        assert _pending_offers(svc) == {}

    async def test_repo_override_in_file_command(self, svc):
        """'file it in owner/repo' — the original incident phrase — files the
        bound draft in the NAMED repo (no default-repo resolution needed)."""
        sid = "e2e-1571-repo"
        await _arm_draft(svc, sid)
        created = {"number": 9, "html_url": "https://x/9", "title": "t"}
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
        ):
            r = await svc.process_intent(
                message="file it in mediajunkie/test-piper-morgan",
                session_id=sid,
                user_id=_USER,
            )
        w.assert_awaited_once()
        _, kwargs = w.await_args
        assert kwargs.get("owner") == "mediajunkie"
        assert kwargs.get("repo_name") == "test-piper-morgan"
        assert "#9" in r.message


# ---------------------------------------------------------------------------
# 5. The placeholder-literal class is unrenderable (renderer-side kill)
# ---------------------------------------------------------------------------


class TestPlaceholderSlotScrub:
    def test_pm_verbatim_placeholder_is_replaced_with_honesty(self):
        from services.intent_service.conversational_floor import (
            strip_placeholder_slots,
        )

        fabricated = "Filed! Here's what I created… #[issue number]"
        clean, n = strip_placeholder_slots(fabricated)
        assert n == 1
        assert "#[" not in clean
        assert "unconfirmed" in clean
        assert "don't have a tool result" in clean

    def test_real_references_and_markdown_pass_untouched(self):
        from services.intent_service.conversational_floor import (
            strip_placeholder_slots,
        )

        legit = (
            "Created issue #123 in widgets — see [the issue](https://x/123). "
            "Checklist:\n- [ ] triage\n- [x] repro"
        )
        clean, n = strip_placeholder_slots(legit)
        assert n == 0
        assert clean == legit

    def test_slot_variants_are_all_caught(self):
        from services.intent_service.conversational_floor import (
            strip_placeholder_slots,
        )

        for slot in ("#[number]", "#[issue-number]", "#[ISSUE NUMBER]", "#[url]"):
            clean, n = strip_placeholder_slots(f"Done — {slot}")
            assert n == 1, slot
            assert "#[" not in clean
