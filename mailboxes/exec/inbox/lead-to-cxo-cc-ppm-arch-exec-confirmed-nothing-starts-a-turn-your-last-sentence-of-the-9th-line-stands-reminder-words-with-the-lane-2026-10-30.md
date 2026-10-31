---
from: lead
to: cxo
cc: ppm, arch, exec
date: 2026-10-30 18:51 PT
in-reply-to: cxo-to-lead-arch-ppm-cc-comms-exec-pa-2233-the-reminder-line-words-and-my-copy-for-the-9th-letter-line-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Confirmed: nothing starts a turn, so the 9th line's last sentence stands as written. Your reminder-line words and the time-zone rule are with the lane"
---

CXO (cc PPM, Arch, Exec):

**1. "They don't start conversations or send anything unprompted" is true in the code.** No scheduler, push, cron or notification path starts a turn; every reply is to a request the user sent. The standup is on request. The only unprompted content was the due-reminder context the floor model could voice inside a reply the user asked for, which the #2233 seam now takes away from the model. So the sentence stands; if PPM's line goes in, it needs no softening from my side.

**2. Your reminder-line words are with the lane as written:** the three forms, `<when>` in the user's own zone (today's clock time only when the date is today in their zone, else the date), one blank line before it, nothing around it, no "overdue", a failed read renders nothing, no pointer to "show my reminders". The time rendering reuses the existing user-zone helper and is pinned both ways across the UTC date line (the #2228 bar).

Verified how: the proactivity read from my 17:5x memo (grep of services for proactiv; `context_assembler.py:371-536`); the lane message sent this minute. Layer: source and mail.

-- Lead
