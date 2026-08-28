"""#1641 — the #1567 repo-question carrier wired onto the remaining call sites.

#1567 gave the update/close handlers the bindable "which repository?" question
(kind ``issue_repo_question`` on the #1190 action-agnostic carrier) and natural
repo-phrasing extraction. #1641 wires the rest:

1. **reopen + comment handlers** get the same shape — explicit/natural repo
   honoring, the carrier armed on repository-not-specified (session-gated; no
   session → the old honest refusal), ``session_id`` threaded where missing.
2. **The three ANALYSIS dead-ends** (analyze_commits / generate_report /
   analyze_data) consult the message + the #1411 default repo
   (``resolve_repo`` via ``_resolve_default_repository``) before asking; the
   armed question's answer re-dispatches the ORIGINAL intent through the rail
   and lands back in the SAME analysis handler.
3. **The create path** resolves natural "in the X repository" phrasing via the
   same extraction the answers use; owner/name keeps working; a user-NAMED
   repo that doesn't resolve asks — never silently falls to the default.

Layer honesty (m-43): copy/verb-family units are pure; handler-level tests
drive the REAL handlers with the router/resolver/repo-search patched at their
seams. The arm→answer→proceed tests drive the ANSWER turn (and, where a
deterministic route exists — reopen and comment ride the pre-classifier —
the ARM turn too) through the REAL ``process_intent`` with an EXPLOSIVE LLM;
the ANALYSIS/create arms are handler-level because no deterministic surface
claims those phrasings (the LLM classifier is the only route, and it must
never fire in these tests).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.repo_clarification import (
    REPO_QUESTION_KIND,
    RepoNameResolution,
    build_repo_question_offer,
    open_repo_question,
    repo_question_decline_message,
    restatement_verbs_for,
)
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
RESOLVER = "services.integrations.github.repo_resolver"
REPO_CLAR = "services.intent_service.repo_clarification"
ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
GH_DOMAIN = "services.domain.github_domain_service.GitHubDomainService"
EXTRACT_SLOTS = "services.slot_filling.slot_extractor.extract_slots"

_USER = "3f7b8a52-1641-4b00-9e00-000000001641"  # valid UUID
_FULL = "mediajunkie/test-piper-morgan"

NATURAL_ANSWER = "in the test-Piper-Morgan repository"


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


def _resolver_unresolved():
    from services.integrations.github.repo_resolver import UnresolvedRepoError

    return patch(f"{RESOLVER}.resolve_repo", new=AsyncMock(side_effect=UnresolvedRepoError()))


def _repos_result(*full_names):
    return MagicMock(
        degradation=None,
        repositories=[{"name": fn.split("/", 1)[1], "full_name": fn} for fn in full_names],
    )


def _adapter_with(*full_names):
    instance = MagicMock()
    instance.search_user_repositories = AsyncMock(return_value=_repos_result(*full_names))
    return patch(f"{ADAPTER}", return_value=instance)


def _no_default():
    return patch(f"{RESOLVER}.get_user_default_repo", new=AsyncMock(return_value=None))


def _resolved_name():
    return patch(
        f"{REPO_CLAR}.resolve_repo_name",
        new=AsyncMock(return_value=RepoNameResolution(status="resolved", full_name=_FULL)),
    )


def _gh_domain(activity=None):
    activity = activity or {
        "commits": [],
        "prs": [],
        "issues_created": [],
        "issues_closed": [],
    }
    instance = MagicMock()
    instance._github_agent.get_recent_activity = AsyncMock(return_value=activity)
    return patch(GH_DOMAIN, return_value=instance)


def _intent(action, message, category=IntentCategory.EXECUTION, **extra_ctx):
    ctx = {"original_message": message, "user_id": _USER, **extra_ctx}
    return Intent(
        category=category,
        action=action,
        original_message=message,
        confidence=1.0,
        context=ctx,
    )


# ---------------------------------------------------------------------------
# Units — the carrier's non-issue-anchored form and the new verb families
# ---------------------------------------------------------------------------


class TestCarrierGeneralizationUnits:
    def test_open_question_issue_form_unchanged(self):
        assert open_repo_question(108).startswith("Which repository is issue #108 in?")

    def test_open_question_operation_form(self):
        q = open_repo_question(None, "analyze commits")
        assert q.startswith("Which repository should I use to analyze commits?")
        assert "owner/name" in q

    def test_decline_copy_issue_form_unchanged(self):
        assert "I haven't touched issue #108" in repo_question_decline_message(108)

    def test_decline_copy_operation_form_names_no_issue(self):
        msg = repo_question_decline_message(None, "generate the report")
        assert "#" not in msg
        assert "generate the report" in msg

    def test_offer_without_issue_number_skips_issue_summary(self):
        intent = _intent("analyze_commits", "analyze commits", IntentCategory.ANALYSIS)
        offer = build_repo_question_offer(intent, None, _USER, operation="analyze commits")
        payload = offer["pending_action"]
        assert payload["kind"] == REPO_QUESTION_KIND
        assert payload["issue_number"] is None
        assert payload["summary"] == "analyze commits"
        assert payload["operation"] == "analyze commits"

    @pytest.mark.parametrize(
        "action,expected_verb",
        [
            ("close_issue", "close"),
            ("reopen_issue_query", "reopen"),
            ("comment_issue_query", "comment"),
            ("add_comment", "comment"),
            ("generate_report", "generate"),
            ("create_report", "generate"),  # report family, NOT issue-create
            ("analyze_commits", "analyze"),
            ("evaluate_metrics", "analyze"),
            ("create_issue", "create"),
            ("update_issue", "change"),
        ],
    )
    def test_restatement_families(self, action, expected_verb):
        assert expected_verb in restatement_verbs_for(action)


# ---------------------------------------------------------------------------
# Wiring 1a — the reopen handler gets the #1567 shape
# ---------------------------------------------------------------------------


class TestReopenRepoWiring:
    pytestmark = pytest.mark.asyncio

    def _reopen_intent(self, message, confirmed=True):
        extra = {"destructive_confirmed": True} if confirmed else {}
        return _intent("reopen_issue_query", message, IntentCategory.QUERY, **extra)

    async def test_named_repo_threads_into_the_reopen_write(self, service):
        reopened = {"number": 108, "title": "t", "state": "open", "html_url": ""}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=reopened)) as w,
            _resolved_name(),
        ):
            result = await service._handle_reopen_issue_query(
                self._reopen_intent("reopen issue #108 in the test-Piper-Morgan repository"),
                "wf-reopen",
                session_id="sess-reopen-named",
            )
        assert result.success is True
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert w.await_args.kwargs["repo_name"] == "test-piper-morgan"
        assert w.await_args.kwargs["state"] == "open"

    async def test_unnamed_reopen_keeps_the_router_resolution_call_shape(self, service):
        """No named repo → the router resolves internally, exactly as before
        (#1042) — no owner/repo kwargs appear."""
        reopened = {"number": 108, "title": "t", "state": "open", "html_url": ""}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=reopened)) as w,
        ):
            result = await service._handle_reopen_issue_query(
                self._reopen_intent("reopen issue #108"), "wf-reopen"
            )
        assert result.success is True
        w.assert_awaited_once_with(108, state="open")

    async def test_reopen_dead_end_becomes_the_bindable_question(self, service):
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
            result = await service._handle_reopen_issue_query(
                self._reopen_intent("reopen issue #108"),
                "wf-reopen",
                session_id="sess-reopen-ask",
            )
        assert result.success is True
        assert "Which repository is issue #108 in?" in result.message
        offer = _pending(service, "sess-reopen-ask")
        assert offer is not None
        assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND
        assert offer["pending_action"]["action"] == "reopen_issue_query"

    async def test_reopen_dead_end_without_session_refuses_honestly(self, service):
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
            result = await service._handle_reopen_issue_query(
                self._reopen_intent("reopen issue #108"), "wf-reopen"
            )
        assert result.success is False
        assert result.clarification_type == "repository_required"
        assert "set my default repo to" in result.message

    async def test_reopen_arm_answer_proceed_full_journey(self, service):
        """The pinned journey through the REAL process_intent: 'reopen issue
        #108' (pre-classified deterministically) → the #1190 destructive
        confirm → 'yes' → the handler hits the no-repo dead-end and ARMS the
        repo question → the natural answer binds and the reopen proceeds."""
        sid = "t-reopen-e2e"
        no_repo = RuntimeError("Cannot update GitHub issue #108: no repo could be resolved.")
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        ):
            r1 = await service.process_intent(
                message="reopen issue #108", session_id=sid, user_id=_USER
            )
        assert "yes" in r1.message.lower()  # the destructive confirm ask
        assert _pending(service, sid) is not None

        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(side_effect=no_repo)),
        ):
            r2 = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert "Which repository is issue #108 in?" in r2.message
        offer = _pending(service, sid)
        assert offer is not None
        assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND

        reopened = {
            "number": 108,
            "title": "t",
            "state": "open",
            "html_url": f"https://github.com/{_FULL}/issues/108",
        }
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=reopened)) as w,
            _no_default(),
            _adapter_with(_FULL),
        ):
            r3 = await service.process_intent(message=NATURAL_ANSWER, session_id=sid, user_id=_USER)
        assert w.await_count == 1
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert w.await_args.kwargs["repo_name"] == "test-piper-morgan"
        assert w.await_args.kwargs["state"] == "open"
        assert "Reopened issue #108" in r3.message
        assert _pending(service, sid) is None


# ---------------------------------------------------------------------------
# Wiring 1b — the comment handler gets the #1567 shape
# ---------------------------------------------------------------------------


def _slots_patch(issue_number="123", comment_text="looks great"):
    return patch(
        EXTRACT_SLOTS,
        new_callable=AsyncMock,
        return_value={"issue_number": issue_number, "comment_text": comment_text},
    )


class TestCommentRepoWiring:
    pytestmark = pytest.mark.asyncio

    def _comment_intent(self, message):
        return _intent("comment_issue_query", message, IntentCategory.QUERY)

    async def test_natural_named_repo_threads_into_add_comment(self, service):
        service.llm_client = MagicMock()
        posted = {"html_url": f"https://github.com/{_FULL}/issues/123#c1"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.add_comment", new=AsyncMock(return_value=posted)) as w,
            _slots_patch(),
            _resolved_name(),
        ):
            result = await service._handle_comment_issue_query(
                self._comment_intent(
                    "comment on issue #123 in the test-Piper-Morgan repository saying looks great"
                ),
                "wf-comment",
                session_id="sess-comment-named",
            )
        assert result.success is True
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert w.await_args.kwargs["repo_name"] == "test-piper-morgan"

    async def test_repo_phrase_inside_comment_text_is_not_routing(self, service):
        """The scrubbed scan: a comment BODY mentioning '... in the config
        repository' must not be read as repo routing — the write goes through
        the router's own internal resolution, and no name lookup fires."""
        service.llm_client = MagicMock()
        body = "we should track this in the config repository"
        posted = {"html_url": "https://github.com/o/r/issues/123#c1"}
        explosive_resolution = patch(
            f"{REPO_CLAR}.resolve_repo_name",
            new=AsyncMock(side_effect=AssertionError("body prose must not resolve")),
        )
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.add_comment", new=AsyncMock(return_value=posted)) as w,
            _slots_patch(comment_text=body),
            explosive_resolution,
        ):
            result = await service._handle_comment_issue_query(
                self._comment_intent(f"comment on issue #123 saying {body}"),
                "wf-comment",
                session_id="sess-comment-body",
            )
        assert result.success is True
        w.assert_awaited_once_with(123, body)  # no owner/repo kwargs

    async def test_comment_dead_end_becomes_the_bindable_question(self, service):
        service.llm_client = MagicMock()
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(
                f"{ROUTER}.add_comment",
                new=AsyncMock(
                    side_effect=RuntimeError(
                        "Cannot add comment to GitHub issue #123: no repo could be resolved."
                    )
                ),
            ),
            _slots_patch(),
        ):
            result = await service._handle_comment_issue_query(
                self._comment_intent("comment on issue #123 saying looks great"),
                "wf-comment",
                session_id="sess-comment-ask",
            )
        assert result.success is True
        assert "Which repository is issue #123 in?" in result.message
        offer = _pending(service, "sess-comment-ask")
        assert offer is not None
        assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND
        assert offer["pending_action"]["action"] == "comment_issue_query"

    async def test_comment_dead_end_without_session_keeps_the_honest_copy(self, service):
        service.llm_client = MagicMock()
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(
                f"{ROUTER}.add_comment",
                new=AsyncMock(
                    side_effect=RuntimeError(
                        "Cannot add comment to GitHub issue #123: no repo could be resolved."
                    )
                ),
            ),
            _slots_patch(),
        ):
            result = await service._handle_comment_issue_query(
                self._comment_intent("comment on issue #123 saying looks great"),
                "wf-comment",
            )
        assert "couldn't tell which repository" in result.message
        assert result.requires_clarification is True

    async def test_comment_arm_answer_proceed_e2e(self, service):
        """arm→answer→proceed through the REAL process_intent: the comment ask
        (pre-classified deterministically) hits the no-repo dead-end and ARMS;
        the owner/name answer binds and the ORIGINAL comment posts."""
        service.llm_client = MagicMock()
        sid = "t-comment-e2e"
        no_repo = RuntimeError(
            "Cannot add comment to GitHub issue #123: no repo could be resolved."
        )
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.add_comment", new=AsyncMock(side_effect=no_repo)),
            _slots_patch(),
        ):
            r1 = await service.process_intent(
                message="comment on issue #123 saying looks great",
                session_id=sid,
                user_id=_USER,
            )
        assert "Which repository is issue #123 in?" in r1.message
        assert _pending(service, sid) is not None

        posted = {"html_url": f"https://github.com/{_FULL}/issues/123#c1"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.add_comment", new=AsyncMock(return_value=posted)) as w,
            _slots_patch(),
        ):
            r2 = await service.process_intent(message=_FULL, session_id=sid, user_id=_USER)
        assert w.await_count == 1
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert w.await_args.kwargs["repo_name"] == "test-piper-morgan"
        assert w.await_args.args[1] == "looks great"  # the ORIGINAL comment
        assert "Successfully added comment to issue #123" in r2.message
        assert _pending(service, sid) is None


# ---------------------------------------------------------------------------
# Wiring 2 — the three ANALYSIS dead-ends
# ---------------------------------------------------------------------------


class TestAnalysisRepoWiring:
    pytestmark = pytest.mark.asyncio

    async def test_default_repo_consulted_before_asking(self, service):
        """#1411 path: no repo in the ask → resolve_repo's answer is used
        without any question."""
        default = MagicMock(full_name=_FULL)
        with (
            _gh_domain(),
            patch(f"{RESOLVER}.resolve_repo", new=AsyncMock(return_value=default)) as rr,
        ):
            result = await service._handle_analyze_commits(
                _intent(
                    "analyze_commits", "analyze commits from the last week", IntentCategory.ANALYSIS
                ),
                "wf-ana",
            )
        assert result.success is True
        assert f"No commits found in {_FULL}" in result.message
        rr.assert_awaited_once()

    async def test_named_repo_in_ask_beats_the_default(self, service):
        """Natural phrasing in the ORIGINAL ask resolves — the default is
        never consulted for a user-NAMED repo."""
        explosive_default = patch(
            f"{RESOLVER}.resolve_repo",
            new=AsyncMock(side_effect=AssertionError("default must not be consulted")),
        )
        with _gh_domain(), explosive_default, _resolved_name():
            result = await service._handle_analyze_commits(
                _intent(
                    "analyze_commits",
                    "analyze commits in the test-Piper-Morgan repository",
                    IntentCategory.ANALYSIS,
                ),
                "wf-ana",
            )
        assert result.success is True
        assert f"No commits found in {_FULL}" in result.message

    async def test_no_repo_arms_the_operation_question(self, service):
        with _resolver_unresolved():
            result = await service._handle_analyze_commits(
                _intent(
                    "analyze_commits", "analyze commits from the last week", IntentCategory.ANALYSIS
                ),
                "wf-ana",
                session_id="sess-ana-ask",
            )
        assert result.success is True
        assert "Which repository should I use to analyze commits?" in result.message
        offer = _pending(service, "sess-ana-ask")
        assert offer is not None
        assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND
        assert offer["pending_action"]["action"] == "analyze_commits"
        assert offer["pending_action"]["issue_number"] is None

    async def test_no_repo_without_session_keeps_the_old_refusal(self, service):
        with _resolver_unresolved():
            result = await service._handle_analyze_commits(
                _intent(
                    "analyze_commits", "analyze commits from the last week", IntentCategory.ANALYSIS
                ),
                "wf-ana",
            )
        assert result.success is False
        assert result.message == (
            "Cannot analyze commits: repository not specified. " "Please specify which repository."
        )
        assert result.clarification_type == "repository_required"

    async def _arm_and_answer(self, service, handler_attr, action, sid):
        """Arm via the real handler (no deterministic classifier surface
        exists for analysis asks), answer through the REAL process_intent."""
        with _resolver_unresolved():
            ask = await getattr(service, handler_attr)(
                _intent(action, "run it for me please", IntentCategory.ANALYSIS),
                "wf-ana",
                session_id=sid,
            )
        assert "Which repository" in ask.message
        assert _pending(service, sid) is not None

        with _gh_domain(), _no_default(), _adapter_with(_FULL):
            result = await service.process_intent(
                message=NATURAL_ANSWER, session_id=sid, user_id=_USER
            )
        assert _pending(service, sid) is None
        return result

    async def test_analyze_commits_arm_answer_lands_back_in_the_same_handler(self, service):
        result = await self._arm_and_answer(
            service, "_handle_analyze_commits", "analyze_commits", "t-ana-commits"
        )
        assert f"No commits found in {_FULL}" in result.message

    async def test_generate_report_arm_answer_lands_back_in_the_same_handler(self, service):
        result = await self._arm_and_answer(
            service, "_handle_generate_report", "generate_report", "t-ana-report"
        )
        assert f"Generated commit_analysis report for {_FULL}" in result.message

    async def test_analyze_data_arm_answer_lands_back_in_the_same_handler(self, service):
        result = await self._arm_and_answer(
            service, "_handle_analyze_data", "analyze_data", "t-ana-data"
        )
        assert f"Analyzed repository metrics for {_FULL}" in result.message

    async def test_analysis_decline_drops_honestly(self, service):
        sid = "t-ana-decline"
        with _resolver_unresolved():
            await service._handle_analyze_commits(
                _intent("analyze_commits", "analyze recent commits", IntentCategory.ANALYSIS),
                "wf-ana",
                session_id=sid,
            )
        explosive_activity = patch(
            GH_DOMAIN, side_effect=AssertionError("declined ask must not analyze")
        )
        with explosive_activity:
            result = await service.process_intent(message="no", session_id=sid, user_id=_USER)
        assert "Name the repository" in result.message
        assert "#" not in result.message  # no phantom issue number
        assert _pending(service, sid) is None


# ---------------------------------------------------------------------------
# Wiring 3 — the create path resolves natural phrasing
# ---------------------------------------------------------------------------


def _github_config():
    return patch(
        "services.configuration.piper_config_loader.piper_config_loader.load_github_config",
        return_value=MagicMock(default_labels=[]),
    )


def _gate_open():
    return patch(
        "services.intent_service.collaboration_gate.gate_holds",
        new=AsyncMock(return_value=False),
    )


class TestCreateNaturalPhrasing:
    pytestmark = pytest.mark.asyncio

    CREATE_MSG = "create an issue in the test-Piper-Morgan repository about flaky login tests"

    def _create_intent(self, message):
        return _intent("create_issue", message)

    async def test_natural_phrasing_resolves_and_create_proceeds(self, service):
        created = {
            "number": 5,
            "title": "flaky login tests",
            "html_url": f"https://github.com/{_FULL}/issues/5",
        }
        explosive_default = patch(
            f"{RESOLVER}.get_user_default_repo",
            new=AsyncMock(side_effect=AssertionError("default must not be consulted")),
        )
        with (
            _gate_open(),
            _github_config(),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            _resolved_name(),
            explosive_default,
        ):
            result = await service._handle_create_issue(
                self._create_intent(self.CREATE_MSG),
                "wf-create",
                "sess-create-natural",
                user_id=_USER,
            )
        assert result.success is True
        assert w.await_count == 1
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert w.await_args.kwargs["repo_name"] == "test-piper-morgan"
        assert w.await_args.kwargs["title"] == "flaky login tests"
        assert "Created issue #5" in result.message

    async def test_owner_name_form_still_works_without_name_resolution(self, service):
        created = {"number": 6, "title": "flaky login tests", "html_url": ""}
        explosive_resolution = patch(
            f"{REPO_CLAR}.resolve_repo_name",
            new=AsyncMock(side_effect=AssertionError("owner/name needs no lookup")),
        )
        with (
            _gate_open(),
            _github_config(),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            explosive_resolution,
        ):
            result = await service._handle_create_issue(
                self._create_intent(f"create an issue in {_FULL} about flaky login tests"),
                "wf-create",
                "sess-create-owner",
                user_id=_USER,
            )
        assert result.success is True
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert w.await_args.kwargs["repo_name"] == "test-piper-morgan"

    async def test_named_but_unfound_create_asks_and_never_writes(self, service):
        explosive_write = patch(
            f"{ROUTER}.create_issue",
            new=AsyncMock(side_effect=AssertionError("unresolved name must not write")),
        )
        with (
            _gate_open(),
            _github_config(),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            explosive_write,
            _no_default(),
            patch(
                f"{REPO_CLAR}.resolve_repo_name",
                new=AsyncMock(return_value=RepoNameResolution(status="not_found")),
            ),
        ):
            result = await service._handle_create_issue(
                self._create_intent(self.CREATE_MSG),
                "wf-create",
                "sess-create-unfound",
                user_id=_USER,
            )
        assert result.requires_clarification is True
        assert "couldn't find one called 'test-Piper-Morgan'" in result.message
        offer = _pending(service, "sess-create-unfound")
        assert offer is not None
        assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND
        assert offer["pending_action"]["operation"] == "create the issue"

    async def test_named_but_unfound_create_without_session_refuses(self, service):
        with (
            _gate_open(),
            _github_config(),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            _no_default(),
            patch(
                f"{REPO_CLAR}.resolve_repo_name",
                new=AsyncMock(return_value=RepoNameResolution(status="not_found")),
            ),
        ):
            result = await service._handle_create_issue(
                self._create_intent(self.CREATE_MSG),
                "wf-create",
                None,
                user_id=_USER,
            )
        assert "couldn't match 'test-Piper-Morgan'" in result.message
        assert result.clarification_type == "repository_required"

    async def test_create_arm_answer_proceed_e2e_binding(self, service):
        """The armed create question binds through the REAL process_intent:
        the owner/name answer re-dispatches the ORIGINAL create intent and
        the issue lands in the named repo."""
        sid = "t-create-e2e"
        with (
            _gate_open(),
            _github_config(),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            _no_default(),
            patch(
                f"{REPO_CLAR}.resolve_repo_name",
                new=AsyncMock(return_value=RepoNameResolution(status="not_found")),
            ),
        ):
            ask = await service._handle_create_issue(
                self._create_intent(self.CREATE_MSG), "wf-create", sid, user_id=_USER
            )
        assert "couldn't find one called 'test-Piper-Morgan'" in ask.message
        assert _pending(service, sid) is not None

        created = {"number": 7, "title": "flaky login tests", "html_url": ""}
        with (
            _github_config(),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
        ):
            result = await service.process_intent(message=_FULL, session_id=sid, user_id=_USER)
        assert w.await_count == 1
        assert w.await_args.kwargs["owner"] == "mediajunkie"
        assert w.await_args.kwargs["repo_name"] == "test-piper-morgan"
        assert w.await_args.kwargs["title"] == "flaky login tests"
        assert "Created issue #7" in result.message
        assert _pending(service, sid) is None
