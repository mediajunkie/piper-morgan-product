"""
Create a LOCAL-DEV test user that can actually log in.

Ported 2026-09-22 (#1853): the original imported `AlphaUser`, a model deleted in
the #262 unification (ImportError since), and predated password auth entirely —
its users could never pass `/api/v1/auth/login`. This version writes the current
`User` model with a real bcrypt hash via `PasswordService`, so the account works
end-to-end against a running local server (the exact need #1793's live
spot-check had to inline).

LOCAL DEVELOPMENT ONLY — for hosted alpha, invites go through the blessed mint
path (`scripts/mint_prod_invite.sh`, trust-zone split per the runbooks). This
script refuses unless the DB it resolves to looks local.

Usage:
    POSTGRES_PORT=5433 venv/bin/python scripts/create_test_alpha_user.py \
        --username dev-tester [--email dev-tester@test.local] [--password ...]

Prints the password ONCE to stdout (never stored anywhere else). Idempotent:
an existing username gets its password reset rather than a duplicate row.
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


def _looks_local() -> bool:
    host = os.environ.get("POSTGRES_HOST", "localhost")
    return host in ("localhost", "127.0.0.1", "::1")


async def create_test_user(username: str, email: str, password: str) -> str | None:
    if not _looks_local():
        print("❌ Refusing: POSTGRES_HOST is not local. This script is local-dev only.")
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
        print("   Verify:  curl -s -X POST http://localhost:8001/api/v1/auth/login \\")
        print(f'              -d "username={username}&password=<the password above>"')
        return str(user.id)


async def main() -> None:
    parser = argparse.ArgumentParser(description="Create a local-dev test user (login-capable)")
    parser.add_argument(
        "--username", required=True, help="Username (required — no default identity)"
    )
    parser.add_argument("--email", default=None, help="Email (default: <username>@test.local)")
    parser.add_argument(
        "--password",
        default=None,
        help="Password (default: a generated random one, printed once)",
    )
    args = parser.parse_args()

    email = args.email or f"{args.username}@test.local"
    password = args.password or ("Dev-" + secrets.token_hex(8))

    result = await create_test_user(args.username, email, password)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    asyncio.run(main())
