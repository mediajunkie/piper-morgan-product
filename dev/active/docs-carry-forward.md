# Docs Carry-Forward

**Updated**: 2026-09-30 23:28 PDT, verified via `date`.

**🔴 CASCADE SEAT 4 — ONE ACTION OWED AT THE 04:12 FIRE TOMORROW, READ THIS FIRST.**
Pard confirmed the 22:12 LaunchAgent fire (`com.xian.pm-docs-cycle`, 7x/day at `:12`, NOT my
session cron's `:57`) met the `consumed` standard on his side — the mechanism itself works. My own
finding (the injected prompt omitted the website worktree + the carry-forward-read instruction) was
real and generalized beyond this seat (comms/web have the same gap, future cascade seats) — **fixed
in the generator** (`798fe73`, not hand-edited, survives regeneration): second worktree now
auto-detected, carry-forward instruction moved to a per-seat extras file.

**At the 04:12 fire tomorrow (10-01), check: does the prompt now name BOTH worktree paths AND
include the carry-forward-read instruction?**
- **If yes**: `CronDelete cb42c0a8` (do NOT re-create), tell Exec the registry flips to
  LaunchAgent-only for this seat, update the registry row to reflect LaunchAgent-only.
- **If still thin**: do NOT retire anything — report back to Pard (`~/Development/mediajunkie/docs/
  mail/`) with the specifics of what's still missing, hold the session cron another cycle.

Until this resolves, both crons fire daily (~45min apart) — accepted cost, not a bug, don't "fix"
it by deleting either preemptively before the check runs.

**09-30 closed cleanly.** Weekly Ship #062 published + fully distributed this morning (PM caught a
real miss — sat ready since 09-27, fixed with new `duty-cycle-tick` Step 1g, which is now proven in
production). Step 1f/1g both live-exercised clean repeatedly through the day. Cascade-seat-4 news
landed and was handled end to end (prompt-gap found, reported, fixed, confirmed). Both worktrees
clean, everything on `origin/main`.

**PM directive still standing: do NOT self-throttle on approved/real work.**

**Crosspost-reminder mechanism (09-29, PM-ratified in conversation) is durable, not memory-only.**
`update-calendar` SKILL.md v1.5 carries the reminder at the blog-first-publish step;
`duty-cycle-tick` SKILL.md v1.42's Docs-only **Step 1f** re-checks every fire for any calendar row
published in the last 7 days still at `status=published`. Live-tested clean twice now (correctly
empty both 09-29 evening fires). Two memory pins point at these mechanisms rather than standing
alone: `feedback_remind_pm_to_crosspost_unsyndicated_publications` and the general
`feedback_prefer_visible_portable_repo_backed_mechanisms`.

**They/them pronoun ruling (PM, 09-29 evening) is durable**: `blog-style-guide.md` v1.1 + a new
template-audit check #12. No separate memory pin needed — the git-tracked guide already carries it.

**Website deploy note**: the site is Vercel-deployed (confirmed via response headers); the GitHub
Actions "Deploy Piper Morgan Website to GitHub Pages" workflow is stale/unused (last run 07-21) —
don't check `gh run list` there for deploy status; live-verify by actual body content after a short
poll instead.

## Active threads

- **Weekly Ship #062 — FULLY DISTRIBUTED 09-30** (blog live + LinkedIn crossposted, both PM-
  provided/confirmed). PM caught a real miss (sat ready+audited since 09-27, nobody checked
  "queued + pubDate arrived" this morning) — fixed the process gap, not just the one post, via new
  `duty-cycle-tick` **Step 1g** (v1.43), which mechanically re-checks this every fire going
  forward. Thread fully closed, no further action.
- **"What Piper Morgan Actually Is" (10-01, Thursday) — PUBLISH-READY memo received 09-29 23:27.**
  Verified against the calendar: `status=ready-for-docs`, draftPath matches the 09-29 rename/
  retitle fix, altText/caption populated, image file present. Clean handoff. Re-verify fresh at
  actual publish time (10-01) — don't trust today's spot-check as still-current by then, same
  standing discipline as every other piece.
- **Mention to PM at next engagement: "Drained on Paper" (08-07) has sat genuinely unsyndicated for
  ~7 weeks** — confirmed real via 08-30 platform verification (not a record gap), re-found twice now
  (Exec's rollup check 09-29, Exec's rollup check again 09-30 night — asked "is this the Ship-058
  shape" since PM said crossposts are generally caught up). **Answered Exec 09-30: can't tell from
  the record alone whether it's been posted-but-unrecorded since 08-30 or still genuinely pending —
  needs PM's direct confirmation specifically for this post, not inferred from a general "caught up"
  read.** Step 1f won't catch it going forward (deliberately 7-day-windowed) — one-time backlog
  item, PM's call on priority and the only one who can actually say whether it's done.
- **Personhood/attribution division of labor with Comms — PROVEN across 4+ pieces, keep using it**
  (Comms owns `template-audit` check #11 at draft time; Docs owns an independent re-check at
  proofread time on every future proofread).
- **#1904 filed (mine, 09-28)**: 3 procedural docs 300+ days stale, describing pre-Fly-migration
  state as "Production Ready." Not mine to fix (needs technical verification against current code)
  — watch for disposition, don't chase.

## Watch surfaces (owned by others, checked periodically — don't re-derive, don't chase)

- **`last_verified` bulk-stamp cluster** — CIO's lane (#1726). 13 of 38 clustered on the identical
  2026-06-19 stamp as of 09-28's audit. Check again at next Weekly Docs Audit (10-05).
- **#1644** — roadmap.md full historical fold, PPM's lane. 16 days stale as of 09-28's audit,
  reported not fixed. Not mine to force.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call.
- **#1710/#1847** — pattern-catalog Status-field frontmatter regression, routed to CIO/Arch.
- **#1720/#1721** — filed by me, triaged by PPM into FLYWHEEL. Watch for progress.
- **CXO's marker-provenance-field finding** — CIO's lane. Watch for the fix landing.
- **GitHub issue backlog health**: 217 of 288 open issues (75%) inactive 30+ days, as of 09-28's
  audit — report as a ratio at each audit, not mine to triage individually.
- **#1901** — closed same-day 09-29 by Lead/CXO. No further watch needed.
- **Deployment pipeline (§4e/§4f)**: fully built, reviewed, fixed, re-reviewed 09-29 (Arch/Pard/
  Lead/Exec). Nothing left but PM minting two Fly tokens + a GitHub environment reviewer, whenever
  convenient. Not mine to track further — Exec/Lead's lane.

## Owed by me — unblocked, low priority

- **PreCompact hook locality differentiation** (owed since May) — real design work, scoping before
  implementing, not a same-fire patch.
- **"Two of Me" art-audit gap** — publish audit checks image existence/dimensions but not
  image-content-matches-alt-text. No process fix yet, not urgent.
- Owed by Web: `piper-morgan-website#37` publish Step 9 automation. Not urgent.
- `knowledge/piper-morgan-glossary-v1.1.md` needs CXO's tracked-state frontmatter at first
  substantive touch. Not urgent.

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
- **Every fire**: Step 1f crosspost-reminder check (09-29) — any calendar row published in the
  last 7 days still `status=published` gets flagged. **Every fire**: Step 1g past-pubDate publish
  check (09-30, new) — any calendar row `queued`/`ready`/`ready-for-docs` with `pubDate` already
  arrived is unblocked work to drain same-fire, not a line to defer.

## Standing operating knowledge (current rules, not incident history)

- **At every proofread, re-run `template-audit`'s full 16-check list myself, including check #11**
  — don't just read Comms' publish-ready memo and trust "clean."
- **Check line endings (`xxd`/`file`) on any UNFAMILIAR CSV before writing with the `csv` module**
  — `piper-morgan-website`'s `data/blog-metadata.csv` uses CRLF; the product repo's own calendar
  CSV uses LF and is fine with the existing pattern.
- **A "silent, account-wide GitHub API rate limit" is real and distinct from an exhausted personal
  quota** — verify via `gh api rate_limit` before assuming either way.
- ⚠️ **Emit the heartbeat every fire** — chained onto the same closing block as the final push of
  each work unit.
- **GitHub-criteria line** (third work-queue source): `gh issue list --search "label:documentation"
  --state open --limit 50` — open each result, don't trust the list view.
- **PM crossposts to Medium/LinkedIn manually.** When PM provides a syndication URL, record it —
  not a delegated pipeline step. The reminder-to-PM half of this is now the Step 1f mechanism
  above, not a manual thing to remember.
- **Only cc PM on memos that** (a) contain a decision only PM can make, (b) relay a PM ruling, or
  (c) contain something PM would want to contradict. **PM does not read mailbox memos** — a cc
  there doesn't actually inform PM; surface real findings via carry-forward for direct mention, or
  in-conversation. Caught myself cc'ing PM on undelivered-in-practice memos twice on 09-29 —
  drop the cc rather than repeat it.
- A subagent's/colleague's self-reported verification pass is a claim, not a fact — re-verify the
  artifact yourself every time.
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
- **Writing directly to `mediajunkie/designinproduct/docs/mail/` is the preferred route for
  anything addressed to Janus.** For Pard, the real inbox is `~/Development/mediajunkie/docs/mail/`
  (NOT `mailboxes/pard/`, gravestoned and hard-refused by `mail-send.sh`) — sync that repo first,
  stage only your own file by explicit path.
- **Never csv-round-trip `dev/active/duty-cycle-registry.tsv`** — use targeted plain-text line
  replacement (match on the `role\t` prefix).
- **autoclose-guard gotcha recurs on Ship numbers** (`#058`, `#062`, etc.) — a close-keyword near
  a `#NNN` triggers the guard even when the number is a Ship number, not a GitHub issue. Write the
  number without `#` in commit messages when this comes up.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.
