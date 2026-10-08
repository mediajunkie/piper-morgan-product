"""Smithery server card (R7 demand probe): public, derived from the live
registrations, and free of user data."""

from __future__ import annotations

import json
import re

from fastapi.testclient import TestClient

from services.mcp.server.app import SERVER_CARD_PATH, build_asgi_app


def _card() -> tuple[int, dict]:
    with TestClient(build_asgi_app(), base_url="http://localhost:8080") as client:
        resp = client.get(SERVER_CARD_PATH)
    return resp.status_code, resp.json()


def test_card_is_public_and_requires_oauth_to_use_the_server() -> None:
    status, card = _card()

    assert status == 200
    assert card["serverInfo"]["name"] == "piper-morgan-mcp"
    assert card["authentication"] == {"required": True, "schemes": ["oauth2"]}


def test_card_lists_exactly_what_the_server_registers() -> None:
    _, card = _card()

    assert [t["name"] for t in card["tools"]] == ["what_piper_knows_about_me"]
    assert card["tools"][0]["annotations"]["readOnlyHint"] is True
    assert sorted(r["uri"] for r in card["resources"]) == [
        "piper://me/colleague-model",
        "piper://me/github/issues",
        "piper://me/profile",
    ]
    assert card["prompts"] == []


def test_card_carries_no_user_data_or_credentials() -> None:
    _, card = _card()
    text = json.dumps(card).lower()

    for marker in ("token", "secret", "password", "user_id", "owner_id"):
        assert marker not in text, marker
    # An email address, not a bare "@": the GitHub resource's description
    # legitimately quotes the search qualifier "assignee:@me".
    assert not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
