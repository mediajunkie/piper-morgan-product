"""Issue 2468 (found by PA, 2026-11-27): the Claude connector's connect-required line
must not follow ``app_mode()``.

Issue 2261 made ``degrade()`` choose that line by ``app_mode()``, which reads the
process's own GitHub App values. The MCP app never holds the App's client secret, so in
its process App mode is always off, and a connector user would have read the line for an
install with no GitHub App while beta offers the App connect.

LAYER: unit. The real adapter's ``degrade()`` and the real ``github_connector_reply``,
with the environment set as each process has it. DENOMINATOR: every member of
``DegradationReason``. Not covered: the MCP server's tool text end to end, and anything
served.
"""

from __future__ import annotations

import pytest

from services.mcp.consumer import github_adapter as adapter_mod
from services.mcp.consumer.connector import DegradationReason
from services.mcp.consumer.github_adapter import (
    CONNECTOR_REPLY_BRANCHES,
    CONNECTOR_REPLY_FALLS_THROUGH,
    GITHUB_CONNECTOR_CONNECT_REQUIRED_REPLY,
    GitHubMCPSpatialAdapter,
    github_connector_reply,
)

_APP_ENV = ("GITHUB_APP_CLIENT_ID", "GITHUB_APP_CLIENT_SECRET")


@pytest.fixture
def mcp_process(monkeypatch):
    """The MCP app's process: no GitHub App values at all."""
    for name in _APP_ENV:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def beta_process(monkeypatch):
    monkeypatch.setenv("GITHUB_APP_CLIENT_ID", "test-app-client-id")
    monkeypatch.setenv("GITHUB_APP_CLIENT_SECRET", "test-app-client-secret")


def test_the_words_are_what_the_connector_said_before_2261():
    assert GITHUB_CONNECTOR_CONNECT_REQUIRED_REPLY == "Connect GitHub to continue."


async def test_in_the_mcp_process_the_connector_line_is_its_own(mcp_process):
    degraded = await GitHubMCPSpatialAdapter().degrade(DegradationReason.CONNECT_REQUIRED)
    # The fact this issue is about: in this process degrade() picks the no-App line.
    assert degraded.user_message == adapter_mod.GITHUB_CONNECT_REQUIRED_NO_APP_LINE
    reply = github_connector_reply(degraded)
    assert reply == GITHUB_CONNECTOR_CONNECT_REQUIRED_REPLY
    assert "personal access token" not in reply
    assert adapter_mod.GITHUB_CONNECT_REQUIRED_NO_APP_LINE not in reply


async def test_the_connector_line_is_the_same_in_either_process(mcp_process, monkeypatch):
    off = github_connector_reply(
        await GitHubMCPSpatialAdapter().degrade(DegradationReason.CONNECT_REQUIRED)
    )
    monkeypatch.setenv("GITHUB_APP_CLIENT_ID", "test-app-client-id")
    monkeypatch.setenv("GITHUB_APP_CLIENT_SECRET", "test-app-client-secret")
    on = github_connector_reply(
        await GitHubMCPSpatialAdapter().degrade(DegradationReason.CONNECT_REQUIRED)
    )
    assert off == on == GITHUB_CONNECTOR_CONNECT_REQUIRED_REPLY


def test_every_reason_has_a_branch_or_falls_through_by_name():
    """Arch's pin: a new reason, or a reason whose ``user_message`` becomes
    mode-dependent, must be placed on one list or the other by hand."""
    assert not (CONNECTOR_REPLY_BRANCHES & CONNECTOR_REPLY_FALLS_THROUGH)
    assert CONNECTOR_REPLY_BRANCHES | CONNECTOR_REPLY_FALLS_THROUGH == set(DegradationReason)


@pytest.mark.parametrize("reason", sorted(CONNECTOR_REPLY_BRANCHES, key=lambda r: r.value))
async def test_a_branched_reason_never_returns_user_message(reason, mcp_process):
    degraded = await GitHubMCPSpatialAdapter().degrade(reason)
    assert github_connector_reply(degraded) != degraded.user_message


@pytest.mark.parametrize("reason", sorted(CONNECTOR_REPLY_FALLS_THROUGH, key=lambda r: r.value))
async def test_a_fall_through_reason_reads_the_same_in_either_process(reason, monkeypatch):
    """What makes falling through safe: these messages do not depend on the mode."""
    for name in _APP_ENV:
        monkeypatch.delenv(name, raising=False)
    off = await GitHubMCPSpatialAdapter().degrade(reason)
    monkeypatch.setenv("GITHUB_APP_CLIENT_ID", "test-app-client-id")
    monkeypatch.setenv("GITHUB_APP_CLIENT_SECRET", "test-app-client-secret")
    on = await GitHubMCPSpatialAdapter().degrade(reason)
    assert off.user_message == on.user_message
    assert github_connector_reply(off) == off.user_message == github_connector_reply(on)


async def test_the_beta_apps_own_surfaces_keep_the_mode_branch(beta_process):
    degraded = await GitHubMCPSpatialAdapter().degrade(DegradationReason.CONNECT_REQUIRED)
    assert degraded.user_message == "Connect GitHub to continue."
