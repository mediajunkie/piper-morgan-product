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
    import inspect

    import tests.conftest as c

    return inspect.getsource(c)


@pytest.mark.asyncio
@pytest.mark.smoke
async def test_every_users_fk_table_is_covered_by_cleanup_helpers(db_session):
    rows = (
        (
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
        )
        .scalars()
        .all()
    )
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


# #2254: base items (item_type = 'item') have no owner column, so the two helpers
# never deleted them; "DELETE FROM lists" left them dangling before s2014items (540
# rows on the shared dev DB, 10-31 and 11-01) and at head fails outright, because
# the FK's SET NULL trips ck_items_base_item_has_list and the rollback leaves the
# lists and the user behind. Both pins below are red on the pre-fix helpers.


def _statement_line(src: str, statement: str) -> int:
    """Offset of the statement as a list entry (a quoted line), not a mention in a comment."""
    match = re.search(rf'^\s*"{re.escape(statement)}', src, re.M)
    assert match, statement
    return match.start()


@pytest.mark.smoke
def test_both_helpers_delete_base_items_before_lists():
    src = _conftest_source()
    blanket = src[src.index("async def fresh_database") : src.index("class TransitionState")]
    per_user = src[src.index("async def delete_test_user_fully") :]
    assert _statement_line(blanket, "DELETE FROM items") < _statement_line(
        blanket, "DELETE FROM lists"
    )
    assert _statement_line(
        per_user, "DELETE FROM items WHERE list_id IN (SELECT id FROM lists WHERE owner_id"
    ) < _statement_line(per_user, "DELETE FROM lists WHERE owner_id")


@pytest.mark.asyncio
@pytest.mark.smoke
async def test_per_user_cleanup_removes_a_base_item_its_list_and_the_user(db_session):
    """At head a list with a base item in it cannot be deleted before the item: the
    statement fails, is rolled back, and the user delete fails after it on lists'
    FK. The helper has to take the item first, and leave none of the three."""
    from uuid import uuid4

    from tests.conftest import delete_test_user_fully

    uid, lid, iid = str(uuid4()), str(uuid4()), str(uuid4())
    await db_session.execute(
        text(
            "INSERT INTO users (id, username, email, password_hash, is_active, is_verified, "
            "created_at, updated_at, role, is_alpha) VALUES (CAST(:u AS uuid), :n, :e, '', "
            "true, false, now(), now(), 'user', true)"
        ),
        {"u": uid, "n": f"cleanup_{uid[:8]}", "e": f"cleanup_{uid[:8]}@example.com"},
    )
    await db_session.execute(
        text(
            "INSERT INTO lists (id, name, owner_id, item_type, created_at, updated_at) "
            "VALUES (:l, 'cleanup-2254', CAST(:u AS uuid), 'item', now(), now())"
        ),
        {"l": lid, "u": uid},
    )
    await db_session.execute(
        text(
            "INSERT INTO items (id, text, item_type, list_id, position, created_at, updated_at) "
            "VALUES (:i, 'base item', 'item', :l, 0, now(), now())"
        ),
        {"i": iid, "l": lid},
    )
    await db_session.commit()

    await delete_test_user_fully(db_session, uid)

    left = {
        "items": await db_session.scalar(
            text("SELECT count(*) FROM items WHERE id = :i"), {"i": iid}
        ),
        "lists": await db_session.scalar(
            text("SELECT count(*) FROM lists WHERE id = :l"), {"l": lid}
        ),
        "users": await db_session.scalar(
            text("SELECT count(*) FROM users WHERE id = CAST(:u AS uuid)"), {"u": uid}
        ),
    }
    assert left == {"items": 0, "lists": 0, "users": 0}, left
