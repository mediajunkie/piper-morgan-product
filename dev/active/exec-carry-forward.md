# Exec carry-forward

**STATE: LIVE.** Cron **`417cb233`**, `38 6,10,14,18,22`, expires ~09-30, re-armed delete-then-create
at each STOP. ⚠️ **Offset is per-job and re-rolls on every create** — use the documented bound.

**Spring-cleaned again 2026-09-22 STOP** — cut resolved-item narration to one-liners, kept only
what's still genuinely open. Full arcs for anything below live in dated session logs, not here.

## Open, real work owed

1. ✅ **Belt classification — DELIVERED 09-24, two days early.**
   `docs/internal/operations/belt-classification-2026-09-24.md`: both halves combined (CIO's proxy
   + my register read + correction counts), recommends **arch then cio** for the Opus 5.5 trial,
   exec explicitly excluded from round 1 (self-dealing + Fable-drift confound, both stated). CIO
   invited to dissent before Pard builds on it. Window question resolved: kept this week, caveat
   leaned on.
2. ✅ **mcp.pipermorgan.ai assignment — RULED 09-23.** PM approved PA's recommendation directly
   (reuse this week's PM+Pard scoped-grant pattern). `decisions.log` entry written. Closed.
3. ✅→🔧 **Duty-cycle cascade — ADOPTED, migration in progress.** PM's word 09-24 ("Yes, adopt
   it"), all four declarations on record. Pard's blocker (the injected prompt text) answered by me
   same-fire with my seat's verbatim prompt + the structural fact that phase is chosen by the SKILL
   at fire time, not the prompt; CIO confirms per-seat variants + does the same-day skill-side
   retirement. **Coordination for MY seat**: migration order is LaunchAgent-loaded-and-verified
   FIRST, then session cron deleted — when Pard confirms my seat's LaunchAgent fired, I CronDelete
   `417cb233` and STOP doing the delete-then-create ritual (retired with the skill prose). Until
   that confirmation: keep the ritual. Pard confirms per seat as each lands (his step 5), cio
   migrates first.
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
   zero violations. `main-old`'s 503 commits NOW REVIEWED (09-24, xian's ask via Janus, subagent + Exec
   spot-check): **nothing critical stranded** — 501 of 503 already on main by content; the 2 absent
   are the obsolete 2025 sprint-creation scripts, fully superseded. main-old safe to freeze or
   delete, disposition PM's whenever.
   One residual oddity, noted by Arch+CIO to PM, no action unless it recurs: an unattributed 23:06
   close event between Arch's reopen and CIO's final work — either PM's own hand or an unidentified
   agent; Arch cleared themselves with first-hand tool-call knowledge.
8. **PM stays ahead on publishing** — tomorrow's post queued, Saturday's being illustrated now.
   No action needed, noted for continuity.
9. ✅ **Fable "drift" — RESOLVED BY INTENT, mostly not drift at all.** PM (via Pard's correction,
   09-24): **exec and pa are on Fable-family DELIBERATELY** ("so they could both be as productive
   as possible in our 1.5 day week"); comms switched back to Sonnet by PM. So this seat stays
   Fable on purpose — nothing to revert, and the classification's exec-exclusion note stands for
   the trial either way. Mechanism of the original switches honestly unsettled (PM "isn't certain
   the switches were manual"), tessera's double-move still unexplained but small. Pard owned the
   framing error (reported an allocation question as a mechanism question) and flagged his own
   instrument's lag caveat (reads last-turn model, not current setting). **Still open, smaller**:
   Pard's intended-model manifest offer (tessera argues for it), xian's word on DinP intended
   models. New useful fact: PM can now read the per-model limit — Fable at 64% of ITS weekly
   ceiling while the account is at 43%; that per-model number is what binds a Fable seat.
10. ✅ **mcp.pipermorgan.ai Phase B — COMPLETE** (09-24, grant 13:00→revoked 19:1x, verified at
   the DNS authority not a resolver cache). One Phase-C fact Pard corrected in advance: Fly won't
   terminate TLS for a machine-less app, so the endpoint stays dark until Lead's first deploy —
   correct behavior, not a broken cut; Pard had told PM to expect otherwise and corrected with a
   test. Phase C is application work; Arch's trigger not yet met.
11. **v0.8.14.0 cut (~14:35), alpha deploy is PM's keystroke** via Pard's sheet; four test-card
   rows waiting on it. Lead also fixed the a1599admin migration guard (keys on DB state, not env) —
   staging can retry paste 3, building from current `origin/main` tip, not the tag.
12. 🔴 **#1885 — three LIVE unused invite tokens were in tracked logs (public repo); scrub done,
   BURN needs PM's hand.** Lead's lint (the #1845 backstop) found full-form tokens in 30 tracked
   files incl. HOST's logs and an omnibus; all scrubbed to masked forms on main, gate now fails CI
   on any new one. **Git history still holds the old bytes — the burn (one command, on #1885) is
   the actual fix, and Lead's prod DELETE was classifier-denied (correctly not routed around).**
   After the burn: mint 2 replacements, re-record roster rows for Savanna and Janne, masked-only
   delivery. Also on the issue for PM's console: two 2025 key-shaped strings (a Google key, an old
   Slack bot token) of unknown liveness.
13. **Cascade prompt-shape finding**: CIO's literal prompt is `DUTY CYCLE TICK (CIO)` — a
   completely different shape from mine. Real variance across 2 of 2 seats checked; CIO's theory
   (Model A pins role/worktree/branch by launch, so my constants block is redundant documentation)
   is consistent with my own stale-model-constant evidence. Pard's generator decision — both
   shapes in front of him; the migration defines the canonical shape going forward regardless of
   historical variance. CIO holds the skill-prose retirement until their own LaunchAgent fire is
   verified — named trigger, correct.

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
  stand as before — neither was contingent on this. Seat-model arc CLOSED: the Sonnet→Fable switch
  was PM's deliberate reset-day allocation (exec+pa productive for the short week), and **PM said
  09-24 evening: after the 10 pm reset, Fable is reserved for Lead** — so a model change on this
  seat tonight/tomorrow is ANNOUNCED, expected, and not to be flagged as unexplained.

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
