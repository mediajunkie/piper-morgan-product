# Docs Carry-Forward

**Updated**: 2026-09-03 ~22:40 PDT (day closed — see `dev/2026/09/03/2026-09-03-0703-docs-code-log.md`,
`<!-- DAY-CLOSED: 2026-09-03 -->`)
**Session log**: none open — next fire (2026-09-04 06:57) creates today's log.
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy, next fire 06:57.

## No unblocked work outstanding — yesterday's backlog is fully closed

2026-09-03 was dense, dominated by one real incident, fully resolved:

**The omnibus-gap incident (headline)**: PM relayed a Janus report of no omnibus for a week.
Confirmed real — 5 missing days (08-29 through 09-02) — root-caused to my own carry-forward
conflating the Workstream Review's genuinely-weekly cadence with the omnibus's genuinely-daily one
(both live in `methodology-25-WORKSTREAM-REVIEW-CADENCE.md`). Fully remediated same-day: 5
backfilled days + today's own (09-03) omnibus, all audited directly (not rubber-stamped) before
committing, 89 total `agent-activity-log.csv` rows reconciled, reply sent to Janus (confirmed
clean resolution on their side too). Chain is now continuous with zero gap. Two self-caught
process errors along the way, both owned in the open and turned into standing practices below —
neither left anything factually wrong in what's now on `origin/main`.

**Also closed**: Ship #058's Medium leg confirmed live (calendar updated to `distributed`), Weekly
Docs Audit #1712 closed (2 real findings filed — #1720, #1721 — both already triaged by PPM into
Sprint FLYWHEEL same-day), CIO's 7-issue FLYWHEEL delegation results read (all handled), a
cohort-wide heartbeat-writer investigation (checked my own case directly — confirmed working as
designed, not a lapse).

**First action next fire**: sync, mail loop, **check today's omnibus exists before anything else**
(see the mechanical check below — this is now checked every fire, not assumed).

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
