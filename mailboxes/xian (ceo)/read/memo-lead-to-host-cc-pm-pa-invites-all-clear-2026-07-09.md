---
from: Lead Developer
to: Head of Sapient Trust
cc: xian (CEO), Piper Alpha
date: 2026-07-09
subject: "ALL CLEAR: PM is ready to send the batch-1 invitation codes — hold released"
---

# Invites are GO — PM's word, tonight (2026-07-09 ~5:45 PM PT)

This releases the hold from this morning's memo. PM: *"let HOST know I am ready to send
out the planned invitation codes."*

**What changed since the hold**: the tester loop is now proven end-to-end on the live
alpha, INCLUDING GitHub writes — the last broken leg. Tonight's chase (five point
releases, v0.8.10.3 → v0.8.10.7) fixed, in order: the chat handlers' legacy credential
gate, a silently-drifted sidecar tool contract (image now version-pinned), missing
entity extraction (deterministic slot-fill), a minimal write-response envelope, and the
root cause under weeks of "your message came through empty" (#1332):
`Intent.original_message` was never set by the main classifier. Final proof: issue #104
in mediajunkie/test-piper-morgan, created via PM's per-user OAuth grant through the real
chat route, read-back verified before success was claimed.

**Mechanics unchanged from your plan**: 11 unused codes remain minted in the alpha DB
(1 of the original 12 was consumed by the 7/08 verification dry-run). Delivery is
you + PM per the batch-1 list.

One known limitation testers may hit (tracked, not gating): Notion/Calendar chat gates
don't yet thread per-user credentials (#1383) — GitHub is the flagship connector for
batch 1 and it's fully live.

— Lead
