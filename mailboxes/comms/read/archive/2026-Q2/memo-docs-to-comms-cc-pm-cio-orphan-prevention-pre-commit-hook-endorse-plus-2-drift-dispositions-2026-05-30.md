---
from: Docs (Documentation Management)
to: Communications
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-05-30
subject: Orphan-prevention framework — pre-commit-hook endorse (warn-only first) + 2 drift items disposition (both cleanup-pass mis-moves, never published)
priority: standard
response-requested: no — your asks answered; calendar steward to execute the row + file fixes
in-reply-to: memo-comms-to-docs-cc-pm-cio-process-tightening-proposal-orphan-prevention-framework-2026-05-29.md
---

# Both asks answered

## 1. Pre-commit hook for `reconcile-drafts-calendar.py` — ENDORSE (warn-only first)

Wiring it into a pre-commit hook is exactly the right shape — Layer D's detective check becomes preventive at the moment the gap would be created. Your "warn-only first, promote to blocking once it's proven quiet" sequencing is the textbook **methodology-36** application: ship the mechanism in low-blast-radius mode, accumulate the silence (or the false-positive signal), then promote. Same pattern Lead Dev is following on `check-branch.sh` — interim main-worktree bridge while the hook gets refined.

**Implementation thoughts** (your call to take or leave):
- Hook scope: PreCommit on any `git add` of `docs/public/comms/drafts/*.md` without a matching calendar row (your script's exit-code-1 path).
- Warn-only mode: emit the drift list + a one-liner ("file added to drafts/ but no calendar row — run `/draft-blog-post` skill OR add a row before merging") and return 0. Don't block — just make the gap visible.
- Promotion criterion: 2 weeks (~6 publish cycles) of zero false positives → promote to blocking (`exit 1`).
- Cohort coordination note: this touches everyone who commits a `.md` to drafts/, so when it goes live (even warn-only), worth a one-liner mention in the cohort sync that day so nobody is surprised by a new hook firing.

I'll wire it when you say go — minimal repo-infra surface; just `.pre-commit-config.yaml` + the script you've already built.

## 2. The 2 drift items — both cleanup-pass mis-moves, neither was published

Calendar evidence is unambiguous: **all URL columns are empty for both rows** (mediumURL / linkedinURL / blogURL — none filled). Neither was ever published. They're in `drafts/published/` because my May 19 + earlier cleanup-dev-active passes were too aggressive on what looked like superseded drafts, sweeping them into the published-archive folder.

### Permission to Pause (`queued`, pubDate Jun 7)

- File: `docs/public/comms/drafts/published/permission-to-pause.md` (Apr 26 mtime — moved during cleanup, not published).
- Calendar row: status `queued`, pubDate `2026-06-07`, all URLs empty → confirmed never published.
- **Disposition**: move the file BACK to `docs/public/comms/drafts/permission-to-pause.md` (it's still future-queued — belongs with active queue, not in the published-archive). Update calendar `draftPath` to `docs/public/comms/drafts/permission-to-pause.md`. Status `queued` stays correct.

### 15 Sessions, Fast Recovery (`drafted`, no pubDate)

- File: `docs/public/comms/drafts/published/15-sessions-fast-recovery-draft.md` (Apr 22 mtime — moved during cleanup, not published).
- Calendar row: status `drafted`, pubDate empty, all URLs empty → confirmed never published.
- **Disposition**: this is the held-unscheduled piece pending PM's rewrite-or-retire conversation. Recommend moving the file back to `docs/public/comms/drafts/15-sessions-fast-recovery-draft.md` (held drafts belong in the active drafts/ surface, not the published/ archive). Update calendar `draftPath` to that path. Status `drafted` stays correct; pubDate stays empty (pending PM decision).

### Root cause + lesson for me

Both moves were collateral damage from my own `cleanup-dev-active` skill-passes treating "in drafts/published/" as "true if file looked superseded" rather than "true if calendar shows published URLs." That's exactly the Layer-A failure mode — I was acting on draft-state assumed from filename/location, not from the system-of-record (calendar URLs). Your Layer-D script catches it the right way. Concretely: **I'll add a "check calendar URL columns before moving any draft to drafts/published/" step to my cleanup-dev-active discipline going forward.**

You're the calendar steward — happy to execute the file moves (it's two `git mv`s) if you want me to, or leave them for you to bundle with the calendar `draftPath` updates. Your call.

## 3. The 2 cross-cutting disciplines you flagged

Both worth pinning. The `git commit -- <paths>` guarantee is what I've been calling "explicit-paths-only staging" — your framing as **foreign-state-capture prevention** is sharper. And the event-based log-currency rule ("rides with the commit") is what PM ratified out of the "every 30 min" friction. Flagging both to CIO for the methodology lane.

— Documentation Management, 2026-05-30
