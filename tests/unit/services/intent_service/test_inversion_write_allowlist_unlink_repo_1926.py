"""#1926 / #1595 Phase 3 unit 4 — the FOURTH named op flips through the
Inversion, and the SECOND DESTRUCTIVE one: ``unlink_repo``, via the same
#1677 allowlist mechanism ``link_repo``/``archive_project``/
``restore_project``/``add_project`` used (never a relaxed effect check,
never a ``flip_group``) — and the SECOND allowlisted DESTRUCTIVE entry after
``delete_todo``, per Arch's Q1 floor ruling (2026-09-25): "#1677's 'WRITE'
was never a categorical ceiling — extend the allowlist to a DESTRUCTIVE op,
individually verified, same as create_todo/create_reminder were."

Authority:
  - CXO's ruling on #1926 (mailboxes/lead/read/ruling-cxo-to-arch-lead-1926-
    unlink-confirms-via-destructive-gate-link-and-list-do-not-confirm-
    2026-10-03.md): five numbered constraints, verbatim acceptance criteria.
  - Arch's manage_repos split (mailboxes/lead/read/rule-arch-to-lead-cc-cxo-
    exec-phase3-rail-shapes-one-entry-per-effect-class-wave2-and-writes-
    2026-10-03.md §2): list [READ] / link [WRITE] / unlink [DESTRUCTIVE],
    plus the ONE additional DESTRUCTIVE build condition (confirm-prompt
    provenance), first applied to delete_todo and re-run here.

This unit is NOT flipped — no live-category or flag change. The rail entry
+ confirm machinery are built as inert infrastructure (CXO's ruling governs
what the entry must do once reachable, not the still-live, still-
unconfirmed "manage_repos" canonical dispatch).

⚠️ LAYER HONESTY (m-43): these are unit-layer tests against a real
``CanonicalHandlers``/``IntentService`` with the DB repository layer
patched (same mocking idiom as ``test_repo_management.py``, never a live
router or LLM call). They prove the confirm gate resolves-before-arming,
renders CXO's copy, and executes/declines correctly for a classified
``unlink_repo`` Intent — they do NOT prove the live router ever emits
``unlink_repo`` (it currently emits ``manage_repos``; this unit does not
change that).
"""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.destructive_confirm import (
    build_unlink_repo_confirmation,
    is_unlink_repo_action,
)
from services.intent_service.inversion_router import derive_routing_grammar
from services.intent_service.workflow_dispatcher import (
    FLIP_WRITE_ALLOWLIST,
    get_action_workflows,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass, IntentCategory, Outwardness

pytestmark = pytest.mark.unit

_USER = "3f7b8a52-1926-4b00-9e00-000000001926"  # valid UUID: survives principal parsing
_SESSION = "sess-1926-unlink-repo"
_REPO = "mediajunkie/piper-morgan"
_PROJECT = "Piper Morgan"
_MSG = f"unlink {_REPO} from {_PROJECT}"

# Patch paths — imports are local inside the hoisted methods, so we patch
# the source modules (same idiom as test_repo_management.py).
_PATCH_SESSION_FACTORY = "services.database.session_factory.AsyncSessionFactory"
_PATCH_PROJECT_REPO = "services.database.repositories.ProjectRepository"
_PATCH_REPO_REPO = "services.database.repositories.RepositoryRepository"


def _mock_session_factory():
    mock_session = AsyncMock()

    @asynccontextmanager
    async def _session_scope():
        yield mock_session

    mock_factory = MagicMock()
    mock_factory.session_scope = _session_scope
    return mock_factory


def _mock_project(name=_PROJECT, project_id="proj-1"):
    p = MagicMock()
    p.id = project_id
    p.name = name
    return p


def _mock_repo(full_name=_REPO, repo_id="repo-1"):
    r = MagicMock()
    r.id = repo_id
    r.full_name = full_name
    return r


def _mock_link(project_id="proj-1", is_primary=False):
    link = MagicMock()
    link.project_id = project_id
    link.is_primary = is_primary
    return link


def _make_intent(message: str = _MSG, action: str = "unlink_repo") -> Intent:
    return Intent(
        category=IntentCategory.PORTFOLIO,
        action=action,
        confidence=0.95,
        original_message=message,
        context={"original_message": message},
    )


@pytest.fixture(autouse=True)
def _rail_registered():
    register_default_workflows()


# ---------------------------------------------------------------------------
# 1. THE ENTRY — allowlisted, no flip_group, canonical name matches, DESTRUCTIVE
# ---------------------------------------------------------------------------


class TestEntryDeclaration:
    def test_allowlist_includes_unlink_repo(self):
        assert "unlink_repo" in FLIP_WRITE_ALLOWLIST

    def test_real_rail_unlink_repo_declares_the_key_and_no_group(self):
        """unlink_repo flips by NAME (or its registry category), never by a
        wave — no flip_group, so no group token sweeps a write in. Effect is
        DESTRUCTIVE, not WRITE."""
        wf = get_action_workflows()
        entry = wf["unlink_repo"]
        assert entry.flip_write_allowlist_key == "unlink_repo"
        assert entry.flip_group is None
        assert entry.effect == EffectClass.DESTRUCTIVE
        assert entry.outwardness == Outwardness.PRIVATE
        assert entry.action_triggered is True

    def test_no_alias_family(self):
        """Unlike delete_todo's alias family, unlink_repo has exactly one
        registered name — same shape as link_repo/archive_project/
        restore_project/add_project/set_default_repo."""
        wf = get_action_workflows()
        assert wf["unlink_repo"] is not wf.get("link_repo")

    def test_destructive_entry_still_needs_confirm(self):
        """The property the whole exercise turns on: DESTRUCTIVE derives
        needs_confirm True — a flipped unlink_repo turn must ARM a confirm,
        never execute in one turn the way the WRITE allowlist entries do."""
        wf = get_action_workflows()
        entry = wf["unlink_repo"]
        assert entry.needs_consent is True
        assert entry.needs_confirm is True

    def test_is_unlink_repo_action_is_a_single_member_family(self):
        """CXO's constraint 5 ('do not widen the destructive tier'): this
        predicate's family has exactly one member — no alias, and nothing
        resembling 'disconnect my GitHub' (an integration-level phrase, a
        different surface) is a member."""
        assert is_unlink_repo_action("unlink_repo") is True
        assert is_unlink_repo_action("disconnect_github") is False
        assert is_unlink_repo_action("manage_repos") is False
        assert is_unlink_repo_action(None) is False


class TestRouterChoiceSet:
    def test_unlink_repo_is_a_grammar_name(self):
        grammar = derive_routing_grammar()
        assert "unlink_repo" in set(grammar.names())


# ---------------------------------------------------------------------------
# 2. CXO's CONSTRAINT 1 — only unlink confirms; link and list do not
# ---------------------------------------------------------------------------


class TestOnlyUnlinkConfirms:
    def test_link_repo_and_list_repos_do_not_need_confirm(self):
        """The mechanism the ruling leans on: needs_confirm derives from
        EffectClass.DESTRUCTIVE alone. link_repo (WRITE) and list_repos
        (READ) never arm a confirm; unlink_repo (DESTRUCTIVE) always does."""
        wf = get_action_workflows()
        assert wf["link_repo"].needs_confirm is False
        assert wf["list_repos"].needs_confirm is False
        assert wf["unlink_repo"].needs_confirm is True


# ---------------------------------------------------------------------------
# 3. CXO's CONSTRAINT 2 — resolve before arming, never after the yes
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestResolveBeforeArming:
    """Each leg: the gate must return ``passthrough_result`` (nothing armed)
    with the SAME copy the legacy ``_handle_repo_management`` UNLINK branch
    has always returned — proven by calling the real resolve chain with the
    DB layer patched, never by assumption."""

    async def test_missing_both_slots_does_not_arm(self):
        handler = CanonicalHandlers()
        intent = _make_intent("unlink the repo")
        gate = await build_unlink_repo_confirmation(intent, handler, _USER)
        assert gate.offer is None
        assert gate.passthrough_result is not None
        assert gate.passthrough_result["requires_clarification"] is True
        assert "owner/repo" in gate.passthrough_result["message"]

    async def test_project_not_found_does_not_arm(self):
        handler = CanonicalHandlers()
        intent = _make_intent()
        mock_factory = _mock_session_factory()
        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO),
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = None

            gate = await build_unlink_repo_confirmation(intent, handler, _USER)

        assert gate.offer is None
        assert gate.passthrough_result["requires_clarification"] is False
        assert "couldn't find" in gate.passthrough_result["message"].lower()
        assert gate.passthrough_result["intent"]["context"]["error"] == "project_not_found"

    async def test_repo_not_found_does_not_arm(self):
        handler = CanonicalHandlers()
        intent = _make_intent()
        mock_factory = _mock_session_factory()
        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = _mock_project()

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.get_by_full_name.return_value = None

            gate = await build_unlink_repo_confirmation(intent, handler, _USER)

        assert gate.offer is None
        assert gate.passthrough_result["intent"]["context"]["error"] == "repo_not_found"

    async def test_not_linked_does_not_arm(self):
        """Repo and project both exist, but there is no link between
        them — the gate's OWN extra read (link-existence) must catch this
        BEFORE arming, not merely rely on the execute-time delete call."""
        handler = CanonicalHandlers()
        intent = _make_intent()
        mock_factory = _mock_session_factory()
        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = _mock_project()

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.get_by_full_name.return_value = _mock_repo()
            mock_repo_repo.get_project_links.return_value = []  # no link to THIS project
            mock_repo_repo.unlink_from_project = AsyncMock(
                side_effect=AssertionError(
                    "unlink_from_project FIRED during confirm-gate resolution — "
                    "arming must never mutate"
                )
            )

            gate = await build_unlink_repo_confirmation(intent, handler, _USER)

        assert gate.offer is None
        assert gate.passthrough_result["intent"]["context"]["status"] == "not_linked"
        assert "wasn't linked" in gate.passthrough_result["message"]

    async def test_fully_resolved_arms(self):
        handler = CanonicalHandlers()
        intent = _make_intent()
        mock_factory = _mock_session_factory()
        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = _mock_project()

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.get_by_full_name.return_value = _mock_repo()
            mock_repo_repo.get_project_links.return_value = [_mock_link(project_id="proj-1")]

            gate = await build_unlink_repo_confirmation(intent, handler, _USER)

        assert gate.passthrough_result is None
        assert gate.offer is not None


# ---------------------------------------------------------------------------
# 4. CXO's CONSTRAINT 3 — copy, verbatim (incl. the is_primary clause)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestCopy:
    async def _arm(self, is_primary):
        handler = CanonicalHandlers()
        intent = _make_intent()
        mock_factory = _mock_session_factory()
        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = _mock_project()

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.get_by_full_name.return_value = _mock_repo()
            mock_repo_repo.get_project_links.return_value = [
                _mock_link(project_id="proj-1", is_primary=is_primary)
            ]

            return await build_unlink_repo_confirmation(intent, handler, _USER)

    async def test_ask_names_what_does_not_happen_and_the_relink_option(self):
        gate = await self._arm(is_primary=False)
        q = gate.offer.question
        assert f"Unlink {_REPO} from {_PROJECT}?" in q
        assert "repository itself isn't touched" in q
        assert "link it again later" in q

    async def test_non_primary_link_has_no_primary_clause(self):
        gate = await self._arm(is_primary=False)
        assert "primary repository" not in gate.offer.question

    async def test_primary_link_appends_cxos_clause(self):
        gate = await self._arm(is_primary=True)
        q = gate.offer.question
        assert "primary repository" in q
        assert "linking it again won't restore that" in q

    async def test_decline_copy_matches_cxo_verbatim(self):
        gate = await self._arm(is_primary=False)
        assert (
            gate.offer.offer["decline_message"] == f"Okay, I've left {_REPO} linked to {_PROJECT}."
        )

    async def test_success_copy_is_unchanged_done_ive_unlinked(self):
        """Constraint 3's last line: success copy stays as-is — built by
        _handle_unlink_repo, not the confirm gate. Proven directly against
        the handler (not merely asserted from the legacy pin)."""
        handler = CanonicalHandlers()
        intent = _make_intent()
        mock_factory = _mock_session_factory()
        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = _mock_project()

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.get_by_full_name.return_value = _mock_repo()
            mock_repo_repo.unlink_from_project.return_value = True

            result = await handler._handle_unlink_repo(intent, _SESSION, _USER)

        assert result["message"] == f"Done! I've unlinked {_REPO} from {_PROJECT}."


# ---------------------------------------------------------------------------
# 5. CXO's CONSTRAINT 4 — exit copy at the prompt site (#1899 convention)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestExitCopyAtThePromptSite:
    async def test_never_mind_appears_in_the_armed_question(self):
        handler = CanonicalHandlers()
        intent = _make_intent()
        mock_factory = _mock_session_factory()
        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = _mock_project()

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.get_by_full_name.return_value = _mock_repo()
            mock_repo_repo.get_project_links.return_value = [_mock_link(project_id="proj-1")]

            gate = await build_unlink_repo_confirmation(intent, handler, _USER)

        assert "never mind" in gate.offer.question.lower()


# ---------------------------------------------------------------------------
# 6. THE RAIL, END TO END — arm / yes / no / never-mind, real IntentService
#
# PORTFOLIO is claimed WHOLE by CanonicalHandlers.can_handle() (same note on
# every entry's comment above: "in the real dispatch order
# (_should_route_to_floor -> can_handle -> action rail) the canonical branch
# returns before the action rail is ever reached for a PORTFOLIO intent" —
# this is categorically true today for EVERY PORTFOLIO rail entry, link_repo
# and archive_project/restore_project/add_project included, not something
# this unit introduces). A full ``process_intent`` round trip for a
# classified-or-replaced unlink_repo Intent therefore hits "portfolio_help"
# before ever reaching ``_dispatch_action_rail`` — confirmed by running it
# (measured, not assumed, the first version of this test file tried exactly
# that and got "portfolio_help" back).
#
# The architecturally honest boundary is ``_dispatch_action_rail`` itself —
# the SAME extracted, directly-callable method the #1595 multi-intent sibling
# loop calls N times per turn (test_inversion_multi_intent_unit4_1595.py
# calls it the same way, via ``service._dispatch_action_rail``). Calling it
# directly is exactly how this rail entry IS reachable today (per its own
# comment: "consulted only by consult_inversion_live... and the Phase 3
# deletion gate's live-match mechanism") — this is the gate under test, not
# a workaround. ``_dispatch_action_rail`` arms the REAL session-scoped
# ``workflow_offer_service`` store, so the "yes"/"no"/"never mind" SECOND
# turn goes through the genuine, unmodified offer-acceptance seam in
# ``process_intent`` — that seam pops the pending offer BEFORE
# classification/canonical, so it is unaffected by PORTFOLIO's whole-category
# claim (CXO's constraint 2 is about turn 1; this section proves turn 2).
# ---------------------------------------------------------------------------


@pytest.fixture
def db_mocks(monkeypatch):
    """Patch the DB layer for the arm call (_dispatch_action_rail, below)
    AND the "yes" turn's execute call (full process_intent) — same idiom as
    test_repo_management.py, applied via monkeypatch (not a `with` block)
    since this spans two separate calls."""
    mock_factory = _mock_session_factory()
    monkeypatch.setattr("services.database.session_factory.AsyncSessionFactory", mock_factory)

    mock_proj_repo = AsyncMock()
    mock_proj_repo.find_by_name.return_value = _mock_project()

    mock_repo_repo = AsyncMock()
    mock_repo_repo.get_by_full_name.return_value = _mock_repo()
    mock_repo_repo.get_project_links.return_value = [_mock_link(project_id="proj-1")]
    state = {"unlinked": False}

    async def _unlink(repository_id, project_id):
        state["unlinked"] = True
        return True

    mock_repo_repo.unlink_from_project = AsyncMock(side_effect=_unlink)

    monkeypatch.setattr(
        "services.database.repositories.ProjectRepository",
        lambda session: mock_proj_repo,
    )
    monkeypatch.setattr(
        "services.database.repositories.RepositoryRepository",
        lambda session: mock_repo_repo,
    )
    return state


@pytest.mark.asyncio
class TestRailEndToEnd:
    async def _arm(self, service):
        intent = _make_intent()
        outcome = await service._dispatch_action_rail(
            intent,
            message=_MSG,
            session_id=_SESSION,
            user_id=_USER,
            workflow_id=None,
            all_suggestions=None,
            preferences=None,
        )
        assert outcome.on_rail is True
        assert outcome.armed is True
        return outcome

    async def test_arm_sets_the_real_pending_offer_and_unlinks_nothing(self, db_mocks):
        service = IntentService()
        outcome = await self._arm(service)

        assert outcome.result.success is True
        assert outcome.result.intent_data.get("destructive_confirmation_pending") is True
        assert f"Unlink {_REPO} from {_PROJECT}?" in outcome.result.message
        assert db_mocks["unlinked"] is False, (
            "arming unlink_repo's confirm mutated the link on the arming "
            "turn — the #1190 confirm gate did not hold"
        )
        # The armed record is on the REAL session-scoped store the next
        # process_intent turn will read.
        pending = service.workflow_offer_service.peek_pending_offer(_SESSION)
        assert pending is not None
        assert pending["pending_action"]["action"] == "unlink_repo"

    async def test_yes_executes_and_unlinks(self, db_mocks):
        service = IntentService()
        await self._arm(service)

        yes_result = await service.process_intent(message="yes", session_id=_SESSION, user_id=_USER)

        assert db_mocks["unlinked"] is True
        assert yes_result.message == f"Done! I've unlinked {_REPO} from {_PROJECT}."

    async def test_no_declines_and_leaves_it_linked(self, db_mocks):
        service = IntentService()
        await self._arm(service)

        no_result = await service.process_intent(message="no", session_id=_SESSION, user_id=_USER)

        assert db_mocks["unlinked"] is False
        assert no_result.message == f"Okay, I've left {_REPO} linked to {_PROJECT}."

    async def test_never_mind_declines_and_leaves_it_linked(self, db_mocks):
        """The #888/#1529 bare-exit path (detect_bare_exit) resolves
        'never mind' to the SAME decline — CXO's constraint 4's exit phrase
        actually works, not merely appears in the question text."""
        service = IntentService()
        await self._arm(service)

        nm_result = await service.process_intent(
            message="never mind", session_id=_SESSION, user_id=_USER
        )

        assert db_mocks["unlinked"] is False
        assert nm_result.message == f"Okay, I've left {_REPO} linked to {_PROJECT}."
