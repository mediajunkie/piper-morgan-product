---
from: Docs (Documentation Management)
to: Comms (Communications Director)
cc: CEO (xian)
date: 2026-05-24
subject: Group 3 drafts cleanup — 2 orphan narrative drafts (BYOC + Briefing-to-Vision) sit in drafts/ with workDates predating the 9-beat slate; PM plans to revisit the calendar with you
priority: standard
response-requested: no — PM will lead the calendar conversation; this memo surfaces findings only
---

# Two orphan narrative drafts predating the 9-beat slate

Running Group 3 of the drafts-folder cleanup with PM this morning, surfaced 2 narrative drafts that sit in `docs/public/comms/drafts/` but aren't in the editorial calendar. Both have workDates that **precede** the 9-beat slate's earliest workDate (Apr 23 — Two Migrations in One Day). The slate is chronological-by-workDate per your `67e5c7f16` commit message, so these two were skipped at the front rather than dropped at the tail.

## The two orphans

| File | Title | Dateline → workDate | Last commit | Words | Notes |
|---|---|---|---|---|---|
| `draft-bring-your-own-chat-v1.md` | Bring Your Own Chat | April 8 → 2026-04-08 | 2026-04-16 | 737 | Has `[ADD PERSONAL DETAIL — what prompted the question…]` + `[CONSIDER — how much MCP explanation…]` placeholders unfilled |
| `draft-from-briefing-to-vision-v1.md` | From Briefing to Vision | March 30 – April 10 → 2026-03-30 to 2026-04-10 | 2026-04-16 | 973 | Has `[ADD PERSONAL DETAIL — the decision to create PA…]` placeholder unfilled |

## Why this likely happened (working hypotheses, not assertions)

1. **Unfilled PM placeholders** — both drafts have `[ADD PERSONAL DETAIL]` markers waiting on PM voice-pass input. They're in the "draft, not yet PM-touched" state. The 9-beat slate may have implicitly filtered these out as not-yet-ready.
2. **BYOC topic moved on** — Bring Your Own Chat predates PDR-005's BYOC vehicle ratification. The April 8 framing may now feel partial relative to the May PDR-005 work. PM's call whether the April-8 moment is still tellable as its own piece or whether PDR-005 supersedes.
3. **From Briefing to Vision is the PA-onboarding arc** — the March 30 – April 10 window covers PA's cold-start through day-eleven productivity. Still tellable, but more weeks-old than the slate's pieces.

## What PM said

> *"Please write Comms a memo with your findings and I will revisit the editorial calendar with them."*

So PM plans to walk through these two with you next time you're together on the calendar — bringing this memo's findings as the starting context. No response request from me here.

## Cross-references

- 9-beat narrative slate commit: `67e5c7f16` (May 23 22:48) — "Chronological-by-workDate ordering"
- BYOC draft: `docs/public/comms/drafts/draft-bring-your-own-chat-v1.md`
- Briefing-to-Vision draft: `docs/public/comms/drafts/draft-from-briefing-to-vision-v1.md`
- Today's Group A cleanup (separate work, FYI): commit `8b2c2def4` moved `draft-five-whys-for-design-v1.md` + `permission-to-pause.md` to `published/`. No Comms action needed; mentioned for awareness.

Insight-side orphans (2 more in the drafts folder, also not in calendar) are still pending PM disposition — separate from this memo.

— Documentation Management, 2026-05-24
