#!/usr/bin/env python3
"""The card-state file: what each Integrations card says and offers, per state.

Arch asked for this on 2026-11-15 after beta served a GitHub card whose link had been put
in the wrong branch of the page's script: the tests had read source text and never drew
a card. CXO reads this file at each promotion, next to the screen atlas ("both, not
either"): this file is the words and the controls; the atlas is the layout.

How a row is made (the method of the #2031 test, with nothing typed by hand):
1. The app's own health route function (``get_integrations_health``, behind
   ``GET /api/v1/integrations/health``) is called with the inputs a state depends on
   stubbed underneath it: the GitHub credential resolver, the config-status lookup and
   the per-account Test result. The payload is the route's, words included. The call
   is direct, not over HTTP, so no sign-in, database or Redis is needed.
2. The Integrations page's own script, taken from ``templates/integrations.html``, is run
   under ``node`` with a small stand-in for the browser. Its ``loadIntegrationsHealth()``
   fetches that payload, draws the headline and the cards, and labels the GitHub
   repositories link from a stubbed install-state answer. The list of connectors this
   beta offers comes from the same function the page route calls.
3. Each card's drawn HTML is read: the text lines, and every button or link with its
   label, its style class and where it goes.

What it is not: a browser, or the served app. No CSS, no layout, no click, no real
account, no network, no middleware.
A control hidden by a style sheet would still be listed.

After a click (CXO and Arch, 2026-11-17: the last two served misses were there): the GitHub
card's Test, state by state. The app's own Test route is called with the same stubs, its
result goes into the same per-account store the health route reads, and the page's own
``testConnection()`` runs under node: the toast, the line the card shows at the click, any
fix line, and the card as the page redraws it from the health route. CXO's rule: the line at
the click and the line on the card are one sentence from one source; the file says whether
the click's line is on the redrawn card. The Notion, Slack and Calendar cards' Tests follow, and
Test All: those Tests run the app's own per-connector checks, with the credential read and the
connector's reply stubbed underneath them (a made-up key; Notion's, Slack's and Google's answers
stood in for, so the words come from the app's code, not this file). Then the confirm dialogs
before a disconnect: each card's Disconnect and Disconnect All are pressed on a drawn page, the
page's own call to ``Dialog.confirm`` is recorded, and the dialog is answered Cancel, so nothing
is disconnected. Not yet here: what happens after a confirmed disconnect.

Usage (from the repository root, with ``node`` on PATH):
    venv/bin/python scripts/card_state_file.py                # write the file
    venv/bin/python scripts/card_state_file.py --check        # exit 1 if the file is stale
    venv/bin/python scripts/card_state_file.py --out some.md

The file is ``docs/internal/operations/card-states.md``. It is the same for the same
code, so ``git diff`` on it between two promotions is the list of words and controls
that changed.

Concept: docs/internal/operations/card-states.md
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import uuid
from contextlib import ExitStack
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Tuple
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "docs" / "internal" / "operations" / "card-states.md"
TEMPLATE = ROOT / "templates" / "integrations.html"
HEALTH = "/api/v1/integrations/health"
INSTALL_STATE = "/api/v1/settings/integrations/github/install-state"
CARDS = ("github", "notion", "slack", "calendar")
SAMPLE_ERROR = "Sample error text from a failed Test"
# Issue 2402: an error that quotes markup must be drawn as text, never as an element.
MARKUP_ERROR = 'Sample error quoting <b>markup</b> & "quotes"'

_ROUTES = "web.api.routes.integrations"
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"


def node_missing_is_a_skip() -> bool:
    """May a test that needs ``node`` be skipped here? On a seat without node, yes. In CI,
    never (Arch 2026-11-17): a skipped pin would leave a stale file unnoticed at a
    promotion, so there the test runs and ``build`` stops it with a failure."""
    return shutil.which("node") is None and not os.environ.get("CI")


class Stopped(Exception):
    """A reason this script can't produce the file; printed as one line."""


# --- the states ---------------------------------------------------------------------


@dataclass(frozen=True)
class Scenario:
    """One payload: what every card's inputs are set to."""

    key: str
    title: str
    # card -> generic state: "not_configured", "check_failed", "connected", "healthy", "failed"
    generic: Dict[str, str] = field(default_factory=dict)
    # GitHub's resolver outcome; None lets ``generic["github"]`` govern (own token, nothing stale)
    github: Optional[str] = None
    install_state: Any = "unknown"  # the install-state route's answer, or "not_ok"
    login: Optional[str] = "octo-example"  # the GitHub login the card reads; None: unreadable
    error_text: str = SAMPLE_ERROR  # what a failed Test recorded
    offered: Tuple[str, ...] = CARDS  # the connectors this beta offers (host configuration)
    show: Tuple[str, ...] = CARDS  # which cards this scenario's rows are for
    # The GitHub read a Test makes: "ok", "not_installed" (the app is on no repository) or
    # "unreachable" (GitHub did not answer)
    repos: str = "ok"
    # Notion, Slack, Calendar: what their Test meets, per card (see _CONNECTOR_OUTCOMES); a
    # card not named meets no stored credential
    tests: Dict[str, str] = field(default_factory=dict)


def _all(state: str) -> Dict[str, str]:
    return {card: state for card in CARDS}


def scenarios() -> List[Scenario]:
    others_off = {c: "not_configured" for c in CARDS if c != "github"}
    gh = ("github",)
    return [
        Scenario(
            "not-connected", "Nothing connected", generic=_all("not_configured"), github="nothing"
        ),
        Scenario(
            "check-failed",
            "The credential lookup itself failed",
            generic=_all("check_failed"),
            github="unreachable",
        ),
        Scenario(
            "connected-untested",
            "Connected, never tested by this account",
            generic=_all("connected"),
            github="own_token",
        ),
        Scenario(
            "healthy",
            "Connected, Test passed just now",
            generic=_all("healthy"),
            github="own_token",
        ),
        Scenario(
            "failed",
            "Connected, Test failed just now (the error text is a sample)",
            generic=_all("failed"),
            github="own_token",
        ),
        Scenario(
            "failed-markup",
            "Connected, Test failed, and the error text holds markup characters (the text is a sample)",
            generic=_all("failed"),
            github="own_token",
            error_text=MARKUP_ERROR,
        ),
        Scenario(
            "github-app-failed-markup",
            "GitHub: connected through the GitHub app, Test failed, the error text holds markup characters",
            generic={**others_off, "github": "failed"},
            github="app",
            install_state={"state": "some"},
            error_text=MARKUP_ERROR,
            show=gh,
        ),
        Scenario(
            "github-app-none",
            "GitHub: connected through the GitHub app, installed on no repository",
            generic=others_off,
            github="app",
            install_state={"state": "none"},
            show=gh,
        ),
        Scenario(
            "github-app-some",
            "GitHub: connected through the GitHub app, installed on a repository",
            generic=others_off,
            github="app",
            install_state={"state": "some"},
            show=gh,
        ),
        Scenario(
            "github-app-unknown",
            "GitHub: connected through the GitHub app, install check did not answer",
            generic=others_off,
            github="app",
            install_state="not_ok",
            show=gh,
        ),
        Scenario(
            "github-app-login-unreadable",
            "GitHub: connected through the GitHub app, the account's login could not be read",
            generic=others_off,
            github="app",
            install_state={"state": "some"},
            login=None,
            show=gh,
        ),
        Scenario(
            "github-app-healthy",
            "GitHub: connected through the GitHub app, Test passed just now",
            generic={**others_off, "github": "healthy"},
            github="app",
            install_state={"state": "some"},
            show=gh,
        ),
        Scenario(
            "github-app-failed",
            "GitHub: connected through the GitHub app, Test failed just now (the error text is a sample)",
            generic={**others_off, "github": "failed"},
            github="app",
            install_state={"state": "some"},
            show=gh,
        ),
        Scenario(
            "github-oauth-classic",
            "GitHub: connected by sign-in without the app (an older connection)",
            generic=others_off,
            github="oauth_classic",
            install_state={"state": "not_app"},
            show=gh,
        ),
        Scenario(
            "github-token-serving-stale",
            "GitHub: a saved token is serving; the sign-in needs re-authorizing",
            generic=others_off,
            github="pat_stale",
            show=gh,
        ),
        Scenario(
            "github-needs-reconnecting",
            "GitHub: the sign-in needs re-authorizing and nothing is serving",
            generic=others_off,
            github="stale_nothing",
            show=gh,
        ),
        Scenario(
            "not-offered",
            "Not offered in this beta, and not connected",
            generic=_all("not_configured"),
            github="nothing",
            offered=(),
        ),
        Scenario(
            "not-offered-connected",
            "Not offered in this beta, but a connection is stored",
            generic=_all("connected"),
            github="own_token",
            offered=(),
        ),
    ]


def clicks() -> List[Scenario]:
    """The GitHub card's Test, state by state: what the card was, and what the Test meets.
    The card starts connected and untested; the other cards are off."""
    off = {c: "not_configured" for c in CARDS if c != "github"}
    start = {**off, "github": "connected"}
    gh = ("github",)
    return [
        Scenario(
            "test-app-installed",
            "Through the GitHub app, installed on a repository",
            generic=start,
            github="app",
            install_state={"state": "some"},
            show=gh,
        ),
        Scenario(
            "test-app-not-installed",
            "Through the GitHub app, installed on no repository",
            generic=start,
            github="app",
            install_state={"state": "none"},
            repos="not_installed",
            show=gh,
        ),
        Scenario(
            "test-own-token", "With a saved token", generic=start, github="own_token", show=gh
        ),
        Scenario(
            "test-token-serving-stale",
            "A saved token is serving; the sign-in needs re-authorizing",
            generic=start,
            github="pat_stale",
            show=gh,
        ),
        Scenario(
            "test-needs-reconnecting",
            "The sign-in needs re-authorizing and nothing is serving",
            generic=start,
            github="stale_nothing",
            show=gh,
        ),
        Scenario("test-not-connected", "Nothing connected", generic=off, github="nothing", show=gh),
        Scenario(
            "test-lookup-failed",
            "The credential lookup itself failed",
            generic=start,
            github="unreachable",
            show=gh,
        ),
        Scenario(
            "test-github-did-not-answer",
            "Connected, and GitHub did not answer the read",
            generic=start,
            github="own_token",
            repos="unreachable",
            show=gh,
        ),
    ]


#: What a Notion, Slack or Calendar Test can meet, per card, in the order the file shows them.
_CONNECTOR_OUTCOMES = {
    "notion": (
        ("ok", "Notion answers"),
        ("refused", "Notion refuses the key"),
        ("no_answer", "Notion answers with a server error"),
        ("raised", "The call to Notion fails on our side"),
        ("not_connected", "No key is stored"),
    ),
    "slack": (
        ("ok", "Slack answers"),
        ("refused", "Slack refuses the token"),
        ("raised", "The call to Slack fails on our side"),
        ("not_connected", "No token is stored"),
    ),
    "calendar": (
        ("ok", "Google refreshes the grant and the calendar read works"),
        ("revoked", "Google says the grant was revoked"),
        ("no_answer", "Google answers the refresh with a server error"),
        ("insufficient_scope", "The grant has no calendar access"),
        ("api_not_enabled", "The Calendar service is not switched on for the app"),
        ("error", "Google refuses the read for a reason it doesn't classify"),
        ("not_found", "Google refuses the read: the calendar was not found"),
        ("raised", "The call to Google fails on our side"),
        ("store_failed", "The credential store did not answer"),
        ("not_connected", "No grant is stored"),
    ),
}


def connector_clicks() -> List[Scenario]:
    """The Notion, Slack and Calendar cards' Test, outcome by outcome. The pressed card
    starts connected and untested (not connected when nothing is stored); the others are off."""
    out = []
    for card, outcomes in _CONNECTOR_OUTCOMES.items():
        for outcome, title in outcomes:
            stored = outcome != "not_connected"
            generic = {c: "not_configured" for c in CARDS}
            generic[card] = "connected" if stored else "not_configured"
            out.append(
                Scenario(
                    f"test-{card}-{outcome.replace('_', '-')}",
                    title,
                    generic=generic,
                    github="nothing",
                    show=(card,),
                    tests={card: outcome},
                )
            )
    return out


def test_all_clicks() -> List[Scenario]:
    """Test All, from three starting pages."""
    return [
        Scenario(
            "test-all-pass",
            "Every card connected, and every Test passes",
            generic=_all("connected"),
            github="own_token",
            tests={"notion": "ok", "slack": "ok", "calendar": "ok"},
        ),
        Scenario(
            "test-all-mixed",
            "One passes, one is refused, one couldn't be checked, one not connected",
            generic={**_all("connected"), "calendar": "not_configured"},
            github="own_token",
            tests={"notion": "refused", "slack": "raised", "calendar": "not_connected"},
        ),
        Scenario(
            "test-all-nothing",
            "Nothing connected",
            generic=_all("not_configured"),
            github="nothing",
        ),
    ]


# --- step 1: the route's payload ------------------------------------------------------


def _setup() -> str:
    """Make the app importable and return a made-up account id."""
    os.environ.setdefault("JWT_SECRET_KEY", secrets.token_urlsafe(32))
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    return str(uuid.uuid4())


def _github_outcome(name: str):
    from services.mcp.consumer.connector import DegradationReason, DegradationResponse
    from services.mcp.consumer.github_adapter import GitHubCredential

    def credential(**extra):
        return GitHubCredential(owner_id="u", mcp_server_ref="github", **extra)

    made_up = "not-a-token"
    return {
        "app": lambda: credential(token=made_up, leg="oauth", app_grant=True),
        "oauth_classic": lambda: credential(token=None, leg="oauth"),
        "own_token": lambda: credential(token=made_up, leg="pat"),
        "pat_stale": lambda: credential(
            token=made_up, leg="pat", stale_oauth_reason=DegradationReason.STALE_TOKEN
        ),
        "stale_nothing": lambda: DegradationResponse(
            reason=DegradationReason.STALE_TOKEN, user_message="needs re-authorizing"
        ),
        "nothing": lambda: DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED, user_message="Connect GitHub to continue."
        ),
        "unreachable": lambda: (_ for _ in ()).throw(RuntimeError("lookup failed")),
    }[name]


def _repos_result(kind: str):
    from services.mcp.consumer.connector import DegradationReason, DegradationResponse
    from services.mcp.consumer.github_adapter import GitHubReposResult
    from services.mcp.consumer.github_app_install import DETAIL_APP_NOT_INSTALLED

    if kind == "not_installed":
        return GitHubReposResult(
            degradation=DegradationResponse(
                reason=DegradationReason.CONNECT_REQUIRED,
                user_message="The GitHub app isn't installed on a repository.",
                detail=DETAIL_APP_NOT_INSTALLED,
            )
        )
    if kind == "unreachable":
        return GitHubReposResult(
            degradation=DegradationResponse(
                reason=DegradationReason.UNREACHABLE, user_message="GitHub didn't answer."
            )
        )
    return GitHubReposResult(repositories=[{"full_name": "o/r"}])


class _Reply:
    """One stood-in reply from Notion, Slack or Google, as ``aiohttp`` hands it over."""

    def __init__(self, status: int, body: Any = None, text: str = "") -> None:
        self.status, self._body, self._text = status, body, text

    async def json(self, *args, **kwargs):
        return self._body

    async def text(self, *args, **kwargs):
        return self._text

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


def _connector_session(tests: Dict[str, str]):
    """An ``aiohttp.ClientSession`` stand-in that answers Notion's, Slack's and Google's
    token addresses from ``tests`` and refuses any other address."""

    def answer(url: str) -> _Reply:
        card = next(
            (c for c, host in _HOSTS.items() if host in url),
            None,
        )
        outcome = tests.get(card or "", "")
        if card is None or outcome == "raised":
            raise OSError("card_state_file: no call leaves this process")
        if card == "notion":
            return _Reply({"ok": 200, "refused": 401, "no_answer": 503}[outcome])
        if card == "slack":
            return _Reply(200, {"ok": True} if outcome == "ok" else {"ok": False, "error": "x"})
        if outcome == "revoked":
            return _Reply(400, text='{"error": "invalid_grant"}')
        if outcome == "no_answer":
            return _Reply(503, text="")
        return _Reply(200, {"access_token": "not-a-token", "expires_in": 3600})

    class Session:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        def get(self, url, **kwargs):
            return answer(url)

        def post(self, url, **kwargs):
            return answer(url)

    return Session


_HOSTS = {"notion": "api.notion.com", "slack": "slack.com", "calendar": "oauth2.googleapis.com"}
_READ_REFUSED = ("insufficient_scope", "api_not_enabled", "error", "not_found")


def _stub_connectors(stack: ExitStack, tests: Dict[str, str]) -> None:
    """The credential each Test reads, and the connector's reply, for Notion, Slack and
    Calendar. Everything above these (the route, the ``_test_*`` checks, the handler's
    refresh, the page) is the app's own code."""
    from services.infrastructure.keychain_service import SecretProvenance, SecretRead

    made_up = "not-a-token"

    def stored(card: str) -> Optional[str]:
        return None if tests.get(card, "not_connected") == "not_connected" else made_up

    async def notion_config(self, user_id):
        return SimpleNamespace(api_key=stored("notion"))

    def slack_config(self, user_id=None):
        return SimpleNamespace(bot_token=stored("slack"))

    async def calendar_secret(self, provider, username=None):
        if tests.get("calendar") == "store_failed":
            return SecretRead(SecretProvenance.STORE_FAILED, error="stub")
        if stored("calendar") is None:
            return SecretRead(SecretProvenance.VERIFIED_ABSENT)
        return SecretRead(SecretProvenance.PRESENT, value=made_up)

    outcome = tests.get("calendar", "")
    read = AsyncMock(return_value=outcome if outcome in _READ_REFUSED else None)
    stack.enter_context(patch("aiohttp.ClientSession", new=_connector_session(tests)))
    stack.enter_context(
        patch(
            "services.integrations.notion.config_service.NotionConfigService.aget_config",
            new=notion_config,
        )
    )
    stack.enter_context(
        patch(
            "services.integrations.slack.config_service.SlackConfigService.get_config",
            new=slack_config,
        )
    )
    stack.enter_context(
        patch(
            "services.infrastructure.keychain_service.KeychainService.aread_secret",
            new=calendar_secret,
        )
    )
    stack.enter_context(
        patch("services.integrations.calendar.oauth_handler.probe_calendar_read", new=read)
    )
    # The handler reads the app's client id; a made-up one keeps it off the config store.
    stack.enter_context(
        patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "made-up", "GOOGLE_CLIENT_SECRET": "made-up"})
    )


def health_payload(user_id: str, scenario: Scenario) -> Dict[str, Any]:
    """The health route's own answer for this scenario."""
    return run_routes(user_id, scenario)[1]


#: ``run_routes``'s ``test`` value that presses Test All.
TEST_ALL = "*"
#: ``draw``'s ``test`` name that presses every Disconnect and answers Cancel.
DIALOGS = "dialogs"


def run_routes(user_id: str, scenario: Scenario, test: Optional[str] = None) -> Tuple[Any, Any]:
    """The Test route's answer for ``test`` (when given; ``TEST_ALL`` for Test All), then
    the health route's answer, both under one set of stubs and one per-account result
    store, as on the server: the health route reads what the Test recorded."""
    from services.integrations.principal_test_results import PrincipalTestResultStore
    from web.api.routes import integrations as routes

    config = {"not_configured": "not_configured", "check_failed": "unknown"}
    store = PrincipalTestResultStore()
    for card, state in scenario.generic.items():
        if state == "healthy":
            store.record_test_result(user_id, card, ok=True)
        elif state == "failed":
            store.record_test_result(user_id, card, ok=False, error=scenario.error_text)

    async def config_status(integration_id, user_id=None):
        return config.get(scenario.generic.get(integration_id, "not_configured"), "configured")

    outcome = _github_outcome(scenario.github or "own_token")

    async def resolve(*args, **kwargs):
        return outcome()

    async def account_login(self, account_id):
        if scenario.login is None:
            raise RuntimeError("the login could not be read")
        return scenario.login

    probe = _repos_result(scenario.repos)
    with ExitStack() as stack:
        stack.enter_context(patch(f"{_ROUTES}._get_integration_config_status", new=config_status))
        stack.enter_context(patch(f"{_ROUTES}._get_test_result_store", new=lambda: store))
        stack.enter_context(patch(f"{_ADAPTER}.resolve_credential", new=resolve))
        stack.enter_context(patch(f"{_ADAPTER}.account_login", new=account_login))
        # The route turns a failure into a "couldn't check" card, so a state that reached
        # for the network would draw the wrong words quietly. Refuse and stop instead.
        reached: List[str] = []

        def no_network(*args, **kwargs):
            reached.append("network")
            raise OSError("card_state_file makes no network call")

        stack.enter_context(patch("socket.socket.connect", new=no_network))
        stack.enter_context(patch("socket.getaddrinfo", new=no_network))
        stack.enter_context(
            patch(f"{_ADAPTER}.search_user_repositories", new=AsyncMock(return_value=probe))
        )
        if test is not None and test != "github":
            _stub_connectors(stack, scenario.tests)
        who = SimpleNamespace(sub=user_id)
        tested = None
        try:
            if test == TEST_ALL:
                tested = [
                    r.model_dump(mode="json")
                    for r in asyncio.run(routes.check_all_connections(current_user=who))
                ]
            elif test is not None:
                tested = asyncio.run(
                    routes.check_integration_connection(test, current_user=who)
                ).model_dump(mode="json")
            reply = asyncio.run(routes.get_integrations_health(current_user=who))
        except Exception as error:
            raise Stopped(f"a route raised {type(error).__name__} for '{scenario.key}'") from None
        if reached:
            raise Stopped(
                f"state '{scenario.key}' reached for the network or a database; an input "
                "it depends on is not stubbed"
            )
    return tested, reply.model_dump(mode="json")


# --- step 2: the page's own script, under node -----------------------------------------

_BROWSER = r"""
const elements = {};
const element = () => ({ innerHTML: '', textContent: '', className: '', style: {}, dataset: {},
  classList: { add() {}, remove() {}, toggle() {}, contains: () => false },
  addEventListener() {}, setAttribute() {}, querySelector: () => null, querySelectorAll: () => [] });
const LINK = 'github-repositories-link';
const document = {
  getElementById(id) {
    // The link exists only if the drawn list holds it, as in a browser.
    if (id === LINK && !(elements['integrations-list'] || {innerHTML: ''}).innerHTML.includes(`id="${LINK}"`)) return null;
    return (elements[id] = elements[id] || element());
  },
  addEventListener() {}, querySelector: () => null, querySelectorAll: () => [],
};
const window = { location: { search: '', pathname: '/settings/integrations' },
  history: { replaceState() {} }, addEventListener() {} };
const localStorage = { getItem: () => null, setItem() {}, removeItem() {} };
const fetched = [];
async function fetch(url) {
  fetched.push(url);
  if (url === INPUT.health_url) return { ok: true, status: 200, json: async () => INPUT.health };
  if (url === INPUT.install_url) {
    if (INPUT.install === 'not_ok') return { ok: false, status: 503, json: async () => ({}) };
    return { ok: true, status: 200, json: async () => INPUT.install };
  }
  return { ok: false, status: 404, json: async () => ({}) };
}
"""

_RUN = r"""
(async () => {
  await loadIntegrationsHealth();
  await new Promise((resolve) => setTimeout(resolve, 0));  // the link label is not awaited
  const text = (id) => (elements[id] ? elements[id].textContent : null);
  process.stdout.write(JSON.stringify({
    list: (elements['integrations-list'] || {}).innerHTML || '',
    title: text('overall-title'), subtitle: text('overall-subtitle'),
    link: elements[LINK] ? { text: elements[LINK].textContent, cls: elements[LINK].className } : null,
    fetched,
  }));
})();
"""


_CLICK = r"""
const toasts = [];
const Toast = { show(kind, title, message) { toasts.push({ kind, title, message }); } };
const appended = [];
// As in a browser: an element nobody has created is not there (the fix line is created
// on the first failed Test, and a passing Test removes it if it is).
document.createElement = () => Object.assign(element(), { remove() {} });
const pageGet = document.getElementById;
document.getElementById = (id) => (id.startsWith('fix-') ? null : pageGet(id));
const styled = (el) => {
  const set = new Set();
  el.classList = { add: (c) => set.add(c), remove: (c) => set.delete(c),
    toggle: (c, on) => ((on === undefined ? !set.has(c) : on) ? set.add(c) : set.delete(c)),
    contains: (c) => set.has(c) };
  el.classes = set;
  return el;
};
const dots = {};
for (const name of INPUT.cards) {
  const dot = (dots[name] = element());
  const details = Object.assign(element(), {
    appendChild: (child) => { if (name === INPUT.name) appended.push(child); },
  });
  elements['card-' + name] = Object.assign(element(), {
    querySelector: (sel) => (sel === '.status-dot' ? dot : sel === '.integration-details' ? details : null),
  });
  elements['status-' + name] = styled(element());
}
const pageFetch = fetch;
fetch = async (url, options) => {
  if (url === INPUT.test_url) {
    fetched.push(url);
    return { ok: true, status: 200, json: async () => INPUT.test };
  }
  return pageFetch(url, options);
};
"""

_CLICK_RUN = r"""
(async () => {
  await testConnection(INPUT.name);
  await new Promise((resolve) => setTimeout(resolve, 0));
  const status = elements['status-' + INPUT.name];
  process.stdout.write(JSON.stringify({
    toasts,
    line: status.textContent,
    style: [...status.classes].filter((c) => c === 'error' || c === 'warning'),
    fix: appended.map((e) => e.textContent),
    dot: dots[INPUT.name].className,
    list: (elements['integrations-list'] || {}).innerHTML || '',
    link: elements[LINK] ? { text: elements[LINK].textContent, cls: elements[LINK].className } : null,
    fetched,
  }));
})();
"""


_TEST_ALL_RUN = r"""
(async () => {
  await testAllConnections();
  // Test All redraws without waiting for it; let the redraw's fetches settle.
  for (let i = 0; i < 10; i++) await new Promise((resolve) => setTimeout(resolve, 0));
  const lines = {};
  for (const name of INPUT.cards) {
    const status = elements['status-' + name];
    lines[name] = { line: status.textContent,
      style: [...status.classes].filter((c) => c === 'error' || c === 'warning') };
  }
  process.stdout.write(JSON.stringify({
    toasts, lines,
    list: (elements['integrations-list'] || {}).innerHTML || '',
    link: elements[LINK] ? { text: elements[LINK].textContent, cls: elements[LINK].className } : null,
    fetched,
  }));
})();
"""


_DIALOG = r"""
const toasts = [];
const Toast = { show(kind, title, message) { toasts.push({ kind, title, message }); } };
const dialogs = [];
// Every dialog is answered Cancel: nothing is disconnected.
const Dialog = { confirm: async (config) => { dialogs.push(config); return false; } };
// Disconnect All reads the drawn cards; as in a browser, a card without a status dot (one
// not offered in this beta) has none.
const pageAll = document.querySelectorAll;
document.querySelectorAll = (sel) => {
  if (sel !== '.integration-card') return pageAll(sel);
  const html = (elements['integrations-list'] || { innerHTML: '' }).innerHTML;
  return html.split('id="card-').slice(1).map((chunk) => {
    const name = chunk.slice(0, chunk.indexOf('"'));
    const h3 = (chunk.match(/<h3>([^<]*)<\/h3>/) || [])[1];
    const cls = (chunk.match(/class="status-dot ([^"]*)"/) || [])[1];
    const dot = cls === undefined ? null
      : { classList: { contains: (c) => cls.split(' ').includes(c) } };
    return { id: 'card-' + name,
      querySelector: (q) => (q === '.status-dot' ? dot : q === 'h3' ? { textContent: h3 } : null) };
  });
};
"""

_DIALOG_RUN = r"""
(async () => {
  await loadIntegrationsHealth();
  await new Promise((resolve) => setTimeout(resolve, 0));
  const html = (elements['integrations-list'] || {}).innerHTML || '';
  const pressed = [];
  for (const m of html.matchAll(/onclick="(disconnect[A-Za-z]*)\(([^)]*)\)"/g)) {
    const arg = m[2].replace(/&#39;|&quot;|['"]/g, '');
    const before = dialogs.length;
    await eval(m[1])(arg);
    pressed.push({ call: `${m[1]}('${arg}')`, card: arg, dialog: dialogs[before] || null });
  }
  const before = dialogs.length;
  const toastsBefore = toasts.length;
  await disconnectAllIntegrations();
  process.stdout.write(JSON.stringify({
    pressed, all: dialogs[before] || null, allToasts: toasts.slice(toastsBefore),
    disconnected: fetched.filter((u) => u.includes('disconnect')),
  }));
})();
"""


def page_scripts() -> Tuple[str, str]:
    """The page's offered-connectors line, and its script from the template."""
    from services.integrations import integration_status_service

    body = TEMPLATE.read_text(encoding="utf-8")
    marker = "<script>\n  // Integration icons mapping"
    if marker not in body or "window.__OFFERED_CONNECTORS__ = {{" not in body:
        raise Stopped("templates/integrations.html no longer has the scripts this reads")
    start = body.index(marker) + len("<script>")
    script = body[start : body.index("</script>", start)]
    if "{{" in script or "{%" in script:
        raise Stopped("the page's script now has template tags; it must be rendered, not read")
    # The page route fills the list from this same call (web/api/routes/ui.py).
    offered = list(integration_status_service.offered_connectors())
    return f"window.__OFFERED_CONNECTORS__ = {json.dumps(offered)};\n", script


def draw(
    payload: Dict[str, Any],
    scenario: Scenario,
    test: Optional[Tuple[str, Any]] = None,
) -> Dict[str, Any]:
    """Run the page's script under node: draw the page, or (``test`` given as the card
    name and the Test route's reply) press that card's Test and let the page redraw.
    With ``TEST_ALL`` as the name, press Test All."""
    offered, script = page_scripts()
    if scenario.offered is not None:
        offered = f"window.__OFFERED_CONNECTORS__ = {json.dumps(list(scenario.offered))};\n"
    given = {
        "health": payload,
        "health_url": HEALTH,
        "install": scenario.install_state,
        "install_url": INSTALL_STATE,
    }
    run = _RUN
    harness = _BROWSER
    if test is not None and test[0] == DIALOGS:
        harness += _DIALOG
        run = _DIALOG_RUN
    elif test is not None:
        url = (
            "/api/v1/integrations/test-all"
            if test[0] == TEST_ALL
            else f"/api/v1/integrations/test/{test[0]}"
        )
        given.update(name=test[0], test=test[1], test_url=url, cards=list(CARDS))
        harness = _BROWSER.replace("async function fetch", "let fetch = async function")
        harness += _CLICK
        run = _TEST_ALL_RUN if test[0] == TEST_ALL else _CLICK_RUN
    # The shell loads the shared escape helpers before any page script (#1582).
    shared = (ROOT / "web" / "static" / "js" / "escape.js").read_text(encoding="utf-8")
    js = f"const INPUT = {json.dumps(given)};\n" + harness + shared + offered + script + run
    done = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    if done.returncode != 0:
        raise Stopped(f"the page's script failed under node for '{scenario.key}'")
    return json.loads(done.stdout)


# --- step 3: read the drawn cards ------------------------------------------------------


class _Card(HTMLParser):
    """Text lines and controls of one card's HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.lines: List[str] = []
        self.controls: List[Dict[str, str]] = []
        self._control: Optional[Dict[str, str]] = None
        self._text: List[str] = []
        self._style = ""  # "error" or "warning" when the element holding the text is styled so

    def _flush(self) -> None:
        text = " ".join("".join(self._text).split())
        self._text = []
        if not text:
            return
        if self._control is not None:
            self._control["label"] = (self._control.get("label", "") + " " + text).strip()
        else:
            self.lines.append(f"{text} [{self._style} style]" if self._style else text)

    def handle_starttag(self, tag, attrs):
        self._flush()
        given = dict(attrs)
        classes = (given.get("class") or "").split()
        self._style = next((c for c in ("error", "warning") if c in classes), "")
        if tag in ("button", "a"):
            self._control = {
                "kind": "button" if tag == "button" else "link",
                "id": given.get("id") or "",
                "class": given.get("class") or "",
                "goes": given.get("href") or _call(given.get("onclick") or ""),
                "disabled": "yes" if "disabled" in given else "",
            }

    def handle_endtag(self, tag):
        self._flush()
        self._style = ""
        if tag in ("button", "a") and self._control is not None:
            self.controls.append(self._control)
            self._control = None

    def handle_data(self, data):
        self._text.append(data)


def _call(onclick: str) -> str:
    match = re.match(r"\s*([A-Za-z_]+)\(", onclick)
    return f"{match.group(1)}()" if match else ""


def card_html(listing: str, name: str) -> Optional[str]:
    marker = f'id="card-{name}"'
    if marker not in listing:
        return None
    start = listing.rindex("<div", 0, listing.index(marker))
    end = listing.find('id="card-', listing.index(marker) + 1)
    return listing[start:] if end == -1 else listing[start : listing.rindex("<div", 0, end)]


def read_card(drawn: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    html = card_html(drawn["list"], name)
    if html is None:
        return None
    parser = _Card()
    parser.feed(html)
    parser.close()
    for control in parser.controls:
        # The link's label is set after the list is drawn; show what the page ended with.
        if control["id"] == "github-repositories-link" and drawn.get("link"):
            control["label"] = drawn["link"]["text"]
            control["class"] = drawn["link"]["cls"]
    return {"lines": parser.lines, "controls": parser.controls}


# --- the file ---------------------------------------------------------------------------


def _shown(line: str) -> str:
    """A line as this Markdown file shows it: one that holds markup characters goes in a
    code span, so a reader sees the characters the card drew, not what they would render."""
    return f"`{line}`" if any(ch in line for ch in "<>&`") else line


def _style(css: str) -> str:
    names = [c for c in css.split() if c != "action-btn"]
    return ", ".join(names) or "plain"


def build() -> str:
    if shutil.which("node") is None:
        raise Stopped("node is not on PATH; the page's script can't be run")
    user_id = _setup()
    out = [
        "# Integrations cards, state by state",
        "",
        "Generated by `scripts/card_state_file.py`; do not edit by hand. Regenerate it with",
        "`venv/bin/python scripts/card_state_file.py` and read `git diff` on this file to see",
        "which words and controls changed.",
        "",
        "Each row is the health route's own payload for that state, drawn by the page's own",
        "script under node. It is not a browser and not the served app: no layout, no",
        "styling, no sign-in. The last sections press each card's Test, then Test All: the",
        "app's Test routes answer, the page shows the result, then redraws from the health",
        "route. Last, the confirm dialogs before a disconnect, answered Cancel. Not here: what",
        "a confirmed disconnect does, the Settings index and the GitHub repository page. The",
        "screen atlas covers layout.",
        "",
    ]
    for scenario in scenarios():
        payload = health_payload(user_id, scenario)
        drawn = draw(payload, scenario)
        out += [f"## {scenario.title}", "", f"State key: `{scenario.key}`", ""]
        if scenario.show == CARDS:
            out += [
                f"Headline: **{drawn['title']}**"
                + (f" ({drawn['subtitle']})" if drawn["subtitle"] else ""),
                "",
            ]
        for name in scenario.show:
            card = read_card(drawn, name)
            out.append(f"### {name}")
            out.append("")
            if card is None:
                out += ["No card is drawn.", ""]
                continue
            out += [f"- {_shown(line)}" for line in card["lines"]] or ["- (no text)"]
            out.append("")
            if card["controls"]:
                out += ["| Control | Label | Style | Goes to |", "|---|---|---|---|"]
                for control in card["controls"]:
                    kind = control["kind"] + (" (disabled)" if control["disabled"] else "")
                    out.append(
                        f"| {kind} | {control['label'] or '(no label)'} | "
                        f"{_style(control['class'])} | `{control['goes'] or 'nothing'}` |"
                    )
            else:
                out.append("No button or link.")
            out.append("")
    out += [
        "# After pressing Test: the GitHub card",
        "",
        "Each state starts from the card as drawn, presses Test, and reads what the page",
        'shows. "On the redrawn card" says whether the line shown at the click is one of',
        "the card's lines after the page redraws it (CXO: one sentence, one source).",
        "",
    ]
    for scenario in clicks():
        tested, payload = run_routes(user_id, scenario, test="github")
        pressed = draw(payload, scenario, test=("github", tested))
        out += [f"## Test: {scenario.title}", "", f"State key: `{scenario.key}`", ""]
        for toast in pressed["toasts"]:
            out.append(
                f"- Toast ({toast['kind']}): **{toast['title']}**. {_shown(toast['message'])}"
            )
        style = f" [{', '.join(pressed['style'])} style]" if pressed["style"] else ""
        out.append(f"- At the click, the card's line: {_shown(pressed['line'])}{style}")
        for fix in pressed["fix"]:
            out.append(f"- At the click, a fix line: {_shown(fix)}")
        card = read_card(pressed, "github")
        lines = card["lines"] if card else []
        out.append("- The card after the page redraws it:")
        out += [f"  - {_shown(line)}" for line in lines] or ["  - (no card is drawn)"]
        on_card = any(pressed["line"] and pressed["line"] in line for line in lines)
        out += [f"- The click's line is on the redrawn card: {'yes' if on_card else '**no**'}", ""]
    out += _connector_click_rows(user_id)
    out += _test_all_rows(user_id)
    out += _dialog_rows(user_id)
    return "\n".join(out).rstrip() + "\n"


_NAMES = {"notion": "Notion", "slack": "Slack", "calendar": "Calendar"}


def _connector_click_rows(user_id: str) -> List[str]:
    out = [
        "# After pressing Test: the Notion, Slack and Calendar cards",
        "",
        "As for GitHub. What each Test meets is stood in for underneath the app's own check:",
        "the stored credential (a made-up one) and the connector's reply. The error text the",
        "app records is its own.",
        "",
    ]
    shown = None
    for scenario in connector_clicks():
        (card,) = scenario.show
        if card != shown:
            out += [f"## {_NAMES[card]}", ""]
            shown = card
        tested, payload = run_routes(user_id, scenario, test=card)
        pressed = draw(payload, scenario, test=(card, tested))
        out += [f"### Test: {scenario.title}", "", f"State key: `{scenario.key}`", ""]
        out += _pressed_rows(pressed, card)
    return out


def _pressed_rows(pressed: Dict[str, Any], card: str) -> List[str]:
    out = [
        f"- Toast ({t['kind']}): **{t['title']}**. {_shown(t['message'])}"
        for t in pressed["toasts"]
    ]
    style = f" [{', '.join(pressed['style'])} style]" if pressed["style"] else ""
    out.append(f"- At the click, the card's line: {_shown(pressed['line'])}{style}")
    out += [f"- At the click, a fix line: {_shown(fix)}" for fix in pressed["fix"]]
    drawn = read_card(pressed, card)
    lines = drawn["lines"] if drawn else []
    out.append("- The card after the page redraws it:")
    out += [f"  - {_shown(line)}" for line in lines] or ["  - (no card is drawn)"]
    on_card = any(pressed["line"] and pressed["line"] in line for line in lines)
    out += [f"- The click's line is on the redrawn card: {'yes' if on_card else '**no**'}", ""]
    return out


def dialog_pages() -> List[Scenario]:
    """The pages the confirm dialogs are pressed from."""
    return [
        Scenario("dialogs-connected", "Every card connected", generic=_all("connected")),
        Scenario(
            "dialogs-nothing",
            "Nothing connected",
            generic=_all("not_configured"),
            github="nothing",
        ),
    ]


def _dialog_rows(user_id: str) -> List[str]:
    out = [
        "# Before a disconnect: the confirm dialogs",
        "",
        "Each card's Disconnect, then Disconnect All, pressed on the drawn page. The rows are",
        "what the page asked the dialog to show; every dialog is answered Cancel, and the last",
        "line of each page says whether anything was sent to a disconnect route.",
        "",
    ]
    for scenario in dialog_pages():
        payload = health_payload(user_id, scenario)
        pressed = draw(payload, scenario, test=(DIALOGS, None))
        out += [f"## Dialogs: {scenario.title}", "", f"State key: `{scenario.key}`", ""]
        for row in pressed["pressed"]:
            out += [f"### Disconnect on {row['card']} (`{row['call']}`)", ""]
            out += _dialog_lines(row["dialog"])
        out += ["### Disconnect All", ""]
        if pressed["all"]:
            out += _dialog_lines(pressed["all"])
        for toast in pressed["allToasts"]:
            out.append(
                f"- Toast ({toast['kind']}): **{toast['title']}**. {_shown(toast['message'])}"
            )
        if not pressed["all"] and not pressed["allToasts"]:
            out.append("- No dialog and no toast.")
        sent = ", ".join(pressed["disconnected"]) or "nothing"
        if out[-1] != "":
            out.append("")
        out += [f"Sent to a disconnect route after Cancel: {sent}", ""]
    return out


def _dialog_lines(dialog: Optional[Dict[str, Any]]) -> List[str]:
    if dialog is None:
        return ["- No dialog.", ""]
    message = [ln for ln in str(dialog.get("message", "")).split("\n")]
    out = [f"- Title: **{_shown(str(dialog.get('title', '')))}**", "- Message:"]
    out += [f"  > {_shown(ln)}" if ln else "  >" for ln in message]
    out.append(
        f"- Buttons: {dialog.get('confirmText') or 'OK'} (confirm), "
        f"{dialog.get('cancelText') or 'Cancel'}"
    )
    return out + [""]


def _test_all_rows(user_id: str) -> List[str]:
    out = [
        "# After pressing Test All",
        "",
        "Test All runs every card's Test through the app's Test All route, shows one toast,",
        "puts each result's line on its card, then redraws the page from the health route.",
        "",
    ]
    for scenario in test_all_clicks():
        tested, payload = run_routes(user_id, scenario, test=TEST_ALL)
        pressed = draw(payload, scenario, test=(TEST_ALL, tested))
        out += [f"## Test All: {scenario.title}", "", f"State key: `{scenario.key}`", ""]
        out += [
            f"- Toast ({t['kind']}): **{t['title']}**. {_shown(t['message'])}"
            for t in pressed["toasts"]
        ]
        out.append("")
        for card in CARDS:
            at = pressed["lines"][card]
            style = f" [{', '.join(at['style'])} style]" if at["style"] else ""
            drawn = read_card(pressed, card)
            lines = drawn["lines"] if drawn else []
            on_card = any(at["line"] and at["line"] in line for line in lines)
            out += [
                f"### {card}",
                "",
                f"- At the click, the card's line: {_shown(at['line'])}{style}",
                "- The card after the page redraws it:",
            ]
            out += [f"  - {_shown(line)}" for line in lines] or ["  - (no card is drawn)"]
            out += [
                f"- The click's line is on the redrawn card: {'yes' if on_card else '**no**'}",
                "",
            ]
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the Integrations card-state file.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true", help="exit 1 if the file is stale")
    args = parser.parse_args(argv)
    # Never the OS keychain (xian, 2026-11-11). Set here, for the script's own process, and
    # not in _setup(): the tests call _setup() and build() inside pytest's process, where a
    # value written to os.environ would stay for every test that runs after them.
    os.environ["PIPER_CREDENTIAL_STORE"] = "db"
    try:
        text = build()
    except Stopped as stopped:
        print(f"card_state_file: stopped: {stopped}", file=sys.stderr)
        return 2
    if args.check:
        current = args.out.read_text(encoding="utf-8") if args.out.exists() else ""
        if current != text:
            print(f"card_state_file: {args.out} is stale; regenerate it", file=sys.stderr)
            return 1
        print(f"card_state_file: {args.out} is current")
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    pressed = len(clicks()) + len(connector_clicks()) + len(test_all_clicks()) + len(dialog_pages())
    print(f"card_state_file: wrote {args.out} ({len(scenarios())} states, {pressed} presses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
