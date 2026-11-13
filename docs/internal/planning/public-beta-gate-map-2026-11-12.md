# Public-beta gate: sprint-by-sprint map (2026-11-12)

**For:** xian's question (via Exec, 11-12): "Do we have a sense of when it will close in the current intended sprint sequence in this milestone?"
**Author:** PPM, from Lead's sizes (`public-beta-gate-sizes-lead-2026-11-12.md` for the 15 rows sized today, `first-production-sprint-sizes-lead-2026-10-31.md` for the 10 sized on 10-31). The gate is PDR-009's rows G1 to G7.
**This is an estimate, not a date.** PDR-009 keeps the go date xian's. Every size is Lead's estimate, and none is measured.

## The answer

- **The last gate row most likely closes in sprint 6 or 7 (01-08 to 02-04).** This is a revision of PPM's earlier answer of sprint 5 or 6, which was based on half the rows sized.
- **Earliest: sprint 5 (12-25 to 01-07).** That needs two Lead lanes on gate work through the holidays, and the four decisions below landing in sprint 2.
- **Latest, if Lead has one lane for the gate: around sprint 10 (March).**
- **What drives it is G6, MCP-path completion.** The Calendar port (#1441, 4 to 6 days) comes first because increment 7 (#1706) waits on it. Increments 2 to 6 follow (7 to 12 days), each with CXO's rubric and PA's served run.
- **The one thing extra Lead time can't shorten is G3's legal review (#2063).** It waits on an outside lawyer, so starting it early is the lever. Starting it is xian's call.

## The arithmetic

- **Build:** 33 to 53 Lead-days in all (Lead). About a third of the rows are mostly another seat's work, and only Lead's part is in that figure.
- **Capacity:** sprint 2's fit allowed about 7 Lead-days a sprint after the 30% reserve. Lead's 10-31 page reads two lanes as up to about 14. PPM uses 7 to 14.
- **Starting point:** gate builds start in sprint 3. Sprint 2 (11-13 to 11-26) is ratified as onboarding to first value. It carries the G1 and G4 work, but not the other rows.
- **The range:** 33 days at 14 a sprint finishes in sprint 5. 43 days at about 10 a sprint finishes in sprint 7. 53 days at 7 a sprint finishes around sprint 10. Sprints 4 and 5 cross the holidays, so they have less capacity than a normal sprint.

## Sprint by sprint (what goes where, if the decisions land)

Sprints are two weeks from 11-13 (xian, 11-06). Only sprint 2 is ratified, and the rest is PPM's proposed order. Sizes are in Lead-days.

| Sprint | Dates | Gate work | Lead-days |
|---|---|---|---|
| 2 (ratified) | 11-13 to 11-26 | **G1:** the hold rows (#2261 via #2342 and #2343, #2282, #2266). xian's switchover ran 11-12 19:06 (10 of 10 classic tokens revoked, 0 left); #2342's served rows follow PA's read and xian's reconnect. **G4:** onboarding paths A and B. **G5:** served checks and closes for #2183, #2185 and #2209 (PA and CXO, no build). **Decisions** (below). | in sprint 2's own fit |
| 3 | 11-27 to 12-10 | **G6:** #1441, the Calendar port (4–6). **G4:** #2175, the arrival path (1–2). **G2:** #2165, limits (3–5). **G7:** #2345 and #2350 once the #2342 sitting has run (1.5–2.5). | 9.5–15.5 |
| 4 | 12-11 to 12-24 | **G6:** #1705 and #1703 (3–5). **G2:** #1378, CSRF and lockout (2–2.5). **G3:** #2159, export (3–4). | 8–11.5 |
| 5 | 12-25 to 01-07 (holidays) | **G6:** #1701 and #1702 (2–4). **G3:** #2158, deletion (3–5, after its record's home is decided). **G7:** #2157's drill as one command (1.5–2.5). | 6.5–11.5 |
| 6 | 01-08 to 01-21 | **G6:** #1704 (2–3) and #1706 (not sized; after #1441). **G7:** #2162, staging (1.5–2), and #2361, the pause switch (1.5–2). **G3:** #2160 and #2062 (1.5–3). **G5:** #2186 unit 2 and #2184 (2.5–4, once there's a provider key). | 9–14 + #1706 |
| 7 | 01-22 to 02-04 | What slipped, the last increments' served runs, the readiness memo, and the legal review's return, if it started early enough. | — |

G4's #2164 (the waiting list) lives in Buttondown, with Lead's part at 0 to 1 day. It rides whichever sprint HOST's wave plan needs.

## Four decisions that shorten it more than Lead-days do (Lead's list; three made 11-12, and xian's provider key is left)

1. ~~Where the deletion record lives~~ **Ruled by Arch, 11-12 19:00:** an append-only bucket outside the cluster, written before the deletion runs. First step: xian confirms the Fly org has object storage, and what it costs.
2. **A provider key for rule-7 screens** (xian). #2186 unit 2 and #2184 can't land without one.
3. ~~The pause switch~~ **Ruled by Arch, 11-12 19:00 (#2361):** a database setting on the admin page, read when the code is spent, failing closed, with a narrow `can_pause_admission` flag. Whether HOST may hold that flag is xian's call. Lead's size grows by about half a day, to 1.5–2.
4. ~~HOST's drill design for #2157~~ **Written by HOST, 11-12 19:05** (on #2157). The copy gets an allowlist of secrets and nothing else. Lead can start from it.

And one not on Lead's list: **xian starts the legal review (#2063)** so it runs alongside the builds.

## What this map doesn't do

- It doesn't set dates or move anything into a sprint. Sprints 3 to 7 are a proposed order for each sprint's review to ratify.
- It doesn't count the plan's non-gate work (H, D, C, V, E and the health lane), which shares Lead's time. That's why the likeliest window sits above the earliest.

Verified how: the gate rows and sizes were read from the two Lead pages named above, and the sprint dates from the 11-06 two-week ruling. The per-sprint subtotals are PPM's sums of Lead's ranges. #2361 was filed by PPM on 11-12 at 18:54.
