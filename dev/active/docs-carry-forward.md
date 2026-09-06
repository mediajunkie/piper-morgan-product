# Docs Carry-Forward

**Updated**: 2026-09-05 ~19:30 PDT (18:57 fire was quiet, no new content)
**Session log**: `dev/2026/09/05/2026-09-05-0727-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy, next fire 21:57 — this is today's LAST
scheduled fire, expect day-close then (write today's own omnibus per the daily-check practice).

## "We Built Onboarding in Our Own Image" fully distributed

Published + both syndication legs live (Medium + LinkedIn), calendar status=distributed. Caught
and fixed a small error from my own 09-03 publish along the way (a `cut`-based CSV check
misparsed due to embedded commas — the real `cluster` convention for recent posts is empty, not
workDate; used the correct value this time). Also caught a small mail-triage lapse this fire
(Comms' PUBLISH-READY memo sat unmoved in inbox/ after I'd already acted on it directly) — fixed,
noted as the same "no immediate visible consequence" shape as this week's other lapses.

## Heartbeat/m-45 thread fully resolved

CIO's backfill fix shipped, tested directly against my own incident as a fixture (21/21 passing),
confirmed live and working this fire (marker updated even on a suppressed row). CXO found one real
residual (no observed/derived provenance field on the marker) rather than report a false
behavioral pass — CIO's lane, not mine. **`methodology-50-SELF-ATTESTATION-IS-NOT-VERIFICATION.md`
filed**, citing my own lapse accurately as one of three real instances. Nothing further owed.

## No unblocked work outstanding right now

**A real heartbeat-invocation lapse found in my own practice, owned and fixed.** Exec corrected
their own earlier "cold-start, not urgent" read about my status (10 of 11 roles now had a marker,
only Docs didn't, 38 hours stale) and asked for a direct check. Ran it — the writer works fine. But
my own first explanation (assumed benign `--if-quiet` suppression) was ALSO wrong, caught only by
checking my own session logs directly rather than trusting the assumption: the explicit per-fire
"Heartbeat: X" practice ran consistently 08-28 through 09-02, then dropped to a single instance on
09-03 (the day the omnibus-gap investigation displaced the normal fire structure) and never
resumed — not for the rest of that day, not on 09-04, not this morning. A genuine "invoked, then
stopped" case, the same shape as two of CXO's lapses this week, HOST's third confirmed instance.
Replied to Exec (cc CIO/CXO/HOST/PM) owning both the lapse and the fact that my own initial
explanation repeated the exact unverified-assertion mistake Exec's own memo had just apologized
for. Re-added the heartbeat step to standing practices below.

**My m-45 citation-drift finding from 09-04 confirmed twice over**: CIO acknowledged directly and
fixed it same-fire; CXO independently made and caught the identical mistake in a separate context.
Disposition correctly deferred by CIO to a fresh session, not rushed. Arch/PA/CXO traced the
citation error's own provenance today (informational, already resolved).

**Today's queue** ("We Built Onboarding in Our Own Image," insight, Saturday) still `status=drafted`
— matches every prior weekend this week, not chasing.

**First action next fire**: sync, mail loop, omnibus currency check, **run the heartbeat step
explicitly this fire and every fire going forward** (see Standing practices), otherwise genuinely
open floor.

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
- **The cohort-wide "recurring duty survival" design thread** (CIO/CXO/HOST/Exec, running since
  09-03 evening) — a joint proposal to PM on self-fired vs. chokepoint duties, my own omnibus-gap
  incident is one of the cited supporting cases. Not mine to co-author (Exec/CIO's lane), but worth
  reading the eventual proposal since it may reshape how my own daily/weekly duties are tracked.

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
- **"Two of Me" art-audit gap** (named honestly in the Ship #059 report, 08-30 incident) — the
  publish audit checks image existence/dimensions but not image-content-matches-alt-text. No
  process fix added yet. Worth a small addition to the publish checklist when there's a natural
  moment, not urgent enough to interrupt other work for.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit — next auto-generates 09-07 (also 1st Monday → Monthly
  Housekeeping same day; watch for the #1713 GH-Actions scheduling defect on both).
- **First Monday of month**: Monthly Housekeeping — just closed (#1486, 09-02); next due 09-07.
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).

(The omnibus is deliberately NOT on this list — it's a daily check, not a day-of-week trigger.)

## Standing practices (apply at every fire, not just START)

- **EVERY FIRE — run the heartbeat step explicitly and log it.**
  ```bash
  bash scripts/duty-cycle-heartbeat.sh docs {START|WATCH|WORK|STOP} --if-quiet
  ```
  Then write `Heartbeat: {phase}` in the fire's log entry. ⚠️ **This is not a fresh reminder — it
  was already the standing practice through 09-02, then genuinely dropped 09-03 through 09-05
  morning** (found via `grep -c "Heartbeat:"` across my own logs when Exec/HOST flagged a real 38-
  hour marker gap — confirmed by direct test that the writer works fine, the step itself had just
  stopped being invoked). The lesson isn't "add the step" — it already existed. It's that a step
  whose omission produces no visible consequence gets silently dropped under load, and the actual
  fix is periodically checking the practice against the log, not re-writing the reminder more
  firmly. If this line is ever removed from carry-forward again, check the logs before assuming
  the practice held.
- **DAILY, CHECKED EVERY FIRE — the omnibus.**
  ```bash
  ls docs/omnibus-logs/[0-9]*.md | tail -1
  ```
  If the latest entry isn't yesterday (or today, once written), that's the fire's top priority.
  Held correctly for its first full day (09-04) since yesterday's fix.
- **A background agent's file-on-disk is provisional until its completion notification confirms
  it, OR its committed line count matches the report exactly.** Verified this explicitly both days
  now (09-03 backfills, 09-04's own) before committing — no repeat of the mid-revision mistake.
- **Verify a flagged discrepancy against the primary source yourself before acting on it or
  passing it along** — did this for the m-45 citation-drift flag today (opened the actual
  methodology file rather than trust the omnibus agent's characterization) before mailing CIO.
- **Cadence/schedule beliefs get re-verified against the canonical doc, never re-propagated from
  my own prior carry-forward wording.**
- **Before starting ANY audit/analysis task on a tracked GitHub issue: `gh issue view --json
  comments` first**, not just the issue body.
- **Omnibus timeline entry formats vary file-to-file** (`**H:MM**:` vs plain `H:MM AM/PM:`) — any
  script parsing timeline entries needs to handle both.
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
- **A `git push` can hit a transient SSH/network timeout** (`kex_exchange_identification`) —
  distinct from a real non-fast-forward rejection; just retry once after confirming the error is
  network-shaped, not a real conflict.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
