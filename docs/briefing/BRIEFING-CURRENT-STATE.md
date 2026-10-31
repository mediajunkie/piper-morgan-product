---
type: briefing
title: BRIEFING-CURRENT-STATE.md - Where We Are Right Now
valid_from: "2025-09-30"
last_updated: 2026-10-30
last_verified: 2026-10-27
size_cap_bytes: 12000
---

# BRIEFING-CURRENT-STATE.md — Now

**What this is**: the one short page that says where the project stands *today*. One dated line per item,
each naming who attests it and how. **Size cap 12,000 bytes (~3k tokens), checked in CI**
(`scripts/check-current-state.py`). It replaced a 169 KB file on 2026-10-08 (R6 step 3, PM-approved
2026-10-04). **History is not lost**: the full previous file is verbatim in
`docs/internal/architecture/decisions/briefing-current-state-history.log`, with older extractions above it.
Day-by-day progress lives in the omnibus logs (`docs/omnibus-logs/`).

**How to update it** (any agent, per CLAUDE.md's staleness rule): replace a line, don't append under it.
Write over the stale line with today's date and your source. Narrative goes to the omnibus or the history
log, never here. Bump `last_updated` to the newest line's date, or CI fails. Skill: `update-current-state`.

**Not here on purpose**: system internals (use Serena / the code), sprint lists (run
`python3 scripts/sprint-truth.py`), PM's open asks in full (the attention rollup, below).

---

## Now

- **Alpha (live)** *(Docs, 2026-10-30 20:36 PDT, `curl https://alpha.pipermorgan.ai/health`)*: healthy, git_sha `ac5b69f865` (the build the MVP gate passed on, see the MVP gate line). No `ops/alpha-hold.md` on main at 20:36. The 10-29 landing queue that was here (the #2195 ledger, #2042a, #2207, #2209, #2151 status gather) is Lead's to restate, I could not attest it. Earlier: `49e0904c3c` (10-28) carried #2184's milestone pick. It was the first promotion deployed by the pushed digest (#2181, closed): flyctl took `piper-morgan@sha256:8fbc5148…`, and the attested sha matched; *(Arch, 2026-10-21)*: `database: healthy`, `loop_watchdog: running`; serves the boolean quiet shape `{quiet, record_failed_in_window}`, first read by a promote step on run 39683038998 (grant condition 3 served end to end). The 10-21 database outage (#2124, ~11:19-14:13) was a kernel OOM kill of Postgres on a 256 MB VM; memory is now 512 MB. #2085 is an MVP must-close (xian 15:11): the external Postgres restarter, on `ops/restarter` (22e70f91bc) *(CIO, 2026-10-23, `gh issue view 2085` and run 39997651271)*: **#2085 closed 10-23** after test 3: xian stopped Postgres, dispatched and approved the job, and the lease-free restart had alpha's db healthy 10 s later (down 2 min 6 s). *(CIO, 2026-10-24, decisions.log 10-23 15:49 and `gh issue view 2146`)*: **recovery is automatic since #2146 (closed 10-23)**: the Alpha Health Watch dispatches the restarter on a database failure, with no reviewer on `alpha-db`. It's skipped while a hold file exists, and stopped after an earlier automatic restart in 24 h. Test 4c healed in 9 min 15 s with nobody touching it. Since 1f795adff1 a promotion refuses while `ops/alpha-hold.md` exists on main (`ops/README.md`). #2112 stays open on the connected-calendar row (xian). Lead holds promotions Thursday from PA's start mail until both runs end.
  (promotion 1 of 2 today). It carries Monday's finds: #2093, #2091, #2092 (calendar in chat), #2094, #2095 (todos), #2096 (`/feedback`), #2097 (create confirmed by number), #2099 (mint refreshes),
  #2100 (what chat reads), #2102, the DB pool pre-ping, the #2101 bounds and the Alpha Health Watch. Slot 2 (same day, from a green Tests on `1cb1e79dc1`) adds the #2101 thread surface,
  the event-loop watchdog, the #2098 consult, the #2097 list-read confirm, the #2106 refusal line, the Slack session fix and the calendar reads off the loop.
  Open MVP 0 at 20:36 on 10-30 (`gh issue list --milestone MVP --state open` returned nothing: the milestone closed, see the MVP gate line). The list this line carried on 10-18 (13 open, must-close #2101) is history. Served checks: `dev/active/pm-test-card.md`.
  *(CIO, 10-16:)* the **standing promotion grant is in force** since xian confirmed it 10-16 08:10 (decisions.log 10-16;
  `docs/internal/operations/alpha-promotion-standing-grant.md`): Lead promotes when Step 0 is READY, no new migration, 07:00-21:00 PT, with no daily count since 10-20 (xian): the next promotion waits for one green Alpha Health Watch run. From 10-23 (partners invited), a promotion waits for alpha's /health `services.chat_turns_last_30m.quiet` = true and `services.uptime_seconds` ≥ 1800; the promote step refuses otherwise (grant condition 3; count served 10-21 on 8e61423f1a, uptime check in the step from 8cdd2afbeb). `origin/main` builds; the droplet
  and `origin/production` are gone (09-29).
- **Version** *(CIO, 2026-10-08, `git tag`)*: latest tag **v0.8.14.0** ("On Your Clock", 09-23). 0.9.0 is
  reserved for beta.
- **MVP gate** *(PPM, 2026-10-30 17:11 PDT, `gh api …/milestones/5`; alpha `/health` git_sha `ac5b69f865`)*: **PASSED. #1386 and the MVP milestone closed on xian's Go (17:03 via Exec); hard stop Fri 10-30 held.** Alpha and beta serve `ac5b69f865`; no promotion before the first invitations (a new build re-runs rows 2-3). Open: PPM's send-time line check on xian's final letter; xian's tracking test (PPM's audit, pass 1: 14 known items, 13 open + #2225 `fix:not-served`).
  *3 not done (2 In Progress, 1 Product Backlog), 1,284 done. `gh issue list --milestone MVP --state open` also returns 3. On 10-19 it was 7 not done, 1,260 done.)* The MVP milestone **is**
  the beta gate. **Dates: design partners Fri 10-23, hard stop Fri 10-30** (baseline 10-05; slips are logged in
  `docs/internal/planning/beta-gate-standard.md` and only PM moves either date). Read the ledger, not this line, for slips.
- **Engineering focus** *(Lead, 2026-10-20 14:17 PDT, from the 10-20 Lead log)*: the partners' invitation surface on alpha — every served miss from the canonical run and scenario A gets a corpus row or a ruled fix the same day (today: eight landings and five promotions; corpus census 606); the event-loop watchdog stays on permanently; the MVP gate (PPM 13:02) is 8 open, 5 must-close, with #2111 #2112 #2114 #2117 on xian's admission ask via Exec.
  re-run at merge: the seven-branch held batch (#2011, ANALYSIS margin, #1965+#2012, #2009/#2013/#2014 with three migrations, #2010), #2020, #2017,
  #2019's delete cap, #1771 in seven units with the #888 escape-word map, #2026, #2027's dead suggestion lists, #2024, #2029 (+ amber icon), #2008
  formats, #2031, #2030, #2033, #2037, #2035, #2039, #2040, #2041, #2044 (Integrations card "Connected / Not checked yet. Press Test."), lint.yml
  queueing, the CI Concept lines. Three red windows, all test-layer misses of the merge re-run, each fixed within the hour; main green through
  `e4f21e9ca8`. Row E calendar connected on alpha (xian, 18:43). Open: #2043 (OAuth redirect defaults base-derived), the #1852 redirect-secrets
  proposal (xian's hand), #2042 class ladder (PPM/Arch). Held: #1982 (xian), PAT dual-write (#1983/#1995), #2005 paused, `lead-1943-clear-todos-resolver`
  (#2021 lifts), #2023 corpus rows first. Pacing: normal from 10-16 (run-hot ended 10-15 22:00).
- **PM's open asks** *(Exec, 2026-10-09 06:4x PDT)*: on Exec's attention rollup at
  `claude.ai/artifact/719UZ4h1NELjEwWZbDCceT` (its own header line carries the current version; do not pin one here, it was v90 at 04:2x and v95 by 06:4x). Do not copy the list here: it goes stale within hours.
- **Usage** *(CIO, 2026-10-25 10:07 PDT, last row of `dev/heartbeats/usage-per-account.tsv`, read 09:23)*: the pipermorgan.ai
  weekly meter is at **17%**; the next reset is **10-29 21:59 PDT** (10-30 04:59Z). The stop line is **95%**
  of the weekly meter (PM-approved 10-06). Normal pacing.
- **Mail** *(CIO, 2026-10-22)*: v3 (`scripts/mail-send.sh`) for everyone. **Mail v4 pilot** (exec, cio and lead)
  runs through `scripts/mail4.py` in the private `piper-morgan-mail` repo; reviewed 10-22 (delivery 23 of 23 on time; it continues for the three seats, not widened before the 11-05 review; the first inbox read of the day now runs the canary); see
  `docs/internal/operations/mail-v4-pilot.md`. HOST and the other seats aren't in v4, and a v4 send to them is refused. No mail to PM:
  anything for PM goes to Exec (10-03). Since 10-14, mail-send refuses any new file in `mailboxes/xian (ceo)/inbox/`.
- **Ruleset refactor (R6)** *(CIO, 2026-10-20, from git log and CIO logs)*: steps 1 to 5 done. The slim CLAUDE.md landed 10-12
  (c3a7345cd3), after xian's D-D, D-E and D-F (e96a8b281b). Step 6: D-G (fleet CLI upgrade) was overtaken. The `piper-guards` plugin
  review was decided 10-19 (`docs/internal/operations/hooks-registry.md`, "Decided 10-19"): M-1 and M-3 keep both mod rule and settings hook,
  M-2/4/5/6 renew, M-9 stays a prototype; no settings hook retires until the mod has run a week on every seat. It runs on CIO's and CXO's
  seats (CXO since 10-19 14:47); 0.2.1 (M-9 reads `main-ci-status.sh`) runs on both since Pard's 10-20 11:04/11:05 restarts (status lines read `CI main: green`); the plugin source is now the primary checkout. The rest of the cohort follows a quiet week on CXO.
- **Operating model** *(standing)*: every cycling role runs the `duty-cycle-tick` skill. State lives in
  `dev/active/{role}-carry-forward.md`; the session log is the one durable record; push to `origin/main`
  routinely. Cohort liveness: `scripts/duty-cycle-freeze-check.sh`. CI on main: `scripts/main-ci-status.sh`.

## Position (Inchworm)

```
1. ✅ The Great Refactor   2. ✅ CORE   3. ✅ ALPHA testing (v0.8.0 → v0.8.4)
4. 🎯 Complete build of MVP
   4.1–4.3 ✅ B1 Beta Enablers · A20 Alpha round 2 · MUX (Jan 2026)
   4.4 🎯 MVP (M0–M6) ← CURRENT
       ✅ M0 Conversational Glue (Mar 4) · ✅ M1 Foundation (Apr 11) · ✅ M2 Conscious Floor (Jun 3)
       ✅ M3 Artifact Persistence (Jun 14) · ✅ D1 Beta Design Quality (Jun 19) · ✅ RECONNECT WS-1 (Jun 22)
       🎯 the MVP milestone = the beta gate (14 open; design partners 10-23, hard stop 10-30) · ⬜ M4 Trust + Learning · ⬜ M5 Distribution
5. Beta testing on 0.9    6. Launch 1.0
```
*(Milestone detail as of the 09-28 snapshot; Lead or PPM to correct any line that has moved.)*

## Where to look

| Need | Source |
|---|---|
| What happened on a given day | `docs/omnibus-logs/YYYY-MM-DD-omnibus-log.md` |
| Sprint / MVP membership | `python3 scripts/sprint-truth.py` (the project board is the source of truth) |
| PM's pending decisions | Exec's attention rollup (link above) |
| Roadmap, vision | `docs/internal/planning/roadmap/roadmap.md`, `docs/internal/planning/current/vision.md` |
| Decisions | `docs/internal/architecture/adrs/`, `docs/internal/product/pdr/`, `docs/internal/architecture/decisions/decisions.log` |
| Roles and lanes | `docs/briefing/ROSTER.md`, `mailboxes/DIRECTORY.md` |
| Terms (Plugin, MCPB, Connector, Cowork…) | `knowledge/piper-morgan-glossary-v1.1.md` |
| Earlier versions of this page | `docs/internal/architecture/decisions/briefing-current-state-history.log` |
