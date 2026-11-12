---
type: briefing
title: BRIEFING-CURRENT-STATE.md - Where We Are Right Now
valid_from: "2025-09-30"
last_updated: 2026-11-11
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

- **Beta (live; alpha 301s to beta.pipermorgan.ai since 11-05 12:47, #2282)** *(Arch, 2026-11-11 06:28 PST, `curl https://beta.pipermorgan.ai/health`)*: healthy, version 0.9.0.0, git_sha `c425fd242f` (promoted 11-10 18:58; carries #2328: a completion whose only target is a pronoun asks which one, armed, and completes nothing). Older shas: `briefing-current-state-history.log` (Arch 11-07); 11-09 ended on 727dd31596, and 11-10 went 6dc21c2ca8, then c425fd242f.
  (promotion 1 of 2 today). It carries Monday's finds: #2093, #2091, #2092 (calendar in chat), #2094, #2095 (todos), #2096 (`/feedback`), #2097 (create confirmed by number), #2099 (mint refreshes),
  #2100 (what chat reads), #2102, the DB pool pre-ping, the #2101 bounds and the Alpha Health Watch. Slot 2 (same day, from a green Tests on `1cb1e79dc1`) adds the #2101 thread surface,
  the event-loop watchdog, the #2098 consult, the #2097 list-read confirm, the #2106 refusal line, the Slack session fix and the calendar reads off the loop.
  Open MVP 0 at 20:36 on 10-30 (`gh issue list --milestone MVP --state open` returned nothing: the milestone closed, see the MVP gate line). The list this line carried on 10-18 (13 open, must-close #2101) is history. Served checks: `dev/active/pm-test-card.md`.
  *(CIO, 10-16:)* the **standing promotion grant is in force** since xian confirmed it 10-16 08:10 (decisions.log 10-16;
  `docs/internal/operations/alpha-promotion-standing-grant.md`): Lead promotes when Step 0 is READY, no new migration, 07:00-21:00 PT, with no daily count since 10-20 (xian): the next promotion waits for one green Alpha Health Watch run. From 10-23 (partners invited), a promotion waits for alpha's /health `services.chat_turns_last_30m.quiet` = true and `services.uptime_seconds` ≥ 1800; the promote step refuses otherwise (grant condition 3; count served 10-21 on 8e61423f1a, uptime check in the step from 8cdd2afbeb). `origin/main` builds; the droplet
  and `origin/production` are gone (09-29).
- **Version** *(Docs, 2026-11-01 11:10 PT, `git ls-remote --tags origin`, `gh release list` and Lead's served reads)*: latest tag **v0.9.0.0** at `c44dd081cb74`, the private beta, served on alpha and beta. Prior tag v0.8.14.0 ("On Your Clock", 09-23). Release page: https://github.com/mediajunkie/piper-morgan-product/releases/tag/v0.9.0.0 (xian ran `gh release create`, 2026-11-01 11:10 PST, Latest); notes are `docs/releases/RELEASE-NOTES-v0.9.0.0.md`. 1.0.0.0 is the production release, cut when the Production milestone closes.
- **MVP gate** *(PPM, 2026-10-30 17:11 PDT, `gh api …/milestones/5`)*: **PASSED; the MVP milestone closed on xian's Go.** The gate's ledger is `docs/internal/planning/beta-gate-standard.md`. History moved to `briefing-current-state-history.log` 11-05.
- **Invite hold** *(PPM, 2026-11-11 06:34 PST, `gh issue view` on #2261, #2282 and #2292; PDR-008)*: **no invitations of any kind** until the six conditions in `docs/internal/product/pdr/PDR-008-invite-readiness.md` are met, then xian's word. PDR-008 was accepted 11-07 (xian yes to P1–P3 by 08:03): only xian admits a new condition; a tenancy P0 after the lift re-holds unsent invitations; and "any" includes waiting-list confirmations that grant access, and re-invites. Met: #1551, #2283, #2178. Open: #2261 (GitHub scope; #2174 passed 11-11 18:52, so the leg is D3, built as #2342, which waits first on xian registering the published GitHub App; Exec 11-12 06:03 from PPM's #2261 comment and 19:11 memo), #2282 (one canonical host; the browser row waits on xian's word for Web's sign-in check) and #2292 (SPF, DKIM, DMARC; xian's records). PPM sends Exec the lift-readiness memo when all six are met.
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
