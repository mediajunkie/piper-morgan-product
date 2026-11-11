#!/usr/bin/env python
"""#2232: the local served fault run.

Starts ``main.py`` from the current tree against a SCRATCH database on the local
Postgres (5433), points one upstream at a failing stub, sends the HTTP request a
partner's browser would send, and prints the reply with the evidence that the
failure branch was the one reached. For the rows whose failure cannot be forced
on alpha (Arch, 2026-10-30: never a fault switch in served code, never a forced
upstream failure on the host partners use).

No served code is changed by this script and nothing here is imported by the app.

Rows (``--rows``, comma-separated; default: all that need no LLM key):
  2125-store   wizard validate-key on a server whose ENCRYPTION_MASTER_KEY is the
               wrong length -> "The server can't store keys right now..."
  2125-check   wizard validate-key while the provider cannot be reached (the
               server's HTTPS proxy is a stub answering 502 to CONNECT)
               -> "The key check couldn't run just now..."
  2154         GET the four preferences routes while the app's database role is refused
               SELECT on connector_configs -> 503 with CXO's line

Arch's conditions for the database row (decisions.log 2026-11-10 19:02):
  1. the app connects as a NON-superuser login role (the compose role ``piper``
     is a superuser and ignores grants); the denial is PROVED with a probe query
     as that role before the request is sent, or the row is reported NOT RUN;
  2. the evidence names the exception (InsufficientPrivilege) and the branch
     reached (the server's own log line).

Usage (repo root, local Postgres up on 5433):
    venv/bin/python scripts/served_fault_run.py
    venv/bin/python scripts/served_fault_run.py --rows 2154 --keep-logs /tmp/x

Concept: docs/internal/operations/canonical-ops-recipes.md (recipe 9)
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import secrets
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import httpx

ROOT = Path(__file__).resolve().parent.parent
PG_CONTAINER = "piper-postgres"
PG_SUPERUSER = "piper"
PG_PORT = os.environ.get("POSTGRES_PORT", "5433")
SCRATCH_DB = "piper_fault_run"
APP_ROLE = "piper_fault_app"
STRIPPED = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_CUSTOM_HEADERS",
    "OPENAI_API_KEY",
    "DATABASE_URL",
    "ALEMBIC_DATABASE_URL",
    "ENCRYPTION_MASTER_KEY",
    "ENCRYPTION_SCOPED_SUBKEYS",
    "HTTPS_PROXY",
    "https_proxy",
    "HTTP_PROXY",
    "http_proxy",
    "ALL_PROXY",
    "all_proxy",
    "FLY_APP_NAME",
)


class NotRun(Exception):
    """A row whose precondition could not be proved. Reported, never passed."""


# ── Postgres (scratch database only) ─────────────────────────────────────────


def _psql(
    sql: str, *, db: str = "postgres", role: str = PG_SUPERUSER
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "docker",
            "exec",
            PG_CONTAINER,
            "psql",
            "-v",
            "ON_ERROR_STOP=1",
            "-U",
            role,
            "-d",
            db,
            "-Atc",
            sql,
        ],
        capture_output=True,
        text=True,
    )


def _psql_ok(sql: str, **kw: Any) -> str:
    out = _psql(sql, **kw)
    if out.returncode != 0:
        raise RuntimeError(f"psql failed: {sql!r}: {out.stderr.strip()}")
    return out.stdout.strip()


def _superuser_password() -> str:
    # The compose default for the local dev container (the same default the app reads).
    return os.environ.get("POSTGRES_PASSWORD", "dev_changeme_in_production")


def prepare_scratch_db() -> str:
    """Drop and recreate the scratch database, migrate it to head, and create the
    non-superuser login role the app will connect as. Returns the role's password."""
    assert SCRATCH_DB != "piper_morgan"
    _psql_ok(f"DROP DATABASE IF EXISTS {SCRATCH_DB} WITH (FORCE)")
    _psql_ok(f"CREATE DATABASE {SCRATCH_DB}")
    env = _base_env()
    env["DATABASE_URL"] = (
        f"postgresql://{PG_SUPERUSER}:{_superuser_password()}@localhost:{PG_PORT}/{SCRATCH_DB}"
    )
    mig = subprocess.run(
        [str(ROOT / "venv/bin/python"), "-m", "alembic", "upgrade", "head"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    if mig.returncode != 0:
        raise RuntimeError(
            f"alembic upgrade head failed:\n{mig.stdout[-2000:]}\n{mig.stderr[-2000:]}"
        )
    password = secrets.token_hex(16)
    _psql_ok(f"DROP ROLE IF EXISTS {APP_ROLE}")
    _psql_ok(
        f"CREATE ROLE {APP_ROLE} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD '{password}'"
    )
    for sql in (
        f"GRANT CONNECT ON DATABASE {SCRATCH_DB} TO {APP_ROLE}",
        f"GRANT USAGE ON SCHEMA public TO {APP_ROLE}",
        f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {APP_ROLE}",
        f"GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO {APP_ROLE}",
    ):
        _psql_ok(sql, db=SCRATCH_DB)
    is_super = _psql_ok(f"SELECT rolsuper FROM pg_roles WHERE rolname = '{APP_ROLE}'")
    if is_super != "f":
        raise RuntimeError(f"{APP_ROLE} is a superuser ({is_super!r}); grants would not bind")
    return password


def drop_scratch_db() -> None:
    _psql(f"DROP DATABASE IF EXISTS {SCRATCH_DB} WITH (FORCE)")
    _psql(f"DROP ROLE IF EXISTS {APP_ROLE}")


def app_db_url(password: str) -> str:
    return f"postgresql://{APP_ROLE}:{password}@localhost:{PG_PORT}/{SCRATCH_DB}"


# ── the outbound sink: an HTTPS proxy that answers 502 to everything ────────


class FailingProxy:
    """Answers ``502 Bad Gateway`` to every request (a CONNECT included) and records
    the request line only (never a header or a body). Every fault server gets one as
    its HTTPS proxy, so a run cannot reach a real provider, and the evidence shows
    what the server tried to reach."""

    def __init__(self) -> None:
        self.requests: List[str] = []
        self._sock = socket.socket()
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("127.0.0.1", 0))
        self._sock.listen(8)
        self.port = int(self._sock.getsockname()[1])
        self._stop = False
        threading.Thread(target=self._serve, daemon=True).start()

    def _serve(self) -> None:
        while not self._stop:
            try:
                conn, _ = self._sock.accept()
            except OSError:
                return
            with conn:
                try:
                    conn.settimeout(5)
                    first = conn.recv(4096).split(b"\r\n", 1)[0].decode("latin-1")
                    self.requests.append(first)
                    conn.sendall(
                        b"HTTP/1.1 502 Bad Gateway\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
                    )
                except OSError:
                    pass

    def close(self) -> None:
        self._stop = True
        self._sock.close()


# ── the local server ─────────────────────────────────────────────────────────


def _base_env() -> Dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in STRIPPED}
    env["POSTGRES_PORT"] = PG_PORT
    env["PYTHONUNBUFFERED"] = "1"
    return env


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


class Server:
    def __init__(
        self,
        db_url: str,
        log_dir: Path,
        name: str,
        extra_env: Optional[Dict[str, Optional[str]]] = None,
    ):
        self.port = _free_port()
        self.base = f"http://127.0.0.1:{self.port}"
        self.log_path = log_dir / f"server-{name}.log"
        env = _base_env()
        # Every outbound HTTPS call is refused and recorded by the sink. The credential
        # store is the encrypted database store the hosted app uses (in the scratch
        # database), never this machine's OS keychain.
        self.sink = FailingProxy()
        sink_url = f"http://127.0.0.1:{self.sink.port}"
        env.update(
            DATABASE_URL=db_url,
            PIPER_PORT=str(self.port),
            JWT_SECRET_KEY=secrets.token_urlsafe(32),
            HTTPS_PROXY=sink_url,
            https_proxy=sink_url,
            NO_PROXY="127.0.0.1,localhost",
            no_proxy="127.0.0.1,localhost",
            PIPER_CREDENTIAL_STORE="db",
            ENCRYPTION_MASTER_KEY=base64.b64encode(secrets.token_bytes(32)).decode(),
        )
        for key, value in (extra_env or {}).items():
            if value is None:
                env.pop(key, None)
            else:
                env[key] = value
        self._log = open(self.log_path, "w")
        self.proc = subprocess.Popen(
            [str(ROOT / "venv/bin/python"), "main.py"],
            cwd=ROOT,
            env=env,
            stdout=self._log,
            stderr=subprocess.STDOUT,
        )

    def wait_healthy(self, timeout: float = 120.0) -> None:
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.proc.poll() is not None:
                raise RuntimeError(f"server exited {self.proc.returncode}; see {self.log_path}")
            try:
                if (
                    httpx.get(f"{self.base}/health", timeout=3.0, trust_env=False).status_code
                    == 200
                ):
                    return
            except httpx.HTTPError:
                pass
            time.sleep(1.0)
        raise RuntimeError(f"server not healthy after {timeout}s; see {self.log_path}")

    def log_lines(self, needle: str) -> List[str]:
        self._log.flush()
        return [
            ln.rstrip()
            for ln in self.log_path.read_text(errors="replace").splitlines()
            if needle in ln
        ]

    def stop(self) -> None:
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self._log.close()
        self.sink.close()


# ── rows ─────────────────────────────────────────────────────────────────────

# Not a real key. It has the shape the format gate wants (length, entropy), so the
# request gets as far as the provider check; a short fake is refused before any call.
FAKE_KEY = "sk-ant-api03-" + secrets.token_urlsafe(81)


def _validate_key(server: Server) -> httpx.Response:
    return httpx.post(
        f"{server.base}/api/v1/setup/validate-key",
        json={"provider": "anthropic", "api_key": FAKE_KEY},
        timeout=60.0,
        trust_env=False,
    )


def row_2125_store(db_url: str, log_dir: Path) -> Dict[str, Any]:
    bad_key = base64.b64encode(b"x" * 48).decode()  # 48 bytes: the length staging had (10-21)
    server = Server(db_url, log_dir, "2125-store", {"ENCRYPTION_MASTER_KEY": bad_key})
    try:
        server.wait_healthy()
        r = _validate_key(server)
        return {
            "row": "2125 (server can't store keys)",
            "fault": "ENCRYPTION_MASTER_KEY set to 48 bytes of base64 (AES-256 needs 32)",
            "request": "POST /api/v1/setup/validate-key {provider: anthropic, api_key: <fake>}",
            "status": r.status_code,
            "reply": r.json().get("message"),
            "body": r.json(),
            "branch": server.log_lines("key_store_unavailable"),
        }
    finally:
        server.stop()


def row_2125_check(db_url: str, log_dir: Path) -> Dict[str, Any]:
    server = Server(db_url, log_dir, "2125-check")
    try:
        server.wait_healthy()
        before = len(server.sink.requests)  # startup may make its own provider calls
        r = _validate_key(server)
        during = server.sink.requests[before:]
        if not any(req.startswith("CONNECT api.anthropic.com") for req in during):
            raise NotRun(f"this request never reached the stub (stub saw {during!r} during it)")
        return {
            "row": "2125 (key check couldn't run)",
            "fault": "the server's HTTPS proxy is a stub answering 502 to CONNECT",
            "stub_saw_during_request": during,
            "stub_saw_at_startup": server.sink.requests[:before],
            "request": "POST /api/v1/setup/validate-key {provider: anthropic, api_key: <fake>}",
            "status": r.status_code,
            "reply": r.json().get("message"),
            "body": r.json(),
            "branch": server.log_lines("key_check_unavailable")[-3:],
        }
    finally:
        server.stop()


def _create_account(server: Server) -> httpx.Client:
    """Create an account the way the wizard does (invite, create-user) and return a
    client carrying its session cookies."""
    token = "FAULTRUN" + secrets.token_hex(8).upper()
    _psql_ok(
        f"INSERT INTO invite_tokens (token, created_at) VALUES ('{token}', now())", db=SCRATCH_DB
    )
    client = httpx.Client(base_url=server.base, timeout=60.0, trust_env=False)
    name = "faultrun" + secrets.token_hex(3)
    password = secrets.token_urlsafe(16)
    r = client.post(
        "/api/v1/setup/create-user",
        json={
            "username": name,
            "email": f"{name}@example.invalid",
            "password": password,
            "password_confirm": password,
            "invite_token": token,
        },
    )
    if r.status_code != 200 or not r.json().get("success"):
        raise NotRun(f"create-user failed: {r.status_code} {r.text[:300]}")
    return client


PREFS_BASE = "/api/v1/settings/integrations"
# The four preferences GETs an account with nothing connected can reach. The calendars
# list, the Notion databases and the GitHub repositories read the provider first, so
# they need a connected account and are not run here.
PREFS_ROUTES = (
    "slack/preferences",
    "calendar/preferences",
    "notion/preferences",
    "github/preferences",
)


def _body(r: httpx.Response) -> Any:
    try:
        return r.json()
    except ValueError:
        return r.text


def row_2154(db_url: str, log_dir: Path) -> Dict[str, Any]:
    server = Server(db_url, log_dir, "2154")
    try:
        server.wait_healthy()
        client = _create_account(server)
        healthy = {route: client.get(f"{PREFS_BASE}/{route}").status_code for route in PREFS_ROUTES}
        if any(code != 200 for code in healthy.values()):
            raise NotRun(f"a healthy read did not answer 200 first: {healthy}")
        _psql_ok(f"REVOKE SELECT ON connector_configs FROM {APP_ROLE}", db=SCRATCH_DB)
        try:
            probe = _psql("SELECT 1 FROM connector_configs LIMIT 1", db=SCRATCH_DB, role=APP_ROLE)
            if probe.returncode == 0 or "permission denied" not in probe.stderr:
                raise NotRun(
                    f"the denial was not proved (probe rc={probe.returncode}: {probe.stderr.strip()!r})"
                )
            replies = {}
            for route in PREFS_ROUTES:
                r = client.get(f"{PREFS_BASE}/{route}")
                body = _body(r)
                replies[route] = {
                    "status": r.status_code,
                    "reply": body.get("detail") if isinstance(body, dict) else body,
                }
        finally:
            _psql_ok(f"GRANT SELECT ON connector_configs TO {APP_ROLE}", db=SCRATCH_DB)
        branch = server.log_lines("InsufficientPrivilege")
        return {
            "row": "2154 (failed preferences read)",
            "fault": f"REVOKE SELECT ON connector_configs FROM {APP_ROLE} (non-superuser app role)",
            "probe": probe.stderr.strip(),
            "healthy_first": healthy,
            "request": f"GET {PREFS_BASE}/<route> (signed-in account made by the wizard's create-user)",
            "replies": replies,
            "status": sorted({v["status"] for v in replies.values()}),
            "reply": sorted({str(v["reply"]) for v in replies.values()}),
            "branch": [ln[:400] for ln in branch],
        }
    finally:
        server.stop()


ROWS: Dict[str, Callable[[str, Path], Dict[str, Any]]] = {
    "2125-store": row_2125_store,
    "2125-check": row_2125_check,
    "2154": row_2154,
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--rows", default=",".join(ROWS))
    ap.add_argument(
        "--keep-logs", default=None, help="directory for server logs (default: a temp dir)"
    )
    ap.add_argument("--keep-db", action="store_true", help="leave the scratch database in place")
    args = ap.parse_args()
    wanted = [r.strip() for r in args.rows.split(",") if r.strip()]
    unknown = [r for r in wanted if r not in ROWS]
    if unknown:
        ap.error(f"unknown rows {unknown}; choose from {list(ROWS)}")

    log_dir = (
        Path(args.keep_logs) if args.keep_logs else Path(tempfile.mkdtemp(prefix="fault-run-"))
    )
    log_dir.mkdir(parents=True, exist_ok=True)
    sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--", "services", "web", "main.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.strip()
    results: List[Dict[str, Any]] = []
    password = prepare_scratch_db()
    try:
        for name in wanted:
            try:
                results.append(
                    {"name": name, "ran": True, **ROWS[name](app_db_url(password), log_dir)}
                )
            except NotRun as e:
                results.append({"name": name, "ran": False, "why": str(e)})
    finally:
        if not args.keep_db:
            drop_scratch_db()

    print(
        json.dumps(
            {"sha": sha, "served_tree_dirty": bool(dirty), "logs": str(log_dir), "rows": results},
            indent=2,
            default=str,
        )
    )
    return 0 if all(r["ran"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
