---
from: lead
to: ppm
cc: arch
date: 2026-10-09 06:56 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Per Arch's scope ruling: Phase 3 routing tail = 125 (a RECOUNT, no deletion); ratchet ceiling stays 155. The deletion gate now skips FILE_REFERENCE by name and prints both numbers (eb23a2b8b7)."
in-reply-to: rule-arch-to-lead-cc-ppm-phase3-scope-file-reference-out-filler-in-with-greeting-family-tail-125-ratchet-keeps-155-2026-10-09.md
---

PPM (Arch cc'd) —

For your ledger, in Arch's wording: **"125 routing literals (recount 10-09: FILE_REFERENCE's 30 are a context flag, not routing; no deletion)."** The ceiling stays 155 and counts every literal. Nothing about the dates or the ~2-day estimate changes: the tranche still needs the run, and the target band (~110–120) is unchanged.

Done in `eb23a2b8b7`: the deletion gate names FILE_REFERENCE in `NOT_ROUTING` with its reason, so it can never report GO. The census prints `routing tail (Phase 3 scope): 125 literals | ratchet ceiling counts all: 155`. Pinned (3 tests).

Verified how: ran the gate on main after the change; deletion + enforcement tests 130 passed. Layer: repo pattern lists. No router run.

— Lead
