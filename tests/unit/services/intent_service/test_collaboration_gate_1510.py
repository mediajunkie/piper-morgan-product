"""#1510 FTUX-TRUST — compose vs. execute: collaborate-first default (UNGATED half).

PM's spec (2026-08-07, verbatim): "It clearly does not involve writing out
anywhere by default. Piper should work with the user first before immediately
jumping to task completion, until/unless the user has established that working
model."

Layer verdict this build rests on (traced 2026-08-09, prog):
- Understanding CANNOT express compose-vs-execute: the classifier prompt
  (services/intent_service/prompts.py) has no compose-side action name — its
  only ticket teachings are "create a ticket for the login bug" ->
  execution/create_ticket (line 252) and "how do I create a ticket?" ->
  GUIDANCE (line 249). "help me write a ticket about X" lands on
  create_ticket/create_issue because there is nothing else for it to land on.
- Acting then executes ANY classified write action unconditionally:
  create_ticket -> create_issue_entry (workflow_entries.py:551-556) ->
  _handle_create_issue -> github_router.create_issue, with no mode awareness.

The buildable half (per PPM unblock memo 2026-08-09) is the DECLARATION
SURFACE + collaborate-first action-layer gate, pinned here:

1. Framing: compose-phrased ("help me write...") vs execute-phrased
   (imperative "create/file/open...") vs ambiguous — deterministic.
2. Working mode: per-user, persisted in users.preferences JSONB (the existing
   DB-backed preference store — NOT the in-memory UserPreferenceManager).
   Default: COLLABORATE. Explicitly declarable ("just do things directly from
   now on") and revertible ("ask me first from now on").
3. Gate semantics: explicit framing wins both ways (compose always
   collaborates, imperative always executes); AMBIGUOUS is decided by the
   declared mode — collaborate-first by default. Mode-tied, not per-verb.
4. THE JAKE REPLAY: "help me write a ticket about X" from a user with no
   declared mode produces collaboration (draft + ask), not a created ticket.

Deliberately NOT here (blocked pending PM, per PPM memo): anything
inferential — counters, per-kind thresholds, trust decay, graduation.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent_service.collaboration_gate import (
    FRAMING_AMBIGUOUS,
    FRAMING_COMPOSE,
    FRAMING_EXECUTE,
    WORKING_MODE_PREF_KEY,
    WorkingMode,
    classify_framing,
    detect_mode_declaration,
    gate_holds,
    get_working_mode,
    set_working_mode,
)
from services.shared_types import IntentCategory

GATE = "services.intent_service.collaboration_gate"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
RESOLVER = "services.integrations.github.repo_resolver.get_user_default_repo"

JAKE = "help me write a ticket about the login timeout on mobile"


def _intent(message, action="create_ticket"):
    return Intent(
        original_message=message,
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=0.95,
        context={},  # what production actually delivers (#1220)
    )


@pytest.fixture
def svc():
    from services.intent.intent_service import IntentService

    return IntentService()


# ---------------------------------------------------------------------------
# 1. Framing classification (deterministic, pure)
# ---------------------------------------------------------------------------


class TestFramingClassification:
    def test_jake_shape_is_compose(self):
        assert classify_framing(JAKE) == FRAMING_COMPOSE

    def test_help_me_draft_is_compose(self):
        assert classify_framing("help me draft an issue for the checkout bug") == FRAMING_COMPOSE

    def test_lets_write_is_compose(self):
        assert classify_framing("let's write a ticket about the flaky tests") == FRAMING_COMPOSE

    def test_bare_draft_verb_is_compose(self):
        # Drafting is compose by definition — even imperative-shaped.
        assert classify_framing("draft a ticket about slow dashboards") == FRAMING_COMPOSE

    def test_imperative_create_is_execute(self):
        assert (
            classify_framing("create an issue in acme/widgets about testing regressions")
            == FRAMING_EXECUTE
        )

    def test_polite_imperative_is_execute(self):
        assert classify_framing("please file a ticket for the login bug") == FRAMING_EXECUTE

    def test_can_you_create_is_execute(self):
        assert classify_framing("can you create a ticket about the 500s") == FRAMING_EXECUTE

    def test_indirect_need_is_ambiguous(self):
        assert classify_framing("I need a ticket for the login bug") == FRAMING_AMBIGUOUS

    def test_empty_message_is_ambiguous(self):
        assert classify_framing("") == FRAMING_AMBIGUOUS


# ---------------------------------------------------------------------------
# 2. Mode declaration detection (the declaration surface, detection half)
# ---------------------------------------------------------------------------


class TestModeDeclarationDetection:
    def test_pm_verbatim_example_declares_execute(self):
        # PM's own example phrasing from the issue.
        assert detect_mode_declaration("just do things directly from now on") is WorkingMode.EXECUTE

    def test_dont_ask_going_forward_declares_execute(self):
        assert (
            detect_mode_declaration("going forward, don't ask — just do it")
            is WorkingMode.EXECUTE
        )

    def test_ask_me_first_reverts_to_collaborate(self):
        assert detect_mode_declaration("ask me first from now on") is WorkingMode.COLLABORATE

    def test_stop_doing_things_directly_reverts(self):
        assert (
            detect_mode_declaration("stop doing things directly from now on")
            is WorkingMode.COLLABORATE
        )

    def test_go_back_form_reverts_without_durative(self):
        assert (
            detect_mode_declaration("go back to checking with me before doing things")
            is WorkingMode.COLLABORATE
        )

    def test_one_off_imperative_is_not_a_declaration(self):
        # "just do it" without a durative marker is a one-off, not a mode change.
        assert detect_mode_declaration("just do it") is None

    def test_task_request_is_not_a_declaration(self):
        assert detect_mode_declaration("create a ticket about login") is None

    def test_jake_shape_is_not_a_declaration(self):
        assert detect_mode_declaration(JAKE) is None

    def test_empty_is_not_a_declaration(self):
        assert detect_mode_declaration("") is None
        assert detect_mode_declaration(None) is None


# ---------------------------------------------------------------------------
# 3. Working-mode persistence (users.preferences JSONB seam)
# ---------------------------------------------------------------------------


class TestWorkingModeStorage:
    pytestmark = pytest.mark.asyncio

    async def test_default_is_collaborate_when_unset(self):
        with patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})):
            assert await get_working_mode("u-1") is WorkingMode.COLLABORATE

    async def test_declared_execute_mode_is_read_back(self):
        with patch(
            f"{GATE}._load_preferences",
            new=AsyncMock(return_value={WORKING_MODE_PREF_KEY: "execute"}),
        ):
            assert await get_working_mode("u-1") is WorkingMode.EXECUTE

    async def test_garbage_stored_value_falls_back_to_collaborate(self):
        with patch(
            f"{GATE}._load_preferences",
            new=AsyncMock(return_value={WORKING_MODE_PREF_KEY: "yolo"}),
        ):
            assert await get_working_mode("u-1") is WorkingMode.COLLABORATE

    async def test_storage_error_fails_safe_to_collaborate(self):
        # Fail-safe direction matters: an error must never escalate to execute.
        with patch(
            f"{GATE}._load_preferences", new=AsyncMock(side_effect=RuntimeError("db down"))
        ):
            assert await get_working_mode("u-1") is WorkingMode.COLLABORATE

    async def test_anonymous_user_gets_collaborate(self):
        assert await get_working_mode(None) is WorkingMode.COLLABORATE

    async def test_set_writes_the_preference_key(self):
        save = AsyncMock(return_value=True)
        with patch(f"{GATE}._save_preference", new=save):
            assert await set_working_mode("u-1", WorkingMode.EXECUTE) is True
        save.assert_awaited_once_with("u-1", WORKING_MODE_PREF_KEY, "execute")

    async def test_set_without_user_id_reports_not_persisted(self):
        assert await set_working_mode(None, WorkingMode.EXECUTE) is False

    async def test_set_storage_error_reports_not_persisted(self):
        with patch(
            f"{GATE}._save_preference", new=AsyncMock(side_effect=RuntimeError("db down"))
        ):
            assert await set_working_mode("u-1", WorkingMode.EXECUTE) is False


# ---------------------------------------------------------------------------
# 4. Gate semantics (mode-tied, not per-verb)
# ---------------------------------------------------------------------------


class TestGateSemantics:
    pytestmark = pytest.mark.asyncio

    async def test_non_write_action_never_gates(self):
        assert await gate_holds("list_issues_query", JAKE, "u-1") is False

    async def test_compose_holds_without_touching_storage(self):
        loader = AsyncMock()
        with patch(f"{GATE}._load_preferences", new=loader):
            assert await gate_holds("create_ticket", JAKE, "u-1") is True
        loader.assert_not_awaited()

    async def test_imperative_passes_without_touching_storage(self):
        loader = AsyncMock()
        with patch(f"{GATE}._load_preferences", new=loader):
            assert (
                await gate_holds("create_issue", "create an issue about login bugs", "u-1")
                is False
            )
        loader.assert_not_awaited()

    async def test_ambiguous_holds_under_default_mode(self):
        with patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})):
            assert await gate_holds("create_ticket", "I need a ticket for the login bug", "u-1") is True

    async def test_ambiguous_passes_under_declared_execute_mode(self):
        with patch(
            f"{GATE}._load_preferences",
            new=AsyncMock(return_value={WORKING_MODE_PREF_KEY: "execute"}),
        ):
            assert (
                await gate_holds("create_ticket", "I need a ticket for the login bug", "u-1")
                is False
            )

    async def test_compose_still_collaborates_in_execute_mode(self):
        # An explicit ask for drafting help wins even after "just do things":
        # executing a request to HELP DRAFT is the Jake failure again.
        with patch(
            f"{GATE}._load_preferences",
            new=AsyncMock(return_value={WORKING_MODE_PREF_KEY: "execute"}),
        ):
            assert await gate_holds("create_ticket", JAKE, "u-1") is True


# ---------------------------------------------------------------------------
# 5. THE JAKE REPLAY (AC-4) — handler level, mocked GitHub router
# ---------------------------------------------------------------------------


class TestJakeReplay:
    pytestmark = pytest.mark.asyncio

    async def test_jake_shape_collaborates_instead_of_creating(self, svc):
        """'help me write a ticket about X', user with NO declared mode ->
        collaboration (draft + ask), and NO GitHub write fires."""
        user_id = str(uuid4())
        intent = _intent(JAKE)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1", user_id=user_id)

        w.assert_not_awaited()  # the crossed wire: this used to fire
        assert result.success is True
        assert result.requires_clarification is True
        assert result.clarification_type == "collaboration_draft"
        # It proposes a draft grounded in the request (the slot-filled subject)...
        assert "login timeout on mobile" in result.message
        # ...and asks, instead of announcing a completed write.
        assert "?" in result.message
        assert result.intent_data.get("collaboration_gate") is True

    async def test_jake_shape_executes_after_declared_execute_mode_if_imperative(self, svc):
        """The declared working model changes AMBIGUOUS escalation: same
        subject, indirect phrasing, execute-mode user -> the write fires."""
        user_id = str(uuid4())
        intent = _intent("I need a ticket about the login timeout on mobile in acme/widgets")
        created = {"number": 7, "html_url": "https://x/7", "title": "t"}
        with (
            patch(
                f"{GATE}._load_preferences",
                new=AsyncMock(return_value={WORKING_MODE_PREF_KEY: "execute"}),
            ),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1", user_id=user_id)
        assert result.success
        w.assert_awaited_once()

    async def test_ambiguous_shape_collaborates_by_default(self, svc):
        """Collaborate-first: the SAME indirect phrasing with no declared mode
        does NOT execute (AC-3)."""
        user_id = str(uuid4())
        intent = _intent("I need a ticket about the login timeout on mobile in acme/widgets")
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1", user_id=user_id)
        w.assert_not_awaited()
        assert result.requires_clarification is True

    async def test_explicit_imperative_still_executes_with_no_declared_mode(self, svc):
        """Zero-regression pin: today's execute-phrased shape keeps working —
        collaborate-first gates ambiguity, it does not confiscate imperatives."""
        intent = Intent(
            original_message="create an issue in acme/widgets about testing regressions",
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=0.95,
            context={},
        )
        created = {"number": 9, "html_url": "https://x/9", "title": "testing regressions"}
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1")
        assert result.success
        w.assert_awaited_once()


# ---------------------------------------------------------------------------
# 6. Declaration surface wiring (chat-reachable, pre-routing)
# ---------------------------------------------------------------------------


class TestDeclarationSurfaceWiring:
    pytestmark = pytest.mark.asyncio

    def _bare_service(self):
        from services.intent.intent_service import IntentService

        svc = IntentService.__new__(IntentService)
        svc.logger = MagicMock()
        return svc

    async def test_execute_declaration_is_caught_and_persisted(self):
        svc = self._bare_service()
        setter = AsyncMock(return_value=True)
        with patch(f"{GATE}.set_working_mode", new=setter):
            result = await svc._process_intent_internal(
                "just do things directly from now on",
                session_id="sess-1510",
                user_id="u-1510",
            )
        setter.assert_awaited_once_with("u-1510", WorkingMode.EXECUTE)
        assert result.success is True
        assert result.intent_data["action"] == "set_working_mode"
        assert result.intent_data["working_mode"] == "execute"

    async def test_revert_declaration_is_caught(self):
        svc = self._bare_service()
        setter = AsyncMock(return_value=True)
        with patch(f"{GATE}.set_working_mode", new=setter):
            result = await svc._process_intent_internal(
                "ask me first from now on", session_id="sess-1510", user_id="u-1510"
            )
        setter.assert_awaited_once_with("u-1510", WorkingMode.COLLABORATE)
        assert result.intent_data["working_mode"] == "collaborate"

    async def test_unpersisted_declaration_is_honest_about_it(self):
        svc = self._bare_service()
        with patch(f"{GATE}.set_working_mode", new=AsyncMock(return_value=False)):
            result = await svc._process_intent_internal(
                "just do things directly from now on",
                session_id="sess-1510",
                user_id="u-1510",
            )
        # No confabulated durability: the reply must flag the save failure.
        assert "couldn't save" in result.message
