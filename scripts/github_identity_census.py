#!/usr/bin/env python3
"""#2266 — read-only census of GitHub identity state (and, with --verify-calendar, Calendar's,
#2283), for the operator, in the container.

Written for the 2026-11-04 report that a beta tester's GitHub connector reached xian's
repositories as mediajunkie. It answers, with counts and ids only, the questions the
incident needs answered server-side:

1. GitHub connector bindings by status, and for every BOUND binding whether its stored
   OAuth grant is READABLE, MISSING (no row) or UNREADABLE (a row whose secret cannot be
   decrypted). Before the #2266 guard, MISSING and UNREADABLE sent the sidecar an
   unauthenticated request.
2. Stored GitHub credentials by kind (OAuth grant rows, personal-token rows), counts only.
3. Accounts whose saved default repository belongs to an owner you name (``--owner``),
   by account id: the #1590 recovery or a deployment default could have pointed a
   newly connected account at someone else's repository.
5. With ``--verify-logins`` (Exec's check 2, 2026-11-04 13:17): for every bound
   binding whose grant is readable, ask GitHub ``GET /user`` with that grant and report,
   counts only, how many grants resolve to the operator's login (``--operator-login``,
   default mediajunkie) under an account other than the operator's
   (``--operator-user-id``), and how many resolve to some other login. Any crossing
   count above zero is a real credential crossing. No login other than the operator's is
   printed; the grant is never printed.
4. Consequential GitHub write rows since ``--since``: by account id, site, status and the
   repository owner the write targeted. Owners not named with ``--owner`` are masked as
   ``other-N`` (stable within one run), so no outside person's handle is printed.

It never prints a secret, a token, an email or a name. It writes nothing. Run inside the
alpha container, where the app's own database configuration applies:

    fly machine exec <machine-id> "python /app/scripts/github_identity_census.py --since 2026-10-16 --owner mediajunkie --owner dinp-machine" -a piper-morgan

With ``--user-email <the tester's sign-in email>`` it first prints that one account's
binding, grant state, credential rows and GitHub audit counts, by id, never the email.

Locally: ``POSTGRES_PORT=5433 venv/bin/python scripts/github_identity_census.py``.

Concept: docs/internal/operations/github-and-tooling-gotchas.md
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text  # noqa: E402

from services.database.connection import db  # noqa: E402

OAUTH_PROVIDER = "github_mcp_oauth"  # ConnectorGrantStore's provider key for GitHub
PAT_PROVIDER = "github"


def _redacted_target() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        host = url.split("@")[-1].split("/")[0]
        return f"DATABASE_URL host={host}"
    return f"POSTGRES_HOST={os.getenv('POSTGRES_HOST', 'localhost')} db={os.getenv('POSTGRES_DB', 'piper_morgan')}"


class _Mask:
    """Stable per-run masking of repository owners not named on the command line."""

    def __init__(self, shown: set[str]) -> None:
        self._shown = {s.lower() for s in shown}
        self._seen: dict[str, str] = {}

    def __call__(self, owner: str | None) -> str:
        if not owner:
            return "(none)"
        if owner.lower() in self._shown:
            return owner
        if owner not in self._seen:
            self._seen[owner] = f"other-{len(self._seen) + 1}"
        return self._seen[owner]


async def _grant_state(session, owner_id: str) -> str:
    from services.security.user_api_key_service import UserAPIKeyService, UserKeyReadFailed

    try:
        secret = await UserAPIKeyService().retrieve_user_key_strict(
            session, str(owner_id), OAUTH_PROVIDER
        )
    except UserKeyReadFailed:
        return "UNREADABLE"
    except Exception as exc:  # a database error is reported as such, never as absence
        return f"ERROR:{type(exc).__name__}"
    return "READABLE" if secret else "MISSING"


async def _focus_account(session, email: str, mask: _Mask) -> None:
    """One account, by its sign-in email (never printed): its id, binding, grant state,
    credential rows, saved default repository owner and GitHub audit rows, counts only."""
    row = (
        await session.execute(
            text("SELECT id FROM users WHERE lower(email) = lower(:e)"), {"e": email}
        )
    ).first()
    if row is None:
        print("0. focus account: no user row for that email")
        print()
        return
    uid = str(row.id)
    print(f"0. focus account {uid} (looked up by email; the email is not printed)")
    b = (
        await session.execute(
            text(
                "SELECT status FROM connector_bindings WHERE connector = 'github' AND owner_id = CAST(:u AS uuid)"
            ),
            {"u": uid},
        )
    ).first()
    print(f"   github binding: {b.status if b else 'none'}")
    if b and b.status == "bound":
        print(f"   grant state: {await _grant_state(session, uid)}")
    keys = (
        await session.execute(
            text(
                "SELECT provider, is_active, count(*) AS n FROM user_api_keys "
                "WHERE user_id = CAST(:u AS uuid) AND provider IN (:oauth, :pat) GROUP BY provider, is_active"
            ),
            {"u": uid, "oauth": OAUTH_PROVIDER, "pat": PAT_PROVIDER},
        )
    ).all()
    print(f"   credential rows: {[(k.provider, k.is_active, k.n) for k in keys] or 'none'}")
    cfg = (
        await session.execute(
            text(
                "SELECT config->>'default_repo' AS default_repo, config->>'github_username' AS handle "
                "FROM connector_configs WHERE connector = 'github' AND owner_id = CAST(:u AS uuid)"
            ),
            {"u": uid},
        )
    ).first()
    if cfg:
        owner = (cfg.default_repo or "").split("/")[0]
        print(
            f"   saved default repository owner: {mask(owner) if owner else '(none)'} · handle set: {bool(cfg.handle)}"
        )
    else:
        print("   connector config: none")
    audit = (
        await session.execute(
            text(
                "SELECT event_type, action, status, count(*) AS n FROM audit_logs "
                "WHERE user_id = CAST(:u AS uuid) AND action LIKE 'github.%' "
                "GROUP BY event_type, action, status ORDER BY 1, 2, 3"
            ),
            {"u": uid},
        )
    ).all()
    print(
        f"   GitHub audit rows (any date): {[(a.event_type, a.action, a.status, a.n) for a in audit] or 'none'}"
    )
    print()


async def _login_for_grant(grant: str) -> str | None:
    """GitHub's login for a bearer, or None when GitHub does not accept it. The bearer is
    sent to api.github.com only; nothing is printed or stored."""
    import aiohttp

    try:
        async with aiohttp.ClientSession() as http:
            async with http.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {grant}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
            ) as response:
                if response.status != 200:
                    return None
                return (await response.json()).get("login")
    except Exception:
        return None


async def _verify_logins(session, operator_login: str, operator_user_id: str | None) -> None:
    from services.security.user_api_key_service import UserAPIKeyService, UserKeyReadFailed

    rows = (
        await session.execute(
            text(
                "SELECT owner_id FROM connector_bindings WHERE connector = 'github' AND status = 'bound'"
            )
        )
    ).all()
    counts = Counter()
    crossing_accounts: list[str] = []
    for r in rows:
        try:
            grant = await UserAPIKeyService().retrieve_user_key_strict(
                session, str(r.owner_id), OAUTH_PROVIDER
            )
        except UserKeyReadFailed:
            counts["grant unreadable"] += 1
            continue
        if not grant:
            counts["grant missing"] += 1
            continue
        # #2342: the stored value is a classic token or a GitHub App grant record. The
        # bearer for an App grant is its access token, never the record.
        from services.mcp.consumer.github_app_grant import GrantRecordDamaged, classify

        try:
            app_grant = classify(grant)
        except GrantRecordDamaged:
            counts["grant unreadable"] += 1
            continue
        if app_grant is not None:
            grant = app_grant.access_token
        login = await _login_for_grant(grant)
        if login is None:
            counts["GitHub rejected the grant"] += 1
        elif login.lower() == operator_login.lower():
            if operator_user_id and str(r.owner_id) == operator_user_id:
                counts["operator's own account -> operator login"] += 1
            else:
                counts["OTHER account -> operator login (CROSSING)"] += 1
                crossing_accounts.append(str(r.owner_id))
        else:
            counts["another login (not printed)"] += 1
    print(f"5. grant logins verified with GitHub: {len(rows)} bound bindings · {dict(counts)}")
    for a in crossing_accounts:
        print(f"   CROSSING: account {a} holds a grant that GitHub says is {operator_login}")
    print()


async def _google_email_for_refresh_token(refresh_token: str) -> str | None:
    """The Google account a stored Calendar refresh token opens, or None when Google does
    not accept it. Refreshes once (Google keeps the refresh token) and reads the userinfo
    email; nothing is printed or stored."""
    from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

    try:
        handler = GoogleCalendarOAuthHandler()
        tokens = await handler.refresh_access_token(refresh_token)
        if not tokens or not tokens.access_token:
            return None
        info = await handler._get_user_info(tokens.access_token)
        email = (info or {}).get("email")
        return str(email).strip().lower() if email else None
    except Exception:
        return None


async def _verify_calendar(session) -> None:
    """#2283 (Arch 2026-11-04 21:29): the Calendar counterpart of section 5. For every Piper
    account with a stored Calendar token, the Google account it opens, compared with that
    account's own sign-in email and with every OTHER Piper account's email. A Google account
    of the person's own that differs from their Piper email is not a crossing; a Google
    account whose email is another Piper account's is. Counts and crossing account ids only,
    never an address."""
    from services.infrastructure.keychain_service import KeychainService

    users = (await session.execute(text("SELECT id, email FROM users"))).all()
    email_owner = {str(u.email).strip().lower(): str(u.id) for u in users if u.email}
    keychain = KeychainService()
    counts = Counter()
    crossing: list[tuple[str, str]] = []
    for u in users:
        try:
            refresh = await keychain.aget_api_key(f"google_calendar_{u.id}")
        except Exception:
            counts["token unreadable"] += 1
            continue
        if not refresh:
            continue
        counts["accounts with a stored Calendar token"] += 1
        google = await _google_email_for_refresh_token(refresh)
        own = str(u.email).strip().lower() if u.email else None
        if google is None:
            counts["Google rejected the token"] += 1
        elif own and google == own:
            counts["opens its own sign-in email"] += 1
        elif google in email_owner and email_owner[google] != str(u.id):
            counts["opens ANOTHER Piper account email (CROSSING)"] += 1
            crossing.append((str(u.id), email_owner[google]))
        else:
            counts["opens another Google account of no Piper account (not printed)"] += 1
    print(f"6. Calendar tokens verified with Google: {len(users)} accounts read · {dict(counts)}")
    for holder, other in crossing:
        print(f"   CROSSING: account {holder} holds a Calendar token for account {other}'s email")
    print()


async def run(
    since: date,
    mask: _Mask,
    focus_email: str | None = None,
    verify_logins: bool = False,
    verify_calendar: bool = False,
    operator_login: str = "mediajunkie",
    operator_user_id: str | None = None,
) -> int:
    await db.initialize()
    async with await db.get_session() as session:
        if focus_email:
            await _focus_account(session, focus_email, mask)
        print(f"GitHub identity census · target {_redacted_target()} · writes since {since}")
        print()

        # 1. bindings and grant state
        rows = (
            await session.execute(
                text(
                    "SELECT owner_id, status FROM connector_bindings "
                    "WHERE connector = 'github' ORDER BY status, owner_id"
                )
            )
        ).all()
        by_status = Counter(r.status for r in rows)
        print(f"1. GitHub bindings: {len(rows)} · by status: {dict(by_status)}")
        bound = [r for r in rows if r.status == "bound"]
        states = Counter()
        for r in bound:
            state = await _grant_state(session, r.owner_id)
            states[state] += 1
            if state != "READABLE":
                print(f"   bound binding with grant {state}: account {r.owner_id}")
        print(f"   bound bindings: {len(bound)} · grant state: {dict(states)}")
        print()

        # 2. stored credentials by kind
        creds = (
            await session.execute(
                text(
                    "SELECT provider, is_active, count(*) AS n FROM user_api_keys "
                    "WHERE provider IN (:oauth, :pat) GROUP BY provider, is_active"
                ),
                {"oauth": OAUTH_PROVIDER, "pat": PAT_PROVIDER},
            )
        ).all()
        print("2. stored GitHub credentials (rows, no values):")
        for c in creds:
            print(f"   provider={c.provider} active={c.is_active}: {c.n}")
        print()

        # 3. saved default repositories by owner
        cfgs = (
            await session.execute(
                text(
                    "SELECT owner_id, config->>'default_repo' AS default_repo "
                    "FROM connector_configs WHERE connector = 'github' "
                    "AND config->>'default_repo' IS NOT NULL"
                )
            )
        ).all()
        print(f"3. accounts with a saved GitHub default repository: {len(cfgs)}")
        owners = Counter()
        for c in cfgs:
            owner = (c.default_repo or "").split("/")[0]
            owners[mask(owner)] += 1
        print(f"   by repository owner: {dict(owners)}")
        for c in cfgs:
            owner = (c.default_repo or "").split("/")[0]
            if mask(owner) == owner:  # a named owner: list the accounts pointing at it
                print(f"   account {c.owner_id} -> owner {owner}")
        print()

        if verify_logins:
            await _verify_logins(session, operator_login, operator_user_id)
        if verify_calendar:
            await _verify_calendar(session)

        # 4. consequential GitHub writes since the date
        writes = (
            await session.execute(
                text(
                    "SELECT user_id, action, status, details->>'owner' AS owner, "
                    "created_at FROM audit_logs "
                    "WHERE event_type = 'consequential' AND action LIKE 'github.%' "
                    "AND created_at >= :since ORDER BY created_at"
                ),
                {"since": datetime(since.year, since.month, since.day, tzinfo=timezone.utc)},
            )
        ).all()
        print(f"4. consequential GitHub write rows since {since}: {len(writes)}")
        per_account: dict[str, Counter] = defaultdict(Counter)
        for w in writes:
            per_account[str(w.user_id)][(w.action, w.status, mask(w.owner))] += 1
        for account, counter in per_account.items():
            print(f"   account {account}:")
            for (action, status, owner), n in sorted(counter.items()):
                print(f"      {action} status={status} owner={owner}: {n}")
        print()
        print(
            "Read: a bound binding with a MISSING or UNREADABLE grant is the #2266 condition; "
            "an account other than the operator's writing to a named owner's repository is "
            "the blast radius; nothing above is a secret, an email or a name."
        )
    return 0


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--since", default="2026-10-16", help="YYYY-MM-DD for the writes census")
    p.add_argument(
        "--user-email",
        default=None,
        help="focus one account by its sign-in email (looked up, never printed): its binding, "
        "grant state, credential rows and GitHub audit counts",
    )
    p.add_argument(
        "--verify-logins",
        action="store_true",
        help="ask GitHub which login each readable grant belongs to (counts only; Exec's check 2)",
    )
    p.add_argument(
        "--verify-calendar",
        action="store_true",
        help="ask Google which account each stored Calendar token opens (counts and crossings only)",
    )
    p.add_argument("--operator-login", default="mediajunkie", help="the operator's GitHub login")
    p.add_argument(
        "--operator-user-id",
        default=None,
        help="the operator's Piper account id (uuid), so its own grant is not a crossing",
    )
    p.add_argument(
        "--owner",
        action="append",
        default=None,
        help="a repository owner to print unmasked (repeatable); default: mediajunkie, dinp-machine",
    )
    args = p.parse_args(argv)
    since = date.fromisoformat(args.since)
    shown = set(args.owner or ["mediajunkie", "dinp-machine"])
    sys.exit(
        asyncio.run(
            run(
                since,
                _Mask(shown),
                args.user_email,
                verify_logins=args.verify_logins,
                verify_calendar=args.verify_calendar,
                operator_login=args.operator_login,
                operator_user_id=args.operator_user_id,
            )
        )
    )


if __name__ == "__main__":
    main()
