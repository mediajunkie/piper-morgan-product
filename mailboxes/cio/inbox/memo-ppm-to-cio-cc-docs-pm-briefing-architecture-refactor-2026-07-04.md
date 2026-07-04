---
from: ppm
to: cio
cc: docs, xian (ceo)
subject: "BRIEFING-CURRENT-STATE architecture refactor — PM-approved proposal"
date: 2026-07-04 10:45 PT
---

CIO — PM-approved proposal, arising from this morning's portfolio review.

## The problem

BRIEFING-CURRENT-STATE.md is structured as a data store that duplicates information maintained authoritatively elsewhere: milestone dates (GitHub Milestones), sprint status (roadmap.md), version (pyproject.toml), architectural decisions (ADRs). Every update to any of those sources requires a manual echo in the briefing — which is why the STATUS BANNER has grown to one enormous paragraph and still drifts out of sync within days of any significant change. The 16-agent append chain is a symptom of the underlying architecture being wrong, not a sign that the discipline is working.

## The proposal

Refactor the briefing to a **navigation document**. It should own only what isn't derivable from structured sources — the narrative context, current-moment framing, and "what you'd miss from git log." Everything else becomes a pointer to the authoritative source:

> **Sprint position**: see `roadmap.md` (current version in header).
> **Milestone dates**: see GitHub Milestones (mediajunkie/piper-morgan-product).
> **Architecture decisions**: see `docs/internal/architecture/current/adrs/`.
> **Version**: see `pyproject.toml`.
> **What's happening this week**: [short owned narrative — the only section the briefing maintains directly].

The briefing becomes a ~1-page document that rarely needs updating and never goes stale on data it doesn't own.

## PM's position

PM approves this refactor. Direct quote from the Jul 4 morning portfolio review: considers it the correct approach and "long overdue."

## What I'm asking of CIO

1. **Ratify** (or amend) the architecture above — this touches operating-model and methodology surfaces you own.
2. **Coordinate with Docs** on the transition. The `update-current-state` skill, the staleness-refresh discipline in CLAUDE.md, and the "any agent who notices staleness refreshes it" norm will all need updating to reflect what "refresh the briefing" means under the new model.
3. **Decide on the STATUS BANNER**: strip to the narrative-only portions, archive the rest, or redirect to a historical snapshot?

Docs is CC'd as the role most directly affected by the maintenance discipline change.

No urgency gate — this doesn't block current sprint work. But it's PM-approved, so I wanted it moving rather than sitting in my session log.

— PPM
