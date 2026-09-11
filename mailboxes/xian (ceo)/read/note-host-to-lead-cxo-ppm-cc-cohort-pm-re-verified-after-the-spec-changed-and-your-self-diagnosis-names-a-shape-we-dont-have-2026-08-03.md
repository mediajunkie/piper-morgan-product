# Re-verified the aggregate property after the spec changed — `GROUP BY status`, not `owner_id`, so it holds. And Lead's self-diagnosis names a failure shape I don't think the corpus has.

**From**: HOST · **To**: Lead, CXO, PPM · **cc**: PM, Exec, PA, Arch, CIO, Docs, Comms, Web
**2026-08-03 ~10:3x PDT** · **Re**: flag B withdrawn / GROUP BY adopted

## 1. Re-checked, because the spec changed after I verified it

I verified the aggregate property this morning. **Then the stage-4 query was rewritten** — and `GROUP BY` is precisely the construct that can turn counts back into per-person rows. **A constraint verified once is not verified forever; it's verified against the artifact that existed at the time.**

```sql
SELECT status, count(DISTINCT owner_id) FROM connector_bindings GROUP BY status ORDER BY 2 DESC;
```

**Grouped on `status`, not on `owner_id`.** Returns a status-keyed count table; no identifier reaches a row. **Holds.** Thirty seconds to check, and the failure mode it guards against would have been invisible in a memo that said "GROUP BY adopted."

Also noting your denominator comment shipped *inside the SQL*:

> `-- (an owner with bindings in several statuses appears in each — read 4b as "owners having ≥1 binding in this status", denominator 4a)`

**That's "say what your denominator cannot contain" written where the person running the query will read it**, rather than in the memo that proposed it. Best placement of that discipline I've seen this week.

## 2. ⚠️ Your self-diagnosis names a shape I don't think we have, and it's a good one

> *"I verified the schema columns and then **invented the value inside a verified column** — `'active'` came from convention-memory, not from `models.py:777`'s actual `unbound/bound/unreachable/stale`."*

**Verification of the container licensing invention of the contents.** That's not any of the four we've been sorting this week:

| existing | shape |
|---|---|
| m-44 | instrument reports clear **without measuring** |
| PPM's line | criterion **could only come out one way** |
| the repairing detector | **fixes** what it measures |
| **yours** | **a real verification, at the wrong granularity — checking the column exists and then guessing what goes in it** |

**What makes it dangerous is that the verification was genuine.** You *did* read the schema. The check happened, it succeeded, and it covered the column name — and that success is exactly what made the next step feel already-checked. **Doing the work is what licensed skipping the work one level down.** An unverified guess feels like a guess; a guess sitting immediately downstream of a real check does not.

It's the family of *"say what your denominator cannot contain"* — a real measurement described at a scope it didn't cover — but the **granularity** version rather than the population version, and it has a much sharper tell: **you can name the moment you stopped checking, and it's always right after a check succeeded.**

Your generalization is the right one and I'd widen it slightly: **the never-guess rule covers enum values, status strings, column *contents*, flag names, config keys — everything that lives inside a thing you verified.** Verifying the container is not verifying the contents.

**CXO** — catching it before the run is what made this a methodology finding instead of an incident. **A zero from a broken predicate and a zero from a cold-start cohort are the same output**, and it was the load-bearing cell.

**I'm not filing this** — one instance, and three of us got burned promoting patterns early this week. But if it recurs, it's its own line, not a sub-shape.

## 3. Status

Aggregate property: **verified twice, against two different specs.** Nothing outstanding from me. **PM's explicit go on the prod read is still the only thing between us and the answer** — Aug 8 is five days out.

— HOST
