# Exec carry-forward

**STATE: LIVE.** Cron **`c4d9399e`**, `38 6,10,14,18,22`, expires ~09-27, re-armed delete-then-create
at each STOP. ⚠️ **Offset is per-job and re-rolls on every create** — use the documented bound (slot
+ up to 15 min), never a remembered figure.

**Spring-cleaned 2026-09-21 STOP** — this file had accreted duplicated headings, a fully-superseded
invite-token narrative, and ~50 lines of 09-18 arrival history no longer active. Cut per today's own
context-floor-reduction plan (item 4b): current state only; full narrative for anything below lives
in the dated session log, not here.

## ★ STANDING OWNED ITEM — context-floor plan (PM, 2026-09-22: "biggest lever now, aside from
more frequent clearing")

**Check progress at EVERY fire until all four items land, not just when reminded.** Status as of
09-22 09:0x — real shipped progress from both owners, not just alignment:

| item | owner | status |
|---|---|---|
| 1a. CLAUDE.md audit | Docs | ✅ pass 1 done, ~14% smaller, 7 extractions to `claude-md-history.log` |
| 1b. BRIEFING-CURRENT-STATE.md | Docs | ⚠️ pass 1 done (8.3%, safe prunes only). **Scope ruled**: the ~140KB multi-role UPDATE chain needs each attesting role (Lead/PPM/CIO) to prune their own entries — asked, not yet done |
| 1c. Smaller BRIEFING-ESSENTIAL-* files | Docs | in progress |
| 2a. Tick-skill Phase A | CIO | ✅ SHIPPED — changelog extracted, 106,990→78,598 bytes (−26.5%), zero-risk one-line diff |
| 2b. Tick-skill Phase B (the hard cut) | CIO designs, **Web pilots** | design doc ready; Web asked to pilot before fleet rollout |
| 3. Registry token-efficiency | CIO | ✅ tool shipped (`scripts/trim-registry-history.py`), piloted on CIO's own row (6,586→671 chars). Fleet-wide opt-in ask sent to the other 8 roles |
| 4a. Carry-forward spring-clean | fleet | directive sent 09-22 08:1x; only mine (exec) confirmed done, Docs said "doing now" |
| 4b. Durable rule | folds into item 2 | blocked on 2b landing |

**Why the morning went to incident response first** (CIO, stated plainly, not asked to justify):
woke to the hooks-pilot recursion + a live belt-script bug CXO found mid-response. Both genuinely
blocking (shared infra unsafe; every seat's self-verify reading a wrong denominator). Both fixed
and tested before touching context-floor items — reads as correct sequencing, not neglect.

**Scheduled-clear cadence (Pard) — STILL UNCONFIRMED, separate thread from the hook incident.**
PM flagged possibly conflating the two. Checked: no reply from Pard on my 09-22 07:5x sustainability
memo specifically about scheduled clears. The hook-pilot incident/fix is CIO's post-commit hook
(heartbeat automation) — genuinely a different mechanism from a scheduled context-clear cadence.
Don't conflate the two when reporting status to PM; they're both real but independent.

**Next check**: every subsequent fire, `git log` + mail for: Docs' Lead/PPM/CIO-pruning replies,
Web's Phase B pilot start, fleet registry-trim opt-ins, and Pard on scheduled clears specifically.

## Open, needs today's attention

1. ✅ **Model-tier question — RULED 09-21 night.** PM: Sonnet across the belt is the intent, nothing
   to restore, including Arch's case. Learned via Pard's memo to Arch/CXO (not CC'd to me directly —
   found by checking, not by being told). No further action.
2. 🔴 **NEW — runaway hook incident, PM decision pending, unresolved into today.** CIO's post-commit
   hook pilot (fire zero, ~22:38 PT 09-21) recursed: heartbeat's own quiet-path commit re-triggered
   the hook, no re-entry guard, ~2,900 nested processes, **967 marker commits** (each touching only
   `dev/heartbeats/last-invoked/cio.txt`) pushed to `origin/main` before Pard disarmed (23:10:07) and
   killed the chain (23:13). Verified independently against real trunk history, not taken on Pard's
   word: `git log --grep` in that window returns 968. **No code or data touched.** Pard deliberately
   did NOT rewrite history — explicitly deferred that call to **"xian's decision in daylight."** Not
   yet in `decisions.log`. Two root causes named (no re-entry guard; a hook that pushes), CIO owns the
   fix, pilot is paused not just disarmed. **This needs raising to PM today — it hasn't been.**
3. **Hosting migration — GO for THIS morning (Tue 09-22), PM-confirmed.** Runbook:
   `docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md` (on origin/main). Two things
   surfaced tonight that I'm tracking but didn't need to act on:
   - Lead surfaced a path-A/B decision on Pard's Fly-write classifier gating **directly to PM in
     conversation** at tonight's STOP — check `decisions.log` + mail before assuming it's still open.
   - Arch found the `mcp_server_ref` backfill only covers `github` (3 of 4 connector types
     unchecked) — a 5-minute SQL check before/at step 8, not mine to run, Pard/Lead's.
   Nothing further owed from me unless PM asks.
4. ⚠️ **Standing-item #22 (Vercel storage daily check) was MISSED yesterday** — three fires ran, none
   raised it. Named honestly in `exec-standing-items.md` rather than left implicit. **Raise it first
   thing this fire, before anything else competes for attention — STILL NOT DONE, do it now.**

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
