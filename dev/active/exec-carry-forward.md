# Exec carry-forward

**STATE: LIVE.** Cron **`c4d9399e`**, `38 6,10,14,18,22`, expires ~09-27, re-armed delete-then-create
at each STOP. ⚠️ **Offset is per-job and re-rolls on every create** — use the documented bound.

**Spring-cleaned again 2026-09-22 STOP** — cut resolved-item narration to one-liners, kept only
what's still genuinely open. Full arcs for anything below live in dated session logs, not here.

## Open, real work owed

1. **Belt classification, due Sat 09-27** — CIO's half is a real first pass, not just a plan:
   `scripts/belt-mechanical-reasoning-proxy.py` built and tested, caught and fixed a genuine 20x
   confound (967 fire-zero-incident heartbeat commits inflating CIO's own mechanical count) before
   reporting a number. Current table (incident window excluded): arch 0.63, cio 0.72, comms 0.75,
   cxo 0.60, docs 0.92, exec 0.80, host 0.78, lead 0.82, pa 0.79, ppm 0.55, web 0.66 (substantive
   ratio). **Confirms the atypical-week caveat hard**: 43% of all commits in the 4-day window came
   from one incident. Open question CIO raised: widen the window past this week, or keep it and lean
   on the caveat — my call to make when I do my own half. **My half (session-log reading) not
   started yet.**
2. ✅ **mcp.pipermorgan.ai assignment — RULED 09-23.** PM approved PA's recommendation directly
   (reuse this week's PM+Pard scoped-grant pattern). `decisions.log` entry written. Closed.
3. **Duty-cycle standard cascade — still waiting on PM's word.** All three declarations in.
   Full context PM asked for, since the rollup card was too thin to decide from: session-scoped
   crons (`CronCreate`) are documented as ephemeral by design — die with the session, auto-expire
   at 7 days — which is the root cause behind a whole week of things I've personally had to manage
   by hand (offset drift, 7-day rotations, the Gap-C compaction-kills-cron incident). The proposal
   replaces that with OS-level LaunchAgents that fire independent of any session's lifetime — a
   stronger "not-failing" guarantee instead of "detect-and-heal." Concrete cost: ~2h Pard's time,
   all 11 seats, reversible per seat with one command, doesn't change *when* anything fires or touch
   the worktree/push-to-main/mail layer. CIO (who owns the mechanism being replaced) recommends it;
   Klatch already adopted independently. If it lands: retire my own manual cron-rotation ritual from
   `duty-cycle-tick`'s text same day — don't let the old prose become its own accretion.
4. ✅ **STALE, corrected 09-23 — this was never mine.** PA's 09-20 calibration-shape question
   ("should Lead's usage-per-account-capture proposal actually get built") was answered by PM
   directly to PA on 09-22 morning: yes, build it. PA is now driving it themselves (writes the spec,
   dispatches to a `prog` subagent), waiting on two sub-answers from **Pard** (is the usage number
   Dispatch-readable) and **PM** (seat→account mapping) — neither is my lane. Caught before I sent
   a redundant answer to something already resolved; removing from my owed list.
5. **Ship #061** — publishes TODAY (Wed 09-23) per Comms' approval.
6. **Records-gap questions 5-6** (Janus) — deferred with a named trigger (dedicated pass), not
   started. Q1-4 already answered by Docs and relayed.
7. ✅ **#1744 — GENUINELY CLOSED, the full arc.** PM deleted classic protection on `main`; Arch
   behaviorally confirmed the ruleset's Admin bypass with a real push (no bypass notice — nothing
   left to mask it); then Arch caught their OWN premature close (misread the synthetic fixture's
   bait checkbox as an attestation), reopened, and CIO ran the actual closing condition end-to-end:
   the scope-guard bot's own `GITHUB_TOKEN` push landed a memo at PPM's inbox through the ruleset,
   zero violations. `main-old` untouched throughout, its 503 unmerged commits still awaiting their
   own separate review (nobody's task yet — genuinely unowned, worth a rollup line eventually).
   One residual oddity, noted by Arch+CIO to PM, no action unless it recurs: an unattributed 23:06
   close event between Arch's reopen and CIO's final work — either PM's own hand or an unidentified
   agent; Arch cleared themselves with first-hand tool-call knowledge.
8. **PM stays ahead on publishing** — tomorrow's post queued, Saturday's being illustrated now.
   No action needed, noted for continuity.
9. 🔴 **Fable drift — CONFIRMED STICKY AND CROSS-ACCOUNT, awaiting PM's two decisions.** Pard
   re-read all 25 host sessions with an independent instrument: comms/exec/pa still Fable-family
   2+ hours post-reset (PA confirmed 3h, third instrument: their own commit trailers). **Tessera
   (DinP account, never near a ceiling) drifted too** — so pure rate-limit-failover doesn't fully
   explain it. Lead's 5→5.1 bump was PM-directed in-conversation ("Move you to Fable 5.1") — that
   row is explained. **Correction mechanics known** (Pard): model is session state; `--resume`
   does NOT restore it and settings.json only affects new launches — the fix is `/model
   claude-sonnet-5` typed in each seat, or relaunch with explicit `--model`. I cannot self-revert.
   **PM's decisions**: (a) revert comms/exec/pa (Pard will execute if asked, won't reach into PM
   seats uninvited); (b) greenlight Pard's offered intended-model manifest + drift check (small,
   this week, turns "seat felt different" into a drumbeat line); (c) xian's word on DinP seats'
   intended models — Tessera is the live example.
10. **mcp.pipermorgan.ai Phase B — READY, waiting on PM's window.** Pard's exact command sheet +
   60-minute scoped grant is in; needs ~10 min of PM attention in two touches (paste the grant, two
   Hover DNS steps, cert-before-traffic per the 09-22 lesson). No app code; nothing for Arch until
   Phase C.
11. **v0.8.14.0 cut (~14:35), alpha deploy is PM's keystroke** via Pard's sheet; four test-card
   rows waiting on it. Lead also fixed the a1599admin migration guard (keys on DB state, not env) —
   staging can retry paste 3, building from current `origin/main` tip, not the tag.

## Context-floor plan — still the standing top priority, real progress this week

Four items, wide movement across 5+ roles (Docs, CIO, Lead, PPM, Web all shipped or correctly
declined work). **Only genuinely open piece**: CIO's own BRIEFING-CURRENT-STATE.md entry and Docs'
two are still unreviewed; Web's tick-skill pilot (Phase B) continues watching, clean through day 1;
Lead opting into the registry-trim tool at tonight's STOP. **Scheduled-clear cadence with Pard is
STILL UNCONFIRMED** — separate from the (fixed) hook-recursion incident, don't let today's other
progress read as covering it. Full detail: `docs/internal/operations/context-floor-reduction-
plan-2026-09-21.md` + this week's session logs.

## Standing PM-gated

- ✅ **The ruleset decision — RESOLVED by the #1744 arc** (09-23). PM created the ruleset, deleted
  classic on `main`, bot delivery behaviorally confirmed. The 09-16 "which surface owns it"
  question is answered: the ruleset does. Arch/CXO unparked.
- **Vercel storage** — raised to PM 09-22, I can't check it myself (no CLI/token/dashboard).

## Resolved this week, no longer tracked in detail (see session logs for the full arc)

- ✅ Model-tier question (Sonnet is the intent, RULED 09-21).
- ✅ Runaway hook incident (both root causes fixed, tested; re-arm is Pard's call, not blocking).
- ✅ Hosting migration — **COMPLETE**. alpha.pipermorgan.ai on Fly, zero data drift, path A revoked.
  Post-cutover deploy path ruled Lead's (§4e, pipeline plan v0.3). #1850/#1852 filed, non-urgent.
- ✅ **Usage crisis — CLOSED 09-23 ~11:5x.** Wall hit, PM applied the one-time reset, full week's
  credit restored. Fleet closure notice sent. Don't-self-throttle + context-floor-top-priority both
  stand as before — neither was contingent on this. ⚠️ **Observed at the same moment: this seat's
  model changed Sonnet 5 → Fable 5, unannounced** — flagged to PM as observed-not-chosen per this
  week's tier-change discipline; awaiting PM's word on whether it was intentional.

## This seat's standing errors (deduplicated, keep watching)

- **Verify the artifact the instrument reads, not the one you edited** (`sync-pm-local.sh`).
- **`echo` after `||` asserts nothing** — always re-read `origin/main`.
- **Mail-send needs BOTH inbox source and read destination in one call** — recurred three times
  this week before it stuck. Verify with `git ls-tree origin/main`, not a clean exit code.
- **`mailboxes/pard/` is HARD-REFUSED** — Pard's real inbox is `~/Development/mediajunkie/docs/
  mail/`, written via manual `git -C` there, verified via `git log origin/main -1` in *that* repo.
  Same convention applies to any cross-repo cc (caught myself dropping this exact discipline on a
  Janus cc that sat uncommitted in DinP for two days). Adopt `reply-to:` frontmatter on anything
  leaving this repo. ⚠️ **PM told PA directly (09-23) to write to Pard's real inbox themselves
  rather than route through Exec-as-relay** — a live exception to the documented default. Worth
  watching whether this becomes the general rule or stays PA-specific; not mine to decide, just
  tracking that it happened.
- **Don't write a decision brief on another role's surface without them reading it first.**
- **A park without a computed deadline is not falsifiable.**
- **Registry/carry-forward text can sit factually wrong for hours after a correction lands** —
  check the actual current-state text, don't assume a fleet-wide memo was enough alone.
- **zsh does not word-split `$VAR`** — build path lists as arrays.
- **`closedAt` is UTC** — compute in Pacific and say which timezone.
- **The registry-row rewrite script keeps producing `active: active:`** — the prefix string I
  build already starts with `active: `, and the reassembly adds it again. Three times now
  (09-21, 09-22, 09-23), caught post-push each time. Next STOP: strip `active: ` from the
  PREFIX, not just the rest, or better — reuse one tested helper instead of retyping the
  logic inline each night.

## Also live, lower priority

- **Weekly reflection proposal** with CIO — must ride an artifact with a live reader.
- **Memory export cadence** — open question with CIO: event or schedule.
