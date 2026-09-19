# Docs Carry-Forward

**Updated**: 2026-09-18 22:50 PDT, verified via `date`.

**09-18 CLOSED — cohort's first full resumption day after the standdown.** Session log
`dev/2026/09/18/2026-09-18-1230-docs-code-log.md` carries `<!-- DAY-CLOSED: 2026-09-18 -->`.
**Duty cycle is ACTIVE.** Cron `0055648a` (`57 6,9,12,15,18,21 * * *`), re-armed at STOP via
delete-then-create (was `37386761`), `CronList`-verified sole job. Registry row `active`.

**What today was**: a cohort-wide mechanical Amber-restart gate (`amber-fleet gate`) required
every live role to write a dated handoff doc before the fleet could reboot — read `24 RED / 0
GREEN` at dawn, cleared to all-cohort-GREEN by end of day purely from individual roles completing
individually-verified deliverables. Layered on top: a 10-role sprint-closeout synthesis (Exec
compiling one primary-goal/on-track/next-steps answer from every leadership role) and — new to
this project — a "Wave 0 / Wave 1" fleet-renewal exercise run by external coordinators Pard
(execution) and Janus (certification) that deliberately `/clear`'d and replaced four live sessions
(Exec, then Arch and Comms) mid-day to test whether a cold-started successor could resume cleanly
from handoff docs + carry-forward alone, with no chat history. Not something Docs was subject to
today, but worth knowing the shape of if it recurs.

**Docs' own day**: wrote+committed `docs/handoff-docs-2026-09-18.md` under real time pressure
(couldn't independently verify the gate flip — `amber-fleet` tooling unreachable from this
worktree; confirmed only that the filename matched the required pattern); sent the sprint closeout
(388 words, cc-delivery correct this time, no warning); wrote+personally-verified the 09-18
omnibus (HIGH-COMPLEXITY, 12 sessions, 193 lines — flagged honestly below the 450–600 advisory
band as a writing-density choice, not padding, per this project's own "gaming a size check is
worse than failing it honestly" rule).

**The catch worth remembering**: the omnibus subagent reported it had already found and fixed one
chronological-ordering defect during its own verification pass. It had — but a SECOND, different
one survived into the delivered draft (HOST's 13:07 PM entry displaced after Lead's 13:24 PM entry
by a section-boundary artifact). Found via a systematic timestamp-grep across the whole file, not
by re-trusting the subagent's self-report. **Lesson: "the subagent said it verified" is a claim,
not verification — check the artifact yourself even when the delegate reports having already
checked it.**

**Also resolved, not a defect**: the omnibus narrates three prog dispatches (#1809/#1819/#1821)
but only one prog log file exists for 09-18. Read it directly — it legitimately holds all three as
sequential same-day sessions inside one file (`## Session 2`, `## Session 3`), per the project's
one-log-per-role-per-day convention. Wrote one activity-log row for prog, not three.

**PM is reconsidering automated crossposting** given the cost-to-value ratio ("the old electric
can opener thing... good to sunset some ideas") — surfaced 09-17, not yet a decision, just a real
signal worth watching. If PM raises this again, don't assume Dispatch-PM syndication requests are
still the default path without checking first.

**Third work-queue source** (PM's v1.33 ruling, established 09-13): Docs's GitHub-criteria line is
`gh issue list --search "label:documentation" --state open --limit 50` — open each result, don't
trust the list view. Denominator 10 as of 09-18, unchanged since 09-15, all already
understood/triaged. Check every WORK fire after the mail loop, alongside standing-items.

**Standing practice**: only cc PM (`xian (ceo)`) on memos that (a) contain a decision only PM can
make, (b) relay a PM ruling, or (c) contain something PM would want to contradict — everything
else reaches PM via the attention rollup. Per Exec's 09-11 proposal relaying PM's own words.

**Watching**: PM's answer on whether to draft a routing memo to Lead Dev for two audit clusters
found 09-13 (see "Watch surfaces" below) — offered 09-13, still not yet answered, not chasing.

## Prior days closed (full detail in their own session logs + omnibus-logs/)

- **09-16, 09-17**: standdown days, retroactively closed 09-18. 09-16: standdown announcement,
  Weekly Ship #060 published, Comms' `continue-narrative` v1.2 fix (STANDARD, 148 lines). 09-17:
  two scoped publishes, HOST's own ~39-hour no-scheduling-turn gap found and closed, a preserved
  cross-role discrepancy in Exec's "all rows parked centrally" claim vs. HOST's own row (STANDARD,
  121 lines).
- **09-15**: published "The Bug That Was Misdiagnosed Twice" (hashId `636ed62140e1`). Two
  self-inflicted misses, both caught same-day: reported the draft's frontmatter as empty from a
  10-commits-stale read (PM caught it directly — "are you synced?"); read and acted on a
  PUBLISH-READY memo without triaging it, an exact recurrence of an already-written rule. Omnibus
  written retroactively 09-16 per PM's explicit "make the omnibus now" instruction.
- **09-14**: closed Weekly Docs Audit #1801 (STATUS BANNER 21-day staleness gap fixed, 4 issues
  filed: #1803/1804/1805/1806); wrote+verified the day's omnibus (HIGH-COMPLEXITY, 17 sessions —
  a cohort-wide false alarm self-corrected to a model-tier-ceiling cause; a live security chain
  #1807→#1809→#1810→#1812 ran PM's-top-priority-to-closed in one day).

## Watch surfaces (things owned by others, checked periodically)

- **Time-handling audit cluster (#1493, closed) → 6 F-slice children**: #1556/1574/1575/1576/1577/1588,
  all filed 08-09/08-10, root cause "no per-user timezone exists anywhere in the system," zero
  progress in over a month. Proposed to PM 09-13 as one project routed to Lead Dev; offered to draft
  the routing memo. Still not yet answered as of 09-18 — watching, not chasing.
- **Three PM-directed audits, early August, zero follow-through**: #1499 (route-surface), #1522
  (false-trails), #1533 (principal-dropping) — each has a real report + explicit remaining-work list,
  5+ weeks with no action. Proposed 09-13 to nudge Lead Dev/Arch directly. Same PM-answer-pending
  status as the cluster above.
- **`last_verified` bulk-stamp cluster**: 24/38 as of 09-07's audit (#1725) — unchanged from 09-03,
  structural fix now filed as #1726 (CIO's lane) rather than re-escalated each audit. Check again
  at the next Weekly Docs Audit (09-21).
- **#1644** — roadmap.md full historical fold still owed (PPM's lane). Not mine to force.
- **#1683** — 2 inverse-case calendar rows need real Medium verification, not guessing.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call.
- **GitHub issue backlog health**: 336 open (as of 09-14), 216 (64%) stale >30 days, 0 unmilestoned
  (PM's 09-12 ruling holding fleet-wide) — reported as a ratio, not mine to triage individually.
- **#1720/#1721** — filed by me, already triaged by PPM into FLYWHEEL — watch for progress.
- **CXO's marker-provenance-field finding** (no observed/derived flag on the heartbeat marker,
  found 09-05) — CIO's lane, not mine. Watch for the fix landing.

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
- **"Two of Me" art-audit gap** (08-30 incident) — the publish audit checks image existence/
  dimensions but not image-content-matches-alt-text. No process fix added yet, not urgent.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit — #1801 closed 09-14; next due 09-21.
- **First Monday of month**: Monthly Housekeeping — #1724 closed 09-07; next due 10-05.
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).

(The omnibus is deliberately NOT on this list — it's a daily check, not a day-of-week trigger.)

## Standing practices (apply at every fire, not just START)

- **A subagent's self-reported verification pass is a claim, not a fact — re-verify the artifact
  yourself.** New 09-18: a delegated omnibus draft's own internal check reported one chronological
  defect found+fixed; a second, different one survived. Caught by a fresh timestamp-grep, not by
  trusting the subagent's report of having already checked.
- **A commit that includes a `git mv`-staged rename alongside separately-staged file
  modifications can silently commit only the rename** — verify via `git status` *after* the
  commit, not just a clean exit code.
- **A live-page 200 status can be a stale cached not-found fallback, not a real render** — always
  do an actual content check (title/image/body-text fragment) after the 200.
- **EVERY FIRE — run the heartbeat step explicitly and log it.**
  ```bash
  bash scripts/duty-cycle-heartbeat.sh docs {START|WATCH|WORK|STOP} --if-quiet
  ```
- **EVERY FIRE — the omnibus.**
  ```bash
  ls docs/omnibus-logs/[0-9]*.md | tail -1
  ```
  If the latest entry isn't yesterday (or today, once written), that's the fire's top priority.
- **A background agent's file-on-disk is provisional until its completion notification confirms
  it, OR its committed line count matches the report exactly.**
- **Verify a flagged discrepancy against the primary source yourself before acting on it or
  passing it along.**
- **Cadence/schedule beliefs get re-verified against the canonical doc, never re-propagated from
  my own prior carry-forward wording.**
- **Before starting ANY audit/analysis task on a tracked GitHub issue: `gh issue view --json
  comments` first**, not just the issue body.
- **A naive `cut -d','` on a CSV with quoted fields containing commas silently misaligns columns**
  — use the `csv` module for any real read, not just writes.
- **Omnibus timeline entry formats vary file-to-file** (`**H:MM**:` vs plain `H:MM AM/PM:`) — any
  script parsing timeline entries needs to handle both.
- A duty-cycle sync from earlier in the session is a timestamped fact, not a durable one — re-sync
  if meaningful time has passed.
- **Sync applies to mid-conversation direct PM engagement too, not just fire-opens.** A
  confident-sounding claim about file content is only as good as the last sync.
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
- **A `git push` can hit a transient SSH/network timeout** — distinct from a real non-fast-forward
  rejection; just retry once after confirming the error is network-shaped. A non-fast-forward
  rejection (someone else pushed first) needs an actual `git fetch` + merge, not a bare retry.
- **After acting directly on a memo during a PM-engaged session, still move it to `read/` before
  moving on** — the actual fix is doing the triage move in the same tool-call sequence as reading
  the memo, not as a separate later step to remember.
- **A cc'd memo needs a physical copy in every named recipient's inbox, not just the `to:`
  recipients' — `mail-send.sh`'s own warning catches this if you miss it, but check before
  sending, not after.**
- **`curl -s` does not follow redirects by default** — always add `-L`, or check headers first
  with `curl -sD -` before trusting a poll loop's absence of output.
- **`cleanup-dev-active` has a mandatory Step 2.1 live-artifact/active-use guard** (v1.2) — before
  filing anything to the forensic archive, check for a published-artifact reference and
  recent-commit activity.
- **A term that looks like a typo may be a documented deliberate house choice** — check
  `docs/internal/planning/comms/blog-style-guide.md` and the glossary before "fixing" any
  spelled-out term that looks wrong.
- **`scripts/validate-editorial-calendar.py` warns on `altText` empty on a published/distributed
  non-Ship row** — run the validator after every publish, not just at CSV-edit time.
- **A prose reminder to "fix this going forward," written in my own carry-forward, does not
  reliably change my own next-day behavior** — when a mistake recurs once, the fix is a mechanical
  check, not a stronger promise to remember.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
