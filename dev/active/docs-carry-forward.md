# Docs Carry-Forward

**Updated**: 2026-09-28 17:33 PDT, verified via `date`.

**Weekly Docs Audit #1903 — CLOSED.** Full checklist worked (briefing refreshed, 4 mechanical
subagent checks, all direct checks) across the 11:27 and 17:27 fires, interrupted mid-close by a
real account-wide GitHub API rate limit (confirmed genuine, cleared by 17:27). Filed **#1904**
(3 procedural docs 300+ days stale). Closed via `close-issue-properly`, verified `state: CLOSED`.
Staggered audit calendar updated, Next Due Oct 5.

✅ **CIO confirmed alive and closed the loop** — the 24h+ silence was a genuine 29-hour LaunchAgent
restore-mechanism gap (no tick reached the seat 09-27 11:1x→09-28 16:07), not a discipline lapse.
My finding was correct; CIO reported two real findings to Pard about the restore step. No further
action needed.

✅ **Cadence question fully resolved (for real this time) — hold at 7x/day, no further flip expected
without an explicit new signal.** Full arc today: reverted 4x/day→7x/day at START (correct) →
Exec's "through Monday" ruling said re-throttle to 4x/day (complied) → Exec retracted that ruling
(PM told Lead "Monday ok" *before* Exec's ruling went out) → re-reverted to 7x/day (job `cb3c489e`,
current). **If another cadence memo arrives, read it as potentially superseding this — don't assume
today's history means the question can't move again.**

**PM directive still standing: do NOT self-throttle on approved/real work.**

## Active threads

- **Personhood/attribution division of labor with Comms — PROVEN across 3 pieces now** (2 on 09-26,
  1 on 09-27/Ship #062). Comms owns `template-audit` check #11 at draft time; I own an independent
  re-check at proofread time. **Keep doing this on every future proofread** — it has caught real,
  distinct misses on both sides every time it's been used, not a one-off.
- **"Three Seats Stay Dark Longer" — queued, awaiting 09-29 pubDate.** Re-sync and re-verify fresh
  at actual publish time, don't trust the 09-26 proofread as still-current.
- **"Weekly Ship #062: Says What It Can Do" — queued, awaiting 09-30 pubDate.** Full independent
  audit clean (09-27). Re-sync and re-verify fresh at publish time, same discipline.
- **"A Primary Log Can Be Wrong, Not Just Incomplete" — published + distributed, 09-27.** Fully
  closed out (blog, Medium, LinkedIn all live, content-verified; alt-text correction propagated).
  One small flag left for Comms: the calendar's own `altText` column for this row is still stale
  (Comms-owned, not touched by me) — mention next contact.
- **"A Fix Needs the Same Rigor as the Claim It Fixes" — published + distributed, 09-26.** Fully
  closed out. Same small stale-column flag for Comms (the `caption` column, period vs. question
  mark) — not urgent, mention next contact alongside the above.
- **Next piece in the pipeline**: "What Piper Morgan Actually Is, Ratified Then Corrected Twice"
  (10-01), currently `drafted`, not yet `ready-for-docs`. Not mine to chase — watch for Comms'
  publish-ready memo.
- **ROSTER.md scoped for cross-project boundary, 09-27** — done, replied to Janus, no further
  action. (Historical note only.)
- **Git-attribution incident (Pard's) — fully resolved, purely historical.** No further action.

## Watch surfaces (owned by others, checked periodically — don't re-derive, don't chase)

- **`last_verified` bulk-stamp cluster** — CIO's lane (#1726). Check at tomorrow's Weekly Docs
  Audit (09-28 — due today per the day-of-week trigger, see below).
- **#1644** — roadmap.md full historical fold, PPM's lane. Not mine to force.
- **#1683** — 2 inverse-case calendar rows need real Medium verification, not guessing.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call.
- **#1710/#1847** — pattern-catalog Status-field frontmatter regression, routed to CIO/Arch.
- **#1720/#1721** — filed by me, triaged by PPM into FLYWHEEL. Watch for progress.
- **CXO's marker-provenance-field finding** — CIO's lane. Watch for the fix landing.
- **CIO's deferred heartbeat corroborating-check** (stale-marker-but-real-commits case) — deferred
  to Monday 09-28 per the throttle. Watch for it landing today, don't implement it myself.
- **GitHub issue backlog health**: report as a ratio at each audit, not mine to triage individually.

## Owed by me — unblocked, low priority

- **PreCompact hook locality differentiation** (owed since May) — real design work, scoping before
  implementing, not a same-fire patch.
- **"Two of Me" art-audit gap** — publish audit checks image existence/dimensions but not
  image-content-matches-alt-text. No process fix yet, not urgent.
- Owed by Web: `piper-morgan-website#37` publish Step 9 automation. Not urgent.
- `knowledge/piper-morgan-glossary-v1.1.md` needs CXO's tracked-state frontmatter at first
  substantive touch. Not urgent.
- **Agent 360 v0.5** (`dev/2026/09/25/agent-360-questionnaire-v0_5.md`) — HOST fielded 09-25,
  ~2-week window. Deliberately deferred to a dedicated future fire — named trigger: a fire with
  room to actually think it through, not "no rush."
- **Note to Comms** (batch both): stale `caption`/`altText` columns on two recently-published rows
  (see Active Threads above). Not urgent, mention next contact.

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits blocking `git pull --ff-only` in PM's own checkout. **Do not act on this
without PM present.**

## Day-of-week duty triggers — check every START

- **Every Monday**: Weekly Docs Audit — #1844 closed 09-21; **next due TODAY, 09-28.**
- **First Monday of month**: Monthly Housekeeping — #1724 closed 09-07; next due 10-05 (not today,
  09-28 is not the first Monday).
- **First Tuesday**: Skill-Candidates Review — not mine.
- **Every START**: omnibus production + missing/unclosed-log nudge (Step 1d, PM ruling 09-25) —
  produce/verify the prior day's omnibus; nudge any role whose log lacks a genuine closing marker.

## Standing operating knowledge (current rules, not incident history)

- **At every proofread, re-run `template-audit`'s full 16-check list myself, including check #11**
  — don't just read Comms' publish-ready memo and trust "clean." Proven 3-for-3 this week catching
  real, distinct misses on both sides.
- ⚠️ **Check line endings (`xxd`/`file`) on any UNFAMILIAR CSV before writing with the `csv`
  module** — `piper-morgan-website`'s `data/blog-metadata.csv` uses CRLF; a default
  `lineterminator='\n'` silently rewrote all 395 rows (786-line diff for a one-field fix), caught
  via `git diff --stat` before it mattered further. The product repo's own calendar CSV uses LF and
  is fine with the existing pattern — this is about files you haven't touched before, not a
  blanket change to how the calendar gets edited.
- ⚠️ **Emit the heartbeat every fire** — chained onto the same closing block as the final push of
  each work unit. Held clean through all of 09-26 (after the fix) and all of 09-27 — genuinely
  looking solid now, but keep watching.
- **GitHub-criteria line** (third work-queue source): `gh issue list --search "label:documentation"
  --state open --limit 50` — open each result, don't trust the list view.
- **PM crossposts to Medium/LinkedIn manually.** When PM provides a syndication URL, record it
  (mediumURL/linkedinURL/status→distributed) — not a delegated pipeline step.
- **Only cc PM on memos that** (a) contain a decision only PM can make, (b) relay a PM ruling, or
  (c) contain something PM would want to contradict.
- A subagent's/colleague's self-reported verification pass is a claim, not a fact — re-verify the
  artifact yourself every time.
- A live-page 200 status can be a stale cached shell — always do an actual content check after the
  200; `curl -s` doesn't follow redirects by default, add `-L`.
- A naive `cut -d','` on a CSV with quoted fields silently misaligns columns — use the `csv` module
  for any real read, not just writes.
- `mail-send.sh` needs BOTH the old (deleted) and new (moved-to) path passed for a triage move.
  Doesn't advance local HEAD — `git merge origin/main` before assuming a triaged file "didn't move."
- `gh issue list` defaults to a 30-item limit if `--limit` is omitted.
- Before starting any audit/analysis task on a tracked GitHub issue: `gh issue view --json comments`
  first, not just the issue body.
- A cron cadence change needs BOTH the explicit session-log id-transition note AND the
  `duty-cycle-registry.tsv` row updated in the same commit.
- A duty-cycle sync from earlier in the session is a timestamped fact, not a durable one — re-sync
  if meaningful time has passed, including mid-conversation with PM directly engaged.
- "Last scheduled fire of today" is arithmetic on the cron expression, not a feel-based judgment.
- A fire is a WAKE, not a time-box — drain unblocked work.
- **Writing directly to `mediajunkie/designinproduct/docs/mail/` is the preferred route for
  anything addressed to Janus.** For Pard, the real inbox is `~/Development/mediajunkie/docs/mail/`
  (NOT `mailboxes/pard/`, gravestoned and hard-refused by `mail-send.sh`) — sync that repo first,
  stage only your own file by explicit path.
- **Never csv-round-trip `dev/active/duty-cycle-registry.tsv`** — use targeted plain-text line
  replacement (match on the `role\t` prefix).

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.
