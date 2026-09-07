# Docs Carry-Forward

**Updated**: 2026-09-07 ~10:35 PDT (Fire 2 / WORK — two audit agents dispatched, in progress)
**Session log**: `dev/2026/09/07/2026-09-07-0727-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy, next fire 12:57.

## IN PROGRESS: 2026-09 Monday audits (#1725, #1724) — background agents dispatched, awaiting audit

Both Monday auto-audits fired cleanly today (no #1713 recurrence — genuinely good news, noted as
such rather than assumed). Fresh issues: **#1725** (Weekly Docs Audit, 74 items) and **#1724**
(Monthly Housekeeping, 33 items). Given both checklists' own precedent (#1712 took 3 days; the
Weekly checklist's FAQ explicitly says "can span multiple days if needed"), dispatched one
thorough background agent per issue rather than rush or silently defer. Both instructed to work
every section with real evidence, file real GitHub issues for real findings, fix quick things
directly, use REST over GraphQL (today's shared cohort GitHub API pool has been intermittently
rate-limited), and NOT close their issue or touch the staggered audit calendar — that's mine to do
after personally auditing each report (line-by-line evidence check, same discipline as the
omnibus audits this week).

**NEXT ACTION when each agent completes**: audit its report against the precedent set by #1712's
and #1486's own closing comments (ratios not lists, real fixes vs. filed issues vs. explicitly
out-of-lane, honest accounting of anything not done) before touching either issue's description,
Completion Matrix, or the staggered audit calendar. Do not trust a "done" claim without evidence
in the report, same discipline as the 09-06 omnibus audit.

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
