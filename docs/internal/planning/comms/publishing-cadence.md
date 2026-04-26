# Publishing Cadence

**Owner**: Communications (with Docs custodianship of the editorial calendar CSV)
**Last Updated**: 2026-04-26
**Sprint week**: Friday–Thursday

---

## Weekly Slot Map

| Day | Slot | Surfaces | Notes |
|-----|------|----------|-------|
| **Friday** | (none) | — | No post |
| **Saturday** | Insight | Blog + Medium + LinkedIn newsletter | Drawn from any point in the narrative |
| **Sunday** | Insight | Blog + Medium + LinkedIn newsletter | Drawn from any point in the narrative |
| **Monday** | (none) | — | No post |
| **Tuesday** | Narrative | Medium only (NOT LinkedIn) | Next article in development narrative |
| **Wednesday** | Weekly Ship | LinkedIn newsletter only (NOT blog, NOT Medium) | Posted to Shipping News section; covers the preceding Fri–Thu week |
| **Thursday** | Narrative | Medium only (NOT LinkedIn) | Next article in development narrative |

LinkedIn readers asked for lower volume, which is why narratives skip LinkedIn and ships skip Medium.

---

## Narrative Ordering Rule

> "As we write them, we add them to the calendar in the upcoming slots."

Narratives publish in chronological order of the **project work** they describe (the `workDate` / `endWorkDate` columns in the calendar), not in writing order. Tue and Thu slots are filled by walking the narrative backlog forward by `workDate`.

Implication: a narrative drafted today about work that happened two weeks ago goes in front of a narrative drafted yesterday about work that happened three days ago.

---

## Weekly Ship Rule

A Weekly Ship publishes Wednesday and covers the Fri–Thu week that ended six days earlier (the preceding sprint week).

| Ship | Covers | Publishes |
|------|--------|-----------|
| #038 | Fri Apr 3 – Thu Apr 9 | Wed Apr 15 |
| #039 | Fri Apr 10 – Thu Apr 16 | Wed Apr 22 |
| #040 | Fri Apr 17 – Thu Apr 23 | Wed Apr 29 |
| #041 | Fri Apr 24 – Thu Apr 30 | Wed May 6 |

Past ships (pre-Apr 2026) sometimes published to blog + LinkedIn. Current cadence (post-Apr 2026 reset) is **LinkedIn newsletter only** for ships, with the blog hosting at `pipermorgan.ai/shipping-news/...` for archival.

---

## Calendar Audit Procedure

When checking the editorial calendar for drift:

1. Pull rows from `docs/internal/planning/comms/editorial-calendar.csv` whose `pubDate` falls in the upcoming window (default: next 30 days).
2. For each row, check that the day-of-week of `pubDate` matches the slot type per the table above.
3. Flag any drift:
   - Narrative on Wed/Fri/Sat/Sun/Mon → wrong day
   - Insight on Tue/Wed/Thu/Fri → wrong day
   - Ship not on Wed → wrong day
4. When fixing drift, walk the narrative backlog chronologically (by `workDate`) and reassign Tue/Thu slots in order.

---

## Editorial Calendar Schema (relevant columns)

`title, theme, status, workDate, endWorkDate, pubDate, mediumURL, liPubDate, linkedinURL, canonicalSite, blogURL, blogPath, cartoon, chatDate, draftPath, notes, altText, caption`

- `theme` values include: `building` (narrative), `insight`, `ship`
- `status` lifecycle: `queued` → `drafted` → `published`
- For narratives (Tue/Thu): expect `mediumURL` populated, `linkedinURL` empty
- For ships (Wed): expect `linkedinURL` populated, `mediumURL` empty
- For insights (Sat/Sun): expect both `mediumURL` and `linkedinURL` populated, plus `blogURL`

---

## Why this document exists

PM (Apr 26 2026) explained the cadence after Docs misidentified Wed Apr 29 as a Tuesday narrative slot during a calendar audit, surfacing existing drift in two queued narratives ("The Deeper Why" had been placed on Wed Apr 29; "The Floor Comes Alive" on Fri May 1). The drift originated from filling slots without checking day-of-week against slot type. Recording the cadence in-repo prevents the same loss next time.
