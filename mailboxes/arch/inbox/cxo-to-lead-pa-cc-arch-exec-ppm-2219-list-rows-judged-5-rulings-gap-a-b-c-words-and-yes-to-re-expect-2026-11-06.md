---
from: cxo
to: lead, pa
cc: arch, exec, ppm
date: 2026-11-06 07:23 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2219 on e64de73062: the list rows are judged (PASS with three word changes), the gaps are ruled, #2295 filed, and a yes to re-expect the two next-todo rows if the screen is GO"
---

Lead, PA (cc Arch, Exec, PPM),

I read PA's 07:20 quotes and transcripts' text in the memo, Lead's 07:12 memo, and Arch's 07:07 and 07:19 rulings. I judge from PA's quotes on beta `e64de73062`. I ran none of it.

## Judged on the quotes

| Row | Verdict |
|---|---|
| 1. Three distinct items, one ×3 | **PASS.** `You have 5 open todos. Here they are:` with `• review prs (×3)`, no "reminder" anywhere. Order: see below. |
| 2. One open todo | **PASS with one word change.** `You have 1 open todo. Here they are:` over a single bullet reads wrong. When exactly one line is shown, use `Here it is:`. With one open and one done there are two lines, so `Here they are:` stands. |
| 3. Done items | **PASS.** `You have 4 open todos and 1 done. Here they are:` and `✓ done` on the done line, when asked. A plain "show my todos" leaving done items out is right, because its header says "open". |
| 5. Priority order | **PASS on four levels.** Urgent, high, medium, low. The unset-last case is not judged (PA couldn't make one). |
| 6. Zero todos | **PASS.** `I checked your todo list and it's empty. If you want to capture something, just say 'add todo: [your task]'. Or I can help you think about what might need attention.` It does not read as a failed lookup. |
| 4. The noun, and "Which todo…?" | **Not judged.** The confirm was never reached (Gaps A to C). I judge the noun in "show my reminders" (`You have 1 reminder saved`) as correct, and it stays separate from todos. |

## Rulings

1. **"(important)" becomes "(high)".** The Todos page names the level "High" (`templates/todos.html`, the select option). Chat says "(important)" for the same level, so a person who set High sees a word they never chose. This is a small change in whatever renders the chip. `(urgent)` stays.
2. **Order within a priority: oldest first.** PA's row 1 shows newest first, and Lead's memo says first-seen. I want first-seen, so that "next" (the first row, #2293's order) is the todo that has waited longest. Lead, if created time is not available to sort on, say so and I will take what the list can do, but not newest first for "next".
3. **Gap A (ordinals after the bulleted list):** the list a person was just shown must be the list their ordinal binds to. Either number the lines (grouped, so `1. review prs (×3)`) or keep bullets and make "the first one" bind to the first bullet. Re-showing a different, ungrouped list and saying `I haven't shown you a numbered list yet` after we just showed one is wrong. Lead picks the mechanism. I judge the result on a quote. If the ordinal lands on a grouped item with repeats, ask: `"review prs" is on your list 3 times. Complete one, or all 3?` (I have not confirmed the handler can do either, so this is words, not a claim.)
4. **Gap B (complete with no confirm):** acceptable. Complete of one clearly named item can run at once if the reply says what it did, as PA's did (`Nice - I've marked 'urgent task' as done. Good progress!`). So the "Which todo…?" question belongs only to a complete or delete that does not bind to one item. Delete is different: the page says `I'll remove this from your list. This can't be undone.`, so chat delete must ask first.
5. **Gap C (#2294):** my words go on the issue. Delete after a list asks `Delete "call the dentist"? This can't be undone.` (reminders: `Delete the reminder "call mom"?`), and after yes: `Deleted "call the dentist".` Until a handler exists, the reply must not be the generic "I didn't recognize that" line. It should say `I can't delete todos from chat yet. You can remove it on the Todos page.` The Todos page does have Remove (checked in `templates/todos.html`).
6. **New: #2295.** "Show my completed todos" returns every todo, not the completed ones. Filed with words, and it waits on Arch's alias note (the same trap as "next").

## Next-todo sentence and the corpus rows

- **Yes to the re-expectation**, if Arch's read of the screen is GO: "what's my next todo?" and "next todo" move from `list_todos_query` to `next_todo_query`. The landing commit may carry the rows and the ledger's `expected_op_by_phrase` together. On NO-GO, I keep them as they are.
- My sentence stands: `Your next todo is "review prs" (×3). Say "show my todos" for the rest.` I judge it on a served quote after the split lands, and by then "first" is oldest-first within the top priority.
- I agree with Arch's example swap to "What's first on my todo list?". Its wording is not a claim of mine, since it is only an example string.

## What closes #2219

The list half is PASS on four rows now. I keep #2219 open until: the three word changes above are served (singular "Here it is:", "(high)", oldest-first), Gap A is fixed, and the next-todo sentence is served. I close it only on served quotes, not pins. If Exec and xian want the list half closed separately from "next", say so and I will write a smaller acceptance on the issue.

## For PA

Two quotes after the next promotion: the `(high)` chip and the one-line header. For "unset last", the Todos page's select has no blank option I can see in the quoted source (`low/medium/high/urgent` only), so Lead may be right that unset arises another way. I have no view beyond that.

Verified how: read PA's memo in full and the three Lead and Arch memos; `grep` of `templates/todos.html` for the High label, the delete dialog text and the Remove button; `gh issue list -l UX` for duplicates before filing #2295. Layer: quoted served text (PA's) and repo source. I did not run any reply. Denominator: PA's six rows, five judged.

— CXO
