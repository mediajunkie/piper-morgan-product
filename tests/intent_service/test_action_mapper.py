"""
Unit tests for ActionMapper (Issue #284, #294)

Tests the action mapping logic for EXECUTION category actions.

ActionMapper handles EXECUTION category actions ONLY.
Other categories (QUERY, ANALYSIS, SYNTHESIS) route by category
and don't use action name mapping.

These tests verify:
- EXECUTION action variations map to correct handler methods
- Unknown actions fall back gracefully
- Mapping is consistent with execution handler expectations
"""

import pytest

from services.intent_service.action_mapper import ActionMapper


class TestActionMapper:
    """Test ActionMapper functionality - EXECUTION actions only"""

    # ===== GITHUB ACTIONS (EXECUTION category) =====

    def test_github_issue_create_mapping(self):
        """Test create_github_issue maps to create_issue"""
        result = ActionMapper.map_action("create_github_issue")
        assert result == "create_issue"

    def test_github_issue_create_item_mapping(self):
        """Test create_item maps to create_issue"""
        result = ActionMapper.map_action("create_item")
        assert result == "create_issue"

    def test_github_issue_update_mapping(self):
        """Test update_github_issue maps to update_issue"""
        result = ActionMapper.map_action("update_github_issue")
        assert result == "update_issue"

    def test_update_ticket_mapping(self):
        """Test update_ticket maps to update_issue"""
        result = ActionMapper.map_action("update_ticket")
        assert result == "update_issue"

    def test_make_github_issue_mapping(self):
        """Test make_github_issue maps to create_issue"""
        result = ActionMapper.map_action("make_github_issue")
        assert result == "create_issue"

    # ===== TODO ACTIONS (EXECUTION category) =====

    def test_add_todo_mapping(self):
        """Test add_todo maps to create_todo (Issue #285)"""
        result = ActionMapper.map_action("add_todo")
        assert result == "create_todo"

    def test_mark_done_mapping(self):
        """Test mark_done maps to complete_todo (Issue #285)"""
        result = ActionMapper.map_action("mark_done")
        assert result == "complete_todo"

    def test_show_todos_mapping(self):
        """Test show_todos maps to list_todos"""
        result = ActionMapper.map_action("show_todos")
        assert result == "list_todos"

    def test_remove_todo_mapping(self):
        """Test remove_todo maps to delete_todo"""
        result = ActionMapper.map_action("remove_todo")
        assert result == "delete_todo"

    def test_add_reminder_mapping(self):
        """Test add_reminder maps to create_reminder (#1426).

        Census D3 (2026-07-16): the LLM classifier emits `add_reminder` for
        some reminder phrasings; unmapped, it fell through to the contextual
        fallback instead of the shipped #903 create_reminder handler. Same
        alias idiom as add_todo -> create_todo.
        """
        result = ActionMapper.map_action("add_reminder")
        assert result == "create_reminder"

    # ===== FALLBACK BEHAVIOR =====

    def test_unmapped_action_fallback(self):
        """Test unmapped action returns original action"""
        result = ActionMapper.map_action("unknown_action_xyz")
        assert result == "unknown_action_xyz"

    def test_empty_action_returns_unknown_intent(self):
        """Test empty action string returns unknown_intent"""
        result = ActionMapper.map_action("")
        assert result == "unknown_intent"

    def test_none_action_returns_unknown_intent(self):
        """Test None action returns unknown_intent"""
        result = ActionMapper.map_action(None)
        assert result == "unknown_intent"

    # ===== METADATA TESTS =====

    def test_mapping_count(self):
        """Test that core EXECUTION mappings exist (Issue #294, refactored #1046).

        Original (#294): asserted exact count == 26. Brittle magic-number
        assertion that broke whenever normal feature work added a mapping
        (count drifted to 31 by 2026-05-03 → silent FAIL until surfaced
        during #790 sweep). Replaced with a name-based existence check
        + lower-bound count per #1046 Option B.
        """
        mappings = ActionMapper.list_all_mappings()

        # All entries must be string→string (the registry contract).
        for k, v in mappings.items():
            assert isinstance(k, str) and isinstance(
                v, str
            ), f"Non-string mapping entry: {k!r} → {v!r}"

        # Core EXECUTION mappings that every release must carry. New
        # mappings are normal feature work and should not break this test;
        # missing core mappings are real regressions.
        core_mappings = {
            "create_github_issue": "create_issue",
            "update_github_issue": "update_issue",
            "create_todo": "create_todo",
            "list_todos": "list_todos",
            "complete_todo": "complete_todo",
        }
        for source, expected_canonical in core_mappings.items():
            assert source in mappings, f"Core EXECUTION mapping {source!r} missing from registry"
            assert mappings[source] == expected_canonical, (
                f"Core mapping {source!r} drifted: "
                f"expected {expected_canonical!r}, got {mappings[source]!r}"
            )

        # Sanity lower-bound (we'd never drop below the core set).
        assert len(mappings) >= len(
            core_mappings
        ), f"Mapping registry shrunk below core: {len(mappings)} < {len(core_mappings)}"

    def test_get_mapping_coverage(self):
        """Test mapping coverage calculation"""
        test_actions = ["create_github_issue", "unknown_action", "add_todo"]
        coverage = ActionMapper.get_mapping_coverage(test_actions)
        assert coverage == pytest.approx(66.67, rel=0.1)  # 2 out of 3 mapped

    def test_dynamic_add_mapping(self):
        """Test dynamically adding a new mapping"""
        ActionMapper.add_mapping("test_action", "test_handler")
        result = ActionMapper.map_action("test_action")
        assert result == "test_handler"

        # Clean up
        ActionMapper.ACTION_MAPPING.pop("test_action", None)
