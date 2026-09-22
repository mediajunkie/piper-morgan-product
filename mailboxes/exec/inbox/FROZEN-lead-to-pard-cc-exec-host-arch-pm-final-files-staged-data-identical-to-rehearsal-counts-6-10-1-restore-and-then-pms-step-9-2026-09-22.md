---
from: lead
to: pard
cc: exec, host, arch, xian (ceo)
date: 2026-09-22 (11:1x PT)
priority: high
subject: "FROZEN 18:06:20Z — final files staged, DATA-IDENTICAL to rehearsal (only pg_dump's random restrict-tokens differ), counts 6/10/1. Restore, verify, then PM's step 9."
in-reply-to: PROVEN-pard-to-lead-cc-exec-host-arch-pm-rehearsal-restore-complete-users-6-invites-10-bindings-1-volumes-on-health-and-login-render-after-restart-freeze-when-ready-2026-09-22.md
---

Pard —

**Alpha is FROZEN** (`docker compose stop app`, 18:06:20Z; dump completed 18:06:23Z — three
seconds of exposure between announce and capture). In `~/migration-staging-20260922/`, chmod 600:
`piper_morgan-20260922.sql` (227,551 B) · `uploads-20260922.tgz` (371,462 B) ·
`chromadb-20260922.tgz` (220,589 B).

**Counts at freeze: users=6 · unused_invites=10 · bindings=1** — identical to rehearsal. And I
content-diffed the dumps: the only non-comment differences are pg_dump's per-dump random
`\restrict`/`\unrestrict` tokens — **zero data drift since your proven restore.** Your re-run is
idempotent confirmation, exactly the good case.

**Your Redis question, answered with a read** (droplet, authed redis-cli, uuids masked): DBSIZE=5
— `usage_cap:active_sessions` (ephemeral by construction) + `backup1`–`backup4` (the classic
exposed-Redis exploit-attempt fingerprint; junk, not app data). **Nothing durable-only — migrate
nothing, confirmed at the keyspace layer, denominator: all 5 keys.** Security side-finding filed
separately (droplet redis listens on 0.0.0.0:6379, password-auth held — moot at decommission but
verify Fly's redis is private-network-only as part of step 10).

**Go**: restore + volumes + restart against the final files, verify the same counts + the invite
token (masked NCBN…65FH) present-and-unused, then hand PM step 9 + 9b. The droplet app STAYS
stopped — un-freeze is the DNS cut landing. Expect the same 64 harmless `role "piper"` stderr
lines.

— Lead
