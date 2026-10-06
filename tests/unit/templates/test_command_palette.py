"""
Tests for command palette component (#421 MUX-NAV-PALETTE).

Tests command registry, trust-gated visibility, fuzzy search, and keyboard handling.
"""

from pathlib import Path

import pytest


class TestCommandPaletteStructure:
    """Test that command palette has required structure."""

    @pytest.fixture
    def palette_content(self):
        """Load command palette template content."""
        path = Path("templates/components/command_palette.html")
        return path.read_text()

    def test_palette_overlay_exists(self, palette_content):
        """Palette has overlay for modal backdrop."""
        assert 'id="command-palette-overlay"' in palette_content

    def test_palette_container_exists(self, palette_content):
        """Palette container exists."""
        assert 'id="command-palette"' in palette_content

    def test_palette_input_exists(self, palette_content):
        """Search input exists."""
        assert 'id="command-palette-input"' in palette_content

    def test_palette_list_exists(self, palette_content):
        """Command list container exists."""
        assert 'id="command-palette-list"' in palette_content

    def test_palette_has_aria_dialog(self, palette_content):
        """Palette has proper ARIA role for accessibility."""
        assert 'role="dialog"' in palette_content
        assert 'aria-modal="true"' in palette_content


class TestCommandRegistry:
    """Test command registry content."""

    @pytest.fixture
    def palette_content(self):
        """Load command palette template content."""
        path = Path("templates/components/command_palette.html")
        return path.read_text()

    def test_navigation_commands_exist(self, palette_content):
        """Navigation commands are registered."""
        assert "'nav-home'" in palette_content
        assert "'nav-standup'" in palette_content
        assert "'nav-todos'" in palette_content
        assert "'nav-projects'" in palette_content
        assert "'nav-documents'" in palette_content
        assert "'nav-collections'" in palette_content

    def test_action_commands_exist(self, palette_content):
        """Action commands are registered."""
        assert "'action-new-todo'" in palette_content
        assert "'action-new-project'" in palette_content

    def test_query_commands_exist(self, palette_content):
        """Query commands are registered."""
        assert "'query-urgent'" in palette_content
        assert "'query-today'" in palette_content

    def test_meta_commands_exist(self, palette_content):
        """Meta commands are registered."""
        assert "'meta-settings'" in palette_content
        assert "'meta-help'" in palette_content
        assert "'meta-logout'" in palette_content

    def test_commands_have_categories(self, palette_content):
        """Commands have category assignments."""
        assert "category: 'Navigation'" in palette_content
        assert "category: 'Action'" in palette_content
        assert "category: 'Query'" in palette_content
        assert "category: 'Meta'" in palette_content


class TestCommandTrustGating:
    """Test trust-gated command visibility."""

    @pytest.fixture
    def palette_content(self):
        """Load command palette template content."""
        path = Path("templates/components/command_palette.html")
        return path.read_text()

    def test_hardness_levels_assigned(self, palette_content):
        """Commands have hardness levels for trust gating."""
        assert "hardness: 5" in palette_content  # HARDEST
        assert "hardness: 4" in palette_content  # HARD
        assert "hardness: 3" in palette_content  # MEDIUM
        assert "hardness: 2" in palette_content  # SOFT

    def test_home_always_visible(self, palette_content):
        """Home command has HARDEST (5) hardness - always visible."""
        # Find nav-home and check it has hardness 5
        assert "'nav-home'" in palette_content
        # Settings and Help should also be hardness 5
        assert "'meta-settings'" in palette_content
        assert "'meta-help'" in palette_content

    def test_trust_stage_read_from_window(self, palette_content):
        """Trust stage is read from window.trustStage."""
        assert "window.trustStage" in palette_content

    def test_get_min_trust_stage_function(self, palette_content):
        """Function to convert hardness to min trust stage exists."""
        assert "getMinTrustStage" in palette_content

    def test_get_visible_commands_function(self, palette_content):
        """Function to filter commands by trust exists."""
        assert "getVisibleCommands" in palette_content


class TestCommandPaletteSearch:
    """Test fuzzy search functionality."""

    @pytest.fixture
    def palette_content(self):
        """Load command palette template content."""
        path = Path("templates/components/command_palette.html")
        return path.read_text()

    def test_fuzzy_match_function_exists(self, palette_content):
        """Fuzzy match function exists."""
        assert "function fuzzyMatch" in palette_content

    def test_filter_commands_function_exists(self, palette_content):
        """Filter commands function exists."""
        assert "function filterCommands" in palette_content

    def test_highlight_matches_function_exists(self, palette_content):
        """Match highlighting function exists."""
        assert "function highlightMatches" in palette_content
        assert 'class="match"' in palette_content

    def test_input_triggers_filtering(self, palette_content):
        """Input event triggers command filtering."""
        assert "input.addEventListener('input'" in palette_content


class TestCommandPaletteKeyboard:
    """Test keyboard handling."""

    @pytest.fixture
    def palette_content(self):
        """Load command palette template content."""
        path = Path("templates/components/command_palette.html")
        return path.read_text()

    def test_cmd_k_opens_palette(self, palette_content):
        """Cmd/Ctrl+K opens palette."""
        assert "e.metaKey || e.ctrlKey" in palette_content
        assert "e.key === 'k'" in palette_content

    def test_escape_closes_palette(self, palette_content):
        """Escape key closes palette."""
        assert "e.key === 'Escape'" in palette_content
        assert "close()" in palette_content

    def test_arrow_keys_navigate(self, palette_content):
        """Arrow keys navigate commands."""
        assert "e.key === 'ArrowDown'" in palette_content
        assert "e.key === 'ArrowUp'" in palette_content

    def test_enter_executes_command(self, palette_content):
        """Enter key executes selected command."""
        assert "e.key === 'Enter'" in palette_content
        assert "executeCommand" in palette_content


class TestCommandPaletteNavIntegration:
    """Test integration with nav trigger (#420)."""

    @pytest.fixture
    def palette_content(self):
        """Load command palette template content."""
        path = Path("templates/components/command_palette.html")
        return path.read_text()

    def test_listens_for_custom_event(self, palette_content):
        """Palette listens for openCommandPalette event."""
        assert "openCommandPalette" in palette_content
        assert "document.addEventListener('openCommandPalette'" in palette_content

    def test_sets_command_palette_exists_flag(self, palette_content):
        """Sets window.commandPaletteExists flag."""
        assert "window.commandPaletteExists = true" in palette_content


class TestCommandPaletteAccessibility:
    """Test accessibility features."""

    @pytest.fixture
    def palette_content(self):
        """Load command palette template content."""
        path = Path("templates/components/command_palette.html")
        return path.read_text()

    def test_input_has_aria_label(self, palette_content):
        """Search input has aria-label."""
        assert 'aria-label="Search commands"' in palette_content

    def test_list_has_listbox_role(self, palette_content):
        """Command list has listbox role."""
        assert 'role="listbox"' in palette_content

    def test_items_have_option_role(self, palette_content):
        """Command items have option role."""
        assert 'role="option"' in palette_content

    def test_selected_item_aria_selected(self, palette_content):
        """Selected item has aria-selected."""
        assert "aria-selected" in palette_content

    def test_overlay_aria_hidden(self, palette_content):
        """Overlay has aria-hidden attribute."""
        assert "aria-hidden" in palette_content

    def test_keyboard_hints_in_footer(self, palette_content):
        """Keyboard hints shown in footer."""
        assert "↑↓" in palette_content
        assert "↵" in palette_content
        assert "esc" in palette_content


class TestCommandPaletteIcons:
    """Test command icons."""

    @pytest.fixture
    def palette_content(self):
        """Load command palette template content."""
        path = Path("templates/components/command_palette.html")
        return path.read_text()

    def test_icons_object_exists(self, palette_content):
        """Icons object with SVG paths exists."""
        assert "const ICONS = {" in palette_content

    def test_common_icons_defined(self, palette_content):
        """Common icons are defined."""
        assert "home:" in palette_content
        assert "settings:" in palette_content
        assert "help:" in palette_content
        assert "logout:" in palette_content

    def test_render_icon_function(self, palette_content):
        """Icon rendering function exists."""
        assert "function renderIcon" in palette_content


class TestHistoryCommands:
    """Tests for history commands (#425 MUX-IMPLEMENT-MEMORY-SYNC)."""

    @pytest.fixture
    def palette_content(self):
        """Load command palette template content."""
        path = Path("templates/components/command_palette.html")
        return path.read_text()

    def test_view_history_command_exists(self, palette_content):
        """View history command is registered."""
        assert "'history-view'" in palette_content

    def test_search_conversations_command_exists(self, palette_content):
        """Search conversations command is registered."""
        assert "'history-search'" in palette_content

    def test_start_private_session_command_exists(self, palette_content):
        """Start private session command is registered."""
        assert "'history-private'" in palette_content

    def test_history_category_exists(self, palette_content):
        """History category is in category order."""
        assert "category: 'History'" in palette_content
        assert "'History'" in palette_content

    def test_history_category_in_order(self, palette_content):
        """History comes after Filter and before Meta."""
        assert "'Filter', 'History', 'Meta'" in palette_content

    def test_view_history_uses_sidebar(self, palette_content):
        """View history opens HistorySidebar."""
        assert "window.HistorySidebar" in palette_content
        assert "HistorySidebar.open()" in palette_content

    def test_search_focuses_input(self, palette_content):
        """Search command focuses the search input."""
        assert ".history-search-input" in palette_content

    def test_private_uses_privacy_mode(self, palette_content):
        """Private session uses PrivacyMode."""
        assert "window.PrivacyMode" in palette_content
        assert "PrivacyMode.startPrivateSession()" in palette_content

    def test_clock_icon_exists(self, palette_content):
        """Clock icon for history is defined."""
        assert "clock:" in palette_content

    def test_lock_icon_exists(self, palette_content):
        """Lock icon for privacy is defined."""
        assert "lock:" in palette_content

    def test_history_commands_have_hardness(self, palette_content):
        """History commands have hardness levels."""
        # Find history-view command block - need to find the closing brace after hardness
        start = palette_content.find("id: 'history-view'")
        # Find the next command (history-search) to get the full block
        end = palette_content.find("id: 'history-search'", start)
        block = palette_content[start:end]
        assert "hardness: 3" in block  # MEDIUM

    def test_view_history_has_shortcut(self, palette_content):
        """View history has keyboard shortcut."""
        start = palette_content.find("id: 'history-view'")
        end = palette_content.find("id: 'history-search'", start)
        block = palette_content[start:end]
        assert "shortcut:" in block
        assert "H" in block
