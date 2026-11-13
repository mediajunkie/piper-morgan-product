"""#2351, CXO's words of 2026-11-12 for the setup page.

1. A saved key is called a saved key, never by where it is kept ("Keychain"): the label
   was wrong on an install that uses the database store.
2. The local-install invite field says the person makes their own code; a code can't
   come from us, because a local database starts empty. The hosted form is unchanged.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

from web.api.routes import setup as setup_routes

REPO_ROOT = Path(__file__).resolve().parents[3]
LOCAL_HELP = (
    "Piper is invite-only while it's in private beta. On your own copy, you make your own "
    "code. Step 8 of the self-host guide (docs/installation/self-host-guide.md in the "
    "Piper Morgan repository) shows the one command."
)


def _render(hosted: bool) -> str:
    env = Environment(loader=FileSystemLoader(str(REPO_ROOT / "templates")))
    return env.get_template("setup.html").render(asset_v="t", hosted=hosted)


@pytest.mark.parametrize("hosted", [True, False])
def test_the_button_says_use_saved_key_and_never_keychain(hosted):
    html = _render(hosted)
    assert "Use Keychain" not in html
    if not hosted:
        assert html.count("Use saved key") >= 1


def test_local_invite_field_says_you_make_your_own_code():
    html = _render(False)
    assert LOCAL_HELP in html
    assert 'placeholder="Your invite code"' in html
    assert "From your invitation" not in html
    assert "paste the code you received" not in html


def test_hosted_invite_words_are_unchanged():
    html = _render(True)
    assert "Alpha access is invite-only. Paste the code you received." in html
    assert LOCAL_HELP not in html


def test_the_guide_step_the_line_names_is_the_mint_step():
    guide = (REPO_ROOT / "docs/installation/self-host-guide.md").read_text()
    step8 = guide[guide.index("\n8. ") : guide.index("\n9. ")]
    assert "mint_invite_tokens.py" in step8


def test_page_script_has_no_keychain_words_a_person_reads():
    js = (REPO_ROOT / "web/static/js/setup.js").read_text()
    for old in (
        "Retrieving from keychain",
        "Keychain retrieval failed",
        "Keychain access failed",
        "Unable to access system keychain",
        "'Keychain Error'",
    ):
        assert old not in js
    assert "On your own copy you make it yourself; the setup guide shows how." in js


@pytest.mark.asyncio
async def test_route_messages_say_saved_not_keychain(monkeypatch):
    class Kc:
        def __init__(self, value):
            self.value = value

        def get_api_key(self, provider):
            return self.value

    monkeypatch.setattr("services.infrastructure.deployment.is_hosted_deployment", lambda: False)
    for value, expect in (
        ("fake-value", "Using the Anthropic key you already saved."),
        (None, "I couldn't find a saved Anthropic key. Paste it above to save one."),
    ):
        monkeypatch.setattr(
            "services.infrastructure.keychain_service.KeychainService", lambda v=value: Kc(v)
        )
        used = await setup_routes.use_keychain(
            setup_routes.KeychainUseRequest(provider="anthropic")
        )
        assert used.message == expect and "keychain" not in used.message.lower()
        checked = await setup_routes.check_keychain("anthropic")
        assert "keychain" not in checked.message.lower()
        assert checked.exists is (value is not None)
