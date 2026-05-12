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

## Load-Bearing vs. Commodity Work in This Role

Per Apr 22–26 leadership migration §6 reflections (Proto-Pattern PP-002). Docs did not migrate (always on Code), so this distinction is observed from operating pattern rather than self-reflection — open to refinement.

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

**Mailbox System (v3)** (`mailboxes/`):
- Use `/deliver-mail` skill for assisted delivery workflow
- `mailboxes/incoming/` is the drop zone for memos downloaded from web agents
- `mailboxes/DIRECTORY.md` is the canonical slug-to-role mapping
- `mailboxes/DELIVERY-LOG.md` tracks each delivery run with timestamps
- Each role has `inbox/`, `read/`, `sent/`, and `inbox/MANIFEST.md`
- Memo naming: `memo-YYYY-MM-DD-from-{slug}-to-{slug}[-cc-{slug}...].md`
- See `docs/internal/development/memo-format-guide.md` for full spec
- Mailboxes are gitignored — delivery is local-only, not committed

**Blog Metadata Pipeline** (cross-repo, `piper-morgan-website`):
- Source of truth: `data/blog-metadata.csv` (slug, hashId, imageSlug, category, pubDate)
- Build: `node scripts/fetch-blog-posts.js` → generates `src/data/medium-posts.json` + `src/data/blog-content.json`
- RSS provides content; CSV provides metadata (imageSlug, category)
- After CSV edits, run fetch script, verify JSON output, commit and push to website repo

**dev/active/ Triage**:
- Archive stale files to `dev/YYYY/MM/DD/` date folders
- Move drafts to `docs/public/comms/drafts/`
- Deliver undelivered memos to recipient mailboxes
- Delete confirmed duplicates (files with `(1)` suffix)
- Keep genuinely active files; ask PM about unclear items

## Merge-Keeper Sweep (Standing Discipline, established 2026-04-28)

Per CLAUDE.md "Sign-Off Discipline" — the agent's responsibility is sign-off correctness; two reactive safety nets back-stop discipline lapses:

1. **PreCompact hook** (`.claude/hooks/precompact-signoff-warning.sh`, Lead Dev ship 2026-05-08, severity-tiered 2026-05-11) — fires *before* context compaction with HARD/SOFT/QUIET tiers. Logs all firings to `dev/active/session-end-warnings.log` for the merge-keeper sweep.
2. **Docs merge-keeper sweep at session start** — this discipline. Catches anything the PreCompact hook didn't surface or the agent skipped.

The **session-end-warnings.log is gitignored** by design (ephemeral, per-machine); the merge-keeper sweep only sees PM's primary-machine log. Cross-machine archival is a v2 question, not v1.

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
# Create: dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-docs-code-opus-log.md

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
