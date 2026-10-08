"""#1856 — the add-project flow dropped its initiation args, then looped.

PM live on alpha, 2026-09-23, verbatim:

    PM  > add project One Job with repo Design-in-Product/one-job
    app < I'd be happy to help you add a new project! What would you like to
          call it?
    PM  > we're going in circles now and no that is not the name of the new
          project
    app < I'd be happy to help you add a new project! What would you like to
          call it?          <-- IDENTICAL. 'cancel' was the only way out.

PM's first turn is **the app's own suggested phrasing**. Both provided
arguments (name AND repo) were discarded, and the correction on turn 2 was
neither consumed nor detected as a repeat.

Reachability trace (intent-routing-stack.md surfaces), measured in-process:
  Surface 1 (pre-classifier) CLAIMS all four initiation shapes AND PM's turn 2
  as PORTFOLIO / ``manage_portfolio`` with ``context == {"original_message":
  ...}`` and NO slots -- there is nothing already-extracted to consume. The
  claim lands in ``canonical_handlers._handle_portfolio_query``, whose
  ``operation == "add"`` branch ignored ``original_message`` entirely.
  Turn 2 re-enters that same branch because it contains the literal token
  "new project" (the branch's keyword sniff is
  ``any(word in message_lower for word in ["add", "create", "new project"])``),
  which is the whole repeat mechanism.

🔴 WHY THE FIX IS AT THIS SEAM AND NOT IN ``PortfolioOnboardingHandler``:
  ``services/process/adapters.py:609`` has
  ``# registry.register(OnboardingProcessAdapter())`` COMMENTED OUT (ADR-059,
  "onboarding on ice"), and ``IntentService._check_active_onboarding`` has no
  production caller. No follow-up turn can reach
  ``PortfolioOnboardingHandler.handle_turn``. The session the add branch
  created was an orphan and its question was one the system was structurally
  incapable of hearing the answer to. Hardening ``_handle_gathering`` would be
  unreachable code; the honest fix is to consume the args at the claiming
  handler and to stop asking an open question that cannot be answered.

Moratorium / ratchet note: NO new pre-classifier pattern -- the claiming
pattern already matches every shape here. The add-family slot extraction lives
beside its existing siblings (ARCHIVE_PATTERNS / DELETE_PATTERNS /
RESTORE_PATTERNS) in ``services/onboarding/portfolio_service.py``, which is
outside ``TestExtractionPatternRatchet.SURFACE_SPANS``; the frozen ceilings are
unchanged by this commit.

Layer honesty (m-43): surface 1 via ``PreClassifier.pre_classify``; the handler
seam via ``CanonicalHandlers._handle_portfolio_query`` with the DB mocked; the
extractor and the plausibility predicate as pure units. Denominator (m-44): the
four initiation shapes named in #1856 plus PM's two verbatim turns.

#1886 UPDATE (2026-10-07): the "did I already ask?" bookkeeping this file's
``TestDefect2NoRepeatedCannedPrompt`` originally pinned lived on a
``PortfolioOnboardingManager`` session created INLINE by
``_handle_add_project`` — Rule-0 deleted along with the rest of the dead
onboarding chain (#1867 finding 1: that session orphaned on a bare-name
reply, since nothing re-armed it). The "never repeat the identical ask"
guarantee now lives one layer up, in the #846/#1190 carrier
(``services/intent_service/add_project_clarify.py``) — covered by
``tests/unit/services/intent_service/test_add_project_name_carrier_1886.py``.
The three tests here that drove that guarantee by calling
``_handle_portfolio_query`` twice IN A ROW with no offer-seam in between
(which is not how two real turns reach this method — the seam sits between
them) were deleted; ``TestDefect1InitiationArgsArePreFilled`` and the
single-ask / bookkeeping-must-not-block-a-later-good-turn tests below are
unaffected (branch 1's create path and branch 2's ask copy are unchanged).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.pre_classifier import PreClassifier
from services.onboarding.portfolio_service import (
    extract_add_project_slots,
    is_plausible_project_name,
)
from services.shared_types import IntentCategory

# --- PM's verbatim turns, 2026-09-23 alpha -------------------------------

PM_TURN_1 = "add project One Job with repo Design-in-Product/one-job"
PM_TURN_2 = "we're going in circles now and no that is not the name of the new project"

# The canned line PM saw twice.
CANNED_PROMPT = "I'd be happy to help you add a new project! What would you like to call it?"

INITIATION_SHAPES = [
    # (utterance, expected name, expected repo)
    (PM_TURN_1, "One Job", "Design-in-Product/one-job"),
    ("add project One Job", "One Job", None),
    ("add a project called One Job", "One Job", None),
    (
        "create project One Job for repo Design-in-Product/one-job",
        "One Job",
        "Design-in-Product/one-job",
    ),
]


# =========================================================================
# Reachability: surface 1 claims every shape, with no slots of its own.
# =========================================================================


class TestReachability:
    @pytest.mark.parametrize("message", [s[0] for s in INITIATION_SHAPES] + [PM_TURN_2])
    def test_claimed_by_portfolio_with_no_slots(self, message):
        intent = PreClassifier.pre_classify(message)
        assert intent is not None, f"pre-classifier did not claim {message!r}"
        assert intent.category == IntentCategory.PORTFOLIO
        assert intent.action == "manage_portfolio"
        # The whole reason extraction has to happen at the handler: the
        # classifier hands over the raw message and nothing else.
        assert set(intent.context) == {"original_message"}


# =========================================================================
# The extractor (pure unit).
# =========================================================================


class TestExtractAddProjectSlots:
    @pytest.mark.parametrize("message,name,repo", INITIATION_SHAPES)
    def test_shapes_named_in_1856(self, message, name, repo):
        slots = extract_add_project_slots(message)
        assert slots["name"] == name
        assert slots["repo"] == repo

    def test_case_is_preserved(self):
        """The archive/delete/restore siblings match against a lowercased
        message, so their captures come back lowercased. A project NAME is
        user-visible data -- 'One Job' must not become 'one job'."""
        assert extract_add_project_slots("add project One Job")["name"] == "One Job"

    def test_pm_turn_2_yields_no_name(self):
        """The correction must not be mined for a name."""
        slots = extract_add_project_slots(PM_TURN_2)
        assert slots["name"] is None

    @pytest.mark.parametrize(
        "message",
        [
            "add a project",
            "add a new project",
            "create a project",
            "I want to add a project",
        ],
    )
    def test_bare_initiation_has_no_name(self, message):
        assert extract_add_project_slots(message)["name"] is None

    def test_quoted_and_polite_forms_are_normalised(self):
        assert extract_add_project_slots('add project "One Job" please')["name"] == "One Job"


class TestIsPlausibleProjectName:
    @pytest.mark.parametrize("text", ["One Job", "HealthTrack", "Piper Morgan", "one-job"])
    def test_plausible(self, text):
        assert is_plausible_project_name(text) is True

    @pytest.mark.parametrize(
        "text",
        [
            PM_TURN_2,  # negation + correction, 14 words
            "no that is not it",
            "cancel",
            "what are you talking about?",
            "we're going in circles",
            "this is not the name of the new project at all",
            "",
            "   ",
        ],
    )
    def test_implausible(self, text):
        assert is_plausible_project_name(text) is False


# =========================================================================
# The handler seam.
# =========================================================================


class _FakeScope:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *args):
        return False


def _portfolio_intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.PORTFOLIO,
        action="manage_portfolio",
        confidence=1.0,
        context={"original_message": message},
    )


@pytest.fixture
def handler():
    return CanonicalHandlers()


class _Recorder:
    """Captures what the handler actually wrote."""

    def __init__(self, existing_project=None):
        self.created = []
        self.linked = []
        self.existing_project = existing_project

    def install(self):
        from services.database.repositories import ProjectRepository, RepositoryRepository
        from services.database.session_factory import AsyncSessionFactory

        created_project = MagicMock()
        created_project.id = "proj-1"
        created_project.name = "One Job"

        async def _create(_self, **kwargs):
            self.created.append(kwargs)
            created_project.name = kwargs.get("name", "One Job")
            return created_project

        async def _find_by_name(_self, **kwargs):
            return self.existing_project

        repo_row = MagicMock()
        repo_row.id = "repo-1"

        async def _get_by_full_name(_self, **kwargs):
            return None

        async def _create_repository(_self, repo_domain):
            repo_row.full_name = repo_domain.full_name
            return repo_row

        async def _get_project_links(_self, _repo_id):
            return []

        async def _link_to_project(_self, **kwargs):
            self.linked.append(kwargs)
            return MagicMock()

        async def _validate(_repo_name):
            v = MagicMock()
            v.validated = False
            v.exists = None
            return v

        return [
            patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())),
            patch.object(ProjectRepository, "create", _create),
            patch.object(ProjectRepository, "find_by_name", _find_by_name),
            patch.object(RepositoryRepository, "get_by_full_name", _get_by_full_name),
            patch.object(RepositoryRepository, "create_repository", _create_repository),
            patch.object(RepositoryRepository, "get_project_links", _get_project_links),
            patch.object(RepositoryRepository, "link_to_project", _link_to_project),
            patch(
                "services.infrastructure.github_repo_validator.validate_github_repo",
                _validate,
            ),
        ]


async def _run(handler, message, recorder, session_id="s1", user_id="u1"):
    import contextlib

    with contextlib.ExitStack() as stack:
        for p in recorder.install():
            stack.enter_context(p)
        return await handler._handle_portfolio_query(
            _portfolio_intent(message), session_id=session_id, user_id=user_id
        )


class TestDefect1InitiationArgsArePreFilled:
    """PM's turn 1 carried BOTH slots and both were dropped."""

    @pytest.mark.asyncio
    async def test_pm_turn_1_creates_the_project_and_links_the_repo(self, handler):
        rec = _Recorder()
        result = await _run(handler, PM_TURN_1, rec)

        # The defect, pinned: it must not ask for what PM just supplied.
        assert CANNED_PROMPT not in result["message"]
        assert "what would you like to call it" not in result["message"].lower()

        assert len(rec.created) == 1, "the named project was never created"
        assert rec.created[0]["name"] == "One Job"
        assert rec.created[0]["owner_id"] == "u1"

        assert len(rec.linked) == 1, "the supplied repo was never linked"

        assert "One Job" in result["message"]
        assert "Design-in-Product/one-job" in result["message"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("message,name,repo", INITIATION_SHAPES)
    async def test_every_named_shape_skips_the_name_prompt(self, handler, message, name, repo):
        rec = _Recorder()
        result = await _run(handler, message, rec)

        assert "what would you like to call it" not in result["message"].lower()
        assert len(rec.created) == 1
        assert rec.created[0]["name"] == name
        assert len(rec.linked) == (1 if repo else 0)

    @pytest.mark.asyncio
    async def test_name_only_shape_asks_only_for_the_repo(self, handler):
        """'ask only for what's missing' -- a name with no repo is a complete
        add; the repo is optional, so the turn offers it rather than blocking
        on it, and never re-asks for the name."""
        rec = _Recorder()
        result = await _run(handler, "add project One Job", rec)

        assert len(rec.created) == 1
        assert "what would you like to call it" not in result["message"].lower()
        assert "repo" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_existing_project_is_not_duplicated(self, handler):
        existing = MagicMock()
        existing.id = "proj-existing"
        existing.name = "One Job"
        rec = _Recorder(existing_project=existing)
        result = await _run(handler, "add project One Job", rec)

        assert rec.created == [], "a duplicate project was created"
        assert "One Job" in result["message"]
        assert "already" in result["message"].lower()


class TestDefect2NoRepeatedCannedPrompt:
    """PM got the IDENTICAL line twice. Never twice in a row.

    #1886: the cross-turn "never repeat the identical ask" guarantee moved
    to the carrier (see the file-level docstring addendum) — that half is
    now pinned in test_add_project_name_carrier_1886.py. What stays here is
    single-call behavior this method still owns directly: the ask's own
    copy, and that bookkeeping removal doesn't block a later good turn.
    """

    @pytest.mark.asyncio
    async def test_the_first_ask_is_imperative_and_offers_cancel(self, handler):
        rec = _Recorder()
        result = await _run(handler, "add a project", rec)
        msg = result["message"]

        assert "add project" in msg.lower(), "no imperative one-liner offered"
        assert "cancel" in msg.lower(), "no way out offered"
        # #1738: angle-bracket placeholders are swallowed by the web render.
        assert "<" not in msg, "angle-bracket placeholder will render as an empty slot"

    @pytest.mark.asyncio
    async def test_a_name_after_a_failed_ask_still_works(self, handler):
        """The pending-ask bookkeeping must not block a later good turn."""
        rec = _Recorder()
        await _run(handler, "add a project", rec)
        await _run(handler, PM_TURN_2, rec)
        result = await _run(handler, PM_TURN_1, rec)

        assert len(rec.created) == 1
        assert rec.created[0]["name"] == "One Job"
        assert "One Job" in result["message"]
