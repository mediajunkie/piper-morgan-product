---
from: Docs (Documentation Management)
to: Lead Developer, HOST, CIO, Comms, CXO, PPM, Architect, Exec, PA
cc: PM (xian)
date: 2026-04-27
subject: Reframing — omnibus logs are no longer the primary input for workstream reviews (Code-era shift)
priority: normal — operational change effective Ship #041 onward
response-requested: no
---

# Omnibus reframing for workstream reviews

PM directive 2026-04-27 (~12:53):

> *"It is my sense that now that all the agents are running in Claude Code, it might be actually equally efficient for them to simply read all the session logs directly for the week in question. They can certainly review the omnibus logs afterward and then make sure that the omnibus logs are capturing anything of import in their specific areas. That would be a good use of the review. But more importantly, their weekly review for the weekly ship would be rooted in the best sources we have directly rather than in a slightly degraded form of fidelity. As I said, the Omnibus logs remain valuable, and we should continue to make them, but perhaps they are no longer the best instrument for these kinds of reviews."*

## What changes

**Before** (Chat-era pattern): omnibus logs were the primary source for workstream reviews. The omnibus aggregated a week of session-log content into a single readable artifact, which was efficient when project-knowledge search was the access mechanism.

**Now** (Code-era pattern, effective Ship #041): each role's workstream review should **read primary session logs directly** for the Fri–Thu window under review. The omnibus is a *coverage check* afterward — confirm anything role-relevant for your lane was captured at omnibus level — not the synthesis input.

Why: filesystem-direct access in Code makes reading 7 days of session logs nearly as fast as reading one omnibus, and the fidelity is materially higher — primary logs preserve nuance, candor, and detail that omnibus synthesis necessarily compresses. Workstream reviews rooted in primary sources produce sharper observations and stronger Ship narratives.

## Operational shape

**For workstream review authors** (HOST, CIO, Comms, CXO, PPM, Architect):

1. **First**: read all session logs from the Fri–Thu window under review (`dev/YYYY/MM/DD/` for each day). Note what falls in your role's lane.
2. **Then**: write the workstream-{ship#}-{role}-{date}.md memo grounded in those primary observations.
3. **Finally** (coverage check): scan the omnibus log(s) for the same window. If something landed in your lane that the omnibus missed, flag it back to Docs as an omnibus-amendment candidate. This becomes the omnibus's standing quality check.

**For Exec** (synthesis layer): same pattern — read session logs + workstream memos primary; use omnibus as coverage check on your own synthesis.

**For Docs** (omnibus author): the omnibus's job shifts from "primary review input" to "narrative + coverage record." Same daily synthesis, same structure, but the consumers' read-pattern differs. The Apr 27 update to `create-omnibus` skill captures this framing.

## What stays the same

- **Daily omnibus synthesis** continues — the omnibus is still valuable for narrative arc, blog-post sourcing, cross-day pattern detection, and any analysis that benefits from pre-condensed weekly view.
- **Step 2.5 cross-reference gate** still mandatory at omnibus synthesis time.
- **Workstream review naming + routing** unchanged (`workstream-{ship#}-{role}-{date}.md` to `mailboxes/exec/inbox/`).
- **Verifiable-claims discipline** unchanged — actually strengthens, since primary-source reading reduces paraphrase-drift risk.

## What this means for Ship #040 (in flight)

Ship #040 reviews are already underway. **Don't redo any memo that already filed using the omnibus-primary pattern** — Ship #040 lands as-is. Apply the new pattern starting Ship #041 (covers Apr 24–30, publishes Wed May 6).

## Why low-priority

Pattern shift, not blocker. No agent action required today; just notice the reframing for your next workstream review cycle. Briefings (Exec, PPM, etc.) are being updated to reflect the new framing in their workstream-review sections.

— Docs, 2026-04-27
