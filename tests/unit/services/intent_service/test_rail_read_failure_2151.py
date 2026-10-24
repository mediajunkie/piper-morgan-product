"""#2151 step 3, RAIL-FALLTHROUGH: a READ rail entry that raises says it couldn't check.

Before: ``dispatch_workflow`` swallowed the handler's exception and returned None, and
the chat rail treated None as "not mine", so the turn fell through to the floor, which
answered as if the read had never been asked for. Arch's ruling (#2151, 6377720778): an
exception on the rail is a failed outcome. CXO's words (17:55): one template, a
source noun and an unknown clause per READ entry, in ONE registry.

LAYER: unit; the real IntentService rail (``_dispatch_action_rail``) with the LLM
boundary explosive and the entry's handler forced to raise. DENOMINATOR: every
canonical action-triggered READ entry is in the registry or the no-user-data list
(derived from WORKFLOW_REGISTRY); the rail behaviour on one READ entry, one alias, one
no-user-data entry and one WRITE entry; the other ``dispatch_workflow`` callers keep None.
"""

from unittest.mock import AsyncMock

import pytest

from services.intent_service.rail_read_failure import (
    NO_USER_DATA_READ,
    RAIL_READ_FAILED_TEMPLATE,
    RAIL_READ_SOURCES,
    RAIL_WRITE_SOURCES,
    rail_read_failed_message,
    rail_write_unconfirmed_message,
)
from services.shared_types import EffectClass


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


def _canonical_read_entries():
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    seen, out = set(), []
    for key, entry in WORKFLOW_REGISTRY.items():
        if not entry.action_triggered or id(entry) in seen:
            continue
        seen.add(id(entry))
        if entry.effect is EffectClass.READ:
            out.append(key)
    return out


class TestOneRegistry:
    def test_every_read_entry_is_worded_or_listed_as_no_user_data(self):
        reads = _canonical_read_entries()
        assert len(reads) > 0
        missing = [k for k in reads if k not in RAIL_READ_SOURCES and k not in NO_USER_DATA_READ]
        assert not missing, (
            f"READ entries with no couldn't-check words: {missing}. Add a "
            "(source_noun, unknown_clause) to RAIL_READ_SOURCES (CXO's template), or list it "
            "in NO_USER_DATA_READ with the reason it reads none of the user's data."
        )

    def test_no_stale_or_doubled_rows(self):
        reads = set(_canonical_read_entries())
        assert set(RAIL_READ_SOURCES) <= reads, set(RAIL_READ_SOURCES) - reads
        assert set(NO_USER_DATA_READ) <= reads, set(NO_USER_DATA_READ) - reads
        assert not set(RAIL_READ_SOURCES) & set(NO_USER_DATA_READ)

    def test_every_write_and_destructive_entry_has_outcome_unknown_words(self):
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        seen, writes = set(), []
        for key, entry in WORKFLOW_REGISTRY.items():
            if not entry.action_triggered or id(entry) in seen:
                continue
            seen.add(id(entry))
            if entry.effect in (EffectClass.WRITE, EffectClass.DESTRUCTIVE):
                writes.append(key)
        assert writes
        missing = [k for k in writes if k not in RAIL_WRITE_SOURCES]
        assert not missing, (
            f"WRITE/DESTRUCTIVE entries with no outcome-unknown words: {missing}. Add an "
            "(action_phrase, where_to_look) to RAIL_WRITE_SOURCES (CXO's case-2 template)."
        )
        assert set(RAIL_WRITE_SOURCES) <= set(writes), set(RAIL_WRITE_SOURCES) - set(writes)

    def test_the_template_renders_cxos_words(self):
        assert rail_read_failed_message("list_prs") == (
            "I couldn't check your GitHub pull requests just now, so I can't say which ones "
            "are open. Try again in a moment; if it keeps failing, tell us."
        )
        assert rail_read_failed_message("prioritize") is None
        assert "{source_noun}" in RAIL_READ_FAILED_TEMPLATE


@pytest.fixture
def service():
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _intent(action):
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=1.0,
        original_message="show me",
        context={"user_id": "5a2c9d10-2151-4b00-9e00-00000000aaaa", "original_message": "show me"},
    )


async def _rail_with_raising_handler(service, monkeypatch, action):
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY

    entry = WORKFLOW_REGISTRY[action]
    monkeypatch.setattr(entry, "entry_point", AsyncMock(side_effect=RuntimeError("read blew up")))
    return await service._dispatch_action_rail(
        _intent(action),
        message="show me",
        session_id="s-2151",
        user_id="5a2c9d10-2151-4b00-9e00-00000000aaaa",
        workflow_id=None,
        all_suggestions=None,
        preferences=None,
    )


async def _raised_step(service, monkeypatch, action):
    """dispatch_workflow(raise_errors=True) raises; the rail's handler renders the reply."""
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY, dispatch_workflow

    entry = WORKFLOW_REGISTRY[action]
    monkeypatch.setattr(entry, "entry_point", AsyncMock(side_effect=RuntimeError("write blew up")))
    with pytest.raises(RuntimeError):
        await dispatch_workflow(action, session_id="s", user_id="u", raise_errors=True)
    return service._rail_read_failed_result(_intent(action), entry)


@pytest.mark.asyncio
class TestTheRailSaysItCouldNotCheck:
    async def test_a_read_entry_that_raises_says_so_and_does_not_fall_through(
        self, service, monkeypatch
    ):
        outcome = await _rail_with_raising_handler(service, monkeypatch, "list_todos_query")
        assert outcome.on_rail is True
        assert outcome.result is not None, "fell through to the floor (RAIL-FALLTHROUGH)"
        assert outcome.result.message == rail_read_failed_message("list_todos_query")
        assert outcome.result.success is False
        assert outcome.result.intent_data["context"]["read_failed"] == "rail_exception"

    async def test_an_alias_gets_its_canonical_entrys_words(self, service, monkeypatch):
        outcome = await _rail_with_raising_handler(service, monkeypatch, "list_reminders")
        assert outcome.result is not None
        assert outcome.result.message == rail_read_failed_message("list_reminders_query")

    async def test_a_no_user_data_read_keeps_the_old_fall_through(self, service, monkeypatch):
        outcome = await _rail_with_raising_handler(service, monkeypatch, "prioritize")
        assert outcome.on_rail is True and outcome.result is None

    async def test_a_write_entry_that_raised_says_it_cant_confirm(self, service, monkeypatch):
        """CXO 10-23 18:22 case 2: a write that raised may have gone through."""
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY

        # A write reaches dispatch only past the consent/confirm gates (which this
        # turn's "show me" would stop at), so the raised step is driven directly,
        # as the #2151 forcing test does: dispatch raises, the rail renders the result.
        entry = WORKFLOW_REGISTRY["archive_project"]
        assert entry.effect is EffectClass.WRITE
        result = await _raised_step(service, monkeypatch, "archive_project")
        assert result is not None, "a write that raised fell through to the floor"
        assert result.message == (
            "I couldn't finish archiving that project just now, and I can't confirm whether it "
            "went through. Check your projects list before you ask again, so it isn't done twice."
        )
        assert result.success is False
        assert result.intent_data["context"]["read_failed"] == "rail_write_exception_unconfirmed"

    async def test_a_destructive_entry_gets_the_same_line(self, service, monkeypatch):
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY

        assert WORKFLOW_REGISTRY["unlink_repo"].effect is EffectClass.DESTRUCTIVE
        result = await _raised_step(service, monkeypatch, "unlink_repo")
        assert result is not None
        assert result.message == rail_write_unconfirmed_message("unlink_repo")


@pytest.mark.asyncio
async def test_other_dispatch_callers_still_get_none(monkeypatch):
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY, dispatch_workflow
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    monkeypatch.setattr(
        WORKFLOW_REGISTRY["list_todos_query"],
        "entry_point",
        AsyncMock(side_effect=RuntimeError("x")),
    )
    assert await dispatch_workflow("list_todos_query", session_id="s", user_id="u") is None
    with pytest.raises(RuntimeError):
        await dispatch_workflow("list_todos_query", session_id="s", user_id="u", raise_errors=True)


@pytest.mark.asyncio
async def test_a_failed_clear_todos_read_says_only_the_couldnt_check_sentence(service, monkeypatch):
    """CXO 10-23 18:12: clear_todos' failed read must never imply anything was cleared or kept."""
    outcome = await _rail_with_raising_handler(service, monkeypatch, "clear_todos")
    assert outcome.result is not None
    assert outcome.result.message == (
        "I couldn't check your tasks and reminders just now, so I can't say which ones would be "
        "cleared. Try again in a moment; if it keeps failing, tell us."
    )
