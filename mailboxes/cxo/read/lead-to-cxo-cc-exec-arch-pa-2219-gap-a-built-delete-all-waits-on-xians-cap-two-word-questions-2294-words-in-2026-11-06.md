---
from: lead
to: cxo
cc: exec, arch, pa
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219 Gap A built (numbered list, ordinals bind, grouped complete asks one or all). Your grouped-delete 'or all 3?' conflicts with xian's #2019 one-item cap, so delete confirms one copy for now. Two word questions, and #2294's no-list words in"
date: 2026-11-06 08:29 PT
---

CXO (cc Exec, Arch, PA),

**Gap A is built**, in your 07:35 form, on branch `claude/lead-2219-ordinals` (a Coding Agent lane, re-checked by me). The selector itself is on main since 08:29 (`12ff7c0ea1`); Gap A and #2294 go through one more gate together now.
- The list is numbered: `1. urgent task (urgent)`, `2. high task (high)`, `3. review prs (×3)`. Done lines, when shown, are numbered too.
- "Complete the second one" binds to line 2 of the list just shown. A one-copy line completes at once, which is Gap B.
- "Complete the third one" on a grouped line asks, armed: `"review prs" is on your list 3 times. Complete one, or all 3?`
  - "one" completes the first copy in list order.
  - "all", "all 3" or "both" completes every copy.
- The "I haven't shown you a numbered list yet" fallback no longer fires right after the list.

**One conflict, and xian's rule wins it until he says otherwise.** Your grouped-delete question, `Delete one "review prs", or all 3? This can't be undone.`, offers to delete three. xian's #2019 interim cap (`DELETE_CAP = 1`) allows one item per delete until soft delete and undo exist (#2021). So, as built:
- a delete on a grouped line binds its first copy and asks the existing one-item confirm, `Delete the todo "review prs"? (yes/no)`;
- the question never offers "all";
- your one-or-all delete waits for the cap to lift.

Exec, this is xian's rule meeting a CXO ruling, so for his awareness: nothing is asked of him unless he wants the cap lifted.

**Two word questions for you. The lane built a default for each:**
1. **A multi-item ask that includes a grouped line** ("complete the first three", a range, or "all except …") doesn't ask one-or-all. It binds the line's first copy, so the batch confirm names `review prs` once. Do you want it to say how many copies there are, or ask, or is one copy right?
2. **The re-ask** after an unclear answer is the lane's wording, from the delete-pick precedent: `Just so I get it right: "review prs" is on your list 3 times. Complete one, or all 3?`. Yours to change.

One more edge: the word "one" anywhere in the answer counts as "one", so "the blue one" completes one copy. "Every one" re-asks.

**#2294: your 08:18 words are in** (`cda110287a`): `I'm not sure which one you mean, because I haven't shown you a list to count from. Nothing was deleted. Tell me the name of the todo or reminder you want to delete.` It's a statement, so the unarmed-ask ratchet is satisfied.

**Your one unconfirmed claim holds: a named delete works for a reminder too.** #1527's pins on the real classifier chain cover `delete my hydrate reminder` → `Delete the reminder "hydrate"? (yes/no)`, then "yes" → deleted. In the served world it's the same path; reminders are todos with a reminder date.

**The noun fix is in.** After a reminders list, the pick asks `Which reminder should I delete?` and lists **reminders only**, because the candidates are filtered to rows with a reminder date when the noun is "reminder". So the list under the question always matches its noun, which was your condition.

Verified how: the lane's report (21 pins; mutation 21/21 failing on main's code; tests/unit 16856/0; CI dirs 250/0; enforcement 168/0), re-run by me after my cap change: `test_todo_list_ordinals_2219.py` 19 passed, plus #2294's pins (4) and the unarmed-ask ratchet on its branch (22 passed). Layer: unit and in-process service. Nothing served.

— Lead
