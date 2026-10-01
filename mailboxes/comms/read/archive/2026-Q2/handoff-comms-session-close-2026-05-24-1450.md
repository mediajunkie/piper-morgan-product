---
from: Comms (Communications Director, May 24 session ~10:50 AM – ~2:50 PM PT)
to: Comms (next session)
cc: CEO (xian)
date: 2026-05-24
subject: Comms session handoff — May 24 close-out + Pending list with priority ordering
priority: STANDARD — read at session start, then move to read/ once you've absorbed the carry-forward state
response-requested: none — informational handoff
---

# Comms session handoff — May 24, 2026

Long session, substantive output, accumulated state worth carrying cleanly. This memo is the institutional-memory layer between today's session and the next one. Read first, then triage the rest of the inbox.

## What landed today (chronological)

- **MUX/UI Round 2 voice-pass cluster — Surface 7, Surface 2, Surface 4** all completed Step 2 with handoff memos to CXO + cohort distribution. Step 2.5 addendum on Surface 2 (parenthetical tightening per PM 11:40). Branch `claude/comms-mux-voice-pass`, several commits. CXO Step 3 cluster review **landed in inbox today (commit `3f70c7ee7`) — 3 flags folded, 1 deferred, 2 resolved, cluster locks at v0.2.** Pending your triage.
- **Six insight drafts** (pipeline-extension per PM "running ahead" directive) on branch `claude/comms-mux-voice-pass`:
  1. *Climbing Higher When the Platform Laps You* (commit `39c0106db`) → scheduled Sat Jul 4
  2. *The Practice That Got Retired* (`1c075a7d8`) → Sun Jul 5
  3. *When the Documentation Drifts* (`5a4d4ee48`) → Sat Jul 11
  4. *The Server Crashed Mid-Draft* (`bef22737f`) → Sun Jul 12
  5. *"Mechanical First, Then Read"* (`b25708093`) → Sat Jul 18
  6. *What Staff Reports Don't Show* (`8f1e9f9f7`) → Sun Jul 19
- **Editorial calendar updated** with 6 new insight rows + handoff memos for all three MUX surfaces distributed on main.
- **Layer A of orphan-prevention framework landed** — `draft-blog-post` skill v1.1 (commit `959e5dca6`) now mandates calendar row at draft creation (status=`drafted`).
- **Memory pin sharpened** — `feedback_addressing_hold_pattern_is_wrong_move_to_read_immediately.md` operationalizes *"used"* as *"downstream artifact exists,"* with annotation-in-inbox rule for active-wait state.
- **Visibility-loss pattern memo filed to CIO (cc HOST + PA + CEO)** as cross-role process-improvement seed.
- **Ship #044 workstream review filed** (`workstream-044-comms-2026-05-24.md`) — drop-dead was Tue May 26 EOD; filed Sun May 24 early. Now in read/.

## Pending in priority order

### High priority (active work, no blocking dependency)

1. **CXO MUX Step 3 cluster review triage.** Just-landed memo in your inbox: `memo-cxo-to-comms-cc-arch-ppm-lead-pa-ceo-exec-mux-step-3-cluster-review-2026-05-24.md`. Cluster locks at v0.2 — 3 flags folded into the docs, 1 deferred, 2 resolved. Your job: read, confirm any final voice work or absorb the resolutions, then move to read/ once you've acted. Step 4 (iterate-if-needed) may be reached or this may be the cluster done.

2. **Framework Layers B → C → D** (PM ratified sequential implementation today):
   - **B**: Retire `dev/active/comms-open-topics.md` as hand-maintained; derive its drafted-and-awaiting view from a calendar query (status=`drafted`). Mechanism that eliminates tracker staleness.
   - **C**: Inventory query as required first step in pipeline-planning. Bake into `draft-blog-post` skill or a separate planning-skill.
   - **D**: Periodic reconciliation — `docs/public/comms/drafts/` filesystem state ↔ calendar `draftPath` column. Catch-net under A/B/C.
   - PM said "one at a time, verifying each. Do all in sequence." Layer A is verified (skill v1.1 landed). Continue with B.

3. **Orphan backfill** (after Layers B/C/D land). Four pieces drafted earlier but never scheduled:
   - *From Briefing to Vision* — narrative, workDate Mar 30 – Apr 10 → **Thu May 28** (per PM 2:19 PM). 3 ADD + 1 CONSIDER placeholders pending PM voice-pass.
   - *Bring Your Own Chat* — narrative, workDate Apr 8 → **Tue Jun 2** (per PM 2:19 PM). 3 ADD + 1 CONSIDER placeholders. **PM ratified keep** ("narrating a core idea that may not have been articulated this way by others yet").
   - *The Meta-Observation Pattern* — insight, workDate Apr 18–21. Placement by theme + editorial judgment (insights are NOT chronological per PM 2:19 PM). Has in-body `[CONSIDER — IMPORTANT, PER COMMS FLAG]` placeholder questioning whether to ship given self-observation arc density. PM ratified keep.
   - *From Abstraction to Worked Example* — insight, workDate Apr 22. Placement by theme + editorial judgment. PM ratified keep.
   - **Inserting the two narratives Thu 5/28 + Tue 6/2 requires shifting Beats 2–9 forward by 2 slots** — see today's session log for the full table. Beat 1 (Tue May 26, *Two Migrations in One Day*) is locked because today's footer teased it.

### Medium priority (waits on external signals)

4. **Retroactive memory-terminology sweep on Surfaces 7 + 2.** PM-ratified terminology norm today (11:40 AM): user-facing prose uses *"what I remember about you"* / *"long-term memory"*; *"working memory"* stays as internal architectural term. Surface 4 voice-pass applied the norm going forward. Retroactive sweep on Surfaces 7 + 2 awaits PM full-leadership cohort conferral (PM said this was happening today; check session log for outcome).

5. **PM voice-pass cycle on the 9-beat narrative slate** (Beats 1–9 on branch `claude/comms-mux-voice-pass`). Not Comms-driven; PM cadence. When PM picks up a beat for voice-pass, that's when it happens.

### Low priority / parked

6. **#7 Forecast-vs-Outcome insight candidate** — held per PM direction (too fresh; today's data point is the only instance so far). May ripen with more cycles.
7. **Layer-E candidate** — bake the move-to-read downstream-artifact discipline more explicitly into a skill update (beyond the memory pin landed today). Mentioned in passing; not yet ratified as a separate task.

## Today's lessons worth carrying

- **Premature move-to-read = visibility loss.** The Ship #044 kickoff incident: read content does not equal used content. Used = downstream artifact exists. Memory pin updated today operationalizes this. Apply going forward.
- **Hand-maintained trackers go stale.** The orphan-drafts incident: `comms-open-topics.md` had the right info on May 10 but wasn't consulted during May 17–23 planning. Framework Layers A–D address this structurally; in the meantime, treat the tracker as a starting point, not ground truth.
- **PM-ratified terminology norm (May 24 11:40):** user-facing = *"what I remember about you"* / *"long-term memory"*; internal = *"working memory"*. Apply at draft time.
- **Narratives chronological; insights themed.** PM clarification today (2:19 PM). Don't over-apply chronological frame to insights.
- **Inventory drafts/ folder before planning new work.** This is the process gap today's framework addresses. Until D is live, do it manually at the start of any planning session.

## Open process decisions awaiting PM ratification

- **Layer B scope** — exact mechanism for deriving open-topics view from calendar query. Implementation detail; PM may want to ratify the shape before I build.
- **Cohort-wide adoption of move-to-read sharpening** — CIO memo filed today proposes this; CIO/HOST/PA responses pending.
- **Orphan backfill calendar entries** — PM ratified the shift (Thu 5/28 + Tue 6/2 for narratives, themed placement for insights) but I haven't yet committed the calendar changes. Do this after Layer D lands so the new mechanics serve as the worked example.

## Where artifacts live

| Artifact | Location | Branch |
|---|---|---|
| MUX voice-pass drafts (Surfaces 7, 2, 4) | `docs/internal/design/mux/` | `claude/comms-mux-voice-pass` (merged to main via CXO's Step 3 review commit `228403fb2`) |
| 6 insight drafts | `docs/public/comms/drafts/` | `claude/comms-mux-voice-pass` (not yet on main) |
| All handoff memos for surfaces + this handoff + workstream review + CIO process memo | `mailboxes/` | main |
| Layer A skill update | `.claude/skills/draft-blog-post/SKILL.md` | main, commit `959e5dca6` |
| Memory pin update | `~/.claude/projects/.../memory/feedback_addressing_hold_pattern_is_wrong_move_to_read_immediately.md` | (user memory, not repo) |
| Today's session log | `dev/2026/05/24/2026-05-24-1050-comms-code-opus-log.md` | `claude/comms-mux-voice-pass` |
| Editorial calendar (with 6 new insight rows; ratified pubDates Jul 4–19) | `docs/internal/planning/comms/editorial-calendar.csv` | main, commit `6cc8a8fa3` |

## Session-start checklist for the next Comms session

1. Read this handoff memo first (you're doing that now). Then move it to `comms/read/` once you've absorbed the carry-forward state — the downstream artifact is this memo being read + the work resuming from the Pending list above, so the move-to-read criterion is satisfied as soon as you've internalized it.
2. Read the CXO Step 3 cluster review memo (next in inbox). Triage per priority 1.
3. Check `dev/active/comms-open-topics.md` for any stale items beyond what this memo names. (Note: Layer B will deprecate this file once implemented.)
4. Verify branch state: `git branch --show-current` should show `claude/comms-mux-voice-pass` if you're picking up the insight/narrative work; `main` if you're doing mail-discipline-only operations.
5. Start the session log per `create-session-log` skill if today's date is past May 24.

— Comms (Communications Director, May 24 session)
*2:50 PM PT, May 24, 2026*
