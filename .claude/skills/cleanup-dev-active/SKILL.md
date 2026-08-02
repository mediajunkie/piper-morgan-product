---
name: cleanup-dev-active
description: Triage and archive stale files from dev/active/. Use during session
  wrap-up, weekly audits, or when dev/active/ exceeds ~15 files. Prevents working
  directory from becoming a graveyard of superseded drafts.
scope: cross-role
version: 1.1
created: 2026-03-30
updated: 2026-05-15
---

# cleanup-dev-active

Triage files in `dev/active/` — archive completed/superseded work, keep only what's genuinely in progress.

## When to Use

- During session wrap-up when you notice dev/active/ is cluttered
- During weekly docs audit (#937-series)
- When dev/active/ exceeds ~15 files
- PM asks to "clean up dev/active" or "sort the working directory"

## Principle

`dev/active/` is a workbench, not a filing cabinet. Files land here during active work and should move out when the work is done. The accumulation pattern is: agent creates file → work completes → file stays because nobody moves it.

## Procedure

### Step 1: Inventory

```bash
# List files with last-modified dates
for f in dev/active/*; do
  if [ -f "$f" ]; then
    modified=$(git log -1 --format='%ai' -- "$f" 2>/dev/null | cut -d' ' -f1)
    echo "$modified | $(basename "$f")"
  elif [ -d "$f" ]; then
    echo "DIR      | $(basename "$f")/"
  fi
done | sort
```

### Step 2.0: Omnibus-coverage guard (MANDATORY — check BEFORE the decision tree)

**A cycle log is durable-capture-pending, not forensic, until its day's omnibus exists.**

Per-fire **cycle logs** (`dev/active/cycle-log-{role}-YYYY-MM-DD.md`) are the *only* granular record of any work that was displaced from a role's session log (see methodology-41 / the CLAUDE.md "displacement trap" rule — June 3–8 2026 displaced ~15 role-days across 6 roles). The omnibus is what makes that content durable: `create-omnibus` reads the cycle logs at synthesis and captures their substance into `docs/omnibus-logs/YYYY-MM-DD-omnibus-log.md`. **Archiving or deleting a cycle log before that omnibus exists can permanently lose displaced work.**

**The guard** — for every `cycle-log-{role}-YYYY-MM-DD.md` you're about to archive/delete:

```bash
DATE=$(echo "$f" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
if [ -f "docs/omnibus-logs/$DATE-omnibus-log.md" ]; then
  echo "OK to archive: $DATE omnibus exists (content captured)"
else
  echo "⛔ HOLD: no omnibus for $DATE yet — cycle log is the live record; do NOT clean"
fi
```

- **Omnibus exists** → the cycle log is now genuinely forensic → Destination 4 (archive to `dev/YYYY/MM/DD/`), same as the omnibus's own Step 10.
- **No omnibus yet** → **HOLD the cycle log in `dev/active/`** (Destination 3) regardless of age. It is load-bearing until covered. Flag the missing omnibus to Docs/PM (a cycle log with no omnibus past its day is itself a signal the omnibus is overdue or the gate is stuck).

This guard is the durability-net layer of the four-layer displacement defense (skill v1.5 dual-surface = source-catch; detector hook = reactive-net; m-31/m-41/CLAUDE.md = framing; **this guard = protect-already-displaced-from-loss**). It protects the reassuring half of the displacement audit ("June 3–8 isn't lost — it's in the omnibi") from having a cleanup time-bomb under it.

### Step 2: Categorize Each File — Destination Decision Tree

**The single most-important call**: distinguish *forensic-only working docs* from *forward-looking artifacts that still need to live somewhere active*. A "completed" file isn't automatically forensic — many "completed" drafts have a forward life (next publish date, ratification target, canonical-doc-on-deck status). Filing forward-looking work to a dated archive makes it invisible right when the next-cycle agent needs it.

**Five possible destinations**, in priority order — check each in this sequence and stop at the first match:

| # | Destination | Signal questions | Action |
|---|---|---|---|
| 1 | **`docs/public/comms/drafts/`** — forward-looking publish drafts | Does the title appear in `docs/internal/planning/comms/editorial-calendar.csv` with **status=queued** + a **future pubDate**? Is the filename `weekly-ship-*-draft-*` or `*-draft-*` matching a queued title? Frontmatter (`image: / alt: / caption:`) populated? | **Move** to `docs/public/comms/drafts/` (with `git mv`) so it stays alongside other in-flight publish work |
| 2 | **`docs/internal/{appropriate-location}/`** — new canonical reference | Methodology doc / ADR proposal / pattern proposal / briefing / discipline note structured for canonical reference (formal sections, versioned, has Status field)? Will agents reference this *forward* (not as historical context but as authoritative source)? | **Move** to canonical doc-tree location (consult `docs/NAVIGATION.md` if unsure) |
| 3 | **Keep in `dev/active/`** — continuously-updated workspace | Continuously-updated tracker (`cio-innovation-backlog.md`, `cio-standing-items.md`, `comms-open-topics.md`, `exec-open-items-tracker.md`, agent workspace subdirectory)? PM-day-of research (<3 days old)? `publish-package/` mid-publish? | **Keep** in dev/active/ |
| 4 | **`dev/YYYY/MM/DD/`** — forensic-only archive | One-time working artifact tied to a closed task: investigation report, audit finding, sent-memo draft, Phase 0 audit doc, gameplan, retest result, intermediate Pattern-Sweep deliverable, etc.? Will future agents only need this for historical reference (not forward citation)? | **Archive** to dev/YYYY/MM/DD/ (use the file's last-modified date) |
| 5 | **Delete** — true duplicate | Multiple versions with `(1)`, `(2)` suffixes where canonical exists elsewhere? Empty stub file with canonical version at correct location? | `git rm` the duplicate; keep the canonical |

**Special cases that need PM confirmation**:
- File < 3 days old that PM may have dropped in (PM uses dev/active/ as a dropbox) → **ask before moving**
- Cross-project files (Klatch, etc. — recognizable by filename) PM may have downloaded → **ask before moving**
- Unknown purpose that doesn't fit any category → **ask PM**

### Destination tells — what to look for

**Forward-looking publish drafts (Destination 1)**: the failure-mode-to-avoid case. Symptoms a file is forward-looking publish material:
- Filename includes `-draft-` AND a date that hasn't passed (e.g., `weekly-ship-042-draft-2026-05-10.md` filed on 2026-05-12 — the *pubDate* is May 13, not 10; the in-filename date is the workDate)
- Title appears in editorial-calendar.csv with `status=queued`
- File has full frontmatter (`image: / alt: / caption:`) — drafts ready to publish carry this; forensic working docs don't
- Lives in `dev/active/` (not yet in `docs/public/comms/drafts/`) because it was drafted there
- **Calendar lookup**: `grep -i '{title}' docs/internal/planning/comms/editorial-calendar.csv` — if the row's pubDate is **future** and status is **queued**, this is Destination 1 not Destination 4

**Canonical reference docs (Destination 2)**: symptoms:
- Filename matches a canonical-doc convention (e.g., `methodology-*.md`, `pattern-*.md`, `adr-*.md`, `briefing-*.md`)
- Document has formal structure (Status / Author / Date / Version / etc.)
- Content reads as authoritative reference, not as a working memo or investigation
- Currently in `dev/active/` because it was drafted there, but the canonical home is `docs/internal/{path}/`

**Workspace trackers (Destination 3)**: stay in `dev/active/`:
- `cio-innovation-backlog.md`, `cio-standing-items.md` — CIO updates continuously
- `comms-open-topics.md` — Comms updates continuously
- `exec-open-items-tracker.md` — Exec updates continuously
- `agent-360-questionnaire-v0_2.md` — HOST iteration target
- `publish-package/` — active publishing artifacts
- `non-doc-files/` — PM workspace dir
- `session-end-warnings.log` — **gitignored, per-seat, and REAL. Preserve it.** ⚠️ *Corrected 2026-08-01: on 07-30 I annotated this as "has NEVER existed," from a `git log` query against a **gitignored** path — a check that returns empty regardless. The hook fires; HOST's seat holds a logged `tier=HARD` firing from 2026-07-29.* Absent in your worktree means no firing **on your seat**, not a dead mechanism.
- Recent PM-dropped research files (<3 days old)

**Forensic archives (Destination 4)**: typical archive shapes:
- `{issue-number}-issue-audit.md` / `{issue-number}-gameplan.md` / `{issue-number}-phase-1-design.md` — Phase 0/1 working artifacts after issue closes
- `floor-fabrication-investigation.md` / `host-role-health-check-*.md` — incident-specific investigations
- `workstream-{ship-number}-{role}-{date}.md` — sent workstream memos (after Ship publishes)
- `canonical-retest-*.{py,md,csv}` — retest run artifacts
- `pattern-{evolution|library-index|meta-synthesis|novelty|usage}-*.md` — Pattern Sweep intermediate deliverables
- `cio-pattern-promotion-analysis-*.md` — completed promotion analysis reports
- `merge-keeper-*.md` — completed merge-keeper sweep reports
- `memo-*-{date}.md` in dev/active/ — drafted memos that already got distributed via `mailboxes/{role}/sent/`

### Step 3: Execute Moves

Use the destination from Step 2's decision tree:

```bash
# Destination 1: forward-looking publish drafts → docs/public/comms/drafts/
git mv dev/active/weekly-ship-NNN-draft-YYYY-MM-DD.md docs/public/comms/drafts/

# Destination 2: canonical reference → docs/internal/{appropriate-location}/
git mv dev/active/methodology-NN-name.md docs/internal/development/methodology-core/

# Destination 4: forensic-only → dev/YYYY/MM/DD/
mkdir -p dev/YYYY/MM/DD
git mv dev/active/NNNN-issue-audit.md dev/YYYY/MM/DD/

# Destination 5: true duplicate → delete
git rm "dev/active/file (1).md"
```

**Before staging the moves, run the discipline opening** per `feedback_clear_index_before_staging_on_shared_main.md`:

```bash
git reset HEAD  # clear any pre-existing index residue
# ... then execute the per-file git mv / git rm commands above ...
git diff --cached --name-only  # READ EVERY LINE — verify only intended moves are staged
```

### Step 4: Verify

```bash
# Count remaining files
ls dev/active/ | wc -l  # Target: <15

# Confirm no broken references
grep -r "dev/active/archived-file" docs/ .claude/  # Should be empty
```

### Step 5: Report

Add to session log:
```
### dev/active/ cleanup
- Before: N files
- Archived: X files to dev/YYYY/MM/DD/
- Deleted: Y duplicates
- Kept: Z active files
- After: Z files
```

## What to Keep (Safe List)

These types of files belong in dev/active/:
- Files for work with an upcoming deadline (conference talks, scheduled publishes)
- `publish-package/` — active publishing workflow artifacts
- Agent workspace directories (e.g., `pa/`) for active agents
- Specs or plans PM is actively reviewing

## What to Archive (Common Accumulations)

**Note**: PM's browser downloads to this folder, so files from other projects (Klatch, etc.) or duplicate downloads with `(1)`, `(2)` suffixes will periodically appear. These are not Piper Morgan work products — archive or delete after confirming with PM.

These commonly pile up and should be moved:
- Superseded briefing drafts (v0.1 when v0.2 is in docs/briefing/)
- Onboarding prompts after agent launch is complete
- Proposals after issues are filed
- Session logs that belong in dev/YYYY/MM/DD/ (rare — create-session-log usually puts them in the right place)
- Completed tracker spreadsheets

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Delete files without checking | May be PM's in-progress work | Archive to dated directory |
| Move files PM dropped here recently | PM uses dev/active/ as a dropbox | Ask before moving files < 3 days old |
| Clean up during active sprint work | Context switching wastes time | Do it at session boundaries |
| Move agent workspace directories | Other agents depend on the path | Only move if agent is decommissioned |

## Frequency

- **Light triage**: Every session wrap-up (move obviously completed files)
- **Full cleanup**: Weekly audit or when file count > 15
- **PM-initiated**: When PM says "clean up" or "sort dev/active"

## Lesson Learned (May 12 → May 15 iteration)

**The Ship #042 draft incident** (May 12 cleanup, `62f5cd0a`): `weekly-ship-042-draft-2026-05-10.md` was filed from `dev/active/` to `dev/2026/05/10/` (Destination 4 / forensic archive) when the correct destination was `docs/public/comms/drafts/` (Destination 1 / forward-looking publish draft headed for May 13 publication). The filename's `2026-05-10` was the **workDate**, not the **pubDate** — the draft was queued for publication 3 days later. Filing it to the dated archive made it invisible right when the next-cycle agent needed to publish it.

**The fix**: the decision-tree in Step 2 now puts Destination 1 *first* in priority order, with explicit calendar-lookup signal. **When in doubt about a `*-draft-*` file**: grep the editorial calendar before archiving. If the title appears with `status=queued` and a future pubDate, the destination is `docs/public/comms/drafts/`, not the dated archive.

**General principle**: a "completed" file isn't automatically forensic. Many "completed" drafts have a forward life. The decision tree's priority order (publish-drafts → reference → workspace → forensic → delete) reflects that forensic is the **last** destination considered, not the default.
