"""
Create a test user that can actually log in: a local-dev user by default, or a
staging user with ``--staging`` when run inside the staging app's container.

Ported 2026-09-22 (#1853): the original imported `AlphaUser`, a model deleted in
the #262 unification (ImportError since), and predated password auth entirely —
its users could never pass `/api/v1/auth/login`. This version writes the current
`User` model with a real bcrypt hash via `PasswordService`, so the account works
end-to-end against a running server (the exact need #1793's live spot-check had
to inline).

Where it runs (#2238, xian 2026-11-03: "provision test accounts directly in the
staging database"):

* local (default): only when no ``DATABASE_URL`` is set, ``FLY_APP_NAME`` is unset
  and ``POSTGRES_HOST`` is local. The old guard read ``POSTGRES_HOST`` alone, which
  a Fly container never sets, so it would have run against any hosted database.
* ``--staging``: only when ``FLY_APP_NAME`` is the staging app (the same test
  ``integration_status_service`` uses). Run by a person, in session, through
  ``fly machine exec <machine> -a piper-morgan-staging "python /app/scripts/create_test_alpha_user.py --username <name> --staging"``.
* alpha (``FLY_APP_NAME=piper-morgan``) is refused on both paths: hosted alpha
  accounts come only through the invite mint (`scripts/mint_prod_invite.sh`).

Usage (local):
    POSTGRES_PORT=5433 venv/bin/python scripts/create_test_alpha_user.py \
        --username dev-tester [--email dev-tester@test.local] [--password ...]

Prints the password ONCE to stdout (never stored anywhere else). Idempotent:
an existing username gets its password reset rather than a duplicate row.

Concept: docs/internal/operations/staging-fly-setup-2026-09-22.md
"""

import argparse
import asyncio
import os
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select  # noqa: E402

from services.auth.password_service import PasswordService  # noqa: E402
from services.database.connection import db  # noqa: E402
from services.database.models import User  # noqa: E402

STAGING_APP_NAME = "piper-morgan-staging"  # services.integrations.integration_status_service
_LOCAL_HOSTS = ("localhost", "127.0.0.1", "::1")


def target_for(env, staging: bool) -> tuple[str | None, str]:
    """``(target, reason)``: ``"local"`` or ``"staging"`` when the run is allowed,
    ``None`` with the reason when it is refused. Pure: reads only ``env``."""
    app = env.get("FLY_APP_NAME")
    if staging:
        if app == STAGING_APP_NAME:
            return "staging", f"FLY_APP_NAME is {STAGING_APP_NAME}"
        return None, (
            f"--staging runs only inside the {STAGING_APP_NAME} app; FLY_APP_NAME is {app!r}"
        )
    if app is not None or env.get("DATABASE_URL"):
        return None, (
            "a hosted database is configured (FLY_APP_NAME or DATABASE_URL set); without "
            "--staging this script is local-dev only, and alpha is never a target"
        )
    host = env.get("POSTGRES_HOST", "localhost")
    if host not in _LOCAL_HOSTS:
        return None, f"POSTGRES_HOST={host!r} is not local"
    return "local", f"POSTGRES_HOST={host!r}"


async def create_test_user(
    username: str, email: str, password: str, *, staging: bool = False
) -> str | None:
    target, reason = target_for(os.environ, staging)
    if target is None:
        print(f"❌ Refusing: {reason}.")
        return None

    await db.initialize()
    password_hash = PasswordService().hash_password(password)

    async with await db.get_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        created = user is None
        if user is None:
            user = User(
                username=username,
                email=email,
                is_active=True,
                is_verified=True,
                is_alpha=True,
            )
            session.add(user)
        user.password_hash = password_hash
        await session.commit()
        await session.refresh(user)

        print(f"✅ {'Created' if created else 'Password reset for'} user '{username}'")
        print(f"   User ID: {user.id}")
        print(f"   Email:   {user.email}")
        print(f"   Password (shown once): {password}")
        print()
        if target == "staging":
            print("   Sign in: https://piper-morgan-staging.fly.dev (Sign In, not Create Account)")
        else:
            print("   Verify:  curl -s -X POST http://localhost:8001/api/v1/auth/login \\")
            print(f'              -d "username={username}&password=<the password above>"')
        return str(user.id)


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a login-capable test user (local by default, --staging inside the staging app)"
    )
    parser.add_argument(
        "--username", required=True, help="Username (required — no default identity)"
    )
    parser.add_argument("--email", default=None, help="Email (default: <username>@test.local)")
    parser.add_argument(
        "--password",
        default=None,
        help="Password (default: a generated random one, printed once)",
    )
    parser.add_argument(
        "--staging",
        action="store_true",
        help="Allow a run inside the staging app's container (FLY_APP_NAME must be "
        f"{STAGING_APP_NAME}); alpha is refused either way",
    )
    args = parser.parse_args()

    email = args.email or f"{args.username}@test.local"
    password = args.password or ("Dev-" + secrets.token_hex(8))

    result = await create_test_user(args.username, email, password, staging=args.staging)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    asyncio.run(main())
