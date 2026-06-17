"""
Unit tests for Documents Page (#422 MUX-IMPLEMENT-DOCS-ACCESS)

Tests the documents.html page with trust-gating and search functionality.
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def documents_html():
    """Load the documents page HTML."""
    page_path = Path("templates/documents.html")
    return page_path.read_text()


@pytest.fixture
def soup(documents_html):
    """Parse the page HTML."""
    return BeautifulSoup(documents_html, "html.parser")


class TestDocumentsPageStructure:
    """Tests for page structure."""

    def test_page_has_title(self, documents_html):
        """Page declares its title via the shell's page_title block (F2 #1171 migration)."""
        assert "{% block page_title %}" in documents_html
        assert "Documents" in documents_html

    def test_includes_navigation(self, documents_html):
        """Nav chrome is shell-owned now — the page extends app_shell, which provides it (F2 #1171)."""
        assert '{% extends "layouts/app_shell.html" %}' in documents_html

    def test_includes_document_window_component(self, documents_html):
        """Page should include document window component."""
        assert "components/document_window.html" in documents_html

    def test_has_documents_container(self, soup):
        """Page should have documents container."""
        container = soup.find("div", class_="documents-container")
        assert container is not None


class TestDocumentsTrustGating:
    """Tests for trust-gated visibility."""

    def test_container_has_trust_gating_attrs(self, soup):
        """Container should have trust-gating data attributes."""
        container = soup.find("div", class_="documents-container")
        assert container.get("data-trust-gated") == "true"
        assert container.get("data-min-stage") == "4"

    def test_has_trust_gate_message(self, soup):
        """Page should have trust gate message for low-trust users."""
        gate_message = soup.find("div", id="trust-gate-message")
        assert gate_message is not None

    def test_trust_gate_message_has_friendly_text(self, soup):
        """Trust gate message should be friendly, not technical."""
        gate_message = soup.find("div", id="trust-gate-message")
        text = gate_message.get_text()
        assert "getting to know" in text.lower() or "built up" in text.lower()
        # Should NOT contain technical terms
        assert "stage 4" not in text.lower()
        assert "trust level" not in text.lower()

    def test_trust_stage_javascript(self, documents_html):
        """Should set trustStage from user context."""
        assert "window.trustStage" in documents_html


class TestDocumentsSearch:
    """Tests for search functionality."""

    def test_has_search_input(self, soup):
        """Page should have search input."""
        search_input = soup.find("input", id="documents-search")
        assert search_input is not None

    def test_search_input_has_placeholder(self, soup):
        """Search input should have helpful placeholder."""
        search_input = soup.find("input", id="documents-search")
        placeholder = search_input.get("placeholder", "")
        assert "search" in placeholder.lower()

    def test_search_input_has_aria_label(self, soup):
        """Search input should have ARIA label for accessibility."""
        search_input = soup.find("input", id="documents-search")
        assert search_input.get("aria-label") is not None


class TestDocumentsGrid:
    """Tests for documents grid."""

    def test_has_documents_grid(self, soup):
        """Page should have documents grid container."""
        grid = soup.find("div", id="documents-grid")
        assert grid is not None

    def test_grid_has_role(self, soup):
        """Grid should have list role for accessibility."""
        grid = soup.find("div", id="documents-grid")
        assert grid.get("role") == "list"

    def test_grid_has_aria_label(self, soup):
        """Grid should have ARIA label."""
        grid = soup.find("div", id="documents-grid")
        assert grid.get("aria-label") is not None

    def test_has_loading_state(self, soup):
        """Grid should have initial loading state."""
        loading = soup.find("div", class_="documents-loading")
        assert loading is not None


class TestDocumentsModal:
    """Tests for document detail modal."""

    def test_has_modal_overlay(self, soup):
        """Page should have modal overlay."""
        modal = soup.find("div", id="document-modal")
        assert modal is not None

    def test_modal_has_dialog_role(self, soup):
        """Modal should have dialog role."""
        modal = soup.find("div", id="document-modal")
        assert modal.get("role") == "dialog"

    def test_modal_has_aria_modal(self, soup):
        """Modal should have aria-modal attribute."""
        modal = soup.find("div", id="document-modal")
        assert modal.get("aria-modal") == "true"

    def test_modal_has_close_button(self, soup):
        """Modal should have close button."""
        close_btn = soup.find("button", class_="document-modal-close")
        assert close_btn is not None
        assert close_btn.get("aria-label") is not None

    def test_modal_has_qa_section(self, soup):
        """Modal should have Q&A section."""
        qa_section = soup.find("div", class_="document-qa-section")
        assert qa_section is not None

        qa_input = soup.find("textarea", id="document-question")
        assert qa_input is not None

        qa_submit = soup.find("button", id="document-qa-submit")
        assert qa_submit is not None

    def test_modal_has_download_action(self, soup):
        """Modal should have download action."""
        download_link = soup.find("a", id="modal-download")
        assert download_link is not None
        assert download_link.has_attr("download")


class TestDocumentsJavaScript:
    """Tests for JavaScript functionality."""

    def test_loads_documents_on_dom_ready(self, documents_html):
        """Should load documents when DOM is ready."""
        assert "DOMContentLoaded" in documents_html
        assert "loadDocuments" in documents_html

    def test_has_search_debouncing(self, documents_html):
        """Search should be debounced."""
        assert "setTimeout" in documents_html
        # Check for debounce delay (300ms)
        assert "300" in documents_html

    def test_uses_document_window_render(self, documents_html):
        """Should use DocumentWindow.render for rendering."""
        assert "DocumentWindow.render" in documents_html

    def test_handles_document_expand_event(self, documents_html):
        """Should listen for documentExpand custom event."""
        assert "documentExpand" in documents_html

    def test_has_keyboard_navigation(self, documents_html):
        """Should support Escape key to close modal."""
        assert "Escape" in documents_html


class TestDocumentsEmptyState:
    """Tests for empty state."""

    def test_empty_state_class_exists(self, documents_html):
        """Should have empty state styling."""
        assert "documents-empty" in documents_html

    def test_empty_state_has_friendly_message(self, documents_html):
        """Empty state should have friendly message."""
        assert "No documents yet" in documents_html
        assert "Upload files" in documents_html or "connect Notion" in documents_html


class TestDocumentsAccessibility:
    """Tests for accessibility."""

    def test_page_has_lang_attribute(self, documents_html):
        """<html lang> is shell-owned now — the page extends app_shell, which sets it (F2 #1171)."""
        assert '{% extends "layouts/app_shell.html" %}' in documents_html

    def test_inputs_have_labels(self, soup):
        """Form inputs should have labels."""
        # Search input
        search_input = soup.find("input", id="documents-search")
        assert search_input.get("aria-label") is not None

        # Q&A textarea
        qa_label = soup.find("label", {"for": "document-question"})
        assert qa_label is not None

    def test_loading_state_has_role(self, soup):
        """Loading state should have status role."""
        loading = soup.find("div", class_="documents-loading")
        assert loading.get("role") == "status"
