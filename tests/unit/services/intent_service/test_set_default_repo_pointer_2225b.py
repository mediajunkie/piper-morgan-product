"""#2225 second shape: ``set_default_github_repo`` is a registered rail op whose
handler returns CXO's Settings line and writes nothing.

LAYER: unit; the real IntentService rail (``_dispatch_action_rail``) with the LLM
boundary explosive and the repo-default setters patched to fail. DENOMINATOR: the one
op (dispatch, no-write, declared axes, catalog render).
"""

from unittest.mock import AsyncMock

import pytest

OP = "set_default_github_repo"
LINE = (
    "I can't change your default repository from chat. "
    "Open Settings → Integrations → GitHub to set it."
)
USER = "5a2c9d10-2225-4b00-9e00-00000000bbbb"


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def service():
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _intent():
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    msg = "Set my default GitHub repository to mediajunkie/piper-morgan-product"
    return Intent(
        category=IntentCategory.EXECUTION,
        action=OP,
        confidence=1.0,
        original_message=msg,
        context={"user_id": USER, "original_message": msg},
    )


async def _rail(service):
    return await service._dispatch_action_rail(
        _intent(),
        message="Set my default GitHub repository to mediajunkie/piper-morgan-product",
        session_id="s-2225b",
        user_id=USER,
        workflow_id=None,
        all_suggestions=None,
        preferences=None,
    )


@pytest.mark.asyncio
class TestPointerDispatch:
    async def test_dispatches_through_the_rail_and_returns_cxos_line_verbatim(self, service):
        outcome = await _rail(service)
        assert outcome.on_rail is True
        assert outcome.result is not None
        assert outcome.result.message == LINE
        assert outcome.result.success is True

    async def test_no_setter_and_no_github_write(self, service, monkeypatch):
        from services.connectors.config_service import ConnectorConfigService
        from services.intent.intent_service import IntentService

        boom = AsyncMock(side_effect=AssertionError("a default-repo setter was called"))
        monkeypatch.setattr(ConnectorConfigService, "set_default_repo", boom)
        monkeypatch.setattr(IntentService, "_handle_set_default_repo", boom)
        import services.integrations.github.repo_resolver as rr

        for name in dir(rr):
            if name.startswith(("set_", "save_", "write_", "persist_")) and callable(
                getattr(rr, name)
            ):
                monkeypatch.setattr(rr, name, boom)
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        write_boundaries = [
            n
            for n in dir(GitHubIntegrationRouter)
            if n.startswith(("create_", "update_", "close_", "reopen_", "comment_"))
        ]
        for name in write_boundaries:
            monkeypatch.setattr(GitHubIntegrationRouter, name, boom)
        outcome = await _rail(service)
        assert outcome.result.message == LINE
        boom.assert_not_called()


class TestRegistrationAndAxes:
    def test_declared_axes_are_read_private(self):
        from services.intent_service.acceptance import declared_axes_for_workflow
        from services.shared_types import EffectClass, Outwardness

        assert declared_axes_for_workflow(OP) == (EffectClass.READ, Outwardness.PRIVATE)

    def test_registered_action_triggered(self):
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        entry = get_action_workflows()[OP]
        assert entry.action_triggered is True

    def test_renders_into_the_router_catalog_with_description_and_example(self):
        from services.intent_service.inversion_router import derive_routing_grammar

        ops = {o.name: o for o in derive_routing_grammar().operations}
        assert OP in ops
        assert ops[OP].description == "Set the default GitHub repository for writes"
        assert ops[OP].example == "Set my default GitHub repository to owner/name"

    def test_axes_do_not_render_into_the_catalog_text(self):
        """Report-only pin of Arch's question: the declared axes are not catalog text."""
        from services.intent_service.inversion_router import derive_routing_grammar

        op = next(o for o in derive_routing_grammar().operations if o.name == OP)
        text = repr(op)
        assert "READ" not in text and "PRIVATE" not in text
