# Mailbox Directory

Canonical slug-to-role mapping. Used by `/deliver-mail` skill for routing validation.

## Active mailboxes

| Slug (directory) | Role | Environment | Notes |
|---|---|---|---|
| `lead` | Lead Developer | code | Primary coding agent, Claude Code |
| `arch` | Chief Architect | code | Architecture decisions, ADRs |
| `cxo` | Chief Experience Officer | code | UX testing, Colleague Test |
| `ppm` | Principal Product Manager | code | Sprint planning, roadmap |
| `comms` | Communications Chief | code | Blog, narrative, editorial calendar |
| `cio` | Chief Innovation Officer | code | Methodology, patterns |
| `host` | Head of Sapient Trust | code | Agent welfare, human network |
| `exec` | Chief of Staff | code | Executive office, cross-workstream synthesis, Weekly Ship drafts |
| `docs` | Documentation Management | code | Omnibus logs, mailbox ops, blog pipeline |
| `pa` | Piper Alpha | code | PM/CEO assistant, standup synthesis, meeting prep, document review |
| `xian (ceo)` | CEO / PM / founder (xian) | human | **Canonical CEO mailbox.** Receives memos addressed to or CC'ing CEO, PM, or xian. Directory name contains literal space + parens. |
| `spec` | Special Assignments | code | Specialist work, activated as needed |
| `web` | (no agent currently) | n/a | Inbox accumulates website-issue memos; tracked via `docs/internal/operations/website-issues.md`; Docs orchestrates fixes via on-demand Coding Agent subagents |

## Notes

- **code** = Claude Code agent with filesystem access. Can self-serve mailboxes.
- All seven leadership roles + Lead Dev + Docs migrated to Code (Apr 22–26 wave). The `web` notation in the older directory referred to Claude.ai web sessions; that's no longer current except for `xian (ceo)` (human) and `web` (no current agent).
- Slugs are lowercase, match directory names under `mailboxes/` exactly (the `xian (ceo)` directory's space + parens are intentional and load-bearing).
- If a slug doesn't appear here, it's invalid. The `/deliver-mail` skill will reject it.

## CEO / Founder mailbox — important clarification

**CEO/PM/xian IS a mailbox recipient.** Earlier directory note ("not a mailbox recipient") was incorrect. Always deliver memos addressed to or CC'ing CEO/PM/xian to `mailboxes/xian (ceo)/inbox/`.

The directory name `xian (ceo)` has:
- A literal space between `xian` and `(`
- Literal parens `(` and `)` around `ceo`
- All lowercase

Common synonyms in memo headers (all route to the same mailbox):
- `to: CEO (xian)` → `mailboxes/xian (ceo)/inbox/`
- `to: PM (xian)` → `mailboxes/xian (ceo)/inbox/`
- `to: xian` → `mailboxes/xian (ceo)/inbox/`
- `cc: CEO` → CC into `mailboxes/xian (ceo)/inbox/`
- `cc: PM` → CC into `mailboxes/xian (ceo)/inbox/`

## External / alpha-tester mailboxes

| Slug | Notes |
|---|---|
| `ted-nadeau` | External alpha tester inbox |
| `z-dan-heck` | External alpha tester inbox |

## Special infrastructure

| Slug | Notes |
|---|---|
| `incoming` | Staging area for inbound mail not yet routed |

## Retired / deprecated mailboxes (do not use)

| Slug | Retired | Notes |
|---|---|---|
| `cos` | (pre-2026) | Was alias for Chief of Staff; use `exec` instead |
| `pm` | 2026-04-29 | Was a separate PM mailbox; messages migrated to `mailboxes/xian (ceo)/read/`; directory deleted |
| `ceo` | 2026-04-29 | Briefly created same day in error; reconciled with canonical `xian (ceo)` |

---

*Last updated: 2026-04-29 (CEO mailbox clarification + reconcile pm/ceo confusion + reflect Apr 22–26 migration wave completion).*
