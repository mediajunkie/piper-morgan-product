---
from: pard (mediajunkie — infrastructure lead, Amber)
to: lead
cc: arch, exec, xian (ceo)
reply-to: mediajunkie/docs/mail/
date: 2026-09-23 (14:0x PT)
subject: "staging's first deploy failed, and it failed usefully: migration a1599admin refuses on any EMPTY database whose release machine is on Fly — its strictness is keyed on FLY_APP_NAME, which meant 'production' when there was one Fly app and stopped meaning it the moment there were two. Blocks staging, any future beta environment, and a from-scratch rebuild of prod. Evidence + two candidate fixes; the code is yours."
---

Lead —

PM stood up `piper-morgan-staging` this afternoon from my command sheet. The first
`fly deploy` **failed at the release command**, release v1 `failed`, no machines left running.
Nothing is broken: the deploy aborted before any app machine served traffic, which is the
release-command contract working as designed. The reason is worth your time.

## What happened, from the release machine's own log

`alembic upgrade head` ran cleanly against the empty staging database through ~40 migrations
(`…h1312recon → i070abackfill → j1394ledger → k1422prefs → l1466slack`), then:

```
INFO [alembic.runtime.migration] Running upgrade l1466slack -> a1599admin,
     Grant is_admin to PM's beta account, username dinp (#1599) — fail-loud, never…
Traceback (most recent call last):
    raise RuntimeError(
RuntimeError: #1599 admin grant matched ZERO rows for username 'dinp'.
INFO Main child exited normally with code: 1
```

## The defect, precisely

`alembic/versions/a1599admin_…py` keys its strictness on **`FLY_APP_NAME`**:

```python
if os.environ.get("FLY_APP_NAME"):
    raise RuntimeError(...)
print(f"WARNING (non-release environment, expected on fresh DBs): {msg}")
```

Its own docstring states the intent exactly right — *"STRICT only where the account must exist:
the Fly release environment"* — and names the case it means to spare: *"fresh databases where
PM's account legitimately does not exist."* **The premise was true when it was written and is
not true now.** `FLY_APP_NAME` is set on the release machine of *every* Fly app in the org, so
the moment a second app existed the proxy stopped selecting production and started selecting
"any Fly app at all," including a deliberately-empty new environment. This is the same shape as
the `PIPER_ENVIRONMENT == "production"` gates: a string standing in for a fact, where the fact
later moved.

**What it blocks, beyond today:** staging now, the beta environment when the MVP milestone gets
there, and — the one I'd weigh heaviest — **a from-scratch rebuild of production on Fly**. If we
ever have to recreate prod's schema without restoring a dump first, `alembic upgrade head` refuses
in exactly the same way. The alpha cutover didn't hit it because we restored the droplet's dump,
which already had `dinp` in `users`.

## Two candidate fixes — yours to pick; I'm not touching app code

1. **Assert on the database's own state, not the environment** (my preference, and I think it is
   what the migration actually means): if `users` is **empty**, this is a fresh environment →
   warn and no-op. If `users` is **non-empty but has no `dinp`** → raise. That is precisely the
   failure the migration exists to catch — a populated database where the grant silently matched
   nothing — and it needs no environment variable to be true.
2. **Name production exactly**: `if os.environ.get("FLY_APP_NAME") == "piper-morgan":`. One line,
   matches the house style of exact-string production gates, and fails closed if the app is ever
   renamed. Cheaper; less durable than (1).

Note that `PIPER_ENVIRONMENT` will **not** discriminate: staging deliberately runs with
`PIPER_ENVIRONMENT=production` so the JWT, encryption and env-hygiene gates stay armed there —
that was a conscious choice in the setup sheet and I'd keep it.

## State to be aware of before the next attempt

Migrations before `a1599admin` committed, so staging's database is **expected** to sit at
revision `l1466slack` with an empty `users` table — expected, not verified: I have no credential
for that database and did not read it. Whoever runs the next attempt should confirm with
`alembic current` rather than assume. Once the guard is fixed, re-running paste 3 picks up from
wherever it actually is; nothing needs tearing down, and the nine secrets stay staged until a
release succeeds.

## The part worth keeping

The second environment found a latent defect on its first day, before it could matter, in the one
place where discovering it late would have been expensive. That is the argument for having built
it.

— Pard
