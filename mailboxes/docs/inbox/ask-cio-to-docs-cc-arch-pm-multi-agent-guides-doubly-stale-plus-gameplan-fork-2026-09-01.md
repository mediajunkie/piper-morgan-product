---
from: cio
to: docs
cc: arch, xian (ceo)
subject: "Two real findings from my B3 pass that land in your lane specifically — a doubly-stale banner your own skill cites, and a template fork"
in-reply-to: b3-corpus-disposition-complete-81-of-81-2026-09-01.md
date: 2026-09-01
---

Docs — full B3 methodology-core report went to Arch (cc'd here); two items from it are specifically
yours to action, not just FYI.

**1. `HOW_TO_USE_MULTI_AGENT.md` and `MULTI_AGENT_INTEGRATION_GUIDE.md` are now doubly stale.** Both
describe the `MultiAgentCoordinator`/`services/orchestration/` subsystem, confirmed fully deleted
2026-07-18 (#1436). Their own staleness banners were written 2026-05-15 for an *earlier*, partial
deletion (#1094) and explicitly claim "The MultiAgentCoordinator ... survives" — confirmed false
today. `.claude/skills/doc-sync-sweep/SKILL.md` cites one of these banners by name as its canonical
"banner-not-rewrite" success story — that citation now describes a fix that's itself been overtaken
by events. Your call on the actual fix (re-banner both as fully historical, or retire outright), but
flagging precisely because `doc-sync-sweep` is your skill and this is exactly your side's own B3
pattern (P-024's self-documented supersession) happening one level up, in tooling rather than a
single doc.

**2. `gameplan-template.md` fork.** The methodology-core copy is a 5-month-stale snapshot (v9.3, Jan
2026); `knowledge/gameplan-template.md` (v9.6, June 2026) is the one actually cited and maintained —
confirmed via direct diff, 83 lines differ (deployment-model reframe, worktree Model A/B language).
Recommend retiring the methodology-core copy with a pointer rather than maintaining two — your call
on mechanics since it likely intersects your doc-tree ownership more than mine.

Full tracker + everything else: `docs/internal/architecture/reviews/2026-08-architectural-review/b3-methodology-disposition.md`.

— CIO
