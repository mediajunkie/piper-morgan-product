# Docs Carry-Forward

**Updated**: 2026-08-24 ~19:3x PDT (Fire 4 — #1644's roadmap.md half already fixed by PPM before
I'd recorded it as open; corrected)
**Session log**: `dev/2026/08/24/2026-08-24-0727-docs-code-log.md` (open).
**Cron**: `a53a00e3`, unchanged today, healthy through ~08-30.

**BRIEFING-CURRENT-STATE thread fully resolved** (Fire 3): Lead Dev refreshed STATUS BANNER's
Current Position + Focus same-day with full engineering attestation, history retained not
deleted — verified independently, matches exactly as described. **Process insight kept live**:
"any agent who notices refreshes it" failed silently for a week because the flag never landed in
a specific inbox; direct-mail-to-visibility-holder is the fix, proven three times this week now
(this thread, CIO's PreCompact-hook thread 08-23, and PPM's #1644 correction below).

**#1644's roadmap.md half: fixed, PPM (`2a75d74eb`, 13:14 PT) — my own carry-forward was stale
about this, corrected by PPM's direct memo.** Verified before recording: header bumped v18.7→
v18.8, honest stale-flag annotation, changelog pointing at live sources. **Issue stays open** —
symptom fixed, the real owed work (full v19 historical fold + 56 residual broken links) isn't.
Progress comment posted to #1644 itself, not left in mail only.

**Nothing else carried forward as blocking.** #1681 (Weekly Docs Audit) fully closed (74/74
checkboxes, evidence-backed). 2 real gaps found+fixed same-session: NAVIGATION.md missing Piper
Alpha (`acd0e40e7`); a genuine 3-day omnibus gap 08-21/22/23, now continuous through 08-23 (6
commits). #1475 (orphaned 08-03 audit) closed as superseded by #1643. #1682 filed for 3 minor
findings.

**Still open, not chased**: PM's offer-to-flag-omnibus-status-before-reviews suggestion from
08-22 — no action taken, pick up only if PM takes it up. CIO's PreCompact-hook locality-
differentiation gap — still my own scoped, deliberately-deferred work (`docs-standing-items.md`).

**Watch, low-priority (recurring theme)**: this carry-forward file was pruned Friday — kept lean
through the week's rewrites, no accumulation. Keep writing fresh entries.

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
