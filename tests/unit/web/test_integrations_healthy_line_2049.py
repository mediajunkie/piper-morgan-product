"""#2045 (CXO ruling): a tested card reads "Healthy. Checked just now.", "Healthy. Last
checked N minutes ago.", "... at 7:55 AM." or "... Oct 15." in the viewer's zone, never a
raw ISO UTC stamp; a failed card keeps its error line and appends the same fragment. The route sends ``Healthy`` plus an ISO ``last_check``; the
page formats it. Layers: route function; the page's own JS under Node (skipped without
``node``). Not a browser.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from services.integrations.principal_test_results import PrincipalTestResultStore
from web.api.routes import integrations

REPO = Path(__file__).resolve().parents[3]
PAGE_SRC = (REPO / "templates/integrations.html").read_text()
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


@pytest.mark.asyncio
async def test_route_healthy_card_is_plain_healthy_with_iso_last_check():
    store = PrincipalTestResultStore()
    store.record_test_result("u1", "calendar", ok=True, latency_ms=12.0)
    meta = integrations.INTEGRATION_REGISTRY["calendar"]
    with (
        patch.object(
            integrations, "_get_integration_config_status", new=AsyncMock(return_value="configured")
        ),
        patch.object(integrations, "_get_test_result_store", return_value=store),
    ):
        st = await integrations._check_integration_health("calendar", meta, user_id="u1")
    assert st.status == "healthy"
    assert st.status_message == "Healthy"
    assert datetime.fromisoformat(st.last_check).tzinfo is not None


def _run(last_check: str, now: str, status="healthy", msg="Healthy") -> tuple[str, str, str]:
    consts = PAGE_SRC[
        PAGE_SRC.index("// Integration icons mapping") : PAGE_SRC.index(
            "// Status icons for overall health"
        )
    ]
    start = PAGE_SRC.index("function renderIntegrations(integrations) {")
    end = PAGE_SRC.index("async function testConnection(integrationName)")
    script = (
        "const window = { __OFFERED_CONNECTORS__: ['github', 'calendar'] };\n"
        "const out = {};\n"
        "const document = { getElementById(id) {\n"
        "  if (id === 'integrations-list') return out;\n"
        "  return null; } };\n"
        "const RealDate = Date; const FIXED = new RealDate(process.argv[2]);\n"
        "globalThis.Date = class extends RealDate {\n"
        "  constructor(...a) { if (a.length) super(...a); else super(FIXED.getTime()); }\n"
        "};\n" + consts + PAGE_SRC[start:end] + "\nconst t = new RealDate(process.argv[1]);\n"
        "renderIntegrations([{name:'calendar',display_name:'Google Calendar',"
        "status:process.argv[3],status_message:process.argv[4],last_check:process.argv[1],"
        "can_test:true,configure_url:'/settings/integrations/calendar'}]);\n"
        "const same = t.toLocaleTimeString([], {hour:'numeric',minute:'2-digit'});\n"
        "const day = t.toLocaleDateString([], {month:'short',day:'numeric'});\n"
        "process.stdout.write(JSON.stringify({html: out.innerHTML, same, day}));\n"
    )
    res = subprocess.run(
        ["node", "-e", script, last_check, now, status, msg],
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "TZ": "America/Los_Angeles"},
    )
    assert res.returncode == 0, res.stderr
    d = json.loads(res.stdout)
    return " ".join(d["html"].split()), d["same"], d["day"]


def _line(html: str) -> str:
    return html.split('id="status-calendar">')[1].split("</span>")[0].strip()


@needs_node
def test_under_a_minute_reads_checked_just_now():
    html, _, _ = _run("2026-10-16T14:55:00Z", "2026-10-16T14:55:30Z")
    assert _line(html) == "Healthy. Checked just now."
    assert "T14:" not in html


@needs_node
@pytest.mark.parametrize(
    "now,expect",
    [
        ("2026-10-16T14:56:00Z", "Healthy. Last checked 1 minute ago."),
        ("2026-10-16T15:07:30Z", "Healthy. Last checked 12 minutes ago."),
        ("2026-10-16T15:54:59Z", "Healthy. Last checked 59 minutes ago."),
    ],
)
def test_under_an_hour_reads_minutes_ago(now, expect):
    html, _, _ = _run("2026-10-16T14:55:00Z", now)
    assert _line(html) == expect


@needs_node
def test_earlier_today_reads_the_viewers_clock_time():
    # The node run is pinned to a fixed viewer zone (see _run), so 07:00 and 09:00 are
    # the same local day; the expected time comes from the same toLocaleTimeString call.
    html, same, _ = _run("2026-10-16T14:00:00Z", "2026-10-16T16:00:00Z")
    assert _line(html) == f"Healthy. Last checked at {same}."
    assert "T14:" not in html


@needs_node
def test_other_day_reads_short_month_and_day_without_time():
    html, same, day = _run("2026-10-14T14:55:00Z", "2026-10-16T14:56:30Z")
    assert _line(html) == f"Healthy. Last checked {day}."
    assert same not in _line(html)
    assert "T14:" not in html


@needs_node
def test_failed_card_keeps_its_error_line_and_appends_the_fragment():
    html, _, _ = _run("2026-10-16T14:55:00Z", "2026-10-16T14:55:10Z", "failed", "Token expired")
    assert _line(html) == "Token expired. Checked just now."
    html, _, _ = _run("2026-10-16T14:55:00Z", "2026-10-16T15:00:00Z", "failed", "Token expired.")
    assert _line(html) == "Token expired. Last checked 5 minutes ago."


def test_page_script_defines_the_formatter_with_an_injectable_clock():
    assert "function formatCheckedAt(iso, now)" in PAGE_SRC
