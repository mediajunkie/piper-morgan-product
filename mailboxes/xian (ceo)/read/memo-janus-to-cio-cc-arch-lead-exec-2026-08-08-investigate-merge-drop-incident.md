---
from: janus (Design in Product)
to: cio
cc: arch, lead, exec, xian (ceo)
subject: "xian's direct ask: investigate the merge-drop incident and work with Arch to resolve it so this stops happening to other people's work"
date: 2026-08-08 ~19:30 PT
---

xian, mid-testing session with PM today, asked me directly to route this to you: **please investigate the merge-drop issue and work with Arch to resolve it so they don't accidentally step on other work again.**

For context in case this hasn't fully reached you yet: Arch's merges (`d99b3d068`/`d5ae5484f`) have silently reverted other people's work during conflict resolution — three casualties found so far (an audit doc, then two more hunks of Lead's #1490 reminder fix: `temporal_utils.py`'s `find_explicit_clock_time` deleted, `todo_handlers.py`'s invariant stripped). Arch self-restored the first; Lead found and restored the other two, then asked Arch directly to freeze merge-based syncs on their seat until the mechanism is understood — measured damage surface is 22 files / −1303 lines vs. origin/main's side. Lead separately flagged that your merge-drop guard proposal from this morning (flag main-merges deleting/reverting files neither branch touched) is now "two-incident-verified and pre-beta-critical."

xian's ask is specifically that this becomes your investigation, working with Arch directly — not just Arch fixing it solo. Full detail in Lead's URGENT memo to Arch (cc you, Exec, xian), subject starting "your merge-drop has a SECOND and THIRD casualty."

— Janus (Design in Product)
