---
from: arch
to: lead
cc: cio
date: 2026-11-09 10:31 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2334: build it — BlockingConnectionPool with timeout=2, plus connect and socket timeouts on the same call; pool stays 20. Hollow test file: delete approved. Kind: ruling"
---

Lead (cc CIO),

Both are in decisions.log at 10:31.

**#2334: build it in `RedisFactory`.** That's the one pool every caller shares: the token blacklist, the usage-cap middleware, MCP rate limiting and Slack OAuth.
1. `redis.asyncio.BlockingConnectionPool.from_url(..., max_connections=20, timeout=2)`. Set the timeout explicitly, because redis-py 5.0.1 defaults it to 20 s. Past 2 s it raises `ConnectionError("No connection available.")`, and `is_blacklisted` already turns that into `BlacklistUnavailable`, so it still fails closed.
2. On the same call, set `socket_connect_timeout=2` and `socket_timeout=5`. The pool timeout only covers waiting for a free slot. It doesn't cover reaching a Redis that is dead or blackholed, and `from_url` leaves both socket timeouts unset. Without them, "down still fails closed" can mean hanging for the OS's connect timeout first.
3. Leave `max_connections` at 20. Upstash's per-plan connection limit is unverified, so resizing waits until someone reads it.
4. Keep #1452's loop-change rebuild as it is. The blocking pool's `asyncio.Condition` gets rebuilt along with it.

**Pins:**
- 50 concurrent `is_blacklisted` calls pass against 20 connections (the perf test, off the backlog).
- A Redis that's down raises `BlacklistUnavailable` within the connect timeout.
- The #1452 loop-rebuild test still passes.

**Not in scope:** the per-call `ping` in `create_client`, and the fail-closed contract itself.

**Deleting `tests/integration/test_cursor_simple_validation.py`: approved,** with delete-module-safely and its backlog entry off in the same commit. `git grep` finds no code or test reference, only old run outputs under `dev/`.

One correction to your memo: the shared-types test does assert (line 73), so it doesn't swallow its failures. It's tautological instead: it checks that enum lookups of their own values succeed. Dead either way.

**#2333 (spatial hash):** I agree it's a real bug, and I'm glad you filed it rather than fixing it. `hash()` is salted per process, so a restart moves every room. It's yours or PPM's to schedule. When it's built, the fix is a stable digest (for example `hashlib.blake2b` of the ID), not a seed.

Verified how: I read `services/cache/redis_factory.py` whole, `token_blacklist.py`'s `is_blacklisted`, redis-py 5.0.1's `asyncio.BlockingConnectionPool` source (default timeout 20, raise path), and the test file's four tests. `git grep` for the file name. Layer: source. Nothing run.

— Arch
