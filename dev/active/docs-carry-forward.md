# Docs Carry-Forward

**Updated**: 2026-09-11 ~22:30 PDT (21:57 fire — day-close in progress). 16 session logs today
(11 roles + 5 prog delegations) — HIGH-COMPLEXITY day. Omnibus synthesis dispatched to a
background agent following full methodology-20; STOP heartbeat run and pushed. Inbox was empty at
STOP. Next: personal audit of the draft, Step 10 archive + Step 10.5 CSV reconciliation, trim this
file, `<!-- DAY-CLOSED: 2026-09-11 -->` marker.
**Session log**: `dev/2026/09/11/2026-09-11-0623-docs-code-log.md` (open).
**New standing practice, effective immediately**: only cc PM (`xian (ceo)`) on memos that (a)
contain a decision only PM can make, (b) relay a PM ruling, or (c) contain something PM would want
to contradict — everything else reaches PM via the attention rollup. Per Exec's 09-11 proposal
memo relaying PM's own words; Exec is holding to it starting today regardless of when CIO formally
updates the skill, and I'm doing the same.
**NO-SESSION-LOG race — RESOLVED (mostly)**: CIO shipped a 10-min grace-window fix (`5ab4a021a`)
same day, but CXO's immediate follow-up found the *original* catch was also false (belt 0-for-2)
and that one real sample already exceeds the new grace window (24-sample measurement). CXO's
proposed real fix: move the skill's Step 0 START-log commit before the mail loop — exactly my own
seat's existing practice, now proposed cohort-wide. CIO owns the skill edit; watch whether it lands.
**Flywheel v3 — fully closed.** Verified directly: my P1/P5 pointer lists and the m-49 correction
all landed verbatim in `methodology-00-EXCELLENCE-FLYWHEEL.md` (CIO's commit `bfd1445bc`). Nothing
further on this workstream, ever — drop from future carry-forwards after today.
**Cron**: `433c7e09`, `57 6,9,12,15,18,21 * * *`, healthy. Expires ~2026-09-15 (7-day auto-expiry)
— watch for a proactive re-arm before then, and watch whether Gap-C recurs.

## Today (09-11) so far — published + syndicated "The Mailbox Trust Violation," flywheel v3 RATIFIED, big cross-cutting mail thread

PM engaged directly at session start (before the 06:57 cron fire): yesterday's scheduled post
never finished (PM's phone image-upload issue), Comms reviewed it overnight, mine to proofread and
publish. Did an independent proofread (not a rubber-stamp of Comms' two passes) — template/voice
guide read fresh, acronym-lint clean (ROLE-GLOSS advisories are expected false positives for this
narrative register), footer tease verified against the live calendar, image verified thematically.
Published (hashId `defb143fe6eb`, `--work-date 2026-08-09`), archived draft to `drafts/published/`,
live-verified via actual rendered content (not just a 200 — see gotcha below). Dispatch-PM
syndicated to Medium same morning; caught and corrected a real error in their proposed `altText`
value by checking three independent sources directly (see Standing practices).

**Flywheel v3 is RATIFIED** — PM approved the Layer 2 text this morning, five days after naming the
feeling that started the re-evaluation. My own piece (P1/P5 pointer lists, the m-49 catch) already
landed 09-10; nothing further owed. CIO applies to canon; the workstream formally closes.

**PM ruled on the work-queue definition** — carried work + mail + newly-observed GitHub issues
meeting role-relevant criteria, idle only when all three are empty — and explicitly named Docs
("the recurring Docs audit and any issues generated from an audit"). Validates what I already do
(picking up hook-flagged audit residuals like #1727); nothing new for me to implement, CIO owns the
mechanical skill change.

**Filed Ship #060's workstream report** (Exec's kickoff this time explicitly included Docs in the
`to:` list, not just cc) — window Fri 09-04–Thu 09-10, Docs-POV per the standing scope memory, all
cited figures re-verified directly (omnibus line counts re-`wc -l`'d, #1725/#1724 facts re-grepped
from source, hashIds re-checked against the live website CSV) rather than recalled from memory.

**Contributed a datapoint to the fire-heading/"next fire" cohort thread** — named twice by PA and
CXO as the seat uniquely positioned to judge whether wake-shaped headings cost real effort (I build
the omnibus from all 11 roles' logs daily). Measured my own logs directly: "next fire" phrase
dropped to zero unprompted from 09-06 on; `Fire N` headings present and wake-shaped same as the
other three seats reporting. Added the omnibus-consumer angle nobody else could supply.

## 09-10 closed (full detail: that day's session log + `docs/omnibus-logs/2026-09-10-omnibus-log.md`)

Flywheel v3 text completed (my P1/P5 pointer lists + a real m-49 catch). Closed #1727+#1742 (13
dead links). Two process defects closed at the class level: `cleanup-dev-active` v1.2 (live-artifact
guard) and confirmed CXO's MANIFEST.md `mail-send.sh` false-positive on a second seat. Omnibus
(529 lines) personally audited, zero discrepancies. Ship #058's `linkedinURL` calendar gap and the
cross-project cc-delivery watch item both still single-instance, not worth escalating.

## Watch surfaces (things owned by others, checked periodically)

- **`last_verified` bulk-stamp cluster**: 24/38 as of 09-07's audit (#1725) — unchanged from 09-03,
  structural fix now filed as #1726 (CIO's lane) rather than re-escalated each audit. Check again
  at the next Weekly Docs Audit (09-14).
- **Flywheel v3 ratification** (Arch-led) — text complete as of 09-10 morning, awaiting PM's word;
  CIO applies to `methodology-00-EXCELLENCE-FLYWHEEL.md` on ratification. Not yet landed as of
  09-10 EOD (verified directly against `decisions.log`). Watch, don't chase.
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
- **`mail-send.sh`'s half-pushed-move check false-positives on any manifest-only send** —
  `MANIFEST.md` exists permanently in both `inbox/` and `read/` as separate regenerated indexes,
  never a moved memo, so the sibling always "exists" and the check always warns. Confirmed on my
  own seat 09-10 (CXO found it first 09-09) via `git diff origin/main -- <path>` empty + clean
  `git status`. Lead owns the one-line fix (`mail-send.sh`); until it lands, a lone
  `MANIFEST.md STRANDED` warning after a manifest regen is expected noise, not a real strand —
  still verify with the diff/status check before assuming, don't just suppress the warning.
- **A `git mv`-staged rename is NOT enough for `mail-send.sh` — pass BOTH the old and new paths
  explicitly, every time, not just the destination.** Git's local rename detection has nothing to
  do with what `mail-send.sh` pushes (it builds the commit from explicit paths against
  `origin/main` via `commit-tree`). Hit this for real (not the MANIFEST.md false-positive class)
  09-11: passed only 7 `read/` destination paths, stranded all 7 `inbox/`-side deletions — confirmed
  real via `git diff origin/main`, fixed by resending with both sides.
- **A cc'd memo needs a physical copy in every named recipient's inbox, not just the `to:`
  recipients' — `mail-send.sh`'s own `#1716` warning catches this if you miss it, but check before
  sending, not after.** Missed 8 of 9 cc'd roles on a broadcast 09-11, caught by the warning,
  fixed by copying to all named inboxes and resending.
- **`curl -s` does not follow redirects by default — a page behind a 301/308 (e.g. a trailing-slash
  normalize) will make a `curl -s -o file && grep` poll loop forever**, saving the tiny redirect
  body every time and never matching real content. Always add `-L`, or check headers first with
  `curl -sD -` before trusting a poll loop's absence of output. Cost 27 minutes of a stuck
  background task 09-11 before caught via `TaskOutput` showing `running` far past a normal
  deploy-propagation window.
- **`cleanup-dev-active` now has a mandatory Step 2.1 live-artifact/active-use guard** (v1.2,
  09-10) — before filing anything to the forensic archive, check for a published-artifact
  reference and recent-commit activity; either fires, hold in `dev/active/` instead. Apply this
  myself on every future cleanup pass, not just cite it as history.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
