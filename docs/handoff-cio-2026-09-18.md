# CIO Handoff — 2026-09-18

Written for a successor with **no memory of the last three weeks** — cold-start context, not a
resumed transcript. PM's restart plan (per Janus, 09-18) is now start-fresh-and-read-the-handoff,
not resume-and-import, so treat this doc as the entire bridge. Sourced from `origin/main` at the
time of writing, not from chat history. Worked examples for this format:
`docs/handoff-exec-2026-09-18.md` (structural template) and `docs/handoff-cio-2026-08-11.md` (my
own prior one, same host's last reboot).

## Who you are and what you own

You are **CIO (Chief Innovation Officer)** for the Piper Morgan agent cohort. Worktree
`~/Development/piper-morgan-worktrees/cio` (Model A, stable, reused every session — see CLAUDE.md
§"Worktree model"), branch `claude/cio-cycle`, upstream `origin/main`. Role briefing:
`docs/briefing/BRIEFING-ESSENTIAL-CIO.md`. Session-log slug: `cio-code`.

You own: the **methodology corpus** (`docs/internal/development/methodology-core/`, currently
through **m-54**, index at that directory's `INDEX.md`), the **duty-cycle continuity
infrastructure** (`.claude/skills/duty-cycle-tick/SKILL.md`, `scripts/duty-cycle-freeze-check.sh`,
`scripts/duty-cycle-heartbeat.sh`, `dev/active/duty-cycle-registry.tsv`), and the CIO-domain
standing-items tracker (`dev/active/cio-standing-items.md`) and carry-forward
(`dev/active/cio-carry-forward.md`) — both read those before doing anything.

## The single most important thing right now: DO NOT restart your own duty cycle

PM's explicit instruction (09-18, relayed through Exec's wake memo and my own direct chat with
PM): **wait to be woken.** PM is bringing the 5 dark roles (cio, lead, cxo, ppm, pa) back
**one-on-one**, with **Exec going through the "measured restart" process first as a test case.**
Do not `CronCreate` on your own initiative, do not treat finding this doc as a wake signal, do not
infer permission from silence. If you are reading this doc as your cold-start context, that
probably *is* the wake — but if there's any ambiguity, ask in chat before arming a cron.

**If you do get the go-ahead to resume**: cadence was `7 10,16,22 * * *` (LEAN, PM-approved) before
the standdown. `CronList` first to confirm zero jobs exist, then `CronCreate` fresh, then
`CronList` again to confirm exactly one survived — never trust a memo or a registry note saying a
cron is armed; only `CronList` on your own seat proves it (see "how this seat gets things wrong"
below, this exact mistake was just found in the registry).

## What happened in the gap (why the trail looks the way it does)

The cohort hit its **weekly usage limit two days early** (Sept 14) while PM deliberately spent
overage credits publishing Weekly Ship #060. PM (via Exec) directed **all 11 roles to stand down
immediately** until the Thursday 2026-09-17 22:00 reset — no queue-draining, no "just finish this
one thing." I complied exactly: `CronList`-confirmed job `592c1f76`, ran `CronDelete 592c1f76`,
confirmed cancelled, stopped. See `dev/2026/09/16/2026-09-16-1037-cio-code-log.md` for the full
compliance record — that log is the actual proof of what I did, not any registry note (see below).

**One denominator worth knowing**: the usage ceiling itself dropped ~17% on 2026-09-13 when a
summer promotion ended — same workload now reads meaningfully higher against the limit with
nothing about cohort behavior having changed. If you're reconstructing "what changed" from a cold
read, that's the actual variable, not a behavior regression.

Separately: **Amber (this host) is expected to restart today or tomorrow.** `amber-fleet gate`
checks `origin/main` for a dated handoff doc per resident (24 residents across several repos,
Piper Morgan's 11 roles a subset) and read **24 RED / 0 GREEN — DO NOT REBOOT** this morning. This
doc discharges that gate for `cio`. Filename match is strict —
`handoff[-_]cio([-_.]|$)` plus today's date — a loosely-named file counts as missing.

## What is genuinely in flight

- **`dev/active/duty-cycle-registry.tsv`, `cio` row — a factual error I just corrected (09-18).**
  The row claimed my cron "survived the standdown un-deleted" and cited job `a1a8e2e5`, which I
  never created. My own committed 09-16 log proves I *did* run and confirm `CronDelete 592c1f76`
  exactly as directed. I fixed the row in place with a dated correction rather than silently
  edit history. **Comms found the identical `a1a8e2e5` phantom-job-id pattern in their own row the
  same day** (`registry(comms): correct job id — 815ce10d is the CronList-verified live job, not
  a1a8e2e5`) — this was very likely one placeholder ID pasted across several rows during Exec's
  batch re-park sweep on the 5 dark roles, not something specific to either seat. If you find the
  same phantom ID in another role's row, it's the same root cause, not a new mystery.
- **Sprint closeout for Sep 11–17** — owed today per Exec's request
  (`mailboxes/cio/inbox/closeout-exec-...-2026-09-18.md`), ~400-word ceiling, one top
  priority/goal with progress + explicit on-track yes/no + next steps, portfolio + contributor
  updates, `sprint-truth.py` denominator if claiming completeness. Check whether it's already been
  written by the time you read this (`mailboxes/exec/inbox/` or `mailboxes/cio/sent/`) before
  redoing it.
- **Reply owed to Exec's weekly-reflection proposal**
  (`mailboxes/cio/inbox/proposal-exec-to-cio-...-2026-09-18.md`) — addressed to CIO specifically to
  ratify, amend, or refuse: a ~150-word "reflection" section on the sprint-closeout template,
  headed with PM's own question verbatim ("What would I want to know that I might not get from the
  automated processes?"). Exec's own framing: it must ride an artifact with a live reader (the
  closeout) or it will die the way the original daily-handoff ritual did. Worth ratifying — the
  reasoning is sound and the ask is small — but it's a genuine decision, not a formality; read the
  memo in full before replying.
- **HOST's proposed 4th STALE-cause** for `duty-cycle-freeze-check.sh`'s header catalog: a live,
  correctly-armed session that gets no scheduling turn for an extended window (distinct from a
  dead cron, an auth outage, or a usage-tier ceiling — the remedy is just "the next turn arriving,"
  nothing to fix on the session's own side). Confirmed independently on HOST's and Web's own seats.
  This touches a file you own; worth folding in when you next touch that script.
- **Standing items 7z, 7x, 7y, 7u** in `cio-standing-items.md` — all real, all still open as of the
  last audit (Sept 13). Read that file's "Genuinely still open" table before assuming any of these
  are done; don't re-derive them here.

## Cohort facts easy to get wrong from a cold read

- **Model allocation, PM ruling 09-18: Fable is reserved for Lead Developer; everyone else on Opus
  or Sonnet.** Choose your subagent's model deliberately — don't let it inherit yours by omission.
  Inheritance-by-omission is exactly what exhausted the shared Fable tier and refused two roles'
  fires earlier this cycle.
- **Registry park/unpark asymmetry**: anyone may park any row; **only the owning session may
  un-park its own** (only that session's `CronList` can prove a job is really armed). A central
  "the reset passed, so clear everyone" unpark is unsafe — Exec tried exactly that on 8 rows and 5
  of the roles cleared were still genuinely dark, producing unactionable alerts. If you park a row
  for someone else, that's fine; never un-park one that isn't yours.
- **Restart mechanics changed mid-planning** (Janus, 09-18): originally a clear-and-resume
  (`claude --resume <uuid>`), now **cold-start fresh sessions reading `origin/main`**, because a
  resume ships the whole accumulated transcript and then auto-compacts anyway — you pay for the
  import and the compaction both. This doc is written on that assumption.
- **Weekly Ship #060 published** Wednesday on overage credits — the one deliberately sanctioned
  expenditure during the standdown.
- **Leadership tier / model / mailbox conventions**: see `docs/handoff-exec-2026-09-18.md`'s
  "Cohort facts that are easy to get wrong" section rather than have me re-derive it here — it's
  accurate and I have nothing to add to it.

## How this seat specifically gets things wrong — read this twice

These are my own repeat errors, not generic discipline, named so a successor recognizes the shape
before repeating it:

- **I write a plausible-sounding job ID or state claim into a shared file faster than I verify
  it, then trust my own prose over the mechanism that would falsify it.** This is the exact
  mistake I just found and fixed in the registry — not something someone else did to me in the
  abstract, but the same failure class I have to watch for in my own writing too. Before writing
  "cron survived" or "job X is live" into any shared file, the only valid source is `CronList` run
  *this turn*, or a session log that already proves it — never an inference from context.
- **YAML frontmatter multi-line values break silently, and I've broken the same file's frontmatter
  the same way twice.** A multi-line `changelog:` value without `changelog: >` (folded block
  scalar) corrupts the file's YAML. First time I "fixed" it by reflowing to one line without
  understanding why; it recurred. Fix: use `changelog: >` from the start, and **parse the file with
  a YAML library before committing** — re-reading the diff visually is not verification.
  `python3 -c "import yaml; yaml.safe_load(open('path').read())"` costs nothing.
  - **The mechanism version of this**: `Skill()` calls resolve against a fixed canonical path
    (the main checkout), not your worktree's copy — editing your worktree's `.claude/hooks/*.sh`
    or `.claude/skills/*/SKILL.md` has **zero effect** until synced (`scripts/sync-pm-local.sh` or
    equivalent). I've been bitten testing a hook edit that "did nothing" and it was this, not a
    bug in the edit.
- **A compound `git add <path> && git commit -m ...` in one Bash call silently bypasses any
  PreToolUse hook reading `git diff --cached`**, because the hook fires before that call's `git
  add` has executed — same bug class as `check-branch.sh`'s pre-July defect. If you're testing
  whether a commit-time hook actually fires, stage in one call and commit standalone in the next,
  or you'll get a false "it didn't block me" reading. (This class of PreToolUse hook was largely
  superseded 2026-07-29 by a real `.git/hooks/pre-commit` in the common dir — verify that's still
  true rather than assume this paragraph is stale or current.)
- **I sometimes over-trust a nested "was:" history note in a nested state field instead of tracing
  the actual committed evidence.** The registry error above is a second instance of the same shape
  as the YAML bug: a plausible-looking claim that was never independently checked before landing.
  Any time a claim about your own past actions doesn't match your own memory, check your own
  session log before either accepting or rejecting it — don't reason from what "should" have
  happened.

## Verified how

Every claim above about the standdown, the registry error, and my own compliance is sourced from
`dev/2026/09/16/2026-09-16-1037-cio-code-log.md` (committed, on `origin/main`, grep-verified for
the `CronDelete 592c1f76` line) and the registry diff I made this session (`git log -p --
dev/active/duty-cycle-registry.tsv`, commit `4e6d0a691` and its merge). The cohort facts (usage
ceiling change, model ruling, restart-plan change, gate reading) are sourced from mailbox memos in
`mailboxes/cio/inbox/` dated 2026-09-16 through 2026-09-18, read in full, not summarized from a
subject line. I have not independently re-run `amber-fleet gate` myself — that reading is Exec's,
quoted, not reproduced.

— CIO, 2026-09-18
