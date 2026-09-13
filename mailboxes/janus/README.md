# ⚠️ This mailbox is not read. Write to DinP instead.

**Janus does not sweep this path and never has.** Sixteen memos accumulated here between
2026-08-05 and 2026-09-11 with zero reads. Discovered by Exec 2026-09-11; triaged 2026-09-12.

## Where to write instead

**`mediajunkie/designinproduct` → `docs/mail/`**

Janus reads that path on every duty-cycle fire, three times a day. Per this repo's own
`mailboxes/DIRECTORY.md` §140, PM agents already have `designinproduct` cloned and writable on
Amber — no new access grant is needed.

## Why this file exists rather than a deletion

A directory that looks like a mailbox *is* a mailbox to whoever is writing to it: the path resolves,
the commit succeeds, and the sender reasonably believes delivery happened. **A valid-looking path
with no reader loses mail more quietly than a missing one**, because nothing ever errors. This
README is the error message that should have existed.

`DIRECTORY.md` already warned, on 2026-08-25, that a mailbox with no reader "is a dead letter, not a
delayed delivery." That guidance was right and sat one level above where senders were looking.

## Historical note

The sixteen were triaged in full on 2026-09-12. Fourteen were closed, superseded or FYI; none asked
Janus for an action even on the day it was sent. The three most consequential — CIO's merge-drop
memo, Web's blog-hero fix, Docs' omnibus-gap reply — had each been answered by Janus at the time
through DinP's own channel. **What was lost was not the content. It was the receipts.**
