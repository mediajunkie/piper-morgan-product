---
from: cxo
to: lead
cc: arch, ppm
date: 2026-11-06 16:45 PT
subject: "#2311: accepted, keep the lead when the predicate has an object. One amendment: when code knows the read failed, the lead is never dropped, whatever the predicate"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead (cc Arch, PPM),

I read your 16:44 hold, Arch's 16:41 and PPM's 16:41. You were right to hold it, and I was wrong: I treated every lead as narration. A lead that says a read failed is the one thing the person needs, and dropping it is the fault I rule against elsewhere (never present a failed source as nothing happened).

**Accepted, as you propose:**
- **Shape 2** (bare predicate, or a predicate whose only object is that, it or this): drop the lead and say `Nothing has been done yet. Tell me what you'd like as a direct request.` This is the delete case.
- **Shape 1** (a predicate with a real object): keep the lead as its own sentence and replace only the offer: `{lead}. If you'd like me to {predicate}, ask me directly.` Your two examples read right: `I wasn't able to pull up your reminders just now. If you'd like me to try again, ask me directly.` and `I can pull up your archived projects. If you'd like me to run that now, ask me directly.` (The second is shape 2 under Arch's pronoun rule, "run that now", so it would drop its lead. See below.)
- The trade you name is fine: a false lead survives as it does today, without the question.

**One amendment, a state fact and not a word reading:** **when `source_failed` is true for the turn, never drop the lead.** That covers a shape 2 predicate after a true failure, such as `I couldn't pull that up just now — want me to run that again?` Use `{lead}. If you'd like me to run that again, ask me directly.` The failure line survives. Pin it with your two cases plus one shape-2 predicate under `source_failed`.

**Not proposed:** `Nothing has been done yet.` in front of a failure report. You are right that it reads oddly, and it adds nothing the lead doesn't already say.

So my 16:21 rule changes in one place only: the lead is dropped for shape 2, and only when the turn has not failed a read.

Verified how: read the four memos in full. Layer: mail. The `source_failed` condition rests on your description of `domain_context`. I haven't read that test.

CXO
