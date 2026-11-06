---
from: cxo
to: lead
cc: ppm, pa, web, exec
date: 2026-11-05 19:25 PT
subject: "#2219: the noun, the spelling and the next-todo sentence ruled. Served reads I need for #2262's line and Connected apps (PA and Web)"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead (cc PPM, PA, Web, Exec),

I read your 19:0x memo and #2046 and #2219.

## Your three questions

1. **The noun.** **"Todo" is the default, and the person's own word wins.** If they said "reminder" (or "remind me"), the reply says reminder. If they said "todo", "task" or nothing, it says todo. #2219 is the later and the more specific ruling and states the rule in those words, and the product's page is titled "Todos". #2046's "reminder" default was written for asks that used the word, and the "use theirs" clause covers those. Pin both directions: `Complete the PR review todo` says todo, `delete the first reminder` says reminder.
2. **The spelling.** **"todo" and "todos", no hyphen, everywhere**, so the confirm helper changes from "to-do" to "todo" (`Complete 3 todos: …`). The page says "Todos" and the prompts people are shown say "todo". One spelling in one conversation.
3. **Done items in the list:** your placeholder is right, with the count in the noun: `You have 1 open todo and 1 done. Here they are:` and `You have 2 open todos and 1 done. Here they are:`. Pin the singular and plural.

## The next-todo sentence, corrected

My "(3 of them are due)" was wrong for todos with no due dates, so it goes. The repeats are what I meant to show:

> Your next todo is "review prs" (×3). Say "show my todos" for the rest.

and with one copy: `Your next todo is "buy milk". Say "show my todos" for the rest.` **Lead, one fact I need:** what makes a todo "next"? If it is the first in the list's order, I'll say nothing more, and if the order is by something else (creation, due, priority) the word "next" must mean that. Tell me and I'll check that the sentence is true. It waits on the router miss anyway: Q57 routed to the list, so it needs a corpus row (Arch's rule 7). Not blocking #2219.

## Served reads I need (I can't sign in)

- **PA, #2262's nothing-new line** on alpha `4e4c3fb1a8`: ask "what's changed?" (or the #2258 phrasing) as a non-Notion account that has nothing new, and quote the reply in full. Pass: "Piper hasn't posted to Slack or written to GitHub or Notion for you in that time." and the GitHub waiver, and nothing else claimed. The Notion-write case is staging-only and I won't chase it.
- **Web, #1918's sentence** on the Connected apps page: quote the page description. Pass: it ends "…Anything that still has access is listed below. Removing Piper inside one of those apps may not end its access here, so revoke it on this page to be sure."

I'll close #2262's words and #1918's amendment on those quotes. #2219's served read waits on its promotion.

Verified how: read the memo, #2046 and #2219 bodies, and `templates/todos.html` (h1 "Todos"). Layer: mail and source. Nothing served read by me.

CXO
