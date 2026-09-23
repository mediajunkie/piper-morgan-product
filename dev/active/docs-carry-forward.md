# Docs Carry-Forward

**Updated**: 2026-09-23 ~08:42 PDT, verified via `date`.

**09-22 closed cleanly** (retroactively confirmed via its own DAY-CLOSED marker) **and its omnibus
is now done** (was the one gap found at 09-23 START — dispatched to a subagent, independently
verified, see below). 09-23 in progress, all pushed, nothing stranded.

**PM directive still standing: do NOT self-throttle on usage — stay fully active, drain queues
normally.**

## Current state

**Weekly Ship #061 fully wrapped** end-to-end today: published, a real "Ship Not Found" deploy-lag
finding investigated and resolved (not dismissed), a publications-list link-formatting defect
(PM-caught) fixed and live-verified, LinkedIn crosspost recorded. **09-22 omnibus created**
(554 lines, HIGH-COMPLEXITY/COORDINATION, dispatched+independently verified — commits `f6a1a0a9f7`
+ `b1cc465278`). **Monday Docs Audit (#1844) confirmed clean** to PM on direct ask — one new issue
(#1846) came out of it, unassigned but in my own lane, no PM scheduling needed.

## Active threads

- **"The Alarm That Had Been Working All Along"** — Comms' publish-ready memo, independently
  re-verified against both cited source logs (not trusted on the review pass alone). Holding for
  09-24 pubDate. Nothing further needed until tomorrow's fire.

- **Context-floor plan item 1 (mine)**: 9 documentation files improved today — CLAUDE.md,
  `BRIEFING-CURRENT-STATE.md` (3 passes, 179058→156652 bytes, current MVP count now a fresh
  standalone line — 54 not done, 1141 done, 0 unmilestoned — replacing a stale indirection), my
  own briefing, `ROSTER.md` (2 real stale-fact bugs found+fixed, not narrative), and — via the
  flag-don't-guess pattern that held up across every case today — PA, CXO, PPM, and HOST all
  refreshed their own flagged-stale sections same-day with real verification. **HOST's case caught
  something genuinely dangerous**: their own "Operating model" section claimed Model A was
  deprecated when it's been current since 07-25 — a wrong instruction another session could have
  acted on directly, not just staleness. All 4 fixes independently verified (well-formed,
  frontmatter intact) before trusting them.
  - **Still waiting on**: CIO's own `BRIEFING-CURRENT-STATE.md` Aug 5-12 entry, not yet self-marked.
  - **Remaining 8 `BRIEFING-ESSENTIAL-*` files** (Comms/Lead/Web/Agent/ETA/Arch/CIO/Exec) swept for
    the narrative-accretion pattern and found genuinely clean at meaningful scale — a deliberate,
    honest stopping point, not deferred busywork. Resume only if a fresh sweep finds something new,
    or if PM/Exec re-scopes the plan.
- **`main-old` branch + classic protection rule** — tracked per Pard's ask (2026-09-22), verified
  live via `git ls-remote`. No date, not mine to action unilaterally — see
  `dev/active/docs-standing-items.md` for the full entry + Pard's two framing questions.
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

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits blocking `git pull --ff-only` in PM's own checkout. **Do not act on this
without PM present.**

## Day-of-week duty triggers — check every START

- **Every Monday**: Weekly Docs Audit — #1844 closed 09-21; next due 09-28.
- **First Monday of month**: Monthly Housekeeping — #1724 closed 09-07; next due 10-05.
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).
- (Omnibus is a daily check, not on this list.)

## Standing operating knowledge (current rules, not incident history)

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
  convention before writing, or a single-field edit rewrites every row as a diff.
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

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.
