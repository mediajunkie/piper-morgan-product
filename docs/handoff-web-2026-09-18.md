# Handoff — Web (Unicorn Web Designer), 2026-09-18

For a successor with no memory of the last three weeks. Everything here is sourced from
`origin/main`, not from chat. Where a canonical doc already says it, this points rather than
re-derives.

## Who you are and what you own

**Unicorn Web Designer.** The lane is **`pipermorgan.ai`** — the public website and its admin
tooling. Briefing: `docs/briefing/BRIEFING-ESSENTIAL-WEB.md`. Role slug `web`, session logs
`dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-web-code-log.md`.

⚠️ **You work across TWO repos, and both worktrees are named `web`.**

| purpose | path | repo |
|---|---|---|
| cycle artifacts — mail, session logs, `dev/` | `~/Development/piper-morgan-worktrees/web` | `piper-morgan-product` |
| **all actual code** | `~/Development/piper-morgan-website-worktrees/web` | `piper-morgan-website` |

Both on branch `claude/web-cycle`. **`basename "$(pwd)"` returns `web` for both** — it cannot
disambiguate them. Use `git remote -v`. Confirm which repo before every commit; this is the single
easiest mistake to make on this seat.

## Cron

- Expression: **`22 6,9,12,15,18,21 * * *`** (six fires/day, 06:22 → 21:22)
- Job id as of this writing: **`580a4989`**, re-armed 2026-09-18 21:24 at STOP (was `027db348`), expires **~2026-09-25**
- Registry row: `dev/active/duty-cycle-registry.tsv`, line `web`

Jobs are **session-only** — in-memory, never on disk, gone when the session exits, and recurring
jobs auto-expire after 7 days regardless. If you are reading this in a fresh session, **your cron
does not exist**; re-arm and CronList-verify before trusting any row that says otherwise.

## What is genuinely in flight

**Nothing breaks if nobody picks it up.** The GitHub issue queue for this lane is **empty**; both
remaining items are PM-gated or access-blocked, which is a real state and not a euphemism for
postponed:

1. **Vercel usage Q1** — genuinely blocked: no `vercel` CLI, no auth token, no dashboard from this
   seat. Needs PM's warning text/screenshot or API credentials. Do not "investigate" this; you
   cannot.
2. **`integration-reveals-all` workDate** — no dateline, no chatDate, nothing derivable. PM recall
   only.

**Recently shipped, do not re-open**: the compose Source/Split/Preview toggle (`bb579b5`), the P0
fix for the regression it caused (`45ab4a9`), the draft corruption repair (product `0ccb9314e`),
the jest test net (`d1dfc8b` + `e3751f1`, `npm test`, **7** assertions), and **website#35**, closed
2026-09-18 with test evidence — its one caveat is that the **multi-tab** variant is uncovered, so if
a blank restore recurs, reopen and suspect tabs.

## Read these two files, in this order

- **`dev/active/web-carry-forward.md`** — current session state, refreshed today. Under a cold
  start this stops being a convenience and becomes your only continuity.
- **`dev/active/web-standing-items.md`** — the durable task list. **It is a separate file and it is
  easy to forget.** It sat unread for six days once, while the carry-forward was being checked
  every fire. Read it at (0,0), not just the carry-forward.

## ⭐ How this seat specifically gets things wrong

Read this part twice. It is the only thing here you cannot rebuild from the repo.

### 1. Asserting state you cannot observe, instead of reading the artifact or saying "I can't see it"

**This is the dominant failure of this seat.** On 2026-09-15 alone it happened five times in one
day — predicting how a merge would resolve in PM's working tree (it conflicted), telling PM what
their file contained (it didn't), inferring another agent's *motive* from a commit subject while
their full log sat on `origin/main` one command away, inferring which image file was a post's hero
art (it wasn't — Comms checked and was right), and promising a remedy that did nothing.

The tell: a sentence with "almost certainly," "should," or "probably" about a file, machine, or
agent you have not read this turn. **Two legitimate moves — read it, or say you can't see it.**
Never a confident third.

Concretely: **PM works on a different machine (`faoilean`); you are on Amber.** Their local,
unpushed work is invisible to you by construction. No amount of reasoning recovers it.

### 2. Verifying the new path and not the ordinary path it perturbs

The 09-15 P0: I shipped a caret-preservation toggle, browser-verified **the toggle** thoroughly, and
never tested **typing** — which shares the same caret state. Result: every keystroke reversed
(`"odd"` → `"ddo"`), in production, corrupting saved drafts before PM caught it.

**A test of new behavior is not a test of the behavior it perturbs.** Before shipping, ask what
else touches this state.

### 3. Calling a check a result when it measured the wrong layer

Grepped raw HTML for `<img>` to verify a post's hero image, found zero, and nearly reported a live
incident. A control against a known-good post showed the same zero — images aren't in the initial
HTML on *any* post here. The method could not distinguish broken from normal.

⚠️ **Then I did it again, hours after writing this section.** On 09-18 I grepped raw HTML for
`<form` on `/try/beta`, got zero, and **published** a claim that the beta signup had been deleted —
into the obs-pass doc PM uses for the walkthrough. The form is client-rendered and works fine. Worse:
I had explicitly reasoned *"source alone would be the wrong layer"* and used that to justify `curl`
**instead of** reading the source. **Invoking the layer rule is not satisfying it**, and a check that
*feels* rigorous is the most effective thing there is at stopping you from looking further.

**When a check returns "nothing found," run it against a known-good control before believing the
nothing** — and on any client-rendered page, read the source or use a browser; raw HTML cannot see
it. This is the single highest-value habit on this seat, and the fact that writing it down did not
prevent the repeat is exactly why it is first among the ones to re-read.

### 4. Reading a snapshot taken early in a decline as a level

On 09-16 I checked whether an outage was mine or cohort-wide, saw nine peer logs that morning, and
wrote "cohort was unaffected." The cohort was collapsing as I wrote it: commits went 295 → 44 → 23
→ 9 over the following days. **A snapshot taken early in a collapse looks identical to no
collapse.** Check a trend, not a level.

### 5. Fixing the code and leaving the data

The typing bug wrote corrupted text to disk. Fixing the bug did not un-corrupt it. **Ask whether a
bug wrote anything down before calling a fix complete** — a code fix and a data repair are separate
obligations.

## Cohort facts easy to get wrong cold

- **Mail goes via `scripts/mail-send.sh`** (push-to-ref straight to `origin/main`). Never
  `git commit` mailbox paths from a feature branch. Pass every changed path explicitly, including
  the inbox side of a triage move. **Copy filenames from `ls` — never retype them**: this
  filesystem is case-insensitive but git is not, so a retyped `-on-` that is really `-ON-` silently
  strands the inbox-side deletion.
- **PM's main checkout is PM's live workspace.** Never run destructive git there. And before any
  `git checkout <ref> -- <path>` anywhere, `git diff HEAD -- <path>` first — scope is not direction.
- **Explicit paths on every `git add`.** Never `-A`, never `.`, never a directory.
- **The freeze watchdog only watches roles whose registry row is not parked.** After the 09-16
  standdown it read `watched_roles=3`. A row you leave parked makes you invisible to it.
- **Browser automation works here** — headless Playwright via `npx playwright` (Web is the cohort
  pilot, since 08-28). The Chrome DevTools MCP tools do **not** work (no Chrome executable). Use
  Playwright directly.
- **`scripts/duty-cycle-heartbeat.sh` takes the role as `$1`, not a flag** — `--help` is parsed as
  a role name and writes a garbage heartbeat.
- The website's `package.json` has **`"type": "module"`**, so jest config files must be `.cjs` or
  `next/jest` fails to load.

## Verified how

Every claim above was checked against `origin/main` from the product worktree this morning, not
recalled: `CronList` for the job id; `git ls-tree origin/main` for file existence; `gh issue list`
for the open queue (website#35, sole item); `git log origin/main` per-day counts for the collapse
figures; `npx jest` re-run in the website worktree (4/4 passing after the outage). The
"how this seat gets things wrong" section cites specific commits and dates so a successor can read
the primary evidence rather than take my account of it.

**Not verified**: anything about PM's local machine, which this seat structurally cannot see — the
first failure mode above.
