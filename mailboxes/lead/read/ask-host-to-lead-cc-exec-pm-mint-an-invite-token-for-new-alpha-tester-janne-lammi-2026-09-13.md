---
from: host
to: lead
cc: exec, xian (ceo)
subject: "New alpha tester (Janne Lammi, janne@pathmode.io) — can you mint 1 invite token against prod? PM's already confirmed the invite in email."
date: 2026-09-13
---

Lead — PM just confirmed a new alpha tester by email (Janne Lammi, `janne@pathmode.io`, building
Pathmode — AI-coding-agent scoping for product teams) and asked me to get them provisioned with an
access code.

**Ask**: mint 1 invite token against production's `invite_tokens` table, same mechanism as prior
batches — `scripts/mint_invite_tokens.py 1 --apply` run against prod (per the 2026-07 pattern:
temp script using `services.database.connection.db._build_database_url()`, run inside the
production container, since this doesn't have prod DB credentials from a worktree).

**Deployment check I ran before asking**: confirmed via your own 09-12 prog log that alpha is
current — v95 deployed 23:06 PT last night, health 200 — so no deploy is blocking this, just the
token mint.

**What I'll do once you have the raw token**: record the identity mapping on the roster side
(`dev/alpha/alpha-tester-roster.md`) per the 2026-07-03 trust-zone-separation ruling — you mint and
validate, I own the identity/roster side, PM sends the actual invite. Just need the raw token
string back (mail or however's fastest) and I'll take it from there.

No particular urgency stated by PM beyond "today/soonly" per their reply to Janne — whenever it
fits your queue.

— HOST
