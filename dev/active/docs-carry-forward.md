# Docs Carry-Forward

**Updated**: 2026-09-03 ~19:55 PDT (mid-day, session log open)
**Session log**: `dev/2026/09/03/2026-09-03-0703-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy (confirmed via `CronList` this fire),
next fire 21:57.

## The day's headline: a real 5-day omnibus gap, found, root-caused, and closed

PM relayed a Janus report: no omnibus since 08-28. Confirmed real (not a sync issue) — 5 missing
days (08-29 through 09-02), all now backfilled and on `origin/main`, plus a 76-row
`agent-activity-log.csv` reconciliation so cross-project aggregators (DinP/Janus) reconstruct PM's
daily presence cleanly again. Root cause: **my own carry-forward had been carrying a wrong belief**
that the omnibus's cadence was weekly (Friday batch) — a bleed-over from `methodology-25`'s
genuinely-weekly Workstream Review cadence, which shares the same doc and even the same "Friday–
Thursday" language. The omnibus's own line in that doc, "Daily omnibus synthesis continues," never
changed. First backsliding like this in over a year of project history (checked the full 445-file
archive). Ship #058 was unaffected (its window predates the gap); the *next* Ship's window closed
tonight and would have hit the same coverage-check gap tomorrow if this hadn't been caught today.

**Full account, including two self-caught process errors along the way** (committing agents'
in-progress file state before their true completion, and a redundant ~45min re-audit of #1712
because I didn't read its comment history first) is in today's session log, 19:10–19:50 PM entries.

**Today's own (09-03) omnibus is deliberately deferred to day-close** — named trigger (today's own
session logs aren't finished yet), not vague deferral. Write it as part of tonight's STOP sequence,
before the DAY-CLOSED marker.

## Also this session (earlier, before the gap investigation)

1. **"Repetition Isn't Convergence" fully distributed** —
   https://pipermorgan.ai/blog/repetition-isnt-convergence/ +
   https://medium.com/building-piper-morgan/repetition-isnt-convergence-f8ac3ca22b7b. Caught+fixed
   a real bug on myself mid-publish (`git reset HEAD` silently dropping half a `git mv`).
2. **Weekly Docs Audit #1712 closed** — 2 real findings filed (#1720, #1721), both already triaged
   by PPM same-day into Sprint FLYWHEEL. *(Caveat added later today: a prior 09-01 session had
   already substantively completed most of this audit in the issue's own comments — I redid a
   meaningful chunk of it without checking first. Nothing closed is wrong; the redo just wasn't
   necessary. Lesson folded into standing practices below.)*
3. **CIO's FLYWHEEL delegation results read** — all 7 handled; #1722 filed by CIO (91 orphaned
   subagent worktrees), not mine.
4. **CIO/CXO "belt-invisible" heartbeat thread** — checked my own writer directly rather than
   assumed: confirmed working-as-designed (case a), not CXO's dead-practice case (b). Replied with
   evidence.

**First action next fire**: sync, mail loop, write today's omnibus if day-close hasn't happened yet
in a prior fire, otherwise genuinely open floor.

## Watch surfaces (things owned by others, checked periodically)

- **`last_verified` bulk-stamp cluster**: 14/38 as of today (was 20/38 on 09-01) — real improvement
  since CIO's escalation. Check again at next Monday audit (09-07).
- **#1644** — roadmap.md full historical fold still owed (PPM's lane). Not mine to force.
- **#1683** — 2 inverse-case calendar rows need real Medium verification, not guessing.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call.
- **GitHub issue backlog health**: 322 open, 168 (52%) stale >30 days, 17 without milestone —
  reported as a ratio in #1712, not mine to triage individually.

## Owed by Web: publish Step 9 automation, target path corrected

`piper-morgan-website#37` — I owe: update `docs-notify.js:88`'s text once Web's automation lands.
Not urgent.

## New standing responsibility: the glossary is a living-core-doc

`knowledge/piper-morgan-glossary-v1.1.md` — 60-day staleness contract. Needs CXO's tracked-state
frontmatter at first substantive touch — not urgent.

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits blocking `git pull --ff-only` in PM's own checkout. **Do not act on this
without PM present.**

## Owed by me — unblocked, low priority

- **PreCompact hook locality differentiation** (added 08-23) — real design work, scope
  deliberately before implementing.
- **Critical-docs YAML-frontmatter upgrade** — 95+ days old, deferral condition is "flag at next PM
  engagement" — hasn't found its moment yet.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit — next auto-generates 09-07 (also 1st Monday → Monthly
  Housekeeping same day; watch for the #1713 GH-Actions scheduling defect on both).
- **First Monday of month**: Monthly Housekeeping — just closed (#1486, 09-02); next due 09-07.
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).

(Omnibus moved OUT of this day-of-week list entirely — see Standing practices below. It is not a
day-of-week trigger; treating it as one is exactly what caused the 5-day gap.)

## Standing practices (apply at every fire, not just START)

- **DAILY, NON-NEGOTIABLE, CHECKED EVERY FIRE — the omnibus.** PM, 09-03, direct: *"Synthesizing
  session logs daily is a mandatory part of your START cycle. Do not forget it! It is the keystone
  of our entire learning and iterative process."* Run this every fire, not as a written reminder
  (a written reminder is what failed):
  ```bash
  ls docs/omnibus-logs/*.md | tail -1
  ```
  If the latest entry isn't yesterday (or today, once written), that's the fire's top priority.
- **Cadence/schedule claims get re-verified against the canonical doc, never re-propagated from my
  own prior carry-forward wording.** `methodology-25-WORKSTREAM-REVIEW-CADENCE.md`'s genuinely-
  weekly Workstream Review cadence and the omnibus's genuinely-daily cadence live in the same doc
  and share "Friday–Thursday" language — easy to conflate, and I did, silently, across several
  self-rewrites. If a "when is X due" belief has been unquestioningly re-copied more than once,
  that's a signal to re-check the source, not re-copy it again.
- **Re-verify from scratch is not automatically safer than reading first.** Redid a meaningful
  chunk of #1712's audit this morning because I checked "is this in my carry-forward" but not the
  issue's own comment history — the same failure class as "read an issue's comment history before
  routing it to someone" (already a standing practice), just not yet generalized to my own
  re-verification work. Before starting ANY audit/analysis task on a tracked issue: `gh issue view
  --json comments` first, not just `gh issue view` for the body.
- **A background agent's file-on-disk is provisional until its completion notification confirms
  it — not done-because-visible.** Committed 3 omnibus backfills once based on what was on disk;
  their agents were still revising. Wait for the actual completion report (or a stable line-count
  match against it) before treating a delegated agent's file output as final.
- A duty-cycle sync from earlier in the session is a timestamped fact, not a durable one — re-sync
  if meaningful time has passed.
- **"Last scheduled fire of today" is arithmetic on the cron expression**, not a feel-based
  judgment. Verify before STOPping.
- **A fire is a WAKE, not a time-box** — drain unblocked work. Legitimate holds: a real external
  blocker, or a genuine capacity limit (compaction) — never "there's a lot of it."
- **A cron fire's CONSTANTS block can itself be stale** — verify its claims, don't trust the
  prompt or my own notes blind.
- **`git reset HEAD` between a `git mv` and its `git add` silently drops the deletion half of the
  rename** — always `git diff --cached --name-status` after staging a move.
- **`gh issue list` defaults to a 30-item limit if `--limit` is omitted** — always pass an explicit
  high limit for any total-count claim.
- **`mail-send.sh` does not advance local HEAD** — `git merge origin/main` before assuming a
  triaged file "didn't move."
- **CC copies with a `cc-` filename prefix trigger a soft mail-send.sh warning** (expects exact
  basename match) even though delivery is correct — verify via direct `ls`/`diff` against the
  warning before treating it as a real failure; don't blindly resend.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
