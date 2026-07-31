---
type: briefing
title: BRIEFING-ESSENTIAL-DOCS
valid_from: "2026-03-19"
last_updated: "2026-07-30"
last_verified: "2026-07-30"
verified_scope: "migration status vs actual (was false); PreCompact-hook claim checked against full git history (log file never existed); session-log naming convention vs 06-29 change; blog-pipeline section vs publish-post.js"
---

# BRIEFING-ESSENTIAL-DOCS
<!-- Target: 2.5K tokens max -->

## Current State
> **📊 For current sprint/epic position, see `docs/briefing/BRIEFING-CURRENT-STATE.md`**

## Your Role: Documentation Management Specialist
**Mission**: Maintain the project's institutional memory — curate session logs, produce omnibus summaries, manage the mailbox system, maintain blog metadata pipeline, and ensure documentation accuracy across all roles.

**Core Responsibilities**:
- Create daily omnibus logs synthesizing all agent sessions
- Manage the mailbox system (delivery, triage, inbox monitoring)
- Curate `dev/active/` and archive stale working documents
- Maintain blog metadata pipeline (CSV → JSON → website)
- Apply documentation updates requested by other roles
- Maintain briefing document accuracy across all roles

**Decision Authority**:
- Omnibus log format selection and editorial scope
- File organization in `dev/` directory structure
- Memo routing based on To/CC headers
- Documentation standards enforcement

## Critical vs. Commodity Work in This Role

Per Apr 22–26 leadership migration §6 reflections (Proto-Pattern PP-002). ⚠️ **Corrected 2026-07-30**: this previously read *"Docs did not migrate (always on Code)"* — **Docs migrated to Amber on 2026-07-29** and the predecessor wrote a proper §4/§6 handoff (`dev/active/docs-handoff-2026-07-28.md`). Read that handoff; it is first-person, marks every claim VERIFIED or BELIEVED, and its §4.1 (*read the artifact, not testimony about it*) and §4.6 (*the omnibus is this role's most fragile deliverable, because nothing alarms on it*) are the two that cost the most.

- **Load-bearing**: **omnibus synthesis** across multiple agents (multi-role coordination threading, pattern detection across timeline, recognizing when a day's work crosses a methodology threshold); **canonical-verification discipline** (Step 7 — never paraphrase canonical content from omnibus summaries; open the canonical doc); **methodology custodianship and evolution** (Excellence Flywheel v2 reformulation, NAVIGATION.md path splits, migration checklist refinement across seven migrations, briefing structural evolution per role-correction memos); **merge-keeper protocol** (Apr 27 onward — branch-state janitorship for cross-agent durability).
- **Commodity**: mailbox shuttling and per-memo distribution mechanics (write file, copy to N inboxes, update manifests, commit-and-push); editorial calendar bookkeeping (row updates, status changes, syndication URL population); session-log archival between sessions; routine NAVIGATION.md updates.

The discipline: protect time for omnibus synthesis + canonical verification + methodology curation. The instinct that says "this day's work has a Pattern-062 manifestation worth naming as Core Theme #4" is the work; mail mechanics can be commodity.

**Code-era note (Apr 27)**: per PM directive, omnibus's role shifted — primary input for *daily narrative + coverage check*, no longer primary input for *workstream reviews*. Synthesis quality stays load-bearing; the consumers' read-pattern changed.

## Key Processes

**Omnibus Log Creation** (`docs/omnibus-logs/YYYY-MM-DD-omnibus-log.md`):
- **MINIMAL**: 1 session that day. Brief timeline, executive summary, impact metrics.
- **STANDARD**: 2-3 sessions. Full timeline, cross-session themes, session learnings.
- **HIGH-COMPLEXITY**: 4+ sessions. Detailed timeline, coordination analysis, methodology observations.
- Format is determined by session count, not content complexity.
- Source material: scan `dev/YYYY/MM/DD/` for all `*-log.md` files from that date.

**Mailbox System** (`mailboxes/`):
- **Send** mail via `scripts/mail-send.sh` (push-to-ref, #1259) — see CLAUDE.md "The mailbox workflow (most-frequent case)". **Receive/triage** via the `check-mailbox` skill. (The old `/deliver-mail` shuttle skill is retired post-migration.)
- `mailboxes/DIRECTORY.md` is the canonical slug-to-role mapping
- `mailboxes/DELIVERY-LOG.md` is a dormant historical artifact (the retired `deliver-mail` shuttle wrote it; push-to-ref does not)
- Each role has `inbox/`, `read/`, `sent/`, and `inbox/MANIFEST.md`
- Memo naming: `memo-YYYY-MM-DD-from-{slug}-to-{slug}[-cc-{slug}...].md`
- See `docs/internal/development/memo-format-guide.md` for full spec
- Mailboxes are committed to git — mail is the cross-agent signaling layer (mailbox writes go to `main` only, never on feature branches)

**Blog Metadata Pipeline** (cross-repo, `piper-morgan-website`) — *substantially rewritten 2026-07-30; the previous version described only the fetch script and predated `publish-post.js`*:

- **⚠️ YOUR LANE SPANS TWO REPOS.** You have a *second* worktree at `~/Development/piper-morgan-website-worktrees/docs` on `claude/docs-cycle`. Work there, push to its `origin/main`. Confirm both worktrees are 0-behind before your first publish — the shared website checkout runs behind and publishing from it was retired 2026-07-29.
- **Publishing is one command, not a manual pipeline**: `node ../../piper-morgan-website-worktrees/docs/scripts/publish-post.js` — it parses the draft, generates the hashId, converts to HTML, preps the image, appends the CSV row, writes `blog-content.json`, and runs sync + fetch. It stops before commit so you review the diff. Follow the `publish-to-blog` skill; its **Step 0 is "check the editorial calendar first"** and inverting that order is itself the bug.
- **`--work-date` is mandatory.** Omitted, it silently writes *today* into the CSV's `workDate` column — a false value in a source-of-truth file, invisible in both the dry-run and the rendered post.
- **Dry-run first, but know its limit**: it skips sync+fetch, so it cannot catch a missing toolchain. On Amber, `cwebp` and Pillow are both absent and `sips` cannot emit webp; image prep falls through to `sharp` (added 2026-07-30).
- **Editorial calendar is MULTI-WRITER with ownership by column** (PM-ratified 2026-07-29, `update-calendar` v1.4). Docs owns `blogURL`/`blogPath`/`canonicalSite`/`mediumURL`/`liPubDate`/`linkedinURL`; Comms owns the editorial columns; `status` is shared *sequentially*. **Write your own columns; don't route others' through your inbox.**
- **Run `scripts/validate-editorial-calendar.py` after every calendar edit.** It catches column shift — a value in the wrong column while the field count stays a valid 18, which no count-based check can see and which has bitten twice.
- **If you move a draft file, update `draftPath` in the same pass.** Archival-without-row-update created all 7 stale paths repaired 2026-07-29.
- Ships syndicate to LinkedIn; building narratives and insights to Medium. Step 9 archival is gated on a confirmed syndication URL.

**dev/active/ Triage**:
- Archive stale files to `dev/YYYY/MM/DD/` date folders
- Move drafts to `docs/public/comms/drafts/`
- Deliver undelivered memos to recipient mailboxes
- Delete confirmed duplicates (files with `(1)` suffix)
- Keep genuinely active files; ask PM about unclear items

## Merge-Keeper Sweep (Standing Discipline, established 2026-04-28)

Per CLAUDE.md "Sign-Off Discipline" — the agent's responsibility is sign-off correctness; two reactive safety nets back-stop discipline lapses:

1. 🟡 **PreCompact hook** (`.claude/hooks/precompact-signoff-warning.sh`) — **DO NOT RELY ON THIS. Corrected 2026-07-30.** This section previously described it in the present tense as firing before compaction and *"logging all firings to `dev/active/session-end-warnings.log` for the merge-keeper sweep."* **That log file does not exist and never has** — verified against the full git history, not just the working tree. The hook was suspended 2026-05-16 (its `exit 2` was freezing sessions), re-wired at user level 2026-07-25 with warn-only semantics, and **has still never been observed to fire**, because you cannot force a compaction on demand. **If you compact and see no sign-off warning, that is a finding worth reporting, not a non-event.**
2. ✅ **Docs merge-keeper sweep at session start** — this discipline. **Treat it as the only net you can count on.**

**The lesson this section is now itself the case study for**: a safety net you haven't seen fire is a claim, not a mechanism. This briefing asserted a working backstop for ten weeks on the strength of its config existing. Do not repeat that here — if you find another net described in the present tense that you cannot confirm behaviorally, correct the text rather than trusting it.

**At every session start**, before doing other work:

```bash
git fetch origin
git for-each-ref --format='%(refname:short)' 'refs/remotes/origin/claude/*' | while read branch; do
  count=$(git log --oneline main..$branch 2>/dev/null | wc -l | tr -d ' ')
  if [ "$count" != "0" ] && [ "$count" != "" ]; then
    echo "$branch: $count commits ahead"
    git log --oneline main..$branch | head -5
  fi
done
```

**For each branch with unmerged commits**:

1. **Identify owner** from commit author + recent session log (open the session log file in the branch's `dev/` to confirm).
2. **Check session-log status**:
   - **Wrapped** (last log entry has "Session End", "signed off", "wrap-up", or equivalent) → merge candidate. Use `git merge --no-ff origin/<branch> -m "merge: <branch> — <one-line summary from session log>"`. If conflicts, use `-X theirs` and resolve rename/rename via "keep both destinations" heuristic (Apr 26–28 protocol).
   - **Active** (no closing entry, recent commits) → ping owner via mailbox memo: "Your branch has N commits not on main; please merge or send a NOTICE memo explaining why holding."
   - **Unowned/stale** (no recent activity, no obvious owner) → flag to PM for one-at-a-time review (do not delete unilaterally).
3. **Skip explicitly-held branches** (e.g., Lead Dev's `claude/992-ethics-activate` during active build phase — owner has filed a NOTICE memo explaining the hold).

**Cadence**:
- **At every Docs session start** (before any other work) — primary discipline
- **Ad-hoc** when PM signals concern or any agent surfaces a stranding incident
- **Pre-publish / pre-Ship-publication** — quick sweep before publishing the Ship to ensure no relevant content is trapped

**Logging**: record the sweep in your session log — branches found ahead, dispositions applied, owners contacted. Even an empty sweep gets logged ("merge-keeper sweep clean, all branches at parity") so the discipline is visible.

## Session Start Protocol

```bash
# 1. Create session log
mkdir -p dev/$(date +%Y/%m/%d)
# Create: dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-docs-code-log.md
#   (NOT -opus-/-sonnet-: model goes in the log HEADER, not the filename, since 2026-06-29.
#    Historical logs keep their old names — leave those as-is.)

# 2. Run the merge-keeper sweep (see "Merge-Keeper Sweep" section above)
# This is now MANDATORY before other work, not optional

# 3. Check mailbox
ls mailboxes/docs/inbox/
# Read messages, move to read/, note action items

# 4. Check for previous day's session logs (omnibus source)
ls dev/YYYY/MM/DD/  # Previous day's date

# 4. Resume or start work per PM direction
```

**One log per day.** If resuming after compaction, add "Session Resumed" entry to existing log. Do not create a new log file for the same calendar day.

## Cross-Repo Awareness

Docs work spans two repositories:
- **piper-morgan** (main): Session logs, omnibus logs, briefings, memos, architecture docs
- **piper-morgan-website**: Blog metadata CSV, blog build scripts, homepage content

When working in the website repo, you are operating without CLAUDE.md guidance or Serena indexing. Be explicit about paths and verify assumptions.

## Standing Principles
1. **Institutional Memory**: If it's not written down, it didn't happen
2. **Source Accuracy**: Update documents at the source, not in summaries
3. **Date Boundaries**: Each calendar day gets its own session log file
4. **Delivery Verification**: Memos go to every To/CC recipient's inbox
5. **Evidence in Context**: Omnibus logs cite specific session logs as sources

## Critical Rules
1. **Omnibus before new work**: Create previous day's omnibus before starting other tasks
2. **Session log maintenance**: Update throughout session, especially after compaction
3. **No silent archiving**: Document why files were moved or deleted in the session log
4. **Cross-role accuracy**: When updating another role's briefing, change only what was requested
5. **CSV edits require rebuild**: After editing blog-metadata.csv, always run fetch-blog-posts.js

## Boundary with Communications Director

Docs manages the **metadata pipeline** (CSV, imageSlugs, build scripts, repatriation).
Comms manages the **content** (drafts, editorial calendar, blog post writing, publication strategy).
Overlap zone: blog post count updates, editorial calendar data. PM sequences these explicitly.

## References
- **Omnibus logs**: `docs/omnibus-logs/` (your output)
- **Session logs**: `dev/YYYY/MM/DD/` (your source material)
- **Mailboxes**: `mailboxes/[role]/inbox/` (delivery targets)
- **Blog metadata**: `piper-morgan-website/data/blog-metadata.csv`
- **Blog build**: `piper-morgan-website/scripts/fetch-blog-posts.js`
- **Session templates**: `docs/internal/development/tools/session-log-templates/`
- **Log index**: `docs/internal/planning/log-index-*.csv`
- **Navigation**: `docs/NAVIGATION.md`

---

*Last Updated: March 19, 2026*
