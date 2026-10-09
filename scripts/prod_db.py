"""prod_db.py — the ONE production-DB URL resolution shared by the ops payloads
(mint_invite_tokens, burn_invite_tokens, mint_mcp_token, prod_user_lookup).

Lifted out of mint_invite_tokens.py (Arch, 2026-10-09) so a payload that only
needs the URL does not inherit another script's import-time side effects. This
module has none: no dotenv load, no environment defaults — it reads the app's own
config at call time and refuses the localhost fallback in production.
"""

from __future__ import annotations

import os


def _to_sync_url(url: str) -> str:
    """Turn the app's async URL into one psycopg2 accepts.

    Two independent differences, both of which bite:
      * driver token: ``postgresql+asyncpg://`` -> ``postgresql://``
      * TLS spelling: asyncpg's ``?ssl=X`` -> libpq's ``?sslmode=X``

    The second is the non-obvious one — psycopg2 does not ignore the foreign
    key, it raises ``invalid connection option "ssl"`` and the connection never
    opens.
    """
    from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit  # noqa: PLC0415

    parts = urlsplit(url.replace("+asyncpg", ""))
    q = [(("sslmode" if k == "ssl" else k), v) for k, v in parse_qsl(parts.query)]
    return urlunsplit(parts._replace(query=urlencode(q)))


def _database_url() -> tuple[str, str]:
    """Resolve the DB URL the way the APP does, falling back to POSTGRES_*.

    Returns (url, source) — source is printed so the operator always sees which
    database is about to be written to.

    Why this isn't just the POSTGRES_* construction it used to be: those
    defaults point at localhost:5433, i.e. the DEV database. Run from a
    worktree that is correct; run anywhere else it silently mints tokens the
    alpha tester cannot use, and the output looks identical to success. The
    2026-07 batch worked around this with a throwaway script that called
    ``db._build_database_url()``; doing it here instead means there is one
    mint path and it is right in both environments.
    """
    try:
        from services.database.connection import db  # noqa: PLC0415

        url = db._build_database_url()
        # The app speaks asyncpg; this script is sync (psycopg2). Stripping the
        # driver is NOT enough: the two drivers spell TLS differently —
        # asyncpg takes ?ssl=…, libpq/psycopg2 takes ?sslmode=…, and psycopg2
        # hard-errors on the foreign key ("invalid connection option 'ssl'").
        return _to_sync_url(url), "app config (services.database.connection)"
    except Exception as exc:  # noqa: BLE001 — fall back LOUDLY, never silently
        # A silent fallback here is the whole hazard: it degrades to localhost,
        # which in production means "mint into a database that isn't the one
        # the app uses" — and the run still looks like a success. So: say what
        # failed, and REFUSE outright when we can see we're in production.
        print(f"!!! app-config DB resolution FAILED: {type(exc).__name__}: {exc}")
        if os.getenv("PIPER_ENVIRONMENT", "").lower() == "production":
            raise SystemExit(
                "REFUSING to fall back to POSTGRES_* defaults in production — "
                "that path points at localhost and would mint unusable tokens. "
                "Fix the resolution error above instead."
            ) from exc
        print("!!! falling back to POSTGRES_* env (dev-only path)")
        u = os.getenv("POSTGRES_USER", "piper")
        p = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
        h = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5433")
        d = os.getenv("POSTGRES_DB", "piper_morgan")
        return (
            f"postgresql+psycopg2://{u}:{p}@{h}:{port}/{d}",
            "POSTGRES_* env fallback",
        )


def _redacted(url: str) -> str:
    """host:port/db only — never the password, this gets printed."""
    tail = url.rsplit("@", 1)[-1]
    return tail if "@" not in url else tail
