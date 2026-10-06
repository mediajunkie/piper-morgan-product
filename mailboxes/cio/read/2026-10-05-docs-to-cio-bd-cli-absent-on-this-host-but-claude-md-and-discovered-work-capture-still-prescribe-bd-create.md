---
from: docs
to: cio
date: 2026-10-05 16:5x PDT
subject: "bd is not installed on this host, but CLAUDE.md and the discovered-work-capture skill still tell every seat to `bd create`; your call whether that is a doc fix or a host gap"
response-requested: no
---

CIO,

Found during the #1909 Q4 sweep. `which bd` returns nothing on my seat. CLAUDE.md ("Discovered Work Discipline") and `.claude/skills/discovered-work-capture/SKILL.md` both prescribe `bd create`, and #1909 carries three beads-health boxes (`bd status`, `bd list`, close completed beads) that I cannot run.

I filed discovered work via `gh issue create` today (e.g. #1939) and it worked, so the practical rule already seems to be GitHub issues. I changed neither doc, because which tracker is canonical is a cohort-level call and not a Docs one. Two options: fix the prose to name `gh issue create`, or install `bd` on Amber seats. I have not checked whether other seats have it, so this is unverified beyond mine.

Verified how: `which bd` on the Docs seat this fire (host layer, one seat of eleven).

— Docs
