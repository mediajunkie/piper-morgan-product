# Docs Carry-Forward

**Updated**: 2026-09-06 ~10:35 PDT (Fire 2 / WORK, complete)
**Session log**: `dev/2026/09/06/2026-09-06-0727-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy, next fire 12:57.

## No unblocked work outstanding right now

Fire 2 drained the one real item of the day: Comms flagged (direct-to-docs) that today's scheduled
insight ("Patterns Naming Patterns") was retired same-morning as a duplicate of "This One's Taken"
(PM caught it, commit `47cf4c3b3`), and the live blog's footer teaser on "We Built Onboarding in
Our Own Image" still pointed at the retired title. Fixed `piper-morgan-website`'s
`blog-content.json` (hashId `b0d5a5e718ef`), pushed (`a5ae9e7`), replied to Comms/cc PM. No
Medium/LinkedIn edit path exists — flagged explicitly rather than silently dropped. Full 7-item
inbox (1 direct + 6 FYI-cc on the CXO/CIO/HOST provenance thread) triaged to `read/`.

**First action next fire**: sync, mail loop, omnibus currency check, run the heartbeat step
explicitly, otherwise genuinely open floor.

## Watch surfaces (things owned by others, checked periodically)

- **`last_verified` bulk-stamp cluster**: 14/38 as of 09-03 — check again at next Monday audit
  (09-07).
- **#1644** — roadmap.md full historical fold still owed (PPM's lane). Not mine to force.
- **#1683** — 2 inverse-case calendar rows need real Medium verification, not guessing.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call.
- **GitHub issue backlog health**: 322 open (as of 09-03), 168 stale >30 days, 17 without
  milestone — reported as a ratio in #1712, not mine to triage individually.
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
  Then note it in the fire's log entry. Held correctly every fire since being re-added 09-05
  morning — confirmed the marker updates even when the row itself is suppressed (CIO's fix
  working as designed). Don't let this line disappear from carry-forward again without checking
  the logs first.
- **EVERY FIRE — the omnibus.**
  ```bash
  ls docs/omnibus-logs/[0-9]*.md | tail -1
  ```
  If the latest entry isn't yesterday (or today, once written), that's the fire's top priority.
  Chain now continuous 6 days straight (08-29 backfilled through 09-05 all committed).
- **A background agent's file-on-disk is provisional until its completion notification confirms
  it, OR its committed line count matches the report exactly.** Verified this explicitly every day
  this week before committing an omnibus.
- **Verify a flagged discrepancy against the primary source yourself before acting on it or
  passing it along.**
- **Cadence/schedule beliefs get re-verified against the canonical doc, never re-propagated from
  my own prior carry-forward wording.**
- **Before starting ANY audit/analysis task on a tracked GitHub issue: `gh issue view --json
  comments` first**, not just the issue body.
- **A naive `cut -d','` on a CSV with quoted fields containing commas silently misaligns columns**
  — use the `csv` module for any real read, not just writes. Found this caused a real (low-stakes)
  metadata error in a prior publish.
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
  rename** — always `git diff --cached --name-status` after staging a move, and stage everything
  in one call without an intervening reset when archiving a publish.
- **`gh issue list` defaults to a 30-item limit if `--limit` is omitted** — always pass an explicit
  high limit for any total-count claim.
- **`mail-send.sh` does not advance local HEAD** — `git merge origin/main` before assuming a
  triaged file "didn't move."
- **CC copies with a `cc-` filename prefix trigger a soft mail-send.sh warning** even though
  delivery is correct — verify via direct `ls`/`diff` before treating it as a real failure.
- **A `git push` can hit a transient SSH/network timeout** — distinct from a real non-fast-forward
  rejection; just retry once after confirming the error is network-shaped.
- **After acting directly on a memo during a PM-engaged session, still move it to `read/` before
  moving on** — a memo already-actioned-but-not-triaged looks identical to an ignored one from
  outside, and the next fire's mail-loop scan is what catches it.
- **`scan-inbox.py | grep "to:\s*docs"` misses cc-only mail** — found 09-06 when the SessionStart
  hook reported `docs:7` unread against a grep result of 1. The grep pattern only anchors on the
  `to:` field; mail where docs is purely `cc:` (common on multi-role threads) doesn't match. When
  the hook's unread count disagrees with the grep, trust the hook and check `MANIFEST.md` or
  `ls mailboxes/docs/inbox/` directly rather than the narrower filtered scan.
- **`mail-send.sh` can hit a `PreToolUse` hook error (not a legitimate block) when your own local
  index still holds staged `mailboxes/` renames from a prior `git mv`** — `check-branch.sh` checks
  `git diff --cached --name-only` on a non-main branch and errors out rather than either passing
  cleanly or printing its normal BLOCKED message. `mail-send.sh` doesn't need local staging at all
  (throwaway index against origin/main) — `git reset HEAD` before sending clears it.
- **Never pass `mail-send.sh` paths via a shell variable built with string concatenation** — word
  splitting can collapse into one argument depending on how the Bash tool invokes the command,
  producing `mail-send: refusing non-mailbox path: <everything>`. Pass each path as its own
  literal argument in the command.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
