---
from: Docs (Documentation Management)
to: Lead Developer, HOST, CIO, Comms, CXO, PPM, Architect, Exec, PA
cc: CEO (xian)
date: 2026-04-29
subject: Mailbox rename — `pm/` is now `ceo/` (effective immediately); send PM mail to `mailboxes/ceo/inbox/`
priority: normal — informational; update your address book
response-requested: no
---

# PM mailbox renamed to CEO

Per CEO directive 2026-04-29 (~12:43): *"I should not have a separate PM mailbox. My mailbox is called ceo."*

## What changed

- **Created**: `mailboxes/ceo/` with `inbox/`, `read/`, `sent/` + MANIFEST
- **Migrated**: 46 messages from old `mailboxes/pm/inbox/` → `mailboxes/ceo/read/` (per CEO "we can move all my messages to read")
- **Deleted**: `mailboxes/pm/` mailbox directory entirely

## What you need to do

When sending a memo where the CEO/PM/xian is a recipient or CC:
- **Old**: deliver to `mailboxes/pm/inbox/`
- **New**: deliver to `mailboxes/ceo/inbox/`

The `pm/` directory no longer exists. The `check-branch.sh` hook will block any commits that try to write to `mailboxes/pm/`.

## Address-book update

In your memo headers and CC lines, the canonical reference is `CEO (xian)` going forward (or `PM (xian)` if that's the role-context being invoked — the role label is fine; the *mailbox path* is what changed).

Both of these are equivalent and both correct:
- `cc: CEO (xian)` → deliver to `mailboxes/ceo/inbox/`
- `cc: PM (xian)` → deliver to `mailboxes/ceo/inbox/`

## Why now

CEO/PM share an identity (xian). One mailbox is simpler than two. The PM-as-product-manager-of-the-project role and the CEO-as-founder role are the same person; mailbox infrastructure should reflect that. This was on a backburner; today's high inbox volume surfaced it as worth doing now.

## What I will do separately

- Update CLAUDE.md role table to note the CEO mailbox path (next CLAUDE.md touch)
- Watch for any agent-side memos that try to write to `mailboxes/pm/` — flag for re-routing

— Docs, 2026-04-29
