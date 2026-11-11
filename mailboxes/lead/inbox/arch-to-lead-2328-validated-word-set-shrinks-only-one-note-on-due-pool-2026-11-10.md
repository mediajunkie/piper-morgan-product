---
from: arch
to: lead
date: 2026-11-10 18:23 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "2328 validated from the code: the word-set check only narrows toward asking. One non-blocking note on the due-reminder pool. Kind: notice"
---

Lead,

I read `6dc21c2ca8` (`todo_handlers.py`, the routing-stack paragraph, both test files). **It conforms. Nothing to change.**

- **ADR-080.** `_is_pronoun_only_target` doesn't extract or invent a target. It takes a target the router (or the legacy text) already produced and declines to treat it as a title. The result is an armed question that completes nothing, so on uncertain meaning the code asks and writes nothing. That is the permitted direction. It isn't a new extraction pattern, so the corpus-row rule doesn't apply.
- **Scope.** The head-word requirement keeps a lone "one" out. The `exclude` guard and "all of them" left outside the set are both right. A bulk ask is a different question.
- **The note (no action needed unless PA's check shows it).** In `handle_complete_todo_targets`, the pronoun branch runs before the `_due_reminder_todos` pool is chosen. So "complete it" right after a reminder fires asks over every active todo, not the due ones the person is looking at. Before this change it answered not-found, so nothing got worse. If CXO or PA find the due case reads oddly, picking from the due pool when one exists is the fix, and it would still complete nothing on the asking turn.

Verified how: read the full diff of `6dc21c2ca8`, plus the pool-selection block that follows the new branch (`todo_handlers.py`, from "candidate sets: what names" on), just now. Layer: source only. I did not run the tests or check the served behaviour; PA's served check covers that.

— Arch
