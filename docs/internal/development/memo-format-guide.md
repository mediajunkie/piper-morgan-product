# Memo Format Guide

Standard format for inter-agent memos in the Piper Morgan project.

## Filename Convention

```
memo-YYYY-MM-DD-from-{sender}-to-{recipient}[-cc-{slug1}[-{slug2}...]].md
```

**Examples**:
- `memo-2026-03-19-from-lead-to-arch-cc-cxo-ppm.md`
- `memo-2026-03-19-from-docs-to-host.md`
- `memo-2026-03-19-from-arch-to-docs-cc-lead.md`

**Rules**:
- Use slugs from `mailboxes/DIRECTORY.md` (e.g., `lead`, `arch`, `cxo`, not `lead-dev`, `architect`)
- Date is the date the memo was written
- Multiple CC recipients are hyphen-separated after `cc-`
- The filename encodes routing for readers and MANIFESTs — you place each memo directly at its recipient's `inbox/` path and send it via `scripts/mail-send.sh` (push-to-ref; see CLAUDE.md "mailbox workflow"). There is no auto-parsing distribution step.

## Header Format

Every memo must begin with:

```markdown
# Memo: [Subject line]

**To**: [Role name(s)]
**CC**: [Role name(s), optional]
**From**: [Role name]
**Date**: YYYY-MM-DD
**Re**: [Brief subject — same as or shorter than the title]

---

[Body]
```

**Header rules**:
- **To/CC** use full role names (e.g., "Chief Architect"), not slugs
- **From** uses full role name
- Headers are the fallback if filename parsing fails
- If To/CC in headers contradicts the filename, headers win

## Body Guidelines

- Lead with the ask or the information. Don't bury the point.
- If referencing repo files, use full relative paths from project root (e.g., `docs/internal/architecture/adrs/adr-060-floor-first-routing.md`)
- If the memo requires a response, say so explicitly: "Please respond to [slug] inbox"
- Sign off with role name and date

## Where Memos Live

| Location | Purpose |
|----------|---------|
| `mailboxes/incoming/` | Drop zone for downloaded memos before routing |
| `mailboxes/[role]/inbox/` | Unread memos for this role |
| `mailboxes/[role]/read/` | Read/processed memos |
| `mailboxes/[role]/sent/` | Copies of memos this role sent |

## Legacy Memos

Memos created before this convention may not follow the naming format. They still have in-file To/CC headers and can be routed manually — read the headers, place the file at each recipient's `inbox/` path, and send via `scripts/mail-send.sh`.

---

*Established March 19, 2026*
