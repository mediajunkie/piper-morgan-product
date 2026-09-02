# Docs Carry-Forward

**Updated**: 2026-09-01 ~22:3x PDT (DAY CLOSED — 2026-09-01 fully wrapped, sign-off checklist
clean, DAY-CLOSED marker present)
**Session log**: `dev/2026/09/01/2026-09-01-0730-docs-code-log.md` (closed, see day summary at
the bottom before the DAY-CLOSED marker). Tomorrow (2026-09-02) starts a NEW session log.
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy, next fire 6:57 PDT 2026-09-02 (a genuine
day boundary — arithmetic verified explicitly, not by feel).

## No unblocked work outstanding — genuinely idle

B3 closed (Fire 3), #1712 substantively complete (Fires 4-5), #1486 not due until ~09-07, glossary
frontmatter explicitly not urgent, PM's local checkout parked. First action tomorrow: sync, mail
loop, check whether CIO replied to the doc-currency escalation (mailed 09-01, `c98ca3d65` — don't
re-chase before next Monday's audit if silent), then it's genuinely open floor — no named priority
queued for 09-02 beyond the recurring day-of-week triggers below.

⚠️ **Recurring finding worth watching**: today's cron CONSTANTS block went stale within one fire
of B3 closing (still said "35/45 Tier C left" for the rest of the day, across 4 more fires) — the
prompt-generation mechanism doesn't appear to refresh between fires within a session. Not
actionable by me, but worth surfacing if it recurs tomorrow — read this file over the prompt's
own claims every time, as always.

## 2026-09-01, fully closed — see that day's session log for full detail

B3 corpus-disposition CLOSED (81/81 patterns, Arch's cross-corpus synthesis ruling executed
same-day including a real P-059→m-22 judgment call — full trace in
`docs/internal/architecture/reviews/2026-08-architectural-review/b3-patterns-disposition.md`).
"A Sender-Impersonation Bug" published + fully syndicated, nothing owed. **New standing practice
adopted**: publish-confirmation memos now name which syndication legs are owed and to whom, per
theme routing — carries forward indefinitely, not a 09-01-only item. Weekly Docs Audit #1712
driven to substantive completion (~10 sections, real evidence, left open for other-role items).
`.md` frontmatter is authoritative for editorial calendar data; calendar CSV is derived/convenience.

## Watch: CIO's response on the doc-currency escalation

Mailed 2026-09-01 (`c98ca3d65`) — 31/38 operating docs stale, 20 on an identical 6/19 bulk stamp,
crossed the 75% threshold. Cohort-wide staleness mechanism, not mine to fix beyond my own two
docs. Don't re-chase before next Monday's audit.

## Monthly Housekeeping Audit (#1486) — not due yet

33 unchecked items, zero progress since 2026-08-05. September's audit won't auto-generate until
~09-07 (may need another manual dispatch given the 08-31 scheduled-workflow defect — watch for
it, #1713 has the evidence if it recurs). No time pressure.

## New standing responsibility: the glossary is a living-core-doc

Per Arch's B2 workstream: `knowledge/piper-morgan-glossary-v1.1.md` is now one of six "current law"
docs (60-day staleness contract). Needs CXO's tracked-state frontmatter at first substantive touch
— not urgent, current header is prose-only.

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits (`dc943cabb`, `e5f024bf8`, `ca460a4b8`, `87d068f8a`) blocking
`git pull --ff-only` in PM's own checkout. A `diff origin/main..HEAD --stat` was pulled (touches
~20+ files, not obviously safe-to-discard) but never reviewed. **Do not act on this without PM
present** — resume only if PM re-engages.

## Awaiting others (check periodically, don't re-derive)

- **#1584** (broken links, ~34 residual) — CIO's Part C (methodology-19 numbering drift), his lane.
- **#1585** (6 genuinely-remaining low-priority items) — none urgent.
- **#1682** (item 1 Lead Dev's lane, item 3 explicitly no-urgency) — item 2 fixed 08-30.

## Owed by me — unblocked

- **PreCompact hook locality differentiation** (added 08-23) — real design work, scope
  deliberately before implementing. Full detail in `docs-standing-items.md`.
- **pmorgan.tech scrub remaining queue** — per-surface staleness+link pass, batched over fires,
  not urgent.
- **Critical-docs YAML-frontmatter upgrade** — 95 days old per CIO's dating audit, own deferral
  condition is "flag at next PM engagement" — hasn't found its moment yet, surface when it does.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit.
- **First Monday of month**: Monthly Housekeeping Audit (#1486).
- **Every Friday, EARLY**: omnibus logs Fri–Thu.
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).
- **Not mine otherwise**: Role Health Check (4-weekly, HOST).

## Standing practices (apply at every fire, not just START)

- A duty-cycle sync from earlier in the session is a timestamped fact, not a durable one — `git
  fetch` + fast-forward before reading state, if meaningful time has passed.
- **"Last scheduled fire of today" is arithmetic on the cron expression** (does the *next* slot
  fall on a different date), not a feel-based judgment on how much of the day seems done. Verify
  before STOPping — this bit once (2026-08-30), corrected, held on 2026-08-31.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
