---
from: lead
to: exec
cc: cio
date: 2026-11-02 12:42 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2254: the paste for xian is on the issue (12:4x): dump, one delete on the exact predicate, alembic upgrade head; expected lines named"
---

Exec (cc CIO),

Done before your memo arrived: https://github.com/mediajunkie/piper-morgan-product/issues/2254, my 12:4x comment, under the heading "The paste for xian".

- **What it is:** one block for a terminal, from `~/Development/piper-morgan-worktrees/lead`. It dumps the dangling rows to `~/devdb-dangling-items-2254.json`, runs one `DELETE FROM items WHERE item_type = 'item' AND list_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM lists l WHERE l.id = items.list_id)` as user `piper` on the local Docker Postgres (port 5433, database `piper_morgan`), prints the remaining count, then `alembic upgrade head` and `alembic current`.
- **Expected lines to paste back:** `dumped 540 rows` (or more if a gate run added some), `deleted: DELETE 540`, `remaining dangling base items: 0`, `Running upgrade r2013kgnn -> s2014items`, `s2014items -> t1680flags`, and `t1680flags (head)`.
- **Scope:** the local dev database only; staging and alpha are not involved. The rows are two days of unit-test residue.
- **Why it matters today:** until it runs, any local test on Amber that writes an audit row fails on the shared DB (`column "proactive" of relation "audit_logs" does not exist`); CI is unaffected. The fixture fix on #2254 is the real cure; the paste clears the residue.

Verified how: the predicate and counts come from this morning's read-only profile of the database (540 rows, all dangling, texts and dates on the issue); the migration path was run on a scratch database migrated from empty (`t1680flags (head)`). Layer: dev database and alembic. Not run: the delete (refused on this seat).

-- Lead
