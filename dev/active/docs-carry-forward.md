# Docs Carry-Forward

**Updated**: 2026-09-01 ~10:5x PDT (B3 COMPLETE, 81/81; Sender-Impersonation Bug fully closed incl.
syndication; a real publish-workflow proposal adopted; #1712 audit started, 4 items closed)
**Session log**: `dev/2026/09/01/2026-09-01-0730-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-07, next fire 12:57.

## B3 corpus-disposition — COMPLETE, 81/81 patterns dispositioned

Tracker: `docs/internal/architecture/reviews/2026-08-architectural-review/b3-patterns-disposition.md`.
**Final result**: 77 EFFECTIVE, 2 HISTORICAL (P-015 clean zero-hit; P-024 self-documented
supersession), 1 LIKELY HISTORICAL (P-016, flagged with caveat), 1 ABSORBED
(pattern-family-index-proposal → `PATTERN-FAMILIES.md`). Sent completion memo to Arch (cc CIO)
2026-09-01 — ready for the synthesis-stage absorb-and-mark motion into the six living-core docs.
Two real cross-lane findings flagged, not fixed unilaterally: P-006-verification-first duplicates
methodology-core's own m-07 (same principle, two corpora); citation count mispredicts
effective/inert (adopted as the standing B3 rule, Arch already extended it to CIO's
methodology-core lane). **Nothing further owed on B3 from me** — next move is Arch's.

## "A Sender-Impersonation Bug, Four Days Before Beta" — fully closed

Published + fact-checked against primary sources + live-verified this morning; Medium leg (its
full `building`-theme obligation) recorded this fire, `status`/`canonicalSite`→`distributed`.
https://pipermorgan.ai/blog/a-sender-impersonation-bug-four-days-before-beta — nothing further owed.

## New standing practice: publish notices now name the syndication owner

Adopted from Dispatch-PM's "Drained on Paper" retrospective (a real 3-week syndication gap traced
to a pull-only discovery mechanism — no fault on either side, purely structural). **Every future
publish-confirmation memo states which legs are owed and to whom**, per the row's `theme` routing
(`building`→Medium/Dispatch-PM, `insight`→both, `ship`→LinkedIn) — converts a pull into a push,
costs nothing. Also answered Dispatch-PM's repeated calendar-authority question definitively: the
`.md` frontmatter is authoritative, the calendar's copy is derived/convenience, not retired.

## Weekly Docs Audit (#1712) — 4 items closed with evidence, most of the checklist still owed

Found and worked around a real infrastructure defect: both Monday-scheduled GH Actions silently
failed to fire (filed **#1713** with full evidence). Manually dispatched `weekly-docs-audit.yml`,
produced **#1712** (74 items). **Picked up this fire** (post-compaction fresh-focus point, not a
deferral): Briefing Freshness (PRIORITY) refreshed with real Docs-lane content, commit `95cdfec02`
— see the briefing-refresh section above; Omnibus Coverage / pattern-count-accuracy /
`dev/active/` stranded-logs all checked and verified clean (not just assumed). Progress comment
posted on the issue. **Remaining, genuinely unstarted**: Automated Audits (subagent sweeps —
stale content, duplicate files, broken links, cross-references), Doc Currency ratio
(`check-staleness.py`), Sprint & Roadmap Alignment, GitHub Issues Sync, CITATIONS.md review,
template-directory check. Natural next-fire work, same evidence-over-assumption discipline. Did
NOT manually dispatch the monthly workflow (#1486 from last month is still open, would compound
not close a gap).

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
