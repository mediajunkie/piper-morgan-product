# Docs Carry-Forward

**Updated**: 2026-09-04 ~13:30 PDT (12:57 fire was quiet, no new content)
**Session log**: `dev/2026/09/04/2026-09-04-0727-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy, next fire 15:57.

## No unblocked work outstanding right now

**Ship #059 contributor workstream report written and filed** (window Fri Aug 28 – Thu Sep 3) —
Exec's kickoff was genuinely time-sensitive, treated as today's top priority, filed within the
first hour. Built from primary session logs per methodology-25 (re-read 08-28 through 09-01 fresh,
09-02/09-03 from first-hand knowledge), organized around real throughlines rather than a day-by-day
recap: every one of 6 posts published in the window had a real defect caught; B3's 81-pattern
Architectural Review workstream ran start-to-finish in <36 hours; a ~1,090-file doc-tree fold with
zero net breakage; #1712 and #1486 both closed. **Named 3 real setbacks plainly, not smoothed
over**: the 5-day omnibus gap (yesterday's headline incident), the redundant #1712 re-audit, and a
still-genuinely-open gap (the "Two of Me" art-content defect has no process fix yet). Filed
`mailboxes/exec/inbox/workstream-059-docs-2026-09-04.md` — 7 other roles' reports already landed
alongside it, on pace with the cohort.

**Yesterday's omnibus-gap remediation holds**: chain continuous through 09-03, mechanical daily
check now in place (see Standing practices below), Janus confirmed clean resolution.

**Also from yesterday, still accurate**: Ship #058's Medium leg live, Weekly Docs Audit #1712
closed (#1720/#1721 filed, both triaged by PPM into FLYWHEEL), CIO's FLYWHEEL delegation results
read, heartbeat-writer investigation resolved (confirmed working as designed).

**First action next fire**: sync, mail loop, omnibus currency check (today's own, once the day is
further along), otherwise genuinely open floor.

## Watch surfaces (things owned by others, checked periodically)

- **`last_verified` bulk-stamp cluster**: 14/38 as of 09-03 — check again at next Monday audit
  (09-07).
- **#1644** — roadmap.md full historical fold still owed (PPM's lane). Not mine to force.
- **#1683** — 2 inverse-case calendar rows need real Medium verification, not guessing.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call.
- **GitHub issue backlog health**: 322 open (as of 09-03), 168 stale >30 days, 17 without
  milestone — reported as a ratio in #1712, not mine to triage individually.
- **#1720/#1721** — filed by me, already triaged by PPM into FLYWHEEL — watch for progress,
  don't chase.

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

(The omnibus is deliberately NOT on this list — it's a daily check, not a day-of-week trigger.
Treating it as one is exactly what caused a 5-day gap this week. See Standing practices.)

## Standing practices (apply at every fire, not just START)

- **DAILY, CHECKED EVERY FIRE — the omnibus.** PM, 09-03, direct: *"Synthesizing session logs
  daily is a mandatory part of your START cycle. Do not forget it! It is the keystone of our
  entire learning and iterative process."*
  ```bash
  ls docs/omnibus-logs/[0-9]*.md | tail -1
  ```
  (Use the `[0-9]*` glob, not `*.md` — a bare `*.md` glob sorts `README.md` after the dated files
  alphabetically and can mask the real answer.) If the latest entry isn't yesterday (or today,
  once written), that's the fire's top priority — not a "next Friday" item.
- **Cadence/schedule beliefs get re-verified against the canonical doc, never re-propagated from
  my own prior carry-forward wording.** A belief re-copied more than once without re-checking the
  source is exactly how the 5-day gap happened.
- **Before starting ANY audit/analysis task on a tracked GitHub issue: `gh issue view --json
  comments` first**, not just the issue body. Redid ~45 minutes of #1712's audit this morning
  because I checked "is this in my carry-forward" but not the issue's own comment history — a
  prior session had already done most of it. Same lesson as "read comment history before routing
  to someone," generalized to re-verification work too.
- **A background agent's file-on-disk is provisional until its completion notification confirms
  it.** Committed 3 of 5 backfilled omnibus files once based on what was on disk while their
  agents were still revising; caught it via line-count mismatch against the agent's own final
  report and corrected. Wait for the actual completion report before treating delegated file
  output as final — or verify the committed line count matches the report exactly.
- **Omnibus timeline entry formats vary file-to-file** (`**H:MM**:` vs plain `H:MM AM/PM:`) — any
  script parsing timeline entries (e.g. for activity-log CSV notes) needs to handle both, checked
  directly against the actual file rather than assumed consistent.
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
- **CC copies with a `cc-` filename prefix trigger a soft mail-send.sh warning** even though
  delivery is correct — verify via direct `ls`/`diff` before treating it as a real failure.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
