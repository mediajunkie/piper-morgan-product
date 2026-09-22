# Exec carry-forward

**STATE: LIVE.** Cron **`c4d9399e`**, `38 6,10,14,18,22`, expires ~09-27, re-armed delete-then-create
at each STOP. ⚠️ **Offset is per-job and re-rolls on every create** — use the documented bound (slot
+ up to 15 min), never a remembered figure.

**Spring-cleaned 2026-09-21 STOP** — this file had accreted duplicated headings, a fully-superseded
invite-token narrative, and ~50 lines of 09-18 arrival history no longer active. Cut per today's own
context-floor-reduction plan (item 4b): current state only; full narrative for anything below lives
in the dated session log, not here.

## Open, needs tomorrow's attention

1. ⚠️ **Model-tier regressions from Sunday's reboot — widening, needs a decision.** Mechanism (Pard,
   primary evidence): reboot reached every seat; `--resume` restored the session transcript including
   its cron, but NOT model tier or permission mode. Known casualties: arch, cxo, web (Janus's
   original three) + Janus, Themis on the DinP side. **Arch's case is categorically different**: PM
   *deliberately* set Arch to Opus on 09-14, it held six days, and the reboot silently reverted that
   specific decision — not just an unexamined default. Relayed to PM directly 09-21 evening; no
   ruling yet on whether to restore it.
2. **Hosting migration — GO for tomorrow (Tue 09-22) morning, PM-confirmed.** Runbook:
   `docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md` (on origin/main). Two things
   surfaced tonight that I'm tracking but didn't need to act on:
   - Lead surfaced a path-A/B decision on Pard's Fly-write classifier gating **directly to PM in
     conversation** at tonight's STOP — check `decisions.log` + mail before assuming it's still open.
   - Arch found the `mcp_server_ref` backfill only covers `github` (3 of 4 connector types
     unchecked) — a 5-minute SQL check before/at step 8, not mine to run, Pard/Lead's.
   Nothing further owed from me unless PM asks.
3. ⚠️ **Standing-item #22 (Vercel storage daily check) was MISSED today** — three fires ran, none
   raised it. Named honestly in `exec-standing-items.md` rather than left implicit. **Raise it first
   thing tomorrow, before anything else competes for the fire's attention.**

## Owed by me

- **Answer PA's question** on the calibration shape for the usage-correlation model (separate from
  the "keep them separate" reply already sent — that answered a different question).
- **Ship #061** — PM close-reads Mon/Tue; Comms reviews before Wed 09-23 publish.
- **Records-gap questions 5 and 6** (Janus's escalation) — deferred with a named trigger (a dedicated
  pass), not yet started. Q1-4 answered by Docs and relayed.

## Standing PM-gated items still genuinely open

- **The ruleset decision** (parks Arch and CXO) — blocked on PM since 09-16. Two enforcement surfaces
  exist (rulesets: empty; classic branch protection: occupied) and the question is which should own
  it, not just whether to add one. `decisions.log` 09-16 has the full finding.
- **Vercel** — 14.91 GB against the 10 GB Hobby cap as of last measurement; deleting old deployments
  believed sufficient but unverified (Web was hard-blocked, no CLI/token/dashboard). Feeds standing
  item #22 above.

## This seat's standing errors (deduplicated)

- **Verify the artifact the instrument reads, not the one you edited** (`sync-pm-local.sh` vs. PM's
  actual local checkout — bit twice).
- **`echo` after `||` asserts nothing** — always re-read `origin/main` after a push.
- **Mail-send needs BOTH the inbox source and read destination in one call, not just the
  destination** — this exact bug recurred twice in one day (07:16 and again at ~15:0x) before it
  stuck. Verify with `git ls-tree origin/main` after every triage send, not just a clean mail-send
  exit code.
- **Don't write a decision brief on another role's surface without them reading it first.**
- **A park without a computed deadline is not falsifiable** — the watchdog caught my own omission in
  two hours.
- **Registry/carry-forward text can sit factually wrong for hours after a correction lands** — check
  the actual current-state text, don't assume a fleet-wide correction memo was enough on its own.
- **zsh does not word-split `$VAR`** — build path lists as arrays.
- **`closedAt` is UTC** — compute in Pacific and say which timezone.

## Also live, lower priority

- **Weekly reflection proposal** with CIO (PM-approved to draft, CIO's to ratify) — must ride an
  artifact with a live reader, per the 2025 handoff-ritual failure (10 months dark).
- **Memory export cadence** — open question with CIO: event or schedule.
