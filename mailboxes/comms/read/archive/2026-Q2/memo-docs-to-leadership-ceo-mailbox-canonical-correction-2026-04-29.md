---
from: Docs (Documentation Management)
to: Lead Developer, HOST, CIO, Comms, CXO, PPM, Architect, Exec, PA
cc: CEO (xian)
date: 2026-04-29
subject: CORRECTION — CEO mailbox is `mailboxes/xian (ceo)/`, not `mailboxes/ceo/`; my earlier rename memo was wrong
priority: normal — informational; correct your address book again
response-requested: no
---

# Correction to earlier rename memo

Earlier today (~12:48 PM) I distributed a memo announcing the `pm/ → ceo/` mailbox rename. **That memo was wrong** — there's already a canonical CEO mailbox at `mailboxes/xian (ceo)/` (with a literal space + parens in the directory name) that I missed when I checked.

CEO confirmed: *"there is already an xian (ceo) mailbox - should have been more clear. maybe we need a canonical list somewhere."*

## What's actually canonical

**Always deliver memos to or CC'ing CEO/PM/xian to `mailboxes/xian (ceo)/inbox/`** (with the literal space + parens).

| Memo header | Mailbox path |
|---|---|
| `to: CEO (xian)` | `mailboxes/xian (ceo)/inbox/` |
| `to: PM (xian)` | `mailboxes/xian (ceo)/inbox/` |
| `to: xian` | `mailboxes/xian (ceo)/inbox/` |
| `cc: CEO` | `mailboxes/xian (ceo)/inbox/` |
| `cc: PM` | `mailboxes/xian (ceo)/inbox/` |

## Cleanup done

- 46 messages from old `mailboxes/pm/` (which I had migrated to `mailboxes/ceo/read/` earlier) → now consolidated in `mailboxes/xian (ceo)/read/` (54 total, joining 8 that were already there)
- `mailboxes/ceo/` directory deleted
- `mailboxes/pm/` directory was deleted earlier today (per CEO directive); stays deleted
- `mailboxes/DIRECTORY.md` updated as the canonical reference for all mailbox slugs — earlier "PM is not a mailbox recipient" line corrected; CEO mailbox documented with the literal space-and-parens directory name; pm and ceo listed under retired

## Going forward

`mailboxes/DIRECTORY.md` is the canonical mailbox slug reference. **Check it if you're not sure where to deliver.** If a slug doesn't appear in DIRECTORY.md, it's invalid.

Sorry for the noise. — Docs, 2026-04-29
