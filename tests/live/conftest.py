"""Live-verification fixture family (#1621) — real server, real login, real turns.

WHAT LAYER THIS VERIFIES (m-43 — name the layer):
    This is a REAL-TURN HTTP-LAYER test harness. It starts the actual server
    (`main.py`) as a SEPARATE PROCESS with a scrubbed environment, authenticates
    through the real POST /api/v1/auth/login (bcrypt verify, JWT mint, cookie
    set), and drives turns through the real POST /api/v1/intent over an actual
    TCP socket — the same surface PM's browser talks to. Everything between the
    socket and the database is production code: middleware, auth dependency,
    intent service, handlers, persistence.

WHAT IT DOES NOT VERIFY:
    - Rendered UI. Nothing here proves a template renders, a message displays,
      or the frontend JS parses the response (the #1480 browser half stays
      manual / chrome-driven).
    - LLM-routed turns, unless the server has a real Anthropic credential
      provisioned (KeychainService). The worked example deliberately uses a
      PRE-CLASSIFIED deterministic path (reminder create/clarify) so the
      harness itself never depends on LLM availability. A turn that DOES fall
      to the LLM without a credential comes back as an honest degradation
      response — which the turn driver refuses to treat as a pass.

HOW THIS DIFFERS FROM tests/e2e/ (which this reuses, not duplicates):
    tests/e2e/ boots the FastAPI app IN-PROCESS via ASGI transport — one layer
    below this. It cannot catch: startup-environment poisoning (the inherited
    empty ANTHROPIC_API_KEY, #1258), real socket/port behavior, or anything in
    the gap between "app object works" and "the process you actually launch
    works". This harness runs the process you actually launch.

OPT-IN GATING:
    These tests start a real server and write real rows to the shared dev
    Postgres (5433). They run ONLY when PIPER_LIVE=1 is set; otherwise every
    test in tests/live/ skips with an explanatory message. They are NOT part
    of smoke/CI.

USAGE:
    PIPER_LIVE=1 POSTGRES_PORT=5433 venv/bin/python -m pytest tests/live/ -v \
        -o addopts="--import-mode=importlib"

    Env knobs:
      PIPER_LIVE=1          required — opt-in gate
      PIPER_LIVE_PORT=NNNN  optional — pin the server port (default: pick a
                            free ephemeral port; NEVER touches a dev server
                            already on 8001)
      PIPER_LIVE_LOG=path   optional — server stdout/stderr log destination
                            (default: temp file, path printed on failure)
      PIPER_LIVE_TRANSCRIPT=1  optional — print each turn's real request and
                            response to stdout (run pytest with -s); made for
                            pasting honest evidence into issue closures

HONESTY RULES BUILT IN (the #1621 spec is explicit about these):
    - The server subprocess env is scrubbed of ANTHROPIC_API_KEY /
      ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN / ANTHROPIC_CUSTOM_HEADERS
      (a Claude Code shell exports an EMPTY key that shadows real resolution —
      diagnosed 2026-06-04, #1258).
    - Health-wait failure dumps the server log tail and raises — no silent
      "server probably came up".
    - The turn driver raises LiveTurnError on any degradation-shaped 200
      (error_type present) unless the test explicitly opts in to receiving it.
      A driver that can't measure must exit loudly, never report a fake pass.
    - Cleanup is FK-ordered AND verified by count afterward — the 2026-08-13
      cleanup silently no-oped TWICE before anyone counted; the count IS the
      cleanup's evidence (m-44: "clear" is not a measurement). Verification
      covers the curated cascade AND a generic information_schema sweep of
      every FK that references users(id), so tables the cascade doesn't know
      about fail the fixture loudly instead of leaking rows silently.

Issue: #1621 (discharges the #1597 backlog class)
"""

import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import httpx
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

REPO_ROOT = Path(__file__).resolve().parents[2]

LIVE_ENABLED = os.environ.get("PIPER_LIVE") == "1"

# Env vars a Claude Code shell exports for its own use; inherited by a child
# server they shadow real key resolution and every LLM call fails with a fake
# "connection error" (#1258). Always scrubbed from the server subprocess.
_POISON_ENV_VARS = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_CUSTOM_HEADERS",
)

# Degradation shapes POST /api/v1/intent returns with HTTP 200 (#875 design:
# business errors are conversational). A live driver must not count these as
# a processed turn.
_DEGRADED_ERROR_TYPES = {
    "service_unavailable",
    "anonymous_key_required",
    "session_expired",
}

HEALTH_WAIT_SECONDS = 120


def _db_url() -> str:
    """Same env resolution as services/database/session_factory.py."""
    user = os.getenv("POSTGRES_USER", "piper")
    password = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    database = os.getenv("POSTGRES_DB", "piper_morgan")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


def _pick_port() -> int:
    """Choose the server port.

    PIPER_LIVE_PORT pins it (and a busy pinned port is a loud failure, never a
    silent fallback). Otherwise pick a free ephemeral port — this harness never
    claims 8001, so an already-running dev server is never disturbed.
    """
    pinned = os.environ.get("PIPER_LIVE_PORT")
    if pinned:
        port = int(pinned)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                raise RuntimeError(
                    f"PIPER_LIVE_PORT={port} is already in use. Refusing to "
                    "reuse someone else's server (results would verify the "
                    "wrong code) or to kill it. Pick another port or unset "
                    "PIPER_LIVE_PORT."
                )
        return port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class LiveTurnError(AssertionError):
    """A live turn could not be measured (HTTP failure or degradation-shaped
    response). Deliberately an AssertionError subclass: it must FAIL the test,
    never read as an environmental skip."""


@dataclass
class LiveServer:
    base_url: str
    port: int
    log_path: Path
    proc: subprocess.Popen


@dataclass
class LiveUser:
    user_id: str
    username: str
    password: str
    # Every session_id driven for this user. POST /api/v1/intent auto-creates
    # a conversation whose id IS the session_id (#731), and conversation_turns
    # carry no FK — cleanup verification counts these ids explicitly.
    session_ids: List[str] = field(default_factory=list)


class TurnDriver:
    """Drives real chat turns for one logged-in user against the live server.

    Holds an httpx.Client whose cookie jar carries the real auth_token cookie
    from POST /api/v1/auth/login — turns authenticate exactly the way the
    browser does.
    """

    def __init__(self, client: httpx.Client, user: LiveUser):
        self._client = client
        self.user = user

    def new_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.user.session_ids.append(session_id)
        return session_id

    def turn(
        self,
        message: str,
        session_id: Optional[str] = None,
        allow_degraded: bool = False,
        timeout: float = 60.0,
    ) -> dict:
        """POST one message to /api/v1/intent; return the parsed response body.

        Raises LiveTurnError (test failure, not skip) if the HTTP call fails
        or the body is degradation-shaped — unless allow_degraded=True, for
        tests whose SUBJECT is the degradation copy itself.
        """
        if session_id is None:
            session_id = self.user.session_ids[-1] if self.user.session_ids else self.new_session()
        transcript = os.environ.get("PIPER_LIVE_TRANSCRIPT") == "1"
        if transcript:
            print(
                f"\n>>> POST {self._client.base_url}/api/v1/intent "
                f"(user={self.user.username}, session={session_id})\n"
                f">>> {{'message': {message!r}, 'session_id': {session_id!r}}}"
            )
        resp = self._client.post(
            "/api/v1/intent",
            json={"message": message, "session_id": session_id},
            timeout=timeout,
        )
        if transcript:
            print(f"<<< HTTP {resp.status_code}\n<<< {resp.text}")
        if resp.status_code != 200:
            raise LiveTurnError(
                f"POST /api/v1/intent returned HTTP {resp.status_code} "
                f"(session={session_id}): {resp.text[:500]}"
            )
        body = resp.json()
        error_type = body.get("error_type")
        if error_type in _DEGRADED_ERROR_TYPES and not allow_degraded:
            raise LiveTurnError(
                "Turn came back degradation-shaped, not processed "
                f"(error_type={error_type!r}): {body.get('message', '')[:300]!r}. "
                "This is a real response from the real server — but it means "
                "the turn was NOT handled, so it cannot count as a pass."
            )
        return body

    def get(self, path: str, **kwargs) -> httpx.Response:
        """Authenticated GET against the live server (e.g. /api/v1/auth/me)."""
        return self._client.get(path, **kwargs)


def _tail(path: Path, lines: int = 40) -> str:
    try:
        content = path.read_text(errors="replace").splitlines()
        return "\n".join(content[-lines:])
    except OSError as e:
        return f"<could not read server log {path}: {e}>"


@pytest.fixture(scope="session")
def live_server():
    """Start the REAL server (main.py) as a subprocess, env-stripped, on a
    port of its own; health-wait; guaranteed teardown.

    Session-scoped: one server boot serves every test in the run (boot is
    tens of seconds — services init, DB, vector store).
    """
    if not LIVE_ENABLED:
        pytest.skip(
            "Live-verification tests are opt-in: set PIPER_LIVE=1 "
            "(starts a real server, writes to the shared dev Postgres)."
        )

    port = _pick_port()
    log_path = Path(
        os.environ.get("PIPER_LIVE_LOG")
        or tempfile.mkstemp(prefix=f"piper-live-{port}-", suffix=".log")[1]
    )

    env = dict(os.environ)
    for var in _POISON_ENV_VARS:
        env.pop(var, None)
    env.setdefault("POSTGRES_PORT", "5433")
    env["PIPER_PORT"] = str(port)

    log_handle = open(log_path, "w")
    proc = subprocess.Popen(
        [sys.executable, "main.py", "--no-browser"],
        cwd=REPO_ROOT,
        env=env,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        start_new_session=True,  # own process group → teardown catches children
    )

    base_url = f"http://127.0.0.1:{port}"
    deadline = time.monotonic() + HEALTH_WAIT_SECONDS
    ready = False
    try:
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                raise RuntimeError(
                    f"Server process exited during startup (code {proc.returncode}). "
                    f"Log tail ({log_path}):\n{_tail(log_path)}"
                )
            try:
                resp = httpx.get(f"{base_url}/health", timeout=2.0)
                if resp.status_code == 200:
                    ready = True
                    break
            except httpx.HTTPError:
                pass
            time.sleep(1.0)
        if not ready:
            raise RuntimeError(
                f"Server did not answer /health within {HEALTH_WAIT_SECONDS}s "
                f"on {base_url}. Log tail ({log_path}):\n{_tail(log_path)}"
            )
        yield LiveServer(base_url=base_url, port=port, log_path=log_path, proc=proc)
    finally:
        # Teardown: nothing left running, whatever happened above.
        if proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait(timeout=10)
        log_handle.close()


@pytest.fixture
async def live_db_session():
    """Direct DB session for provisioning/cleanup/assertions.

    Same database the live server uses (env-resolved, port 5433 default).
    Commits are real — the server's separate connection must see them.
    """
    engine = create_async_engine(_db_url(), echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


async def _fk_leftovers(session, user_id: str) -> List[str]:
    """Count rows still referencing this user, m-44-honestly.

    Two sweeps, because the schema has two kinds of user references:
    1. Every DECLARED FK to users(id), discovered live from
       information_schema — so a table added after this file was written
       fails loudly here instead of leaking rows silently.
    2. The FK-LESS references the schema is known to carry (conversations
       .user_id is varchar with no constraint — the #1603-class split found
       2026-08-13), which no catalog sweep can discover.
    Returns human-readable "table.column: N rows" lines; empty means clean.
    """
    leftovers: List[str] = []

    fk_pairs = (
        await session.execute(
            text(
                """
                SELECT tc.table_name, kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                 AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage ccu
                  ON tc.constraint_name = ccu.constraint_name
                 AND tc.table_schema = ccu.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND ccu.table_name = 'users'
                  AND ccu.column_name = 'id'
                  AND tc.table_schema = 'public'
                """
            )
        )
    ).fetchall()

    for table, column in fk_pairs:
        count = (
            await session.execute(
                # ::text comparison works for uuid AND varchar columns; the
                # canonical lowercase uuid string matches both.
                text(f'SELECT COUNT(*) FROM "{table}" WHERE "{column}"::text = :uid'),  # noqa: S608
                {"uid": user_id},
            )
        ).scalar()
        if count:
            leftovers.append(f"{table}.{column}: {count} rows (declared FK)")

    # FK-less references (not discoverable from the catalog):
    count = (
        await session.execute(
            text(
                "SELECT COUNT(*) FROM conversations "
                "WHERE user_id = :uid OR owner_id::text = :uid"
            ),
            {"uid": user_id},
        )
    ).scalar()
    if count:
        leftovers.append(f"conversations.user_id/owner_id: {count} rows (FK-less)")

    return leftovers


async def _session_leftovers(session, session_ids: List[str]) -> List[str]:
    """conversation_turns / conversation_links carry no FK to users; count them
    by the session ids this run actually drove (conversation id == session_id,
    #731 auto-create)."""
    if not session_ids:
        return []
    leftovers = []
    for table in ("conversation_turns", "conversation_links"):
        count = (
            await session.execute(
                text(f'SELECT COUNT(*) FROM "{table}" WHERE conversation_id = ANY(:ids)'),  # noqa: S608
                {"ids": session_ids},
            )
        ).scalar()
        if count:
            leftovers.append(f"{table}: {count} rows for this run's session ids (FK-less)")
    return leftovers


@pytest.fixture
async def live_user(live_server, live_db_session):
    """A throwaway user with a REAL password hash (PasswordService bcrypt),
    created directly in the DB; FK-ordered cleanup VERIFIED BY COUNT after.

    Yields a LiveUser. Credentials are generated, never guessed, never reused:
    no secret is needed to run this harness.
    """
    from services.auth.password_service import PasswordService

    user_id = str(uuid.uuid4())
    username = f"live_verify_{user_id[:8]}"
    email = f"{username}@live-verify.local"
    password = f"live-{uuid.uuid4().hex[:16]}"

    password_hash = PasswordService().hash_password(password)
    await live_db_session.execute(
        text(
            """
            INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                               created_at, updated_at, role, is_alpha, setup_complete)
            VALUES (CAST(:id AS uuid), :username, :email, :password_hash, true, true,
                    :now, :now, 'user', true, true)
            """
        ),
        {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "now": datetime.now(timezone.utc),
        },
    )
    await live_db_session.commit()

    user = LiveUser(user_id=user_id, username=username, password=password)
    try:
        yield user
    finally:
        # FK-ordered cascade (curated, shared with the e2e layer)...
        from tests.conftest import delete_test_user_fully

        await delete_test_user_fully(live_db_session, user_id)
        # conversation_turns/links for this run's sessions are covered by the
        # cascade's conversations subquery only BEFORE conversations delete;
        # sweep by recorded session ids for anything the cascade ordering missed.
        for table in ("conversation_turns", "conversation_links"):
            if user.session_ids:
                await live_db_session.execute(
                    text(f'DELETE FROM "{table}" WHERE conversation_id = ANY(:ids)'),  # noqa: S608
                    {"ids": user.session_ids},
                )
        await live_db_session.commit()

        # ...then the part that makes the cleanup TRUE rather than claimed:
        # count what's left. The 08-13 cleanup printed "cleaned" twice while
        # deleting nothing; a count is the only exit condition honored here.
        remaining_user = (
            await live_db_session.execute(
                text("SELECT COUNT(*) FROM users WHERE id = CAST(:uid AS uuid)"),
                {"uid": user_id},
            )
        ).scalar()
        leftovers = await _fk_leftovers(live_db_session, user_id)
        leftovers += await _session_leftovers(live_db_session, user.session_ids)
        if remaining_user:
            leftovers.append(f"users.id: {remaining_user} row (the user itself)")
        if leftovers:
            raise RuntimeError(
                f"Cleanup VERIFICATION FAILED for throwaway user {username} "
                f"({user_id}) — rows remain:\n  " + "\n  ".join(leftovers)
            )


@pytest.fixture
async def turn_driver(live_server, live_user):
    """Log the throwaway user in through the REAL login endpoint and yield a
    TurnDriver whose cookie jar carries the real auth cookies."""
    client = httpx.Client(base_url=live_server.base_url, timeout=30.0)
    try:
        resp = client.post(
            "/api/v1/auth/login",
            data={"username": live_user.username, "password": live_user.password},
        )
        assert resp.status_code == 200, (
            f"Programmatic login failed (HTTP {resp.status_code}): {resp.text[:500]}"
        )
        body = resp.json()
        assert body.get("token"), "Login returned 200 but no token in body"
        assert client.cookies.get("auth_token"), (
            "Login returned 200 but set no auth_token cookie — cookie-auth "
            "turns would silently run anonymous (the layer this harness exists "
            "to verify)"
        )
        yield TurnDriver(client, live_user)
    finally:
        client.close()
