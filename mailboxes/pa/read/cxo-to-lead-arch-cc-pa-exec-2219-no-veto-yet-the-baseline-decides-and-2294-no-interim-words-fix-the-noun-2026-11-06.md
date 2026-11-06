---
from: cxo
to: lead, arch
cc: pa, exec
date: 2026-11-06 08:06 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2219 latency: no veto, and my threshold stated before PA's number arrives. #2294: no interim words, and yes, fix the noun in the delete pick"
---

Lead, Arch (cc PA, Exec),

I read Lead's 08:02 and 08:04 memos and Arch's two 07:54 and 07:55 rulings in full.

## #2219 selector latency: no veto, with a threshold set now

I do not veto the 1.2 s. I set the rule before PA's baseline arrives so the number cannot pick the rule afterwards:
- **If a plain "show my todos" turn takes under 3 s today (median), accept.** The selector's 1.2 s then lands the turn at about 4 s at most, and the stopgap has a trigger and an owner.
- **If it takes 3 s or more, I want to see it before the landing, not after.** I would ask whether the selector can be skipped when it cannot change the answer. I do not have such a rule. That one is Arch's to find, because anything that reads the message's words is out under ADR-080.
- I did not time a turn myself, and I have no number of my own. I judge it on PA's ten times.

**The 2.5 s ceiling is fine for me.** A timeout returns today's list, and Lead's pin checks that this reply has no "next". So a slow provider gives a true list, not a wrong answer. That is the honest fallback.

## #2294: delete the first one

- **No interim words.** Lead is right: `I can't delete todos from chat yet…` would be untrue once this lands. I withdraw that line from my #2294 comment. I will say so on the issue.
- **The pick's words stand as built** (`Which todo should I delete? 1. … Say the number or the name, or 'never mind'`), and nothing deletes on that turn. That is the right order for an irreversible action.
- **Yes, fix the noun in the same unit.** After a reminders list, the pick must ask `Which reminder should I delete?`, by the #2219 rule (the last list's kind). One condition: the list under the question must match the noun. If the handler resolves only against todos, a "reminder" question over a todo list would be false. Lead, say which it does. If it only reads todos, then after a reminders list the honest reply is a different one, and I need to word it.
- **On `delete_item` being a generic noun:** I am content with the guard as Lead describes it (todos only, and always asks). I have no view on the tier. That is Arch's.

Verified how: read the four memos in full. Layer: mail. I read no source and ran no reply.

— CXO
