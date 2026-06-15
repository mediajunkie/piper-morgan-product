# CXO Migration Handoff — paste into OLD-account CXO session

**Author**: CIO (supervising the wave) · **Date**: 2026-06-15 · **For**: PM to paste into the old-account CXO session when ready to close it. Same shape as the Docs/PA/HOST/Comms handoffs. **NB: CXO is ACTIVE this morning (has a 2026-06-15 session log), so this is pasted into a LIVE mid-session — capture in-flight threads before you close.**

---

CXO — migration handoff. PM is closing this session and opening a fresh Code session on DinP (xian@designinproduct.com), on **Sonnet** (your tier per the role-model map — a model change from your current Opus; bundled with the account move, like the others). You don't supervise others (CIO does). You're mid-session, so the priority is **capturing your in-flight state cleanly** before close. Steps:

1. **Capture in-flight threads in your continuity FIRST** (you're live — don't lose the open work). CXO's state lives in the **session log** (there's no `cxo-carry-forward.md`). Write a day-close to today's session log that captures, in particular:
   - **#1236 Radar / "ship all 4 Layer-2 entity types for beta"** — the RadarEntity contract you just froze (facets = your design: `lifecycle_state={label,tone}`, `provenance={status,source?}`; People facets per #1217+HOST). Record that the contract is **frozen + sent to Lead+PPM**, and the critical-path flag (People/PPM-model + WorkItem #1233 are the long poles).
   - **#1164 privacy-toggle placement** — your answer (session-level switch on the provenance pipeline; effect visible in Radar) so new-CXO doesn't re-open it.
   - The **Radar entities-surfacing mockup** (`dev/active/radar-entities-surfacing-mockup-2026-06-14.html`) — the binding artifact + #1090 handoff status.
   - **HOST people-entity inputs** (auditability + BYOC consent-asymmetry) folded into the People-entity contract; **#1217 collegiality** state.
   - Queued/standing: #313 (≤2-organizers), #048 (Web/public-surface), #1169–1173 design-floor specs (delivered), #950 floor-quality watch, #992 ethics-decline voice oversight.

2. **Close your log (single-surface, skill v1.8)**: write the day-close to your **session log** (the durable record) — day-arc + memory-eval 3-bucket + sign-off checklist + the `<!-- DAY-CLOSED: 2026-06-15 -->` marker. (The cycle log is optional scratch now — no formal close needed. The session log is THE record.)

3. **CronDelete the active duty-cycle cron** (`CronList` to find its id — was `2d04f16f`; today's log notes it was CronDeleted at fire-start and re-armed, so delete whatever is currently live). The new session arms a fresh CronCreate cron (see the bootstrap — the scheduled-task approach was tried + suspended 6/14).

4. **Commit + push EVERYTHING to `origin/main`** — run + read each:
   ```bash
   git status                    # clean
   git log --oneline @{u}..HEAD  # empty (pushed)
   git log --oneline main..HEAD  # empty — or merge to main now
   ```
   CXO especially: you're on a **Model-A `claude/cxo-cycle`-style branch** (`claude/peaceful-almeida-32a5f5`) — make sure the mockup + design-floor specs + today's session log are all on `origin/main`, not stranded on that branch.

5. **Report back**: continuity recap (1-line) + confirmation the #1236 RadarEntity-contract state + #1164 answer are captured in the session log + crons clear (`CronList`) + the **actual output** of `git log --oneline main..HEAD` (empty is correct). Then stand by for PM to close + reopen.
