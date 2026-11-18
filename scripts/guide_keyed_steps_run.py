#!/usr/bin/env python
"""Issue 2404 (ADR-084 D2): run the self-host guide's keyed steps on a scratch install.

The guide is ``docs/installation/self-host-guide.md``. Steps 6 (start Piper), 7 (connect
your AI), 8 (create your account), 9 (finish) and its "Check it works" need a provider
key in the install's own database. This script takes those steps as the guide states
them, against a scratch database on the running local Postgres, and prints for each one
the line the guide tells a person to expect beside the line that was seen, and the
layer it was seen at. Step 5 (``scripts/local_key_setup.py``) needs a person at a
terminal and is not run.

Status-line wording for what this measures (Arch, 2026-11-17): "run by a seat against a
scratch database on a running local Postgres, key seeded by a driver".

Two modes, one of them required:
  --stub   no provider key and no provider call. A made-up key is seeded, the model is a
           local stand-in (``ANTHROPIC_BASE_URL``), and every other outbound HTTPS request
           from a proxy-honouring client is refused and recorded by a local sink. Spends
           nothing; the tests and the sample output use it.
  --real   the seat key, from the environment variable PIPER_SEAT_ANTHROPIC_KEY only
           (ADR-084 Step A). Never from argv, a file or a prompt. It spends: see PLANNED.

What the run holds to (Arch's read list and CIO's conditions on issue 2404):
  1. The key enters by the environment name only, is never printed or logged, and is
     written only to the scratch database's encrypted store: a seed process reads it on
     stdin and calls ``KeychainService().store_api_key(provider, key)``, the call step 5
     makes, then reads it back and compares. No SQL writes the row.
  2. ``ENCRYPTION_MASTER_KEY`` is generated for the run, given to the seed process and
     the server only, and is useless once the database is dropped. No ``.env`` is read
     or written: every process the run starts carries ``PYTHON_DOTENV_DISABLED=1``
     (python-dotenv 1.2.1 honours it), and the server starts in a run folder that holds
     no ``.env`` (point 6). Issue 2403 (the import-time load) is not needed for this.
  3. ``PIPER_CREDENTIAL_STORE=db``; nothing reaches a keyring. The server log's
     "from keychain" lines are counted.
  4. Spend: a served chat turn has no per-run stop, so the bound is the turns this script
     sends. It prints PLANNED before the first one and sends no more. COST is the sum of
     the provider's own token counts in the server's ``llm_usage`` lines (LOG_LEVEL=INFO
     for the run), priced from ``services/llm/spend_cap.py``. The server's startup key
     check is a raw call that writes no ``llm_usage`` line; it is reported apart, with
     its bound.
  5. Teardown runs on every exit path and says what it dropped: the server, the scratch
     database and its role, the run's Redis keys, the run folder.
  6. Shared stores (CIO, 2026-11-17). Postgres: a database and a login role made for the
     run (``piper_guide_run_<id>``, never ``piper_morgan``), the role a non-superuser with
     rights on that database only; the server is given the database by name. Redis: the
     run's own database number (REDIS_DB below), checked empty first, holding an owner
     marker, and the keys it lists at the end are deleted by name. Chroma: the server
     only opens a TCP connection to the shared Chroma server (the setup check); the
     app's in-process Chroma client writes under ``./data/chromadb``, and in Lead's
     worktree that folder IS the shared Chroma container's volume. So the server runs in
     a run folder whose entries link to the tree's, except ``data`` (an empty folder of
     its own) and ``.env`` (absent). The shared ``data/chromadb`` is listed before and
     after, and the run says whether it changed.
  7. A leftover from a crashed run (database, role, or Redis keys under this run's
     marker) is listed and removed by the next run. Redis keys without the marker stop
     the run.

Usage (repo root, local Postgres and Redis up):
    venv/bin/python scripts/guide_keyed_steps_run.py --stub
    venv/bin/python scripts/guide_keyed_steps_run.py --real --turns 1

Concept: issue 2404; ADR-084 D2; docs/internal/operations/canonical-ops-recipes.md (recipe 9).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
PG_CONTAINER = "piper-postgres"
PG_SUPERUSER = "piper"
PG_PORT = os.environ.get("POSTGRES_PORT", "5433")
REDIS_CONTAINER = "piper-redis"
REDIS_DB = 14  # empty on Amber's shared Redis when chosen (2026-11-18, INFO keyspace)
REDIS_MARKER = "piper_guide_run:owner"
NAME_PREFIX = "piper_guide_run_"
ROLE_PREFIX = "piper_guide_app_"
KEY_VAR = "PIPER_SEAT_ANTHROPIC_KEY"
PROVIDER = "anthropic"
CHAT_QUESTION = "What can you help me with?"  # Docs's proposal (issue 2404, 6967308743)
MAX_TURNS = 2

# Never passed to a process this run starts. The seat's key variables first: the server
# must find the key only where step 5 would have put it.
STRIPPED_PREFIXES = ("PIPER_SEAT_",)
STRIPPED = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_CUSTOM_HEADERS",
    "OPENAI_API_KEY",
    "GEMINI_API_KEY",
    "PERPLEXITY_API_KEY",
    "DATABASE_URL",
    "ALEMBIC_DATABASE_URL",
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_HOST",
    "REDIS_URL",
    "ENCRYPTION_MASTER_KEY",
    "ENCRYPTION_SCOPED_SUBKEYS",
    "JWT_SECRET_KEY",
    "PIPER_CREDENTIAL_STORE",
    "PIPER_PORT",
    "PIPER_BASE_URL",
    "LOG_LEVEL",
    "HTTPS_PROXY",
    "https_proxy",
    "HTTP_PROXY",
    "http_proxy",
    "ALL_PROXY",
    "all_proxy",
    "FLY_APP_NAME",
)

# What the guide tells a person to expect, per step. Docs read these from the guide and
# the code at main on 2026-11-17 (mail 01M7P7XSQN), recorded on issue 2404 as
# issuecomment-6967308743. The script compares against them; it does not reword them.
GUIDE = {
    "5": {
        "title": "Store your provider key",
        "action": "python scripts/local_key_setup.py",
        "expected": "not run by a seat: needs a person at a terminal",
    },
    "6": {
        "title": "Start Piper",
        "action": "python main.py",
        "expected": "It prints the setup address, `http://localhost:8001/setup`. "
        "(For this run the port is the run's own; the address ends in /setup.) "
        "Then the setup page answers HTTP 200.",
    },
    "7": {
        "title": "Connect your AI",
        "action": 'On the setup page choose Check System. Under "Connect Your AI" pick '
        "your provider and press Use saved key.",
        "expected": "After Check System, one line per service, each ✓ or ✗: Docker, "
        "PostgreSQL, Redis, ChromaDB, Temporal (optional); the message is "
        '"All services ready" or "Core services ready (Temporal optional)". '
        "Use saved key: success and valid true, and the page shows "
        "✓ Using the Anthropic key you already saved.",
    },
    "8": {
        "title": "Create your account",
        "action": "PYTHONPATH=. python3 scripts/mint_invite_tokens.py 1 --apply, then the "
        "code, a username and a password on the account page",
        "expected": "It prints one code. The account is created and signed in.",
    },
    "9": {
        "title": "Finish",
        "action": "Add a project or skip. Press Open Piper.",
        "expected": 'The heading "Setup Complete", the text "You\'re all set. You\'re '
        'signed in, and Piper is ready to help.", a link "Open Piper" to /. '
        "A seat can't press the link: / answers 200 with the session.",
    },
    "check": {
        "title": "Check it works",
        "action": f"Ask Piper a short question in the chat: {CHAT_QUESTION!r}",
        "expected": "A non-empty reply with no error banner. (Docs's proposal; the guide "
        "names no question and no pass rule.)",
    },
}


class Refused(Exception):
    """The run stopped before (or instead of) the step named in the message."""


# ── the key ──────────────────────────────────────────────────────────────────


def key_from_env(environ: Mapping[str, str]) -> str:
    """The seat key, from its environment name only. The message never holds a value."""
    value = environ.get(KEY_VAR, "")
    if not value.strip():
        raise Refused(
            f"{KEY_VAR} is not set in this environment, so no real run. "
            f"Check with: scripts/seat_settings_grant.py check-env --name {KEY_VAR}"
        )
    return value


def made_up_key() -> str:
    """A key-shaped value made for a stub run, built from parts so no source line holds
    a credential shape. It was never issued by anyone."""
    return "".join(("sk", "-ant-", "api03-", secrets.token_urlsafe(72)))


def leak_found(secret: str, texts: Iterable[str]) -> bool:
    return bool(secret) and any(secret in t for t in texts)


# ── names, environment, run folder ───────────────────────────────────────────


def run_names(run_id: str) -> Tuple[str, str]:
    if not re.fullmatch(r"[a-f0-9]{8}", run_id):
        raise ValueError("run id must be 8 hex characters")
    db, role = NAME_PREFIX + run_id, ROLE_PREFIX + run_id
    assert db != "piper_morgan" and role != PG_SUPERUSER
    return db, role


def base_env(environ: Mapping[str, str]) -> Dict[str, str]:
    """The parent environment minus every key, store and database variable."""
    return {
        k: v
        for k, v in environ.items()
        if k not in STRIPPED and not any(k.startswith(p) for p in STRIPPED_PREFIXES)
    }


def new_master_key() -> str:
    return base64.b64encode(secrets.token_bytes(32)).decode()


def child_env(
    environ: Mapping[str, str],
    *,
    db_url: str,
    master_key: str,
    redis_db: int = REDIS_DB,
) -> Dict[str, str]:
    """The environment every process this run starts gets (the seed, the mint, the
    server): the run's database by name, the run's master key, the database store, the
    run's Redis database, and no ``.env``."""
    env = base_env(environ)
    env.update(
        DATABASE_URL=db_url,
        POSTGRES_PORT=PG_PORT,
        REDIS_URL=f"redis://localhost:6379/{redis_db}",
        ENCRYPTION_MASTER_KEY=master_key,
        PIPER_CREDENTIAL_STORE="db",
        PYTHON_DOTENV_DISABLED="1",
        PYTHONUNBUFFERED="1",
        PYTHONPATH=str(ROOT),
    )
    return env


def server_env(
    environ: Mapping[str, str],
    *,
    db_url: str,
    master_key: str,
    port: int,
    stub_url: Optional[str] = None,
    sink_url: Optional[str] = None,
) -> Dict[str, str]:
    env = child_env(environ, db_url=db_url, master_key=master_key)
    env.update(
        PIPER_PORT=str(port),
        PIPER_BASE_URL=f"http://localhost:{port}",
        JWT_SECRET_KEY=secrets.token_urlsafe(32),
        LOG_LEVEL="INFO",  # the llm_usage lines are info; COST is read from them
        NO_PROXY="127.0.0.1,localhost",
        no_proxy="127.0.0.1,localhost",
    )
    if stub_url:
        env["ANTHROPIC_BASE_URL"] = stub_url
    if sink_url:
        env.update(HTTPS_PROXY=sink_url, https_proxy=sink_url)
    return env


def make_run_folder(root: Path, run_dir: Path) -> List[str]:
    """Link every top-level entry of ``root`` into ``run_dir`` except ``data`` and
    ``.env``; make ``data`` an empty folder of the run's own. Returns what was left out.
    The server's cwd-relative reads (``config/PIPER.md``, ``alembic.ini``) then resolve
    to the tree's files, and its cwd-relative writes (``./data/...``) to the run's."""
    left_out = []
    for entry in sorted(root.iterdir()):
        if entry.name in ("data", ".env"):
            left_out.append(entry.name)
            continue
        (run_dir / entry.name).symlink_to(entry)
    (run_dir / "data").mkdir()
    return left_out


def listing(folder: Path) -> Dict[str, Tuple[int, int]]:
    """name -> (size, mtime_ns) for every file under ``folder``; empty if absent."""
    out: Dict[str, Tuple[int, int]] = {}
    if not folder.is_dir():
        return out
    for path in folder.rglob("*"):
        try:
            if path.is_file():
                st = path.stat()
                out[str(path.relative_to(folder))] = (st.st_size, st.st_mtime_ns)
        except OSError:
            continue
    return out


def listing_change(before: Mapping[str, Any], after: Mapping[str, Any]) -> List[str]:
    changes = [f"added {n}" for n in sorted(set(after) - set(before))]
    changes += [f"removed {n}" for n in sorted(set(before) - set(after))]
    changes += [f"changed {n}" for n in sorted(set(before) & set(after)) if before[n] != after[n]]
    return changes


# ── Postgres (scratch database only) ─────────────────────────────────────────


def psql(sql: str, *, db: str = "postgres") -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "exec", PG_CONTAINER, "psql", "-v", "ON_ERROR_STOP=1", "-U", PG_SUPERUSER]
        + ["-d", db, "-Atc", sql],
        capture_output=True,
        text=True,
    )


def psql_ok(sql: str, **kw: Any) -> str:
    out = psql(sql, **kw)
    if out.returncode != 0:
        raise Refused(f"psql failed: {sql.split()[0]} ... ({out.stderr.strip()[:200]})")
    return out.stdout.strip()


def leftover_names(databases: str, roles: str) -> Tuple[List[str], List[str]]:
    dbs = [n for n in databases.split() if n.startswith(NAME_PREFIX)]
    rls = [n for n in roles.split() if n.startswith(ROLE_PREFIX)]
    return dbs, rls


def drop_db_and_role(db: str, role: str) -> List[str]:
    assert db.startswith(NAME_PREFIX) and role.startswith(ROLE_PREFIX)
    said = []
    if psql(f"DROP DATABASE IF EXISTS {db} WITH (FORCE)").returncode == 0:
        said.append(f"database {db} dropped")
    else:
        said.append(f"database {db}: DROP FAILED, remove it by hand")
    if psql(f"DROP ROLE IF EXISTS {role}").returncode == 0:
        said.append(f"role {role} dropped")
    else:
        said.append(f"role {role}: DROP FAILED, remove it by hand")
    return said


def remove_leftovers() -> List[str]:
    dbs, roles = leftover_names(
        psql_ok(f"SELECT datname FROM pg_database WHERE datname LIKE '{NAME_PREFIX}%'"),
        psql_ok(f"SELECT rolname FROM pg_roles WHERE rolname LIKE '{ROLE_PREFIX}%'"),
    )
    said = []
    for db in dbs:
        r = psql(f"DROP DATABASE IF EXISTS {db} WITH (FORCE)")
        said.append(
            f"leftover database {db} " + ("dropped" if r.returncode == 0 else "NOT dropped")
        )
    for role in roles:
        r = psql(f"DROP ROLE IF EXISTS {role}")
        said.append(f"leftover role {role} " + ("dropped" if r.returncode == 0 else "NOT dropped"))
    return said


def create_db_and_role(db: str, role: str, environ: Mapping[str, str]) -> str:
    """Create the run's database, migrate it to head as the compose superuser, and create
    a non-superuser login role with rights on that database only. Returns the app URL."""
    psql_ok(f"CREATE DATABASE {db}")
    password = os.environ.get("POSTGRES_PASSWORD", "dev_changeme_in_production")
    env = base_env(environ)
    env.update(
        DATABASE_URL=f"postgresql://{PG_SUPERUSER}:{password}@localhost:{PG_PORT}/{db}",
        PYTHON_DOTENV_DISABLED="1",
    )
    mig = subprocess.run(
        [str(ROOT / "venv/bin/python"), "-m", "alembic", "upgrade", "head"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    if mig.returncode != 0:
        raise Refused(f"alembic upgrade head failed on {db}: {mig.stderr.strip()[-400:]}")
    role_password = secrets.token_hex(16)
    psql_ok(
        f"CREATE ROLE {role} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE "
        f"PASSWORD '{role_password}'"
    )
    for sql in (
        f"REVOKE ALL ON DATABASE {db} FROM PUBLIC",
        f"GRANT CONNECT ON DATABASE {db} TO {role}",
        f"GRANT USAGE ON SCHEMA public TO {role}",
        f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {role}",
        f"GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO {role}",
    ):
        psql_ok(sql, db=db)
    if psql_ok(f"SELECT rolsuper FROM pg_roles WHERE rolname = '{role}'") != "f":
        raise Refused(f"{role} came out a superuser; stopping")
    return f"postgresql://{role}:{role_password}@localhost:{PG_PORT}/{db}"


# ── Redis (the run's own database number) ────────────────────────────────────


def redis_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "exec", REDIS_CONTAINER, "redis-cli", "-n", str(REDIS_DB), *args],
        capture_output=True,
        text=True,
    )


def redis_keys(cli: Callable[..., subprocess.CompletedProcess] = redis_cli) -> List[str]:
    out = cli("--scan")
    if out.returncode != 0:
        raise Refused(f"redis-cli --scan failed on database {REDIS_DB}: {out.stderr.strip()}")
    return sorted(k for k in out.stdout.splitlines() if k)


def claim_redis(
    run_id: str, cli: Callable[..., subprocess.CompletedProcess] = redis_cli
) -> List[str]:
    """Make the run's Redis database its own. Empty: set the marker. Holding only an
    earlier run's marker and keys: delete them by name, say so, set the marker. Holding
    keys with no marker: someone else uses that number; stop."""
    said = []
    keys = redis_keys(cli)
    if keys:
        if REDIS_MARKER not in keys:
            raise Refused(
                f"Redis database {REDIS_DB} holds {len(keys)} key(s) and no run marker; "
                "something else uses it. Nothing was changed."
            )
        for key in keys:
            cli("DEL", key)
        said.append(f"leftover Redis keys from an earlier run deleted: {len(keys)}")
    if cli("SET", REDIS_MARKER, run_id).returncode != 0:
        raise Refused("could not set the run's Redis marker")
    return said


def release_redis(cli: Callable[..., subprocess.CompletedProcess] = redis_cli) -> List[str]:
    """List what the run left in its Redis database (names only, long runs cut), delete
    exactly those keys, and say what is left."""
    keys = redis_keys(cli)
    written = [k for k in keys if k != REDIS_MARKER]
    for key in keys:
        cli("DEL", key)
    left = redis_keys(cli)
    shown = sorted({_key_shape(k) for k in written})
    return [
        f"Redis database {REDIS_DB}: the server wrote {len(written)} key(s); shapes: "
        + (", ".join(shown) if shown else "none"),
        f"Redis database {REDIS_DB}: deleted {len(keys)} key(s) by name; "
        f"{len(left)} left" + ("" if not left else " (REMOVE BY HAND)"),
    ]


def _key_shape(key: str) -> str:
    """A key name with any run of 12 or more letters and digits shown as <id>, so a
    token or nonce inside a key name is never printed."""
    return re.sub(r"[A-Za-z0-9_\-]{12,}", "<id>", key)


# ── stand-ins for a stub run ─────────────────────────────────────────────────


class Sink:
    """An HTTPS proxy that answers 502 to everything and records only the request line,
    so a stub run sends nothing to a provider. Proxy-honouring clients only (httpx, the
    Anthropic SDK); see ``served_fault_run.FailingProxy`` for the aiohttp limit."""

    def __init__(self) -> None:
        self.requests: List[str] = []
        self._sock = socket.socket()
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("127.0.0.1", 0))
        self._sock.listen(8)
        self.url = f"http://127.0.0.1:{self._sock.getsockname()[1]}"
        threading.Thread(target=self._serve, daemon=True).start()

    def _serve(self) -> None:
        while True:
            try:
                conn, _ = self._sock.accept()
            except OSError:
                return
            with conn:
                try:
                    conn.settimeout(5)
                    self.requests.append(conn.recv(4096).split(b"\r\n", 1)[0].decode("latin-1"))
                    conn.sendall(b"HTTP/1.1 502 Bad Gateway\r\nContent-Length: 0\r\n\r\n")
                except OSError:
                    pass

    def close(self) -> None:
        self._sock.close()


STUB_REPLY = "This is the run's stand-in model. No provider was called."


class ModelStub:
    """Answers ``POST /v1/messages`` with ``STUB_REPLY`` and fixed usage counts, and
    records per request the model asked for and whether the key header was the seeded
    made-up key (never the header itself)."""

    USAGE = {"input_tokens": 11, "output_tokens": 7}

    def __init__(self, seeded_key: str) -> None:
        import http.server

        self.hits: List[Dict[str, Any]] = []
        stub = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a: Any) -> None:
                return

            def do_POST(self) -> None:
                raw = self.rfile.read(int(self.headers.get("content-length") or 0))
                try:
                    req = json.loads(raw)
                except ValueError:
                    req = {}
                stub.hits.append(
                    {
                        "path": self.path,
                        "model": req.get("model"),
                        "seeded_key": self.headers.get("x-api-key") == seeded_key,
                    }
                )
                body = json.dumps(
                    {
                        "id": "msg_guide_run_stub",
                        "type": "message",
                        "role": "assistant",
                        "model": req.get("model"),
                        "content": [{"type": "text", "text": STUB_REPLY}],
                        "stop_reason": "end_turn",
                        "stop_sequence": None,
                        "usage": stub.USAGE,
                    }
                ).encode()
                self.send_response(200)
                self.send_header("content-type", "application/json")
                self.send_header("content-length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        self._httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._httpd.server_address[1]}"
        threading.Thread(target=self._httpd.serve_forever, daemon=True).start()

    def close(self) -> None:
        self._httpd.shutdown()


# ── the seed: step 5's own call, in a process with the run's environment ─────

SEED = """
import sys
from services.infrastructure.keychain_service import KeychainService, selected_store

provider = sys.argv[1]
key = sys.stdin.readline().rstrip("\\n")
if selected_store() != "db":
    print("REFUSED: the credential store is not db"); sys.exit(2)
service = KeychainService()
if getattr(service, "_db_store", None) is None:
    print("REFUSED: the database store did not open"); sys.exit(2)
service.store_api_key(provider, key)
same = service.get_api_key(provider) == key
print("store: db; stored with KeychainService().store_api_key; read back " + ("and matched" if same else "and DID NOT match"))
sys.exit(0 if same else 1)
"""


def seed_command() -> List[str]:
    """argv for the seed. It names the provider; the key goes on stdin."""
    return [str(ROOT / "venv/bin/python"), "-c", SEED, PROVIDER]


# ── reading the server log ───────────────────────────────────────────────────

_KV = re.compile(r"(\w+)=('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|[^\s,}]+)")


def _fields(line: str) -> Dict[str, Any]:
    start = line.find("{")
    if start >= 0:
        try:
            obj = json.loads(line[start:])
            if isinstance(obj, dict):
                return obj
        except ValueError:
            pass
    out: Dict[str, Any] = {}
    for k, v in _KV.findall(line):
        out[k] = v.strip("'\"")
    return out


def usage_calls(lines: Iterable[str]) -> List[Dict[str, Any]]:
    """One dict per ``llm_usage`` line: provider, model and the provider's counts."""
    calls = []
    for line in lines:
        if "llm_usage" not in line:
            continue
        f = _fields(line)

        def num(name: str) -> int:
            try:
                return int(f.get(name) or 0)
            except (TypeError, ValueError):
                return 0

        calls.append(
            {
                "provider": f.get("provider"),
                "model": f.get("model"),
                "input_tokens": num("prompt_tokens"),
                "output_tokens": num("completion_tokens"),
                "cache_creation_input_tokens": num("cache_write_tokens"),
                "cache_read_input_tokens": num("cache_read_tokens"),
            }
        )
    return calls


def _spend_cap() -> Any:
    """``services/llm/spend_cap.py`` loaded by its path: the one price table, without
    importing the ``services.llm`` package (whose ``__init__`` builds the LLM client)."""
    import importlib.util

    if "guide_run_spend_cap" not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            "guide_run_spend_cap", ROOT / "services" / "llm" / "spend_cap.py"
        )
        mod = importlib.util.module_from_spec(spec)
        sys.modules["guide_run_spend_cap"] = mod
        spec.loader.exec_module(mod)
    return sys.modules["guide_run_spend_cap"]


def priced(calls: Sequence[Mapping[str, Any]]) -> Tuple[float, List[str]]:
    """Total USD from the provider's counts, and a line per call. A model with no
    recorded price is named and left out of the total, never guessed."""
    cap = _spend_cap()
    SpendCapReached, usage_usd = cap.SpendCapReached, cap.usage_usd

    total, lines = 0.0, []
    for c in calls:
        counts = (
            f"in {c['input_tokens']}, out {c['output_tokens']}, cache write "
            f"{c['cache_creation_input_tokens']}, cache read {c['cache_read_input_tokens']}"
        )
        try:
            usd = usage_usd(str(c["model"]), c)
        except SpendCapReached:
            lines.append(f"{c['model']}: {counts}; NO RECORDED PRICE, not in the total")
            continue
        total += usd
        lines.append(f"{c['model']}: {counts}; ${usd:.6f}")
    return total, lines


def startup_check_bound() -> float:
    """The most the server's startup key check can cost: one Messages call to Haiku 4.5
    with the two-character prompt "Hi" and max_tokens 1
    (services/config/llm_config_service.py, ``_validate_anthropic``)."""
    return _spend_cap().upper_usd(
        "claude-haiku-4-5", 64, 1
    )  # 64 characters covers the request's text


def mask_codes(text: str, codes: Iterable[str]) -> str:
    for code in codes:
        if code and len(code) > 8:
            text = text.replace(code, f"{code[:4]}…{code[-4:]}")
    return text


# ── the server ───────────────────────────────────────────────────────────────


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


class Server:
    def __init__(self, env: Dict[str, str], run_dir: Path, port: int) -> None:
        self.port = port
        self.base = f"http://127.0.0.1:{port}"
        self.log_path = run_dir / "server.log"
        self._log = open(self.log_path, "w")
        self.proc = subprocess.Popen(
            [str(ROOT / "venv/bin/python"), str(ROOT / "main.py"), "--no-browser"],
            cwd=run_dir,
            env=env,
            stdout=self._log,
            stderr=subprocess.STDOUT,
        )

    def wait_healthy(self, timeout: float = 120.0) -> None:
        import httpx

        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.proc.poll() is not None:
                raise Refused(f"the server exited ({self.proc.returncode}) before it was healthy")
            try:
                if httpx.get(f"{self.base}/health", timeout=3, trust_env=False).status_code == 200:
                    return
            except httpx.HTTPError:
                pass
            time.sleep(1.0)
        raise Refused(f"the server was not healthy after {timeout:.0f}s")

    def lines(self, needle: str = "") -> List[str]:
        if not self._log.closed:
            self._log.flush()
        text = self.log_path.read_text(errors="replace")
        return [ln.rstrip() for ln in text.splitlines() if needle in ln]

    def stop(self) -> str:
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=10)
        self._log.close()
        return f"server stopped (exit {self.proc.returncode})"


# ── the steps ────────────────────────────────────────────────────────────────


@dataclass
class Block:
    step: str
    seen: List[str]
    layer: str
    note: str = ""

    def render(self) -> List[str]:
        g = GUIDE[self.step]
        head = f"STEP {self.step}" if self.step != "check" else "CHECK IT WORKS"
        out = [f"{head}: {g['title']}", f"  guide action: {g['action']}"]
        out.append(f"  expected: {g['expected']}")
        out += [f"  seen: {s}" for s in self.seen] or ["  seen: (nothing)"]
        out.append(f"  layer: {self.layer}")
        if self.note:
            out.append(f"  note: {self.note}")
        return out


@dataclass
class Run:
    mode: str  # "stub" or "real"
    turns: int
    environ: Mapping[str, str]
    out: Callable[[str], None] = print
    run_id: str = field(default_factory=lambda: secrets.token_hex(4))
    blocks: List[Block] = field(default_factory=list)
    teardown: List[str] = field(default_factory=list)

    def say(self, line: str = "") -> None:
        self.out(line)

    def execute(self) -> int:
        if self.mode not in ("stub", "real"):
            raise Refused("choose --stub or --real")
        if not 1 <= self.turns <= MAX_TURNS:
            raise Refused(f"--turns must be 1 to {MAX_TURNS}")
        key = key_from_env(self.environ) if self.mode == "real" else made_up_key()
        db, role = run_names(self.run_id)
        self.say(f"guide keyed-steps run {self.run_id} ({self.mode})")
        self.say(
            f"tree: {_git('rev-parse', 'HEAD')}" + (" (served paths edited)" if _dirty() else "")
        )
        shared_chroma = ROOT / "data" / "chromadb"
        chroma_before = listing(shared_chroma)
        run_dir = Path(tempfile.mkdtemp(prefix="guide-run-"))
        server: Optional[Server] = None
        stub = sink = None
        texts_to_scan: List[str] = []
        redis_claimed = False
        try:
            for line in remove_leftovers():
                self.say(line)
            for line in claim_redis(self.run_id):
                self.say(line)
            redis_claimed = True
            db_url = create_db_and_role(db, role, self.environ)
            self.say(
                f"scratch database {db}, login role {role} (non-superuser, this database only)"
            )
            master = new_master_key()
            left_out = make_run_folder(ROOT, run_dir)
            self.say(f"run folder: links to the tree except {', '.join(left_out) or 'nothing'}")

            # Step 5: not run; the key goes in through step 5's own call.
            seed = subprocess.run(
                seed_command(),
                input=key + "\n",
                cwd=run_dir,
                env=child_env(self.environ, db_url=db_url, master_key=master),
                capture_output=True,
                text=True,
            )
            texts_to_scan += [seed.stdout, seed.stderr]
            if seed.returncode != 0:
                raise Refused(f"seeding the key failed: {seed.stdout.strip()[-300:]}")
            self.blocks.append(
                Block(
                    "5",
                    [GUIDE["5"]["expected"]],
                    "none",
                    "The key was seeded by this driver through the call step 5 makes, "
                    "in a process with the run's environment: " + _last_line(seed.stdout, "store:"),
                )
            )

            # PLANNED, before anything can call a model.
            self.say(
                f"PLANNED: {self.turns} chat turn(s) of {CHAT_QUESTION!r}. A turn is usually "
                "2 to 3 model calls (the router's, the reply's, sometimes one more), each "
                "counted from the server's llm_usage lines. Before that, the server's startup "
                "key check: one Messages call to claude-haiku-4-5 with max_tokens 1 per "
                "validation pass, at most "
                f"${startup_check_bound():.6f} each; a stub run on 2026-11-18 saw two passes "
                "(two requests to api.anthropic.com at the sink). "
                + (
                    "Stub run: the model is a local stand-in and the startup check goes to "
                    "a refusing sink, so nothing is spent."
                    if self.mode == "stub"
                    else f"Real run on {KEY_VAR}: no other model call is sent by this script."
                )
            )

            if self.mode == "stub":
                stub, sink = ModelStub(key), Sink()
            port = free_port()
            env = server_env(
                self.environ,
                db_url=db_url,
                master_key=master,
                port=port,
                stub_url=stub.url if stub else None,
                sink_url=sink.url if sink else None,
            )
            server = Server(env, run_dir, port)
            self._steps(server, db, env, key, run_dir, texts_to_scan)
            if stub:
                self.say(
                    f"stand-in model: {len(stub.hits)} request(s), every one with the seeded "
                    f"key: {all(h['seeded_key'] for h in stub.hits) if stub.hits else 'n/a'}; "
                    f"models asked for: {sorted({str(h['model']) for h in stub.hits})}"
                )
            if sink:
                self.say(
                    f"refusing sink: {len(sink.requests)} request(s): "
                    f"{sorted(set(sink.requests)) or 'nothing'}"
                )
            return 0
        finally:
            if server is not None:
                self.teardown.append(server.stop())
                texts_to_scan.append(server.log_path.read_text(errors="replace"))
                self._cost(server)
            if stub:
                stub.close()
            if sink:
                sink.close()
            rendered = [line for b in self.blocks for line in b.render()]
            leaked = leak_found(key, texts_to_scan + rendered)
            if not leaked:
                for line in rendered:
                    self.say(line)
            self.say(
                "KEY CHECK: the key appears in "
                + (
                    "the run's logs or outputs, so the step blocks are WITHHELD"
                    if leaked
                    else "none of the run's logs, outputs or step blocks"
                )
            )
            if redis_claimed:
                try:
                    self.teardown += release_redis()
                except Refused as e:
                    self.teardown.append(f"Redis: {e}")
            else:
                self.teardown.append(
                    f"Redis database {REDIS_DB}: not claimed by this run, not touched"
                )
            self.teardown += drop_db_and_role(db, role)
            shutil.rmtree(run_dir, ignore_errors=True)
            self.teardown.append(f"run folder {run_dir} removed: {not run_dir.exists()}")
            change = listing_change(chroma_before, listing(shared_chroma))
            self.teardown.append(
                "shared data/chromadb: "
                + ("unchanged" if not change else "CHANGED: " + "; ".join(change[:10]))
            )
            for line in self.teardown:
                self.say(f"TEARDOWN: {line}")

    def _cost(self, server: Server) -> None:
        calls = usage_calls(server.lines("llm_usage"))
        total, lines = priced(calls)
        for line in lines:
            self.say(f"  call: {line}")
        checks = server.lines("Validating LLM providers")
        self.say(
            f"COST: ${total:.6f} from {len(calls)} llm_usage line(s), the provider's own counts"
            + (
                " (the stand-in's fixed counts on a stub run; nothing spent)"
                if self.mode == "stub"
                else ""
            )
            + f"; plus the startup key check ({len(checks)} 'Validating LLM providers' line(s) "
            f"in the server log), at most ${startup_check_bound():.6f} each"
        )

    def _steps(
        self,
        server: Server,
        db: str,
        env: Dict[str, str],
        key: str,
        run_dir: Path,
        texts_to_scan: List[str],
    ) -> None:
        import httpx

        server.wait_healthy()
        client = httpx.Client(base_url=server.base, timeout=180.0, trust_env=False)

        # Step 6
        printed = [ln.strip() for ln in server.lines() if "Web Interface:" in ln or "/setup" in ln]
        setup_page = client.get("/setup")
        root_anon = client.get("/", follow_redirects=False)
        self.blocks.append(
            Block(
                "6",
                printed[:3]
                + [
                    f"GET /setup -> {setup_page.status_code}",
                    f"GET / (no session) -> {root_anon.status_code}"
                    + (
                        f", Location {root_anon.headers.get('location')}"
                        if root_anon.is_redirect
                        else ""
                    ),
                ],
                "server stdout; HTTP reply",
            )
        )

        # Step 7
        check = client.post("/api/v1/setup/check-system")
        cb = _json(check)
        services = [
            ("Docker", "docker_available"),
            ("PostgreSQL", "postgres_ready"),
            ("Redis", "redis_ready"),
            ("ChromaDB", "chromadb_ready"),
            ("Temporal (optional)", "temporal_ready"),
        ]
        use = client.post("/api/v1/setup/use-keychain", json={"provider": PROVIDER})
        ub = _json(use)
        self.blocks.append(
            Block(
                "7",
                [f"check-system -> {check.status_code}"]
                + [f"{'✓' if cb.get(field_) else '✗'} {name}" for name, field_ in services]
                + [
                    f"message: {cb.get('message') or cb.get('detail')!r}",
                    f"use-keychain -> {use.status_code}: success {ub.get('success')}, "
                    f"valid {ub.get('valid')}",
                    "page line: "
                    + (
                        ("✓ " if ub.get("success") and ub.get("valid") else "✗ ")
                        + str(ub.get("message"))
                    ),
                ],
                "HTTP reply (the page's two calls); the ✓/✗ lines are built from the reply "
                "the way setup.js builds them",
                f"store before the call: {env['PIPER_CREDENTIAL_STORE']} (the run's own "
                "database); the key came from the run's database, seeded at step 5's call",
            )
        )

        # Step 8: the guide's own mint command, then the page's create-user call.
        mint = subprocess.run(
            [str(ROOT / "venv/bin/python"), "scripts/mint_invite_tokens.py", "1", "--apply"],
            cwd=run_dir,
            env=child_env(
                self.environ, db_url=env["DATABASE_URL"], master_key=env["ENCRYPTION_MASTER_KEY"]
            ),
            capture_output=True,
            text=True,
        )
        codes = [
            ln.strip()
            for ln in mint.stdout.splitlines()
            if re.fullmatch(r"[A-Z0-9]{16,40}", ln.strip())
        ]
        if mint.returncode != 0 or len(codes) != 1:
            raise Refused(f"the mint did not print one code (exit {mint.returncode})")
        code = codes[0]
        if db not in mint.stdout:
            raise Refused("the mint's target line does not name the run's database")
        name = "guiderun" + secrets.token_hex(3)
        password = secrets.token_urlsafe(18)
        made = client.post(
            "/api/v1/setup/create-user",
            json={
                "username": name,
                "email": f"{name}@example.invalid",
                "password": password,
                "password_confirm": password,
                "invite_token": code,
            },
        )
        mb = _json(made)
        complete = client.post(
            "/api/v1/setup/complete",
            json={
                "user_id": mb.get("user_id"),
                "default_llm_provider": PROVIDER,
                "openai_key": None,
                "anthropic_key": None,  # what setup.js sends for a key taken by Use saved key
                "gemini_key": None,
                "notion_key": None,
            },
        )
        comp = _json(complete)
        self.blocks.append(
            Block(
                "8",
                [
                    "mint: " + mask_codes(ln.strip(), [code])
                    for ln in mint.stdout.splitlines()
                    if ln.startswith(("===", "---")) or ln.strip() == code
                ]
                + [
                    f"create-user -> {made.status_code}: {mb.get('message') or mb.get('detail')!r}",
                    f"signed in: {'yes' if made.cookies else 'no'} (session cookies set by create-user)",
                    f"complete -> {complete.status_code}: {comp.get('message') or comp.get('detail')!r}",
                ],
                "the mint's stdout (code masked); HTTP reply",
                "The account was made with the guide's invite path (its mint command, then "
                "create-user). The mint's last line, about HOST's roster, is left out, as the "
                "guide says to ignore it. complete is the call setup.js makes after "
                "create-user, with no key in it for a key taken by Use saved key.",
            )
        )

        # Step 9
        page = setup_page.text
        wanted = [
            "<h2>Setup Complete</h2>",
            "You're all set. You're signed in, and Piper is ready to help.",
            ">Open Piper</a",
        ]
        home = client.get("/", follow_redirects=False)
        self.blocks.append(
            Block(
                "9",
                [f"setup page HTML holds {w!r}: {w in page}" for w in wanted]
                + [
                    f"GET / with the session -> {home.status_code}"
                    + (f", Location {home.headers.get('location')}" if home.is_redirect else "")
                ],
                "page HTML (the finish panel is in the page from the start; skip only shows "
                "it); HTTP reply",
                "Skip was taken (no project). A seat can't press Open Piper; / was fetched "
                "with the session instead.",
            )
        )

        # Check it works: the planned turns and no more.
        seen = []
        for n in range(self.turns):
            r = client.post(
                "/api/v1/intent",
                json={"message": CHAT_QUESTION, "session_id": str(uuid.uuid4())},
            )
            b = _json(r)
            reply = b.get("message") or b.get("response") or ""
            seen += [
                f"turn {n + 1}: POST /api/v1/intent -> {r.status_code}",
                f"turn {n + 1} reply: {str(reply)[:600]!r}",
                f"turn {n + 1} error_type: {b.get('error_type')!r}",
            ]
        time.sleep(5)  # calls the server makes after the reply land in the log too
        texts_to_scan.append(mint.stdout + mint.stderr)
        self.blocks.append(
            Block(
                "check",
                seen,
                "HTTP reply of the call chat.js makes",
                "Model calls, from the server log, are under COST.",
            )
        )
        self.say(
            "credential store, from the server log's own line: "
            + "; ".join(sorted({_backend(ln) for ln in server.lines("os_backend=")}) or ["no line"])
            + f". (Lines worded 'from keychain': {len(server.lines('from keychain'))}; that is "
            "the log's old wording for the store in use, not an OS keychain read.)"
        )


def _last_line(text: str, prefix: str) -> str:
    hits = [ln.strip() for ln in text.splitlines() if ln.strip().startswith(prefix)]
    return hits[-1] if hits else "(no line)"


def _backend(line: str) -> str:
    """The store part of the "Keychain service initialized" line, as the log wrote it."""
    at = line.find("backend=")
    return " ".join(line[at:].split()) if at >= 0 else line.strip()


def _json(r: Any) -> Dict[str, Any]:
    try:
        body = r.json()
    except ValueError:
        return {}
    return body if isinstance(body, dict) else {}


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def _dirty() -> bool:
    return bool(_git("status", "--porcelain", "--", "services", "web", "templates", "main.py"))


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Run the self-host guide's keyed steps (issue 2404).")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--stub", action="store_true", help="no key, no provider call")
    mode.add_argument("--real", action="store_true", help=f"the seat key from {KEY_VAR}; spends")
    ap.add_argument("--turns", type=int, default=1, help=f"chat turns, 1 to {MAX_TURNS}")
    args = ap.parse_args(argv)
    # Before anything this process imports could call load_dotenv: no .env, here either.
    os.environ["PYTHON_DOTENV_DISABLED"] = "1"
    try:
        return Run("real" if args.real else "stub", args.turns, os.environ).execute()
    except Refused as refusal:
        print(f"guide_keyed_steps_run: stopped: {refusal}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
