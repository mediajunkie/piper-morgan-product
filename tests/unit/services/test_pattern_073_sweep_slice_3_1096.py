"""
Tests for #1096 slice 3 Pattern-073 fixes — sweep of consciousness +
intent_service handler empty-state / future-promise copy.

Slice 3 (this file) covers:
- format_patterns_learned_conscious: dropped "I'll keep these in mind
  going forward" — the intent_service._learn_*_patterns methods do NOT
  persist patterns; the assertion promised future memory the system
  doesn't deliver
- handle_next_todo empty state: "nothing pending" → "no active todos"
  to bound the claim to what was queried
"""

import inspect
from pathlib import Path

import pytest


@pytest.fixture
def learning_consciousness_source() -> str:
    return Path("services/consciousness/learning_consciousness.py").read_text()


@pytest.fixture
def todo_handlers_source() -> str:
    return Path("services/intent_service/todo_handlers.py").read_text()


# format_patterns_learned_conscious ---------------------------------------


def test_patterns_learned_does_not_promise_persistent_memory(
    learning_consciousness_source: str,
) -> None:
    """Pattern-073: 'I'll keep these in mind going forward' was a future-tense
    promise of persistent memory the intent_service._learn_*_patterns flow
    doesn't deliver (patterns computed inline, returned in intent_data,
    not persisted to a store future inferences read)."""
    # Look for the surface assertion in the actual returned strings (not docstrings)
    # Find the function body
    src = learning_consciousness_source
    start = src.find("def format_patterns_learned_conscious")
    end = src.find("def format_preference_saved_conscious")
    assert start >= 0 and end > start
    block = src[start:end]
    # The promised-future phrasing must be gone
    assert "I'll keep these in mind going forward" not in block, (
        "Pattern-073 violation: promised persistent memory the system doesn't deliver"
    )


def test_patterns_learned_describes_bounded_scope(
    learning_consciousness_source: str,
) -> None:
    """Replacement copy describes that patterns are computed from the data
    just looked at + flags that cross-session persistence is a separate feature."""
    assert "data I just looked at" in learning_consciousness_source
    assert "Persisting them across sessions is a separate feature" in learning_consciousness_source


def test_patterns_learned_documents_pattern_073_reason(
    learning_consciousness_source: str,
) -> None:
    """Per close-issue-properly + Pattern-073 discipline: the WHY is in
    a comment so a future agent doesn't restore the over-claim."""
    assert "#1096 slice 3" in learning_consciousness_source
    assert "Pattern-073" in learning_consciousness_source


# handle_next_todo empty-state --------------------------------------------


def test_next_todo_empty_state_does_not_assert_nothing_pending(
    todo_handlers_source: str,
) -> None:
    """Pattern-073: 'nothing pending' is a categorical claim that exceeds
    the bounded knowledge 'list_todos returned 0 active todos'. Check that
    the phrase does not appear inside a triple-quoted or regular string
    literal that gets returned to the user (the explanatory comment may
    legitimately reference the old phrase to document the discipline)."""
    src = todo_handlers_source
    start = src.find("async def handle_next_todo")
    end = src.find("async def handle_complete_todo")
    assert start >= 0 and end > start
    block = src[start:end]
    # The phrase must not appear inside a quoted return-string literal
    # (i.e., after `return (` or `return "` patterns within the block).
    # Simple heuristic: check that "nothing pending!" with the bang doesn't appear
    # (the old copy had that exclamation; comments don't).
    assert "nothing pending!" not in block, (
        "Pattern-073 violation: 'nothing pending!' phrasing must be removed "
        "from rendered output"
    )


def test_next_todo_empty_state_uses_bounded_observation(
    todo_handlers_source: str,
) -> None:
    """The replacement copy describes 'active todos' (what was queried) and
    'there are none' (the bounded observation)."""
    src = todo_handlers_source
    start = src.find("async def handle_next_todo")
    end = src.find("async def handle_complete_todo")
    block = src[start:end]
    assert "active todos" in block
    assert "there are none" in block


def test_next_todo_empty_state_documents_discipline(
    todo_handlers_source: str,
) -> None:
    """The change includes a comment citing #1096 + Pattern-073."""
    src = todo_handlers_source
    start = src.find("async def handle_next_todo")
    end = src.find("async def handle_complete_todo")
    block = src[start:end]
    assert "#1096 slice 3" in block
    assert "Pattern-073" in block
