"""#313 CONV-UX-DOCS slice 1: file browser search + type filter.

Template-content assertions (same pattern as test_empty_states.py) verifying the
/files browser renders the search input + type filter and wires the client-side
applyFileFilter() over the loaded list. The filter *behavior* (JS) is verified by
live UAT via #1165; these guard that the UI + wiring are present in the template.
"""

from pathlib import Path

import pytest


@pytest.fixture
def files_html() -> str:
    p = Path(__file__).parent.parent.parent.parent / "templates" / "files.html"
    return p.read_text()


class TestFileBrowserSearchFilter313:
    def test_search_input_present(self, files_html):
        assert 'id="file-search"' in files_html
        assert 'type="search"' in files_html
        assert (
            "Search documents by name" in files_html
        )  # #1270: page self-titles "Documents" (files→documents copy)
        # Wired to the filter on every keystroke.
        assert 'oninput="applyFileFilter()"' in files_html

    def test_type_filter_present_with_kinds(self, files_html):
        assert 'id="file-type-filter"' in files_html
        assert 'onchange="applyFileFilter()"' in files_html
        # Filters by the #355 `kind` discriminator (file vs artifact) + all.
        assert 'value="all"' in files_html
        assert 'value="file"' in files_html
        assert 'value="artifact"' in files_html

    def test_filter_function_defined_and_kind_aware(self, files_html):
        assert "function applyFileFilter()" in files_html
        # Filters on filename + kind, and re-renders via renderFiles.
        assert "f.filename" in files_html
        assert "f.kind" in files_html
        assert "renderFiles(filtered)" in files_html

    def test_loadFiles_stores_full_list_for_filtering(self, files_html):
        # The full list is retained so filtering doesn't require a refetch.
        assert "window._allFiles" in files_html

    def test_no_match_state_distinct_from_empty_state(self, files_html):
        # "No match" must be honest — distinct from the genuine "no files yet".
        assert (
            "No documents match your search." in files_html
        )  # #1270: page self-titles "Documents"
        assert "No documents in your knowledge base yet." in files_html
