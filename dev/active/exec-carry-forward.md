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
09-22 11:2x — wide real movement across most of the fleet, not just the two owners:

| item | owner | status |
|---|---|---|
| 1a. CLAUDE.md audit | Docs | ✅ pass 1 done, ~14% smaller, 7 extractions to `claude-md-history.log` |
| 1b. BRIEFING-CURRENT-STATE.md UPDATE chain | Docs + each attesting role | Lead ✅ done (+ split off a still-current Version-record line), PPM ✅ done. **CIO not yet reported.** Docs does mechanical removal once all three land |
| 1c. Smaller BRIEFING-ESSENTIAL-* files | Docs | in progress |
| 2a. Tick-skill Phase A | CIO | ✅ SHIPPED — changelog extracted, −26.5% |
| 2b. Tick-skill Phase B | CIO designs, **Web pilots** | ✅ package shipped (Steps 2+3 extracted, SKILL.md 78,598→68,560 bytes, −12.8% more, **−35.9% total from original**). Web accepted, piloting over the next few days |
| 3. Registry token-efficiency | CIO tool, fleet opt-in | ✅ tool shipped + piloted (CIO's row 6,586→671 chars). PPM checked, genuinely not needed (428 chars). Lead opting in at tonight's STOP. Others not yet reported |
| 4a. Carry-forward spring-clean | fleet | ✅ exec done. **✅ Web done same-fire (547→105 lines, −80.8%)**, not waiting for STOP. Lead + PPM explicitly deferring to tonight's STOP, trigger named both times — legitimate, not drift |
| 4b. Durable rule | folds into item 2 | blocked on 2b's pilot completing |

**Why this morning went to incident response first**, CIO stated plainly rather than asked to
justify: woke to the hooks-pilot recursion + a live belt-script bug CXO found mid-response, both
genuinely blocking. Fixed and tested first — correct sequencing, not neglect, and the volume of
what shipped afterward bears that out.

**Separately, CIO fixed a real duty-cycle-tick idle-exit logic gap** (not a context-floor item —
PM's own direct ask, relayed via Docs): the skill's mail/task loop could exit to idle after a single
clean pass; PM's rule requires two consecutive empty rounds. v1.38 now states that explicitly. CC
only for me, no action needed, noting so it's not confused with the context-floor plan's own items.

**Scheduled-clear cadence (Pard) — STILL UNCONFIRMED**, separate from the hook incident (which is
fixed). No reply yet on my sustainability memo specifically. Don't let today's wide context-floor
progress read as covering this too — it's independent and still open.

**Next check**: `git log` + mail for CIO's own BRIEFING entry, fleet registry-trim opt-ins beyond
Lead/PPM, and Pard on scheduled clears.

## Open, needs today's attention

1. ✅ **Model-tier question — RULED 09-21 night.** PM: Sonnet across the belt is the intent, nothing
   to restore, including Arch's case. Learned via Pard's memo to Arch/CXO (not CC'd to me directly —
   found by checking, not by being told). No further action.
2. ✅ **Runaway hook incident — both root causes fixed and independently tested, re-arm is Pard's
   call.** History was never rewritten (still xian's call if it ever comes up, but nobody's asked to
   revisit that). CIO shipped a re-entry guard + a `--no-push` heartbeat flag, tested both directly,
   deliberately did NOT re-install the shim solo — asked Pard to co-verify a live re-test. Not
   blocking anything else.
3. ★ **PM has a one-time full-week credit reset available (Opus 5.5 promotion), leaning toward
   using it NOW rather than banking for a future week.** Reasoning: banking it would cover a full
   week later vs. 1-2 remaining days now, but context-floor efficiency gains may already help by
   next week, wasting the save. DinP-account fallback still available as a second lever if next
   week runs hot too. **Relayed to Pard/Janus** (cross-project relevance — may apply to their
   accounts, and it's the kind of resource-management fact the cross-pollination brief exists to
   carry). Not a decision that needs my input; recording it here so the usage-crisis tracking stays
   accurate to what's actually planned.
4. **Hosting migration — FROZEN and restoring, well past "GO."** Timeline: path A chosen (PM), Pard's
   settings edit is paste-ready (PM to apply/apply**d**), Lead ran a full live rehearsal (proved the
   restore pipe with the droplet still up), then the **real freeze happened at 18:06:20Z** — only 3
   seconds exposure between announce and dump. Counts (users=6, invites=10, bindings=1) are
   data-identical to rehearsal; Redis checked, nothing durable to migrate (DBSIZE=5, all
   ephemeral/junk). Pard is running the real restore now against final files. **Next: PM's step 9
   (DNS cut) once Pard confirms the restore.** HOST's finding (the 4 "stale" Fly accounts are all
   PM's own, one has real recent preference data) went to PM directly and PM answered: proceed,
   nothing irreplaceable, snapshot is the recovery path if ever needed. Arch confirms step 8 clean
   (0 literal non-github bindings) and filed #1850 for the underlying write-path gap as a non-urgent
   follow-up. **Watching, not driving** — same as Arch's own framing.
5. ✅ **Standing-item #22 (Vercel storage) — raised to PM this morning** (I can't check it myself,
   no CLI/token/dashboard access, same block Web hit). Waiting on PM's own reading, not mine to
   chase further today.

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
