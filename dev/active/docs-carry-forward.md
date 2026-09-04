# Docs Carry-Forward

**Updated**: 2026-09-03 ~16:30 PDT (mid-day, session log open; 15:57 fire was quiet, no new content)
**Session log**: `dev/2026/09/03/2026-09-03-0703-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy (confirmed via `CronList` this fire),
next fire 18:57.

## No unblocked work outstanding right now

Three substantive things done this session already:

1. **"Repetition Isn't Convergence" fully distributed** —
   https://pipermorgan.ai/blog/repetition-isnt-convergence/ +
   https://medium.com/building-piper-morgan/repetition-isnt-convergence-f8ac3ca22b7b (building
   theme, LinkedIn correctly empty). Calendar status=distributed, canonicalSite=distributed. Caught
   +fixed a real bug on myself mid-publish: a `git reset HEAD` silently dropped the deletion half of
   a `git mv` during drafts archival — 2nd confirmed instance of the exact failure class named in
   yesterday's carry-forward. Full trace in today's log.
2. **Weekly Docs Audit #1712 closed** (3 days late — found via a CONSTANTS-block mismatch check,
   not the actual Monday trigger). Full 8-section pass, 2 real findings filed (**#1720** stale
   `MorningStandupWorkflow` refs in 2 public guides, **#1721** 5 missing screenshots), frontmatter-
   drift fixes on `BRIEFING-CURRENT-STATE.md` + `ROLE-PORTFOLIO-DOCS.md`, corrected a real miscount
   from yesterday's #1486 (skills = 35, not 37). **Both filed issues already triaged by PPM
   same-day** into Milestone Ongoing / Sprint FLYWHEEL — nothing further owed.
3. **Read CIO's FLYWHEEL delegation results** (the 7-issue delegation I sent 09-02): all 7 handled,
   4 were already done before dispatch, 2 genuinely new fixes shipped with real evidence, 1 done
   directly, 1 filed as CIO's own standing item. CIO also filed **#1722** (91 orphaned subagent
   worktrees) — not mine, noted for awareness only.

**First action next fire**: sync, mail loop, otherwise genuinely open floor — nothing owed.

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
- **DAILY, NON-NEGOTIABLE, PART OF EVERY START — omnibus logs.** PM, 09-03, direct instruction:
  *"Synthesizing session logs daily is a mandatory part of your START cycle. Do not forget it! It
  is the keystone of our entire learning and iterative process."* This is not a day-of-week trigger
  like the others on this list — check "does today already have an omnibus?" at the START of
  **every** fire, not on a Friday-shaped schedule.
  ⚠️ **CORRECTED 09-03, after a real 5-day gap (08-29→09-02) went unnoticed through 5 duty-cycle
  fires**, surfaced only when PM relayed a Janus report. **Root cause, PM's own diagnosis, confirmed
  against the doc**: `methodology-25-WORKSTREAM-REVIEW-CADENCE.md` legitimately uses "Friday–
  Thursday sprint window" language for **Workstream Reviews** (a separate, genuinely-weekly
  deliverable) and mentions the omnibus in the very same breath — that doc's real weekly cadence
  got conflated with the omnibus's own unrelated line in the SAME doc, "Daily omnibus synthesis
  continues," which never changed. This line used to correctly carry that distinction ("Friday is
  the designed weekly catch-up — not evidence of a failing daily cadence") and it eroded across
  several self-rewrites this week into "next batch due Friday," which read as on-schedule from
  inside my own tracking. **Checked the full history**: every gap since 2025-09-02 had been ≤1 day
  until this one — first backsliding like this in over a year, not a recurring pattern. **Checked
  Ship impact**: Ship #058 (published 09-02) was NOT affected — its workstream-review window
  (08-21–08-27) fully predates the gap. The upcoming Ship's window (08-28–09-03) DOES overlap it,
  but workstream-review drafting for that window doesn't start until tomorrow (Friday) — a
  near-miss, not actual damage, contingent on the backfill landing before then.
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
- **`mail-send.sh` does not advance local HEAD** — it pushes via `commit-tree` straight to
  `origin/main`. Right after a send, local disk for the paths involved can still look pre-move
  until an explicit `git merge origin/main`. If a triaged file appears to still be sitting in
  `inbox/` right after a successful send, check `git log HEAD..origin/main` before assuming
  anything went wrong or re-sending.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START. (Just drained as of this rewrite — should read empty next fire
unless something new arrived.)

## Omnibus currency check — RUN EVERY FIRE, NOT A WEEKLY BULLET (added 09-03 after the 5-day gap)

```bash
python3 -c "
import datetime
today = datetime.date(2026, 9, 3)   # update mentally to actual today
latest = max(__import__('glob').glob('docs/omnibus-logs/????-??-??-omnibus-log.md'))
print('latest omnibus:', latest)
"
ls docs/omnibus-logs/*.md | tail -1
```
If the latest entry isn't yesterday (or today, once today's has been written), that is the single
highest-priority item of the fire — not a "next Friday" item. This is a mechanical replacement for
a written reminder, because the written reminder is exactly what failed here.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
