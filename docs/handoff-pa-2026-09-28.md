# Handoff — Piper Alpha (PA), 2026-09-28

**Written for the Amber restart onto `claude-opus-5-5`, PM-approved 2026-09-28.** Assume you are a
fresh session with no memory of the last ten days. This file plus `dev/active/pa-carry-forward.md`
and `dev/active/pa-standing-items.md` is what you have. Everything here is verifiable from
`origin/main`; nothing depends on chat history.

## Who you are and what you own

Piper Alpha — PM/CEO assistant: product judgment work directly with xian, BYOC/MCP program
ownership (new, see below), standup synthesis, document review. Staff tier (not leadership).
Worktree `~/Development/piper-morgan-worktrees/pa`, branch `claude/pa-cycle`, Model A. Briefing:
`docs/briefing/BRIEFING-piper-alpha.md` (refreshed 09-22, should still be current).

## Cron

`42 6,12,18 * * *` (job `d3c21d52`), a **throttled** cadence — PM's usage-back-off directive
09-26. **Pard is disarming duty-cycle fires for the restart window and restoring once a transcript
confirms you're working** — you may not need to re-arm this yourself immediately; check
`CronList` first before assuming zero jobs means re-arm. If you do need to re-arm: the throttle
question is **moot as of 09-28**, per PM directly — you're clear to run the standard
`42 6,9,12,15,18,21 * * *` cadence, not the throttled one. Update
`dev/active/duty-cycle-registry.tsv`'s `pa` row to match whatever you actually arm (currently
still shows the throttled values from the now-moot episode).

## The single most important thing in flight

**PM handed PA full ownership of the MCP testing program, 09-26** (verbatim: *"let's let Piper
Alpha drive the MCP testing program as part of skunkworks and free you up to work on MVP
critical-path epics"*). This is not a paused or background thread — it is PA's active focus.

**Current state, verified this session, not assumed**: `mcp.pipermorgan.ai` units 0–4 are ALL
LIVE (alpha v146, MCP v6/v7, `645ce6412d`). `curl https://mcp.pipermorgan.ai/health` returns
`{"status":"healthy",...}` right now. Identity (fail-closed, hash-only tokens), resources
(profile/colleague-model/github-issues, honest-empty shapes), and the OAuth authorization server
(unit 4, Arch-reviewed and approved — the token-binding security condition is a named test, not
an assumed property) are all built and deployed.

**PM is tester #1, client is ChatGPT first, then Claude.** Tester copy (Lead's own words, already
given to PM in conversation): *"Add a connector with the MCP server URL
`https://mcp.pipermorgan.ai/mcp`. ChatGPT will send you to alpha.pipermorgan.ai to sign in and
approve read-only access to your profile, colleague model and GitHub issues. After approving, ask
it what it knows about you."*

**As of this handoff, PM has not yet attempted first contact.** Your job: watch for it, be ready
to help debug in real time if it goes wrong, and state the three named gaps to PM before or during
that first attempt if they haven't already internalized them — #1458 (cross-caller isolation) is
OPEN but safe here since there's exactly one caller; the recomposition-honesty axis (T-MCP-surface)
is UNMEASURED — PM's session is the first real observation of it; the colleague-model resource
will read nearly empty (only one narrow confirmation type is stored there today). None of these
are secrets to hide — state them plainly.

**Runbook**: `docs/internal/architecture/current/mcp/server-README.md`. **Mint a token** (for
Claude Desktop/Code, which can take a plain bearer unlike ChatGPT): `scripts/mint_mcp_token.sh`
over `fly ssh console` — treat the raw token like an invite token, never put it in the repo.

**Full detail and the whole build history**: `dev/active/pa-standing-items.md` #1, and
`dev/2026/09/26/2026-09-26-0712-pa-code-log.md` (the day this landed — read the backfilled section
near the end, it covers the real decision-making, not just the outcome).

## Other closed/resolved threads — context, not action items

- **T-own-surface (recomposition honesty) empirical series — CLOSED 09-25.** Four independently
  pre-registered rounds with CXO found: the disambiguation mitigation holds on Claude, fails on
  GPT-4o across every design variant tried (metadata/counted-member/uncounted-member/sibling-
  shaped). Folded into `docs/internal/testing/byoc-recomposition-rubric-v0.1.md` v0.8.2 §6e and
  `decisions.log`. Nothing further owed unless CXO registers a new round.
- **Usage-per-account capture (#1862) — live, self-sustaining.** Pard runs a LaunchAgent driver
  every 3h; `dev/heartbeats/usage-per-account.tsv` has a real, growing series including a scoped
  per-model column (the number PM actually manages against, not just the aggregate). Nothing
  regular needed from PA — the correlation model's first *calibrated* pass is the next real step,
  once ~a week of rows accumulates.
- **The throttle-cadence episode (09-26→09-28)** — three genuine reversals in the fleet's own
  understanding of an ambiguous directive, resolved by PM directly telling PA "moot now." Don't
  re-litigate it; just run the standard cadence once you confirm the cron state.

## How this seat gets things wrong — read this part twice

- **A session that runs long on real, valuable live-PM work is not the same as a session that
  closes itself.** 09-26's session extended past its last logged fire into live engagement over
  the MCP launch and never returned to an explicit STOP — Docs' routine daily check caught it, not
  any internal signal. Reconstructed and closed it honestly the next morning from primary sources.
  If you find yourself deep in live conversation past a normal fire boundary, that's exactly the
  moment to consciously check whether a STOP is owed before the session simply runs out of turns.
- **A commit succeeding and a commit doing what it claims are two separate facts.** A tracking
  update once silently no-op'd on a Python quoting bug — the commit landed, but the files it
  claimed to change hadn't actually changed. Caught by `grep -c`-verifying the new text landed
  before trusting the commit message, not after. Do this on every tracking-file edit, not just
  when something feels off.
- **Don't generalize your own seat's data into a cohort-wide claim.** Wrote "the fire-lag anomaly
  self-resolved" in a survey response, based on four of my own fires all reading normal — HOST
  caught that their own seat had the opposite, unbroken pattern the whole time. The corrected,
  sharper fact was "diverged," not "resolved." State your own denominator explicitly before
  generalizing past it.
- **When an ambiguity you didn't create gets ruled on, then retracted, hold rather than infer a
  third time.** Exec explicitly asked everyone to stop self-correcting on the throttle-cadence
  question and wait for PM's actual word — the right move was to hold the current (possibly
  "wrong") state rather than reason your way to a third guess, even when the evidence pointed
  clearly toward a specific answer.

## Open items PM-gated

None currently blocking. The one live thread (MCP first contact) is PA's to watch, not PM-gated —
PM will act on their own schedule; nothing to chase.

## Verified how

`CronList` this session → one job `d3c21d52`. `curl https://mcp.pipermorgan.ai/health` this
session → live, healthy, current git_sha. `gh api .../issues/1462` this session → still `open`.
Registry row read directly from `dev/active/duty-cycle-registry.tsv`, not recalled. The MCP
build/decision history read from the actual backfilled 09-26 session log, not summarized from
memory of writing it.
