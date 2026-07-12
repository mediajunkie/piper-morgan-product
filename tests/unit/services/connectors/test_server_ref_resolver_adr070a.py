"""ADR-070 Amendment A — resolve_server_ref() contract (A1–A4).

The one-resolver authority that replaces literal mcp_server_ref reads. The
2026-07-12 incident: a pg_dump/restore host move carried `http://github-mcp:
8082/mcp` (compose hostname) onto Fly, where PM's healthy-looking binding
degraded as a phantom server outage.
"""

import pytest

from services.connectors.server_ref_resolver import (
    ServerRefResolutionError,
    resolve_server_ref,
)


class TestLogicalKeys:
    def test_bare_key_resolves_from_deployment_config(self, monkeypatch):
        """A1: the key is topology-free; each deployment supplies its URL."""
        monkeypatch.setenv("GITHUB_MCP_SERVER_URL", "http://piper-morgan-gh-mcp.internal:8082/mcp")
        assert resolve_server_ref("github") == "http://piper-morgan-gh-mcp.internal:8082/mcp"

    def test_null_ref_falls_back_to_connector_key(self, monkeypatch):
        """Legacy NULL-ref rows resolve through the same authority."""
        monkeypatch.setenv("GITHUB_MCP_SERVER_URL", "http://github-mcp:8082/mcp")
        assert resolve_server_ref(None, connector="github") == "http://github-mcp:8082/mcp"

    def test_unset_env_names_the_config(self, monkeypatch):
        """A4: the error points at the MISSING CONFIG, not a server outage."""
        monkeypatch.delenv("CALENDAR_MCP_SERVER_URL", raising=False)
        with pytest.raises(ServerRefResolutionError, match="CALENDAR_MCP_SERVER_URL, which is unset"):
            resolve_server_ref("calendar")

    def test_unknown_key_lists_known_connectors(self):
        with pytest.raises(ServerRefResolutionError, match="not a known connector key"):
            resolve_server_ref("gitbook")


class TestByocLiterals:
    def test_scheme_prefixed_returns_verbatim(self):
        """A3: a literal URL is the user's OWN server — never remapped."""
        assert resolve_server_ref("https://mcp.example.com/gh") == "https://mcp.example.com/gh"

    def test_literal_wins_even_when_key_env_is_set(self, monkeypatch):
        monkeypatch.setenv("GITHUB_MCP_SERVER_URL", "http://managed.internal:8082/mcp")
        assert resolve_server_ref("http://byoc.local:9000/mcp") == "http://byoc.local:9000/mcp"


class TestEmpty:
    def test_empty_with_no_connector_raises(self):
        with pytest.raises(ServerRefResolutionError):
            resolve_server_ref("")
