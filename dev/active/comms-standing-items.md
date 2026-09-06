# Comms standing items

**Purpose**: persistent (across-days) Comms-side task list — items that aren't tied to a specific blog post or pubDate but need surfacing/advancing as cycle fires advance. Lives across days; not a per-day artifact. (Per-day work goes in the dated session log under `dev/2026/MM/DD/`.)

**Dating convention (effective 2026-08-31, CIO broadcast, ratified into CLAUDE.md)**: every new row added to this file from now on carries the date it was added — write it inline next to the row, diary-style. No retroactive dating of existing rows expected. Feeds `scripts/aging-standing-items.sh` (flags rows >21 days old with no stated blocker).

**Last refreshed**: 2026-08-31, following CIO's cohort-wide standing-items audit (`dev/active/cohort-standing-items-audit-2026-08-31.md`). CIO cross-checked every row below "The Ritual Becomes a Skill" against the live editorial calendar and confirmed the file's own staleness self-admission held — everything CIO could verify as published/resolved has been removed from this table (the closure detail lives in the session logs and git history that already recorded it, not duplicated here). One item CIO flagged as a real miss — a mechanical "awaiting direction" phrase-match that was actually stale — got a full re-investigation below, not just a re-flag.

---

## Active

| Topic | State | Owner of next move | Notes |
|---|---|---|---|
| **Series structure — era split + blog-index featuring** | Raised by PM 2026-08-02, for a Web discussion. My POV recorded in `docs/internal/planning/comms/upcoming-beats-plan.html`: Era 2 has absorbed 107+ posts over 6+ months and multiple working models — overdue for a split at the late-July move to the always-on host. On featuring: couldn't verify the rendered blog-index page (client-rendered) so no layout opinion, but the editorial case is real since narratives skip LinkedIn and Ships skip Medium — some readers only ever meet a post on-site. CIO's 08-31 audit confirmed this is still genuinely open, not neglect — it wouldn't show up in the calendar either way. **2026-09-06 note**: a directly-related but distinct issue (website#39 — 288 posts miscategorized/unclustered in the newer 7-era taxonomy, PM caught the site's nav looking worse than before the reorg) got fully root-caused and resolved as a data question this morning (era assignment is 100% mechanical from publish date, not judgment-based as Web's issue had assumed) — full mapping committed to `dev/active/era-backfill-2026-09-06.csv`, handed to Web to execute. That's the *data-correctness* half of era clustering; this row's *structural* question (splitting Era 2, blog-index featuring) is still separately open. | PM / Web | |
| **ChicagoCamps / Leadership By Design talk — Sept 17, 2026** | PM speaking Thu Sept 17, Session 2, 12:45p Central, 30 min incl. Q&A. Full script (3 acts matching the sent abstract) + slide plan delivered 2026-08-29 at `dev/2026/08/29/chicagocamps-talk-2026-09-17.md`. 2 existing Rosenverse-archive images reusable as-is; 4-5 new cartoon prompts written for PM to generate. PM reviewing in the week of 2026-08-31 (after an overnight trip). Russ mentioned a brief dry run ~week of Sep 1-5 — watch for that follow-up. | PM (review/adapt script, generate slide images) | |

## Cross-cutting PM topics (verify still alive at next surface; ≥30 days stale flagged)

CIO's 08-31 audit confirmed these are genuinely "awaiting PM direction by nature" — not neglect, just old even by their own self-flagging standard.

- Fresher style/concision/jargon feedback (PM May 10 — likely superseded by subsequent rubric work)
- Conference invitation (PM Apr 24; details never shared)
- "Code-enabled workflow" conversation (PM Apr 24 deferred)
- Larger Comms remit review (PM Apr 24 Step 4)
- Filing system review of comms tree (PM Apr 24 — defer until use-experience accrues)

---

*Edit conventions: any role can read; only Comms hand-edits. Per methodology-36, prefer derived views (the 3 scripts in `scripts/`) over hand-maintained tracking where the calendar/code is the source of truth. Closed-item history lives in dated session logs (`dev/2026/MM/DD/`) and git — not duplicated here anymore as of the 2026-08-31 cleanup.*
