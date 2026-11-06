"""#2069, Arch's condition (2026-10-16 21:28): the consent line names the
project from the SAME source the handler writes from.

Before: ``consent_gate._summary_for`` named an add's target with
``display_name_for`` → the #1856 extractor (the add regex), while the
handler took the router's ``name`` first. On a router-args turn the check
would read "add project Baz with description testing the description" and
the row would be "Baz".

After: one resolver, ``portfolio_service.resolve_add_project_slots`` (the
router's honesty-guarded ``name`` first, the extractor as the fallback),
called by the handler AND by ``display_name_for`` (the consent line, the
#2057 question how-to, the adopted-category confirm).

Layer: the REAL ``_summary_for`` / ``build_consent_check_offer`` and the
REAL rail adapter ``run_add_project_workflow`` → ``_handle_add_project`` →
``_create_or_report_project`` with the DB session and repositories faked
(the created row echoes what was written). No LLM: the router's args are
supplied as the ``inversion_args`` the live consult writes onto the Intent.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from services.intent_service import consent_gate
from services.intent_service import workflow_entries as we
from services.intent_service.adopted_category_reads_only import (
    display_name_for,
    question_how_to,
)
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.onboarding.portfolio_service import resolve_add_project_slots
from services.shared_types import EffectClass

BAZ = "Add a project called Baz with description testing the description"
BAZ_ARGS = {"name": "Baz", "description": "testing the description"}


class _FakeScope:
    async def __aenter__(self):
        return SimpleNamespace()

    async def __aexit__(self, *exc):
        return False


def _intent(message, router_args=None):
    ctx = {"original_message": message}
    if router_args is not None:
        ctx["inversion_args"] = router_args
    return SimpleNamespace(action="add_project", context=ctx, original_message=message)


async def _stored_name(intent) -> str:
    """Run the add through the rail adapter; return the stored row's name."""
    from services.database.repositories import ProjectRepository
    from services.database.session_factory import AsyncSessionFactory

    rows = []

    async def _create(_self, **kwargs):
        row = SimpleNamespace(
            id="proj-2069c", name=kwargs.get("name"), description=kwargs.get("description")
        )
        rows.append(row)
        return row

    async def _find_by_name(_self, **kwargs):
        return None

    async def _link(_self, repo_repo, repo_name, project_id, user_id):
        return True, ""

    svc = SimpleNamespace(
        canonical_handlers=CanonicalHandlers(),
        _is_generic_canonical_response=lambda *a, **k: False,
        _arm_write_offer=lambda *a, **k: None,
        _track_offer_hint=lambda *a, **k: None,
    )
    with contextlib.ExitStack() as stack:
        stack.enter_context(
            patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope()))
        )
        stack.enter_context(patch.object(ProjectRepository, "create", _create))
        stack.enter_context(patch.object(ProjectRepository, "find_by_name", _find_by_name))
        stack.enter_context(patch.object(CanonicalHandlers, "_link_repo_to_new_project", _link))
        await we.run_add_project_workflow(
            "s-2069c", "u-2069c", {"intent": intent, "intent_service": svc}
        )
    (row,) = rows
    return row.name


def _named_in_summary(intent) -> str:
    summary = consent_gate._summary_for(intent)
    assert summary.startswith("add project")
    return summary[len("add project") :].strip()


# ---------------------------------------------------------------------------
# The condition: on a router-args turn the consent line's name == stored name
# ---------------------------------------------------------------------------


class TestConsentLineNamesTheStoredName:
    @pytest.mark.asyncio
    async def test_router_args_turn_consent_name_equals_stored_name(self):
        intent = _intent(BAZ, BAZ_ARGS)
        named = _named_in_summary(intent)
        stored = await _stored_name(intent)
        assert named == stored == "Baz"

    @pytest.mark.asyncio
    async def test_the_check_question_asks_about_baz_not_the_whole_tail(self):
        # #2304: the check asks in add_project's own words (CXO's existing confirm),
        # named by the same resolver. Was "...asking me to add project Baz, ...".
        from services.intent_service.write_confirm_words import (
            WriteAskRequest,
            add_project_write_ask,
        )

        intent = _intent(BAZ, BAZ_ARGS)
        ask = await add_project_write_ask(WriteAskRequest(intent=intent, message=BAZ))
        offer = consent_gate.build_consent_check_offer(intent, ask.words)
        assert offer.question.startswith('Add a project called "Baz"? (yes/no)')
        assert "with description" not in offer.question
        assert offer.offer["pending_action"]["summary"] == 'add a project called "Baz"'
        assert offer.offer["decline_message"].startswith(
            'Okay — I won\'t add a project called "Baz".'
        )

    @pytest.mark.asyncio
    async def test_router_name_with_repo_clause_matches(self):
        msg = "add project Baz with repo octo/baz"
        intent = _intent(msg, {"name": "Baz", "repo": "octo/baz"})
        assert _named_in_summary(intent) == await _stored_name(intent) == "Baz"

    @pytest.mark.asyncio
    async def test_no_router_args_both_fall_back_to_the_extractor(self):
        # The fallback is the same on both sides: whatever the extractor
        # yields is named AND stored (no "with description" regex added).
        intent = _intent(BAZ)
        named = _named_in_summary(intent)
        stored = await _stored_name(intent)
        assert named == stored == "Baz with description testing the description"

    @pytest.mark.asyncio
    async def test_invented_router_name_both_fall_back_to_the_extractor(self):
        intent = _intent("Add a project called Bar", {"name": "Quux"})
        named = _named_in_summary(intent)
        stored = await _stored_name(intent)
        assert named == stored == "Bar"

    @pytest.mark.asyncio
    async def test_plain_turn_unchanged(self):
        intent = _intent("add a project called Baz", {"name": "Baz"})
        assert _named_in_summary(intent) == await _stored_name(intent) == "Baz"


# ---------------------------------------------------------------------------
# The one resolver
# ---------------------------------------------------------------------------


class TestResolver:
    def test_router_name_first(self):
        slots = resolve_add_project_slots(BAZ, BAZ_ARGS)
        assert slots == {
            "name": "Baz",
            "repo": None,
            "description": "testing the description",
            "description_asked": True,
            "source": "router",
        }

    def test_extractor_fallback_stores_no_description(self):
        slots = resolve_add_project_slots(BAZ, None)
        assert slots["source"] == "extractor"
        assert slots["name"] == "Baz with description testing the description"
        assert slots["description"] is None
        assert slots["description_asked"] is False

    def test_rejected_router_name_keeps_description_asked_for_the_honest_line(self):
        slots = resolve_add_project_slots(
            "Add a project called Bar", {"name": "Quux", "description": "x y"}
        )
        assert slots["source"] == "extractor"
        assert slots["name"] == "Bar"
        assert slots["description"] is None
        assert slots["description_asked"] is True

    def test_router_name_without_repo_keeps_the_utterance_repo_clause(self):
        slots = resolve_add_project_slots("add project Baz with repo octo/baz", {"name": "Baz"})
        assert (slots["name"], slots["repo"], slots["source"]) == ("Baz", "octo/baz", "router")

    def test_handler_delegate_is_the_same_guard(self):
        assert CanonicalHandlers._router_add_project_args(BAZ_ARGS, BAZ)["name"] == "Baz"

    def test_display_name_for_uses_the_resolver(self):
        assert display_name_for("add", BAZ, BAZ_ARGS) == "Baz"
        assert display_name_for("add", BAZ) == "Baz with description testing the description"

    def test_question_how_to_uses_the_resolver(self):
        line = question_how_to("add_project", BAZ, BAZ_ARGS)
        assert line is not None and "Baz" in line and "with description" not in line
