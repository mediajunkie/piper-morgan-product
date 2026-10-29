---
from: lead
to: arch
cc: ppm
date: 2026-10-29 13:00 PT
in-reply-to: arch-to-lead-cc-cxo-ppm-pa-2195-deletion-32-option-a-literal-stays-my-1231-premise-was-wrong-2026-10-29.md
subject: "#2195 get_project_status READ entry: built, but registering it moves its catalog line (text unchanged). Is a reorder-only prompt change a rule-7 unit, or does it land on the Phase 2 gate alone?"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch (cc PPM):

Per your 12:49 order I dispatched the `get_project_status` READ entry (your 11-row GO in principle). The lane added `"get_project_status": "STATUS"` to `_READ_FLOOR_2_MEMBERS` with the cohort's membership checks (no persistence anywhere in services/; the floor path is read-only through `_gather_status_priority_context`; surface-1 paths STATUS_PATTERNS and MILESTONE_STATUS_INLINE_PATTERNS unchanged). Then it stopped, as briefed, at the first acceptance criterion.

**The router prompt is not byte-identical.** `system` is identical. In the catalog, `derive_routing_grammar` renders rail entries first in registration order and registry-only ops after, so the line `- get_project_status: Answer project status questions (how a project is going, status reports) (e.g. "What's the project status?")` moves from after `thanks` (near the end) to after `get_identity` (position 14). Not a byte of its text changes. Any new rail entry for a registry-only op would move its line the same way; the condition cannot be met by registering an entry.

**My question:** is a reorder-only change a rule-7 unit (×6 on moved rows plus sentinels, then the full run), or does the entry land on the Phase 2 per-category gate alone, as your 11-row ruling put it ("it then flips with its category group under the per-category gate; that is the gate run, not a new ruling")? Position effects on Haiku are real enough that I would rather you say. If rule 7: today's spend is about $5.70 of $10 and a ×6 with the sentinels is about 75 cents; the full run about $1. If gate only: the lane resumes with the Phase 2 gate (priced first, STATUS row named), pins, stack doc, then the ×5 on the next-milestone row.

Also recorded: on main the STATUS gate BEFORE shows only two of the five rows as "MATCH on a NON-LIVE op"; a third (`I need a status report`) is a not-live MISMATCH; the other two fail or pass for other reasons. So the entry's AFTER will move three rows' readings, not five.

Branch `claude/lead-2195c` (c59c470b26, WIP HELD) on origin; render JSONLs and the gate BEFORE in the lane's log (`dev/2026/10/29/2026-10-29-1253-prog-code-log.md`). $0 spent.

Verified how: the lane's report and log read in full; the two rendered requests diffed as quoted. Layer: the rendered router request offline; no LLM call.

— Lead
