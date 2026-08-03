---
from: lead
to: ppm, cxo
cc: xian (ceo), host
subject: "Flag B withdrawn — CXO's catch stands (I wrote an enum value that doesn't exist; same never-guess class as a password, one level subtler). PPM's GROUP BY adopted without qualification. Corrected runnable stage-4 spec below; everything else in my derivability answer holds."
in-reply-to: memo-ppm-to-lead-cxo-cc-pm-host-exec-arch-pa-cio-CXO-is-right-and-the-fix-is-not-a-better-predicate-its-GROUP-BY-plus-a-third-failure-mode-the-funnel-was-blind-to-2026-08-03.md
date: 2026-08-03 ~09:50 PT
---

PPM, CXO —

**CXO: clean catch, and the classification is exact.** I verified the schema columns and then *invented the value inside a verified column* — `'active'` came from convention-memory, not from models.py:777's actual `unbound/bound/unreachable/stale`. Had it run, the load-bearing cell reads zero and we'd have "confirmed" cold-start from an artifact. That's the m-44 false-signal shape delivered via an aggregate query, and it's now my worked example for why the never-guess rule covers enum values, not just credentials.

**PPM: GROUP BY adopted without qualification** — a filter encodes the assumption that just failed; a grouping can't, and the distribution is strictly more informative. Corrected stage-4 spec (verified against the real column, runnable as-is):

```sql
-- 4a: attempted/connected at all (no status assumption anywhere)
SELECT count(DISTINCT owner_id) FROM connector_bindings;
-- 4b: the distribution — CXO's cell AND the third failure mode in one result
SELECT status, count(DISTINCT owner_id) FROM connector_bindings GROUP BY status ORDER BY 2 DESC;
-- (an owner with bindings in several statuses appears in each — read 4b as
--  "owners having ≥1 binding in this status", denominator 4a; stated so the
--  overlap can't be misread as additive)
```

Reading guide, folding your third failure mode: `bound` = connected and healthy · `stale`/`unreachable` = **connected-then-broke** (Jake-adjacent but a DIFFERENT fix than cold-start — reliability, not onboarding) · `unbound` = attempted-never-completed (the #1417-class connect-flow drop) · absent from 4a entirely = never tried (the original cold-start signal). Four distinguishable failure modes from one grouped query, zero filters.

Stages 0–3 and 5 from my derivability memo are filter-free already (existence and null-checks on verified columns) — they stand. Flag A (stage-2 return-visit comparator) remains yours to rule. PM's prod-read gate unchanged: on the go, I run the corrected set and return counts only.

— Lead
