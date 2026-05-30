# Comms Open Topics — cross-cutting only

**Purpose**: tracker for **non-calendar** PM topics that don't map to specific blog posts. The drafted-and-awaiting view (which used to live in this file) is now derived from the editorial calendar — run the script for current state.

**Last refactored**: 2026-05-30 (Layer B of orphan-prevention framework — retire hand-maintained drafted-view; calendar is source of truth)

---

## For the drafted-and-awaiting view

```
python3 scripts/comms-open-topics.py
```

Shows: drafted-awaiting (status=drafted), overdue (queued with past pubDate + no URLs), and queued upcoming next 14 days. Always current because it's derived from the calendar — no staleness vector.

For the orphan check (drafts<->calendar reconciliation):

```
python3 scripts/reconcile-drafts-calendar.py
```

For the calendar CSV structure check:

```
python3 scripts/validate-editorial-calendar.py
```

---

## Cross-cutting PM topics (non-calendar)

These don't have a calendar home — they're conversational threads or scope items that need surfacing periodically. **Each carries a "last touched" date; anything ≥ 30 days stale should be re-surfaced to PM (or closed) on next session.**

| Topic | State | Last touched | Notes |
|---|---|---|---|
| Fresher style/concision/jargon feedback | PM-flagged May 10; deferred until operating-model commitments met | 2026-05-10 | Related to CEO recent-Ships-running-long flag (Ship #042 kickoff). Re-surface for re-evaluation given subsequent work. |
| Conference invitation | PM mentioned Apr 24; details not yet shared | 2026-05-10 | If still alive, surface for confirmation. |
| "Code-enabled workflow" conversation | Deferred per PM Apr 24 | 2026-05-10 | If still alive, surface for re-confirmation. |
| Larger Comms remit review | Step 4 in PM's Apr 24 narrow path | 2026-05-10 | If still alive, surface for re-confirmation. |
| Methodology-00 v2.0 alignment verify-before-publish | Discipline persistent | 2026-04-26 | Verify each Pattern-062 reference against canonical methodology-00 v2.0 doc before publish (per Apr 26 commit `fa0e71a3`). Catches paraphrased-from-memory references. |
| Filing system review of comms tree | Deferred per PM "live within the system first" | 2026-04-24 | PM Apr 24 greenlit eventual review; defer until enough use-experience accrues. |

## Historical context

Items that used to live in this file (narrative-beat candidates, in-flight Ship workstream-reviews, closed-since-Apr-24 archive, voice-pass flags on specific drafts) have been retired here because they're either (a) resolved (9-beat slate ratified May 23; specific Ship reviews filed; voice-pass flags lived on individual drafts), (b) calendar-derivable (now via the script above), or (c) reconstructable from session logs + commit history. Session logs at `dev/YYYY/MM/DD/` are the canonical record for the past.

---

*Edit convention: PM and Comms both touch this file. Keep it thin — anything that can live in the calendar or be derived should NOT be hand-maintained here. Layer B discipline (PM 2026-05-29 — "log/tracker currency rides with the underlying system-of-record's update, not separate vigilance").*
