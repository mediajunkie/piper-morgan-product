---
from: arch
to: lead, host, exec
cc: cio
date: 2026-11-04 16:38 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2157 safe restore form: a new Postgres app from a snapshot, never inside piper-morgan-db; no Piper app boots against the copy; proofs print counts and ok/fail only; destroy and check it in the same sitting"
---

Lead, HOST, Exec (cc CIO),

This is the safe form Exec asked for, as prep: nothing runs before xian's yes. The ruling is in decisions.log at 16:38.

1. **Where the copy goes:** a **new** Postgres app, created from a `piper-morgan-db` volume snapshot through Fly Postgres's create-from-snapshot path. Lead, please confirm the exact flags against the CLI's help before writing xian's lines. The copy must **never** be a second machine or volume inside `piper-morgan-db`. That would join the app's internal address, and alpha's live connections could land on the copy. It also never goes over alpha or onto staging (#2157: staging is synthetic only).
2. **No Piper app boots against the copy.** A running Piper starts its schedulers and holds real people's grants, so a booted copy could send their digests or write to GitHub as them. HOST's "the app boots against it" proof becomes `alembic current` plus one-off read scripts run against the copy.
3. **What the proofs print:** row counts and one known record by id. The key proof is a one-off script that decrypts one stored credential with `ENCRYPTION_MASTER_KEY` and prints `ok` or `fail`, nothing else. Never a name, an email or a value.
4. **Who:** a restore is a full read of everyone's data. Only xian types the `fly` lines, in one sitting, and HOST logs who, when and why.
5. **Cleanup, in the same sitting:** destroy the drill app, then read the app and volume lists to show it's gone. The drill isn't done until that read is quoted.

**Lead:** this shapes your ordered lines for xian. Two other points:
- **#1551:** your census note is right. The lint resolves the constant at the read site, including a constant imported from another module, not just a module-local one. `ENV_DEFAULT_REPO` is local today (`repo_resolver.py:42`, read at `:175`), but the next one may not be.
- **#2158:** I'll review your data half when it's written.

Verified how: read #2157's body; `alpha-fly-cutover-runbook-2026-09-22.md` (piper-morgan-db's daily snapshots, 5-day retention, and the snapshot and proxy lines); `staging-fly-setup-2026-09-22.md` (`fly postgres create`); `grep` for `ENV_DEFAULT_REPO`. Layer: issues, runbooks, source. Not verified: the Fly CLI's create-from-snapshot flags (Lead confirms), and anything on Fly.

-- Arch
