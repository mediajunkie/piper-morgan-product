# Docs Carry-Forward

**Updated**: 2026-09-09 ~10:35 PDT (Fire 3 / WORK, complete)
**Session log**: `dev/2026/09/09/2026-09-09-0609-docs-code-log.md` (open; started PM-initiated pre-cron).
**Cron**: `433c7e09`, `57 6,9,12,15,18,21 * * *`, healthy. Expires ~2026-09-15 (7-day auto-expiry)
— watch for a proactive re-arm before then, and watch whether Gap-C recurs.

## Today so far: Weekly Ship #059 published + syndicated, both legs

PM-initiated pre-cron ask to publish today's Ship. Proofread clean (independently verified, not
just trusted Comms' report); one real timing snag — the first "200 OK" was a stale cached
not-found fallback, resolved with more propagation wait, confirmed live via actual content check.
LinkedIn leg (the whole syndication obligation for `ship` theme) landed same-morning, calendar
updated to `distributed`. Self-caught a real triage lapse: forgot to move Comms' original
PUBLISH-READY memo to `read/` after acting on it directly — fixed at the next fire's mail loop,
exactly the failure shape my own standing lesson already named.

**Two real gotchas from today, added to Standing practices below**: (1) a commit combining a
`git mv`-staged rename with separately-staged modifications can silently commit only the rename
— now observed twice, always verify `git status` after committing, not just a clean exit; (2) a
live page's 200 status can be a stale cached not-found fallback — always do a real content check.

**Watch, not chase**: Ship #058's own calendar row has `canonicalSite=distributed` with an empty
`linkedinURL` — a pre-existing data gap noticed in passing, out of scope for today's task.

## Watch: `<figure>`/`<figcaption>` markup proposal — spec sent to Web, not urgent

Dispatch-PM proposed standardizing captioned-image markup (real accessibility gap + a documented
07-16 incident). Web shipped the hero-image half same-day. I own the in-body-teaser half:
investigated the actual `convertToHtml()` mechanism directly (source-adjacency, not renderer
drift), confirmed my own authoring convention already matches what's needed, and sent Web a
concrete implementable spec rather than leave it abstract. Explicitly not urgent — genuinely
watch, not chase, until Web has bandwidth. **Note for future mail loops**: the original proposal
never actually landed in my own inbox despite being cc'd (found it by reading Web's `read/`
folder directly) — worth a light watch for whether this is a one-off or a cross-project cc
delivery gap worth flagging if it recurs.

## Day closed clean — headline: full flywheel re-evaluation arc + a real publish, same day

Published "More Than Anyone Ever Reported to Me" (PM-initiated pre-cron), self-healed a dead cron
(Gap-C), fixed a real syndication-metadata gap. Sent an independent Q2 read for the PM-approved
Excellence Flywheel re-evaluation — verified as one of the exercise's genuine three-way
independent convergences (Practice 3's rewrite). Caught and corrected a real misattribution (D5)
before it reached PM. Today's omnibus (`docs/omnibus-logs/2026-09-08-omnibus-log.md`, 483 lines,
HIGH-COMPLEXITY:COORDINATION) covered the full same-day flywheel arc (kickoff → 5 independent
reads → 7-decision synthesis → active challenge round → v3.0.1 amendments → a still-unresolved
finding that the amendments landed only in a footer, not the enforcement table itself — audited
and confirmed accurate by reading the primary file directly) plus a 6-role PM-test-round fix
chain. Clean first-pass audit this time (unlike the prior two days, no second compression round
needed). Omnibus (`85f4de376`) and activity-log reconciliation (`cd5c52b6a`) both pushed.

**First action next fire (06:57 tomorrow)**: sync, mail loop (raw `ls`), omnibus currency check
(should read 09-08 as "yesterday," correct), heartbeat step. Watch for the flywheel challenge
round closing (09-09 EOD) and whether the table-vs-footer finding gets resolved — not mine to fix,
just worth checking if it lands in v3's final text before it goes to PM.

**New cohort-wide standing rule (Exec, PM-ratified 2026-09-06, still in force)**: probes/
experiments under ~25 API calls proceed without PM asking first; report the actual cost with the
result. Production data, live-user-in-the-loop, and never-used-before vendors stay asks regardless
of size. Low relevance to Docs' typical work but noted in case it ever applies.

## Watch surfaces (things owned by others, checked periodically)

- **`last_verified` bulk-stamp cluster**: 24/38 as of 09-07's audit (#1725) — unchanged from 09-03,
  structural fix now filed as #1726 (CIO's lane) rather than re-escalated each audit. Check again
  at the next Weekly Docs Audit (09-14).
- **Flywheel re-evaluation v3** (Arch-led) — challenge round closes 09-09 EOD; a live finding as of
  09-08 EOD is that v3.0.1's enforcement-column fixes landed only in an amendment footer, not the
  actual table (CXO's catch, personally verified). Watch whether this lands in the final v3 text
  before it reaches PM — not mine to fix, just worth checking.
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

- **Every Monday**: Weekly Docs Audit — #1725 closed same-day 09-07 (first time this cycle); next
  due 09-14. #1713 (GH-Actions no-fire defect) confirmed clean on 09-07 — still open as a question,
  watch for recurrence.
- **First Monday of month**: Monthly Housekeeping — #1724 closed same-day 09-07; next due 10-05.
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).

(The omnibus is deliberately NOT on this list — it's a daily check, not a day-of-week trigger.)

## Standing practices (apply at every fire, not just START)

- **A commit that includes a `git mv`-staged rename alongside separately-staged file
  modifications can silently commit only the rename** — now observed twice (09-06's footer fix
  publish, 09-09's Ship #059 publish), same shape both times: `git status` shows everything
  staged immediately before the commit, but the commit only picks up the renamed file. Always
  verify via `git status` *after* the commit, not just a clean exit code — fix is a simple
  re-add + separate commit, cheap once caught, but easy to miss if not checking.
- **A live-page 200 status can be a stale cached not-found fallback, not a real render** — hit
  this on the Ship #059 publish: `x-vercel-cache: PRERENDER` served instantly with `title: "Ship
  Not Found"` embedded. Always do an actual content check (title/image/body-text fragment) after
  the 200, and if it fails, don't assume broken — compare response headers against a known-good
  page of the same type first; this one resolved with more propagation time, not a fix.
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
