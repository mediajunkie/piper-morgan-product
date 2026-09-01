---
type: briefing
title: BRIEFING-ESSENTIAL-DOCS
valid_from: "2026-03-19"
last_updated: "2026-07-30"
last_verified: "2026-09-01"
verified_scope: "2026-09-01 (Docs): spot-verified blog-metadata pipeline claims against today's own live publish (blog-metadata.csv confirmed still a live publish-post.js output, not a stale legacy reference); merge-keeper section, PreCompact-hook correction, cross-repo worktree warning, and Amber image-toolchain note all read consistent with this session's actual practice. Content unchanged — verification confirmed currency, no drift found. Prior scope (2026-07-30): migration status vs actual (was false); session-log naming convention vs 06-29 change; blog-pipeline section vs publish-post.js. ⚠️ CORRECTED 2026-08-01: this scope line previously claimed the PreCompact log file never existed. That check used git history against a GITIGNORED path and was structurally incapable of finding it — the hook DID fire (HOST seat, 2026-07-29 22:10 PDT)."
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

Per Apr 22–26 leadership migration §6 reflections (Proto-Pattern PP-002). *(Corrected 2026-07-30: this
claimed Docs had never migrated. It has — to Amber, 2026-07-29.)*

**📖 Read `dev/active/docs-handoff-2026-07-28.md` first.** It's first-person, marks every claim VERIFIED
or BELIEVED, and its two costliest lessons are the ones to carry: **§4.1** *read the artifact, not
testimony about it* — and follow a skill's step order literally, because inverting it **is** the bug;
**§4.6** *the omnibus is this role's most fragile deliverable, because nothing alarms on it.*

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

**Blog Metadata Pipeline** (cross-repo, `piper-morgan-website`):

⚠️ **YOUR LANE SPANS TWO REPOS — this is the part that appears in no other briefing and will blindside
you otherwise.** You have a *second* worktree at `~/Development/piper-morgan-website-worktrees/docs` on
`claude/docs-cycle`. Work there, push to its `origin/main`, and confirm **both** worktrees are 0-behind
before your first publish. Publishing from the shared website checkout was retired 2026-07-29.

**The procedure lives in the skills, not here** — `publish-to-blog` (Step 0 is *check the calendar
first*, and inverting that order is itself the bug; `--work-date` is mandatory; dry-run before every
publish) and `update-calendar` v1.4 (column ownership, the validator, and update `draftPath` in the same
pass when you move a draft). **Read them at publish time rather than trusting a summary here** — a
summary in a briefing is exactly the surface that goes stale without anyone noticing.

**The one thing the skills can't tell you, because it's environmental**: on Amber, `cwebp` and Pillow
are both absent and `sips` cannot emit webp, so image prep falls through to `sharp` (added 2026-07-30).
The dry-run **skips sync+fetch**, so it structurally cannot catch a missing toolchain — a clean dry-run
is not a proven path.

**dev/active/ Triage**:
- Archive stale files to `dev/YYYY/MM/DD/` date folders
- Move drafts to `docs/public/comms/drafts/`
- Deliver undelivered memos to recipient mailboxes
- Delete confirmed duplicates (files with `(1)` suffix)
- Keep genuinely active files; ask PM about unclear items

## Merge-Keeper Sweep (Standing Discipline, established 2026-04-28)

**This is now AUTOMATED. Run the script; do not hand-walk the branch loop** — the manual procedure that
used to live here was superseded by `scripts/merge-keeper-sweep.py` and was occupying 24% of this
briefing describing by hand what the script does.

```bash
python3 scripts/merge-keeper-sweep.py          # DRY-RUN IS THE DEFAULT — safe
python3 scripts/merge-keeper-sweep.py --apply  # actually merges the clean ones
```

**Verified working 2026-07-31**: evaluated the live branch set and correctly escalated
`claude/fix-docker-migration-setup`. Writes `dev/active/merge-keeper-YYYY-MM-DD.md`.

**What it decides for you**: auto-merges branches that are *wrapped* (last commit older than
`--age-hours`, default 24) **and** *clean* (no conflicts, no blobs >1MB, no `.env`/`.DS_Store`).
**It always escalates rather than guessing** — anything younger than the threshold, anything with
conflicts, anything with suspicious files in the diff.

**What is still YOUR judgment, and why the script can't do it**:

- **Identify the owner** of an escalated branch from its commits + that role's session log, then act: *wrapped* → merge; *active* → mailbox memo asking them to merge or send a NOTICE; *unowned/stale* → flag to PM one at a time, **never delete unilaterally**.
- **Skip explicitly-held branches** — a branch whose owner filed a NOTICE memo explaining the hold is not stranded, it's parked. ⚠️ **`claude/fix-docker-migration-setup` is currently held pending PM authorization to delete — do not delete without it** (carried from the 2026-07-21 handoff).
- **Log the sweep in your session log even when it's clean** (*"merge-keeper sweep clean, all branches at parity"*), so the discipline is visible rather than inferred from silence.

**Cadence**: every Docs session start, before other work · ad-hoc when PM or any agent surfaces a
stranding incident · before publishing a Ship.

### ✅ The PreCompact hook — it DOES fire (corrected 2026-08-01)

**`.claude/hooks/precompact-signoff-warning.sh` works.** Evidence: `dev/active/session-end-warnings.log`
on HOST's seat carries a real firing — `event=PreCompact tier=HARD ... unpushed=6217`, 2026-07-29 22:10.

⚠️ **How I got this wrong on 07-30, because the shape will catch you too**: I checked
`git log --all -- dev/active/session-end-warnings.log`, got nothing, and concluded the file *"has never
existed."* **The path is gitignored** (`.gitignore:136`) — so that query returns empty whether the file
exists on every seat or none. **The instrument could not see the thing it was asked about, and its
silence read exactly like proof of absence.**

**Two operative consequences:**
- **The log is per-seat and gitignored.** Absent in your worktree means *you* haven't had a firing — not that the mechanism is dead. Check your own seat with `ls`, never with `git log`.
- **You now have two working nets**, not one: this hook *and* the merge-keeper sweep.

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
