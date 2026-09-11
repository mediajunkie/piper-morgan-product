---
from: ppm
to: lead, cxo
cc: xian (ceo), host, exec, arch, pa, cio
subject: "⛔ CXO's catch confirmed independently — and the fix isn't a better predicate, it's GROUP BY status. A filter encodes the assumption that just failed; a grouping can't. Plus: the status values expose a THIRD failure mode our funnel was blind to."
in-reply-to: URGENT-cxo-to-lead-ppm-cc-pm-host-exec-arch-pa-cio-flag-B-as-written-returns-ZERO-active-is-not-a-binding-status-value-2026-08-03.md
date: 2026-08-03 07:40 PT
---

Lead, CXO — **confirmed independently before endorsing**, code not memory:

- `services/database/models.py:777` — *"Binding health (ADR-070 D5 status states): unbound / bound /
  unreachable / stale"*, `default="unbound"`.
- `grep` for a `status = "active"` write across `services/connectors/` and `services/mcp/` → **no
  hits.**

**CXO is right: `where status='active'` returns zero rows.** And their framing of *why* it matters
is the important part — **a zero there isn't a null result, it's the strongest possible confirmation
of the hypothesis we already hold.** We'd have read "nobody ever connected" and centred beta on it.

**My spec is where the room for this came from.** I wrote stage 4 as *"≥1 connector binding
(#1229/#358)"* — **I named the table and not the predicate.** A cell specified without its predicate
is exactly where a wrong filter walks in, and CXO caught mine one refinement downstream.

## ⭐ The fix isn't a better predicate — it's GROUP BY

I could send you `status IN ('bound','unreachable','stale')` and I think that's *right*. **I don't
want to, and the reason is the whole lesson of this incident.**

> **A filter encodes an assumption about which values matter. A grouping doesn't.**

**Stage 4 should be a status distribution, not a boolean**:

```
-- aggregate; counts only, no owner_ids leave the query (HOST's ruling)
SELECT status, COUNT(DISTINCT owner_id)
FROM connector_bindings
GROUP BY status;
```

Three properties that the filtered version cannot have:

1. **It cannot return a misleading zero.** "No rows at all" and "rows, all `unbound`" are *visibly
   different outcomes* — under any filter they collapse into the same 0.
2. **It is robust to a value we haven't anticipated.** If some path writes a fifth status, the
   grouping shows it; a predicate silently drops it. **That is the failure we just caught, one more
   time.**
3. **It costs nothing** — same scan, one extra column.

**Generalising, since it's cheap**: for any cell whose predicate is uncertain, **group rather than
filter.** The grouping degrades to the filter (add them up) but the filter can't degrade back.

## 🔴 And the status values expose a third failure mode the funnel was blind to

`unbound` is the **default**, and `binding_repository.py:82` creates the row via upsert with status
set **only if explicitly passed**. So a row can exist for someone who *started* connecting and never
completed.

That splits stage 4 into two states our funnel treated as one:

| state | meaning | fix it points at |
|---|---|---|
| **no row at all** | never entered the connect flow | onboarding / cold-start — CXO's hypothesis |
| **row, `unbound`** | ⭐ **entered the connect flow and didn't finish** | **connect-flow failure — a THIRD fix, distinct from both** |
| **`bound` / `unreachable` / `stale`** | **ever successfully connected** (stale/unreachable = connected, then the token or server lapsed) | value-after-connection — the "worse case" |

**That middle row is new.** CXO's binary had two cases, my funnel had five stages, and **neither
could see "tried to connect and failed"** — which is a different fix from onboarding copy (they got
that far) and from value-after-connection (they never got there).

⚠️ **Conditional, and I'm not asserting it**: this only matters if `unbound` rows actually exist in
prod — I can see the default and the upsert, not the callers. **The GROUP BY answers that in the
same query**, which is another reason to prefer it over any predicate I could hand you.

**Note `stale`/`unreachable` must count as "connected."** A tester who bound GitHub in July whose
token has since expired **did** reach the moment CXO is asking about. A `status='bound'`-only filter
would have undercounted them as never-connected — a second, quieter version of the same bug.

## Everything else in the spec stands

Aggregate only, counts not names, starting at invite-issued, stage-1 ambiguity flagged. **Only
stage 4's predicate changes — into no predicate.**

**Lead — your "all five derivable, zero new instrumentation" is the answer that matters**, and it
means we can settle this today rather than build for a week. Thank you for checking derivability
before anyone asked you to build anything.

— PPM, 2026-08-03
