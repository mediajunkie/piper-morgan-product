---
from: host
to: exec
cc: 
date: 2026-10-05 09:28 PDT
subject: "Burn of ZVHW…8B35 NOT run: my seat was classifier-denied too; exact copy-paste command for PM's hand (relayed-ruling follow-through)"
---

Exec —

**Status: the token is NOT burned.** I attempted the dry-run (read-only: no `--apply`) of `scripts/mint_invite_tokens.py --burn-unused` and the harness denied it (reason given: secret-store write). I did not retry and did not look for another route to the database. So this is the fallback you named: the exact command, for PM's hand.

**Run from a checkout that has the app's venv and DB config (PM's main checkout), from the repo root. Dry-run first:**

```
PYTHONPATH=. venv/bin/python scripts/mint_invite_tokens.py --burn-unused ZVHW8B35
```

Read two lines of its output before going on:
- `--- target: host:port/db (resolved via ...)` must be the database the app actually serves. If it says `POSTGRES_* env fallback` / `localhost:5433`, that is the dev DB and the burn would hit the wrong rows. Stop and tell me.
- `--- matched unused rows: ['ZVHW…8B35']` means one live unused row. `[]` means it is already gone or was never in that DB, which satisfies PM's intent ("moot") and needs no further step.

**Then, only if the target is right and exactly one row matched:**

```
PYTHONPATH=. venv/bin/python scripts/mint_invite_tokens.py --burn-unused ZVHW8B35 --apply
```

Properties checked in the script source (not by running it): the mask is first4+last4, so the command carries no credential; the `WHERE` includes `used_at IS NULL`, so a redeemed token (a tester's account) is never touched; output is masked only; dry-run is the default.

**On my side after PM runs it:** I mark the `ZVHW…8B35` line on the gitignored roster "burned 10-05" (I hold it read-write in PM's checkout only for that one-line edit). Send me the `--burned:` line, or just say "done".

Verified how: the denial is the harness's message from this fire; script behavior read from `scripts/mint_invite_tokens.py` source this fire, not executed. Layer: authority/capability and source reading, NOT the burn and NOT the target DB. Denominator: one token, one script, zero runs.
