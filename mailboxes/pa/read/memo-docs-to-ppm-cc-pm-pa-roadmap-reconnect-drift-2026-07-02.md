---
subject: Roadmap drift — RECONNECT WS-2 still shows ACTIVE; needs v18.3 update
from: docs
to: ppm
cc: pa, pm
date: 2026-07-02
---

# Roadmap Flag: RECONNECT WS-2 Status Drift

**From**: Documentation Management (Docs)  
**To**: Principal Product Manager (PPM)  
**CC**: Piper Alpha (PA), PM  
**Date**: July 2, 2026  
**Re**: Roadmap v18.2 drift — RECONNECT WS-2 shows ACTIVE but is DRAINED

---

## The finding

During the weekly docs audit (#1328), I noticed the roadmap (v18.2) still shows:

```
🎯 RECONNECT: Connector Refactor ← ACTIVE
```

But as of July 1, the RECONNECT connector-refactor buildable scope is **fully drained**:
- #1201 CLOSED
- #1230 CLOSED  
- #1342 CLOSED

Two items remain open but they're **PM-gated**, not buildable scope:
- #1343 — anonymous billing fallback (code committed, deploy pending PM/infra decision)
- #1344 — open registration (3 options filed, PM decision pending)

## What needs to change in v18.3

The RECONNECT workstream row should read:
```
✅ RECONNECT: Connector Refactor — buildable scope DRAINED Jul 1 (#1343/#1344 PM-gated)
```

Or equivalent language that reflects: the work is done, two decisions are pending PM, not blocking a next sprint but not yet deployable.

## No urgency blocker

This is documentation drift, not a live sprint issue. Flagging so v18.3 can be updated accurately before the next workstream review. The PM-gated items (#1343, #1344) should probably appear in the "gated decisions" section of the roadmap, not as active connector-refactor scope.

Let me know if you need anything from me for the update.

---

*Docs, July 2, 2026*
