"""Guard (#1452 class, added 2026-08-03): the user-cleanup helpers rot silently
when a new table gains an FK to users — fresh_database's list predated half the
schema once (#1452) and the three #1466 slack tables rotted it again the same
week the comment claimed it was derived. This test DERIVES the FK-to-users
table set from information_schema at runtime and fails the build until every
such table is either handled in BOTH helpers or explicitly allowlisted with a
reason. Join-by-existing: a new FK table cannot ship without a cleanup decision.
"""
import re

import pytest
from sqlalchemy import text

# Tables with an FK to users that the PER-USER helper deliberately does not
# delete from, each with the reason (the auditable-allowlist shape).
PER_USER_ALLOWLIST = {
    "invite_tokens": "used_by_user_id is NULLed, not deleted (token survives its redeemer)",
    "slack_link_attempts": "no user FK — rate-limit ledger keyed by Slack ids",
}


def _conftest_source():
    import tests.conftest as c
    import inspect
    return inspect.getsource(c)


@pytest.mark.asyncio
@pytest.mark.smoke
async def test_every_users_fk_table_is_covered_by_cleanup_helpers(db_session):
    rows = (
        await db_session.execute(
            text(
                """
                SELECT DISTINCT tc.table_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.constraint_column_usage ccu
                  ON tc.constraint_name = ccu.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND ccu.table_name = 'users'
                """
            )
        )
    ).scalars().all()
    src = _conftest_source()
    missing = []
    for tbl in rows:
        handled = re.search(rf"(DELETE FROM|UPDATE) {tbl}\b", src)
        allowlisted = tbl in PER_USER_ALLOWLIST
        if not handled and not allowlisted:
            missing.append(tbl)
    assert not missing, (
        f"Tables with an FK to users but NO cleanup handling in tests/conftest.py "
        f"(fresh_database + delete_test_user_fully) and no allowlist reason: {missing}. "
        f"Add DELETE/UPDATE statements to both helpers (verify column names/types "
        f"against information_schema first — do not guess) or allowlist with a reason."
    )
