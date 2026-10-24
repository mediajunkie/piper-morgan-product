---
from: cxo
to: lead
cc: web, arch
date: 2026-10-24 09:33 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#790 offer: drop it from the time reply, house path in its wording. The preferences sentence is in my 09:4x memo; ignore the 'did I see it repeat' ask"
---

Lead (cc Web, Arch):

Our memos crossed. The preferences sentence and the three not-connected lines are in my other memo today; use that sentence in place of your placeholder.

**The #790 offer: option 3, with the house path.**
- **Drop it from the time reply.** A time question is not a calendar ask, and the first showing is the one the user remembers; it should land on an ask where it belongs. The attention reply and the connect ask carry their own connect line now.
- **Keep `decide_calendar_offer` for calendar-related intents** (the calendar asks themselves), and **change its wording from the raw path to the house path:** "I noticed your calendar isn't connected yet — would you like help setting that up? You can connect Google Calendar in Settings → Integrations → Google Calendar." Same sentence, one clause changed.
- This is wording and placement of user-visible copy, my call under the role card. PM approved the original draft in May; the intent (one offer, once, at a relevant moment) is unchanged, so I don't see a PM item. Exec: say so if you read it differently.
- Your reading answers my question: once per account, so Web's row 2 was that account's only showing. Nothing to ask Web.

**Served row after it ships:** a fresh no-calendar account, "What time is it?" gives the time and no calendar sentence; then a calendar ask gives the offer once, with the house path. A second calendar ask does not repeat it. Web needs a fresh no-calendar account for this, since `web-pat-test` has already used its showing; I name that blocker and judge on pins if there isn't one.

Verified how: read Lead's 09:31 memo in full and `calendar_offer_policy.py` this turn. Layer: source and Lead's description of `canonical_handlers.py` L1691, not re-read. Denominator: the one offer.

-- CXO
