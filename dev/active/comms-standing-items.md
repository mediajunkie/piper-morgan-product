# Comms standing items

**Purpose**: persistent (across-days) Comms-side task list — items that aren't tied to a specific blog post or pubDate but need surfacing/advancing as cycle fires advance. Lives across days; not a per-day artifact. (Per-day work goes in the dated session log under `dev/2026/MM/DD/`.)

**Dating convention (effective 2026-08-31, CIO broadcast, ratified into CLAUDE.md)**: every new row added to this file from now on carries the date it was added — write it inline next to the row, diary-style. No retroactive dating of existing rows expected. Feeds `scripts/aging-standing-items.sh` (flags rows >21 days old with no stated blocker).

**Last refreshed**: 2026-08-31, following CIO's cohort-wide standing-items audit (`dev/2026/08/31/cohort-standing-items-audit-2026-08-31.md` — archived from `dev/active/` 2026-09-07 monthly housekeeping). CIO cross-checked every row below "The Ritual Becomes a Skill" against the live editorial calendar and confirmed the file's own staleness self-admission held — everything CIO could verify as published/resolved has been removed from this table (the closure detail lives in the session logs and git history that already recorded it, not duplicated here). One item CIO flagged as a real miss — a mechanical "awaiting direction" phrase-match that was actually stale — got a full re-investigation below, not just a re-flag.

---

## Active

| Topic | State | Owner of next move | Notes |
|---|---|---|---|
| **Series structure — era split + blog-index featuring** | Raised by PM 2026-08-02, for a Web discussion. My POV recorded in `docs/internal/planning/comms/upcoming-beats-plan.html`: Era 2 has absorbed 107+ posts over 6+ months and multiple working models — overdue for a split at the late-July move to the always-on host. On featuring: couldn't verify the rendered blog-index page (client-rendered) so no layout opinion, but the editorial case is real since narratives skip LinkedIn and Ships skip Medium — some readers only ever meet a post on-site. CIO's 08-31 audit confirmed this is still genuinely open, not neglect — it wouldn't show up in the calendar either way. **2026-09-06, CLOSED same day**: a directly-related but distinct issue (website#39 — 288 posts miscategorized/unclustered in the newer 7-era taxonomy, PM caught the site's nav looking worse than before the reorg) got fully root-caused, mapped, and shipped by Web same-day (era assignment is 100% mechanical from publish date, not judgment-based as Web's original issue had assumed; commit `1bc123f`, Vercel-deployed, verified live). Web found one more thing my date-based mapping couldn't see — a genuine orphan duplicate JSON entry (`weekly-ship-44`) — filed separately as website#41, confirmed clean on the calendar side (only one row exists, already correctly clustered), and closed same-fire by Web (root cause: a same-day slug-fix commit that added a corrected entry instead of updating in place; removed, verified, shipped `441ef10`). Both #39 and #41 fully closed. That closes the *data-correctness* half of era clustering entirely. This row's *structural* question (splitting Era 2, blog-index featuring) is still separately open — website#39/#41 didn't touch it. | PM / Web | |
| **ChicagoCamps / Leadership By Design talk — Sept 17, 2026 (date now PASSED)** | PM spoke (scheduled) Thu Sept 17, Session 2, 12:45p Central, 30 min incl. Q&A. Full script (3 acts matching the sent abstract) + slide plan delivered 2026-08-29 at `dev/2026/08/29/chicagocamps-talk-2026-09-17.md`. **2026-09-12: PM landed the actual slide deck** — `..."curious-fail-leadership-design-chicago-camps-2026.pdf"` plus 2 new cartoon images (`blog-eras.png`, `first-time.png`) committed directly to `docs/public/comms/drafts/`, no accompanying memo. Not yet reviewed by Comms; landed via a raw commit (not the admin-UI edit pattern), so treated as a drop rather than an explicit ask. **2026-09-19: re-verified — no mention of the talk in any 09-17/18/19 session log; outcome unconfirmed.** The talk date has passed; this row's "confirm final" framing is stale pre-event phrasing. Next move is to ask PM how it went, not to keep waiting on a pre-talk confirmation. | PM (how did it go?) / Comms (review PDF, maybe fold into a post) | 2026-09-19 (re-verified stale) |

## Recurring practices (cadence-driven, not one-off — tracked with a rolling Next due)

### Biweekly editorial mining pass — every other Friday

**Filed**: 2026-09-23 (PM-ratified in conversation: "I like your proposal from above. Please do it.")
**Next due**: 2026-09-25 (Friday) — **first pass is a catch-up**, not steady-state
**Last run**: never (first pass pending)
**Cadence after first pass**: every 14 days on Friday — 2026-10-09, 2026-10-23, 2026-11-06, …

**What it is**: PM + Comms collaborative editorial-calendar planning, with the prep automated in
Comms' duty cycle. Comms surveys the sprint weeks closed since the last pass for narrative-beat
candidates (and insight-pairing candidates), then brings a written recommendations report to PM
for a joint decision. **Comms does not auto-schedule anything into the calendar from this pass** —
the recommendations are input to a conversation, not a commit. PM's framing: "reviewing the past
several week-sprints and mining them for stories."

**Why it exists**: ad-hoc surveys have twice missed real material (Aug 21-26, Aug 10-18 — see
`continue-narrative` v1.2's own history), and at the time of filing, narrative-beat coverage
stopped at workDate Aug 29 with ~3.5 sprint weeks (Aug 30 → Sept 23) never surveyed at all. A
cadence prevents the backlog from forming rather than draining it after PM notices.

**How to run it** (the trigger is checked at the Friday START fire — this file is already read in
the duty-cycle task loop, so it can't be silently skipped):
1. On a Friday START fire, compare today against **Next due** above. If today ≥ Next due, the pass
   is due this fire — drain it, don't defer it to a later fire.
2. Scope = every sprint week (Fri→Thu) closed since Last run **whose Thursday omnibus exists on
   disk** (`docs/omnibus-logs/YYYY-MM-DD-omnibus-log.md` for that Thursday). This is a mechanical
   check, not a timing guess: Docs synthesizes Thursday's omnibus on Friday morning, so at a
   Friday 06:12 START the just-closed week may not be surveyable yet — if its omnibus isn't there,
   that week rolls to the next pass rather than getting a half-sourced survey. **Front-date
   correction, caught at the first pass (09-25)**: the "front" (Step 1 of `continue-narrative`) is
   the beat's full covered span (`workDate` through `endWorkDate`), not `workDate` alone — the
   original text here said coverage ended Aug 29, but the actual front (per the last beat's
   `endWorkDate`) is **Aug 31**. Scope starts at front+1.
3. Run the survey through `continue-narrative` v1.2's **per-day ledger discipline** — every calendar
   day in scope gets an explicit `candidate`/`thin` verdict, embedded in the session log, validated
   by `scripts/check-narrative-survey-coverage.py`. Not an aggregate "rich everywhere" skim — that's
   the exact shape that missed material twice.
4. Deliverable: a written recommendations report — per-day verdicts, proposed beats with working
   titles and A-plot framing, suggested insight pairings, suggested calendar slotting — sent to PM's
   inbox (cc nobody unless PM says otherwise) and flagged in chat if PM is around.
5. Update **Last run** and roll **Next due** forward 14 days, in the same commit as the report.

**Mechanism the trigger rides on**: nothing new — the duty-cycle task loop already reads this file
every fire. The only addition is the date comparison in step 1, which the Friday START fire owns.

## Cross-cutting PM topics (verify still alive at next surface; ≥30 days stale flagged)

CIO's 08-31 audit confirmed these are genuinely "awaiting PM direction by nature" — not neglect, just old even by their own self-flagging standard.

- Fresher style/concision/jargon feedback (PM May 10 — likely superseded by subsequent rubric work)
- Conference invitation (PM Apr 24; details never shared)
- "Code-enabled workflow" conversation (PM Apr 24 deferred)
- Larger Comms remit review (PM Apr 24 Step 4)
- Filing system review of comms tree (PM Apr 24 — defer until use-experience accrues)

---

*Edit conventions: any role can read; only Comms hand-edits. Per methodology-36, prefer derived views (the 3 scripts in `scripts/`) over hand-maintained tracking where the calendar/code is the source of truth. Closed-item history lives in dated session logs (`dev/2026/MM/DD/`) and git — not duplicated here anymore as of the 2026-08-31 cleanup.*
