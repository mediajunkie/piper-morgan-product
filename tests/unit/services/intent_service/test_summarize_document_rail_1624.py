"""#1624 — chat document-summarize: the #1187-deferred `document` branch, finished.

Fifteen months of forensic history behind this file
(docs/internal/operations/summarize-intent-forensics-2026-08-15.md): chat
document-summarize NEVER worked end-to-end — acknowledgment theater (2025-06),
a real handler shipped dark (#290, 2025-11: chat dispatch existed only in a
guidance doc), the resolver stranded by the main.py gutting (2025-10), the
deferral closed untracked (#1187, 2026-06), and the source_type vocabulary
silently narrowed by the #1432 re-land (2026-08). PM ruled 2026-08-15: wire
chat to the SAME code path the working REST endpoint uses, and delete the dead
vocabulary honestly.

What this file pins:
  1. Wiring — registry canonical + verb-shim cell + rail keys + prompt vocab
     all name the same action, `summarize_document`; every OTHER summarize
     source stays floor-routed per #1158 (the shim cells stay None).
  2. Same-path — the rail handler calls `handle_summarize_document`, the
     function the REST route imports (identity-asserted), stubbed only at the
     DB/analyzer boundary so the REAL formatting path runs.
  3. Honesty — no uploaded document → a deterministic honest reply (never a
     fabricated summary, never floor improvisation); ambiguity → a question
     listing candidates; issue/commit-shaped requests fall through (None) to
     the working #1187 floor path.
  4. Option-C deletions stay deleted — the dormant `_handle_summarize`, the
     orphaned IntentEnricher, and the never-fired template rows.

Layer honesty (m-43): the end-to-end class drives the REAL
``IntentService.process_intent`` (the #1190/#1411/#1605 idiom), mocked ONLY at
the LLM boundary (explosive — classification stubbed deterministically) and
the file-store/analyzer boundary. The rail handler itself is real.
"""

import importlib
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.action_registry import (
    ACTION_REGISTRY,
    ActionDisposition,
    Verb,
    get_verb,
    verb_sourcetype_to_legacy_action,
)
from services.intent_service.classifier import IntentClassifier
from services.intent_service.workflow_dispatcher import (
    get_action_workflows,
    wired_chat_actions,
)
from services.intent_service.workflow_entries import (
    register_default_workflows,
    run_summarize_document_workflow,
)
from services.shared_types import EffectClass, IntentCategory, Outwardness

_USER = "3f7b8a52-1624-4b00-9e00-000000001624"  # valid UUID: survives principal parsing

_ALIASES = [
    "summarize_document",
    "summarize_file",
    "summarize_upload",
    "summarize_uploaded_file",
]


# ---------------------------------------------------------------------------
# 1. Wiring — one action name across every vocabulary surface
# ---------------------------------------------------------------------------


class TestSummarizeDocumentWiring:
    def test_all_aliases_dispatch_via_the_rail(self):
        register_default_workflows()
        keys = get_action_workflows().keys()
        for alias in _ALIASES:
            assert alias in keys, (
                f"{alias!r} must be rail-dispatchable — chat document-summarize "
                f"has no other dispatch surface (#1624)"
            )

    def test_aliases_share_one_entry(self):
        register_default_workflows()
        wf = get_action_workflows()
        assert len({id(wf[a]) for a in _ALIASES}) == 1

    def test_entry_declares_read_effect_and_private_outwardness(self):
        # effect: READ — owner-scoped SELECT + read-only analyze; no writes
        # (document_handlers.py). outwardness: PRIVATE — declared explicitly
        # per the #1624 build directive (#1509 axis).
        register_default_workflows()
        entry = get_action_workflows()["summarize_document"]
        assert entry.effect == EffectClass.READ
        assert entry.outwardness == Outwardness.PRIVATE
        assert entry.action_triggered is True

    def test_manifest_carries_the_capability_exactly_once(self):
        register_default_workflows()
        assert wired_chat_actions().count("summarize_document") == 1

    def test_registry_canonical_exists_and_is_workflow(self):
        assert ACTION_REGISTRY[("SYNTHESIS", "summarize_document")] is ActionDisposition.WORKFLOW
        assert get_verb("summarize_document") is Verb.SUMMARIZE

    def test_verb_shim_maps_document_and_only_document(self):
        """The one mapped SUMMARIZE cell is the uploaded-document source; every
        other source stays None → free-form action → SYNTHESIS → the #1187
        fetch-augment floor path (the #1158 ruling, unreversed)."""
        assert verb_sourcetype_to_legacy_action(Verb.SUMMARIZE, "document") == "summarize_document"
        for floor_source in ("github_issue", "commit_range", "text", "conversation", None):
            assert (
                verb_sourcetype_to_legacy_action(Verb.SUMMARIZE, floor_source) is None
            ), f"(SUMMARIZE, {floor_source!r}) must stay floor-routed"

    def test_prompt_teaches_the_restored_source_vocabulary(self):
        """Break 4 (forensics timeline, 5fba0f1be+7e866d87b): the 08-02 re-land
        dropped `document`/`conversation` from the source_type vocabulary the
        live classifier is taught. #1624 restores the #1158 5-set and teaches
        the document example the rail-keyed action."""
        from services.intent_service.prompts import INTENT_CLASSIFICATION_PROMPT

        assert (
            "github_issue, commit_range, text, conversation, document"
            in INTENT_CLASSIFICATION_PROMPT
        )
        assert '"action": "summarize_document"' in INTENT_CLASSIFICATION_PROMPT

    def test_classifier_normalization_targets_the_rail_key(self):
        """The #290 normalization ("summarize" → "summarize_document") was dead
        vocabulary for 15 months; the rail key makes it a live mode-4 net."""
        import inspect

        src = inspect.getsource(IntentClassifier)
        assert '"summarize": "summarize_document"' in src


# ---------------------------------------------------------------------------
# 2 + 3. Dispatch layer — same path as REST, honest in every failure shape
# ---------------------------------------------------------------------------


def _intent(message, source_type="document", action="summarize_document"):
    ctx = {"original_message": message}
    if source_type is not None:
        ctx["source_type"] = source_type
    return Intent(
        category=IntentCategory.SYNTHESIS,
        action=action,
        original_message=message,
        confidence=0.9,
        context=ctx,
    )


@asynccontextmanager
async def _fake_scope():
    yield MagicMock()


def _uploaded(filename, file_id="file-1624"):
    f = MagicMock()
    f.id = file_id
    f.filename = filename
    return f


def _boundary_patches(resolve=("file-1624", 0.92), resolve_exc=None, analysis=None):
    """Patch the DB-session/repository/resolver boundary + the analyzer
    boundary INSIDE handle_analyze_document — the REAL
    handle_summarize_document still runs (the same-path property under test)."""
    resolver_cls = MagicMock()
    if resolve_exc is not None:
        resolver_cls.return_value.resolve_file_reference = AsyncMock(side_effect=resolve_exc)
    else:
        resolver_cls.return_value.resolve_file_reference = AsyncMock(return_value=resolve)
    analyze = AsyncMock(
        return_value=analysis
        or {
            "file_id": "file-1624",
            "filename": "roadmap.pdf",
            "summary": ("The roadmap covers Q3. It has three phases. Risks are listed"),
            "key_findings": ["Phase gating", "Risk register"],
            "analyzed_at": "2026-08-16T00:00:00",
        }
    )
    return (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            _fake_scope,
        ),
        patch("services.repositories.file_repository.FileRepository", MagicMock()),
        patch("services.file_context.file_resolver.FileResolver", resolver_cls),
        patch(
            "services.intent_service.document_handlers.handle_analyze_document",
            analyze,
        ),
        resolver_cls,
        analyze,
    )


class TestSummarizeDocumentDispatch:
    def test_rest_and_rail_share_the_same_function(self):
        """Option A's definition: the chat handler calls the SAME code path the
        working REST endpoint uses. Identity, not similarity."""
        from services.intent_service import document_handlers
        from web.api.routes import documents as rest_documents

        assert (
            rest_documents.handle_summarize_document is document_handlers.handle_summarize_document
        )

    @pytest.mark.asyncio
    async def test_resolved_document_is_summarized_via_the_rest_path(self):
        p1, p2, p3, p4, resolver_cls, analyze = _boundary_patches()
        with p1, p2, p3, p4:
            result = await run_summarize_document_workflow(
                session_id="sess-1624",
                user_id=_USER,
                context={"intent": _intent("summarize this document")},
            )
        assert result is not None and result.success is True
        assert "Here's my summary of roadmap.pdf:" in result.message
        # REAL handle_summarize_document ran: bullet formatting applied to the
        # analyzer's summary (proof the chat turn traversed the REST function,
        # not a parallel renderer).
        assert "• The roadmap covers Q3" in result.message
        analyze.assert_awaited_once_with("file-1624", _USER)
        # owner-scoped resolution: the resolver was handed the USER id (the
        # repository has been owner-scoped since #1312).
        args = resolver_cls.return_value.resolve_file_reference.await_args.args
        assert args[1] == _USER
        assert result.intent_data["action"] == "summarize_document"

    @pytest.mark.asyncio
    async def test_no_uploaded_document_answers_honestly(self):
        """The failure case PM's 15-month theater lesson demands: no document
        → a deterministic honest reply. Never a fabricated summary, never a
        floor improvisation."""
        p1, p2, p3, p4, _resolver, analyze = _boundary_patches(resolve=(None, 0.0))
        with p1, p2, p3, p4:
            result = await run_summarize_document_workflow(
                session_id="sess-1624",
                user_id=_USER,
                context={"intent": _intent("summarize the document")},
            )
        assert result is not None and result.success is True
        assert "I don't see any uploaded documents" in result.message
        assert "summary of" not in result.message
        analyze.assert_not_awaited()
        assert result.intent_data["context"]["reason"] == "no_uploaded_documents"

    @pytest.mark.asyncio
    async def test_ambiguous_reference_asks_which_file(self):
        from services.file_context.exceptions import AmbiguousFileReferenceError

        exc = AmbiguousFileReferenceError(
            [_uploaded("roadmap.pdf"), _uploaded("budget.xlsx", "file-2")],
            [0.71, 0.69],
        )
        p1, p2, p3, p4, _resolver, analyze = _boundary_patches(resolve_exc=exc)
        with p1, p2, p3, p4:
            result = await run_summarize_document_workflow(
                session_id="sess-1624",
                user_id=_USER,
                context={"intent": _intent("summarize the document")},
            )
        assert result.requires_clarification is True
        assert "roadmap.pdf" in result.message and "budget.xlsx" in result.message
        analyze.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_issue_and_commit_shapes_fall_through_to_the_floor_path(self):
        """classifier.py's bare-"summarize" normalization can land issue/commit
        summarizes on this key; the handler must hand them back (None → the
        rail falls through to the working #1187 SYNTHESIS floor path)."""
        for msg, source in [
            ("summarize github issue #1124", "github_issue"),
            ("summarize the commits from last week", "commit_range"),
            ("summarize issue #42", None),
            ("summarize last week's commits", None),
        ]:
            result = await run_summarize_document_workflow(
                session_id="sess-1624",
                user_id=_USER,
                context={"intent": _intent(msg, source_type=source, action="summarize")},
            )
            assert result is None, f"{msg!r} must fall through to the floor path"

    @pytest.mark.asyncio
    async def test_missing_file_content_degrades_honestly(self):
        p1, p2, p3, p4, _resolver, analyze = _boundary_patches()
        analyze.side_effect = FileNotFoundError("gone")
        with p1, p2, p3, p4:
            result = await run_summarize_document_workflow(
                session_id="sess-1624",
                user_id=_USER,
                context={"intent": _intent("summarize the document")},
            )
        assert result.success is False
        assert "couldn't access" in result.message
        assert "summary of" not in result.message

    @pytest.mark.asyncio
    async def test_no_user_id_asks_for_sign_in(self):
        result = await run_summarize_document_workflow(
            session_id="sess-1624",
            user_id=None,
            context={"intent": _intent("summarize the document")},
        )
        assert result.success is True
        assert "signing in" in result.message


# ---------------------------------------------------------------------------
# E2E — a real chat turn through process_intent (explosive-LLM idiom)
# ---------------------------------------------------------------------------


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. The rail turn
    (and the honest no-document turn) must resolve without it."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1624 rail turns must resolve " "deterministically"
        )


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _stub_classification(monkeypatch, service, message):
    intent = _intent(message)

    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        return SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(service.intent_classifier, "classify_multiple", _classify_multiple)


class TestSummarizeDocumentEndToEnd:
    @pytest.mark.asyncio
    async def test_summarize_this_document_turn_reaches_the_rest_path(
        self, live_service, monkeypatch
    ):
        """The turn the issue is titled after, through the REAL process_intent:
        classified SYNTHESIS/summarize_document → pre-floor rail → the REST
        path's handle_summarize_document → a real summary in the reply. The
        floor LLM is explosive — if this turn improvised, it would blow up."""
        message = "summarize this document"
        _stub_classification(monkeypatch, live_service, message)
        p1, p2, p3, p4, _resolver, analyze = _boundary_patches()
        with p1, p2, p3, p4:
            result = await live_service.process_intent(
                message=message, session_id="e2e-1624", user_id=_USER
            )
        assert result.success is True
        assert "Here's my summary of roadmap.pdf:" in result.message
        assert "• The roadmap covers Q3" in result.message
        analyze.assert_awaited_once_with("file-1624", _USER)
        assert result.intent_data["action"] == "summarize_document"

    @pytest.mark.asyncio
    async def test_no_document_turn_answers_honestly_not_fabricated(
        self, live_service, monkeypatch
    ):
        """The failure case: same turn, nothing uploaded. The reply is the
        deterministic honest degrade — no summary, no theater, no floor
        improvisation (explosive LLM proves the floor was never consulted)."""
        message = "summarize this document"
        _stub_classification(monkeypatch, live_service, message)
        p1, p2, p3, p4, _resolver, analyze = _boundary_patches(resolve=(None, 0.0))
        with p1, p2, p3, p4:
            result = await live_service.process_intent(
                message=message, session_id="e2e-1624-none", user_id=_USER
            )
        assert result.success is True
        assert "I don't see any uploaded documents" in result.message
        assert "summary of" not in result.message
        analyze.assert_not_awaited()


# ---------------------------------------------------------------------------
# 4. Option-C deletions stay deleted
# ---------------------------------------------------------------------------


class TestDeadVocabularyStaysDeleted:
    def test_dormant_handle_summarize_is_gone(self):
        """Dormant since #1158 (summaries always floor; the structured renderer
        was ruled never-to-be-built). Recoverable at 2d8ccc5ac if ever needed."""
        assert not hasattr(IntentService, "_handle_summarize")
        assert not hasattr(IntentService, "_summarize_with_llm")
        assert not hasattr(IntentService, "_format_summary")
        assert not hasattr(IntentService, "_extract_text_content")

    def test_fetch_helpers_survive_the_deletion(self):
        """The LIVE #1187 fetch path must not ride along with the dead wrapper."""
        assert hasattr(IntentService, "_fetch_summary_source_content")
        assert hasattr(IntentService, "_fetch_issue_content")
        assert hasattr(IntentService, "_fetch_commit_content")

    def test_intent_enricher_module_is_gone(self):
        """Orphaned since the 2025-10-01 main.py gutting (zero non-test callers,
        forensics-verified); its live half, FileResolver, is consumed by the
        rail handler instead."""
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module("services.intent_service.intent_enricher")

    def test_never_fired_template_rows_are_gone(self):
        from services.ui_messages.templates import INTENT_BASED_TEMPLATES

        assert ("synthesis", "summarize_document") not in INTENT_BASED_TEMPLATES
        assert ("synthesis", "summarize_file") not in INTENT_BASED_TEMPLATES
