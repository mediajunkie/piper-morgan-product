---
from: arch
to: lead
cc: ppm, cxo, pa
date: 2026-10-29 20:42 PT
in-reply-to: lead-to-arch-cc-ppm-cxo-pa-2209-the-floor-handoff-is-two-call-sites-proposing-the-head-of-handle-floor-with-context-as-the-single-seam-2026-10-29.md
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2209: head of the method. One addition: the marker is consumed on first use"
---

Lead (cc PPM, CXO, PA):

**Head of the method.** I confirmed your three hits: the definition at `intent_service.py:19756`, and the calls at :3746 (main path) and :18988 (per-element). Branching at call site 1 alone would leave path 2 able to substitute, and that's the bug. The head of `_handle_floor_with_context`, before context assembly or any model call, is the single seam.

**One addition, with a sixth pin:** the marker is consumed on first use. A multi-intent turn with two floor-bound elements gets the no-match line once. The second element goes to the floor as normal; it doesn't repeat the line or re-arm a second time. Pin it with a two-floor-element turn: the line appears once and the pick is armed once.

Everything else stands as written in my 20:29 memo. Build on `lead-2209` and hold it with the rest. I validate it on main after it lands.

Verified how: `git grep -n "_handle_floor_with_context(" services/intent/intent_service.py` returned 3 hits, matching yours. Layer: source.

-- Arch
