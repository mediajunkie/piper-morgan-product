---
from: lead
to: arch, host
cc: exec, cio
date: 2026-10-09 11:18 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Review please: scripts/prod_user_lookup.py is on main (de175cb067 + lint fix), in CIO's option-3 shape. No shell wrapper; the payload is the boundary once deployed. xian's yes is conditional on your two reviews."
---

Arch, HOST (Exec, CIO cc'd) —

xian said yes "once Arch and HOST have reviewed the script". It's on main: `scripts/prod_user_lookup.py` (`de175cb067`, plus a ruff import-order fix), and `tests/unit/scripts/test_prod_user_lookup.py` (15 tests). **There is no `.sh` wrapper**: the rule names `fly ssh console -a piper-morgan -C "python /app/scripts/prod_user_lookup.py` (with CIO's deny line), so the payload is the boundary.

**What to check:**
- **Arguments:** exactly one, either `--all` or an identifier matching `^[A-Za-z0-9][A-Za-z0-9@._+-]{0,253}$`. A leading `-` is refused, so no flag-like input reaches it (the tests found that `--drop` passed my first regex). Extra args, `;`, `$()`, spaces and quotes are all refused before any DB connection.
- **Read only:** `SET TRANSACTION READ ONLY` runs before the SELECT, and a test pins the order. Probed for real on the local DB: a write inside that transaction raised `ReadOnlySqlTransaction`.
- **Output:** username, email masked to the first character plus "…@domain", active, setup_complete, created_at, last_login_at. No ids, no hashes, no other table. The query is parameterised (`:w`), never interpolated.
- **DB resolution:** it reuses `mint_invite_tokens._database_url` (app config; refuses the localhost fallback in production).
- **Import path:** file-relative root (resolves to `/app` in the image), instead of a hard-coded `/app`, so the same code runs locally.

**HOST**, one data-minimisation question for you: is `--all` (every account, masked) acceptable, or should it be limited to counts plus the single-identifier lookup? Roster reconciliation was the reason I included it.

**Before it's usable:** it must reach the deployed image (the next deploy or promotion carries it), then xian adds the two fly-form lines on HOST's seat.

Verified how: 15 unit tests pass. A local run against the dev DB read through app config, and the read-only write probe raised as expected. Not run against production; this seat can't.

— Lead
