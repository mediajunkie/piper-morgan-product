"""
Unit tests for History Sidebar Component (#425 MUX-IMPLEMENT-MEMORY-SYNC)

Tests the history_sidebar.html component for:
- Date grouping (today, yesterday, this week, older)
- Search functionality
- Privacy controls
- Conversation item display
- Pagination
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def history_html():
    """Load the history sidebar component HTML."""
    component_path = Path("templates/components/history_sidebar.html")
    return component_path.read_text()


@pytest.fixture
def soup(history_html):
    """Parse the component HTML."""
    return BeautifulSoup(history_html, "html.parser")


class TestHistorySidebarTemplate:
    """Tests for main template structure."""

    def test_sidebar_template_exists(self, soup):
        """Sidebar template should exist."""
        template = soup.find("template", id="history-sidebar-template")
        assert template is not None

    def test_has_sidebar_element(self, soup):
        """Template should have sidebar element."""
        template = soup.find("template", id="history-sidebar-template")
        sidebar = template.find(class_="history-sidebar")
        assert sidebar is not None

    def test_sidebar_has_role(self, soup):
        """Sidebar should have complementary role."""
        template = soup.find("template", id="history-sidebar-template")
        sidebar = template.find(class_="history-sidebar")
        assert sidebar.get("role") == "complementary"

    def test_has_header(self, soup):
        """Template should have header."""
        template = soup.find("template", id="history-sidebar-template")
        header = template.find(class_="history-sidebar-header")
        assert header is not None

    def test_has_title(self, history_html):
        """Template should have title."""
        assert 'class="history-sidebar-title"' in history_html
        assert ">History<" in history_html

    def test_has_close_button(self, soup):
        """Template should have close button."""
        template = soup.find("template", id="history-sidebar-template")
        close_btn = template.find(class_="history-sidebar-close")
        assert close_btn is not None

    def test_close_has_aria_label(self, soup):
        """Close button should have aria-label."""
        template = soup.find("template", id="history-sidebar-template")
        close_btn = template.find(class_="history-sidebar-close")
        assert close_btn.has_attr("aria-label")


class TestHistorySearch:
    """Tests for search functionality."""

    def test_has_search_container(self, soup):
        """Template should have search container."""
        template = soup.find("template", id="history-sidebar-template")
        search = template.find(class_="history-search")
        assert search is not None

    def test_has_search_input(self, soup):
        """Template should have search input."""
        template = soup.find("template", id="history-sidebar-template")
        input_el = template.find(class_="history-search-input")
        assert input_el is not None

    def test_search_input_type(self, soup):
        """Search input should have type search."""
        template = soup.find("template", id="history-sidebar-template")
        input_el = template.find(class_="history-search-input")
        assert input_el.get("type") == "search"

    def test_search_has_placeholder(self, soup):
        """Search input should have placeholder."""
        template = soup.find("template", id="history-sidebar-template")
        input_el = template.find(class_="history-search-input")
        assert input_el.has_attr("placeholder")
        assert "Search" in input_el.get("placeholder")

    def test_search_has_aria_label(self, soup):
        """Search input should have aria-label."""
        template = soup.find("template", id="history-sidebar-template")
        input_el = template.find(class_="history-search-input")
        assert input_el.has_attr("aria-label")


class TestHistoryContent:
    """Tests for content area."""

    def test_has_content_container(self, soup):
        """Template should have content container."""
        template = soup.find("template", id="history-sidebar-template")
        content = template.find(class_="history-content")
        assert content is not None

    def test_content_has_list_role(self, soup):
        """Content should have list role."""
        template = soup.find("template", id="history-sidebar-template")
        content = template.find(class_="history-content")
        assert content.get("role") == "list"


class TestHistoryItemTemplate:
    """Tests for conversation item template."""

    def test_item_template_exists(self, soup):
        """Item template should exist."""
        template = soup.find("template", id="history-item-template")
        assert template is not None

    def test_has_item_element(self, soup):
        """Item template should have article element."""
        template = soup.find("template", id="history-item-template")
        item = template.find(class_="history-item")
        assert item is not None
        assert item.name == "article"

    def test_item_has_listitem_role(self, soup):
        """Item should have listitem role."""
        template = soup.find("template", id="history-item-template")
        item = template.find(class_="history-item")
        assert item.get("role") == "listitem"

    def test_item_is_focusable(self, soup):
        """Item should be focusable for keyboard nav."""
        template = soup.find("template", id="history-item-template")
        item = template.find(class_="history-item")
        assert item.has_attr("tabindex")

    def test_has_topic_element(self, soup):
        """Item should have topic element."""
        template = soup.find("template", id="history-item-template")
        topic = template.find(class_="history-item-topic")
        assert topic is not None

    def test_has_summary_element(self, soup):
        """Item should have summary element."""
        template = soup.find("template", id="history-item-template")
        summary = template.find(class_="history-item-summary")
        assert summary is not None

    def test_has_meta_element(self, soup):
        """Item should have meta element."""
        template = soup.find("template", id="history-item-template")
        meta = template.find(class_="history-item-meta")
        assert meta is not None

    def test_has_time_element(self, soup):
        """Item should have time element."""
        template = soup.find("template", id="history-item-template")
        time = template.find(class_="history-item-time")
        assert time is not None

    def test_has_private_indicator(self, soup):
        """Item should have private indicator."""
        template = soup.find("template", id="history-item-template")
        private = template.find(class_="history-item-private")
        assert private is not None


class TestHistoryGroupTemplate:
    """Tests for date group template."""

    def test_group_template_exists(self, soup):
        """Group template should exist."""
        template = soup.find("template", id="history-group-template")
        assert template is not None

    def test_has_group_element(self, soup):
        """Group template should have section element."""
        template = soup.find("template", id="history-group-template")
        group = template.find(class_="history-group")
        assert group is not None
        assert group.name == "section"

    def test_group_has_role(self, soup):
        """Group should have group role."""
        template = soup.find("template", id="history-group-template")
        group = template.find(class_="history-group")
        assert group.get("role") == "group"

    def test_has_group_header(self, soup):
        """Group should have header."""
        template = soup.find("template", id="history-group-template")
        header = template.find(class_="history-group-header")
        assert header is not None

    def test_has_group_items_container(self, soup):
        """Group should have items container."""
        template = soup.find("template", id="history-group-template")
        items = template.find(class_="history-group-items")
        assert items is not None


class TestDateGroups:
    """Tests for month-based date grouping functions (#786)."""

    def test_group_by_month_defined(self, history_html):
        """groupByMonth function should be defined."""
        assert "groupByMonth" in history_html

    def test_get_month_key_defined(self, history_html):
        """getMonthKey function should be defined."""
        assert "getMonthKey" in history_html

    def test_format_month_label_defined(self, history_html):
        """formatMonthLabel function should be defined."""
        assert "formatMonthLabel" in history_html

    def test_group_by_date_alias_defined(self, history_html):
        """groupByDate alias should exist for compatibility."""
        assert "groupByDate" in history_html


class TestPagination:
    """Tests for pagination."""

    def test_has_load_more_container(self, soup):
        """Template should have load more container."""
        template = soup.find("template", id="history-sidebar-template")
        load_more = template.find(class_="history-load-more")
        assert load_more is not None

    def test_has_load_more_button(self, history_html):
        """Template should have load more button."""
        assert 'class="history-load-more-btn"' in history_html
        assert ">Load more<" in history_html


class TestPrivacyControls:
    """Tests for privacy mode controls."""

    def test_has_privacy_footer(self, soup):
        """Template should have privacy footer."""
        template = soup.find("template", id="history-sidebar-template")
        footer = template.find(class_="history-privacy-footer")
        assert footer is not None

    def test_has_privacy_toggle(self, soup):
        """Template should have privacy toggle button."""
        template = soup.find("template", id="history-sidebar-template")
        toggle = template.find(class_="history-privacy-toggle")
        assert toggle is not None

    def test_privacy_toggle_has_aria_pressed(self, soup):
        """Privacy toggle should have aria-pressed."""
        template = soup.find("template", id="history-sidebar-template")
        toggle = template.find(class_="history-privacy-toggle")
        assert toggle.has_attr("aria-pressed")

    def test_privacy_has_icon(self, soup):
        """Privacy toggle should have icon."""
        template = soup.find("template", id="history-sidebar-template")
        icon = template.find(class_="history-privacy-icon")
        assert icon is not None

    def test_privacy_has_label(self, soup):
        """Privacy toggle should have label."""
        template = soup.find("template", id="history-sidebar-template")
        label = template.find(class_="history-privacy-label")
        assert label is not None

    def test_privacy_footer_hidden_for_beta_1164(self, soup):
        """#1164: the 'Start private session' backend is not wired yet (gated on #1089),
        so the no-op footer is HIDDEN for beta. Shipping a clickable-but-dead privacy
        control would mislead beta users into believing a session is private when it is
        not — a trust risk. The markup is retained (the sidebar JS still queries
        `.history-privacy-toggle`), so re-enabling when the privacy feature lands
        (postponed to the dot-releases milestone) is just removing `hidden`."""
        template = soup.find("template", id="history-sidebar-template")
        footer = template.find(class_="history-privacy-footer")
        assert (
            footer is not None
        ), "markup must be retained (the sidebar JS still queries the toggle)"
        assert footer.has_attr("hidden"), (
            "the no-op privacy footer must carry `hidden` until the privacy backend "
            "(#1164 / #1089) lands — a visible no-op privacy control misleads beta users"
        )


class TestOverlay:
    """Tests for modal overlay."""

    def test_has_overlay(self, soup):
        """Template should have overlay."""
        template = soup.find("template", id="history-sidebar-template")
        overlay = template.find(class_="history-overlay")
        assert overlay is not None

    def test_overlay_has_presentation_role(self, soup):
        """Overlay should have presentation role."""
        template = soup.find("template", id="history-sidebar-template")
        overlay = template.find(class_="history-overlay")
        assert overlay.get("role") == "presentation"


class TestJavaScriptAPI:
    """Tests for JavaScript API."""

    def test_history_sidebar_namespace(self, history_html):
        """Should create HistorySidebar namespace."""
        assert "window.HistorySidebar" in history_html

    def test_mount_function_exposed(self, history_html):
        """Should expose mount function."""
        assert "mount: mount" in history_html

    def test_open_function_exposed(self, history_html):
        """Should expose open function."""
        assert "open: open" in history_html

    def test_close_function_exposed(self, history_html):
        """Should expose close function."""
        assert "close: close" in history_html

    def test_toggle_function_exposed(self, history_html):
        """Should expose toggle function."""
        assert "toggle: toggle" in history_html

    def test_update_function_exposed(self, history_html):
        """Should expose update function."""
        assert "update: update" in history_html

    def test_set_privacy_state_exposed(self, history_html):
        """Should expose setPrivacyState function."""
        assert "setPrivacyState: setPrivacyState" in history_html

    def test_group_by_date_exposed(self, history_html):
        """Should expose groupByDate function."""
        assert "groupByDate: groupByDate" in history_html

    def test_format_time_exposed(self, history_html):
        """Should expose formatTime function."""
        assert "formatTime: formatTime" in history_html

    def test_loaded_flag(self, history_html):
        """Should set loaded flag."""
        assert "historySidebarLoaded = true" in history_html


class TestEscapeKeyClosing:
    """Tests for Escape key closing."""

    def test_escape_key_handler(self, history_html):
        """Should close on Escape key."""
        assert "Escape" in history_html


class TestStyling:
    """Tests for CSS styling."""

    def test_open_class(self, history_html):
        """Should have open class for showing sidebar."""
        assert ".history-sidebar.open" in history_html

    def test_slide_transition(self, history_html):
        """Should have slide transition."""
        assert "translateX" in history_html

    def test_search_highlight_class(self, history_html):
        """Should have search highlight class."""
        assert ".history-search-highlight" in history_html

    def test_active_privacy_styling(self, history_html):
        """Should have active privacy toggle styling."""
        assert ".history-privacy-toggle.active" in history_html


class TestRadarSurface:
    """#1236 — Layer-2 Radar entities surface rendered in the sidebar slot.

    The sidebar is a template-clone render component; the Radar surface reuses
    it to render whatever RadarView /api/v1/radar returns. These guard the
    render functions, the API export, the honest-provenance markers, the
    XSS-safe construction, and the self-contained CSS.
    """

    def test_render_radar_card_defined(self, history_html):
        """renderRadarCard builds one entity card."""
        assert "function renderRadarCard(entity)" in history_html

    def test_render_radar_defined(self, history_html):
        """renderRadar renders a RadarView into the content area."""
        assert "function renderRadar(view)" in history_html

    def test_update_radar_exposed_on_namespace(self, history_html):
        """HistorySidebar.updateRadar is the entry point home.html calls."""
        assert "updateRadar: renderRadar" in history_html

    def test_radar_card_css_present(self, history_html):
        """Self-contained radar-card CSS (token-with-fallback)."""
        assert ".radar-card {" in history_html
        assert ".radar-card-title" in history_html
        assert ".radar-card-prov" in history_html

    def test_example_provenance_has_distinct_styling(self, history_html):
        """example-provenance cards render visually distinct (dashed)."""
        assert ".radar-card--example" in history_html
        assert "border-style: dashed" in history_html

    def test_empty_state_css_present(self, history_html):
        """Empty-state teaching surface has its own styling."""
        assert ".radar-empty" in history_html
        assert ".radar-empty-title" in history_html

    def test_honest_provenance_markers(self, history_html):
        """#1214/#1216: observed (real) vs example must read differently —
        a filled marker for observed, a hollow one for example."""
        assert "entity.provenance === 'observed' ? '● '" in history_html  # ●
        assert "radar-card--example" in history_html

    def test_card_title_is_xss_safe(self, history_html):
        """User-controlled title rendered via textContent, never innerHTML."""
        assert "title.textContent = entity.title" in history_html

    def test_card_meta_and_type_are_xss_safe(self, history_html):
        """Meta + entity_type also rendered via textContent."""
        assert "meta.textContent = entity.meta" in history_html
        assert "etype.textContent = entity.entity_type" in history_html

    def test_empty_state_renders_teaching_explainer(self, history_html):
        """Empty Radar teaches what will populate it (CXO empty-state spec)."""
        assert "Your Radar fills as Piper notices what you're working on." in history_html

    def test_renders_into_history_content_slot(self, history_html):
        """Radar reuses the existing content slot (frame-agnostic for #1171)."""
        assert ".history-content" in history_html

    def test_radar_title_branding(self, history_html):
        """Surface relabels to Radar (mockup fidelity) when in radar mode."""
        assert "\U0001f4e1 Radar" in history_html  # 📡 Radar

    # --- #1090 swap: Radar cards must be navigable (the History list was
    # click-to-resume; the Radar feed replaces it as the default panel) ---

    def test_radar_card_is_navigable(self, history_html):
        """A card with a ref carries the routing attributes + a focusable, clickable
        affordance (else graduating Radar-as-default would lose conversation-resume)."""
        assert "card.setAttribute('data-entity-type'" in history_html
        assert "card.setAttribute('data-ref', entity.ref)" in history_html
        assert "card.setAttribute('tabindex', '0')" in history_html
        assert "card.classList.add('radar-card--clickable')" in history_html

    def test_radar_card_only_clickable_when_ref_present(self, history_html):
        """Refless cards (e.g. the empty-state example) are not made clickable."""
        assert "if (entity.ref) {" in history_html

    def test_radar_card_click_routes_by_entity_type(self, history_html):
        """Delegated click opens the referent: Conversation resumes the chat,
        Work item opens the issue, Document goes to the Documents page."""
        assert "e.target.closest('.radar-card[data-ref]')" in history_html
        assert "if (type === 'Conversation') {" in history_html
        assert "options.onSelect({ id: ref })" in history_html  # resume the chat
        assert "window.open(ref, '_blank', 'noopener')" in history_html  # work item
        assert "window.location.href = '/documents'" in history_html  # document

    def test_radar_card_keyboard_navigable(self, history_html):
        """Enter/Space activates a radar card (a11y parity with conversation items)."""
        assert ".history-item, .radar-card[data-ref]" in history_html

    def test_radar_card_clickable_css_present(self, history_html):
        """Clickable cards show a pointer cursor + a focus ring."""
        assert ".radar-card--clickable" in history_html

    # --- #1236: entity-search that subsumes chat-search (the last unmet AC) ---

    def test_radar_search_placeholder_spans_all_types(self, history_html):
        """The Radar search 're-earns everything' — placeholder names all entity types,
        not just conversations (the old conversation-only placeholder is gone)."""
        assert "Search everything — issues, docs, people, chats" in history_html

    def test_radar_entity_search_filter_defined(self, history_html):
        """The client-side entity-filter + its render pass are wired."""
        assert "function renderRadarEntities()" in history_html
        assert "function radarEntityMatches(entity, q)" in history_html

    def test_radar_search_filters_in_radar_mode(self, history_html):
        """In Radar mode the search input re-renders the filtered entities (it no longer
        falls through to the conversation-only onSearch path)."""
        assert "if (radarMode) {" in history_html
        assert "renderRadarEntities();" in history_html

    def test_radar_entity_match_spans_searchable_facets(self, history_html):
        """A match spans every type's searchable facets: title + meta + type + lifecycle."""
        for facet in (
            "entity.title",
            "entity.meta",
            "entity.entity_type",
            "entity.lifecycle_state",
        ):
            assert facet in history_html

    def test_radar_search_empty_result_message(self, history_html):
        """A search with no matches reads honestly (not the new-user empty-state)."""
        assert "Nothing on your Radar matches your search." in history_html


class TestRadarPinnedReminders1625:
    """#1625 — due reminders render in a pinned section locked at the top of Radar
    (PM ruling: the persistent surface owns persistence; conversation mentions once)."""

    def test_pinned_section_rendered_before_unpinned_cards(self, history_html):
        assert "const pinned = matches.filter(e => e.pinned);" in history_html
        assert "const unpinned = matches.filter(e => !e.pinned);" in history_html
        # The pinned section is appended before the unpinned card loop.
        assert history_html.index("section.className = 'radar-pinned'") < history_html.index(
            "unpinned.forEach(e => content.appendChild(renderRadarCard(e)));"
        )

    def test_pinned_section_is_labeled(self, history_html):
        assert "Due reminders" in history_html
        assert "aria-label', 'Due reminders — pinned'" in history_html

    def test_pinned_card_class_and_styles_defined(self, history_html):
        assert "radar-card--pinned" in history_html
        assert ".radar-pinned {" in history_html
        assert ".radar-pinned-title {" in history_html
