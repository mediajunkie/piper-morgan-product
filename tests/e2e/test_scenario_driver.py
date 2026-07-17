"""
E2E: Multi-turn + multi-tenant scenario driver.

The dynamic complement to the multi-tenancy audit (#1419) and the automated
answer to PM's "this feels not ready for human testing yet — plumb this build
out thoroughly." The canonical suite (`test_canonical_conversations.py`, #928)
is single-turn / single-user; this driver adds the two things a real tester
exercises that canonical does not:

  1. MULTI-TURN conversations on a STABLE session — the onboarding flow PM ran
     by hand (greeting -> "how do I address you?" -> "connect my github" -> ...),
     with a per-turn assertion for each bug that flow surfaced.
  2. MULTI-USER isolation — two users in one app, asserting user B never sees
     user A's data (the runtime check for the owner-scoping the audit inventoried).

Each turn's assertions are pinned to a filed issue so this file is a living
regression harness: when a fix lands the assertion goes green and stays green.

Regression targets encoded here:
  - #1414  classification-failure must surface an honest error, never the bare
           "something unexpected happened" (the provider incident's mask)
  - #1416  the greeting must ANSWER the user's question, not swallow it
  - #1417  "connect my github" must not be falsely declined as un-built
  - #1421  a user with no project must not inherit another tenant's default project

Run modes:
  - pytest (CI regression):   pytest tests/e2e/test_scenario_driver.py -v
  - ad-hoc "plumb it now":    python tests/e2e/test_scenario_driver.py
    (boots the app in-process, runs every scenario, prints a pass/fail report,
     exits non-zero on any failure)

Requirements (same as the canonical suite):
  - PostgreSQL on port 5433, migrations current
  - A real LLM API key loadable from .env (strip inherited empty ANTHROPIC_* vars
    per the CLAUDE.md gotcha before invoking the __main__ runner)

Issue: #1419 (multi-tenancy epic — dynamic verification workstream)
"""

from __future__ import annotations

import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Make the project root importable when invoked directly (python tests/e2e/...).
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional
from uuid import uuid4

import httpx
import pytest
import pytest_asyncio
from httpx import ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


# ---------------------------------------------------------------------------
# Assertion vocabulary — fingerprints, pinned to the bug each one guards.
# ---------------------------------------------------------------------------

# Generic hard-failure phrasings (a superset check; honest limitations excluded
# on purpose — "I couldn't find any X" is honest, not a failure). Mirrors the
# canonical suite's ERROR_FINGERPRINTS so the two suites agree on what "broken"
# looks like.
ERROR_FINGERPRINTS = [
    "something unexpected happened",
    "something went wrong",
    "an error occurred",
    "unexpected error",
    "internal server error",
    "internal error",
    "service unavailable",
    "failed to process",
    "unable to complete your request",
    "traceback",
]

# #1417 — the unwired-write generic decline. If "connect my github" trips these,
# the tester is told a real capability is "still on the way."
FALSE_DECLINE_FINGERPRINTS = [
    "still on the way",
    "can't do that from chat yet",
    # ("make the change directly in the relevant tool" removed 2026-07-16 —
    # the #1426 copy fix retired that misdirecting sentence; the two phrases
    # above still identify the generic decline until #1417's routing fix.)
]


def _text(resp: dict) -> str:
    return (resp.get("message") or "").lower()


def no_error_fingerprint(resp: dict) -> bool:
    t = _text(resp)
    return not any(f in t for f in ERROR_FINGERPRINTS)


def no_false_decline(resp: dict) -> bool:
    t = _text(resp)
    return not any(f in t for f in FALSE_DECLINE_FINGERPRINTS)


def nonempty(resp: dict) -> bool:
    return len((resp.get("message") or "").strip()) > 10


def answers_how_to_address(resp: dict) -> bool:
    """#1416: the greeting must engage 'how do I address you?', not just say hello.

    A response that answers the question names what to call the assistant — its
    name, or an explicit invitation to name it. The weak greeting that shipped
    ("I'm here and ready. Hello!") contains none of these; a real answer does.
    """
    t = _text(resp)
    return any(cue in t for cue in ("piper", "call me", "address me", "my name", "you can call"))


# ---------------------------------------------------------------------------
# Scenario abstraction
# ---------------------------------------------------------------------------


@dataclass
class Assertion:
    name: str  # e.g. "#1416 greeting answers the question"
    check: Callable[[dict], bool]
    hint: str


@dataclass
class Turn:
    message: str
    asserts: list[Assertion] = field(default_factory=list)


@dataclass
class Scenario:
    name: str
    turns: list[Turn]


@dataclass
class TurnResult:
    turn_index: int
    message: str
    response_text: str
    failures: list[str]  # assertion names that failed (empty == pass)
    http_ok: bool


# The onboarding flow PM ran by hand, turn for turn. Each turn carries the
# assertion for the bug it surfaced.
FRESH_TESTER_ONBOARDING = Scenario(
    name="fresh_tester_onboarding",
    turns=[
        Turn(
            "Hi, I just got access to this and am excited to try it. How do I address you?",
            asserts=[
                Assertion("nonempty", nonempty, "greeting returned <10 chars"),
                Assertion("no_error", no_error_fingerprint, "greeting turn hit an error fingerprint"),
                Assertion(
                    "#1416 answers 'how do I address you?'",
                    answers_how_to_address,
                    "greeting ignored the question (weak 'hello, ready' with no name / no invitation to name)",
                ),
            ],
        ),
        Turn(
            "can we connect my github?",
            asserts=[
                Assertion("nonempty", nonempty, "connect-github turn returned <10 chars"),
                Assertion(
                    "#1417 not falsely declined",
                    no_false_decline,
                    "'connect my github' met the unwired-write generic decline ('still on the way' / 'use the relevant tool')",
                ),
            ],
        ),
        Turn(
            "What can you help me with?",
            asserts=[
                Assertion("nonempty", nonempty, "capability turn returned <10 chars"),
                Assertion(
                    "#1414 no bare failure on an LLM turn",
                    no_error_fingerprint,
                    "an LLM-backed turn returned the bare 'something unexpected happened' (the provider-incident mask)",
                ),
            ],
        ),
    ],
)

ALL_SCENARIOS = [FRESH_TESTER_ONBOARDING]


# ---------------------------------------------------------------------------
# Driver core — reusable by both the pytest tests and the __main__ runner.
# ---------------------------------------------------------------------------


async def drive_scenario(client, auth: dict, scenario: Scenario) -> list[TurnResult]:
    """Run every turn of a scenario on ONE stable session; collect per-turn results.

    Stable session_id (opposite of the canonical suite's per-query-unique id) so
    multi-turn context persists exactly as it does for a real tester.
    """
    session_id = str(uuid4())  # faithful client: browsers send a UUID (crypto.randomUUID())
    results: list[TurnResult] = []
    for i, turn in enumerate(scenario.turns):
        kwargs = {"json": {"message": turn.message, "session_id": session_id}}
        kwargs.update(auth)
        resp = await client.post("/api/v1/intent", **kwargs)
        http_ok = resp.status_code == 200
        data = resp.json() if http_ok else {"message": f"HTTP {resp.status_code}: {resp.text[:200]}"}
        failures = [a.name for a in turn.asserts if not _safe_check(a, data)]
        results.append(
            TurnResult(
                turn_index=i,
                message=turn.message,
                response_text=(data.get("message") or "")[:400],
                failures=failures,
                http_ok=http_ok,
            )
        )
    return results


def _safe_check(assertion: Assertion, data: dict) -> bool:
    try:
        return assertion.check(data)
    except Exception:
        return False


# ---------------------------------------------------------------------------
# User factory (mirrors the canonical suite fixture; FK-ordered cleanup).
# ---------------------------------------------------------------------------


@asynccontextmanager
async def _make_user(client, *, seed_default_project: Optional[str] = None):
    """Create a user, log in, yield (user_id, auth, username). Cleans up on exit.

    seed_default_project: if set, insert a project owned by this user with
    is_default=true and this (distinctive) name — used to bait the #1421
    get_default_project cross-tenant leak.
    """
    from services.auth.password_service import PasswordService

    user_id = str(uuid4())
    username = f"scen_{user_id[:8]}"
    password = "testpass123"
    password_hash = PasswordService().hash_password(password)

    engine = create_async_engine(_DB_URL, echo=False)
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
        if seed_default_project:
            await s.execute(
                text(
                    "INSERT INTO projects (id, name, description, owner_id, is_default, "
                    "is_archived, created_at, updated_at) "
                    "VALUES (:pid, :name, :desc, :oid, true, false, :now, :now)"
                ),
                {
                    "pid": str(uuid4()),
                    "name": seed_default_project,
                    "desc": "seeded to bait cross-tenant default-project leak (#1421)",
                    "oid": user_id,
                    "now": datetime.now(timezone.utc),
                },
            )
        await s.commit()

    login = await client.post(
        "/api/v1/auth/login", data={"username": username, "password": password}
    )
    assert login.status_code == 200, f"login failed for {username}: {login.text}"

    try:
        yield user_id, {"cookies": login.cookies}, username
    finally:
        # FK-safe teardown: delete every user-owned row before the user. The app
        # touches many owner-scoped tables across a multi-turn session
        # (personalization_contexts, personality_profiles, learned_patterns,
        # knowledge_*, user_trust_profiles, audit_logs, ...), so a minimal
        # conversations+projects cleanup FK-crashes. Children before parents.
        async with async_session() as s:
            for stmt in (
                "DELETE FROM todo_items WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM list_items WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM list_memberships WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM lists WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM knowledge_edges WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM knowledge_nodes WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM project_integrations WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM projects WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM connector_bindings WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM connector_configs WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM documents WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM repositories WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM uploaded_files WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM feedback WHERE owner_id = CAST(:uid AS uuid) OR user_id = CAST(:uid AS uuid)",
                "DELETE FROM personality_profiles WHERE owner_id = CAST(:uid AS uuid) OR user_id = CAST(:uid AS uuid)",
                "DELETE FROM personalization_contexts WHERE owner_id = CAST(:uid AS uuid)",
                "DELETE FROM learned_patterns WHERE user_id = CAST(:uid AS uuid)",
                "DELETE FROM learning_settings WHERE user_id = CAST(:uid AS uuid)",
                "DELETE FROM user_api_keys WHERE user_id = CAST(:uid AS uuid)",
                "DELETE FROM user_trust_profiles WHERE user_id = CAST(:uid AS uuid)",
                "DELETE FROM audit_logs WHERE user_id = CAST(:uid AS uuid)",
                "DELETE FROM password_reset_tokens WHERE user_id = CAST(:uid AS uuid)",
                "DELETE FROM token_blacklist WHERE user_id = CAST(:uid AS uuid)",
                "DELETE FROM conversations WHERE user_id = :uid",
                "DELETE FROM users WHERE id = :uid",
            ):
                await s.execute(text(stmt), {"uid": user_id})
            await s.commit()
        await engine.dispose()


# ---------------------------------------------------------------------------
# pytest fixtures — module-scoped app boot (boot once; see #1165 rationale in
# the canonical suite).
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture(scope="module")
async def app_client():
    from web.app import app

    @asynccontextmanager
    async def _lifespan():
        async with app.router.lifespan_context(app):
            yield

    async with _lifespan():
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


# ---------------------------------------------------------------------------
# Tier 1: multi-turn onboarding (the flow PM ran by hand)
# ---------------------------------------------------------------------------


@pytest.mark.xfail(
    reason="#1416 (weak greeting) + #1417 (github false-decline) are OPEN. This is a "
    "live regression harness: it xfails today and will xPASS the moment both land — "
    "flip to strict=True (a hard gate) in that same fix commit.",
    strict=False,
)
@pytest.mark.asyncio
@pytest.mark.parametrize("scenario", ALL_SCENARIOS, ids=lambda s: s.name)
async def test_multi_turn_scenario(app_client, scenario):
    async with _make_user(app_client) as (_uid, auth, _uname):
        results = await drive_scenario(app_client, auth, scenario)

    lines = []
    any_failed = False
    for r in results:
        status = "PASS" if not r.failures else "FAIL"
        if r.failures:
            any_failed = True
        lines.append(
            f"  [{status}] turn {r.turn_index}: {r.message[:60]!r}"
            + (f"  -> failed: {r.failures}" if r.failures else "")
            + f"\n         resp: {r.response_text[:160]!r}"
        )
    report = f"\nScenario '{scenario.name}':\n" + "\n".join(lines)
    assert not any_failed, report


# ---------------------------------------------------------------------------
# Tier 2: multi-tenant isolation — two users, one app.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_no_cross_tenant_default_project_leak(app_client):
    """#1421: user B (no project) must not inherit user A's is_default project.

    User A owns an is_default project with a distinctive name. User B — who has
    no project — asks project-context questions. B's responses must never contain
    A's project name. (Best-effort: floor may not echo a bound project name even
    when the binding is wrong, so a PASS means 'not leaked via chat', not 'fully
    isolated' — the repo-level unit test in #1421 is the authoritative check. A
    FAIL here is a confirmed live leak.)
    """
    bait = f"ZebraAlphaSecret-{uuid4().hex[:6]}"
    async with _make_user(app_client, seed_default_project=bait) as (_a, _auth_a, _ua):
        async with _make_user(app_client) as (_b, auth_b, _ub):
            probes = [
                "What projects am I working on?",
                "What's my current project?",
                "What should I focus on today?",
            ]
            leaks = []
            for msg in probes:
                kwargs = {"json": {"message": msg, "session_id": str(uuid4())}}
                kwargs.update(auth_b)
                resp = await app_client.post("/api/v1/intent", **kwargs)
                body = (resp.json().get("message") or "") if resp.status_code == 200 else resp.text
                if bait.lower() in body.lower():
                    leaks.append((msg, body[:200]))

    assert not leaks, (
        f"#1421 CROSS-TENANT LEAK: user B saw user A's default project {bait!r}:\n"
        + "\n".join(f"  probe {m!r} -> {b!r}" for m, b in leaks)
    )


# ---------------------------------------------------------------------------
# __main__ runner — "plumb it now" against the in-process app.
# ---------------------------------------------------------------------------


async def _run_all_and_report() -> int:
    from web.app import app

    @asynccontextmanager
    async def _lifespan():
        async with app.router.lifespan_context(app):
            yield

    failures = 0
    async with _lifespan():
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            print("\n" + "=" * 72)
            print("SCENARIO DRIVER — multi-turn onboarding")
            print("=" * 72)
            async with _make_user(client) as (_uid, auth, uname):
                for scenario in ALL_SCENARIOS:
                    results = await drive_scenario(client, auth, scenario)
                    print(f"\n[{scenario.name}]  (user {uname})")
                    for r in results:
                        ok = not r.failures and r.http_ok
                        mark = "  OK " if ok else "FAIL"
                        print(f"  {mark}  turn {r.turn_index}: {r.message[:64]!r}")
                        print(f"          resp: {r.response_text[:150]!r}")
                        for f in r.failures:
                            print(f"          !! {f}")
                        failures += len(r.failures)

            print("\n" + "=" * 72)
            print("SCENARIO DRIVER — multi-tenant isolation (#1421)")
            print("=" * 72)
            bait = f"ZebraAlphaSecret-{uuid4().hex[:6]}"
            async with _make_user(client, seed_default_project=bait) as (_a, _auth_a, ua):
                async with _make_user(client) as (_b, auth_b, ub):
                    print(f"  user A ({ua}) owns is_default project {bait!r}; user B ({ub}) has none")
                    leaked = False
                    for msg in ("What projects am I working on?", "What's my current project?"):
                        kwargs = {"json": {"message": msg, "session_id": str(uuid4())}}
                        kwargs.update(auth_b)
                        resp = await client.post("/api/v1/intent", **kwargs)
                        body = (resp.json().get("message") or "") if resp.status_code == 200 else resp.text
                        hit = bait.lower() in body.lower()
                        leaked = leaked or hit
                        print(f"  {'LEAK' if hit else ' ok '}  B probe {msg[:48]!r}")
                        print(f"          resp: {body[:150]!r}")
                    if leaked:
                        failures += 1

    print("\n" + "=" * 72)
    print(f"RESULT: {'FAIL' if failures else 'PASS'} — {failures} assertion failure(s)")
    print("=" * 72)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_run_all_and_report()))
