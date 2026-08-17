"""#1567 — repo clarification binds, and natural repo phrasing extracts.

PM's transcript (2026-08-10, the #1411 retest): after "Cannot update issue:
repository not specified. Please specify which repository." PM answered
"change the title of issue 108 in the test-Piper-Morgan repository" — and got
the SAME refusal. Only the compressed owner/name form worked. This file pins
the fixed transcript shape end-to-end plus the two mechanisms:

1. **The question BINDS**: the update/close repository dead-end now arms the
   #846/#1190 action-agnostic carrier (kind ``issue_repo_question``); the next
   turn's answer — bare ``owner/name``, bare repo name resolved against the
   user's actual repos, natural phrasing, or a same-operation re-statement —
   slot-fills the ORIGINAL intent and the operation proceeds. Unrelated
   commands mid-ask still route (off-intent abandons via the pop; the #1631
   prose/command discrimination is inherited at the generic seam).

2. **Natural phrasing extracts from the ORIGINAL ask**: "in the
   test-Piper-Morgan repository" (bare name, mixed case) resolves and
   short-circuits the question entirely; "in my default repository" stays the
   #1411 resolver's business (never read as a repo literally named
   "default"); a slot-filled title never swallows the routing clause.

Layer honesty (m-43): extraction/resolution units are pure; handler-level
tests drive the REAL ``_handle_update_issue`` / ``_handle_close_issue_query``
with the router, resolver, and repo-search patched at their seams; the
transcript classes drive the REAL ``process_intent`` with an EXPLOSIVE LLM
(PM's sentences resolve deterministically) and GitHub patched at the API
boundary only.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.repo_clarification import (
    REPO_QUESTION_KIND,
    RepoNameResolution,
    extract_natural_repo_name,
    extract_repo_answer,
    resolve_repo_name,
    strip_trailing_repo_clause,
)
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
RESOLVER = "services.integrations.github.repo_resolver"
REPO_CLAR = "services.intent_service.repo_clarification"
ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"

_USER = "3f7b8a52-1567-4b00-9e00-000000001567"  # valid UUID
_FULL = "mediajunkie/test-piper-morgan"

# PM's literal follow-up phrasing (the turn that used to re-refuse).
PM_NATURAL_ANSWER = "in the test-Piper-Morgan repository"
PM_RESTATEMENT = "change the title of issue 108 in the test-Piper-Morgan repository"
ASK_NO_REPO = "change the title of issue #108 to Testing"


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — these turns resolve deterministically"
        )


@pytest.fixture
def service():
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            return IntentService(intent_classifier=clf)


def _pending(service, sid):
    return service.workflow_offer_service._pending_offers.get(sid)


def _update_intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.EXECUTION,
        action="update_issue",
        original_message=message,
        confidence=1.0,
        context={"original_message": message, "user_id": _USER},
    )


def _resolver_unresolved():
    from services.integrations.github.repo_resolver import UnresolvedRepoError

    return patch(
        f"{RESOLVER}.resolve_repo", new=AsyncMock(side_effect=UnresolvedRepoError())
    )


def _repos_result(*full_names):
    return MagicMock(
        degradation=None,
        repositories=[
            {"name": fn.split("/", 1)[1], "full_name": fn} for fn in full_names
        ],
    )


def _adapter_with(*full_names):
    instance = MagicMock()
    instance.search_user_repositories = AsyncMock(return_value=_repos_result(*full_names))
    return patch(f"{ADAPTER}", return_value=instance)


def _no_default():
    return patch(f"{RESOLVER}.get_user_default_repo", new=AsyncMock(return_value=None))


# ---------------------------------------------------------------------------
# Extraction units — natural phrasing
# ---------------------------------------------------------------------------


class TestNaturalRepoNameExtraction:
    def test_pm_phrase_extracts_the_bare_name(self):
        assert extract_natural_repo_name(PM_RESTATEMENT) == "test-Piper-Morgan"

    def test_fragment_answer_extracts(self):
        assert extract_natural_repo_name(PM_NATURAL_ANSWER) == "test-Piper-Morgan"

    def test_default_repository_phrase_is_not_a_name(self):
        """'in my default repository' is the #1411 resolver's business."""
        assert (
            extract_natural_repo_name(
                "change the status of issue #108 to Done in my default repository"
            )
            is None
        )

    def test_repo_called_form(self):
        assert (
            extract_natural_repo_name("close issue #9 in the repo called piper-thing")
            == "piper-thing"
        )

    def test_quoted_name_in_natural_phrase(self):
        assert (
            extract_natural_repo_name('the issue lives in the "test-Piper-Morgan" repository')
            == "test-Piper-Morgan"
        )

    def test_no_phrasing_returns_none(self):
        assert extract_natural_repo_name(ASK_NO_REPO) is None
        assert extract_natural_repo_name("") is None


class TestRepoAnswerExtraction:
    @pytest.mark.parametrize(
        "answer,expected",
        [
            ("mediajunkie/test-piper-morgan", "mediajunkie/test-piper-morgan"),
            ("https://github.com/mediajunkie/test-piper-morgan", "mediajunkie/test-piper-morgan"),
            (PM_NATURAL_ANSWER, "test-Piper-Morgan"),
            ("test-piper-morgan", "test-piper-morgan"),
            ("use test-piper-morgan", "test-piper-morgan"),
            ("it's in test-piper-morgan", "test-piper-morgan"),
            ("the test-piper-morgan repo", "test-piper-morgan"),
            ('"test-piper-morgan"', "test-piper-morgan"),
        ],
    )
    def test_answer_shapes_extract(self, answer, expected):
        assert extract_repo_answer(answer) == expected

    @pytest.mark.parametrize("non_answer", ["yes", "no", "ok", "thanks", "cancel", "hmm"])
    def test_bare_non_answers_do_not_extract(self, non_answer):
        assert extract_repo_answer(non_answer) is None

    def test_bare_token_suppressed_when_disallowed(self):
        """With an accept/decline already detected, a bare token is never
        reinterpreted as a repo name."""
        assert extract_repo_answer("test-piper-morgan", allow_bare_token=False) is None
        # …but the explicit shapes still extract.
        assert (
            extract_repo_answer(PM_NATURAL_ANSWER, allow_bare_token=False)
            == "test-Piper-Morgan"
        )


class TestTitleNeverSwallowsRoutingClause:
    def test_natural_clause_stripped(self):
        assert (
            strip_trailing_repo_clause("Testing in the test-piper-morgan repository")
            == "Testing"
        )

    def test_owner_name_clause_stripped(self):
        assert (
            strip_trailing_repo_clause("Testing in mediajunkie/test-piper-morgan")
            == "Testing"
        )

    def test_plain_prose_tail_kept(self):
        """'in Chrome' is title content — no slash, no repository noun."""
        text = "fix the crash when logging in Chrome"
        assert strip_trailing_repo_clause(text) == text

    def test_slotfill_title_excludes_the_clause(self):
        slots = IntentService._slotfill_issue_request(
            "change the title of issue #108 to Testing in the test-Piper-Morgan repository"
        )
        assert slots.get("title") == "Testing"
        # the natural form carries no owner/name pair for the slot-fill
        assert slots.get("repository") is None


# ---------------------------------------------------------------------------
# Bare-name resolution against the user's actual repos
# ---------------------------------------------------------------------------


class TestResolveRepoName:
    pytestmark = pytest.mark.asyncio

    async def test_default_repo_name_match_wins_without_search(self):
        with (
            patch(f"{RESOLVER}.get_user_default_repo", new=AsyncMock(return_value=_FULL)),
            patch(f"{ADAPTER}") as adapter_cls,
        ):
            res = await resolve_repo_name(_USER, "Test-Piper-Morgan")
        assert res.status == "resolved"
        assert res.full_name == _FULL
        adapter_cls.assert_not_called()

    async def test_case_insensitive_match_among_user_repos(self):
        with (_no_default(), _adapter_with(_FULL, "mediajunkie/other")):
            res = await resolve_repo_name(_USER, "test-Piper-Morgan")
        assert res.status == "resolved"
        assert res.full_name == _FULL

    async def test_ambiguous_when_two_owners_share_the_name(self):
        with (
            _no_default(),
            _adapter_with("mediajunkie/tools", "someoneelse/tools"),
        ):
            res = await resolve_repo_name(_USER, "tools")
        assert res.status == "ambiguous"
        assert set(res.candidates) == {"mediajunkie/tools", "someoneelse/tools"}

    async def test_not_found_when_searched_and_absent(self):
        with (_no_default(), _adapter_with(_FULL)):
            res = await resolve_repo_name(_USER, "banana")
        assert res.status == "not_found"

    async def test_unavailable_when_repos_unreadable(self):
        """m-43: a degrade is 'couldn't check', never 'not found'."""
        instance = MagicMock()
        instance.search_user_repositories = AsyncMock(
            return_value=MagicMock(degradation=object(), repositories=None)
        )
        with (_no_default(), patch(f"{ADAPTER}", return_value=instance)):
            res = await resolve_repo_name(_USER, "test-piper-morgan")
        assert res.status == "unavailable"

    async def test_unavailable_without_a_principal(self):
        res = await resolve_repo_name(None, "test-piper-morgan")
        assert res.status == "unavailable"

    async def test_owner_qualified_passes_through(self):
        res = await resolve_repo_name(_USER, _FULL)
        assert res.status == "resolved"
        assert res.full_name == _FULL


# ---------------------------------------------------------------------------
# Mechanism 2 — natural phrasing in the ORIGINAL ask short-circuits the ask
# ---------------------------------------------------------------------------


class TestOriginalAskNaturalPhrasing:
    pytestmark = pytest.mark.asyncio

    async def test_named_repo_resolves_and_update_proceeds(self, service):
        updated = {"number": 108, "title": "Testing", "state": "open"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=updated)) as w,
            patch(
                f"{REPO_CLAR}.resolve_repo_name",
                new=AsyncMock(
                    return_value=RepoNameResolution(status="resolved", full_name=_FULL)
                ),
            ) as resolver,
        ):
            result = await service._handle_update_issue(
                _update_intent(
                    'change the title of issue #108 to "Testing" in the test-Piper-Morgan repository'
                ),
                "wf-1567",
                session_id="sess-natural",
                user_id=_USER,
            )
        assert result.success is True
        resolver.assert_awaited_once_with(_USER, "test-Piper-Morgan")
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert w.await_args.kwargs["repo_name"] == "test-piper-morgan"
        assert w.await_args.kwargs["title"] == "Testing"
        assert _pending(service, "sess-natural") is None

    async def test_named_but_unfound_repo_asks_and_never_uses_default(self, service):
        """A user-NAMED repo that doesn't resolve asks — it must never fall
        through to the default silently (the wrong-repo write)."""
        explosive_default = patch(
            f"{RESOLVER}.resolve_repo",
            new=AsyncMock(side_effect=AssertionError("default must not be consulted")),
        )
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            explosive_default,
            _no_default(),
            patch(
                f"{REPO_CLAR}.resolve_repo_name",
                new=AsyncMock(return_value=RepoNameResolution(status="not_found")),
            ),
        ):
            result = await service._handle_update_issue(
                _update_intent(PM_RESTATEMENT),
                "wf-1567",
                session_id="sess-unfound",
                user_id=_USER,
            )
        assert result.success is True
        assert result.requires_clarification is True
        assert "couldn't find one called 'test-Piper-Morgan'" in result.message
        offer = _pending(service, "sess-unfound")
        assert offer is not None
        assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND
        assert offer["pending_action"]["asked_name"] == "test-Piper-Morgan"

    async def test_unfound_name_with_default_offers_the_closed_question(self, service):
        """#1411 default-repo integration: when a default exists, the failed
        name lookup asks 'say yes to use your default, owner/name'."""
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(
                f"{RESOLVER}.get_user_default_repo",
                new=AsyncMock(return_value="mediajunkie/piper-thing"),
            ),
            patch(
                f"{REPO_CLAR}.resolve_repo_name",
                new=AsyncMock(return_value=RepoNameResolution(status="not_found")),
            ),
        ):
            result = await service._handle_update_issue(
                _update_intent(PM_RESTATEMENT),
                "wf-1567",
                session_id="sess-default-offer",
                user_id=_USER,
            )
        assert "say 'yes' to use your default, mediajunkie/piper-thing" in result.message
        offer = _pending(service, "sess-default-offer")
        assert offer["pending_action"]["default_repo"] == "mediajunkie/piper-thing"

    async def test_unavailable_copy_never_claims_a_search(self, service):
        """m-43: 'couldn't check your repositories' — not 'couldn't find'."""
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            _no_default(),
            patch(
                f"{REPO_CLAR}.resolve_repo_name",
                new=AsyncMock(return_value=RepoNameResolution(status="unavailable")),
            ),
        ):
            result = await service._handle_update_issue(
                _update_intent(PM_RESTATEMENT),
                "wf-1567",
                session_id="sess-degrade",
                user_id=_USER,
            )
        assert "couldn't check your repositories" in result.message
        assert "couldn't find" not in result.message


# ---------------------------------------------------------------------------
# The pinned transcript — through the REAL process_intent
# ---------------------------------------------------------------------------


class TestPinnedTranscript:
    pytestmark = pytest.mark.asyncio

    async def _ask_turn(self, service, sid):
        """Turn 1: PM's update ask with NO repo and NO resolvable default →
        the question (not the dead-end refusal)."""
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            _resolver_unresolved(),
        ):
            return await service.process_intent(
                message=ASK_NO_REPO, session_id=sid, user_id=_USER
            )

    def _answer_patches(self, updated=None):
        updated = updated or {
            "number": 108,
            "title": "Testing",
            "state": "open",
            "html_url": f"https://github.com/{_FULL}/issues/108",
        }
        return (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=updated)),
            _no_default(),
            _adapter_with(_FULL),
        )

    async def test_ask_without_repo_produces_the_question(self, service):
        result = await self._ask_turn(service, "t-ask")
        assert "Which repository is issue #108 in?" in result.message
        assert "repository not specified" not in result.message
        offer = _pending(service, "t-ask")
        assert offer is not None
        assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND
        assert offer["pending_action"]["issue_number"] == 108

    async def test_pm_natural_fragment_answer_binds_and_proceeds(self, service):
        """The AC transcript: question → 'in the test-Piper-Morgan
        repository' → the update proceeds with the ORIGINAL title, against
        the repo resolved case-insensitively from the user's own repos."""
        sid = "t-natural"
        await self._ask_turn(service, sid)
        p = self._answer_patches()
        with p[0], p[1], p[2] as w, p[3], p[4]:
            result = await service.process_intent(
                message=PM_NATURAL_ANSWER, session_id=sid, user_id=_USER
            )
        assert w.await_count == 1
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert w.await_args.kwargs["repo_name"] == "test-piper-morgan"
        assert w.await_args.kwargs["title"] == "Testing"  # the ORIGINAL ask's title
        assert "Updated issue #108" in result.message
        assert _pending(service, sid) is None

    async def test_bare_name_answer_binds(self, service):
        sid = "t-bare"
        await self._ask_turn(service, sid)
        p = self._answer_patches()
        with p[0], p[1], p[2] as w, p[3], p[4]:
            result = await service.process_intent(
                message="test-piper-morgan", session_id=sid, user_id=_USER
            )
        assert w.await_count == 1
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert "Updated issue #108" in result.message

    async def test_owner_qualified_answer_binds(self, service):
        sid = "t-owner"
        await self._ask_turn(service, sid)
        p = self._answer_patches()
        with p[0], p[1], p[2] as w, p[3], p[4]:
            result = await service.process_intent(
                message=_FULL, session_id=sid, user_id=_USER
            )
        assert w.await_count == 1
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert "Updated issue #108" in result.message

    async def test_pm_full_restatement_binds(self, service):
        """PM's literal second turn — a re-statement of the SAME operation
        with the repo phrased naturally — is an answer, not a new dead-end."""
        sid = "t-restate"
        await self._ask_turn(service, sid)
        p = self._answer_patches()
        with p[0], p[1], p[2] as w, p[3], p[4]:
            result = await service.process_intent(
                message=PM_RESTATEMENT, session_id=sid, user_id=_USER
            )
        assert w.await_count == 1
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert "Updated issue #108" in result.message

    async def test_unrelated_command_mid_ask_still_routes(self, service):
        """An off-intent command abandons the question via the pop and routes
        normally through the chain — nothing writes, no repo ask repeats."""
        sid = "t-offintent"
        await self._ask_turn(service, sid)
        explosive_write = patch(
            f"{ROUTER}.update_issue",
            new=AsyncMock(side_effect=AssertionError("off-intent turn must never write")),
        )
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            explosive_write,
        ):
            result = await service.process_intent(
                message="what reminders do I have?", session_id=sid, user_id=_USER
            )
        assert "Which repository" not in result.message
        assert _pending(service, sid) is None  # abandoned via the pop

    async def test_bare_yes_re_asks_and_re_arms(self, service):
        """'yes' answers nothing on the open question — the generic accept
        re-dispatches the original handler, which re-asks (self-re-arming)."""
        sid = "t-yes"
        await self._ask_turn(service, sid)
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            _resolver_unresolved(),
        ):
            result = await service.process_intent(
                message="yes", session_id=sid, user_id=_USER
            )
        assert "Which repository is issue #108 in?" in result.message
        assert _pending(service, sid) is not None

    async def test_decline_drops_honestly_and_nothing_fires(self, service):
        sid = "t-no"
        await self._ask_turn(service, sid)
        explosive_write = patch(
            f"{ROUTER}.update_issue",
            new=AsyncMock(side_effect=AssertionError("declined ask must never write")),
        )
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            explosive_write,
        ):
            result = await service.process_intent(
                message="no", session_id=sid, user_id=_USER
            )
        assert "I haven't touched issue #108" in result.message
        assert _pending(service, sid) is None

    async def test_unfound_answer_re_arms_with_honest_copy(self, service):
        sid = "t-unfound"
        await self._ask_turn(service, sid)
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            _no_default(),
            _adapter_with(_FULL),
        ):
            result = await service.process_intent(
                message="in the banana repository", session_id=sid, user_id=_USER
            )
        assert "couldn't find one called 'banana'" in result.message
        assert _pending(service, sid) is not None  # re-armed; the next answer still binds


# ---------------------------------------------------------------------------
# Close path — named repo honored; the dead-end asks
# ---------------------------------------------------------------------------


class TestClosePathRepoClarification:
    pytestmark = pytest.mark.asyncio

    def _close_intent(self, message, confirmed=True):
        ctx = {"original_message": message, "user_id": _USER}
        if confirmed:
            ctx["destructive_confirmed"] = True
        return Intent(
            category=IntentCategory.EXECUTION,
            action="close_issue",
            original_message=message,
            confidence=1.0,
            context=ctx,
        )

    async def test_named_repo_threads_into_the_close_write(self, service):
        closed = {"number": 108, "title": "t", "state": "closed", "html_url": ""}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=closed)) as w,
            patch(
                f"{REPO_CLAR}.resolve_repo_name",
                new=AsyncMock(
                    return_value=RepoNameResolution(status="resolved", full_name=_FULL)
                ),
            ),
        ):
            result = await service._handle_close_issue_query(
                self._close_intent(
                    "close issue #108 in the test-Piper-Morgan repository"
                ),
                "wf-close",
                session_id="sess-close-named",
            )
        assert result.success is True
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert w.await_args.kwargs["repo_name"] == "test-piper-morgan"

    async def test_unnamed_close_keeps_the_router_resolution_call_shape(self, service):
        """No named repo → the router resolves internally, exactly as before
        (#1042) — no owner/repo kwargs appear."""
        closed = {"number": 108, "title": "t", "state": "closed", "html_url": ""}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=closed)) as w,
        ):
            result = await service._handle_close_issue_query(
                self._close_intent("close issue #108"), "wf-close"
            )
        assert result.success is True
        w.assert_awaited_once_with(108, state="closed")

    async def test_close_repo_dead_end_becomes_the_bindable_question(self, service):
        """The router's 'no repo could be resolved' no longer dead-ends in a
        generic error — with a session it ARMS the repo question."""
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(
                f"{ROUTER}.update_issue",
                new=AsyncMock(
                    side_effect=RuntimeError(
                        "Cannot update GitHub issue #108: no repo could be resolved."
                    )
                ),
            ),
        ):
            result = await service._handle_close_issue_query(
                self._close_intent("close issue #108"),
                "wf-close",
                session_id="sess-close-ask",
            )
        assert result.success is True
        assert "Which repository is issue #108 in?" in result.message
        offer = _pending(service, "sess-close-ask")
        assert offer is not None
        assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND
        assert offer["pending_action"]["action"] == "close_issue"

    async def test_close_repo_dead_end_without_session_refuses_honestly(self, service):
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(
                f"{ROUTER}.update_issue",
                new=AsyncMock(
                    side_effect=RuntimeError(
                        "Cannot update GitHub issue #108: no repo could be resolved."
                    )
                ),
            ),
        ):
            result = await service._handle_close_issue_query(
                self._close_intent("close issue #108"), "wf-close"
            )
        assert result.success is False
        assert result.clarification_type == "repository_required"
        assert "set my default repo to" in result.message
