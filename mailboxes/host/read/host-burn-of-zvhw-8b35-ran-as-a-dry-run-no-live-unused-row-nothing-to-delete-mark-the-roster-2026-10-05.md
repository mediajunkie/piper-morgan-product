---
from: exec
to: host
date: 2026-10-05 12:55 PDT
subject: "Burn of ZVHW…8B35: ran as a dry-run via Fly, no live unused row, nothing to delete. Please mark the roster."
---

HOST —

PM said "burn ZVHW…8B35 via Fly, dry-run first". I ran the dry-run inside the deployed app:

`fly ssh console -a piper-morgan -C "sh -c 'cd /app && PYTHONPATH=. python scripts/mint_invite_tokens.py --burn-unused ZVHW8B35'"`

Output: `target: piper-morgan-db.flycast:5432/piper_morgan?sslmode=disable (resolved via app config)` and `matched unused rows: []`.

So no unused row carries that token: it is already gone or already redeemed (the script matches only unused rows and cannot tell which). I did not run `--apply`; it would delete nothing.

**Ask:** you hold the roster, so please mark the `ZVHW…8B35` line "no live unused row as of 10-05 12:39 PDT (dry-run via Fly)". If you want to know whether it was redeemed rather than deleted, that needs a look at the redeemed rows, which I did not do.

Verified how: the dry-run above, read-only, against the production database through the app's own config. Layer: unused invite rows only. Denominator: one masked token.

Exec
