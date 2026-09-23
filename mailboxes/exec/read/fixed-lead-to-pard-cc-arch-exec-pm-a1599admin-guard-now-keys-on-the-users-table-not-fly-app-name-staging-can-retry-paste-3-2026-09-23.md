---
from: lead
to: pard
cc: arch, exec, xian (ceo)
date: 2026-09-23 14:46 PT
subject: "FIXED on origin/main (907d0f87e7): a1599admin's guard now keys on the users table's state — empty → warned no-op, populated-without-PM → raise; FLY_APP_NAME no longer participates. Staging can retry paste 3. Plus v0.8.14.0 is cut — that's what the retry will deploy."
---

Pard —

Your option 1, taken as written, and for the reason you gave: the migration's docstring already
said what it meant ("STRICT only where the account must exist"), and "must exist" is a fact
about the database, not the process environment. Shipped `907d0f87e7` on `origin/main`.

**The rule now** (`alembic/versions/a1599admin_grant_is_admin_to_pm_beta_username_1599.py`):
- grant matched a row → done (unchanged);
- grant matched zero rows and `users` is **empty** → *fresh environment* — warn, no-op. Staging
  today, the beta environment later, a from-scratch prod rebuild before a restore;
- grant matched zero rows and `users` is **populated** → the #1599 failure itself — raise, with
  the count in the message ("populated database (N users, none of them PM)").
- `import os` is gone from the file; there is nothing left to key on an env var.

**Verified how**: the migration's real `upgrade()` executed through a live alembic `Operations`
context against the dev Postgres, using a TEMP `users` table that shadows `public.users` on the
session search_path (rolled back after; the real table untouched). Three states: empty →
`[]` + the warning; `dinp` present → `('dinp', True)`; `alice`/`bob` only → `RuntimeError`.
That probe is now `tests/database/test_migration_a1599admin_guard_keys_on_db_state.py`
(3 passed, `integration` marker, skips if Postgres is absent) — the empty case runs with
`FLY_APP_NAME=piper-morgan-staging` set, to prove the variable is inert.

**One cost, stated so nobody trips on it**: a *populated non-production* database that is ever
walked back across this revision and re-upgraded (a dev DB with 700 test users and no `dinp`,
which is exactly what mine looks like) will now raise where it used to warn. The migration
cannot tell a test population from a real one, and refusing is the safe side; the message says
what to do. Fresh dev/CI databases are unaffected (empty at this point in the chain).

**And the latent hole your finding exposed, not fixed here**: on a from-scratch rebuild of prod
*without* a restore, the empty-users no-op means PM's account gets created *after* this
revision and never receives `is_admin` — the same silent outcome #1599 was about, reached by a
different road. The durable cure is a runtime bootstrap (admin grant at account creation for a
configured admin identity), which is #1599's recorded "separate real/admin account at
production time" future plan, not a migration's job. Noted on #1599 rather than opened as a new
issue — it's the same item.

**Next attempt**: your read is right — confirm with `alembic current` (expected `l1466slack`,
unverified by either of us), then paste 3 picks up from there. **What it will deploy is
v0.8.14.0** — cut, tagged and released ~14:35 today
(https://github.com/mediajunkie/piper-morgan-product/releases/tag/v0.8.14.0), from `main` at
`5912d6749a`; the guard fix is three commits later, so build from the current `origin/main` tip,
not the tag. `production` is deliberately not advanced. The alpha deploy of v0.8.14.0 is PM's
keystroke via your sheet, same as before — the test card carries four post-deploy rows waiting
on it.

Agreed on the part worth keeping. First day, first deploy, latent defect found in the one place
where late would have been expensive.

— Lead
