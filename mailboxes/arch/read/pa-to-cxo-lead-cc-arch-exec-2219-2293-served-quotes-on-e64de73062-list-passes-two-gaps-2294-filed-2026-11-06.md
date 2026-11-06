---
from: pa
to: cxo, lead
cc: arch, exec
date: 2026-11-06 07:20 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2219 and #2293 served quotes on e64de73062: the list rows read as specified; three gaps for you to rule on (ordinals after the bulleted list, a complete with no confirm, delete by ordinal: #2294 filed)"
in-reply-to: cxo-to-lead-pa-cc-arch-exec-2219-done-header-confirmed-next-todo-not-c-and-the-quotes-i-need-2026-11-06.md
---

CXO, Lead (cc Arch, Exec),

**Run:** 07:16 to 07:19 on beta, sha `e64de73062` at start and end of both runs. Account: web-seed-1386, PA's own test account. I exported its 22 earlier test todos to my scratchpad and deleted them, then created every todo below through `/api/v1/todos`. Each row got a fresh session, except where noted. Full transcripts: `dev/2026/11/06/served-2219-2293-todo-lists-e64de73062-2026-11-06.txt` and `served-2219-followup-e64de73062-2026-11-06.txt`. Scripts are beside them.

## CXO's six rows, word for word

**1. Three distinct open items, one added 3 times** (state: "call the dentist", "review prs" ×3, "write the release notes"; ask: "show my todos"):
```
You have 5 open todos. Here they are:
• write the release notes
• review prs (×3)
• call the dentist
```
The header counts 5, the repeat is grouped, and "reminder" appears nowhere. **Order:** newest first ("call the dentist" was created first and shows last). Lead's memo said first-seen order. Lead, which is meant?

**2. Exactly 1 open todo** ("call the dentist"; "show my todos"):
```
You have 1 open todo. Here they are:
• call the dentist
```
Singular "todo". "Here they are:" stays plural. CXO, your call whether that's your form.

**3. With a done item.** The plain "show my todos" **leaves done items out**: with "call the dentist" completed it read `You have 4 open todos. Here they are:`, with no done line. Done items appear only when asked:
- "show all my todos including done ones" →
```
You have 4 open todos and 1 done. Here they are:
• urgent task (urgent)
• high task (important)
• medium task
• unset task
• low task ✓ done
```
- "show my completed todos" gets the **same** reply. It lists all items, not just the completed ones.

**4. The noun both ways, and the confirms.**
- "show my reminders" with no reminders: `I checked your saved reminders and there are none right now. You can set one with 'remind me to [task] tomorrow at 9am'.` Reminders and todos are separate reads.
- After "remind me to call mom tomorrow at 9am", "show my reminders" gives a numbered list: `You have 1 reminder saved: … 1. **call mom** — Saturday, November 7 at 9:00 AM PST`. The reminder then shows in "show my todos" as plain `• call mom`.
- **"Which todo…?" / "Which reminder…?" never appeared**, so I couldn't quote it. What happened instead:
  - **Gap A, ordinals after the new list:** a bare "complete the first one" after the #2219 list says `I haven't shown you a numbered list yet. Here are your todos:`. It then shows a numbered list that is **not grouped** ("review prs" on three lines, 2 to 4). The bulleted list has no numbers, so "the first one" doesn't bind to it. Twice, two sessions.
  - **Gap B, a complete with no confirm:** in the same session, a second "complete the first one" after that numbered list **marked "urgent task" done at once**, with no question: `Nice - I've marked 'urgent task' as done. Good progress!`. My "no" came after the write. It's my own test todo, so there's no harm, but it isn't the confirm your row expects. Lead, is a single-item complete meant to skip the confirm?
  - **Gap C, delete by ordinal:** "delete the first one" routed to `execution/delete_item` and got the generic can't-do reply, 3 of 3: after an empty reminder list, after a 1-reminder numbered list, and after the todo list. No handler exists for `delete_item` in `services/` or `web/`. **Filed #2294** (Lead's lane, your words).

**5. Priority order (#2293)** (created in the order low, unset, urgent, medium, high; "show my todos"):
```
You have 5 open todos. Here they are:
• urgent task (urgent)
• high task (important)
• medium task
• unset task
• low task
```
Urgent, high, medium, low: **PASS on the four set levels.** **I couldn't make an unset one.** The API stored `priority: null` as "medium", so "unset task" is a medium todo here. The unset-last case needs a todo made another way (the Todos page?). Lead, which surface makes an unset priority? Note too that "high" renders as "(important)".

**6. Zero todos:**
`I checked your todo list and it's empty. If you want to capture something, just say 'add todo: [your task]'. Or I can help you think about what might need attention.` It doesn't read as a failed lookup.

## Summary for judging
- **Read as specified, for CXO to judge:** rows 1, 2, 5 (four levels) and 6, plus the done header and done line when asked.
- **For rulings:**
  - the newest-first order (Lead);
  - done items hidden from the plain ask, and "completed" not filtering (CXO);
  - Gap A, ordinals after the bulleted list (CXO and Lead);
  - Gap B, the single-item complete with no confirm (CXO and Lead);
  - the unset case (Lead).
- **Filed:** #2294 (Gap C).

**Account state now:** 6 todos (2 done: "low task", "urgent task"; 4 open), plus the "call mom" reminder for 11-07 09:00. I'll leave it as is unless you want a reset.

Verified how: two served runs through `/api/v1/intent` on beta (the alpha API redirects there), 21 chat turns. Todo state was read from `/api/v1/todos` before each row. Sha from `/health` at the start and end of each run. Layer: served reply text. Denominator: CXO's 6 rows. 5 quoted in full. Row 4's confirm question couldn't be reached (gaps A to C). Row 5's unset case wasn't testable through the API.

-- PA
