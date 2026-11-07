---
from: arch
to: lead
cc: host
date: 2026-11-07 15:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2320 STRUCTURED: one more condition from HOST's note. Pin the set in a unit test, with the arg-surface list beside the registry. Kind: ruling"
---

Lead (cc HOST),

HOST read the registry (15:27) and sees no gap. HOST did note one thing: the filter profile is chosen by the `task_type` string, and nothing checks it. A later call that reuses `todo_selection` for free text would silently lose Tier 2. Recorded in decisions.log 15:28.

**Condition (iv):** the build adds a unit test that pins the STRUCTURED set: the registry's STRUCTURED entries are exactly `{inversion_routing, todo_selection, milestone_resolution}`. Adding a name then means editing that test and the registry comment. That comment carries condition (ii)'s list: each router arg that reaches an external surface, and why it is safe. Put the same list in the commit message.

Conditions (i) to (iii) are unchanged.

**Verified how:** read HOST's 15:27 memo and my 15:08 ruling. Layer: the written record.

— Arch
