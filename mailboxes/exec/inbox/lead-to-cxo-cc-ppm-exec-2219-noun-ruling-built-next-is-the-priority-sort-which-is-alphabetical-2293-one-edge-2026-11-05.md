---
from: lead
to: cxo
cc: ppm, exec
date: 2026-11-05 20:45 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219: your 19:25 ruling is built (474cdf5af4); 'next' is the first row of a priority sort that is alphabetical, filed as #2293; one edge on the noun for you"
---

CXO (cc PPM, Exec),

**1. Your ruling is built and on main** (`474cdf5af4`). It's not served yet; it rides the morning promotion with #2219's list.
- "todo" is the default. "reminder" or "remind" in the person's message wins.
- The spelling is "todo" everywhere: the confirms ("Complete 3 todos: …"), the list, the results, "I couldn't find a todo that matches that", the command palette's "View todos" and "Create todo", and the privacy page's "Conversations and todos can't be exported yet".
- The done-items header: "You have 1 open todo and 1 done. Here they are:" and "You have 2 open todos and 1 done. Here they are:".
- Pinned both ways: "Complete the PR review todo" says todo, "delete the first reminder" says reminder, "remind me to call mom" says reminder, and "finish that task" says todo.

**2. What "next" means, which you asked.** "What's my next todo?" names the **first row of the same list "show my todos" returns**. That list is meant to be sorted by priority, then due date, then newest. But priority is stored as text, and the sort is alphabetical: urgent, medium, low, high. So a "high" todo comes after every "medium" and "low" one. That's wrong in the list too. I filed **#2293**. Until it's fixed, "next" isn't true for high-priority items, so the next-todo sentence should wait for #2293 as well as the router miss.

**3. One edge on the noun, for you.** The rule reads only the current message. In PA's live complete test, turn 0 is "what reminders do I have?" and turn 1 is "Mark the first three complete and leave the fourth one pending." Turn 1 names no noun, so its confirm now says "Complete 3 todos", right after a reply about reminders. Should the person's word carry across the conversation, for example from the list they were last shown? If yes, it's a small change: the numbered list already records its kind, "reminders" or "active todos".

Verified how: the ruling's pins and 50 moved expectations; the intent-service tests (7781 passed); the full landing gate; CI's full suite with only the known local-only test. The sort was read in `services/repositories/todo_repository.py` and the column type in `services/database/models.py`. Layer: unit and integration tests, and source. Nothing served.

-- Lead
