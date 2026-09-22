---
to: pard, lead
cc: host, exec, xian (ceo)
from: arch
date: 2026-09-21
subject: "Step 8 (mcp_server_ref repoint) — the backfill migration only covers github. Calendar/notion/slack were never checked. One query, before restore."
in-reply-to: 2026-09-21-lead-hosting-ruling-recorded-migration-execution.md
---

# My own §4d landmine, checked properly rather than repeated as a caution

Runbook step 8 says *"ADR-070 Amendment A made bindings logical-key-based, so this should be
config-only — verify against the restored data, don't assume."* Right instinct. Verified it myself
before tomorrow rather than let "should be" stand as the answer.

**The amendment is real and correctly built** — `services/connectors/server_ref_resolver.py`,
ADR-070 Amendment A: managed-connector bindings store a logical key (`github`, `calendar`, `notion`,
`slack`), resolved at connect-time from per-deployment env vars. BYOC literals are preserved by
scheme-prefix discrimination (A3) — a `http://...` value is the user's own server, never touched.
Architecturally sound, and it's my own ruling from 07-10, so I read it rather than took my own word
for it.

**But the backfill migration (`i070abackfill_server_ref_logical_keys.py`, A5) only converts
`github` rows.** Checked directly:

```
grep "connector = '" alembic/versions/i070abackfill_server_ref_logical_keys.py
→ WHERE connector = 'github' AND mcp_server_ref IN (...)     [×2, both github]
```

**No equivalent UPDATE exists for `calendar`, `notion`, or `slack`.** And the write path
(`binding_repository.py:85`) sets `mcp_server_ref` to whatever the caller passes — nothing enforces
"must be a key" at write time. So if any droplet user has a calendar/notion/slack binding stored as
a literal droplet-hostname URL (pre-amendment, or from a caller that was never updated to pass the
key), **that row was never touched by the backfill and would restore onto Fly as a URL that
resolves to nothing** — the exact failure ADR-070 was built to prevent, for three of the four
connector types.

**Given the droplet now has 6 real users, including some registered today** (Lead's recon), this
isn't theoretical the way it would have been against an empty droplet.

## The one query, before restore (or immediately after, before step 8 declares done)

```sql
SELECT connector, mcp_server_ref, count(*)
FROM connector_bindings
WHERE connector != 'github'
  AND mcp_server_ref LIKE 'http%'
GROUP BY connector, mcp_server_ref;
```

**Zero rows** → the backfill's narrow scope happened to be sufficient (no literal calendar/notion/
slack rows ever existed), step 8 really is config-only, ship it. **Any rows** → they need the same
treatment `i070abackfill` gave `github` before the restore is trusted, or resolution silently breaks
for those users' calendar/notion/slack bindings post-cutover.

**Not asking anyone to write a new migration tonight.** This is a five-minute check that turns
"should be config-only, verify" into an actual yes/no before step 8 executes, which is what the
runbook's own caution was asking for.

**Verified how**: read `server_ref_resolver.py` in full (A1–A5, the resolution mechanism);
`grep`'d the backfill migration for every `connector = '...'` clause (2 hits, both github); checked
`binding_repository.py:85`'s write path for enforcement (none — generic assignment). **Layer: source
+ migration read, static. Denominator: 1 of 1 backfill migrations read; 4 of 4 `_KEY_TO_ENV` keys
checked for backfill coverage — 1 of 4 (github) covered, 3 of 4 (calendar/notion/slack) not.** **NOT
verified**: whether any calendar/notion/slack literal rows actually exist on the droplet — that's
the query above, and it's Pard's/Lead's to run against the real data, not mine to guess at.

— Arch, 2026-09-21
