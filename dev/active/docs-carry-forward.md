# Docs Carry-Forward

**Updated**: 2026-08-23 ~13:5x PDT (Fire 3 — Mock First syndicated + PreCompact-hook audit
corrected, 1 genuine gap added to standing items)
**Session log**: `dev/2026/08/23/2026-08-23-0727-docs-code-log.md` (open).
**Cron**: `eaf72d50`, unchanged today, healthy through ~08-29.

**New owed item**: PreCompact hook's locality-differentiation gap (CIO-flagged, confirmed
genuine after independent verification — 2 of the 3 originally-ranked options turned out to
already be addressed in substance, just not in the literal wording a grep would catch; fixed the
wording gap same-fire). Real design work, deliberately deferred to a dedicated session rather than
rushed on a hook that's wedged agents before — see `docs-standing-items.md` for full scope.

**Nothing else carried forward as blocking.** "Read the Mock First" published, fact-checked (PM's
UAT quotes + the undefinedundefined bug all verbatim matches against 06-19 primary logs), live-
verified (survived a genuine deploy-lag 404 — confirmed data was correct on origin/main before
concluding it was just lag, not a defect). Independent audit caught 2 real defects the earlier
admin-UI review pass hadn't (a negation-reveal AI tic; a "(Lead)"→"(Lead Dev)" gloss
inconsistency) — worth noting since the calendar notes claimed "PUBLISH-READY, clear for Docs"
and were accurate about *readiness to review*, just not exhaustive on their own. The doubled-
apostrophe defect from the last 2 publishes did NOT recur — checked deliberately this time, clean.

**Resolved from yesterday's watch**: the doubled-apostrophe-into-CSV mistake (2 occurrences,
08-20 and 08-22) did not recur today — checked deliberately, clean. Downgrading from "watch for a
3rd occurrence" back to routine care; no longer flagging unless it happens again.

**Still open from yesterday, not chased**: PM's offer-to-flag-omnibus-status-before-reviews
suggestion — no action taken yet, pick up if PM takes it up.

**Watch, low-priority (recurring theme)**: this carry-forward file was pruned Friday and is still
lean — kept that way through today's rewrites. Keep writing fresh entries rather than letting old
detail accumulate.

## Awaiting PM (genuine, not urgent, don't chase)

- **Docs-tree flattening plan go/no-go** — plan posted 2026-08-11
  (`docs/internal/operations/docs-tree-flattening-plan-2026-08-11.md`), one recommended flatten
  (`roadmap/CORE/`), still no PM decision. Re-verified genuinely still open 2026-08-21
  (`roadmap/CORE/` still has its original 9-subdir structure, no resolution note in the plan doc).

## Awaiting others (check periodically, don't re-derive)

- **#1584** (broken links, ~34 residual after the big 08-10/11 pass) — CIO's Part C
  (methodology-19 numbering drift) still open, his lane.
- **PDR-007** — awaits CIO only (Arch + Web already signed); measurement window runs to
  2026-08-27.

## Owed by me — unblocked

- **PreCompact hook locality differentiation** (added 08-23) — real design work on a hook that's
  wedged agents before; scope deliberately before implementing. Full detail in
  `docs-standing-items.md`.
- **#1486** (Monthly Housekeeping Audit, next due ~09-01) — routine cadence, not urgent yet.
- **pmorgan.tech scrub remaining queue** — per-surface staleness+link pass on the ~160-page
  keep-list, batched over fires (scope ratified 08-12, most of the corpus already passed; this
  is finishing the tail, not urgent).

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit.
- **First Monday of month**: Monthly Housekeeping Audit (#1486, next ~09-01).
- **Every Friday, EARLY**: omnibus logs Fri–Thu (the designed weekly catch-up — worked as intended
  08-21, closing a 2-day gap cleanly; not evidence of a failing daily cadence).
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).
- **Not mine otherwise**: Role Health Check (4-weekly, HOST).

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full pre-2026-08-21 history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
