# Docs Carry-Forward

**Updated**: 2026-09-29 ~08:15 PDT, verified via `date`.

**09-28 closed cleanly, 09-29 in progress.** 09-28 omnibus built (13 sessions, HIGH-COMPLEXITY:
COORDINATION, `docs/omnibus-logs/2026-09-28-omnibus-log.md`) — all 11 core roles' logs carried a
real `DAY-CLOSED` marker, no nudge needed. Activity-log reconciled (+13 rows, verified exact).
**"Three Seats Stay Dark Longer" PUBLISHED and live-verified** by actual body content (not just
status code) at `https://pipermorgan.ai/blog/three-seats-stay-dark-longer/` — calendar updated
(status→published, blogURL/blogPath set), draft archived to `drafts/published/`. Session Objective
#3 for today, complete. Both worktrees clean, everything on `origin/main`. Cron unchanged (normal
7x/day, `973d1bab` — **no throttle in effect, cadence question fully resolved as of 09-28 evening**).

**PM directive still standing: do NOT self-throttle on approved/real work.**

**Website deploy note (new, 09-29)**: the site is Vercel-deployed (confirmed via response headers
on a known-live post); the GitHub Actions "Deploy Piper Morgan Website to GitHub Pages" workflow in
that repo is stale/unused — last run 2026-07-21, not the actual deploy mechanism. Don't check `gh
run list` there for deploy status; live-verify by actual body content after a short poll instead
(a fresh publish took ~2 minutes to go live this morning, 404→200 with real content).

## Active threads

- **Personhood/attribution division of labor with Comms — PROVEN across 4 pieces now, keep using
  it** (Comms owns `template-audit` check #11 at draft time; Docs owns an independent re-check at
  proofread time on every future proofread — "Three Seats..." re-check this morning found check #11
  clean, consistent with the 09-26 record).
- **"Weekly Ship #062: Says What It Can Do" — queued, awaiting 09-30 pubDate (tomorrow).** Full
  independent audit clean (09-27). Re-sync and re-verify fresh at publish time, same discipline —
  don't trust an earlier proofread as still-current.
- **#1904 filed (mine, 09-28)**: 3 procedural docs (`TESTING.md`, `database-production-setup.md`,
  `api-key-management.md`) 300+ days stale, describing pre-Fly-migration state as "Production
  Ready." Not mine to fix (needs technical verification against current code) — watch for
  disposition, don't chase.
- **Two stale Comms-owned calendar columns — memo sent 09-29** (`mailboxes/comms/inbox/note-docs-
  to-comms-two-stale-calendar-columns-2026-09-29.md`), cleared from my owed-items list. Watch for
  Comms picking it up, not mine to chase.
- **Next piece in the pipeline**: "What Piper Morgan Actually Is, Ratified Then Corrected Twice"
  (10-01), currently `drafted`, not yet `ready-for-docs`. Watch for Comms' publish-ready memo.

## Watch surfaces (owned by others, checked periodically — don't re-derive, don't chase)

- **`last_verified` bulk-stamp cluster** — CIO's lane (#1726). 13 of 38 clustered on the identical
  2026-06-19 stamp as of 09-28's audit (down from 14 at 09-21). Check again at next Weekly Docs
  Audit (10-05).
- **#1644** — roadmap.md full historical fold, PPM's lane. 16 days stale as of 09-28's audit,
  reported not fixed. Not mine to force.
- **#1683** — 2 inverse-case calendar rows need real Medium verification, not guessing.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call.
- **#1710/#1847** — pattern-catalog Status-field frontmatter regression, routed to CIO/Arch.
- **#1720/#1721** — filed by me, triaged by PPM into FLYWHEEL. Watch for progress.
- **CXO's marker-provenance-field finding** — CIO's lane. Watch for the fix landing.
- **CIO's 8c heartbeat corroborating-check** — shipped 09-28 per CIO's own log (v0.16, past-
  threshold readings now annotated with real post-invocation commits). Confirmed landed, no
  further watch needed.
- **CIO's/Pard's LaunchAgent restore-mechanism follow-up** — CIO flagged two real findings to Pard
  (no named trigger on the restore step; a disarmed seat reads as dead, `parked:` state should be
  used at disarm time). Watch for either landing, not mine to implement.
- **GitHub issue backlog health**: 217 of 288 open issues (75%) have had no activity in 30+ days,
  as of 09-28's audit — report as a ratio at each audit, not mine to triage individually.
- **#1901** — a real new bug (unarmed-offer rewriter mangling a compound question), unmilestoned
  as of 09-28. Not Docs' lane to triage.

## Owed by me — unblocked, low priority

- **PreCompact hook locality differentiation** (owed since May) — real design work, scoping before
  implementing, not a same-fire patch.
- **"Two of Me" art-audit gap** — publish audit checks image existence/dimensions but not
  image-content-matches-alt-text. No process fix yet, not urgent.
- Owed by Web: `piper-morgan-website#37` publish Step 9 automation. Not urgent.
- `knowledge/piper-morgan-glossary-v1.1.md` needs CXO's tracked-state frontmatter at first
  substantive touch. Not urgent.
- **Agent 360 v0.5** (`dev/2026/09/25/agent-360-questionnaire-v0_5.md`) — HOST fielded 09-25.
  Deliberately deferred to a dedicated future fire — named trigger: a fire with room to actually
  think it through, not "no rush." Getting toward the edge of the ~2-week window (fielded 09-25,
  so due ~10-09) — pick a genuinely quiet fire for this soon, don't let the window lapse silently.
- **Note to Comms** (batch both): stale `caption`/`altText` columns on two recently-published rows
  (see Active Threads above).

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits blocking `git pull --ff-only` in PM's own checkout. **Do not act on this
without PM present.**

## Day-of-week duty triggers — check every START

- **Every Monday**: Weekly Docs Audit — #1903 closed 09-28; next due 10-05.
- **First Monday of month**: Monthly Housekeeping — #1724 closed 09-07; next due 10-05 (same day
  as next Weekly Audit — both land 10-05, per the calendar's own noted "worst case" combination).
- **First Tuesday**: Skill-Candidates Review — not mine.
- **Every START**: omnibus production + missing/unclosed-log nudge (Step 1d, PM ruling 09-25) —
  produce/verify the prior day's omnibus; nudge any role whose log lacks a genuine closing marker.

## Standing operating knowledge (current rules, not incident history)

- **At every proofread, re-run `template-audit`'s full 16-check list myself, including check #11**
  — don't just read Comms' publish-ready memo and trust "clean." Proven 3-for-3 this week.
- **Check line endings (`xxd`/`file`) on any UNFAMILIAR CSV before writing with the `csv` module**
  — `piper-morgan-website`'s `data/blog-metadata.csv` uses CRLF; a default `lineterminator='\n'`
  silently rewrote all 395 rows once already. The product repo's own calendar CSV uses LF and is
  fine with the existing pattern.
- **A "silent, account-wide GitHub API rate limit" is real and distinct from an exhausted personal
  quota** — verify via `gh api rate_limit` (checks primary quota) before assuming either way; if
  primary quota is healthy but `gh` commands still fail with a rate-limit error, that's the
  secondary/abuse limit, not something to route around — wait and retry.
- ⚠️ **Emit the heartbeat every fire** — chained onto the same closing block as the final push of
  each work unit. Holding clean for 3 straight days now.
- **GitHub-criteria line** (third work-queue source): `gh issue list --search "label:documentation"
  --state open --limit 50` — open each result, don't trust the list view.
- **PM crossposts to Medium/LinkedIn manually.** When PM provides a syndication URL, record it —
  not a delegated pipeline step.
- **Only cc PM on memos that** (a) contain a decision only PM can make, (b) relay a PM ruling, or
  (c) contain something PM would want to contradict.
- A subagent's/colleague's self-reported verification pass is a claim, not a fact — re-verify the
  artifact yourself every time. **Verify a subagent's own findings too, not just its existence as a
  report** — spot-checking the 09-28 audit subagents' claims directly (not just trusting their
  self-reported "clean") is what surfaced real evidence rather than passing along an unverified
  summary.
- **After issuing a `gh issue close` (or any state-changing command), verify the actual resulting
  state directly** (`gh issue view --json state`) rather than trust the command's exit code alone.
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
- **A ruling can be retracted or superseded same-day — don't assume today's history means a
  question can't move again.** The cadence question flipped 3 times on 09-28 alone; each flip was
  a correct response to the then-current instruction, not a mistake to have avoided.
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
