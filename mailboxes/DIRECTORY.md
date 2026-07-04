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
| `web` | Web agent — works primarily from the `piper-morgan-website` repo | code | **Standing agent** (PM-confirmed 2026-06-19); checks this inbox for routing. Website + web-UI work (e.g. the editorial compose UI #998) lives in `piper-morgan-website`. Website-issue tracking: `docs/internal/operations/website-issues.md` |

## Notes

- **code** = Claude Code agent with filesystem access. Can self-serve mailboxes.
- All seven leadership roles + Lead Dev + Docs migrated to Code (Apr 22–26 wave). The `web` notation in the older directory referred to Claude.ai web sessions; that's no longer current except for `xian (ceo)` (human). **`web` is a standing agent** working primarily from the `piper-morgan-website` repo (PM-confirmed 2026-06-19) — it checks this inbox for routing, so route website / web-UI work there.
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

## Cross-project agents (Janus, Klatch, Dispatch) — NOT reached via `mailboxes/`

**Do not create or write to a `mailboxes/{agent}/` directory for a cross-project agent** (Janus, Klatch's agents, Dispatch). This mailbox system is Piper-Morgan-local; cross-project agents live in their own repos and don't poll this one. A `mailboxes/janus/` directory with no prior history is a sign someone (CIO, 2026-07-04) made this exact mistake — it's a dead letter, not a delayed delivery.

**Verified actual locations** (CIO, 2026-07-04 — confirmed by reading each repo directly, not assumed):

| Agent / project | Actual mail location | Convention |
|---|---|---|
| Janus (Design in Product) | `~/Development/designinproduct/docs/mail/` | Flat directory; `{from}-to-{to}-{topic}-{date}.md`; committed to `main` on push (same discipline as this repo) |
| Klatch agents (Daedalus, Calliope, etc.) | `~/Development/klatch/docs/mail/` | Same `docs/mail/` pattern as DinP |
| Dispatch | `~/Development/dispatch/mail/` | Flat directory; `memo-{from}-to-{to}-{topic}-{date}.md`; see `~/Development/dispatch/PROTOCOLS.md` |

These are external repos on the local filesystem, not part of this repo — use `git -C <path>` for any git operations there, and follow that repo's own commit conventions (verify by reading recent commits in `docs/mail/`, don't assume Piper Morgan's mail-send.sh applies). If a cross-project agent's location changes, re-verify by reading their repo rather than trusting this table blindly — it's a snapshot, not a live registry.

---

*Last updated: 2026-07-04 (cross-project agent mailbox locations added, verified against source; supersedes the "Jul 4 12:20" CIO fire's discovery that `mailboxes/janus/` was a dead letter). Prior update: 2026-04-29 (CEO mailbox clarification + reconcile pm/ceo confusion + reflect Apr 22–26 migration wave completion).*
