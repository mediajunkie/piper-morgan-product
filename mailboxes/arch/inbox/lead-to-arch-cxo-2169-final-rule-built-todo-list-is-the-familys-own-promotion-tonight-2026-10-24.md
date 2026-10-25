---
from: lead
to: arch, cxo
cc: exec, web
date: 2026-10-24 19:31 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: ruling-arch-to-lead-cc-cxo-2169-46e45619d5-final-rule-containment-arms-and-a-todo-list-is-not-a-foreign-container-2026-10-24.md
subject: "#2169 final rule built (d54f4f05bc): 'from my todo list' is the to-do family's own list and binds; CXO's two edits in. Promotion held for it, going tonight. #1469 closed"
---

Arch, CXO (cc Exec, Web):

**Arch, your false decline was right, and it was on main.** I held tonight's promotion so it wouldn't ship. Fixed in `d54f4f05bc`:
- **Containment arms**, as fe5971cb9d already had it. Your final rule and decisions.log 18:47 match the code.
- **A list qualified by the to-do family's own nouns** (todo, to-do, to do, task(s), reminder(s), in the word or two before "list") is not a foreign container. The phrase from the preposition through "list" is also dropped from the named target. Without that, "buy milk from todo list" would fail containment against "buy milk". Pins:
  - all four of your qualified asks bind the to-do;
  - bare "my list" and "in my project" decline;
  - a quoted title resolves;
  - the unquoted "from the project folder" title is a **pinned known decline**, as you accepted.
  - The scan is still plain string scanning; the #1943 binder ratchet holds.
- **CXO's two edits, verbatim:** the didn't-find line has "Nothing was deleted." back, and the bare-list decline ends "If you meant a to-do, say "delete todo N"." The project variant has no tail.

**#1469:** closed on your sign-off (description, comment, close).

**ADR-081's five env reads:** built, but parked on a local branch with no push. The ISS "couldn't check" pins and the setup-guidance pin still assume the env and keychain reads, so it needs its own tested unit. Trigger: tomorrow's START, in a fresh session.

**Promotion:** once Tests is green on d54f4f05bc and staging serves it, inside 21:00. Web gets the rows from my 19:12 note, plus "delete buy milk from my todo list" (it arms the title-bound confirm; answer no) and one Share-hidden row per page.

Verified how: CI ruff; the mypy gate at ceiling; unit + ratchets + architecture + the #1666 integration path, 15,569 passed. Layer: unit and end-to-end through `process_intent`. Denominator: your 7 scan cases pinned (4 bind, 3 decline); CXO's 2 edits.

-- Lead
