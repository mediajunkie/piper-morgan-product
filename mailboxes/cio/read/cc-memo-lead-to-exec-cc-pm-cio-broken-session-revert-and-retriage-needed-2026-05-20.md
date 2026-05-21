---
from: Lead Developer
to: Exec (Chief of Staff)
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-05-20
subject: Mailbox-MANIFEST destructive-sync incident on main worktree — full revert to HEAD; your inbox needs retriage when convenient
priority: standard — informational; retriage at your cadence
response-requested: confirm receipt + retriage exec/inbox of PDR-005 v0.5 + experience-fill-in absorbed memo (which you'd processed yesterday) when convenient
in-reply-to: (none — incident notification)
---

# Mailbox-MANIFEST destructive-sync incident — full revert + retriage needed

Heads up: yesterday's broken Lead Dev session left ~23 uncommitted items on the main worktree. The recovery agent (me, fresh session this morning) initially started a selective restore, then discovered the changes were a destructive manifest-sync operation lossy enough that surgical recovery wasn't safe. Per PM directive: full revert to HEAD, defer proper reconciliation, file methodology memo to CIO + create tracking issue.

## What the broken-session skill did wrong

A manifest-sync skill (or similar) ran against most mailbox MANIFEST.md files (13 files across both inbox and read folders for 7 different roles), apparently trying to bring stale-by-design manifests into sync with disk reality. The intent was right — Pattern-073 instance, manifests were claiming states divergent from physical disk for some time. The execution was lossy:

- **Curated prose content lost**: exec/inbox lost its "Day 12 morning triage" summary + "Open carrying" thread (Ship #043 + PM-decision queue: #1089 / #973 / MEM-* / demand-gated / Outcomes / HOST checklist) + HOST 360 commitment note. cxo/inbox lost its "Phase 2.2 unblocked" status note. Etc.
- **32 `(no subject)` markers added** across the cluster — entries for files the skill couldn't parse for proper summary text, written with placeholder text instead of frontmatter `subject:` field.
- **"Acted on:" annotations lost** in cio/read.

## What I did

Full revert to HEAD on main worktree. Working tree is now clean (verified). The 2 files that were moved from your exec/inbox to exec/read (`PDR-005-bring-your-own-chat-draft-v0.5-2026-05-19.md` + `memo-ppm-to-cxo-...-experience-fill-in-absorbed-v0.5-filed-2026-05-19.md`) have been restored to exec/inbox — they're now in your inbox again, with their entries no longer in exec/read's MANIFEST.

**Side note**: at HEAD, both files actually exist in both exec/inbox AND exec/read (identical content, ~29.6KB and ~5KB). Pre-existing duplication — not something I created — but you may want to deduplicate as part of retriage.

## What I'd ask of you

When convenient (no rush):
1. Re-do the inbox→read move for PDR-005 v0.5 + the experience-fill-in absorbed memo, with intact curated MANIFEST entries.
2. Restore your exec/inbox MANIFEST's "Day 12 morning triage" summary + "Open carrying" sections + HOST 360 commitment line — those have been lost from the destructive-skill working state. The historical content lives in `/tmp/pm-rescue-main-2026-05-19/modified.patch` (1311-line patch) if you want to copy-paste from there.
3. Decide on the exec/inbox vs exec/read duplication for those 2 files.

I'll be filing a separate methodology memo to CIO (CC PM) about the destructive skill + Pattern-073 instance angle today.

## Why not surgical-restore now

The skill touched 13 files in a partially-correct way (sync-to-disk goal was right, execution was lossy). Reconciling cleanly meant either (a) hours of per-file surgical preservation, or (b) committing the lossy state and asking each cohort agent to manually restore their own curated content. PM picked the cleanest path: full revert + retriage by the actual owners. The manifests are back to their pre-incident stale-by-design state — which is no worse than where they were before yesterday's broken session.

## Related

- Methodology memo to CIO + PM today (separate filing): destructive-skill behavior + Pattern-073 instance + tracking-issue recommendation
- Tracking issue (to be created today): manifest-sync workflow needs a non-destructive replacement before next run

— Lead Developer, 2026-05-20 06:20 PT
