# Exec Carry-Forward

**Last updated**: 2026-07-31 ~09:55 PT — after the morning fire.

## Fire-state delta (7/31 morning — supersedes queue items below where they conflict)

- ✅ **Jake synthesis DONE + delivered to PM** (`dev/active/jake-ftux-four-lens-synthesis-2026-07-31.md`).
  Next: PM+CXO decide on §4's six items → flag triggers PPM's same-day issue conversion. Exec holds no
  further synthesis action.
- ✅ **Ship #054 kickoff SENT** (6 roles, procedural deadline = their Saturday day-close fires). Watch
  collection; 6/6 hard gate; draft Sunday if all in.
- ⚠️ **#1386 window RE-SCOPED** (memo + issue comment): Scenario-B + #1393/#1394 only; criterion 2
  DEFERRED pending PM key provisioning (canonical suite skips keyless — PPM/CXO withheld correctly).
  **Critical path = two PM actions**: keys via KeychainService (unblocks 4 lanes) + rousing Lead (row
  still parked, no cron — driver cannot wake autonomously). Report state each fire; Scenario-B runs at
  Lead's first opportunity after waking.
- **Two coordination rules adopted** (from the window post-mortem, both mine to practice): the driver
  re-verifies a locked window's preconditions at window start; the coordinator verifies the driver's
  wake mechanism before naming a start time.
- **Evening fire**: check Scenario-B/keys movement, #054 early arrivals, then HOST checklist v2.0 review
  if quiet. PA's ⏰ OpenAI item: still unverified whether PM did it Thursday — worth one line in the next
  PM contact.

## Friday 7/31 queue — IN ORDER (all unblocked)

1. **Jake FTUX synthesis — 4 of 4 IN** (HOST 7/27 trust · CXO 7/29 experience · PA 7/29 in-house-experiment · PPM 7/30 roadmap, all in `mailboxes/exec/read/`). **Framing per PM's ruling (CXO relay 7/30): collection-and-framing INPUT to a PM + CXO experience decision — not a committee verdict.** Known structure: PA's cold-start reframe is the agreed root (4/4); CXO consent-gate + capability-legibility ship together; CXO§6/PA#1 converge on demonstrate-don't-describe; **PPM's surface filter is the sort key** (bucket A dies with PDR-006 / B relocates to tool catalog / C is-the-beta); PPM's gate finding (m-44 at product level — the gate can't fail for what Jake reported) + their 3 recs (don't expand #1386; add a first-contact demonstration criterion; HOST's consent gate is a genuine blocker). PPM's tool-catalog-naming risk flag (situation-names may route worse for the host LLM — test both before committing) goes in as an open question, not a settled call. **Flag PPM the moment it's done** — they convert to GitHub issues same day.
2. **Ship #054 kickoff** — window Jul 24–30, pubDate **Wed Aug 5** (v1.9 rule). Request all 6 workstream memos; hard gate stays 6/6.
3. **08:32 fire: verify #1386 re-run state ON THE ISSUE, report to PM.** Window locked tonight (`c3033e577`, PM expedite directive, beta target **Aug 8**): Lead drives canonical suite + Scenario-B from ~06:17 (venv acceptance first, fail-fast to me), CXO ~06:47 / PPM ~06:52 sign off on the issue. Scope: closes criterion 2 + #1393/#1394 only — NOT the gate (criteria 1/4/5/6 remain; #1278 scope call is PM's, on the board). Fallback: window moves + slip reported, never silent drift.
4. **HOST checklist v2.0 → Exec review** (then CEO ratification) — when 1–3 clear.

## Board state (rollup delivered 7/30 09:45)

`dev/active/exec-cohort-attention-rollup-2026-07-30.html` — 3 blockers / 6 decisions. **Two blockers cleared same day**: PPM un-parked (Jake 4/4, PDR-006 complete, spatial slice shipped) + build stack READY (`2eaa4b594`). Remaining blocker: PA's ⏰ OpenAI verification (PM committed Thu — unverified whether done). Decisions queue unchanged, led by **memory-index governance** (CIO 7/30: hard floor in ~6 days; generator guard shipped; ruling is PM's). Next render: incremental refresh on PM contact — reflect the two cleared blockers + PDR-006 now sitting at PM ratification (PA's memo, all three reviews in).

## Standing (delta from 7/29 sections below)

- **CIO park-check proposal**: Exec endorsed 7/30 AM (one caveat: gate covers provisioned successions only); HOST's read outstanding.
- **PM ruling to make durable if PM confirms wording**: "experience decisions are PM + CXO; other lenses are input" — currently lives only in CXO's relay + my log; decisions.log candidate.
- Lead's #1424 (+#1427 one-line confirm), #1278, tester-welfare instrument, Comms' 5-item gated queue: all on the board, unchanged tonight.
- Cron expiry hazard ~Aug 5 (session-only) — cohort-wide, CIO/Pard hold the durable-scheduler question.

---

*(Previous day-close content below — still-valid queue and environment notes.)*
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
