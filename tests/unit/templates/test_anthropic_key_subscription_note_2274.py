"""#2274 (CXO 11-04): the Anthropic key step says a subscription is not API access.

Beta session 11-04: a person with a Claude Pro subscription did not know the API is
funded separately. CXO's sentence sits before the key field wherever the key is asked
for (the setup wizard's key step and Settings, LLM API Keys), links to the Anthropic
Console, and shows only while Anthropic is the chosen provider.

Layers: source pins on the two templates and the wizard's script. This is not a
browser render; the served quote of each page is Web's.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SETUP = ROOT / "templates/setup.html"
SETTINGS = ROOT / "templates/settings_llm_keys.html"
SETUP_JS = ROOT / "web/static/js/setup.js"

SENTENCE = (
    "A Claude subscription (Pro or Max) doesn't include API access. Piper needs an API key "
    "from the Anthropic Console, which is billed separately from your subscription."
)
LINK = '<a href="https://console.anthropic.com/" target="_blank" rel="noopener noreferrer">'


def _note(path: Path) -> str:
    match = re.search(
        r'<p [^>]*id="llm-key-subscription-note"[^>]*>.*?</p>', path.read_text(), re.S
    )
    assert match, f"{path.name}: the subscription note is missing"
    return match.group(0)


@pytest.mark.parametrize("path", [SETUP, SETTINGS], ids=["wizard", "settings"])
def test_the_note_says_cxos_sentence_and_links_to_the_console(path):
    note = _note(path)
    text = re.sub(r"<[^>]+>", "", note)
    assert " ".join(text.split()) == SENTENCE
    assert note.count(LINK + "Anthropic Console</a>") == 1
    assert path.read_text().count('id="llm-key-subscription-note"') == 1


def test_the_note_comes_before_the_key_field_on_both_pages():
    wizard = SETUP.read_text()
    assert wizard.index('id="llm-key-subscription-note"') < wizard.index('id="llm-key"')
    settings = SETTINGS.read_text()
    assert settings.index('id="llm-key-subscription-note"') < settings.index('id="llm-key-input"')


def test_the_wizard_note_starts_hidden_and_shows_for_anthropic_only():
    tag = re.search(r'<p [^>]*id="llm-key-subscription-note"[^>]*>', SETUP.read_text()).group(0)
    assert " hidden" in tag  # no provider is chosen when the step opens
    assert "subscriptionNote.hidden = provider !== 'anthropic'" in SETUP_JS.read_text()


def test_settings_shows_it_for_the_default_provider_and_follows_the_select():
    src = SETTINGS.read_text()
    select = re.search(r'<select id="llm-provider".*?</select>', src, re.S).group(0)
    # Anthropic is the first option, so the note is visible when the page opens.
    assert re.findall(r'<option value="([^"]+)"', select)[0] == "anthropic"
    assert " hidden" not in re.search(r'<p [^>]*id="llm-key-subscription-note"[^>]*>', src).group(0)
    assert 'subscriptionNote.hidden = providerSel.value !== "anthropic";' in src
    assert 'providerSel.addEventListener("change", syncSubscriptionNote);' in src


def test_copy_rules_hold():
    """No "alpha", no issue number, no internals in what a person reads."""
    assert "alpha" not in SENTENCE.lower()
    assert not re.search(r"#\d{3,}", SENTENCE)
