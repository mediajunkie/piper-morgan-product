# Docs Carry-Forward

**Updated**: 2026-09-03 ~07:40 PDT (mid-day, session log open)
**Session log**: `dev/2026/09/03/2026-09-03-0703-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy (confirmed via `CronList` this fire),
next fire 09:57.

## No unblocked work outstanding right now

Two substantive things done this session already:

1. **"Repetition Isn't Convergence" published** — https://pipermorgan.ai/blog/repetition-isnt-convergence/
   Live-verified by content. Caught+fixed a real bug on myself mid-publish: a `git reset HEAD`
   silently dropped the deletion half of a `git mv` during drafts archival — 2nd confirmed instance
   of the exact failure class named in yesterday's carry-forward. Full trace in today's log.
2. **Weekly Docs Audit #1712 closed** (3 days late — found via a CONSTANTS-block mismatch check,
   not the actual Monday trigger; the CONSTANTS block a cron fire carried was stale on 3 separate
   claims, all checked against real state before trusting any of them). Full 8-section pass, 2 real
   findings filed (**#1720** stale `MorningStandupWorkflow` refs in 2 public guides, **#1721** 5
   missing screenshots), frontmatter-drift fixes on `BRIEFING-CURRENT-STATE.md` +
   `ROLE-PORTFOLIO-DOCS.md`, corrected a real miscount from yesterday's #1486 (skills = 35, not 37).

**First action next fire**: sync, mail loop (should be empty — just drained), check whether the
#1720/#1721 findings get picked up by anyone, otherwise genuinely open floor.

## Watch surfaces (things owned by others, checked periodically)

- **`last_verified` bulk-stamp cluster**: 14/38 as of today (was 20/38 on 09-01) — real, ongoing
  improvement since CIO's cohort-wide escalation. Don't re-chase; check again at next Monday audit
  (09-07).
- **#1644** — roadmap.md full historical fold still owed (PPM's lane); header-date symptom already
  fixed, narrative content still frozen at July state. Not mine to force.
- **#1683** — 2 inverse-case calendar rows need real Medium verification, not guessing.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call, premise no
  longer holds as originally filed.
- **GitHub issue backlog health**: 322 open, 168 (52%) stale >30 days, 17 without milestone —
  reported as a ratio in #1712, not mine to triage individually. Flag if it becomes relevant to a
  future audit, don't chase proactively.

## Doc-currency escalation is working — CIO broadcast it, roles are self-correcting for real

CIO broadcast my 8/31 escalation to the 6 role owners; PA already found a real stale claim in their
own briefing. Cluster shrinking (20→14 since 09-01). Nothing further needed from me; watch
periodically.

## Owed by Web: publish Step 9 automation, target path corrected

`piper-morgan-website#37` — I corrected the automation's target (co-located `published/`). **I
owe**: update `docs-notify.js:88`'s text once Web's automation lands. Not urgent.

## New standing responsibility: the glossary is a living-core-doc

`knowledge/piper-morgan-glossary-v1.1.md` — 60-day staleness contract (Arch's B2 workstream). Needs
CXO's tracked-state frontmatter at first substantive touch — not urgent, current header is
prose-only.

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits blocking `git pull --ff-only` in PM's own checkout. **Do not act on this
without PM present** — resume only if PM re-engages.

## Owed by me — unblocked, low priority

- **PreCompact hook locality differentiation** (added 08-23) — real design work, scope
  deliberately before implementing. Full detail in `docs-standing-items.md`.
- **Critical-docs YAML-frontmatter upgrade** — 95+ days old, own deferral condition is "flag at
  next PM engagement" — hasn't found its moment yet.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit — next auto-generates 09-07 (also 1st Monday → Monthly
  Housekeeping same day; watch for the #1713 GH-Actions scheduling defect on both).
- **First Monday of month**: Monthly Housekeeping — just closed (#1486, 09-02); next due 09-07.
- **Every Friday, EARLY**: omnibus logs Fri–Thu. Chain current through 08-28; next batch due 09-04
  (tomorrow, Friday) — covers 08-29 through 09-04.
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).

## Standing practices (apply at every fire, not just START)

- A duty-cycle sync from earlier in the session is a timestamped fact, not a durable one — re-sync
  if meaningful time has passed.
- **"Last scheduled fire of today" is arithmetic on the cron expression**, not a feel-based
  judgment. Verify before STOPping.
- **A fire is a WAKE, not a time-box** — drain unblocked work rather than deferring to "an upcoming
  fire." Legitimate holds: a real external blocker, or a genuine capacity limit (compaction) —
  never "there's a lot of it."
- **A cron fire's CONSTANTS block can itself be stale** — verify its claims against carry-forward
  AND against GitHub/live state before trusting either the prompt or your own notes blind. Caught
  today: the fire's CONSTANTS cited B3/#1486 as still-owed (both closed) and also under-reported a
  genuinely real, unworked item (#1712) that neither the prompt's memory nor my carry-forward had
  been tracking accurately.
- **`git reset HEAD` between a `git mv` and its `git add` silently drops the deletion half of the
  rename** — 2nd confirmed instance today. Always `git diff --cached --name-status` after staging a
  move, not just after a plain add, and specifically check both the old (deleted) and new (added)
  paths appear.
- **Read an issue's comment history before routing it to someone** — not just the original filing.
- **`gh issue list` defaults to a 30-item limit if `--limit` is omitted** — always pass an explicit
  high limit for anything claiming to be a total count; a suspiciously round or low number is a
  signal to re-check, not trust.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START. (Just drained as of this rewrite — should read empty next fire
unless something new arrived.)

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
