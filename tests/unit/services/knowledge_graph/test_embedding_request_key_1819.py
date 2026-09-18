"""#1819 — KG embeddings resolve their OpenAI credential at SPEND time, never server-owned.

Before: ``DocumentIngester.embedding_function`` read the SERVER's OpenAI key from the
keychain (``ingestion.py:50``) and baked it into ChromaDB's ``OpenAIEmbeddingFunction`` —
every embedding (document ingest, semantic search) billed a product-owned credential,
bypassing the #1809-inverted chokepoint entirely. PM ruled the server key "is not a real
concept" (#1812, decisions.log 2026-09-14 ×2).

RED evidence (pre-fix tree, 2026-09-18 probe):
    keychain read for provider: call('openai')
    embedding fn constructed with: sk-SERVER-KEYCHAIN-OPENAI

Now ``RequestKeyedOpenAIEmbeddingFunction`` holds NO key and asks ``request_spend_key
("openai")`` at each call: the user's own bound key, or the operator's explicit
authorization (#1807 seam — the CLI ingest path), or an honest ``UnboundLLMKeyError``.
"""

from unittest.mock import MagicMock, patch

import pytest

from services.knowledge_graph.ingestion import RequestKeyedOpenAIEmbeddingFunction
from services.llm.request_key import (
    OPERATOR_SERVER_KEY_ENV,
    LLMKeyRequiredError,
    UnboundLLMKeyError,
    request_api_key,
)

USER_OPENAI_KEY = "sk-user-openai-EMBED"


class TestRequestKeyedEmbeddingFunction:
    def test_unbound_refuses_and_never_touches_the_keychain(self):
        """THE #1819 pin (red on the pre-fix tree: keychain read + server key baked in)."""
        fn = RequestKeyedOpenAIEmbeddingFunction()
        with patch("services.knowledge_graph.ingestion.KeychainService") as keychain_cls:
            with pytest.raises(UnboundLLMKeyError):
                fn(["some document text"])
        keychain_cls.assert_not_called()
        keychain_cls.return_value.get_api_key.assert_not_called()

    def test_bound_user_key_embeds_on_the_users_own_key(self):
        fn = RequestKeyedOpenAIEmbeddingFunction()
        with patch(
            "services.knowledge_graph.ingestion.embedding_functions.OpenAIEmbeddingFunction"
        ) as ef_cls:
            ef_cls.return_value.return_value = [[0.1, 0.2]]
            with patch("services.knowledge_graph.ingestion.KeychainService") as keychain_cls:
                with request_api_key({"openai": USER_OPENAI_KEY}):
                    out = fn(["some document text"])
        assert out == [[0.1, 0.2]]
        assert ef_cls.call_args.kwargs["api_key"] == USER_OPENAI_KEY
        keychain_cls.assert_not_called()  # the user's key means no server credential read

    def test_an_anthropic_binding_does_not_authorize_an_embedding_spend(self):
        """#1815's constraint applied to embeddings: an Anthropic key never pays OpenAI."""
        fn = RequestKeyedOpenAIEmbeddingFunction()
        with request_api_key("sk-ant-user-KEY"):
            with pytest.raises(UnboundLLMKeyError):
                fn(["text"])

    def test_operator_binding_with_gate_uses_the_operators_server_credential(self, monkeypatch):
        """The CLI ingest path (#1807 seam): explicit None binding + gate 1 → the
        operator's own keychain (or env) credential — the one surviving server-side
        spend, until #1812 step 5."""
        monkeypatch.setenv(OPERATOR_SERVER_KEY_ENV, "1")
        fn = RequestKeyedOpenAIEmbeddingFunction()
        with patch("services.knowledge_graph.ingestion.KeychainService") as keychain_cls:
            keychain_cls.return_value.get_api_key.return_value = "sk-OPERATOR-KEYCHAIN"
            with patch(
                "services.knowledge_graph.ingestion.embedding_functions.OpenAIEmbeddingFunction"
            ) as ef_cls:
                ef_cls.return_value.return_value = [[0.3]]
                with request_api_key(None):
                    out = fn(["text"])
        assert out == [[0.3]]
        keychain_cls.return_value.get_api_key.assert_called_once_with("openai")
        assert ef_cls.call_args.kwargs["api_key"] == "sk-OPERATOR-KEYCHAIN"

    def test_operator_binding_without_gate_refuses(self):
        with request_api_key(None):
            with pytest.raises(UnboundLLMKeyError):
                RequestKeyedOpenAIEmbeddingFunction()(["text"])

    def test_no_key_is_cached_across_requests(self):
        """The wrapper is cacheable on the module-singleton ingester precisely because
        the credential decision happens per call — two requests, two different keys."""
        fn = RequestKeyedOpenAIEmbeddingFunction()
        seen = []
        with patch(
            "services.knowledge_graph.ingestion.embedding_functions.OpenAIEmbeddingFunction"
        ) as ef_cls:
            ef_cls.return_value.return_value = [[0.0]]
            with request_api_key({"openai": "sk-user-A"}):
                fn(["a"])
            seen.append(ef_cls.call_args.kwargs["api_key"])
            with request_api_key({"openai": "sk-user-B"}):
                fn(["b"])
            seen.append(ef_cls.call_args.kwargs["api_key"])
        assert seen == ["sk-user-A", "sk-user-B"]
        with pytest.raises(UnboundLLMKeyError):
            fn(["c"])  # and between requests: refusal, not residue

    def test_ingester_property_builds_the_wrapper_without_reading_any_key(self, tmp_path):
        """#1452 lazy-construction guarantee holds a fortiori: constructing the
        embedding function reads NOTHING — keyless environments never raise here."""
        from services.knowledge_graph.ingestion import DocumentIngester

        with patch("services.knowledge_graph.ingestion.KeychainService") as keychain_cls:
            ingester = DocumentIngester(chroma_path=str(tmp_path / "chroma"))
            fn = ingester.embedding_function
        assert isinstance(fn, RequestKeyedOpenAIEmbeddingFunction)
        keychain_cls.assert_not_called()


class TestFindDecisionsSurfacesTheRefusal:
    @pytest.mark.asyncio
    async def test_find_decisions_reraises_a_key_refusal_instead_of_fallback_mode(self):
        """#1809/#1815-Gap-2 at the KG read path: a spend refusal must reach the route
        (which turns it into the honest 'add your OpenAI key' 403), not degrade into a
        quietly empty 'fallback_mode' result."""
        from services.knowledge_graph.document_service import DocumentService

        ingester = MagicMock()
        type(ingester).collection = property(
            lambda self: (_ for _ in ()).throw(UnboundLLMKeyError("no key"))
        )
        svc = DocumentService(session_scope=MagicMock(), ingester=ingester)
        with pytest.raises(LLMKeyRequiredError):
            await svc.find_decisions(topic="pricing")

    @pytest.mark.asyncio
    async def test_a_non_refusal_failure_still_degrades_to_fallback_mode(self):
        """The carve-out is ONLY for the refusal family — infrastructure failures keep
        the existing honest-degradation contract."""
        from services.knowledge_graph.document_service import DocumentService

        ingester = MagicMock()
        type(ingester).collection = property(
            lambda self: (_ for _ in ()).throw(RuntimeError("chroma down"))
        )
        svc = DocumentService(session_scope=MagicMock(), ingester=ingester)
        result = await svc.find_decisions(topic="pricing")
        assert result["fallback_mode"] is True
        assert result["decisions"] == []
