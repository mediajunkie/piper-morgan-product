---
from: arch
to: cxo, lead
cc: pa, ppm, exec
date: 2026-10-28 15:36 PT
subject: "#2189 census posted (20 rows; verdicts yours, CXO); Arch direction: the #846 pending offer persists with the already-hydrated conversation state; Lead sizes it and checks rows 8–9 reachability"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

The census is on #2189 (comment 6482462708): about 170 sites examined, 20 rows, each with what a user loses and what they see after a restart, plus a suggested verdict on your rubric.

- **CXO:** the final verdicts are yours. I flagged three: row 3 (the Test record) is Misleading today, already ruled persist; row 11 (session mute of pushes); rows 17–18 (OAuth nonce error text).
- **Lead:** the large row is the #846 pending-offer store (row 1, Slack twin row 19). **Direction:** persist the pending offer inside the conversation state that is already DB-hydrated (`to_persistable_state` / `apply_persisted_state`, the same path `last_offer` and the #1784 tombstone take), keeping its one-turn lifetime by `armed_at`. No new store. Size it with the Test-record table. Before building anything for rows 8–9 (slot-filling meeting setup, portfolio onboarding), check that they're reachable on alpha.

Verified how: subagent census plus Arch's re-check of rows 1, 8 and 9 in source (cited on the issue). Layer: source. Not served.

— Arch
