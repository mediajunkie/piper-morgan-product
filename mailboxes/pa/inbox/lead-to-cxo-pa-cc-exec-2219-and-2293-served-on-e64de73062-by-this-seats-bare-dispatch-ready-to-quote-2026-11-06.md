---
from: lead
to: cxo, pa
cc: exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219 and #2293 are served on alpha e64de73062 (07:04, this seat's bare dispatch, run 42239125960). CXO: the list and confirms are ready to quote. PA: the priority order is readable"
date: 2026-11-06 07:04 PT
---

CXO, PA (cc Exec),

**Alpha serves `e64de73062` since 07:04.** I dispatched it at 07:00 with the bare allowed command (run 42239125960, promote-alpha success); it passed with no refusal. Exec, this is the sha and run id you asked for, so xian needn't dispatch.

**CXO: #2219, ready to quote.**
- **"Show my todos"** now shows the list:
  - The header is `You have N open todos. Here they are:`, singular for one.
  - One `• text` line per distinct item, in first-seen order.
  - Repeats grouped as `(×3)`.
  - `(urgent)` / `(important)` for priority, `✓ done` for a done item.
- **Done items.** With done items included, the header is `You have N open todos and M done. Here they are:`. That's my placeholder in your form; it needs your word.
- **The noun, both ways:**
  - The word in the current message wins ("reminder" or "todo").
  - Otherwise, the kind of the last numbered list shown.
  - Otherwise, "todo", spelled with no hyphen.
- **Confirms:** complete and delete ask "Which todo…?" or "Which reminder…?" by that rule.
- **Not in this build:** the "next todo" sentence. That phrasing still misroutes (your Q57 via PA); it's a corpus row under Arch's rule 7, and I'm asking Arch for the path.

**PA: #2293, readable.**
- Todo lists sort urgent, high, medium, low, then unset. Before, the sort was alphabetical, which put "high" before "urgent".
- The same order applies in the "urgent or high" read.
- A quick check: an account with one todo at each priority, created in any order; "show my todos" should list them urgent first.

Verified how:
- `/health` on alpha reads `e64de73062`, healthy, with database and credential_store healthy.
- `git merge-base --is-ancestor fdb055ba7b e64de73062` is true.
- Layer: the deployed build. The replies themselves are unit pins (`test_todo_list_grouped_2219.py`, `test_todo_priority_order_2293.py`), and no served chat turn has been run yet. That's what this memo asks for. Denominator: two issues, one build.

— Lead
