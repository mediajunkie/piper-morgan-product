# Docs Carry-Forward

**Updated**: 2026-09-22 ~14:20 PDT, verified via `date`.

**Spring-cleaned this fire** per the context-floor-reduction plan (item 4a,
`docs/internal/operations/context-floor-reduction-plan-2026-09-21.md`) — resolved narrative
deleted rather than archived-in-place. The durable record for everything cut here lives in the
dated session logs (`dev/2026/MM/DD/*-docs-code-log.md`) and `docs/omnibus-logs/`, per PM's
2026-06-12 "one place" ruling. If you need the pre-cleanup version, `git log -p -- dev/active/
docs-carry-forward.md`.

## Current state

- **09-21 closed cleanly**, all 7 work items landed (see that day's session log + omnibus for
  full detail): Weekly Docs Audit #1844 closed, #1847/#1846/#1848 filed, 2026-05-12 omnibus
  backfilled, Janus/DinP records-gap escalation fully resolved.
- **09-22 in progress**: published "The Near-Miss and the Missing Key" (hashId `b4f93c0eca6f`,
  distributed — Medium crosspost recorded), backfilled the 09-21 omnibus, shifted duty-cycle cron
  to `57 4,7,10,13,16,19,22 * * *` per PM's direct request (start no later than 5am; added a
  22:57 fire per PM's suggestion rather than trading off evening coverage — registry row updated
  to match). Currently working the context-floor-reduction plan's item 1 (CLAUDE.md + briefing
  audit for accreted incident narrative) — top priority per PM/Exec, 2026-09-22.

## Active threads

- **Context-floor plan item 1 (mine)**: audit CLAUDE.md + `docs/briefing/*` for narrate-vs-state
  passages, move history to a dated log, re-measure length only after.
  - **CLAUDE.md**: pass 1 done (73093→~63000 bytes, `df5050664`).
  - **`BRIEFING-CURRENT-STATE.md`**: pass 1 (179058→164260, `675b4bf67`), pass 2 — Lead's + PPM's
    self-marked entries removed (`6d23dfa0e`), pass 3 — my own two entries self-reviewed and
    removed (`6c324d0376`; Sep 2-14's MVP count was still load-bearing, replaced with a fresh live
    `sprint-truth.py` pull — **54 not done, 1141 done, 0 unmilestoned, #1850 off-board** — rather
    than just deleted). Now 156,652 bytes. **Still waiting on**: CIO's own Aug 5-12 entry, not yet
    self-marked.
  - **`BRIEFING-ESSENTIAL-DOCS.md`** (mine, full judgment authority): pass 1 done, 13030→11776
    bytes, `fbe973cae8` — also removed one genuinely dead branch reference outright (verified gone
    via `git branch -r`).
  - **`ROSTER.md`**: pass 1 done, 7789→7119 bytes, `1cc794ca7c` — found and fixed **2 real
    stale-fact bugs**, not narrative (the session-log filename convention wrongly claimed a
    `{model}` component defaulting to `opus`; the general-purpose slug was documented as
    `code-opus` when CLAUDE.md says `code`). Both verified against live evidence before fixing.
  - **Next**: the remaining `BRIEFING-ESSENTIAL-*` files (10 more, 5-23KB each) — same judgment
    authority, no cross-role dependency.
- **Duty-cycle flywheel relay — CLOSED.** PM's mail/task-loop formalization relayed to CIO
  yesterday; CIO confirmed the gap was real (single-pass exit vs. PM's required two-consecutive-
  empty-rounds), shipped `duty-cycle-tick` v1.38 fixing it, and forwarded to Janus per PM's own
  ask. Nothing further owed on this thread.
## ⚠️ TOP-OF-QUEUE 09-23 (Wednesday): publish Weekly Ship #061 "Closed Means Observed" — proofread done, do NOT publish before Wednesday

PM (09-22): "Tomorrow's Weekly Ship is ready for proofreading after which we can schedule it for
publishing tomorrow am." Calendar confirms: `status: ready-for-docs`, `pubDate: 2026-09-23`.

**Proofread complete and independently verified this session (09-22)**:
- Re-synced both worktrees + re-checked the calendar row fresh before reading anything.
- Diffed the `dev/active/` copy against `docs/public/comms/drafts/` — identical, no divergence.
- Mechanical checks: 1,405 words (Ship norm), 0 semicolons, no banned terms
  (load-bearing/cohort), negation-tics reviewed — all "somebody/nobody/anyone" instances are
  legitimate thematic/epistemic statements, not hiding an attributable actor (the one genuinely
  attributable event — the epic-2 reopen — IS correctly attributed as "a direct call" later in
  the piece, not hidden behind a vague pronoun). Title case and dateline format correct.
- Fact-checked independently, not just trusting Comms' memo: all 6 cited publications verified
  exact against the editorial calendar (dates + titles + status all match, full-window scan
  confirms no 7th omitted); commits figure (1,804) verified exact via `git log --oneline
  --since="2026-09-11 00:00" --until="2026-09-18 00:00"`; beta-blocker figure (246/302) traced to
  Comms' own Sep 19 drafting-day log; the security-chain narrative (global unprefixed key
  discovery) verified against Arch's actual Sep 14 log, matches precisely.
- Did NOT re-run the issues-closed=45/created=56/net+11 GitHub query — Comms explicitly declined
  this in their own memo to conserve the shared API rate limit, a reasoned tradeoff, not a gap;
  respecting that call rather than force-verifying.
- No defects found. Ship posts need no per-post image (always `piper-ship.webp`); the frontmatter
  `image:`/inline embed at line 58 is last week's cartoon shown as a visual callback in the
  External Relations section, not this post's own header image — expected pattern, not a bug.

**Publish parameters, pre-derived**:
- Draft: `docs/public/comms/drafts/weekly-ship-061-draft-2026-09-19.md`
- `--slug weekly-ship-061-closed-means-observed` (derive from title; confirm no existing slug
  collision before using — check `data/blog-metadata.csv` fresh on the day)
- `--category ship`
- `--work-date 2026-09-11` (matches calendar `workDate`, the window start date)
- `--cluster the-alpha` (derived from nearby Sep 2026 rows in `blog-metadata.csv`, including the
  immediately-prior Weekly Ship #060)
- No `--image` flag (Ships use `piper-ship.webp` automatically)

**Wednesday's sequence**: same full procedure as every prior publish (re-sync both worktrees
first — this plan will be ~24h old by the time it's used; re-verify the calendar row and slug
availability haven't changed; re-run pre-flight checks fresh including the dev/active-vs-drafts
diff; dry-run; real publish; website commit; calendar update (`canonicalSite` stays EMPTY —
blog-first, not cross-post; Ships syndicate to LinkedIn only per category convention, not
Medium); live content-verify by content, not status code — remember the trailing-slash 308
redirect from yesterday's publish, use `curl -L` or check raw HTML directly, not WebFetch alone;
archive draft (no separate image file to archive for Ships), update `draftPath` in the same
commit; then message PM it's live).

**After publishing, delete this section from carry-forward** — one-shot plan, not standing.

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
