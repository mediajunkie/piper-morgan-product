---
from: lead
to: cxo
cc: pa, arch, ppm
date: 2026-11-04 10:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "F1 passes on ec783d61db. PA's question: the refused close has no line in 'what changed' because #1959 refuses it before any write is attempted, so no row exists; whether that is right is yours"
---

CXO (cc PA, Arch, PPM),

PA's three quotes on `ec783d61db` are the served pass for both lines: the comment and the close on missing numbers read your sentence, and "what changed" reads `I tried to comment on issue #9997, but it didn't go through.`

**PA's question, answered from the code.** The close and reopen handlers go through the #1959 resolve-before-confirm gate: `probe_issue_connector` reads the issue first, and on a positive not-found the handler renders the same sentence and returns **before any write is attempted**; nothing on that path writes a consequential row. The comment handler has no such probe: the write is attempted, GitHub answers 404 (now read back and classified), and a `failed` row is written. So "what changed" lists what Piper attempted, and the refused close never became an attempt.

**My read, yours to rule:** leave it out. The census is "what Piper did or tried for you"; a close refused at the time, with the person told in that same turn, is a reply, not an action, and a line for it would claim an attempt that did not happen. The alternative, a row for refusals too, would also list every "I couldn't find" on update and reopen, and the "I tried to close issue #N, but it didn't go through" wording would be untrue of a write that was never sent. If you want refusals visible somewhere, that is a different line and a different list.

Nothing further is owed from this seat on F1 unless you rule the other way.

Verified how: read `destructive_confirm.py`'s probe branch (returns on `not_found` before the write, no `log_consequential_action` on that path) and the comment handler's audit call; PA's transcript quotes. Layer: source and PA's served text. Not run: anything served.

-- Lead
