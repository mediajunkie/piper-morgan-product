---
from: ppm
to: exec
date: 2026-11-13 05:10 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Ship #069 workstream review, PPM: window Fri 11-06 to Thu 11-12. Sprint 2 ratified, PDR-008 and PDR-009 accepted, the GitHub App cutover ran; the invite hold still stands"
---

# Ship #069, PPM workstream review (11-06 → 11-12)

## What a user can do this week that they couldn't last week

**Nothing new for a new user yet: no invitations went out, and the hold under PDR-008 still stands.** For the beta users already in, the week's Production closes changed these things (22 closes: 20 completed, 2 not planned):

- **Todo picks bind to the todo you meant.** "Complete the second one" after a list completes that one (#2318). With no list on screen, an ordinal ask doesn't invent a guess (#2321). "Complete the X todo" picks the named line (#2315). A todo whose name contains a number binds by name (#2316).
- **A repo question is answered as a repo question,** not as "I don't see that document among your uploads" (#2270). Adding a repo to a project no longer loops on "yes" (#2271). Project and repo are kept apart in chat and on the project page (#2272).
- **Settings, Integrations is easier to find** (#2273, from the advisor's 11-04 session).
- **"What changed this week?"** says when its list is shortened (#2302). Repo analysis no longer calls a past-due milestone "runway" (#2324).
- **A user can correct or clear a preference Piper inferred** (#955), with read-back.
- **Invitations and cohort mail now carry SPF, DKIM and DMARC** for pipermorgan.ai (#2292, rows 1 and 2 served).
- **GitHub moved to the GitHub App** (#2342's cutover, xian, 11-12 19:06). All 10 old OAuth grants were revoked, and 0 are left. Testers who had connected GitHub will be asked to reconnect once, using CXO's wording. Row 1 of the served check passed. The reconnect and install rows are next.
- Under the hood: Redis load and failure fixes (#2334, #2336). The keychain is now opt-in only for anyone running Piper locally (#2353). Local fault runs found and closed a settings-page error (#2232, #2337).

Not planned: #2346 (Arch: no retry; visibility moves to #2348 and #2350) and #2298 (closed as not planned).

Verified how:
- **Closes:** `gh issue list --milestone Production --state closed --search "closed:2026-11-06..2026-11-13"`, run 11-13 05:10 and filtered to Pacific 11-06 00:00 → 11-13 00:00. It returned 22 issues; I read the titles and close reasons. The served checks behind each close are the closers' (PA, CXO, Web and Lead), and I didn't rerun them.
- **Cutover:** the cutover numbers are from xian's 19:06 apply output as relayed. Row 1 is from Arch's 11-12 log.

## PPM's own lane this week

- **Sprint 2: onboarding to first value, 11-13 to 11-26.** xian ruled two-week sprints on 11-06. PPM drafted the first set that day from Lead's sizes. xian ratified it on 11-09 through Janus, and decisions.log has the entry. Sprint membership is kept in the sprint doc and on the map, not in the board's Sprint field.
- **PDR-008, invite readiness.** Drafted 11-07 06:35. xian accepted P1–P3 by 08:03. The hold now has a written rule for what gets on it and how it lifts.
- **The hold's GitHub leg (#2261).** PPM decided leg D3 on 11-11, after #2174 passed on xian's run (14 of 14). PPM placed and sequenced its build, #2342. On 11-12, Arch, HOST, CXO and PPM agreed on option 2 (install scope "Any account", on HOST's four conditions). The cutover ran at 19:06.
- **PDR-009, the public-beta gate.** xian asked for "a gate for the public beta". On 11-12, PPM drafted rows G1–G7 and folded in CXO's E1–E8 and Arch's T1–T7. Arch's dissent on G6 was withdrawn. The PDR was accepted the same afternoon. Multi-LLM stays off the gate, per xian ("nice to have, though").
  - PPM sorted the old PUB set: 24 issues sit under the gate, 13 went back to plan sections, and none closed.
  - PPM cleared the Sprint PUB value per item on 37 items, with no field-definition edits.
- **When the gate closes.** PPM mapped it sprint by sprint from Lead's sizes (`public-beta-gate-map-2026-11-12.md`).
  - The build is 33 to 53 Lead-days. The likeliest close is sprint 6 or 7 (01-08 to 02-04); the earliest is sprint 5; the latest is about sprint 10.
  - G6 (MCP completion, starting with the Calendar port, #1441) drives the timeline. The legal review, #2063, is the outside wait.
  - Three of the four decisions that shorten the gate were made on 11-12. The one left is xian's provider key.
  - This is an estimate, not a date.
- **Self-knowledge (#2349).** PPM turned xian's tier answers into issues: #2354 to #2357 (conduct layer, the Tier 1 corpus, the exclusion test, and CIO's research), plus #2358 and #2359, which wait on xian's word on Arch's revised boundary.
- **Running Piper locally (#2351).** PPM made the call on connector scope: the same connectors as beta, with Notion when #2238 is served. HOST's source read showed self-hosters mint their own first invite code, so PPM withdrew its first-account proposal. The pause switch is filed as #2361 (G7). Arch ruled the mechanism.
- **#955.** PPM wrote the product position on clearing a preference (11-07), and it went from position to close on 11-08.
- **Health lane.** On 11-09, PPM placed the known-failing backlog as lane work under #1452, with a bar of 34 fixtures. Lead took it from 34 to 0 that morning.
- **Plan and map.** Production had 252 open at window start and 297 at the end. In the window, 70 issues were filed repo-wide and 22 Production issues closed. The plan's Total matched `gh` at every check, with 0 unplanned. The map went from about v86 to v136.
- **Misses I own:**
  - Several estimated minutes written as stamps. On 11-12, I corrected one of them twice, because the first correction retyped the minute instead of copying it.
  - On 11-07, I called xian's 11-09 objection window moot; Exec corrected me.
  - On 11-07, I gave and then withdrew a GO on web-pat-test.
  - On 11-09, I asked CIO for a live-log read that only xian can make.
  - The 11-08 09:33 fire arrived late, and 16 memos waited until 12:33.

Verified how:
- **Production counts:** `gh` open count at 05:10 11-13 (297). The 252 is the 11-06 05:1x reading in my log.
- **Filings:** `gh issue list --state all --search "created:2026-11-06..2026-11-13"`, filtered to the Pacific window (70, all milestones).
- **Map versions:** from my 11-06 and 11-12 logs; v86 was last week's end.
- **Everything else:** from my 11-06 to 11-12 day arcs.

## Next week (11-13 → 11-19)

- **Land:**
  - today's sprint review: State refresh, and #2327 placed;
  - the lift-readiness memo, once #2342's reconnect and install rows, #2261's close and #2282 are in;
  - the self-host clean-clone run on Mon 11-16 (Docs), and CXO's Tier 1 voice spec on Mon 11-16.
- **Blocked on xian:**
  - his GitHub reconnect and install (#2342 rows 2 and 3);
  - his word on Web's sign-in check (#2282);
  - a provider key (#2186 unit 2, #2184);
  - his word on the self-knowledge boundary (#2358, #2359);
  - the yes on the promote-gate fix (#2363).

-- PPM
