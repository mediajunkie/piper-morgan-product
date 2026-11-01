"""#2132 (i) — analyze_document binds only real referents (the handler half).

Arch (2026-10-22 15:05, 16:24, 18:5x): which handler owns an ask is meaning,
routed by corpus rows and entry descriptions; a handler checks state only. A
document ask resolves in order to (1) a file of the user's the turn binds, (2)
a Notion title (the router's title arg, else a classifier slot), with the page
named, (3) CXO's line. Never the top hit of a search on the bare message.

This is split (i) of Arch's 18:5x ruling: handler changes only, no catalog
text, so no rule-7 run. compare_documents, the #2133 decline and the routing
edits land in their own screened changes.

There is no chat-session file list in the product (uploads and artifacts are
owner-scoped and carry no session id), so a held file is what the summarize
rail's FileResolver binds from the message: a stored filename named verbatim,
or "the file I uploaded" with exactly one file. These pins run with no LLM and
no database: the DB, resolver and analyzer boundaries are stubbed.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.shared_types import IntentCategory

_USER = "3f7b8a52-2132-4b00-9e00-000000002132"
# #2138 (CXO 18:5x): Notion connected, nothing bound, no title.
NO_DOC_LINE = (
    "I couldn't tell which document you mean. Name an uploaded file or a "
    "Notion page, or paste the text here and I'll work with it."
)


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _notion_router():
    r = MagicMock()
    r.is_available.return_value = True
    r.ais_available = AsyncMock(return_value=True)  # #2238: the async gate
    r.connect_for_user = AsyncMock()
    r.search_notion = AsyncMock(return_value=[{"id": "page-x", "properties": {}}])
    r.get_page = AsyncMock(return_value={"title": "Some Page", "url": "u"})
    r.get_page_blocks = AsyncMock(return_value=[])
    return r


# ---------------------------------------------------------------------------
# 1. analyze_document: a held file (the summarize rail's resolver) comes first
# ---------------------------------------------------------------------------

_HELD = "services.intent_service.document_handlers.resolve_held_files"
_ANALYZE = "services.intent_service.document_handlers.handle_analyze_document"
_NOTION = "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"


def _analyze_intent(message, **ctx):
    return Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_document",
        original_message=message,
        context={"original_message": message, **ctx},
    )


class TestHeldFileFirst:
    @pytest.mark.asyncio
    async def test_owned_upload_named_with_notion_unavailable_is_analyzed(self, intent_service):
        """Lead's served case (Web, alpha fc183c41bc, Notion NOT connected):
        "Analyze launch-notes-2131.txt" after the upload got the
        Notion-not-connected line. The file is read first; no Notion line."""
        intent = _analyze_intent("Analyze launch-notes-2131.txt", user_id=_USER)
        router = _notion_router()
        router.is_available.return_value = False
        router.ais_available = AsyncMock(return_value=False)  # #2238
        held = AsyncMock(return_value=[{"file_id": "f-1", "filename": None}])
        analyze = AsyncMock(
            return_value={
                "file_id": "f-1",
                "filename": "launch-notes-2131.txt",
                "summary": "Launch notes.",
                "key_findings": ["Ship Friday"],
                "recommendations": [],
            }
        )
        with (
            patch(_NOTION, return_value=router),
            patch(_HELD, held),
            patch(_ANALYZE, analyze),
        ):
            result = await intent_service._handle_analyze_document_notion(intent, "wf", "s")

        held.assert_awaited_once_with("Analyze launch-notes-2131.txt", _USER, "analyze_document")
        analyze.assert_awaited_once_with("f-1", _USER)
        router.search_notion.assert_not_called()
        router.is_available.assert_not_called()
        router.ais_available.assert_not_awaited()  # #2238: the held file is answered before any gate
        assert "Notion" not in result.message
        assert "can't read your Notion pages" not in result.message
        assert result.message.startswith("I read 'launch-notes-2131.txt' from your files.")
        assert "Launch notes." in result.message and "- Ship Friday" in result.message

    @pytest.mark.asyncio
    async def test_named_held_file_beats_a_connected_notion(self, intent_service):
        intent = _analyze_intent("Analyze q3-plan.pdf", user_id=_USER)
        router = _notion_router()
        with (
            patch(_NOTION, return_value=router),
            patch(_HELD, AsyncMock(return_value=[{"file_id": "f-2", "filename": None}])),
            patch(
                _ANALYZE,
                AsyncMock(
                    return_value={"file_id": "f-2", "filename": "q3-plan.pdf", "summary": "S"}
                ),
            ),
        ):
            result = await intent_service._handle_analyze_document_notion(intent, "wf", "s")
        router.search_notion.assert_not_called()
        assert result.message.startswith("I read 'q3-plan.pdf' from your files.")

    @pytest.mark.asyncio
    async def test_nothing_held_and_notion_unavailable_names_no_notion(self, intent_service):
        intent = _analyze_intent("Analyze launch-notes-2131.txt", user_id=_USER)
        router = _notion_router()
        router.is_available.return_value = False
        router.ais_available = AsyncMock(return_value=False)  # #2238
        analyze = AsyncMock()
        with (
            patch(_NOTION, return_value=router),
            patch(_HELD, AsyncMock(return_value=[])),
            patch(_ANALYZE, analyze),
        ):
            result = await intent_service._handle_analyze_document_notion(intent, "wf", "s")
        analyze.assert_not_called()
        # #2138 (Arch 18:4x, step 3): Notion not connected → no Notion named.
        assert result.message == (
            "I don't see that document among your uploads. Paste the text here and I'll work with it."
        )
        assert "Notion" not in result.message

    @pytest.mark.asyncio
    async def test_several_named_files_are_listed_and_none_is_read(self, intent_service):
        intent = _analyze_intent("Analyze notes.md", user_id=_USER)
        analyze = AsyncMock()
        with (
            patch(
                _HELD,
                AsyncMock(
                    return_value=[
                        {"file_id": "a", "filename": "notes.md"},
                        {"file_id": "b", "filename": "notes.md"},
                    ]
                ),
            ),
            patch(_ANALYZE, analyze),
        ):
            result = await intent_service._handle_analyze_document_notion(intent, "wf", "s")
        analyze.assert_not_called()
        assert result.message.count("- notes.md") == 2
        assert "?" not in result.message  # stated, not asked (#1730)

    @pytest.mark.asyncio
    async def test_a_bound_notion_page_id_skips_the_file_lookup(self, intent_service):
        intent = _analyze_intent("Analyze it", user_id=_USER, document_id="page-x")
        held = AsyncMock(return_value=[])
        with patch(_NOTION, return_value=_notion_router()), patch(_HELD, held):
            await intent_service._handle_analyze_document_notion(intent, "wf", "s")
        held.assert_not_called()


# ---------------------------------------------------------------------------
# 1b. The live router's ``title`` arg is the Notion title (served fc183c41bc)
# ---------------------------------------------------------------------------


def _router_intent(message, args):
    ctx = {"original_message": message, "inversion_live": True}
    if args is not None:
        ctx["inversion_args"] = args
    return Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_document",
        original_message=message,
        context=ctx,
    )


async def _run_with_router(intent_service, intent):
    router = _notion_router()
    router.search_notion = AsyncMock(
        return_value=[
            {
                "id": "page-prd",
                "properties": {
                    "title": {"title": [{"text": {"content": "PRD Writing Guidelines"}}]}
                },
            }
        ]
    )
    router.get_page = AsyncMock(
        return_value={"title": "PRD Writing Guidelines", "url": "https://notion.so/prd"}
    )
    with patch(_NOTION, return_value=router):
        result = await intent_service._handle_analyze_document_notion(intent, "wf", "s")
    return router, result


class TestRouterTitleArg:
    @pytest.mark.asyncio
    async def test_router_title_is_searched_and_the_page_is_named(self, intent_service):
        intent = _router_intent(
            "Analyze the document called PRD Writing Guidelines",
            {"title": "PRD Writing Guidelines"},
        )
        router, result = await _run_with_router(intent_service, intent)
        assert router.search_notion.await_args.kwargs["query"] == "PRD Writing Guidelines"
        assert result.message.startswith("I read 'PRD Writing Guidelines' in Notion.")

    @pytest.mark.asyncio
    async def test_router_title_after_no_held_file_is_searched(self, intent_service):
        intent = _router_intent(
            "Analyze the document called PRD Writing Guidelines",
            {"title": "PRD Writing Guidelines"},
        )
        intent.context["user_id"] = _USER
        with patch(_HELD, AsyncMock(return_value=[])):
            router, result = await _run_with_router(intent_service, intent)
        assert router.search_notion.await_args.kwargs["query"] == "PRD Writing Guidelines"
        assert result.message.startswith("I read 'PRD Writing Guidelines' in Notion.")

    @pytest.mark.asyncio
    async def test_no_router_title_gets_cxos_line_and_no_search(self, intent_service):
        router, result = await _run_with_router(
            intent_service, _router_intent("Analyze this document", {})
        )
        router.search_notion.assert_not_called()
        assert result.message == NO_DOC_LINE

    @pytest.mark.asyncio
    @pytest.mark.parametrize("title", ["this document", "it", "the file", "this Notion page"])
    async def test_a_title_that_names_no_document_is_not_searched(self, intent_service, title):
        router, result = await _run_with_router(
            intent_service,
            _router_intent(f"Analyze {title} for me, this Notion page", {"title": title}),
        )
        router.search_notion.assert_not_called()
        assert result.message == NO_DOC_LINE

    @pytest.mark.asyncio
    async def test_a_title_with_words_the_user_did_not_say_is_not_searched(self, intent_service):
        router, result = await _run_with_router(
            intent_service,
            _router_intent("Analyze this document", {"title": "Q4 Roadmap"}),
        )
        router.search_notion.assert_not_called()
        assert result.message == NO_DOC_LINE

    @pytest.mark.asyncio
    async def test_non_string_title_is_ignored(self, intent_service):
        router, result = await _run_with_router(
            intent_service, _router_intent("Analyze this document", {"title": ["x"]})
        )
        router.search_notion.assert_not_called()
        assert result.message == NO_DOC_LINE


# ---------------------------------------------------------------------------
# 2. resolve_held_files: the summarize rail's FileResolver, confident binds only
# ---------------------------------------------------------------------------


class _Scope:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *exc):
        return False


def _resolver_returning(result=None, raises=None):
    resolver = MagicMock()
    if raises is not None:
        resolver.resolve_file_reference = AsyncMock(side_effect=raises)
    else:
        resolver.resolve_file_reference = AsyncMock(return_value=result)
    return resolver


class TestResolveHeldFiles:
    async def _run(self, resolver, message="Analyze launch-notes-2131.txt"):
        from services.intent_service import document_handlers

        with (
            patch.object(
                document_handlers.AsyncSessionFactory, "session_scope", return_value=_Scope()
            ),
            patch("services.file_context.file_resolver.FileResolver", return_value=resolver),
        ):
            return await document_handlers.resolve_held_files(message, _USER, "analyze_document")

    @pytest.mark.asyncio
    async def test_no_user_or_message_reads_nothing(self):
        from services.intent_service import document_handlers

        with patch.object(document_handlers, "AsyncSessionFactory") as factory:
            assert await document_handlers.resolve_held_files("Analyze x.txt", None, "a") == []
            assert await document_handlers.resolve_held_files("", _USER, "a") == []
            factory.session_scope.assert_not_called()

    @pytest.mark.asyncio
    async def test_a_named_file_binds(self):
        resolver = _resolver_returning(("f-1", 0.98))
        assert await self._run(resolver) == [{"file_id": "f-1", "filename": None}]
        view = resolver.resolve_file_reference.await_args.args[0]
        assert view.context["original_message"] == "Analyze launch-notes-2131.txt"
        assert resolver.resolve_file_reference.await_args.args[1] == _USER

    @pytest.mark.asyncio
    async def test_a_scored_pick_binds_like_summarize(self):
        """Arch 18:28 (#2138): the summarize contract, no extra cutoff. The
        resolver's own pick binds; its None is what falls through."""
        assert await self._run(_resolver_returning(("f-1", 0.62)), "Analyze this document") == [
            {"file_id": "f-1", "filename": None}
        ]

    @pytest.mark.asyncio
    async def test_nothing_resolved_binds_nothing(self):
        assert await self._run(_resolver_returning((None, 0.0))) == []

    @pytest.mark.asyncio
    async def test_exact_name_ambiguity_returns_every_named_file(self):
        from services.file_context.exceptions import AmbiguousFileReferenceError

        files = [MagicMock(id="a", filename="a.md"), MagicMock(id="b", filename="b.md")]
        got = await self._run(
            _resolver_returning(raises=AmbiguousFileReferenceError(files, [0.98, 0.98])),
            "Compare a.md and b.md",
        )
        assert got == [{"file_id": "a", "filename": "a.md"}, {"file_id": "b", "filename": "b.md"}]

    @pytest.mark.asyncio
    async def test_scored_ambiguity_returns_the_candidates(self):
        """Arch 18:28: an ambiguous match lists the candidates, as summarize does."""
        from services.file_context.exceptions import AmbiguousFileReferenceError

        files = [MagicMock(id="a", filename="a.md"), MagicMock(id="b", filename="b.md")]
        got = await self._run(
            _resolver_returning(raises=AmbiguousFileReferenceError(files, [0.6, 0.55])),
            "Analyze the notes",
        )
        assert got == [{"file_id": "a", "filename": "a.md"}, {"file_id": "b", "filename": "b.md"}]
