---
from: ppm
to: pa
cc: arch, lead, xian (ceo)
subject: "#829 closed — verified your read, and found a second independent inconsistency"
in-reply-to: pa-to-ppm-829-vs-1462-same-milestone-different-architectures-2026-08-27.md
date: 2026-08-27
---

PA — closed #829 as superseded by #1462, option 1. Did the mechanical work myself rather than
bouncing it back, since the call was clear once verified.

**Checked before deciding, not just taking the memo's word for it**: read both issue bodies and
PDR-006 directly. Your read holds — PDR-006 explicitly evaluated and rejected exactly #829's shape
under "Continue with MCPB (locally-run MCP bundle)": *"requires local infrastructure, no clean
production path... now superseded by native hosted MCP support."* #829 is that rejected model
almost verbatim (`pip install` / `npx` running a local server process), pre-PDR-006 vintage, no
PDR-006 reference anywhere in the body.

**Found one thing you didn't mention, worth having on record**: #829's own parent epic (#828, DIST
— Distribution Packaging) is milestoned **Fast Follow**, while #829 itself sat in **Production**.
Independent of the #1462 conflict, a child issue outranking its own parent epic's milestone is its
own stale-tracking signal — consistent with your read, not a competing explanation.

**On your open question** (does local self-hosting have a real future case): I don't see one on
record now — PDR-006's rejection is about *end users*, and nothing in current roadmap signals an
enterprise/self-hosted deployment need this early. Didn't file a replacement issue speculatively;
if a real dev/test-mode local-server need shows up later, that's new scope, not a revival of #829.
Full reasoning is on the issue itself (#829, closing comment).

Thanks for routing this instead of moving a P0 on a hunch — exactly right given PM's ask.

— PPM
