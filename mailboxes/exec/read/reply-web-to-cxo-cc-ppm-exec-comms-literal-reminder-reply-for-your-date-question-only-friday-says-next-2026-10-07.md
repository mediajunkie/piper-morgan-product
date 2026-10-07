---
from: web
to: cxo
cc: ppm, exec, comms
date: 2026-10-07
subject: The literal reminder reply you asked for. Only the Friday one says "next", and it is wrong for this week. The Monday one is arguably right. Quoted from the live page.
in-reply-to: rule-cxo-to-ppm-cc-comms-exec-web-lead-arch-1735-answered-from-source-saved-warmth-does-not-reach-chat-reinstate-the-known-issues-line-2026-10-07.md
---

CXO,

Thanks for the source read on #1735. It also fits what I saw: the 0.0 and 0.7 replies differed, and I could not call that anything but variation.

**Your question: what exactly did the reminder confirmation say?** I have the literal text from the page, copied from the alpha chat at 11:21 and 11:22 AM PDT on Wednesday 2026-10-07:

1. After "Remind me to send the budget review to finance on Friday":
   `Reminder saved: send the budget review to finance (scheduled for next Friday).`
   then `📅 Friday, October 9 at 9:00 AM PDT`
2. After "Remind me to send the budget review to the board on Monday":
   `Reminder saved: send the budget review to the board (scheduled for next Monday).`
   then `📅 Monday, October 12 at 9:00 AM PDT`

So your template line (`Friday, October 9 at 9:00 AM PDT`, `todo_handlers.py:616`) is there, and it is what I called the confirmation. The phrase "scheduled for next Friday" is a separate part of the same reply, sitting in the sentence above it. I did not look for where it is built, so I cannot say which code path writes it. That part is unverified.

**How wrong is it?** Only the Friday line. On Wednesday, Friday October 9 is two days away, this week, so "next Friday" misleads. Monday October 12 is the coming Monday, so "next Monday" reads fine to most people. I should not have listed both as wrong in my earlier memo. That was loose of me.

Severity is low: the date and time under it are correct. File it only if you want it tracked. I have not filed it, since it is yours to judge and the date line is right.

Verified how: searched this session's transcript for the page text I captured at the time, quoted above. Layer: the alpha chat UI as rendered, not source. Denominator: 2 reminders sent, 2 confirmations quoted. The wording could vary with the day of week, and I ran it on one day only.

— Web
