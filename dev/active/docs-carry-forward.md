# Docs Carry-Forward

**Updated**: 2026-09-01 ~07:3x PDT (PM-engaged session start, "A Sender-Impersonation Bug"
published + fact-checked + live-verified; day otherwise starting fresh)
**Session log**: `dev/2026/09/01/2026-09-01-0730-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-07, next fire 09:57.

**"A Sender-Impersonation Bug, Four Days Before Beta" (Beat 4) fully closed**: published,
independently fact-checked against both primary source logs (not the calendar's summary), live-
verified. https://pipermorgan.ai/blog/a-sender-impersonation-bug-four-days-before-beta — no
syndication legs yet (awaiting PM/Dispatch-PM as usual, not chasing).

## B3 corpus-disposition — 46/81 patterns done, real work still ahead

Tracker: `docs/internal/architecture/reviews/2026-08-architectural-review/b3-patterns-disposition.md`.
**Tiers A+B fully complete** (29 patterns, light-touch — citation strength + no supersession
marker). **Tier C: 10/45 done** — the harder tier, each needs an individual grep-against-code (or
grep-against-practice, for behavioral patterns) read. **35 patterns remain**, natural work for
tomorrow's fires. Two real findings already shared with Arch/CIO (mail sent, no reply needed):
citation count mispredicts effective/inert (adopted as the standing B3 rule), and patterns'
P-006-verification-first duplicates methodology-core's own m-07 (flagged for synthesis, not fixed
unilaterally). **Disposition motion is absorb-and-mark** — mark absorption into the six
living-core-docs as part of the same motion, not a separate pass.

## Weekly Docs Audit (#1712) — generated, 74 items, still owed

Found and worked around a real infrastructure defect today: both Monday-scheduled GH Actions
silently failed to fire (filed **#1713** with full evidence). Manually dispatched
`weekly-docs-audit.yml`, produced **#1712** (74 unchecked items) — deliberately deferred to a
fresh fire rather than rushed (checklist-scale work, named trigger, not "no rush"). Did NOT
manually dispatch the monthly workflow (#1486 from last month is still open, would compound not
close a gap).

## Monthly Housekeeping Audit (#1486) — still sequenced behind B3 + #1712

33 unchecked items, zero progress since 2026-08-05. September's audit won't auto-generate until
~09-07 (and may need another manual dispatch given today's scheduled-workflow defect — watch for
it). No time pressure; picked up when B3/#1712 leave room.

## New standing responsibility: the glossary is a living-core-doc

Per Arch's B2 workstream: `knowledge/piper-morgan-glossary-v1.1.md` is now one of six "current law"
docs (60-day staleness contract). Needs CXO's tracked-state frontmatter at first substantive touch
— not urgent, current header is prose-only.

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits (`dc943cabb`, `e5f024bf8`, `ca460a4b8`, `87d068f8a`) blocking
`git pull --ff-only` in PM's own checkout. A `diff origin/main..HEAD --stat` was pulled (touches
~20+ files, not obviously safe-to-discard) but never reviewed. **Do not act on this without PM
present** — resume only if PM re-engages.

## 2026-08-31, fully closed — see that day's session log for full detail

#1708 (ALPHA_QUICKSTART hosted-primary) landed and independently verified; `SETUP.md`'s 3 real
defects fixed; compose UI Phase 4 closed (no real gap, verified against actual practice); calendar
column-ownership and #1585/#1682/#1644/#1683 all closed the day before. Nothing carries forward
from either day except what's listed above.

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
