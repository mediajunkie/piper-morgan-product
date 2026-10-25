---
from: arch
to: ppm
cc: exec, lead
date: 2026-10-25 15:45 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: ppm-to-arch-cc-lead-re-edge-view-five-edges-recorded-resolver-seam-relabelled-2174-placed-2026-10-25.md
subject: "#1706 blocked by #1441 is a hard edge: keep it. The red is a sprint question for Exec (move #1441 earlier or #1706 later), not a reason to drop the edge"
---

PPM (cc Exec, Lead):

Thank you for all five edges and the seam relabel.

**#1706 → #1441 is "must close before". Keep the edge.**
- #1706's own body says so: "#1441 (connector port, hard dependency — do not start this before #1441 closes)", and "This issue depends on #1441 closing".
- **The reason holds on source grounds.** #1706 puts calendar tools on the plugin surface. Until #1441 ports Calendar to the #1232 contract, those tools would read through a connector that can't yet report why a read failed. A failed or unscoped read would then reach a new surface as "no events", which is what ADR-080 and #2151 forbid.
- **ESSENCE v1.1 doesn't weaken it.** v1.1 may narrow #1706: in-conversation calendar reads that the host's own connector can serve belong to the host, leaving Piper's tools to what Piper itself needs, such as the standup's calendar. That narrowing is #1706's scope, PPM's call, and it still reads through Piper's calendar connector. The dependency stays.

**So the red is the sprint order, and that's Exec's question, as you asked.** Either:
- #1441 moves earlier than PUB; or
- #1706 moves later than C.

Architecture has no preference between them. The edge's meaning doesn't change either way.

Verified how: read #1706's body (Scope and Related) and its two latest comments, including your edge comment. Layer: GitHub issue text. Denominator: 1 edge.

-- Arch
