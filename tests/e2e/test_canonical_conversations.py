"""
E2E: Automated canonical conversation suite.

Converts the manual canonical-retest-m1.py runner into a pytest parametrized
suite using ASGI transport. Two tiers:

Tier 1 (deterministic, every PR):
  - Routing assertions: verify each query reaches expected destination
  - Response structure: 200 OK, non-empty message, no error fingerprints
  - No LLM judge calls — fast and free

Tier 2 (LLM judge, scheduled/manual):
  - Quality scoring via Colleague Test rubric (R/C/T 0-3)
  - Requires CANONICAL_JUDGE_ENABLED=true and an API key
  - Marks: @pytest.mark.llm_judge

Issue: #928 E2E Automated canonical conversation suite
Supports: #926 M1 Gate, canonical-query-test-matrix-v3.md

Cost note: Tier 1 is free. Tier 2 costs ~$0.40/run at Sonnet pricing,
or less with Gemini as judge. Configure CANONICAL_JUDGE_MODEL to switch.

Requirements:
- PostgreSQL running on port 5433
- Database migrations current
- LLM API key in environment (for floor responses)
"""

import json
import os
from collections import Counter
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from unittest.mock import AsyncMock, patch
from uuid import UUID, uuid4

import httpx
import pytest
import pytest_asyncio
from httpx import ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------------------------
# Canonical query corpus (from canonical-retest-m1.py, reconciled Apr 12)
# Format: (query_num, query_text, category, expected_routing, known_issue)
# ---------------------------------------------------------------------------

CANONICAL_QUERIES = [
    # Identity (5) — all floor
    (1, "What's your name?", "Identity", "floor", None),
    (2, "What can you help me with?", "Identity", "floor", None),
    (3, "Are you working properly?", "Identity", "floor", None),
    (4, "How do I get help?", "Identity", "floor", None),
    (5, "What makes you different?", "Identity", "floor", None),
    # Temporal (5) — Q6 canonical, Q7/9/10 floor, Q8 canonical (pre-classifier→query)
    (6, "What day is it?", "Temporal", "canonical", None),
    (7, "What did we accomplish yesterday?", "Temporal", "floor", None),
    (8, "What's on the agenda for today?", "Temporal", "canonical", None),
    (9, "When was the last time we worked on this?", "Temporal", "floor", None),
    (10, "How long have we been working on this project?", "Temporal", "floor", None),
    # Spatial / Status (4) — all floor
    (11, "What projects are we working on?", "Spatial", "floor", None),
    (12, "Show me the project landscape", "Spatial", "floor", None),
    (13, "Which project should I focus on?", "Spatial", "floor", None),
    (14, "What's the status of project X?", "Spatial", "floor", None),
    # Capability (5)
    (16, "Create a GitHub issue about testing", "Capability", "action", None),
    (17, "Analyze this document", "Capability", "canonical", None),  # routes as analysis
    (18, "List all my projects", "Capability", "floor", None),
    (19, "Generate a status report", "Capability", "floor", None),
    (
        20,
        "Search for authentication in our documents",
        "Capability",
        "canonical",
        None,
    ),  # routes as query
    # Predictive (5)
    (21, "What should I focus on today?", "Predictive", "floor", None),
    # #1395 rev NOTE — Q22 HELD at floor, deliberately excluded from the 6-row rev:
    # it OSCILLATED across runs with no intervening routing change (canonical in
    # Run 15 2026-07-12; floor in the 2026-08-01 baseline). An oscillator must not
    # enter the contract on a single observation (the one-green-observation error).
    # STABILITY CRITERION before any future flip (Arch-ratified 2026-08-01): THREE
    # consecutive full-corpus runs, same destination, no intervening routing-code
    # change. If Q22 oscillates AGAIN after meeting that bar, do NOT keep
    # re-testing — mark it a known non-deterministic row; that is a finding about
    # the classifier, not a row awaiting resolution.
    # ✅ CRITERION MET 2026-08-05 (#1467 closed): floor ×3 consecutive on an
    # unchanged routing stack (8/2 22:00, 8/5 06:50, 8/5 12:50) — the floor
    # expectation is CONFIRMED. The Run-15 canonical observation stands as a
    # one-off; a future flip re-enters through this same criterion.
    (22, "What patterns do you see?", "Predictive", "floor", "M2 Beta"),
    (23, "What risks should I be aware of?", "Predictive", "floor", "M2 Beta"),
    (24, "What opportunities should I pursue?", "Predictive", "floor", "M2 Beta"),
    (
        25,
        "What's the next milestone?",
        "Predictive",
        "canonical",
        None,
    ),  # routes as list_milestones_query — deliberate (#898 status fix, #1039 milestone handler); stale floor expectation fixed per #1200
    # Conversational (5)
    (26, "What else can you help with?", "Conversational", "floor", None),
    (27, "Tell me more about the GitHub integration", "Conversational", "floor", None),
    (28, "How do I use the calendar feature?", "Conversational", "floor", None),
    (29, "What changed since yesterday?", "Conversational", "canonical", None),
    (30, "What needs my attention?", "Conversational", "canonical", None),
    # Scheduling (5)
    (31, "Schedule a meeting about the roadmap", "Scheduling", "canonical", "M2"),
    (32, "Remind me to review PRs tomorrow", "Scheduling", "action", "M2"),
    (33, "Find time for a 1:1 with the team lead", "Scheduling", "canonical", "M2"),
    (34, "How much time am I spending in meetings?", "Scheduling", "canonical", None),
    (35, "Review my recurring meetings", "Scheduling", "canonical", None),
    # Documents (4)
    (36, "Create a doc from this conversation", "Documents", "action", "1395-rev"),
    (37, "Compare these two documents", "Documents", "floor", "M2"),
    # Q38 expectation updated 2026-08-21: #1624 (chat summarize, shipped 08-16) added the
    # bare-`summarize` normalization -> summarize_document rail; this phrasing now routes
    # CANONICAL to the rail's honest no-upload answer instead of the #1187 floor path.
    # That is the DESIGNED behavior, not drift — the rail answers honestly when no
    # document resolves. Pre-1624 expectation was "floor" (Run 11 era).
    (38, "Synthesize these sources into a summary", "Documents", "canonical", "M2"),
    (
        40,
        "Update the project roadmap document",
        "Documents",
        "canonical",
        "M2",
    ),  # routes as portfolio
    # GitHub Ops (8)
    (41, "What did we ship this week?", "GitHub Ops", "canonical", None),
    (42, "Show me stale PRs", "GitHub Ops", "canonical", None),
    (43, "What's blocking the milestone?", "GitHub Ops", "floor", None),
    (44, "Create issues from this meeting's action items", "GitHub Ops", "action", "1395-rev"),
    (45, "Close completed issues", "GitHub Ops", "action", "1395-rev"),
    (58, "Update issue #123", "GitHub Ops", "action", None),
    (59, "Comment on issue #456", "GitHub Ops", "canonical", None),
    (60, "Review issue #789", "GitHub Ops", "canonical", None),
    # Slack (5)
    (46, "Any mentions I missed?", "Slack", "floor", "M2"),
    (47, "Summarize #general from yesterday", "Slack", "floor", "M2"),
    (48, "Post this update to the team channel", "Slack", "action", "1395-rev"),
    (49, "/standup", "Slack", "action", None),
    (50, "/piper help", "Slack", "floor", None),
    # Productivity (3)
    (51, "What's my productivity this week?", "Productivity", "canonical", "1395-rev"),
    (52, "Are we on track for the milestone?", "Productivity", "floor", None),
    (53, "What did the team accomplish this sprint?", "Productivity", "floor", None),
    # Todo Management (4)
    (54, "Add a todo: review the deployment plan", "Todos", "action", None),
    (55, "Complete the PR review todo", "Todos", "action", None),
    (56, "Show my todos", "Todos", "canonical", None),
    (57, "What's my next todo?", "Todos", "canonical", None),
    # Calendar Extended (2)
    (61, "What's my week look like?", "Calendar Ext", "canonical", None),
    (62, "Check my calendar for conflicts", "Calendar Ext", "canonical", None),
    # Knowledge (1)
    (63, "Upload a file to the knowledge base", "Knowledge", "action", "1395-rev"),
]

# Error fingerprints that indicate broken responses.
# #1213 P2: broadened beyond the original 4 — the Q16 lesson is that error /
# graceful-degradation detection must NOT hinge on one canned string (Q16's
# "something unexpected happened" was the only thing that caught a real wiring
# failure). The additions are high-confidence FAILURE phrasings. Honest
# *limitations* are deliberately excluded ("I couldn't find any X", "you have no
# X", "I don't have access yet", "no results" are honest, not errors) so the
# every-PR structure tier doesn't false-fail them. Verified against all 61
# canonical responses (no legit response trips the broadened list).
ERROR_FINGERPRINTS = [
    "something unexpected happened",
    "internal server error",
    "traceback",
    "exception",
    # P2 additions (generic failures, not honest limitations):
    "something went wrong",
    "an error occurred",
    "unexpected error",
    "failed to process",
    "unable to complete your request",
    "service unavailable",
    "internal error",
]

# Template fingerprints that indicate canned (non-floor) responses
# These should NOT appear in floor-routed responses
TEMPLATE_FINGERPRINTS = [
    "i'm piper morgan — i work alongside you on product management",
    "i'm here to help! what's on your mind",
    "looking forward to getting to know you better",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def send_canonical_query(client, query_text, query_num, auth=None):
    """Send a canonical query and return the parsed response."""
    kwargs = {
        "json": {
            "message": query_text,
            # #1165: unique session_id PER CALL. With the module-scoped (boot-once)
            # app, the in-memory conversation registry persists across the suite, so
            # a stable per-query session_id would bleed context across the 4 tiers
            # that each re-ask the same Q. A unique id reproduces the old
            # fresh-app-per-test isolation (each canonical query is single-turn).
            # #1395: a REAL UUID, not "canonical-e2e-qN-<hex>" — the old 26-char
            # slug flowed into owner_id::UUID queries downstream (productivity
            # handler) and manufactured an asyncpg DataError that poisoned Q51's
            # quality row. Query-number traceability lives in the assert messages.
            "session_id": str(uuid4()),
        }
    }
    if auth:
        kwargs.update(auth)
    response = await client.post("/api/v1/intent", **kwargs)
    assert (
        response.status_code == 200
    ), f"Q{query_num} HTTP {response.status_code}: {response.text[:200]}"
    return response.json()


def determine_actual_routing(intent_data: dict) -> str:
    """Classify the actual routing from the API response."""
    if not intent_data:
        return "unknown"
    if intent_data.get("floor_hit") is True:
        return "floor"
    category = (intent_data.get("category") or "").lower()
    if category == "execution":
        return "action"
    return "canonical"


# ---------------------------------------------------------------------------
# #1676: serving-LLM capture — record which provider+model ACTUALLY answered
# this run's queries. The confound this closes: the seat's primary provider can
# 429 (credit exhaustion) and classification silently falls back cross-provider,
# so two runs can classify on DIFFERENT MODELS with nothing in
# canonical-retest-history.csv recording it (Run 14 vs Run 15's Q36 flip is
# fully explainable this way). Same discipline as #1620 / the Phase-2 gate's
# "Model identity (m-43)" section — but recorded BY THE HARNESS at run time
# from the serving site (services/llm/clients.py SERVING_MODEL_RECORD,
# incremented only on a successful provider call), never reconstructed from
# config-at-rest. Works because this suite boots the app IN-PROCESS
# (ASGITransport), so the module-level Counter is directly readable.
#
# NOT counted: Tier 2's judge calls — the judge_client is a direct Anthropic
# SDK client, not routed through LLMClient. The judge model stays a notes-level
# fact (JUDGE_MODEL env); the new CSV columns describe the SERVING LLM only.
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[2]
SERVING_REPORT_PATH = _REPO_ROOT / "dev" / "active" / "canonical-retest-serving-llm.json"


def build_serving_report(served: Counter) -> dict:
    """Collapse the per-run serving delta into the CSV-ready shape.

    CSV-safety invariant: neither value ever contains a comma (the history CSV
    is comma-delimited with unquoted fields) — mixed-run detail uses ';'.
    """
    total = sum(served.values())
    if total == 0:
        provider = model = "none"
    elif len(served) == 1:
        provider, model = next(iter(served)).split(":", 1)
    else:
        # More than one provider:model served this run — the run itself is the
        # confound. Name every serving pair with counts; don't average it away.
        provider = "mixed"
        model = ";".join(f"{k}({n})" for k, n in sorted(served.items()))
    return {
        "serving_provider": provider,
        "serving_model": model,
        "llm_calls_served": total,
        "calls": dict(sorted(served.items())),
    }


@pytest.fixture(scope="module", autouse=True)
def serving_llm_report():
    """#1676: snapshot SERVING_MODEL_RECORD around the whole module; on
    teardown, print the run's serving-LLM report and write it to
    dev/active/canonical-retest-serving-llm.json so the operator appending the
    history-CSV row has the serving_provider/serving_model values verbatim
    (see docs/internal/operations/canonical-retest-history-update.md)."""
    from services.llm.clients import SERVING_MODEL_RECORD

    before = Counter(SERVING_MODEL_RECORD)
    yield
    served = Counter(SERVING_MODEL_RECORD) - before
    report = build_serving_report(served)
    report["run_at"] = datetime.now(timezone.utc).isoformat()
    report["judge_model"] = JUDGE_MODEL if JUDGE_ENABLED else "judge-off"
    try:
        SERVING_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        SERVING_REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    except OSError:  # silent-ok: report file is best-effort; the print below still lands
        pass
    print("\n=== CANONICAL RUN SERVING LLM (#1676) ===")
    print(json.dumps(report, indent=2))
    print(
        "history-CSV columns -> "
        f"serving_provider={report['serving_provider']} "
        f"serving_model={report['serving_model']}"
    )


class TestServingReportShape:
    """#1676: the report builder's contract (no LLM, no app boot — runs in
    keyless sweeps)."""

    def test_zero_served_is_none_not_a_guess(self):
        r = build_serving_report(Counter())
        assert r["serving_provider"] == "none"
        assert r["serving_model"] == "none"
        assert r["llm_calls_served"] == 0

    def test_single_provider_model_splits_cleanly(self):
        r = build_serving_report(Counter({"anthropic:claude-haiku-4-5": 117}))
        assert r["serving_provider"] == "anthropic"
        assert r["serving_model"] == "claude-haiku-4-5"
        assert r["llm_calls_served"] == 117

    def test_mixed_run_names_every_pair_and_stays_csv_safe(self):
        r = build_serving_report(
            Counter({"anthropic:claude-haiku-4-5": 57, "openai:gpt-4o": 4})
        )
        assert r["serving_provider"] == "mixed"
        assert "anthropic:claude-haiku-4-5(57)" in r["serving_model"]
        assert "openai:gpt-4o(4)" in r["serving_model"]
        # CSV-safety: values must never contain the delimiter
        assert "," not in r["serving_provider"]
        assert "," not in r["serving_model"]


# ---------------------------------------------------------------------------
# #1165: MODULE-scoped app fixtures — boot the app ONCE for the whole canonical
# suite. The shared (function-scoped) e2e_client in conftest boots the full app
# PER TEST (~240 boots/process); accumulated logging/runtime state makes
# LLMDomainService.initialize's env-var-fallback warning recurse at ~boot 49,
# erroring every subsequent test at setup (the long-standing "env-error cascade").
# Production boots once and never hits this. Booting once here makes the suite
# runnable end-to-end + removes the env-error column. These OVERRIDE the conftest
# fixtures BY NAME for this module only (surgical — zero blast radius to other
# tests/e2e suites). The session-scoped event_loop (tests/conftest.py, Issue #290)
# lets module-scoped async fixtures work with no event-loop override.
# ---------------------------------------------------------------------------

_CANON_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest_asyncio.fixture(scope="module")
async def e2e_client():
    """#1165: module-scoped — boot the real app once for the canonical suite."""
    from web.app import app

    @asynccontextmanager
    async def _lifespan():
        async with app.router.lifespan_context(app):
            yield

    async with _lifespan():
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest_asyncio.fixture(scope="module")
async def e2e_auth_state(e2e_client):
    """#1165: module-scoped — one shared canonical test user (created + cleaned
    once). Per-query isolation comes from send_canonical_query's unique
    session_id, so the shared app's conversation registry doesn't bleed across
    queries; canonical queries are single-turn so a shared user is fine.

    #1675: yields BOTH the httpx auth kwargs and the authenticated user's id —
    the ground-truth tier seeds rows AS this principal through the service
    layer, so it needs the id, not just the cookie. (Kept out of
    e2e_auth_headers because send_canonical_query does kwargs.update(auth) —
    any non-httpx key there would break every call.)"""
    from services.auth.password_service import PasswordService

    user_id = str(uuid4())
    username = f"canon_e2e_{user_id[:8]}"
    password = "testpass123"
    password_hash = PasswordService().hash_password(password)

    engine = create_async_engine(_CANON_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        await s.execute(
            text(
                "INSERT INTO users (id, username, email, password_hash, is_active, "
                "is_verified, created_at, updated_at, role, is_alpha) "
                "VALUES (:id, :u, :e, :ph, true, true, :now, :now, 'user', true)"
            ),
            {
                "id": user_id,
                "u": username,
                "e": f"{username}@test.example.com",
                "ph": password_hash,
                "now": datetime.now(timezone.utc),
            },
        )
        await s.commit()

    login = await e2e_client.post(
        "/api/v1/auth/login", data={"username": username, "password": password}
    )
    assert login.status_code == 200, f"canonical login failed: {login.text}"
    yield {"auth": {"cookies": login.cookies}, "user_id": user_id}

    # Cleanup — the app creates dependent rows (personalization_contexts etc.)
    # mid-test; the hand-rolled FK order rotted as tables were added (#1452).
    # delete_test_user_fully is THE cascade (information_schema-derived).
    from tests.conftest import delete_test_user_fully

    async with async_session() as s:
        await delete_test_user_fully(s, user_id)
        await s.commit()
    await engine.dispose()


@pytest_asyncio.fixture(scope="module")
async def e2e_auth_headers(e2e_auth_state):
    """#1165: httpx auth kwargs only — the shape send_canonical_query splats.
    Derived from e2e_auth_state (#1675) so both fixtures share the one user."""
    return e2e_auth_state["auth"]


# ---------------------------------------------------------------------------
# Tier 1: Routing + Structure (deterministic, every PR)
# ---------------------------------------------------------------------------


class TestCanonicalRouting:
    # #1452: this tier drives the LIVE classifier (LLM calls) — the marker was
    # missing, so keyless sweeps (CI + local enumeration) ran it and failed all
    # of it; 227 of the burn-down backlog's entries were this one omission.
    pytestmark = pytest.mark.llm

    """Verify each canonical query reaches the expected routing destination.

    Deterministic — asserts on routing metadata, not LLM content.
    Safe for CI on every PR (no LLM judge cost).
    """

    @pytest.mark.e2e
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "query_num,query_text,category,expected_routing,known_issue",
        CANONICAL_QUERIES,
        ids=[f"Q{q[0]}-{q[2]}" for q in CANONICAL_QUERIES],
    )
    async def test_routing(
        self,
        e2e_client,
        e2e_auth_headers,
        query_num,
        query_text,
        category,
        expected_routing,
        known_issue,
    ):
        """Each query routes to its expected destination (floor/canonical/action)."""
        data = await send_canonical_query(e2e_client, query_text, query_num, e2e_auth_headers)

        intent = data.get("intent", {})
        actual = determine_actual_routing(intent)

        assert actual == expected_routing, (
            f"Q{query_num} ({category}): expected {expected_routing}, got {actual}. "
            f"Category={intent.get('category')}, floor_hit={intent.get('floor_hit')}"
        )


class TestCanonicalResponseStructure:
    # #1452: this tier drives the LIVE classifier (LLM calls) — the marker was
    # missing, so keyless sweeps (CI + local enumeration) ran it and failed all
    # of it; 227 of the burn-down backlog's entries were this one omission.
    pytestmark = pytest.mark.llm

    """Verify response structure is sound — non-empty, no errors, no dead ends.

    Deterministic — no LLM judge cost.
    """

    @pytest.mark.e2e
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "query_num,query_text,category,expected_routing,known_issue",
        CANONICAL_QUERIES,
        ids=[f"Q{q[0]}-{q[2]}" for q in CANONICAL_QUERIES],
    )
    async def test_response_not_empty(
        self,
        e2e_client,
        e2e_auth_headers,
        query_num,
        query_text,
        category,
        expected_routing,
        known_issue,
    ):
        """Every query gets a non-empty response."""
        data = await send_canonical_query(e2e_client, query_text, query_num, e2e_auth_headers)
        msg = data.get("message", "")
        assert len(msg) > 10, f"Q{query_num}: response too short ({len(msg)} chars): {msg}"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "query_num,query_text,category,expected_routing,known_issue",
        [q for q in CANONICAL_QUERIES if q[3] == "floor"],
        ids=[f"Q{q[0]}-{q[2]}" for q in CANONICAL_QUERIES if q[3] == "floor"],
    )
    async def test_floor_response_no_template(
        self,
        e2e_client,
        e2e_auth_headers,
        query_num,
        query_text,
        category,
        expected_routing,
        known_issue,
    ):
        """Floor-routed queries should NOT return template fingerprints."""
        data = await send_canonical_query(e2e_client, query_text, query_num, e2e_auth_headers)
        msg_lower = data.get("message", "").lower()

        for fingerprint in TEMPLATE_FINGERPRINTS:
            assert (
                fingerprint not in msg_lower
            ), f"Q{query_num}: floor response contains template: '{fingerprint}'"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "query_num,query_text,category,expected_routing,known_issue",
        CANONICAL_QUERIES,
        ids=[f"Q{q[0]}-{q[2]}" for q in CANONICAL_QUERIES],
    )
    async def test_no_error_fingerprints(
        self,
        e2e_client,
        e2e_auth_headers,
        query_num,
        query_text,
        category,
        expected_routing,
        known_issue,
    ):
        """No query should return error fingerprints in the response."""
        data = await send_canonical_query(e2e_client, query_text, query_num, e2e_auth_headers)
        msg_lower = data.get("message", "").lower()

        for fingerprint in ERROR_FINGERPRINTS:
            assert (
                fingerprint not in msg_lower
            ), f"Q{query_num}: response contains error fingerprint: '{fingerprint}'"


# ---------------------------------------------------------------------------
# Tier 2: Quality via LLM Judge (scheduled, costs ~$0.40/run)
# ---------------------------------------------------------------------------

JUDGE_ENABLED = os.getenv("CANONICAL_JUDGE_ENABLED", "false").lower() == "true"
JUDGE_MODEL = os.getenv("CANONICAL_JUDGE_MODEL", "claude-sonnet-4-6")

# Colleague Test rubric for the judge
JUDGE_SYSTEM_PROMPT = """You are scoring Piper Morgan's response against the Colleague Test rubric.

Score three dimensions, 0-3 each:

Relevance (R): Does the response engage with what the user asked?
0=ignored question, 1=vaguely gestured, 2=partial engagement, 3=directly engaged

Context (C): Does the response reference real data or acknowledge gaps honestly?
0=fabricated/empty, 1=generic, 2=some real context, 3=rich accurate context

Tone (T): Does the response sound like a colleague?
0=robotic/template, 1=polite but stilted, 2=conversational, 3=distinctly colleague-like

Return ONLY valid JSON:
{"relevance": <0-3>, "context": <0-3>, "tone": <0-3>, "total": <sum>, "verdict": "PASS"|"MARGINAL"|"FAIL"}

PASS: total >= 7, no dimension = 0. MARGINAL: total 5-6, no zeros. FAIL: total < 5 or any zero."""


@pytest.mark.skipif(not JUDGE_ENABLED, reason="CANONICAL_JUDGE_ENABLED not set")
class TestCanonicalQuality:
    # #1452: this tier drives the LIVE classifier (LLM calls) — the marker was
    # missing, so keyless sweeps (CI + local enumeration) ran it and failed all
    # of it; 227 of the burn-down backlog's entries were this one omission.
    pytestmark = pytest.mark.llm

    """LLM-as-judge quality scoring. Requires CANONICAL_JUDGE_ENABLED=true.

    Cost: ~$0.01 per query at Sonnet pricing. ~$0.40 for full 61-query run.
    Set CANONICAL_JUDGE_MODEL to use a cheaper model (e.g., gemini-1.5-flash).
    """

    @pytest.fixture(scope="class")
    def judge_client(self):
        """Create the judge LLM client."""
        try:
            from anthropic import Anthropic

            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                return Anthropic(api_key=api_key)
        except ImportError:
            pass
        pytest.skip("Anthropic client not available for judge")

    @pytest.mark.e2e
    @pytest.mark.llm_judge
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "query_num,query_text,category,expected_routing,known_issue",
        [q for q in CANONICAL_QUERIES if q[3] == "floor" and q[4] is None],
        ids=[f"Q{q[0]}-{q[2]}" for q in CANONICAL_QUERIES if q[3] == "floor" and q[4] is None],
    )
    async def test_quality_pass(
        self,
        e2e_client,
        e2e_auth_headers,
        judge_client,
        query_num,
        query_text,
        category,
        expected_routing,
        known_issue,
    ):
        """Floor-routed queries (non-known-issue) should score 7+ on Colleague Test."""
        data = await send_canonical_query(e2e_client, query_text, query_num, e2e_auth_headers)
        response_text = data.get("message", "")

        # Call judge
        judge_prompt = f'Query: {query_text!r}\n\nResponse:\n"""\n{response_text}\n"""'
        msg = judge_client.messages.create(
            model=JUDGE_MODEL,
            max_tokens=300,
            temperature=0.2,
            system=JUDGE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": judge_prompt}],
        )
        raw = msg.content[0].text.strip()

        # Parse judge response
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        scores = json.loads(raw)
        total = scores.get("total", 0)
        verdict = scores.get("verdict", "FAIL")
        ctx = scores.get("context", 0)

        # #1213 P4: raise the scoring bar (PM 2026-06-13: "raise the scoring; we
        # can always compare new and old rubrics over time"). The judge still
        # returns the full R/C/T + verdict (so scores stay comparable run-to-run);
        # only the PASS THRESHOLD changes, and it's a toggle so old-vs-new pass
        # rates are an env flip, not a code change:
        #   STRICT (default): require a real PASS (verdict==PASS == total>=7, no
        #     zeros). Drops MARGINAL-as-pass — the old bar let 5-6/9 through.
        #   LENIENT (CANONICAL_JUDGE_STRICT=false): the old bar (PASS or MARGINAL).
        # NOTE: deliberately NOT a per-dimension Context floor. Verified 2026-06-13
        # that Context=1 is *correct* for context-less queries (identity "what's
        # your name" legitimately references no user data → R=3 C=1 T=3 = PASS), so
        # a blanket Context>=2 floor false-fails them. Data-grounding for
        # data-bearing queries is P1's job (deterministic ground-truth assertions),
        # not a judge floor.
        strict = os.getenv("CANONICAL_JUDGE_STRICT", "true").strip().lower() == "true"
        if strict:
            passed = verdict == "PASS"
            bar = "STRICT (PASS only)"
        else:
            passed = verdict in ("PASS", "MARGINAL")
            bar = "LENIENT (PASS|MARGINAL)"

        assert passed, (
            f"Q{query_num} ({category}): quality {verdict} under {bar} "
            f"(R={scores.get('relevance')} C={ctx} T={scores.get('tone')} = {total}/9). "
            f"Response: {response_text[:150]}"
        )


# ---------------------------------------------------------------------------
# Tier 1b: Multi-turn antecedent resolution (deterministic, every PR) — #1213 P3
#
# Guards the #1122 / #1207 antecedent-resolution surface (the floor + structured
# dispatch must see prior-turn history) with a CHEAP, every-PR check. This
# COMPLEMENTS — does not duplicate — the gated, LLM-judge AAXT golden scenarios
# (tests/aaxt/test_golden_scenarios.py, which need AAXT_ENABLED + ~$0.50/run).
#
# The assertion is the #1122 regression's robust primary signal: when antecedent
# resolution FAILS, the handler emits a CANNED clarification punt ("I need to
# know which document to update", services/intent/intent_service.py:2927); when
# it SUCCEEDS, that punt is absent. The punt is templated (not LLM-generated), so
# a string-not-contains check is deterministic — no judge needed.
#
# Side-effect-free by construction: the doc scenario names a NONEXISTENT document,
# so a resolved antecedent leads to a clean "not found" (no write), while a
# regressed antecedent still surfaces the "which document" punt this test catches.
# ---------------------------------------------------------------------------


async def converse(client, messages, session_id, auth=None):
    """Send a sequence of messages on ONE shared session_id; return per-turn data.

    Unlike send_canonical_query (unique session per call = single-turn), this
    REUSES session_id, so turn N sees turns 1..N-1 — the multi-turn surface.
    """
    out = []
    for msg in messages:
        kwargs = {"json": {"message": msg, "session_id": session_id}}
        if auth:
            kwargs.update(auth)
        resp = await client.post("/api/v1/intent", **kwargs)
        assert resp.status_code == 200, f"turn HTTP {resp.status_code}: {resp.text[:200]}"
        data = resp.json()
        out.append(
            {"user": msg, "piper": data.get("message", ""), "intent": data.get("intent", {})}
        )
    return out


# Canned antecedent-clarification punts a handler emits when it FAILED to carry
# the entity from a prior turn (services/intent/intent_service.py). Their presence
# in a follow-up response == antecedent resolution regressed.
_DOC_ANTECEDENT_PUNT = "i need to know which document"


class TestCanonicalMultiTurn:
    # #1452: this tier drives the LIVE classifier (LLM calls) — the marker was
    # missing, so keyless sweeps (CI + local enumeration) ran it and failed all
    # of it; 227 of the burn-down backlog's entries were this one omission.
    pytestmark = pytest.mark.llm

    """#1213 P3: deterministic multi-turn antecedent guard (no LLM judge).

    Cheap every-PR regression check for #1122/#1207, complementing the gated
    AAXT golden scenarios. Asserts a follow-up turn does NOT emit a canned
    antecedent-clarification punt (the pre-#1122 failure shape).
    """

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_structured_dispatch_antecedent_no_punt(self, e2e_client, e2e_auth_headers):
        """#1122 structured-dispatch: 'the doc' in turn 2 must resolve to turn 1's
        named document — the handler must NOT fall back to the canned 'which
        document' clarification. Deterministic mirror of the AAXT judge test.
        Uses a nonexistent doc name so a resolved antecedent yields a clean
        not-found (no mutation), not a write."""
        convo = await converse(
            e2e_client,
            [
                "Update the p3-regression-nonexistent-doc-xyz document",
                "Add a paragraph to the doc saying 'P3 antecedent regression marker'",
            ],
            f"canonical-mt-doc-{uuid4().hex[:8]}",
            e2e_auth_headers,
        )
        final = convo[-1]["piper"]
        assert final, "empty final response — harness wiring problem"
        assert _DOC_ANTECEDENT_PUNT not in final.lower(), (
            "#1122 antecedent regression: follow-up emitted the canned "
            f"'{_DOC_ANTECEDENT_PUNT}' punt though turn 1 named the document. "
            f"Response: {final[:300]}"
        )

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_conversation_pronoun_retention(self, e2e_client, e2e_auth_headers):
        """#1207 context-retention: a pronoun follow-up gets a substantive,
        context-aware response — not empty, no error fingerprint, no generic
        non-comprehension punt. Read-only (conversation-shaped, no mutation)."""
        convo = await converse(
            e2e_client,
            [
                "I need to plan a stakeholder presentation for next week",
                "Can you help me structure that?",
            ],
            f"canonical-mt-pron-{uuid4().hex[:8]}",
            e2e_auth_headers,
        )
        final = convo[-1]["piper"]
        assert len(final) > 20, f"follow-up too short ({len(final)} chars): {final!r}"
        low = final.lower()
        for fp in ERROR_FINGERPRINTS:
            assert fp not in low, f"follow-up error fingerprint '{fp}': {final[:200]}"
        for punt in ("i'm not sure what you mean", "please specify."):
            assert punt not in low, (
                f"#1207 context-retention regression: pronoun follow-up punted "
                f"('{punt}') instead of using turn-1 context. Response: {final[:300]}"
            )


# ---------------------------------------------------------------------------
# Tier 1c: Ground-truth assertions (deterministic, every PR) — #1213 P1
#
# The biggest hole the routing/structure tiers miss: a data-bearing query can
# route correctly + return a non-empty, error-free, well-formed response that is
# nonetheless WRONG — stale/empty/fabricated data behind a structurally-fine
# answer. That's where "passes 100% but has wiring bugs" lives (PM 2026-06-12).
#
# This tier seeds a KNOWN ground-truth state and asserts a data-bearing query
# actually reflects it. Deterministic (string match on a unique marker the
# handler echoes verbatim) — NO LLM judge, so it sidesteps the stateless-judge
# problem (#1131: the judge can't verify user data) AND runs every PR for free.
#
# First slice = todos (cleanly user-scoped + seeded through the real service
# write path under the authenticated principal — see seed_ground_truth_todo;
# the e2e_auth_state fixture's user-delete cascade cleans them up). Extending
# to other data types (issues, milestones, calendar) is follow-on P1 work —
# same pattern, new marker.
# ---------------------------------------------------------------------------


async def seed_ground_truth_todo(user_id: str, text: str):
    """#1675: seed the ground-truth todo through the REAL write path
    (TodoManagementService.create_todo — the exact call handle_create_todo
    makes, same session/commit/cache-invalidation behavior) under the
    AUTHENTICATED principal — NOT via a chat turn.

    Why not 'Add a todo: <marker>' over HTTP (the original design): that shape
    has no pre-classifier claim, so the SEED rode the live LLM classifier, and
    the ticket-shaped marker (P1GT-<hex> reads like an issue key) drew
    create_ticket ~1/3 of sampled classifications → 'GitHub isn't connected'
    → no row written → the subsequent list read was HONESTLY empty. That is
    what Run 14 (2026-08-21) recorded as a wrong-empty on both sibling tests
    (#1675): a harness artifact — production was never wrong; the read rail
    (list_todos_query) is pre-classifier-claimed and owner-scoped correctly.
    A ground-truth premise must be deterministic; the LLM-routed seed wasn't.
    """
    from services.todo.todo_management_service import TodoManagementService

    todo = await TodoManagementService().create_todo(user_id=UUID(user_id), text=text)
    assert todo is not None and todo.id, "#1675: ground-truth seed failed to persist"
    return todo


class TestCanonicalGroundTruth:
    # #1452: this tier drives the LIVE classifier (LLM calls) — the marker was
    # missing, so keyless sweeps (CI + local enumeration) ran it and failed all
    # of it; 227 of the burn-down backlog's entries were this one omission.
    pytestmark = pytest.mark.llm

    """#1213 P1: seed known state, assert a data-bearing query reflects it.

    Catches stale/empty/fabricated-data wiring bugs that route + structure tiers
    pass. Deterministic (marker echo), no judge cost.
    """

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_show_todos_reflects_seeded_todo(
        self, e2e_client, e2e_auth_headers, e2e_auth_state
    ):
        """Seed a uniquely-marked todo (real service write path, authenticated
        principal — #1675), then assert 'show my todos' returns it — i.e. real
        user data flows through, not a generic/empty/stale answer. The marker is
        echoed verbatim by the handler (verified live), so a plain substring
        assertion is robust + judge-free.

        #1675: the seed used to be a chat turn ('Add a todo: <marker>') — an
        LLM-routed shape that stochastically drew create_ticket, voiding the
        premise (see seed_ground_truth_todo). Chat-based add-todo ROUTING is
        real product surface but is not this tier's subject; it needs its own
        deterministic claim or routing-tier coverage (discovered-work issue
        filed from #1675)."""
        marker = f"P1GT-{uuid4().hex[:10]}"

        await seed_ground_truth_todo(e2e_auth_state["user_id"], marker)

        show = await send_canonical_query(
            e2e_client, "Show my todos", "p1gt-show", e2e_auth_headers
        )
        msg = show.get("message") or ""
        assert marker in msg, (
            f"#1213 P1 ground-truth FAIL: seeded todo {marker!r} not reflected in "
            f"'show my todos' — the data didn't flow through (wiring bug the routing/"
            f"structure tiers would miss). Response: {msg[:300]}"
        )
        low = msg.lower()
        for fp in ERROR_FINGERPRINTS:
            assert fp not in low, f"show-todos error fingerprint '{fp}': {msg[:200]}"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_completed_todo_drops_from_active_list(
        self, e2e_client, e2e_auth_headers, e2e_auth_state
    ):
        """#1213 P1/P5 — ground-truth LIFECYCLE: seed a marked todo (real
        service write path, authenticated principal — #1675), confirm it's
        listed, complete it, then assert 'show my todos' no longer lists it as
        active. Catches a 'complete didn't actually complete' wiring bug — where
        the action routes + responds fine but the state change never lands. The
        marker is unique, so other accumulated todos don't affect the assertion.
        The complete + show turns stay REAL chat turns — both shapes are
        pre-classifier-claimed (deterministic), unlike the retired add turn."""
        marker = f"P1GT-life-{uuid4().hex[:10]}"

        await seed_ground_truth_todo(e2e_auth_state["user_id"], marker)
        show1 = await send_canonical_query(
            e2e_client, "Show my todos", "p1gt-life-show1", e2e_auth_headers
        )
        assert marker in (show1.get("message") or ""), (
            f"#1213 P1: seeded todo {marker!r} not listed before completion — "
            f"can't test the lifecycle. Response: {(show1.get('message') or '')[:200]}"
        )

        comp = await send_canonical_query(
            e2e_client, f"Complete the {marker} todo", "p1gt-life-comp", e2e_auth_headers
        )
        comp_action = (comp.get("intent") or {}).get("action") or ""
        assert "complete" in comp_action or "done" in comp_action, (
            f"#1213 P1: complete-todo did not route to a complete action "
            f"(got {comp_action!r}); response: {(comp.get('message') or '')[:200]}"
        )

        show2 = await send_canonical_query(
            e2e_client, "Show my todos", "p1gt-life-show2", e2e_auth_headers
        )
        msg2 = show2.get("message") or ""
        assert marker not in msg2, (
            f"#1213 P1 lifecycle FAIL: completed todo {marker!r} still shows as "
            f"active — the complete action's EFFECT didn't flow through (state "
            f"change lost behind a fine-looking response). Response: {msg2[:300]}"
        )


# ---------------------------------------------------------------------------
# Tier 1d: External-data ground-truth via mock-adapter (deterministic, every PR)
#          — #1213 P1 follow-on (#1221)
#
# External-data queries (calendar, GitHub) can't be seeded like todos — the data
# lives in real services. This tier patches the integration router's async fetch
# method to return KNOWN data, then asserts the query response reflects it (and
# degrades honestly on empty). In-process patching works because the suite's
# ASGITransport runs the handler in the same process + event loop, so a
# patch.object() around the request is visible to the handler. Plan:
# docs/internal/testing/mock-adapter-groundtruth-harness-plan.md
#
# First slice: calendar (calendar is freshly connected; #1215). The week handler
# (_handle_week_calendar_query) calls CalendarIntegrationRouter.authenticate()
# then .get_events_in_range(); both are patched.
# ---------------------------------------------------------------------------


class TestCanonicalGroundTruthMocked:
    """#1213 P1 (#1221): external-data ground truth via mocked integration router.

    Mock the calendar router to return known events; assert the response reflects
    them (and an empty result is surfaced honestly, not fabricated). Deterministic,
    no live external calls, no judge.
    """

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_week_calendar_reflects_known_events(self, e2e_client, e2e_auth_headers):
        """Patch the calendar router to return a known event, assert 'what's my
        week look like?' renders it — i.e. external data flows through the
        handler→formatter wiring."""
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        marker = f"MOCK-EVT-{uuid4().hex[:8]}"
        start = (datetime.now(timezone.utc) + timedelta(days=1)).replace(
            hour=15, minute=0, second=0, microsecond=0
        )
        known = [
            {
                "start_time": start.isoformat(),
                "summary": marker,
                "duration_minutes": 30,
                "is_all_day": False,
            }
        ]
        with (
            patch.object(
                CalendarIntegrationRouter, "authenticate", new=AsyncMock(return_value=True)
            ),
            patch.object(
                CalendarIntegrationRouter,
                "get_events_in_range",
                new=AsyncMock(return_value=known),
            ),
        ):
            data = await send_canonical_query(
                e2e_client, "what's my week look like?", "gtmock-cal", e2e_auth_headers
            )
        msg = data.get("message") or ""
        assert marker in msg, (
            f"#1213 P1 mock ground-truth FAIL: known calendar event {marker!r} not "
            f"reflected in the week response — external data didn't flow through. "
            f"Response: {msg[:300]}"
        )

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_week_calendar_empty_is_honest(self, e2e_client, e2e_auth_headers):
        """Patch the calendar router to return NO events, assert the response says
        so honestly (doesn't fabricate a schedule)."""
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        with (
            patch.object(
                CalendarIntegrationRouter, "authenticate", new=AsyncMock(return_value=True)
            ),
            patch.object(
                CalendarIntegrationRouter, "get_events_in_range", new=AsyncMock(return_value=[])
            ),
        ):
            data = await send_canonical_query(
                e2e_client, "what's my week look like?", "gtmock-cal-empty", e2e_auth_headers
            )
        msg = (data.get("message") or "").lower()
        assert "didn't find any events" in msg or "no events" in msg, (
            f"#1213 P1 mock ground-truth: empty calendar not surfaced honestly "
            f"(possible fabrication). Response: {msg[:300]}"
        )

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_week_calendar_degrades_honestly_on_adapter_error(
        self, e2e_client, e2e_auth_headers
    ):
        """Patch the calendar router to RAISE; assert the response degrades to a
        conversational message and NO raw exception/traceback leaks to the user
        (#876). This is the degradation half of the ground-truth contract — an
        adapter failure must surface honestly, not as a raw error or a silent
        fabrication."""
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        boom = "P1GTadapterboommarker"  # raw text that must NOT reach the user
        with (
            patch.object(
                CalendarIntegrationRouter, "authenticate", new=AsyncMock(return_value=True)
            ),
            patch.object(
                CalendarIntegrationRouter,
                "get_events_in_range",
                new=AsyncMock(side_effect=RuntimeError(boom)),
            ),
        ):
            data = await send_canonical_query(
                e2e_client, "what's my week look like?", "gtmock-cal-err", e2e_auth_headers
            )
        msg = data.get("message") or ""
        assert len(msg) > 10, f"degradation response too short/empty: {msg!r}"
        low = msg.lower()
        assert (
            boom.lower() not in low
        ), f"#876 violation: raw exception text leaked to the user. Response: {msg[:200]}"
        for raw in ("traceback", "runtimeerror"):
            assert raw not in low, f"raw error fingerprint '{raw}' leaked: {msg[:200]}"

    # --- GitHub slice (#1221) — same pattern, second integration ------------

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_milestones_reflect_known_data(self, e2e_client, e2e_auth_headers):
        """Patch the GitHub router to return a known milestone, assert the
        milestones query renders it (GitHub external data flows through)."""
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        marker = f"MOCK-MS-{uuid4().hex[:8]}"
        known = [{"title": marker, "due_on": "2026-07-01T00:00:00Z", "open_issues": 3}]
        with patch.object(
            GitHubIntegrationRouter,
            "list_milestones_via_mcp",
            new=AsyncMock(return_value=known),
        ):
            data = await send_canonical_query(
                e2e_client, "What's the next milestone?", "gtmock-ms", e2e_auth_headers
            )
        msg = data.get("message") or ""
        assert marker in msg, (
            f"#1213 P1 mock ground-truth FAIL: known milestone {marker!r} not "
            f"reflected — GitHub data didn't flow through. Response: {msg[:300]}"
        )

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_milestones_empty_is_honest(self, e2e_client, e2e_auth_headers):
        """Patch the GitHub router to return NO milestones, assert the response
        says so honestly (no fabrication)."""
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        with patch.object(
            GitHubIntegrationRouter,
            "list_milestones_via_mcp",
            new=AsyncMock(return_value=[]),
        ):
            data = await send_canonical_query(
                e2e_client, "What's the next milestone?", "gtmock-ms-empty", e2e_auth_headers
            )
        msg = (data.get("message") or "").lower()
        assert "don't have any open milestones" in msg or "no milestones" in msg, (
            f"#1213 P1 mock ground-truth: empty milestones not surfaced honestly. "
            f"Response: {msg[:300]}"
        )
