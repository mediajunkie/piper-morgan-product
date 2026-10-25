"""CXO's #2167 nit, served on 45d6642da7 (Web 10-25): the keys page names each provider
(table row, Remove dialog, status line) instead of showing its id. Web found the GitHub
row still lower-case ("github"); it is the account's GitHub token at rest, listed here."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_every_listed_provider_has_a_display_name():
    src = (ROOT / "templates/settings_llm_keys.html").read_text()
    line = next(ln for ln in src.splitlines() if "const PROVIDER_NAMES" in ln)
    for provider, name in [
        ("anthropic", "Anthropic"),
        ("openai", "OpenAI"),
        ("gemini", "Google Gemini"),
        ("github", "GitHub"),
    ]:
        assert f'{provider}: "{name}"' in line
    assert "PROVIDER_NAMES[k.provider] || k.provider" in src
