#!/usr/bin/env python3
"""erase_user.py — count, then (only on request) erase, one user and everything they own.  DESTRUCTIVE.

Why (#2064, Arch-ruled shape, 2026-10-16): the live /privacy page promises
"email support and we'll delete your account and everything in it within 14
days". Before this payload no code path could keep that promise: a bare
``DELETE FROM users`` stops on the foreign keys that have no ON DELETE, and the
tables with no FK to users at all would keep the user's rows forever.

THE BOUNDARY IS THIS FILE IN THE DEPLOYED IMAGE (the prod-exec rule,
docs/internal/operations/prod-command-permissions.md): the production command is
    fly ssh console -a piper-morgan -C "python /app/scripts/erase_user.py <id-or-username-or-email>"
with no shell, so everything after the prefix arrives here as argv. Every
limit lives in this file: the argv shape, count-by-default, the two-step erase.

Usage:
  python /app/scripts/erase_user.py <user-id | username | email>
      COUNT ONLY (the default). Prints every store and how much of this user it
      holds. Writes nothing anywhere.
  python /app/scripts/erase_user.py <user-id | username | email> --erase --confirm <user-id>
      ERASE. ``--confirm`` must repeat the user's full id exactly as the count
      run printed it (the two-step: you cannot erase without having counted, or
      without already holding the exact id). Prints the same counts after.
      Rerunning by id after the account row is gone counts (and erases) any
      leftovers keyed by that id, so a partial run can always be finished.

Before anything else, both modes run the PRE-FLIGHT (Arch's condition,
2026-10-16): every statement of the plan, in order, inside a transaction that
is always rolled back. A statement that raises (another user's row still
references this user's data, an FK the plan missed) means the real erase would
roll back at step 4 AFTER steps 1-3 had already destroyed the outside stores.
So count mode prints the verdict ("would erase cleanly" / "would refuse at
<table>"), and erase mode refuses on a failed pre-flight with nothing erased
anywhere, naming the table and the error class, and exits non-zero.

What erase does, in this order (each pointer-holding store outside Postgres
is cleared BEFORE the rows that hold its pointer, so a rerun after any failure
still finds what is left; the whole thing is idempotent):
  1. provider grants: for each connector the user has a stored credential for,
     the app's own ``disconnect_connector`` (revokes on the provider's side
     where the provider supports it, then clears the local credential).
     Best effort: a provider failure is printed and the erase continues.
  2. upload files: every DB-known ``uploaded_files.storage_path`` through the
     storage seam (``delete_file_from_storage``), then anything left under
     ``<UPLOAD_DIR>/<user-id>/`` and that directory itself.
  3. ChromaDB chunks of the user's documents (the in-app store, if present).
  4. Postgres: ONE transaction, the plan below in dependency order. Any error
     rolls the whole transaction back; nothing partial is committed.
  5. Redis cache keys naming the user or their conversations (TTL caches;
     best effort).

Never printed: the user's email or username (sha256 fingerprints only, as
services/utils/utterance_log.py does for user text), any row content.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

# Replaces PYTHONPATH=/app (there is no shell to set it in). File-relative, so in
# the image this resolves to /app, and locally to the checkout.
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
if str(_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(_ROOT / "scripts"))

# First character alphanumeric: nothing that could read as a flag reaches a query.
_SAFE = re.compile(r"[A-Za-z0-9][A-Za-z0-9@._+\-]{0,253}")


# ---------------------------------------------------------------------------
# The plan. ORDER IS THE DEPENDENCY ORDER: children before parents, users last.
# ``where`` is a SQL predicate over the step's table. It may use :uid (the
# user's id as text) and the scope arrays resolved once before any write
# (:conv_ids, :todo_ids, :list_ids, :project_ids, :repo_ids, :node_ids,
# :slack_ids). Every column is compared as ``::text`` so the predicate holds
# for UUID, CHAR(36) and VARCHAR owner columns alike (the #1621 lesson: the
# live schema's column types drifted from the model's).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Step:
    table: str
    where: str
    action: str = "delete"  # "delete" | "detach" (UPDATE … SET <detach_column> = NULL)
    detach_column: Optional[str] = None
    why: str = ""


def _own(*cols: str) -> str:
    return " OR ".join(f"{c}::text = :uid" for c in cols)


def _in(col: str, scope: str) -> str:
    return f"{col}::text = ANY(CAST(:{scope} AS text[]))"


PLAN: Tuple[Step, ...] = (
    # --- conversations and everything hanging off them (no FK to users) ---
    Step(
        "conversation_links",
        _in("conversation_id", "conv_ids"),
        why="links between the user's turns",
    ),
    Step(
        "conversation_turns",
        _in("conversation_id", "conv_ids"),
        why="the user's messages and Piper's replies",
    ),
    Step(
        "conversational_memory_entries",
        f"{_own('user_id', 'owner_id')} OR {_in('conversation_id', 'conv_ids')}",
        why="memory of the user's conversations (FK to conversations, no ondelete)",
    ),
    Step(
        "session_activity", _own("owner_id"), why="external artifacts the user's sessions created"
    ),
    Step("conversations", _own("user_id", "owner_id"), why="no FK to users"),
    Step("standup_conversations", _own("user_id", "owner_id"), why="no FK to users"),
    Step("insights", _own("user_id", "owner_id"), why="no FK to users"),
    Step("artifacts", _own("owner_id"), why="no FK to users"),
    Step("ethics_audit_log", _own("user_id"), why="no FK to users; per-user boundary decisions"),
    Step("feedback", _own("user_id", "owner_id"), why="user_id FK has no ondelete"),
    # --- lists and todos (joined inheritance: todo_items.id -> items.id) ---
    Step(
        "list_memberships",
        f"{_own('owner_id')} OR {_in('todo_id', 'todo_ids')} OR {_in('list_id', 'list_ids')}",
        why="references todo_items and lists without ondelete",
    ),
    Step(
        "list_items",
        f"{_own('owner_id')} OR {_in('list_id', 'list_ids')}",
        why="list_id FK has no ondelete",
    ),
    Step(
        "todo_items",
        _own("owner_id"),
        why="owner FK has no ondelete; self-parent FK in one statement",
    ),
    Step(
        "items",
        f"{_in('id', 'todo_ids')} OR {_in('list_id', 'list_ids')}",
        why="base rows of the user's todos (no owner column of their own)",
    ),
    Step("lists", _own("owner_id"), why="owner FK has no ondelete"),
    # --- knowledge graph ---
    Step(
        "knowledge_edges",
        f"{_own('owner_id')} OR {_in('source_node_id', 'node_ids')} OR {_in('target_node_id', 'node_ids')}",
        why="node FKs have no ondelete",
    ),
    Step("knowledge_nodes", _own("owner_id")),
    # --- projects and repositories ---
    Step(
        "project_repository_links",
        f"{_in('project_id', 'project_ids')} OR {_in('repository_id', 'repo_ids')}",
        why="no owner column; FKs to projects and repositories have no ondelete",
    ),
    Step(
        "project_integrations",
        f"{_own('owner_id')} OR {_in('project_id', 'project_ids')}",
        why="owner and project FKs have no ondelete",
    ),
    Step("projects", _own("owner_id")),
    Step("repositories", _own("owner_id"), why="owner FK has no ondelete"),
    # --- content stores (their outside-Postgres halves are cleared before this) ---
    Step(
        "documents", _own("owner_id"), why="owner FK has no ondelete; ChromaDB chunks cleared first"
    ),
    Step(
        "uploaded_files", _own("owner_id"), why="files on disk removed first via the storage seam"
    ),
    # --- connectors, personalization, learning ---
    Step("connector_bindings", _own("owner_id"), why="owner FK has no ondelete"),
    Step("connector_configs", _own("owner_id"), why="owner FK has no ondelete"),
    Step("personality_profiles", _own("user_id", "owner_id"), why="user_id FK has no ondelete"),
    Step("personalization_contexts", _own("owner_id"), why="owner FK has no ondelete"),
    Step("learned_patterns", _own("user_id")),
    Step("learning_settings", _own("user_id")),
    Step("user_trust_profiles", _own("user_id")),
    # --- identity, auth and Slack linking ---
    Step("password_reset_tokens", _own("user_id"), why="user FK has no ondelete"),
    Step("slack_link_codes", _own("user_id"), why="user FK has no ondelete"),
    Step(
        "slack_link_attempts",
        _in("slack_user_id", "slack_ids"),
        why="rate-limit ledger keyed by the user's Slack ids (no FK)",
    ),
    Step("slack_identities", _own("owner_id"), why="owner FK has no ondelete"),
    Step("mcp_oauth_codes", _own("user_id")),
    Step("mcp_oauth_refresh_tokens", _own("user_id")),
    Step("mcp_access_tokens", _own("user_id")),
    Step("token_blacklist", _own("user_id")),
    Step("audit_logs", _own("user_id")),
    Step("user_api_keys", _own("user_id"), why="the user's stored provider keys (#358)"),
    Step(
        "secure_credentials",
        "strpos(name, :uid) > 0",
        why="hosted keychain rows; names carry the user id ({uid}_{provider}_api_key)",
    ),
    Step(
        "invite_tokens",
        _own("used_by_user_id"),
        action="detach",
        detach_column="used_by_user_id",
        why="operator records of minted invites: unlink the user, keep the spent token",
    ),
    Step("users", "id::text = :uid", why="the account itself, last"),
)

# Tables that carry a user-owner column (or an FK to users / to a planned table)
# but are deliberately NOT in the plan. Each needs a written reason; the census
# ratchet (tests/test_architecture_enforcement.py::TestEraseUserCensus2064)
# fails on any user-owned table that is neither planned nor listed here.
ALLOW_LIST: Dict[str, str] = {}

# Column names that make a table user-owned for the census (plus any column
# ending in ``_user_id`` and any FK to users.id).
OWNER_COLUMN_NAMES = frozenset(
    {
        "user_id",
        "owner_id",
        "created_by",
        "added_by",
        "linked_by",
        "used_by_user_id",
        "principal",
        "principal_id",
    }
)

SCOPE_QUERIES: Dict[str, str] = {
    "conv_ids": "SELECT id::text FROM conversations WHERE " + _own("user_id", "owner_id"),
    "todo_ids": "SELECT id::text FROM todo_items WHERE " + _own("owner_id"),
    "list_ids": "SELECT id::text FROM lists WHERE " + _own("owner_id"),
    "project_ids": "SELECT id::text FROM projects WHERE " + _own("owner_id"),
    "repo_ids": "SELECT id::text FROM repositories WHERE " + _own("owner_id"),
    "node_ids": "SELECT id::text FROM knowledge_nodes WHERE " + _own("owner_id"),
    "slack_ids": "SELECT slack_user_id::text FROM slack_identities WHERE " + _own("owner_id"),
}

# Connector credential evidence -> the connector name disconnect_connector takes.
_CREDENTIAL_PROVIDERS = {
    "github": "github",
    "github_token": "github",
    "slack": "slack",
    "slack_bot": "slack",
    "slack_user": "slack",
    "google_calendar": "calendar",
    "calendar": "calendar",
    "notion": "notion",
}


def plan_tables() -> List[str]:
    return [s.table for s in PLAN]


# ---------------------------------------------------------------------------
# The census (shared by the ratchet and the live-schema check)
# ---------------------------------------------------------------------------


def is_owner_column(name: str) -> bool:
    return name in OWNER_COLUMN_NAMES or name.endswith("_user_id")


def user_owned_tables(metadata) -> Dict[str, str]:
    """Every table in ``metadata`` that holds user data, with why it counts.

    A table counts when it has an owner-named column, an FK to users.id, or an
    FK to another table that counts (a child of user data is user data). The
    last rule runs to a fixed point, so grandchildren count too.
    """
    owned: Dict[str, str] = {}
    for t in metadata.tables.values():
        if t.name == "users":
            owned[t.name] = "the account"
            continue
        cols = [c.name for c in t.columns if is_owner_column(c.name)]
        fk_users = [fk.parent.name for fk in t.foreign_keys if fk.column.table.name == "users"]
        if cols or fk_users:
            owned[t.name] = f"owner columns {sorted(set(cols) | set(fk_users))}"
    changed = True
    while changed:
        changed = False
        for t in metadata.tables.values():
            if t.name in owned:
                continue
            parents = sorted({fk.column.table.name for fk in t.foreign_keys} & set(owned))
            if parents:
                owned[t.name] = f"FK to user-owned {parents}"
                changed = True
    return owned


def fk_census(metadata) -> Dict[str, int]:
    """Arch's 10-16 numbers, recomputed: FKs to users by ondelete, and owner
    columns with no FK to users at all."""
    cascade = no_action = 0
    no_fk_cols = 0
    for t in metadata.tables.values():
        fk_cols = set()
        for fk in t.foreign_keys:
            if fk.column.table.name == "users":
                fk_cols.add(fk.parent.name)
                if (fk.ondelete or "").upper() == "CASCADE":
                    cascade += 1
                else:
                    no_action += 1
        for c in t.columns:
            if is_owner_column(c.name) and c.name not in fk_cols and t.name != "users":
                no_fk_cols += 1
    return {"fk_cascade": cascade, "fk_no_ondelete": no_action, "owner_cols_without_fk": no_fk_cols}


def unplanned(owned: Iterable[str]) -> List[str]:
    planned = set(plan_tables()) | set(ALLOW_LIST)
    return sorted(set(owned) - planned)


# ---------------------------------------------------------------------------
# Argument handling (before any connection)
# ---------------------------------------------------------------------------


def fingerprint(value: Optional[str]) -> str:
    if not value:
        return "(none)"
    return hashlib.sha256(value.strip().lower().encode()).hexdigest()[:16]


def _is_uuid(s: str) -> bool:
    try:
        return str(uuid.UUID(s)) == s.lower()
    except ValueError:
        return False


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="erase_user.py",
        description="Count (default) or erase (--erase --confirm <user-id>) one user's data. #2064.",
    )
    parser.add_argument("identifier", help="user id, username or email")
    parser.add_argument("--erase", action="store_true", help="DESTRUCTIVE: erase after counting")
    parser.add_argument("--confirm", help="the user's full id, exactly as the count run printed it")
    args = parser.parse_args(list(argv))
    if not _SAFE.fullmatch(args.identifier):
        parser.exit(
            2,
            "refusing: identifier must start with a letter or digit and use only [A-Za-z0-9@._+-]\n",
        )
    if args.confirm is not None and not args.erase:
        parser.exit(
            2, "refusing: --confirm without --erase (count mode takes only the identifier)\n"
        )
    if args.erase and not args.confirm:
        parser.exit(
            2,
            "refusing: --erase needs --confirm <user-id> (run the count first; it prints the id)\n",
        )
    if args.erase and not _is_uuid(args.confirm):
        parser.exit(2, "refusing: --confirm must be the user's full id (a UUID)\n")
    return args


# ---------------------------------------------------------------------------
# Resolution, scope, counting
# ---------------------------------------------------------------------------


def resolve_user(conn, identifier: str) -> Tuple[str, Optional[str], Optional[str]]:
    """(id, username, email) of exactly one user, or SystemExit."""
    from sqlalchemy import text

    if _is_uuid(identifier):
        rows = conn.execute(
            text("SELECT id::text, username, email FROM users WHERE id::text = :w"),
            {"w": identifier.lower()},
        ).fetchall()
    else:
        rows = conn.execute(
            text(
                "SELECT id::text, username, email FROM users "
                "WHERE lower(username) = lower(:w) OR lower(email) = lower(:w)"
            ),
            {"w": identifier},
        ).fetchall()
    if not rows and _is_uuid(identifier):
        # Idempotency: the account row is already gone (an earlier erase, or a
        # naive delete) but rows keyed by its id may remain. Counting and
        # erasing those leftovers by id is the same plan with users = 0.
        return identifier.lower(), None, None
    if len(rows) != 1:
        raise SystemExit(
            f"refusing: identifier matched {len(rows)} users (needs exactly 1); "
            f"identifier sha256={fingerprint(identifier)}"
        )
    uid, username, email = rows[0]
    return uid.strip(), username, email


def existing_tables(conn) -> set:
    from sqlalchemy import text

    rows = conn.execute(
        text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = current_schema()"
        )
    ).fetchall()
    return {r[0] for r in rows}


def resolve_scope(conn, uid: str, present: set) -> Dict[str, Any]:
    from sqlalchemy import text

    params: Dict[str, Any] = {"uid": uid}
    for key, sql in SCOPE_QUERIES.items():
        table = sql.split(" FROM ", 1)[1].split()[0]
        if table not in present:
            params[key] = []
            continue
        params[key] = [
            r[0].strip() for r in conn.execute(text(sql), {"uid": uid}).fetchall() if r[0]
        ]
    return params


def count_rows(conn, params: Dict[str, Any], present: set) -> Dict[str, Optional[int]]:
    """Rows per planned table (None = table absent from this database)."""
    from sqlalchemy import text

    out: Dict[str, Optional[int]] = {}
    for step in PLAN:
        if step.table not in present:
            out[step.table] = None
            continue
        out[step.table] = conn.execute(
            text(f"SELECT count(*) FROM {step.table} WHERE {step.where}"), params
        ).scalar_one()
    return out


def erase_rows(conn, params: Dict[str, Any], present: set) -> Dict[str, int]:
    """The deletes, in plan order, on ``conn`` (the caller owns the transaction)."""
    from sqlalchemy import text

    out: Dict[str, int] = {}
    for step in PLAN:
        if step.table not in present:
            continue
        if step.action == "detach":
            sql = f"UPDATE {step.table} SET {step.detach_column} = NULL WHERE {step.where}"
        else:
            sql = f"DELETE FROM {step.table} WHERE {step.where}"
        out[step.table] = conn.execute(text(sql), params).rowcount
    return out


@dataclass(frozen=True)
class Preflight:
    """The pre-flight verdict. ``table`` is the plan step whose statement raised;
    ``error`` is the error class (SQLAlchemy's, then the driver's); ``detail``
    names the constraint and the referencing table when the driver reports
    them (schema identifiers only, never row content)."""

    ok: bool
    table: Optional[str] = None
    error: Optional[str] = None
    detail: Optional[str] = None

    def line(self) -> str:
        if self.ok:
            return (
                "pre-flight: would erase cleanly (every planned statement ran and was rolled back)"
            )
        extra = f"; {self.detail}" if self.detail else ""
        return f"pre-flight: would refuse at {self.table} ({self.error}{extra})"


def _error_class(exc: BaseException) -> Tuple[str, Optional[str]]:
    orig = getattr(exc, "orig", None)
    name = type(exc).__name__
    if orig is not None and type(orig).__name__ != name:
        name = f"{name}/{type(orig).__name__}"
    diag = getattr(orig, "diag", None)
    constraint = getattr(diag, "constraint_name", None)
    ref_table = getattr(diag, "table_name", None)
    detail = None
    if constraint or ref_table:
        detail = f"constraint {constraint or '?'} on table {ref_table or '?'}"
    return name, detail


def preflight(conn, params: Dict[str, Any], present: set) -> Preflight:
    """Run the plan's statements on ``conn`` and ROLL BACK, always.

    ``conn`` must not be inside a transaction the caller means to keep: this
    function ends whatever transaction is open on it with a rollback, in a
    ``finally``, whatever happens. It never commits. If the process dies while
    this runs, no COMMIT was ever sent, so Postgres aborts the transaction when
    the connection drops; ``idle_in_transaction_session_timeout`` bounds the
    case where the client hangs without the socket closing.

    ``SET CONSTRAINTS ALL IMMEDIATE`` makes any DEFERRABLE INITIALLY DEFERRED
    constraint fire per statement here, since a rollback never reaches the
    commit-time check where the real erase would meet it.
    """
    from sqlalchemy import text

    try:
        conn.rollback()  # start from a clean transaction (reads before this are kept by nobody)
        conn.execute(text("SET LOCAL idle_in_transaction_session_timeout = '60s'"))
        conn.execute(text("SET CONSTRAINTS ALL IMMEDIATE"))
        for step in PLAN:
            if step.table not in present:
                continue
            if step.action == "detach":
                sql = f"UPDATE {step.table} SET {step.detach_column} = NULL WHERE {step.where}"
            else:
                sql = f"DELETE FROM {step.table} WHERE {step.where}"
            try:
                conn.execute(text(sql), params)
            except Exception as exc:  # noqa: BLE001 — the verdict names it
                error, detail = _error_class(exc)
                return Preflight(ok=False, table=step.table, error=error, detail=detail)
        return Preflight(ok=True)
    finally:
        conn.rollback()


def live_unplanned(conn) -> List[str]:
    """The census on the LIVE schema: tables with an owner-named column or an FK
    to users that the plan does not cover (the model can drift from what a
    migration actually built). Erase refuses while this is non-empty."""
    from sqlalchemy import text

    owners = conn.execute(
        text(
            "SELECT DISTINCT table_name, column_name FROM information_schema.columns "
            "WHERE table_schema = current_schema()"
        )
    ).fetchall()
    found = {t for t, c in owners if is_owner_column(c)}
    fks = conn.execute(
        text(
            "SELECT DISTINCT conrelid::regclass::text FROM pg_constraint "
            "WHERE contype = 'f' AND confrelid = to_regclass('users')"
        )
    ).fetchall()
    found |= {r[0].split(".")[-1].strip('"') for r in fks}
    found.discard("users")
    return unplanned(found)


# ---------------------------------------------------------------------------
# Outside Postgres
# ---------------------------------------------------------------------------


def credential_connectors(conn, uid: str, present: set) -> List[str]:
    """Connectors this user holds a stored credential or binding for."""
    from sqlalchemy import text

    evidence: set = set()
    if "secure_credentials" in present:
        for (name,) in conn.execute(
            text("SELECT name FROM secure_credentials WHERE strpos(name, :uid) > 0"), {"uid": uid}
        ).fetchall():
            stem = name.replace(uid, "").replace("_api_key", "").strip("_")
            evidence.add(stem)
    if "user_api_keys" in present:
        for (provider,) in conn.execute(
            text("SELECT provider FROM user_api_keys WHERE user_id::text = :uid"), {"uid": uid}
        ).fetchall():
            evidence.add(provider)
    for table in ("connector_bindings", "connector_configs"):
        if table in present:
            for (connector,) in conn.execute(
                text(f"SELECT connector FROM {table} WHERE owner_id::text = :uid"), {"uid": uid}
            ).fetchall():
                evidence.add(connector)
    return sorted({_CREDENTIAL_PROVIDERS[e] for e in evidence if e in _CREDENTIAL_PROVIDERS})


def upload_paths(conn, uid: str, present: set) -> List[str]:
    from sqlalchemy import text

    if "uploaded_files" not in present:
        return []
    return [
        p
        for (p,) in conn.execute(
            text(
                "SELECT storage_path FROM uploaded_files "
                "WHERE owner_id::text = :uid AND storage_path IS NOT NULL"
            ),
            {"uid": uid},
        ).fetchall()
    ]


def chroma_base_ids(conn, uid: str, present: set) -> List[str]:
    from sqlalchemy import text

    if "documents" not in present:
        return []
    return [
        b
        for (b,) in conn.execute(
            text("SELECT chromadb_base_id FROM documents WHERE owner_id::text = :uid"), {"uid": uid}
        ).fetchall()
    ]


def user_upload_dir(uid: str, base: Optional[Path] = None) -> Path:
    if not _is_uuid(uid):  # never let anything but a UUID become a path segment
        raise SystemExit("refusing: user id is not a UUID; will not build an upload path from it")
    if base is None:
        from services.file_context.storage import get_upload_base

        base = get_upload_base()
    return Path(base) / uid


def count_files(paths: Sequence[str], user_dir: Path) -> Dict[str, int]:
    known = {str(Path(p)) for p in paths}
    on_disk = sum(1 for p in paths if Path(p).exists())
    extra = 0
    if user_dir.is_dir():
        extra = sum(1 for f in user_dir.rglob("*") if f.is_file() and str(f) not in known)
    return {
        "db_known_on_disk": on_disk,
        "db_known_missing": len(paths) - on_disk,
        "untracked_in_user_dir": extra,
        "user_dir_exists": int(user_dir.is_dir()),
    }


def erase_files(paths: Sequence[str], user_dir: Path) -> Dict[str, int]:
    from services.file_context.storage import delete_file_from_storage

    removed = 0
    for p in paths:
        if delete_file_from_storage(p):
            removed += 1
    swept = 0
    if user_dir.is_dir():
        for f in sorted(user_dir.rglob("*"), key=lambda x: len(x.parts), reverse=True):
            if f.is_file() or f.is_symlink():
                f.unlink()
                swept += 1
            elif f.is_dir():
                f.rmdir()
        user_dir.rmdir()
    return {"removed_via_seam": removed, "swept_from_user_dir": swept}


def _chroma_collection(path: Optional[Path] = None):
    """The app's in-app store, or None when it isn't there. Never creates a store.

    #2244: the store is under PIPER_DATA_DIR when that is set (the volume on Fly);
    otherwise DocumentIngester's ./data/chromadb, read here from the repo root."""
    if path is None:
        from services.infrastructure.data_paths import data_root, document_index_path

        path = document_index_path() if data_root() is not None else _ROOT / "data" / "chromadb"
    if not path.is_dir():
        return None
    import chromadb  # noqa: PLC0415

    client = chromadb.PersistentClient(
        path=str(path), settings=chromadb.config.Settings(anonymized_telemetry=False)
    )
    try:
        # No embedding function: get and delete never embed.
        return client.get_collection(name="pm_knowledge", embedding_function=None)
    except Exception:
        return None


def chroma_chunk_ids(collection, base_ids: Sequence[str]) -> List[str]:
    if collection is None or not base_ids:
        return []
    wanted = set(base_ids)
    ids = collection.get(include=[]).get("ids", [])
    return [i for i in ids if i.rsplit("_chunk_", 1)[0] in wanted]


def _redis_client():
    import redis  # noqa: PLC0415

    client = redis.Redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379"), socket_timeout=3, socket_connect_timeout=3
    )
    client.ping()
    return client


def redis_keys(client, uid: str, conv_ids: Sequence[str]) -> List[bytes]:
    if client is None:
        return []
    keys = set(client.scan_iter(match=f"*{uid}*", count=500))
    for cid in conv_ids:
        keys |= set(client.scan_iter(match=f"*{cid}*", count=500))
    return sorted(keys)


def revoke_grants(uid: str, connectors: Sequence[str], disconnect=None) -> Dict[str, str]:
    """Best effort, per connector: the app's own disconnect (provider-side
    revoke where supported, then the local credential)."""
    if not connectors:
        return {}
    import asyncio

    if disconnect is None:
        from services.connectors.disconnect import disconnect_connector as disconnect

    results: Dict[str, str] = {}
    for c in connectors:
        try:
            asyncio.run(disconnect(uid, c))
            results[c] = "disconnected"
        except Exception as exc:  # noqa: BLE001 — best effort, printed, never silent
            results[c] = f"FAILED ({type(exc).__name__})"
    return results


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


@dataclass
class Census:
    rows: Dict[str, Optional[int]]
    files: Dict[str, int]
    chroma: Optional[int]
    redis: Optional[int]
    connectors: List[str]
    unplanned_live: List[str]

    def total_rows(self) -> int:
        return sum(n for n in self.rows.values() if n)


def take_census(
    conn, uid: str, upload_base: Optional[Path], chroma, redis_client
) -> Tuple[Census, Dict[str, Any]]:
    present = existing_tables(conn)
    params = resolve_scope(conn, uid, present)
    rows = count_rows(conn, params, present)
    paths = upload_paths(conn, uid, present)
    files = count_files(paths, user_upload_dir(uid, upload_base))
    chroma_n = (
        None
        if chroma is None
        else len(chroma_chunk_ids(chroma, chroma_base_ids(conn, uid, present)))
    )
    redis_n = (
        None if redis_client is None else len(redis_keys(redis_client, uid, params["conv_ids"]))
    )
    census = Census(
        rows=rows,
        files=files,
        chroma=chroma_n,
        redis=redis_n,
        connectors=credential_connectors(conn, uid, present),
        unplanned_live=live_unplanned(conn),
    )
    return census, {"present": present, "params": params, "paths": paths}


def format_census(c: Census, heading: str) -> str:
    lines = [f"--- {heading}"]
    lines.append(f"database rows ({len(PLAN)} planned tables, dependency order):")
    for table, n in c.rows.items():
        lines.append(f"  {table}: {'absent' if n is None else n}")
    lines.append(f"  total: {c.total_rows()}")
    lines.append("outside the database:")
    f = c.files
    lines.append(
        f"  upload files: {f['db_known_on_disk']} on disk, {f['db_known_missing']} missing-on-disk, "
        f"{f['untracked_in_user_dir']} untracked in the user's upload dir "
        f"(dir {'present' if f['user_dir_exists'] else 'absent'})"
    )
    lines.append(f"  chromadb chunks: {'store absent' if c.chroma is None else c.chroma}")
    lines.append(f"  redis keys: {'unavailable' if c.redis is None else c.redis}")
    lines.append(
        f"  provider grants (connectors with a stored credential): {', '.join(c.connectors) or 'none'}"
    )
    lines.append(
        "live-schema census: "
        + (
            f"UNPLANNED user tables {c.unplanned_live}"
            if c.unplanned_live
            else "0 unplanned user tables"
        )
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------


def run(
    identifier: str,
    *,
    erase: bool,
    confirm: Optional[str],
    engine,
    upload_base: Optional[Path] = None,
    chroma=None,
    redis_client=None,
    disconnect: Optional[Callable] = None,
    out: Callable[[str], None] = print,
) -> Census:
    with engine.connect() as conn:
        uid, username, email = resolve_user(conn, identifier)
        out(
            f"user: id={uid} · username_sha256={fingerprint(username)} · "
            f"email_sha256={fingerprint(email)}"
        )
        before, ctx = take_census(conn, uid, upload_base, chroma, redis_client)
        conn.rollback()
        verdict = preflight(conn, ctx["params"], ctx["present"])
    out(format_census(before, "COUNT ONLY, nothing written" if not erase else "before erase"))
    out(verdict.line())
    if not erase:
        return before

    if confirm is None or confirm.lower() != uid.lower():
        raise SystemExit("refusing: --confirm does not match this user's id; nothing erased")
    if before.unplanned_live:
        raise SystemExit(
            f"refusing: the live schema has user tables the plan does not cover "
            f"{before.unplanned_live}; extend scripts/erase_user.py PLAN first; nothing erased"
        )
    if not verdict.ok:
        extra = f"; {verdict.detail}" if verdict.detail else ""
        raise SystemExit(
            f"refusing: pre-flight failed at {verdict.table} ({verdict.error}{extra}); "
            f"nothing erased anywhere (another user's row still references this user's "
            f"data, or the plan misses an FK: resolve it, count again, then erase)"
        )

    # 1. provider grants (reads the stored tokens, so before the rows go)
    for c, result in revoke_grants(uid, before.connectors, disconnect).items():
        out(f"provider grant {c}: {result}")
    # 2. upload files via the seam, then the user's upload dir
    with engine.connect() as conn:
        paths = upload_paths(conn, uid, existing_tables(conn))
        conn.rollback()
    files = erase_files(paths, user_upload_dir(uid, upload_base))
    out(
        f"upload files: {files['removed_via_seam']} removed via the storage seam, "
        f"{files['swept_from_user_dir']} swept from the user's upload dir"
    )
    # 3. chromadb chunks
    if chroma is not None:
        with engine.connect() as conn:
            ids = chroma_chunk_ids(chroma, chroma_base_ids(conn, uid, existing_tables(conn)))
            conn.rollback()
        if ids:
            chroma.delete(ids=ids)
        out(f"chromadb chunks: {len(ids)} deleted")
    # 4. Postgres, one transaction
    with engine.begin() as conn:
        present = existing_tables(conn)
        params = resolve_scope(conn, uid, present)
        erased = erase_rows(conn, params, present)
    out(f"database: {sum(erased.values())} rows erased or detached in one transaction")
    # 5. redis caches
    if redis_client is not None:
        keys = redis_keys(redis_client, uid, ctx["params"]["conv_ids"])
        if keys:
            redis_client.delete(*keys)
        out(f"redis keys: {len(keys)} deleted")

    # The same shape of counts, after. The user row is gone, so count by id.
    with engine.connect() as conn:
        after, _ = take_census(conn, uid, upload_base, chroma, redis_client)
        conn.rollback()
    out(format_census(after, "after erase"))
    return after


def _engine():
    from prod_db import _database_url, _redacted  # noqa: PLC0415
    from sqlalchemy import create_engine  # noqa: PLC0415

    url, source = _database_url()
    print(f"--- target: {_redacted(url)}  (resolved via {source})")
    return create_engine(url)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    try:
        redis_client = _redis_client()
    except Exception:  # noqa: BLE001 — reported as "unavailable" in the census
        redis_client = None
    try:
        chroma = _chroma_collection()
    except Exception:  # noqa: BLE001 — reported as "store absent"
        chroma = None
    print(f"--- mode: {'ERASE' if args.erase else 'COUNT ONLY'}")
    after = run(
        args.identifier,
        erase=args.erase,
        confirm=args.confirm,
        engine=_engine(),
        chroma=chroma,
        redis_client=redis_client,
    )
    if args.erase and after.total_rows():
        print(f"!!! {after.total_rows()} rows remain after erase; rerun (idempotent) and report")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
