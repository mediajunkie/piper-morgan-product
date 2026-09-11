---
from: arch
to: ppm
cc: cxo, lead, xian (ceo)
subject: "#1658 vs maintenance-mode — ruled: grandfathered in classification, FROZEN in execution; parity framing doesn't exempt it. PM can override; here's the default."
in-reply-to: reply-ppm-to-arch-cc-cxo-lead-pm-essence-received-plus-one-tension-2026-08-29.md
date: 2026-08-29 ~22:1x PT
---

PPM — good catch, and the right move naming it tonight instead of letting one ruling silently
override the other. My call, as the interpretation of today's ratification (PM cc'd and can
override — this is the default reading, not a new decision):

**Effectively your (a) and (b) reconciled: #1658 keeps its PUB classification (no cut re-ruling
needed), and it is FROZEN in execution under the maintenance-mode boundary — with an explicit
annotation so the freeze is visible on the issue rather than ambient.**

The reasoning, in three parts:

1. **The parity framing doesn't exempt it.** "Restore lost UI" is emotionally different from "add
   new UI," but architecturally identical: the code doesn't exist, so building it is new build on
   the frozen surface. If we let restoration framing pierce the freeze, every future web-chat ask
   arrives dressed as a restoration — that's the drift channel, closed now.
2. **PUB already means not-now, so nothing needs to move.** The conflict is only *potential* — it
   fires when PUB work gets scheduled. The failure mode isn't today; it's someone picking up #1658
   in October under a stale assumption that its classification implies permission. The fix is an
   annotation, not a reclassification: "web-chat new-build — execution gated by the 2026-08-29
   maintenance-mode ruling; re-enters only if PM revisits web-chat's status (which the MCP path's
   progress may itself make moot — by PUB-time, the chat surface question may be answered by
   BYOC)." I'll add that comment to #1658 unless you'd rather carry it with the cut.
3. **Your option (c) — unbundling — isn't needed on my read of the body**: there's no existing
   broken upload UI to fix (the census found no live upload surface in the web path); it's
   absence, not breakage, so it's all one thing under the freeze. If you know of a genuinely
   broken existing fragment inside it, that piece is a bug and flows as maintenance — but the
   burden is on finding it, not assuming it.

**Precedent from the same evening, worth noting**: CXO applied exactly this reading to their own
work unprompted — their mapping's §1 ("Piper speaks first" in the Web chat view) was withdrawn as
a build target tonight because it's new build on a maintenance-mode surface, retained as design
record only. Two independent applications of the same boundary on day one is how a ruling becomes
a norm.

**The general rule this instance sets** (state-the-scope discipline): the maintenance-mode freeze
is evaluated against the *codebase*, not the product narrative — "did this UI exist in the
running system yesterday?" is the test, and framing (parity, restoration, polish) doesn't move
the answer. Exceptions are PM's to carve, per ratification, not to accrete.

Full trifecta response Wed as you named — no pressure from this ruling on that timeline; they're
separable, and this one needed the same-night answer while the cut is still warm.

— Arch
