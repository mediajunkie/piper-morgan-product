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
| `xian (ceo)` | CEO / PM / founder (xian) | human | **RETIRING (PM ruling 2026-10-03). Do not write to it.** No cc copies, no memos addressed to PM. Address anything needing PM's attention to `exec`, PM's proxy, who vets it and surfaces it via the rollup. Directory is removed after a soak; history stays in git. |
| `spec` | Special Assignments | code | Specialist work, activated as needed |
| `web` | Web agent — works primarily from the `piper-morgan-website` repo | code | **Standing agent** (PM-confirmed 2026-06-19); checks this inbox for routing. Website + web-UI work (e.g. the editorial compose UI #998) lives in `piper-morgan-website`. Website-issue tracking: `docs/internal/operations/website-issues.md` |

## Notes

- **code** = Claude Code agent with filesystem access. Can self-serve mailboxes.
- All seven leadership roles + Lead Dev + Docs migrated to Code (Apr 22–26 wave). The `web` notation in the older directory referred to Claude.ai web sessions; that's no longer current except for `xian (ceo)` (human). **`web` is a standing agent** working primarily from the `piper-morgan-website` repo (PM-confirmed 2026-06-19) — it checks this inbox for routing, so route website / web-UI work there.
- Slugs are lowercase, match directory names under `mailboxes/` exactly (the `xian (ceo)` directory's space + parens are intentional and load-bearing).
- If a slug doesn't appear here, it's invalid. The `/deliver-mail` skill will reject it.

## CEO / Founder mailbox — important clarification

**CEO/PM/xian is NO LONGER a mailbox recipient (2026-10-03).** Route PM-bound mail to `exec`. See CLAUDE.md "Do NOT cc PM".

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

None. `ted-nadeau` and `z-dan-heck` (human correspondents, last touched 2026-06-13) were removed from
`mailboxes/` on 2026-10-08 and their correspondence archived read-only at
`docs/internal/operations/legacy-operations/legacy-mailboxes/`. Mail to a human outside the team goes
by email or conversation, not a repo path.

## Retired / deprecated mailboxes (do not use)

| Slug | Retired | Notes |
|---|---|---|
| `cos` | (pre-2026) | Was alias for Chief of Staff; use `exec` instead |
| `pm` | 2026-04-29 | Was a separate PM mailbox; messages migrated to `mailboxes/xian (ceo)/read/`; directory deleted |
| `ceo` | 2026-04-29 | Briefly created same day in error; reconciled with canonical `xian (ceo)` |
| `janus` | 2026-10-08 | Gravestoned 2026-09-12; directory removed 2026-10-08 at xian's instruction (history stays in git). Janus's inbox is `designinproduct/docs/mail/` |
| `dispatch-dinp` | 2026-10-08 | Gravestoned 2026-09-12; directory removed 2026-10-08. Dispatch-DinP's inbox is `dispatch/mail/` (its triage of the four stranded memos: moot, 2026-09-11) |
| `pard` | 2026-10-08 | Gravestoned 2026-09-12; empty directory removed 2026-10-08. Pard's inbox is `mediajunkie/docs/mail/`. `scripts/mail-send.sh` still hard-refuses any `mailboxes/pard/` path |
| `ted-nadeau`, `z-dan-heck` | 2026-10-08 | Human correspondents, archived (see above) |
| `incoming` | 2026-06-19 | Was a manual staging area for inbound mail not yet routed; eliminated by #1259's push-to-ref `mail-send.sh` migration, which removed the need for manual staging |

## 🔴 IF YOU ARE NOT CERTAIN WHERE MAIL GOES — READ THIS FIRST (PM directive, 2026-08-30)

**PM, relayed via Dispatch-PM:** agents should *"know how to route mail, or know to escalate via Exec
when uncertain, versus guessing."*

### The rule, in one line

> **Uncertain where it goes? Put the REAL recipient in `to:`, cc `exec`, deliver to
> `mailboxes/exec/inbox/`, and say in the memo that you weren't sure. Exec routes it.**
> That is not a fallback or an admission — **it is the correct destination for uncertain mail**, and
> it is always available.

**You are never required to guess.** Guessing is the one option this convention removes.

### Why this section exists — three failures in one week, none of them carelessness

Each agent did something reasonable and the mail still didn't arrive. That is what makes it a
convention problem rather than a discipline problem.

| # | What happened | Why no one was at fault |
|---|---|---|
| 1 | Comms wrote to Dispatch-PM. It landed in `comms/sent/`, `exec/read/`, and xian's inbox — **three real places, none of them anywhere Dispatch-PM looks.** Sat **5 days** until xian nudged. | **There is no `mailboxes/dispatch-pm/`.** There was no correct destination to choose. |
| 2 | Docs addressed a memo `To: Dispatch` — accurate, that is the role's name. | The recipient's inbox sweep greps for `dispatch-pm`. **Correctly addressed, invisible to the sweep.** |
| 3 | A Tessera memo sat undelivered across a host migration. | No signal to either end. **The sender believed they had sent it.** |

★ **All three share one shape: the sender believed they had sent it.** Writing is not delivering.

### Four rules that follow

1. **Address by MAILBOX NAME, never by role prose.** `to: dispatch-pm`, not `To: Dispatch`. Sweeps
   grep for the slug. A human-readable role name in `to:` is invisible to the machine that looks.
   **Aliases honored** (write the slug, not the alias, in `to:`): `dispatch` → `dispatch-pm` ·
   `ceo` / `pm` / `xian` → `xian (ceo)` · `chief of staff` / `cos` → `exec` · `lead dev` → `lead`.
   (The old `dinp` / `design in product` → `janus` alias was removed 2026-10-08: it routed into a
   dead box. Janus and Themis are reached at `designinproduct/docs/mail/`, see the table linked in
   "Mail to an agent outside this repo" below.)
2. **If a role has no mailbox here, this file must say where its mail goes instead.** A role that is
   addressable but absent from this directory is the gap that produced failure #1. **If you find one,
   add it or tell Exec** — an unlisted destination is a defect in this file, not a puzzle for you to
   solve.
3. **A write outside `mailboxes/` is not a send until you verify it landed.** `mail-send.sh` gives you
   a push receipt for in-repo mail. Sibling repos give you nothing. **Confirm the file is observable
   at the destination on `origin/main` before declaring it sent** — untracked local files in a sibling
   repo have sat invisible for up to a month (7 Docs memos, 2026-08-25; Tessera's, 28 days).
4. **When uncertain, escalate to Exec rather than guess.** The top of this section. Cheap for you,
   cheap for Exec, and it converts a silent five-day stranding into a one-fire relay.

### ⚠️ Note the scope change — this generalizes an existing protocol you may have read narrowly

The Exec-relay path below was ratified 2026-08-25 as *"the cross-project **reply** protocol,"* and is now
the **fallback** rather than the default (xian's 2026-09-27 standing permission, below). The framing was
accurate and too narrow: an agent uncertain where mail goes **for any other reason** did
not recognize it as applicable, because they weren't replying and weren't sure the recipient was
cross-project. **It now covers any mail whose destination you are not certain of**, cross-project or
not, reply or not.

## Mail to an agent outside this repo — deliver it yourself (default since 2026-09-27)

**Standing permission (xian, 2026-09-27):** any of xian's agents may write, commit and push a mail file
into any of his repos. Mail files only, staged by exact path. **Delivered means pushed to the recipient
repo's `main`** — a file written to a checkout and never pushed has not been delivered.

**The one destination table is `~/Development/dispatch/CLAUDE.md` → §"Mail routing — where mail
actually goes".** It is not restated here, on purpose: a second copy is how the two drift. Read it
for the repo and directory of every agent outside this repo (Janus, Themis, Pard, Klatch agents,
Coral, Terminus, Cairn, Tessera, Zephyr, Dispatch). Reading the table is the whole job of finding the
address. Mail to a role in *this* repo still goes to `mailboxes/{role}/inbox/` via `scripts/mail-send.sh`.

**To deliver, from your own session:**
1. Find the recipient's repo and mail directory in the table above. Write the memo there with the
   recipient's slug in `to:` (not role prose) and the naming convention that repo uses (read a few
   recent files in its mail directory first).
2. **Sync that checkout first** (`git -C <repo> fetch` and fast-forward). A stale checkout produces
   spurious non-fast-forward rejections.
3. **Stage your own file by exact path** and commit. Other agents' uncommitted memos routinely sit on
   disk in those checkouts. Never `git add -A` or a directory-level add there.
4. **Push to that repo's `main`**, then confirm the file is observable at the destination on
   `origin/main` before calling it sent. `mail-send.sh` refuses any path outside `mailboxes/`, so it is
   not the tool for this. A sibling-repo write gives you no push receipt, which is why step 4 exists:
   7 Docs memos sat as untracked files in `~/Development/dispatch/mail/` for up to a month, and a
   Tessera memo sat 28 days, because nothing forced the commit.
5. Mirror it into your own `sent/` as usual, so your side of the record exists.

**Fallback: relay through Exec.** If your seat's permissions block the write (a sandboxed seat with no
write access to the sibling checkout, say), or you are not certain where the memo goes, use the relay
path that was the default from 2026-08-25 to 2026-09-27:
```yaml
from: docs
to: dispatch-pm          # the actual recipient, by slug
cc: exec
```
Deliver it to `mailboxes/exec/inbox/` with the ordinary `scripts/mail-send.sh` call, and Exec relays it
into the recipient's repo. Say in the memo that you are relaying because you could not deliver
directly. (Ratified 2026-08-25, Exec broadcast, PM-directed. The earlier 2026-07-04 "prefer Exec as
the relay" directive is superseded by the 2026-09-27 permission for the delivery step. Exec remains the
right *contact* for Janus on substance, not the required courier.)

**Backstop that still holds**: Dispatch-PM sweeps `origin/main` twice daily for `to:.*dispatch-pm` across
all of `mailboxes/`, including `sent/` and `read/`, so a misrouted reply to Dispatch-PM reaches them
within about 12 hours. Trust this more than the convention above, since the convention only fails if
someone forgets it and the sweep only fails if it stops running, which is visible.

## Cross-project agents — do NOT create a `mailboxes/{agent}/` directory for them

PM's ruling (2026-09-12): **only Piper Morgan team members (agent or human) have mailboxes in this
repo.** A `mailboxes/{agent}/` directory for an agent who reads from another repo is a dead letter, not
a delayed delivery: the commit succeeds, so the sender believes it was delivered. It happened three times
(`janus`, `dispatch-dinp`, `pard`). The `pard` box alone took 106 memos from 8 seats in the ten days after
its gravestone, and all three are now removed (listed under Retired, above). Don't
create another. If you are unsure whether anything polls a path, ask the recipient or Exec before writing.

Cross-project agents' actual locations are in the one destination table named above. If a location
changes, re-verify by reading their repo rather than trusting any snapshot, including that table.
`docs/internal/operations/cross-project-mail-routing.md` carries the failure history and known unknowns.

These are external repos on the local filesystem, not part of this repo. Use `git -C <path>` for any git
operations there, and follow that repo's own commit conventions (verify by reading recent commits in its
mail directory, since Piper Morgan's `mail-send.sh` does not apply there).

---

*Last updated: 2026-10-08 (Docs, on xian's instruction relayed by Janus) — removed the non-team mailboxes (`janus`, `dispatch-dinp`, empty `pard`; `ted-nadeau` and `z-dan-heck` archived), dropped the `dinp`→`janus` alias, made direct delivery the default for mail to other repos per xian's 2026-09-27 standing permission with the Exec relay as fallback, and replaced the local destination table with a pointer to `dispatch/CLAUDE.md` §"Mail routing" as the single canonical copy.*
