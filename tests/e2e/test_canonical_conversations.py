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
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

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
    (36, "Create a doc from this conversation", "Documents", "floor", "M2"),
    (37, "Compare these two documents", "Documents", "floor", "M2"),
    (38, "Synthesize these sources into a summary", "Documents", "floor", "M2"),
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
    (44, "Create issues from this meeting's action items", "GitHub Ops", "floor", None),
    (45, "Close completed issues", "GitHub Ops", "floor", None),
    (58, "Update issue #123", "GitHub Ops", "action", None),
    (59, "Comment on issue #456", "GitHub Ops", "canonical", None),
    (60, "Review issue #789", "GitHub Ops", "canonical", None),
    # Slack (5)
    (46, "Any mentions I missed?", "Slack", "floor", "M2"),
    (47, "Summarize #general from yesterday", "Slack", "floor", "M2"),
    (48, "Post this update to the team channel", "Slack", "floor", "M2"),
    (49, "/standup", "Slack", "action", None),
    (50, "/piper help", "Slack", "floor", None),
    # Productivity (3)
    (51, "What's my productivity this week?", "Productivity", "floor", None),
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
    (63, "Upload a file to the knowledge base", "Knowledge", "floor", "M2"),
]

# Error fingerprints that indicate broken responses
ERROR_FINGERPRINTS = [
    "something unexpected happened",
    "internal server error",
    "traceback",
    "exception",
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
            "session_id": f"canonical-e2e-q{query_num}-{uuid4().hex[:8]}",
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
async def e2e_auth_headers(e2e_client):
    """#1165: module-scoped — one shared canonical test user (created + cleaned
    once). Per-query isolation comes from send_canonical_query's unique
    session_id, so the shared app's conversation registry doesn't bleed across
    queries; canonical queries are single-turn so a shared user is fine."""
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
    yield {"cookies": login.cookies}

    # Cleanup (user-scoped, FK order — mirrors conftest)
    async with async_session() as s:
        for stmt in (
            "DELETE FROM todo_items WHERE owner_id = CAST(:uid AS uuid)",
            "DELETE FROM items WHERE list_id IN (SELECT id FROM lists WHERE owner_id = CAST(:uid AS uuid))",
            "DELETE FROM lists WHERE owner_id = CAST(:uid AS uuid)",
            "DELETE FROM projects WHERE owner_id = :uid",
            "DELETE FROM conversations WHERE user_id = :uid",
            "DELETE FROM users WHERE id = :uid",
        ):
            await s.execute(text(stmt), {"uid": user_id})
        await s.commit()
    await engine.dispose()


# ---------------------------------------------------------------------------
# Tier 1: Routing + Structure (deterministic, every PR)
# ---------------------------------------------------------------------------


class TestCanonicalRouting:
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

        assert verdict in ("PASS", "MARGINAL"), (
            f"Q{query_num} ({category}): quality {verdict} (R={scores.get('relevance')} "
            f"C={scores.get('context')} T={scores.get('tone')} = {total}/9). "
            f"Response: {response_text[:150]}"
        )
