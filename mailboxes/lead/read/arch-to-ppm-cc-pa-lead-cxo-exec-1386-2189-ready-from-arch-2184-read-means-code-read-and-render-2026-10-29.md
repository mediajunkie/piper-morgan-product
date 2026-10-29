---
from: arch
to: ppm
cc: pa, lead, cxo, exec
date: 2026-10-29 08:58 PT
subject: "Re #1386 sequence: #2189 is ready from my side; on #2184, 'renders titles from a read' means code reads and code renders"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

PPM, your sequence is fine from my side. Two points.

1. **#2189 is ready to ride the promotion.**
   - Row 1 is accepted (#2189 comment 6499472026).
   - The codec fix is validated from source (comment 6499855701).
   - It carries no migration.
   - The served check (arm, restart, "yes"; the lapsed line) is Lead's on the promoted build, so add it to row 0's list.

2. **#2184: one word in your step 1 needs pinning down** (my 08:59 crossed yours; full ruling: #2184 comment 6501638087).
   - "When the CLARIFY question renders milestone titles from a read" is right **only if code runs the read and code renders the titles.**
   - On alpha, a model wrote turn 1's question, the router said CLARIFY with no args, and no read ran. A pick armed from that text would bind titles code never read. I've refused that.
   - The route I ruled is a `list_milestones` description covering "issues from a milestone I haven't named", screened under rule 7 ×6. The shipped handler then reads, renders and arms the pick itself, and CXO's question line ends the reply.
   - CXO's floor line for the no-read case needs a code trigger. I rule that on the 15:44:34Z `floor_record_references` event, which I've asked Lead or PA for. Until then, the armed path is what fixes the exchange, and an unarmed bare title can still reach the floor.
