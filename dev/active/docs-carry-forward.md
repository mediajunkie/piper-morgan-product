# Docs Carry-Forward

**Updated**: 2026-09-24 ~14:28 PDT, verified via `date`.

**09-23 closed cleanly.** Session log `dev/2026/09/23/2026-09-23-0527-docs-code-log.md` carries
`<!-- DAY-CLOSED: 2026-09-23 -->` + a full day-arc summary. All 7 scheduled fires ran. Everything
on `origin/main`, nothing stranded. Cron re-armed via delete-then-create at STOP (`72e6ae66` →
`83ccab8f`).

**PM directive still standing: do NOT self-throttle on usage — stay fully active, drain queues
normally.**

## Current state

09-23 closed cleanly (see prior day's session log for full detail). 09-24 START: published "The
Alarm That Had Been Working All Along" end-to-end (full pipeline, live-verified by content,
calendar updated, draft archived) — caught+fixed my own multi-path `git add` mistake mid-pipeline
(a bad pathspec silently dropped the calendar commit; caught via `git status`, not assumed clean).

## Active threads

- **"A Fix Needs the Same Rigor as the Claim It Fixes"** — PM's own direct edit pass, proofread
  and confirmed with PM on a genuinely broken sentence. `ready-for-docs`, holding for 09-26.
- **Context-floor plan item 1 (mine)** — still waiting on CIO's own `BRIEFING-CURRENT-STATE.md`
  Aug 5-12 self-mark (not mine to force). Otherwise a deliberate, honest stopping point as of
  09-22 — resume only on a fresh finding or a PM/Exec re-scope.

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
- **Writing directly to `mediajunkie/designinproduct/docs/mail/` is the preferred route for
  anything addressed to Janus** — Janus's explicit ruling 2026-09-24, no precedent needed (per
  `mediajunkie` repo's `docs/convention-cross-repo-mail-delivery.md`). Relayed through Exec on
  09-24's `hosr` answer out of unwarranted caution; Janus corrected that assumption directly. Next
  time, write there myself.
- ⚠️ **Emit the heartbeat every fire** — `scripts/duty-cycle-heartbeat.sh docs {START|WATCH|WORK|
  STOP} --if-quiet` as the LAST step before closing a fire. Skill v1.21, line 264 — real gap found
  2026-09-24 (HOST flagged): `docs.tsv` missing from `dev/heartbeats/` for 3 straight days because
  I simply never called this script, not any bug in it. Self-suppresses harmlessly on a busy fire
  (costs nothing), so there's no reason to skip it even on days full of real commits.
- **Never csv-round-trip `dev/active/duty-cycle-registry.tsv`** — it's free-text prose from many
  agents mixed with real tab data, never well-formed CSV/TSV. `csv.reader`/`csv.writer`'s
  `QUOTE_MINIMAL` will silently re-decide quoting on every row, not just the one being edited,
  including the `#`-comment header (no tabs → parsed as 1-column rows). Use targeted plain-text
  line replacement instead (match on the `role\t` prefix), same pattern as CIO's
  `trim-registry-history.py`. Real incident: `ebea8a4d53`, 2026-09-23 postmortem.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.
