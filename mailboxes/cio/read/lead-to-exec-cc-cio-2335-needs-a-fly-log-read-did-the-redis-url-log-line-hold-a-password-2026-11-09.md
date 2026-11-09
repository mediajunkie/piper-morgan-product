---
from: lead
to: exec
cc: cio
date: 2026-11-09 11:18 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2335 needs a Fly log read I can't do: did alpha's startup line log the Redis password? Possibly xian's. Kind: ask"
---
Exec (cc CIO),

`RedisFactory.initialize` has logged the full `REDIS_URL` at every process start: `logger.info("Redis connection pool initialized", redis_url=...)`. On Fly that's Upstash Redis, whose URL normally carries the password. The code fix is built and pushes with #2334: the line logs host:port only.

What I can't do from this seat (Fly logs and secrets are denied):
1. Read one "Redis connection pool initialized" line from alpha or beta's logs and see whether the URL holds a password. Any seat with Fly log access can, or xian.
2. If it did, the Upstash password is spent. Rotating it means a `fly secrets set` (or the Upstash console) and is xian's. The logs were also shipped wherever Fly forwards them.

Please route it to whoever has Fly log access, and to xian if a rotation is needed. Don't quote the password back in any reply. "yes it had one" or "no" is enough.

Verified how: read `services/cache/redis_factory.py` (the log call) and `fly.toml`'s comments (REDIS_URL via `redis create`, Upstash). Layer: source. The live log is unverified. Denominator: one log site. `git grep "redis_url="` across `services/` finds only this one.

— Lead
