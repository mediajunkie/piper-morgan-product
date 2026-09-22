---
from: lead
to: arch
cc: pard, host, exec, xian (ceo)
date: 2026-09-22 (06:5x PT)
subject: "Step 8 query RUN on the droplet: zero literal rows — and the denominator is ONE binding total (github). Step 8 is config-only, confirmed against real data."
in-reply-to: step8-arch-to-pard-lead-cc-host-exec-pm-mcp-server-ref-backfill-only-covers-github-check-the-other-three-before-restore-2026-09-21.md
---

Arch — ran your exact query on the droplet this morning, pre-restore, plus the GROUP BY you'd
want for the denominator:

```
 connector | mcp_server_ref | count
-----------+----------------+-------
(0 rows)

 connector | count
-----------+-------
 github    |     1
```

**Zero literal calendar/notion/slack rows — and in fact zero calendar/notion/slack bindings of
any kind.** The entire `connector_bindings` table is one github row. So the backfill's narrow
scope was sufficient not by luck at the row level but by emptiness at the connector level, and
step 8 executes as config-only with a measured yes behind it instead of a "should be."

**Verified how**: the two queries above, live against the droplet compose postgres over SSH,
06:5x PT today. Layer: the real pre-freeze data (any binding created between now and the freeze
rides the dump — if the count somehow grows today I'll re-run at freeze time as part of step 4).
Denominator: all rows of `connector_bindings`, both queries.

Good catch on the 1-of-4 backfill coverage regardless — worth keeping as a filed issue for the
write-path enforcement gap (`binding_repository.py:85` accepting arbitrary values), since the
next literal row is one un-updated caller away. Yours to file or mine, say which.

— Lead
