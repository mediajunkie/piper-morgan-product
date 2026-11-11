#!/usr/bin/env python
"""#2232: the local served fault run.

Starts ``main.py`` from the current tree against a SCRATCH database on the local
Postgres (5433), points one upstream at a failing stub, sends the HTTP request a
partner's browser would send, and prints the reply with the evidence that the
failure branch was the one reached. For the rows whose failure cannot be forced
on alpha (Arch, 2026-10-30: never a fault switch in served code, never a forced
upstream failure on the host partners use).

No served code is changed by this script and nothing here is imported by the app.

Rows (``--rows``, comma-separated; default: all; none needs a real LLM key):
  2125-store   wizard validate-key on a server whose ENCRYPTION_MASTER_KEY is the
               wrong length -> "The server can't store keys right now..."
  2125-check   wizard validate-key while the provider cannot be reached (the
               server's HTTPS proxy is a stub answering 502 to CONNECT)
               -> "The key check couldn't run just now..."
  2154         GET the four preferences routes while the app's database role is refused
               SELECT on connector_configs -> 503 with CXO's line
  955          chat turn "forget my clear preference" while the app's role is refused
               UPDATE on users.preferences -> "I couldn't change that just now..."
               The model is a local scripted stub (Arch, decisions.log 2026-11-11
               06:55): its answers are copied from a served trace of the same phrasing,
               the row proves the stub was the model (no key, stub hits, nothing sent
               to the real provider), and the row says "routing scripted from <trace>".

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
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

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
    its HTTPS proxy, and the evidence shows what the server tried to reach.

    Limit (found 2026-11-11): only clients that read the proxy from the environment
    go through it (httpx, the Anthropic SDK). The ``aiohttp.ClientSession()`` call
    sites (Slack's client, the settings routes' provider lists) do not, so the sink
    neither refuses nor records them. The rows here run on accounts with nothing
    connected, so by a source reading none reaches those sites; the sink cannot show
    that, and a row that would reach one must not cite the sink as proof."""

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
        # Outbound HTTPS from proxy-honouring clients is refused and recorded by the
        # sink (see FailingProxy for the aiohttp limit). The credential
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
    client.fault_run_login = (name, password)  # type: ignore[attr-defined]
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


def hold_2154(db_url: str, log_dir: Path, hold_file: Path) -> Dict[str, Any]:
    """The page half of 2154 (CXO, 11-11): bring the server up in the failed-read state
    and HOLD it there for a browser check. Writes the base URL and the scratch account's
    sign-in to ``hold_file`` (a throwaway account in a database that is dropped on exit)
    and waits until that file is deleted, then restores the grant and stops."""
    server = Server(db_url, log_dir, "2154-hold")
    try:
        server.wait_healthy()
        client = _create_account(server)
        name, password = client.fault_run_login  # type: ignore[attr-defined]
        _psql_ok(f"REVOKE SELECT ON connector_configs FROM {APP_ROLE}", db=SCRATCH_DB)
        try:
            probe = _psql("SELECT 1 FROM connector_configs LIMIT 1", db=SCRATCH_DB, role=APP_ROLE)
            if probe.returncode == 0 or "permission denied" not in probe.stderr:
                raise NotRun(f"the denial was not proved ({probe.stderr.strip()!r})")
            hold_file.write_text(
                json.dumps({"base": server.base, "username": name, "password": password})
            )
            while hold_file.exists():
                time.sleep(1.0)
        finally:
            _psql_ok(f"GRANT SELECT ON connector_configs TO {APP_ROLE}", db=SCRATCH_DB)
        return {
            "row": "2154 (held for a browser check)",
            "probe": probe.stderr.strip(),
            "posts_seen_by_server": server.log_lines('"POST /api/v1/settings/integrations'),
            "gets_seen_by_server": server.log_lines('"GET /api/v1/settings/integrations'),
        }
    finally:
        server.stop()


# ── the scripted model: a local stand-in for the Anthropic Messages API ────


def _prompt_text(req: Dict[str, Any]) -> str:
    """Every text part of a Messages request (system and messages), unescaped."""
    parts: List[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, str):
            parts.append(node)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            walk(node.get("text") if "text" in node else node.get("content"))

    walk(req.get("system"))
    walk(req.get("messages"))
    return "\n".join(parts)


class LLMStub:
    """Answers ``POST /v1/messages`` from a script (Arch, decisions.log 2026-11-11
    06:55). Each rule is ``(name, needles, reply text)``; a request whose prompt holds
    every needle gets that reply in the Messages API shape. A request no rule matches
    is answered 500 and counted as unscripted, so a run never rests on an answer nobody
    wrote down. Records, per request: the rule, the model asked for, and whether the
    key header was the run's throwaway string (never the header itself)."""

    def __init__(self, rules: List[Tuple[str, Tuple[str, ...], str]], fake_key: str) -> None:
        import http.server

        self.rules = rules
        self.hits: List[Dict[str, Any]] = []
        stub = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a: Any) -> None:  # quiet
                return

            def do_POST(self) -> None:
                raw = self.rfile.read(int(self.headers.get("content-length") or 0))
                try:
                    req = json.loads(raw)
                except ValueError:
                    req = {}
                prompt = _prompt_text(req)
                rule = next(
                    (r for r in stub.rules if all(n in prompt for n in r[1])),
                    None,
                )
                stub.hits.append(
                    {
                        "path": self.path,
                        "model": req.get("model"),
                        "rule": rule[0] if rule else None,
                        "throwaway_key": self.headers.get("x-api-key") == fake_key,
                        "prompt_head": prompt[:160] if rule is None else None,
                    }
                )
                if rule is None:
                    body = {
                        "type": "error",
                        "error": {"type": "api_error", "message": "unscripted"},
                    }
                    code = 500
                else:
                    body = {
                        "id": "msg_fault_run_stub",
                        "type": "message",
                        "role": "assistant",
                        "model": req.get("model"),
                        "content": [{"type": "text", "text": rule[2]}],
                        "stop_reason": "end_turn",
                        "stop_sequence": None,
                        "usage": {"input_tokens": 1, "output_tokens": 1},
                    }
                    code = 200
                data = json.dumps(body).encode()
                self.send_response(code)
                self.send_header("content-type", "application/json")
                self.send_header("content-length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self._httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._httpd.server_address[1]}"
        threading.Thread(target=self._httpd.serve_forever, daemon=True).start()

    def close(self) -> None:
        self._httpd.shutdown()


# ── row 955: the failed-write line of "forget my clear preference" ─────────

TRACE_955 = "dev/2026/11/08/served-8677aa05f5-955-set-asks-2026-11-08.txt"
PHRASE_955 = "forget my clear preference"
# The served trace (beta 8677aa05f5, 15:20:40) stamps this phrasing
# ``route query/forget_clear_preference``: the classifier's category and action. The
# alias takes no arguments. Two things the trace does NOT record are written here:
#   * the classifier's confidence (0.9 is the value in the served prompt's own example
#     for this phrase, ``services/intent_service/prompts.py``);
#   * the live router's answer. The entry is router-hidden (#2132), so the router
#     cannot name it, and the stamped route shows the router did not send the turn
#     elsewhere; NONE is scripted, the case the landing pin covers
#     (``test_landing_pin_the_routers_none_does_not_floor_the_hidden_entry``).
CLASSIFIER_955 = json.dumps(
    {
        "category": "query",
        "action": "forget_clear_preference",
        "confidence": 0.9,
        "reasoning": f"scripted from {TRACE_955}",
    }
)
ROUTER_955 = json.dumps(
    {
        "operation": "NONE",
        "args": {},
        "confidence": 0.95,
        "rationale": "scripted: the entry is router-hidden",
    }
)
# The mirror of alpha's live flag kept in scripts/inversion_phase3_deletion_gate.py
# (CURRENT_LIVE_CATEGORIES). The served secret itself is not read by this script.
ALPHA_LIVE_MIRROR = (
    "ADD_PROJECT,COMPLETE_TODO,CREATE_REMINDER,CREATE_TODO,DELETE_TODO,READ_CANONICAL,"
    "READ_FLOOR,READ_FLOOR_2,READ_PORTFOLIO,READ_REFERENT,READ_STATUS,READ_STRATEGIC,"
    "READ_SYNTHESIS,READ_TEMPORAL,SET_DEFAULT_REPO"
)
PREF_KEY_955 = "reminder_clear_verb:clear"


def _seed_clear_preference(db_url: str, user_id: str) -> None:
    """Store "clear means mark it done" with the product's own writer, in the scratch
    database, so the stored record has the shape the first-time answer writes."""
    env = _base_env()
    env["DATABASE_URL"] = db_url
    env["PIPER_CREDENTIAL_STORE"] = "db"  # never this machine's OS keychain
    code = (
        "import asyncio, sys\n"
        "from services.intent_service import verified_inference as vi\n"
        "from services.intent_service.reminder_clear import VALUE_COMPLETE\n"
        f"ok = asyncio.run(vi.store_verified_inference({user_id!r}, {PREF_KEY_955!r}, VALUE_COMPLETE))\n"
        "sys.exit(0 if ok else 1)\n"
    )
    out = subprocess.run(
        [str(ROOT / "venv/bin/python"), "-c", code],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    if out.returncode != 0:
        raise NotRun(f"seeding the preference failed: {out.stderr[-400:]}")


def _stored_clear_value(user_id: str) -> str:
    return _psql_ok(
        "SELECT coalesce(preferences->'verified_inferences'->"
        f"'{PREF_KEY_955}'->>'value', '') FROM users WHERE id = '{user_id}'",
        db=SCRATCH_DB,
    )


def _chat(client: httpx.Client, message: str, fake_key: str) -> Dict[str, Any]:
    r = client.post(
        "/api/v1/intent",
        json={"message": message, "session_id": str(uuid.uuid4())},
        headers={"X-User-Api-Key": fake_key},
        timeout=180.0,
    )
    body = _body(r)
    data = body if isinstance(body, dict) else {}
    intent = data.get("intent") or data.get("intent_data") or {}
    return {
        "status": r.status_code,
        "route": f"{intent.get('category')}/{intent.get('action')}",
        "preference_change": intent.get("preference_change"),
        "reply": data.get("message") or data.get("response") or body,
    }


def row_955(db_url: str, log_dir: Path) -> Dict[str, Any]:
    fake_key = "fault-run-not-a-key-" + secrets.token_hex(8)
    stub = LLMStub(
        [
            # The classifier's prompt lists the alias by name; the router's cannot.
            ("classifier", (PHRASE_955, "forget_clear_preference"), CLASSIFIER_955),
            ("router", (PHRASE_955, '"operation"'), ROUTER_955),
        ],
        fake_key,
    )
    server = Server(
        db_url,
        log_dir,
        "955",
        extra_env={
            "ANTHROPIC_BASE_URL": stub.url,
            "PIPER_INVERSION_LIVE_CATEGORIES": ALPHA_LIVE_MIRROR,
        },
    )
    try:
        server.wait_healthy()
        client = _create_account(server)
        name, _pw = client.fault_run_login  # type: ignore[attr-defined]
        user_id = _psql_ok(f"SELECT id FROM users WHERE username = '{name}'", db=SCRATCH_DB)
        stored_keys = _psql_ok("SELECT count(*) FROM user_api_keys", db=SCRATCH_DB)

        # Healthy first: the same turn on a writable store forgets, and the key is gone.
        _seed_clear_preference(db_url, user_id)
        if _stored_clear_value(user_id) == "":
            raise NotRun("the seeded preference was not stored")
        healthy = _chat(client, PHRASE_955, fake_key)
        healthy["stored_after"] = _stored_clear_value(user_id)
        if healthy["preference_change"] != "forgotten" or healthy["stored_after"] != "":
            raise NotRun(f"the healthy turn did not forget: {healthy}; stub {stub.hits}")

        # The fault: this role may update every users column except preferences.
        _seed_clear_preference(db_url, user_id)
        seeded = _stored_clear_value(user_id)
        cols = _psql_ok(
            "SELECT string_agg(quote_ident(column_name), ', ') FROM information_schema.columns "
            "WHERE table_schema = 'public' AND table_name = 'users' "
            "AND column_name <> 'preferences'",
            db=SCRATCH_DB,
        )
        _psql_ok(f"REVOKE UPDATE ON users FROM {APP_ROLE}", db=SCRATCH_DB)
        _psql_ok(f"GRANT UPDATE ({cols}) ON users TO {APP_ROLE}", db=SCRATCH_DB)
        hits_before = len(stub.hits)
        try:
            probe = _psql(
                "UPDATE users SET preferences = preferences WHERE false",
                db=SCRATCH_DB,
                role=APP_ROLE,
            )
            if probe.returncode == 0 or "permission denied" not in probe.stderr:
                raise NotRun(
                    f"the denial was not proved (probe rc={probe.returncode}: {probe.stderr.strip()!r})"
                )
            read_probe = _psql(
                f"SELECT preferences IS NOT NULL FROM users WHERE id = '{user_id}'",
                db=SCRATCH_DB,
                role=APP_ROLE,
            )
            if read_probe.returncode != 0:
                raise NotRun(f"the read was refused too: {read_probe.stderr.strip()!r}")
            failed = _chat(client, PHRASE_955, fake_key)
        finally:
            _psql_ok(f"GRANT UPDATE ON users TO {APP_ROLE}", db=SCRATCH_DB)
        stored_after = _stored_clear_value(user_id)
        real_provider = [q for q in server.sink.requests if "anthropic" in q.lower()]
        unscripted = [h for h in stub.hits if h["rule"] is None]
        fault_hits = stub.hits[hits_before:]
        # The classifier caches by message in process (IntentCache), so the fault turn
        # reuses the stub's own classifier answer from the healthy turn; the router is
        # asked again. Either way every model answer in this row came from the stub.
        if not fault_hits or not any(h["rule"] == "classifier" for h in stub.hits):
            raise NotRun(f"the scripted model was not asked: {stub.hits}")
        if unscripted:
            raise NotRun(f"the server asked the model something unscripted: {unscripted}")
        if real_provider:
            raise NotRun(f"the server tried the real provider: {real_provider}")
        return {
            "row": "955 (failed write on forget; routing scripted from " + TRACE_955 + ")",
            "routing": {
                "scripted_from": TRACE_955,
                "phrase": PHRASE_955,
                "served_route_in_trace": "query/forget_clear_preference",
                "scripted_classifier_answer": json.loads(CLASSIFIER_955),
                "scripted_router_answer": json.loads(ROUTER_955),
                "not_in_trace": [
                    "the classifier's confidence (0.9, the served prompt's own example)",
                    "the classifier's reasoning text (a required field; a label here)",
                    "the live router's answer (NONE scripted; the entry is router-hidden)",
                ],
                "live_flag": "mirror of alpha's set from the deletion gate, not read from the host",
            },
            "model_was_the_stub": {
                "anthropic_env_stripped": [k for k in STRIPPED if k.startswith("ANTHROPIC")],
                "stored_llm_keys_in_scratch_db": stored_keys,
                "request_key": "a throwaway string in X-User-Api-Key (not a provider key)",
                "stub_hits": len(stub.hits),
                "stub_hits_by_rule": {
                    r: sum(1 for h in stub.hits if h["rule"] == r) for r in ("router", "classifier")
                },
                "stub_hits_on_fault_turn": fault_hits,
                "classifier_on_fault_turn": (
                    "asked"
                    if any(h["rule"] == "classifier" for h in fault_hits)
                    else "not asked: the classifier's in-process cache (IntentCache, keyed "
                    "on the message) returned the stub's answer from the healthy turn"
                ),
                "unscripted_requests": unscripted,
                "requests_to_real_provider": real_provider,
                "sink_saw": sorted(set(server.sink.requests)),
            },
            "fault": (
                f"REVOKE UPDATE ON users FROM {APP_ROLE}, then GRANT UPDATE on every "
                "users column except preferences (non-superuser app role)"
            ),
            "probe": probe.stderr.strip(),
            "seeded_value": seeded,
            "healthy_first": healthy,
            "request": f"POST /api/v1/intent {{message: {PHRASE_955!r}}} (signed-in scratch account)",
            "status": failed["status"],
            "route": failed["route"],
            "preference_change": failed["preference_change"],
            "reply": failed["reply"],
            "stored_value_after": stored_after,
            "branch": [
                ln[:500] for ln in server.log_lines("verified_inference_forget_write_failed")
            ],
        }
    finally:
        server.stop()
        stub.close()


ROWS: Dict[str, Callable[[str, Path], Dict[str, Any]]] = {
    "2125-store": row_2125_store,
    "2125-check": row_2125_check,
    "2154": row_2154,
    "955": row_955,
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--rows", default=",".join(ROWS))
    ap.add_argument(
        "--keep-logs", default=None, help="directory for server logs (default: a temp dir)"
    )
    ap.add_argument("--keep-db", action="store_true", help="leave the scratch database in place")
    ap.add_argument(
        "--hold-2154",
        default=None,
        metavar="FILE",
        help="hold the 2154 failed-read state for a browser check; sign-in details are "
        "written to FILE, and deleting FILE ends the hold (no other row runs)",
    )
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
        if args.hold_2154:
            wanted = []
            try:
                held = hold_2154(app_db_url(password), log_dir, Path(args.hold_2154))
                results.append({"name": "2154-hold", "ran": True, **held})
            except NotRun as e:
                results.append({"name": "2154-hold", "ran": False, "why": str(e)})
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
