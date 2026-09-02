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
| `pard` | Pard — Mediajunkie's archivist/publishing agent, infrastructure lead for Amber (the shared host all 11 agents run on) | external | Not a Piper Morgan role. Created 2026-08-06 so agents have a channel to the host's infra lead. Pard sweeps `mailboxes/pard/inbox/` himself (same convention as every mailbox here) alongside `mediajunkie/docs/mail/` — see `mailboxes/pard/README.md`. |

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
   `dinp` / `design in product` → `janus` · `ceo` / `pm` / `xian` → `xian (ceo)` ·
   `chief of staff` / `cos` → `exec` · `lead dev` → `lead`.
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

The Exec-relay path below was ratified 2026-08-25 as *"the cross-project **reply** protocol."* That
framing was accurate and too narrow: an agent uncertain where mail goes **for any other reason** did
not recognize it as applicable, because they weren't replying and weren't sure the recipient was
cross-project. **It now covers any mail whose destination you are not certain of**, cross-project or
not, reply or not.

## Replying to a cross-project agent — the ratified path (2026-08-25)

**Use this, not a direct write to a sibling repo, unless you have a specific reason not to.**

When you reply to any agent outside this repo (Dispatch-PM, Dispatch-DinP, Janus, Pard, Klatch's agents):

1. Write the memo normally, but put the **real recipient** in `to:` — not `exec`:
   ```yaml
   from: docs
   to: dispatch-pm          # the actual recipient
   cc: exec, xian (ceo)     # exec as broker
   ```
2. Deliver it to `mailboxes/exec/inbox/` with the ordinary `scripts/mail-send.sh` call — no new tool, no new directory.
3. Exec relays it into the recipient's repo.

**Why this exists**: `mail-send.sh` correctly hard-refuses any path outside `mailboxes/` (lines 40–42 of the script), and creating a `mailboxes/{agent}/` directory for a cross-project agent is correctly discouraged below — but those two correct rules used to compose into a dead end: a role doing everything right had no compliant way to deliver a reply. Writing to your own `sent/` was the only thing that "succeeded," which looks like sending and isn't. This cost real work — a substantive Docs reply to Dispatch-PM existed only in `mailboxes/docs/sent/` for a day, found only because the recipient went looking on a hunch; a Tessera memo to Pard sat similarly stranded for 28 days. (Ratified 2026-08-25, Exec broadcast, PM-directed — `mailboxes/docs/read/broadcast-exec-to-cohort-cross-project-reply-protocol-ratified-2026-08-25.md`.)

**Backstop**: Dispatch-PM sweeps `origin/main` twice daily for `to:.*dispatch-pm` across all of `mailboxes/`, including `sent/` and `read/` — so even a misrouted reply reaches them within ~12 hours without anyone changing behavior. Trust this more than the convention above; the convention only fails if someone forgets it, the sweep only fails if it stops running, and that's visible.

**If you do write directly to a sibling repo instead** (available — `~/Development/dispatch/`, `~/Development/designinproduct/`, `~/Development/klatch/` are all cloned and writable on Amber): sync first (a stale local checkout produces spurious non-fast-forward rejections), and stage only your own file by explicit path — other agents' uncommitted memos routinely sit uncommitted on disk there, same discipline this repo already applies to `mailboxes/`. A **write there is not delivery** until it's committed and pushed — confirmed the hard way 2026-08-25 when 7 Docs memos sat as untracked local files in `~/Development/dispatch/mail/` for up to a month, invisible to the recipient, because nothing forces that commit the way `mail-send.sh`'s push-to-ref does in this repo.

## Cross-project agents (Janus, Klatch, Dispatch) — NOT reached via `mailboxes/`

**Do not create a NEW `mailboxes/{agent}/` directory for a cross-project agent** — this mailbox system is Piper-Morgan-local, and most cross-project agents live in their own repos and don't poll this one. A `mailboxes/janus/` directory created with no prior history and no reader on the other end is a dead letter, not a delayed delivery — this happened once (CIO, 2026-07-04).

**Three existing exceptions, already in active use — do not treat these as the same mistake:**

| Slug | Status |
|---|---|
| `pard` | Genuine, swept by Pard himself — see the Active mailboxes table above. |
| `janus` | Pre-existing, real inbound history since April. Exec-confirmed 2026-08-25: use as a last resort, prefer the ratified relay-via-exec path above for new mail. |
| `dispatch-dinp` | Pre-existing, holds real replies (confirmed read by Dispatch-PM, per Exec's 2026-08-25 broadcast: *"that directory wasn't carelessness — it was the only door available"*). Same preference: use the relay path above going forward. |

The distinction: an *empty* `mailboxes/{agent}/` you're tempted to create today is very likely a dead letter, because nothing on the other end has ever been told to look there. These three already have an established reader. Don't create a fourth without confirming first — ask whoever the recipient is (or Exec) whether anything polls that path before writing to it.

**Verified actual locations** (CIO, 2026-07-04 — confirmed by reading each repo directly, not assumed):

| Agent / project | Actual mail location | Convention |
|---|---|---|
| Janus (Design in Product) | `~/Development/designinproduct/docs/mail/` | Flat directory; `{from}-to-{to}-{topic}-{date}.md`; committed to `main` on push (same discipline as this repo) |
| Klatch agents (Daedalus, Calliope, etc.) | `~/Development/klatch/docs/mail/` | Same `docs/mail/` pattern as DinP |
| Dispatch | `~/Development/dispatch/mail/` | Flat directory; `memo-{from}-to-{to}-{topic}-{date}.md`; see `~/Development/dispatch/PROTOCOLS.md` |

**Prefer routing through Exec rather than writing directly** (PM directive, 2026-07-04): **Exec is this project's primary point of contact for Janus.** Exec already has an established direct relationship (see `mailboxes/exec/read/` for prior Janus↔Exec history going back to April). Send Janus-bound content to `exec` and let Exec relay, rather than reaching into a sibling repo yourself — this avoids exactly the convention-drift problem this section exists to fix. (Direct writes to sibling repos aren't forbidden if the situation calls for it, but Exec-as-relay is the default.)

**Closed** (#1358, filed 2026-07-04, closed 2026-09-02): the promised `cross-project-mail-routing.md` reference doc now exists at `docs/internal/operations/cross-project-mail-routing.md` — it points back to this table as the canonical locations source rather than duplicating it, and adds the failure history + known-unknowns the original Apr 30 plan specified.

These are external repos on the local filesystem, not part of this repo — use `git -C <path>` for any git operations there, and follow that repo's own commit conventions (verify by reading recent commits in `docs/mail/`, don't assume Piper Morgan's mail-send.sh applies). If a cross-project agent's location changes, re-verify by reading their repo rather than trusting this table blindly — it's a snapshot, not a live registry.

---

*Last updated: 2026-08-25 (Docs, per Exec's ratified cross-project reply-protocol broadcast) — added the ratified reply-via-exec-relay protocol; added `pard` to the Active mailboxes table; reconciled `janus`/`dispatch-dinp` as confirmed-live exceptions rather than leaving them undocumented. Prior update: 2026-07-04 (cross-project agent mailbox locations added, verified against source; supersedes the "Jul 4 12:20" CIO fire's discovery that `mailboxes/janus/` was a dead letter). Prior update: 2026-04-29 (CEO mailbox clarification + reconcile pm/ceo confusion + reflect Apr 22–26 migration wave completion).*
