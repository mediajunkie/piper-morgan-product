"""#1380 — the Settings LLM-key page: the /api/v1/keys backend gets a UI.

House discipline (feedback_ui_fix_requires_template_render_test): a UI change is
verified by a REAL template.render(), not file-content greps and not a bare
route 200 — greps rot when templates migrate shells (#1350's failure mode), and
a 200 can serve an empty shell.
"""

from jinja2 import Environment, FileSystemLoader


def _render(template_name: str) -> str:
    env = Environment(loader=FileSystemLoader("templates"))
    return env.get_template(template_name).render(request=None, user={"username": "t"})


class TestLLMKeysPageRenders:
    def test_page_renders_through_the_real_shell(self):
        html = _render("settings_llm_keys.html")
        # the three interactive surfaces the page exists to provide:
        assert 'id="llm-provider"' in html  # provider select
        assert 'id="llm-key-input"' in html  # key entry
        assert 'id="llm-keys-tbody"' in html  # stored-keys table

    def test_page_wires_the_orphaned_keys_api(self):
        """The whole point of #1380: /api/v1/keys/* finally has a consumer."""
        html = _render("settings_llm_keys.html")
        assert "/api/v1/keys/list" in html
        assert "/api/v1/keys/store" in html
        assert '"/api/v1/keys/"' in html  # the DELETE base

    def test_write_only_disclosure_present(self):
        html = _render("settings_llm_keys.html")
        assert "never be viewed again" in html

    def test_settings_index_links_the_page(self):
        html = _render("settings-index.html")
        assert "/settings/llm-keys" in html
        assert "LLM API Keys" in html

    def test_route_registered_in_ui_module(self):
        """The page is reachable: ui.py declares GET /settings/llm-keys."""
        import web.api.routes.ui as ui

        paths = [r.path for r in ui.router.routes]
        assert "/settings/llm-keys" in paths
