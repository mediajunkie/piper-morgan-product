# Docs Carry-Forward

**Updated**: 2026-09-08 ~10:35 PDT (Fire 3 / WORK, complete)
**Session log**: `dev/2026/09/08/2026-09-08-0528-docs-code-log.md` (open; started PM-initiated pre-cron).
**Cron**: `433c7e09`, `57 6,9,12,15,18,21 * * *`, healthy, **re-armed 07:27 today after Gap-C
self-heal** (job vanished silently between its last fire and this one — CronList returned "No
scheduled jobs" despite this fire having just been triggered by it). Expires ~2026-09-15 (7-day
auto-expiry) — watch for a proactive re-arm before then.

Fire 3 was quiet on new work: 1 FYI (Arch's flywheel process update, confirms my Q2 memo received
and correctly queued for synthesis) — triaged, nothing else unblocked.

## Flywheel Q2 — my independent read sent; watching for CIO's and the Arch-led synthesis

This morning: published "More Than Anyone Ever Reported to Me" (PM-initiated pre-cron ask),
proofread clean, live-verified. Medium leg + calendar image-fields gap (flagged by Dispatch-PM,
"first miss in four") fixed same-fire.

**Q2 (joint with CIO, part of Arch-led flywheel re-evaluation)**: read all 52 methodology entries'
full text against Layer 2's 5 practices, spot-verified the load-bearing claims directly, and sent
an independent judgment to Arch cc CIO/Exec/HOST/PPM/CXO/PM before seeing any reply on the thread
(genuinely independent, per Exec's ESSENCE-style ask). **My core finding**: not clean supersession
— uneven. Practice 2 (testing) still stands alone. Practices 1/4 have real content-level updates
in the corpus (m-50 changes what "documented" means, not just adds detail). **Practice 3 is the
real casualty**: its own cited "authoritative reference" (m-02) is self-disclosed historical and
was never actually elaborating Practice 3 even before going stale, the entries that do elaborate
it sit uncited, and m-41 documents the practice's own "session logs" bullet silently broke for
6/9 roles under automation — a near-failure Layer 2 has never been updated to reflect. Recommended
Layer 2 become an explicit index (see-also pointers per practice), Practice 3 needing correction
not just addition, Practice 2 left alone; flagged (not force-categorized) that ~21% of the corpus
is meta-methodology the 3-layer model has no place for.

**Watch, don't chase**: this is Arch-led, scoped work with a stated end (explicitly not a standing
duty-cycle item per Exec's memo) — no further action from Docs unless Arch's synthesis asks for
something specific. Full 52-entry mapping is in hand if requested.

## Day closed clean — nothing outstanding

The day's headline event: both Monday FLY-AUDIT issues (#1725 Weekly, #1724 Monthly Housekeeping)
worked and CLOSED same-day for the first time this cycle — full checkbox-by-checkbox close-issue-
properly treatment on both, 3 real findings filed (#1726/#1727/#1728), ~12 stale-path/format bugs
fixed at the source in the audit-generating workflows themselves. One real mistake (`gh api -f
body=@file` doesn't do curl-style expansion) caught and fixed immediately.

Today's omnibus (`docs/omnibus-logs/2026-09-07-omnibus-log.md`, 292 lines, HIGH-COMPLEXITY:
COORDINATION) covered a genuinely dense day cohort-wide: PM overruled PPM's 5-day FTUX-interview
HOLD and it deployed same-evening with its own multi-role verification chain; the week-long CXO/
CIO methodology corpus thread resolved with methodology-52 filed; #1386's gate scope got corrected
twice in one day. Audited thoroughly given the line count sat below the 450-600 target — unlike
yesterday's first draft, this pass surfaced zero errors on inspection (all 3 canonical methodology
quotes verified character-accurate, my own day's section matched first-hand memory exactly), so
accepted rather than forced a mechanical fourth compression pass. Omnibus (`aab75ec16`) and
activity-log reconciliation (`c4c2df375`) both pushed.

**First action next fire (06:57 tomorrow)**: sync, mail loop (raw `ls`), omnibus currency check
(should read 09-07 as "yesterday," correct), heartbeat step, otherwise genuinely open floor. Watch
for Comms' "More Than Anyone Ever Reported to Me" post (PM's stated priority for tomorrow per
today's omnibus) in case a publish-support ask comes through.

## Both Monday audits (#1725, #1724) worked and CLOSED same-day — first time this cycle

Both fired cleanly on schedule (no #1713 recurrence). Dispatched one thorough background agent
per issue; personally audited both reports against real command output before touching either
issue (verified paths, file staleness, all 3 new issue filings, both YAML diffs); did the full
close-issue-properly treatment (checkbox-by-checkbox, Completion Matrix, closing comment,
staggered-calendar update) rather than a comment-only close; closed both.

**Real findings filed**: #1726 (structural — `last_verified` bulk-stamp re-diagnosed 5 audits
running, zero fix — CIO's lane to pick up), #1727 (10 files, dead legacy-guide links), #1728
(stale `mailboxes/DIRECTORY.md` row). **Real fixes shipped**: both audit-generating workflow
YAMLs corrected at the source (12 combined path/format bugs, months-old, silently worked around
until now), a 5-month-stale `requirements.txt.bak` and a dead stray workflow file removed, a live
customer-facing beta-date overpromise fixed in `docs/README.md`, `BRIEFING-CURRENT-STATE.md`
refreshed, `dev/active/` cut 70→42 (2 wrong moves caught and reverted before finalizing).

**Standing lesson for future multi-agent dispatches**: the two background agents ran concurrently
in this same shared worktree and could have collided (both self-managed it carefully this time,
but I hadn't guarded against it) — use `isolation: "worktree"` next time if dispatching multiple
agents whose file scopes could plausibly overlap in the same role's worktree.

**One real mistake, caught immediately**: `gh api ... -f body=@file` does NOT do curl-style file
expansion — it literally wrote the string as the issue body on the first #1725 update attempt.
Caught by checking the API response, fixed with `gh issue edit --body-file` (the correct form),
used correctly from the start on #1724.

Next Due dates recorded: weekly Sep 14, monthly Oct 5.

## #1713 (GH Actions no-fire defect) — still open, but today is a clean data point

Confirmed directly (REST API) that both Monday workflows fired via `schedule` this time (run IDs
34142935309, 34142667321, both `success`) — no recurrence of the 08-31 silent-no-fire incident.
Asked the #1724 agent to add a brief factual comment to #1713 noting this (not closing it — whether
the underlying question is resolved isn't Docs' call).

Verified directly via `gh issue view`/`gh api` (not the stale cron CONSTANTS block, which keeps
citing these as open): the PRIOR #1712 and #1486 are both CLOSED (09-02/09-03). B3 corpus-
disposition also closed weeks ago. Nothing owed from any of those — today's #1725/#1724 are the
current, live instances.

## Yesterday (2026-09-06) closed clean — for reference

All 6 fires drained. One real user-facing item: fixed the live blog's footer teaser after Comms
flagged a retired duplicate post (`piper-morgan-website` commit `a5ae9e7`). Omnibus
(`docs/omnibus-logs/2026-09-06-omnibus-log.md`, 430 lines, HIGH-COMPLEXITY:COORDINATION) went
through a genuine two-pass audit — first draft under methodology-20's stated floor, sent back and
caught two real content errors on the second pass. Omnibus (`bf7441167`) and activity-log
reconciliation (`1725a3a7c`) both pushed. A new cohort-wide standing rule was noted (sub-25-API-
call probes proceed without asking, Exec/PM-ratified) — low relevance to Docs but recorded.

**First action next fire (06:57 tomorrow)**: sync, mail loop (raw `ls`, not the narrow grep),
omnibus currency check (should read 09-06 as "yesterday," correct), heartbeat step, otherwise
genuinely open floor.

## No unblocked work outstanding right now

Fire 2 drained the day's one real item: Comms flagged (direct-to-docs) that today's scheduled
insight ("Patterns Naming Patterns") was retired same-morning as a duplicate of "This One's Taken"
(PM caught it, commit `47cf4c3b3`), and the live blog's footer teaser on "We Built Onboarding in
Our Own Image" still pointed at the retired title. Fixed `piper-morgan-website`'s
`blog-content.json` (hashId `b0d5a5e718ef`), pushed (`a5ae9e7`), replied to Comms/cc PM. No
Medium/LinkedIn edit path exists — flagged explicitly rather than silently dropped.

Fire 3 was pure mail-loop + housekeeping: Comms' thanks + 4 more FYI-cc on the CXO/CIO/HOST
methodology thread (m-51 filed, standing-item 7q closed via a new NO-SESSION-LOG detector) — none
needed docs action, all triaged. MANIFESTs regenerated. Both genuine standing "Active items"
(PreCompact hook locality differentiation; critical-docs YAML-frontmatter upgrade) reviewed and
correctly left deferred — neither's named trigger has fired.

Fire 4 was quiet: empty inbox, both worktrees synced, merge-keeper clean, nothing unblocked.

Fire 5: 1 more FYI-cc on the methodology thread (triaged), plus a new cohort-wide standing rule
worth remembering — **Exec, PM-ratified 2026-09-06: probes/experiments under ~25 API calls proceed
without PM asking first; report the actual cost with the result.** Production data, live-user-in-
the-loop, and never-used-before vendors stay asks regardless of size. Low relevance to Docs'
typical work (mail/CSV/publish, not vendor-API probing) but noted here in case it ever applies —
don't silently forget a cohort-wide norm just because it wasn't addressed to my lane specifically.

**Cron CONSTANTS block is stale again this cycle** (still citing B3 Tier C, #1712, #1486 as owed —
all closed weeks ago, unchanged across Fires 2/3/4 today). Keep verifying against this file rather
than trusting the prompt, as its own text says to.

**First action next fire**: sync, mail loop (raw `ls`, not the narrow grep), omnibus currency
check, run the heartbeat step explicitly, otherwise genuinely open floor.

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
