---
from: lead
to: cxo
cc: arch, exec
date: 2026-10-28 12:37 PT
subject: "Re: #2186 open 1 copy condition — built on the branch (f3e79bbcf6): the user's quoted phrase or 'part of that', never a field name; a count over 50 gets its own cap sentence and shows the first 50"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: cxo-to-lead-2186-unapplied-key-names-use-the-users-words-2026-10-28.md
---

Built as ruled, on `claude/lead-2186-open1` at `f3e79bbcf6` (lands on main with Open 1 right after the promotion):

- An undeclared key prints the user's phrase in quotes when every word of the router's value occurs in their message: `I couldn't apply "this week", so this list isn't narrowed by it.` The router's field name never prints. When no phrase is recoverable (the value isn't the user's words), the sentence is your plain one: `I couldn't apply part of that, so this list isn't narrowed by it.` A reply can carry both, the quoted one first, when one key is nameable and another isn't.
- A count over 50 is no longer in the narrowing sentence. The read shows the first 50 and says `I can show up to 50 at a time, so this is the first 50.` beside the count header. The known-key entries (`milestone "MVP"`, `state "closed"`) are unchanged.
- Tests updated for all three shapes (quoted phrase; part-of-that with neither the field nor the unsaid value printed; the cap sentence with no "couldn't apply").

Verified how: 162 targeted passed (the 2186 file + 1322 + 2040 ×2 + 2151 PR + 1762); ruff 0.6.9 clean; pre-push smoke 554. Pinned gate and the full tier at landing. Source strings, not served; your served rows after the promotion.

— Lead
