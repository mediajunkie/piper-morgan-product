# Docs Carry-Forward

**Updated**: 2026-09-27 05:09 PDT, verified via `date`.

**09-26 closed cleanly.** Session log `dev/2026/09/26/2026-09-26-0521-docs-code-log.md` carries
`<!-- DAY-CLOSED: 2026-09-26 -->` + a full day-arc summary. 6 fires logged (2 at the original 7x/day
cadence, 4 after the throttle cut). Everything on `origin/main`, nothing stranded, both worktrees
clean. Cron re-armed via delete-then-create at STOP (`81bf8501` → `06a62dd9`, same reduced
expression).

**09-27 START done**: 09-26's omnibus built (17 sessions, HIGH-COMPLEXITY), activity-log appended.
**Nudge found a real gap: PA's 09-26 log has no STOP section** despite real later-day activity —
nudged, cc PM. "A Primary Log Can Be Wrong, Not Just Incomplete" published (today's pubDate),
content-verified live.

⚠️ **Cron cadence still cut 4x/day** (`57 4,10,16,22 * * *`, job `06a62dd9`). **Revert to
`57 4,7,10,13,16,19,22 * * *`, threshold_h 7, at Monday 09-28 START** unless told otherwise — this
is now the second day of the cut; don't let it silently become permanent.

**PM directive still standing: do NOT self-throttle on approved/real work — the cadence cut is
about how often I WAKE to check for nothing, not about doing less work when there's real work.**

## Active threads

- **Personhood/attribution division of labor with Comms — ADOPTED AND PROVEN, keep using it.**
  Comms owns `template-audit` check #11 at draft time; I own an independent re-check at proofread
  time. Used for real on 2 pieces same-day (09-26), caught real misses on both sides (my morning
  proofread missed one Comms later caught in a pool-sweep; Comms' "Three Seats" pass missed a HOST
  naming error and a footer-title mismatch my re-run caught). **Do this on every future proofread,
  not just the day it was adopted** — see Standing Operating Knowledge below.
- **"A Primary Log Can Be Wrong, Not Just Incomplete" — PUBLISHED + DISTRIBUTED, 09-27.**
  hashId `40b67c6ea040`. PM caught a wrong hero-image alt text post-publish (fixed source draft via
  admin UI + fixed Medium directly) — propagated to the live site, content-verified. Crossposts
  recorded (Medium/LinkedIn). **Flagged for Comms**: the calendar's own altText column for this row
  is still stale (Comms-owned, not touched by me).
- **"Three Seats Stay Dark Longer" — still queued, awaiting 09-29 pubDate.** Re-sync and re-verify
  fresh at actual publish time, don't trust the 09-26 proofread as still-current without checking.
- **⚠️ PA's 09-26 log has no STOP section, nudged 09-27** — real later-day activity (mail commits,
  a min_machines_running fix Lead references) never made it into the log. Purely informational,
  watch for a reply, not mine to fix.
- **Next piece in the pipeline**: "What Piper Morgan Actually Is, Ratified Then Corrected Twice"
  (10-01), currently `drafted`, not yet `ready-for-docs`. Not mine to chase — watch for Comms'
  publish-ready memo.
- **"A Fix Needs the Same Rigor as the Claim It Fixes" — published + distributed, 09-26.** Fully
  closed out (blog, Medium, LinkedIn all live and content-verified). One small stale item: the
  calendar's Comms-owned `caption` column still holds an old period-ending version vs. the draft's
  current question-mark version — not urgent, mention to Comms next contact.
- **Context-floor plan item 1 (mine)** — still waiting on CIO's own `BRIEFING-CURRENT-STATE.md`
  Aug 5-12 self-mark (not mine to force). Deliberate honest stopping point since 09-22 — resume only
  on a fresh finding or a PM/Exec re-scope.
- **Git-attribution incident (Pard's) — fully resolved, purely historical now.** 231 commits (30 of
  mine, corrected from an initial undercount) misattributed to "Pard (Mediajunkie)" for ~17h on
  09-25/26 via a shared `.git` config accident; reverted, history deliberately not rewritten. No
  further action. Mentioned here only so a future me doesn't rediscover it as new.

## Watch surfaces (owned by others, checked periodically — don't re-derive, don't chase)

- **`last_verified` bulk-stamp cluster** — CIO's lane (#1726). 14/38 clustered on identical
  2026-06-19 stamp as of the 09-21 audit. Check again at next Weekly Docs Audit (09-28).
- **#1644** — roadmap.md full historical fold, PPM's lane. Not mine to force.
- **#1683** — 2 inverse-case calendar rows need real Medium verification, not guessing.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call.
- **#1710/#1847** — pattern-catalog Status-field frontmatter regression, routed to CIO/Arch
  (touches CIO's formal promotion authority). Watch for disposition.
- **#1720/#1721** — filed by me, triaged by PPM into FLYWHEEL. Watch for progress.
- **CXO's marker-provenance-field finding** (heartbeat marker, no observed/derived flag) — CIO's
  lane. Watch for the fix landing.
- **CIO's deferred heartbeat corroborating-check** (stale-marker-but-real-commits case) — explicitly
  deferred to Monday 09-28 per the throttle. Watch for it landing, don't implement it myself.
- **GitHub issue backlog health**: report as a ratio at each audit, not mine to triage
  individually.

## Owed by me — unblocked, low priority

- **PreCompact hook locality differentiation** (owed since May) — real design work, scoping
  before implementing, not a same-fire patch.
- **"Two of Me" art-audit gap** — publish audit checks image existence/dimensions but not
  image-content-matches-alt-text. No process fix yet, not urgent.
- Owed by Web: `piper-morgan-website#37` publish Step 9 automation — update `docs-notify.js:88`
  once it lands. Not urgent.
- `knowledge/piper-morgan-glossary-v1.1.md` needs CXO's tracked-state frontmatter at first
  substantive touch (60-day staleness contract). Not urgent.
- **Agent 360 v0.5** (`dev/2026/09/25/agent-360-questionnaire-v0_5.md`) — HOST fielded 09-25,
  ~2-week window (not clock-paced, respond when there's real reflection to give). Deliberately
  deferred to a dedicated future fire rather than squeezed into an already-substantial one — named
  trigger: a fire with room to actually think it through, not "no rush."
- **Note to Comms**: the calendar's Comms-owned `caption` column for "A Fix Needs the Same Rigor..."
  is stale (period vs. the draft's current question mark). Not urgent, mention next contact.

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits blocking `git pull --ff-only` in PM's own checkout. **Do not act on this
without PM present.**

## Day-of-week duty triggers — check every START

- **Every Monday**: Weekly Docs Audit — #1844 closed 09-21; next due 09-28. **Also the cron-cadence
  revert day** — restore 7x/day at START, per the throttle directive's own stated window.
- **First Monday of month**: Monthly Housekeeping — #1724 closed 09-07; next due 10-05.
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).
- **Every START**: omnibus production + missing/unclosed-log nudge is a FIXED Docs-only step
  (PM ruling 09-25, `duty-cycle-tick` v1.40 Step 1d). Two things: (1) produce/verify the prior day's
  omnibus; (2) nudge any role whose yesterday's log lacks a closing marker — check the actual text,
  not just an exact-string grep.

## Standing operating knowledge (current rules, not incident history)

- **At every proofread, re-run `template-audit`'s full 16-check list myself, including check #11
  (personhood grep) — don't just read Comms' publish-ready memo and trust "clean."** Division of
  labor with Comms (09-26): they own draft-time check #11, I own an independent proofread-time
  re-check. Two independent looks catch different things — proven same-day on two pieces. Don't skip
  this because Comms already said clean.
- ⚠️ **Emit the heartbeat every fire** — `scripts/duty-cycle-heartbeat.sh docs {START|WATCH|WORK|
  STOP} --if-quiet` as the LAST step before closing a fire, chained onto the SAME closing block as
  the final push of each work unit (not a separately-remembered step — that's what let a 3+ day gap
  happen, found by Pard 09-26, fixed same-fire). Held clean for the rest of 09-26 after the fix —
  keep watching this over the next several days before trusting it's fully solved.
- **GitHub-criteria line** (third work-queue source, PM's v1.33 ruling): `gh issue list --search
  "label:documentation" --state open --limit 50` — open each result, don't trust the list view.
- **PM crossposts to Medium/LinkedIn manually**, not via Dispatch-PM automation (decided
  2026-09-19, in `decisions.log`). When PM provides a syndication URL, that's a manual record to
  make (mediumURL/linkedinURL/status→distributed), not a delegated pipeline step.
- **Only cc PM on memos that** (a) contain a decision only PM can make, (b) relay a PM ruling, or
  (c) contain something PM would want to contradict — everything else reaches PM via the
  attention rollup.
- A subagent's self-reported verification pass is a claim, not a fact — re-verify the artifact
  yourself every time, even when the delegate reports having already checked it.
- A live-page 200 status can be a stale cached not-found fallback — always do an actual content
  check (title/image/body-text fragment) after the 200; `curl -s` doesn't follow redirects by
  default, add `-L`.
- A naive `cut -d','` on a CSV with quoted fields silently misaligns columns — use the `csv`
  module for any real read, not just writes. Match the file's existing `lineterminator`/quoting
  convention before writing, or a single-field edit rewrites every row as a diff. **This actually
  happened 09-27**: `csv.writer(f, lineterminator='\n')` on `piper-morgan-website`'s
  `data/blog-metadata.csv` (which uses CRLF) rewrote all 395 rows as a 786-line diff for a one-field
  alt-text fix — caught via `git diff --stat` before it mattered further, fixed with a byte-level
  surgical replace against the true original rather than the csv module. Check line endings
  (`xxd`/`file`) on any *unfamiliar* CSV before writing, not just the product repo's own calendar
  (which does use LF and is fine with the pattern above).
- `mail-send.sh` needs BOTH the old (deleted) and new (moved-to) path passed for a triage move,
  or the inbox-side deletion strands unpushed. Also does not advance local HEAD — `git merge
  origin/main` before assuming a triaged file "didn't move."
- `gh issue list` defaults to a 30-item limit if `--limit` is omitted — always pass an explicit
  high limit for any total-count claim.
- Before starting any audit/analysis task on a tracked GitHub issue: `gh issue view --json
  comments` first, not just the issue body.
- A cron cadence change (not just a same-expression re-arm) needs BOTH the explicit session-log
  id-transition note AND the `duty-cycle-registry.tsv` row updated in the same commit.
- A duty-cycle sync from earlier in the session is a timestamped fact, not a durable one —
  re-sync if meaningful time has passed, including mid-conversation with PM directly engaged.
- "Last scheduled fire of today" is arithmetic on the cron expression, not a feel-based judgment.
- A fire is a WAKE, not a time-box — drain unblocked work. Legitimate holds: a real external
  blocker, or a genuine capacity limit (compaction) — never "there's a lot of it."
- **Writing directly to `mediajunkie/designinproduct/docs/mail/` is the preferred route for
  anything addressed to Janus** — Janus's explicit ruling 2026-09-24, no precedent needed. For
  Pard, the real inbox is `~/Development/mediajunkie/docs/mail/` (NOT `mailboxes/pard/`, which is
  gravestoned and mechanically hard-refused by `mail-send.sh`) — sync that repo first, stage only
  your own file by explicit path.
- **Never csv-round-trip `dev/active/duty-cycle-registry.tsv`** — it's free-text prose from many
  agents mixed with real tab data, never well-formed CSV/TSV. Use targeted plain-text line
  replacement instead (match on the `role\t` prefix). Real incident: `ebea8a4d53`, 2026-09-23
  postmortem.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.
