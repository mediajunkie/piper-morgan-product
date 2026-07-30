# Exec Carry-Forward

**Last updated**: 2026-07-29 ~21:40 PT — day-close of the first Amber successor session.
**Session log today**: `dev/2026/07/29/2026-07-29-1220-exec-code-log.md` (successor; predecessor's Desktop close-out is `…-0705-…`, complete without a DAY-CLOSED marker per PM)
**Role**: Chief of Staff (Exec) | Amber, Model A worktree `~/Development/piper-morgan-worktrees/exec`, branch `claude/exec-cycle`
**Cron**: `32 8,20 * * *` — re-armed at STOP (see registry row; job id in session log). ⚠️ Session-only, auto-expires ~Aug 5 — re-arm needs a live session by then.
**Handoff of record**: `dev/active/exec-handoff-2026-07-21.md` (predecessor's final refresh) — still the role primer; THIS file is current state.

## Tomorrow's 08:32 fire — the queue, in order

1. **Cohort-attention rollup** (PM-requested via CIO→Lead relay; quality-banked tonight with explicit trigger, promised to Lead for this fire). Inputs in `mailboxes/exec/read/`: Lead's detailed lane summary (§4 one-liners are rollup-shaped), Janus' checkout-conflict memo (PM explicitly routed it here), HOST's URGENT belt false-alarm (CIO/Pard own the fix; rollup notes it), migration/provisioning state. Use the `cohort-attention-rollup` skill — the GitHub-verify step is the load-bearing part.
2. **Jake FTUX synthesis — fires when PPM lands (3 of 4 in: HOST 7/27, CXO + PA 7/29; PM nudged PPM directly midday 7/29).** Key synthesis structure already identified: HOST consent-gate + CXO capability-legibility are complementary-ship-together on the file-a-ticket incident; CXO §6 and PA #1 (ingest-and-reflect / demonstrate-don't-describe) converge independently; PA's baseline metric ("does the next tester reach a first automated action?") is the measure to propose; PA flagged the meta-intent routing question (read intent-routing-stack.md before anyone patches).
3. **#1386 criterion-2 re-run window — Exec coordinates** (reconciled from the issue: PPM's reopen names Exec active coordinator; go/no-go stays PM's). One canonical-suite re-run against v28 verifies #1393 + #1394. **Chained on the build-stack go** (PM/Pard decision on CIO's spec) — Lead's seat can't run sweeps until then. Track as one chained item, not two.

## Ship #054 — kickoff due Friday Jul 31

Window Jul 24–30, **pubDate Wednesday 2026-08-05** (per `draft-weekly-ship` v1.9's fixed rule — the old "target Tuesday" text and #053's day-after-drafting slip are both dead; see tonight's fire entry). Standard process; the skill has the hero-image Step 4c since v1.8. **After the #054 cycle is under way: raise PM's open ask about day-of-week-aware duty cycling** (kickoff Friday, synthesis Saturday-once-all-6-in) — don't let a second cycle pass.

## Ship #053 — DONE, published, loop closed

Live at pipermorgan.ai (Docs verified 200). Driver gloss race owned by PM directly. Comms' date-slippage sweep answered: skill was the generator, fixed v1.9. Nothing open.

## Standing items

- **Lead's #1424/#1427** — still awaiting PM's calls (open since Jul 18; Lead's 7/29 summary re-confirms, lean: close #1424).
- **Lead lane flags for rollup**: 4 of 6 drain-surfaced fixes have no recorded class sweep (2 cheap greps owed once venv exists, chained on build-stack go); #1457 is the five-whys recurrence case (guard decision open, not the file).
- **Beta Blockers count** — stale; re-pull via `query-github-board` before citing.
- **Tracker reconciliation** (`exec-open-items-tracker.md`) — last 7/20; decide post-rollup whether it still earns its keep or the rollup + carry-forward supersede it.
- **Stale branches (CXO's 3 MUX + CIO's xpoll hook)** — nudged 7/25, no reply; re-check at rollup.
- **Registry/watchdog**: exec row `active` (annotated 7/29); HOST's heartbeat-belt false-alarm fix is with CIO/Pard.

## Environment notes (Amber, verified 7/29)

- Real git-level `pre-commit` gate live in common hooks since 7/29 16:24 (TOCTOU fix; both shapes covered; probe apparatus retired upstream in duty-cycle-tick v1.22 — my local skill copy may still say v1.19+correction until next sync).
- `mail-send.sh` works from this worktree (multiple first-attempt pushes 7/29, incl. a 75-path batch). Build path lists from `git status --short -z`, never memory.
- Memory pool shared (168 files); git identity clean; do not port Model-B collision self-fix (no referent).

## STANDING

- Bridge Log (predecessor's): `https://claude.ai/code/artifact/68f209ae-94fc-484a-8e68-fbc53b3771f8` — Desktop-era; decide at rollup whether to continue or retire.

---

*— Exec (Amber), 2026-07-29 ~21:40 PT, day-close.*
