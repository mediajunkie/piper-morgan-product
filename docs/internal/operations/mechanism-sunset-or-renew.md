# Mechanism sunset-or-renew (R3 step 3)

**Status**: active from 2026-10-04 (PM approved R3; CIO drafts, Exec applies first). **Owner**: CIO.

## The rule
Every **new** watcher, hook, gate, cron or recurring check carries four lines where it is defined (the
script header, or the registry/settings comment that installs it):

```
Cost:    <what it spends: commits/day, tokens/fire, seconds/commit, a seat's attention>
Benefit: <what it has caught, with counts, or "none yet: measuring">
Review:  <YYYY-MM-DD, at most 8 weeks out>
Owner:   <role>
```

At the review date the owner writes one line, **renew** (with updated counts) or **sunset** (it gets
removed, with a pointer to what replaces it, if anything). A mechanism with no benefit recorded at its
first review is sunset by default, unless the owner says why the absence of catches is itself the
benefit (a guard that prevents rather than detects). That argument has to be made in writing, not
assumed.

## Existing mechanisms: one-time inventory
The existing mechanisms aren't grandfathered forever. Each gets the four lines at its next edit, or by
**2026-11-01**, whichever comes first. Watchers with a **false-clear history** get one consolidation
review first:

| Mechanism | Why it's reviewed first |
|---|---|
| freeze-check BELT-INVISIBLE/NO-SESSION-LOG paths | Pre-v0.16 they read "stopped" for busy seats; now corroborated. Keep, measure. |
| Step 0 DAY-CLOSED self-verification | HOST's 6-day prose-verified pass (09-23..28); the v0.17 detector now covers it externally. Consider retiring the self-check in favour of the external one. |
| post-commit heartbeat hook | 09-21 runaway; re-armed as a pilot 10-01. Record cost (commits/day) explicitly. |
| `mailbox_filename_lint` grandfathering | Archive moves passed while lengthening paths (fixed at the tool, 10-01). |

## Already compliant, as examples
- `scripts/ensure-ruff.sh` + `pre-commit-ruff-warn.sh` (10-01): cost ≈ 0.02 s per `.py` commit once the
  pinned ruff is cached; benefit being measured (Lead's one-week advisory window ends 10-08).
- `duty-cycle-freeze-check.sh` v0.17 NO-DAY-CLOSE (10-01): cost is one `git show` per logged day per role,
  about 1 s total; benefit replayed 6 real unmarked days (HOST).

## Measuring cost honestly
State **steady-state** cost, and report incident spikes separately. Example from 2026-10-04: CIO's
1,061 heartbeat-type commits over 09-05..10-03 were **968 from one runaway hour (09-21)** and **93 in
steady state (~3/day)**. Quoting the 1,061 as routine cost would have overstated it ~11×.
