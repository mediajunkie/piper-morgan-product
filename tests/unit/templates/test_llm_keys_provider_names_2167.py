"""CXO's #2167 nit, served on 45d6642da7 (Web 10-25): the keys page names each provider
(table row, Remove dialog, status line) instead of showing its id. Web found the GitHub
row still lower-case ("github"). Since Arch's 10-25 allowlist ruling the routes no longer
list it at all (tests/unit/web/api/routes/test_keys_routes_llm_allowlist.py), so the map
names only the LLM providers."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_every_listed_provider_has_a_display_name():
    src = (ROOT / "templates/settings_llm_keys.html").read_text()
    line = next(ln for ln in src.splitlines() if "const PROVIDER_NAMES" in ln)
    for provider, name in [
        ("anthropic", "Anthropic"),
        ("openai", "OpenAI"),
        ("gemini", "Google Gemini"),
    ]:
        assert f'{provider}: "{name}"' in line
    assert "PROVIDER_NAMES[k.provider] || k.provider" in src
    assert "github" not in line
