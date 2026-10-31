# First sprint toward the Production release: candidates (PPM, 2026-10-30)

**For:** xian's priorities talk after the beta letters go out (Sat 10-31), which Exec is setting up.
**Status:** these are candidates, not a plan. xian picks the priorities, the length and any dates; PPM proposes none.
**Sizes (added 10-31):** Lead's, in `first-production-sprint-sizes-lead-2026-10-31.md`. PA's MCP-lane ordering is folded in below.
**Source:** the 10-23 plan (`production-sprint-proposal-2026-10-23.md`, 240 open, every one with a board Sprint), today's tracking audit (28 known-not-working issues), and the beta letter's nine known-issue lines.

## The lens PPM proposes

The private beta began today. The first sprint should make what partners meet **more true and less broken**, in this order:

1. Ship what's already built and frozen.
2. Strike known-issue lines from the letter.
3. Keep the beta safe to widen.
4. Leave room for what partners report.

The bigger Production tracks (the plugin surface, more LLM providers, the full connector ports, FTUX) come after that, unless xian wants one of them pulled forward.

## Tier 0: built, waiting for the first promotion after the letters

There's no new build here. It's one promotion plus PPM's check list (Exec has the list, and it's in PPM's carry-forward).

| Issue | What partners get | State |
|---|---|---|
| #2225 | Naming the repo after "Which repository…" files the draft | Closed with `fix:not-served`. Letter line 7 is struck from later editions only on the served check |
| #2236 | "What can you help me with?" lists what's true, rendered by code | On main (parts 1 and 2, plus four fixes). Letter line 9 |
| #2233 | A name question gets the name and stops. Due reminders appear once, after the answer, on own-work turns | On main |
| #2237 | Slack and Notion cards show "Not in this beta", and the server refuses connecting them | On main |
| #2230 | Setting the default repo in chat works, validated against the account | The setter is on main. The flip needs xian's word, then CIO or HOST applies it (HOST only with xian present). Letter line 8 |

## Tier 1: strike known-issue lines

| Letter line | Issue(s) | Why now / what it needs |
|---|---|---|
| 4: two-step milestone ask | #2184, with the class fix #2186 and its kin #2183, #2185, #2197, #2209 | Top of PUB triage on xian's 10-29 word. #2186 (list reads use the router's arguments) fixes the class, not one phrasing |
| 1: misreads what you ask | #2195 (literal 32 stays) | It waits on #2149's catalog shape (Arch, 10-30), so **#2149 is the real first-sprint item** |
| 2 and 3: an answer about your data can be wrong | #2042 | xian asked Arch for a diagnosis, not a patch (10-29). The sprint item is that diagnosis and its first fix |
| 5: no undo for deleted to-dos | #2021 | Soft delete with an undo window. Small and well specified (xian's 10-14 ruling) |
| 6: document search from chat | #2226 | Needs a decision on the embedding provider (an OpenAI key, or another way) before it's a build |

## Tier 2: keep the beta safe to widen

| Issue | Why |
|---|---|
| #2165 | Per-account rate and abuse limits, with a user-facing line. Needed before the beta goes beyond the inner circle |
| #1378 | Auth polish (CSRF, lockout, timeout warnings), marked as a public-beta gate item by PM on 07-07 |
| #2229 | The public site still invites people to the alpha. It needs xian's decision on what a visitor does now; then Comms, CXO and Web do it |
| #2238 | Notion's global-key fallback (N1/C1). Required before Notion is offered at all |
| #2235 | Repo validation for OAuth-only accounts. Partners on OAuth can't set a default in chat until it lands |

## Tier 3: room for partner reports

Reserve part of the sprint for what testers report. HOST is the intake. PPM places each report the day it arrives, using the tracking rule from today's audit (every known-not-working item sits on an open issue, and a fix that isn't served carries `fix:not-served`).

## Sizes and the MCP lane (added 10-31 06:55)

**Lead's sizes** (Lead-days; two lanes run at once, so calendar is about half when units are independent):

- Tier 0: no build; one promotion and about half a day of served reads.
- Tier 1: about 10.5–19.5 Lead-days. The large items are #2149 (Arch's catalog shape first, then 2–5 days and two rule-7 runs, about $10) and #2021 (3–4 days, and a promotion carrying a migration, which needs xian's explicit word). The #2184 family is 3–4.5 days; #2183, #2185 and #2209 close on the served check.
- Tier 2: #2165 3–5 days, #1378's CSRF 1–1.5 days, #2235 1 day, #2238 half a day; #2229 is Web's to size.
- Tier 3: hold about 30% for partner reports.

PPM's suggested set (decision 1) comes to about 14–25 Lead-days: two to three weeks before the reserve, three to four with it. Lead names two levers that bring it to two weeks: move #2021 to the sprint after, and take #2226's half-day option (an operator-funded embedding key). **PPM recommends both levers** if xian wants two weeks. #2021's migration promotion needs his word anyway, and letter line 5 stays true and honest meanwhile. Without #2149 the sprint strikes line 4 but not line 1, so PPM would keep #2149. **Order (Arch, 10-31, #2197 ruled):** #2197 declares an argument on `list_milestones`, which changes the router's catalog, the edit #2149 found moves the milestone boundary. So #2197 lands after #2149's shape holds, or inside #2149's run. Arch starts #2149's design once the talk puts it in. #2241 with #2022 is ruled (Arch, 10-31) and landed on main at e394cb4c21 (Lead, 08:36); it serves on PA's next MCP deploy, so it leaves the sprint's tier 2; PA's whole MCP lane is sized in an addendum to Lead's file.

**MCP lane (PA's ordering, 10-31).** None of these block the hosted web beta; MCP completion gates the public beta (PDR-005 Am. 1).

1. Make what's live honest and usable: #2218 (landed 66d4b58492, Arch validated; serves on PA's deploy at Exec's timing), then #2241 (the profile returns 431k characters) with #2022 as one unit.
2. Decide who may connect the hosted MCP now: #2242 (decision 7 below).
3. Trust surfaces a listing needs: #1911, #1918, #2175, and Arch's #2174 read in parallel.
4. Capability increments: #1705 and #1703 first, then #1701, #1702, #1704, #1706.

PPM proposes #2241 with #2022 for this sprint's tier 2. It's small, it's the live surface xian uses, and any client may refuse a payload that size. The rest of the MCP lane answers decision 6.

## Decisions only xian can make

1. **Sprint length and how many tiers it holds.** PPM suggests tiers 0 and 1, plus #2165 and #2229 from tier 2, with tier 3's slot.
2. **The `set_default_repo` flip:** when, and who applies it.
3. **#2229:** what a visitor to the public site should do now.
4. **#2226:** the embedding provider for document search.
5. **Notion in the beta set:** only after #2238 is served and a tester's own key works in chat. Slack waits for #1481 and #1514, and for a reversal of the 08-27 descope for 1.0.
6. **What comes second:** the plugin and MCP increments (#1701–#1707, with #2168's rubric first), more LLM providers (#1612), or FTUX (#1537–#1540).
7. **#2242, who may connect the hosted MCP during the beta.** Today any signed-in account can. PPM recommends an allowlist (xian's account and the cohort's test accounts) until the MCP is offered. If (a): Lead sizes it at 1–1.5 Lead-days across both apps, with no migration (the list is an operator-set flag in the shared database). The MCP half is half a day, ships alone on PA's `deploy-mcp.sh`, and closes access by itself, so it can go the day xian decides. The web half (consent line, refresh grant) rides the next promotion.

Verified how:
- `gh issue view` at 20:5x on 12 of the issues named: #2021, #2226, #2149, #2186, #1378, #2165, #2164, #2230, #2236, #2233, #2237 (all open) and #2225 (closed). The others (#2184, #2195, #2042, #2229, #2235, #2238 and #2183's kin) were read open earlier this evening, in the audit and the 19:51 line check.
- The PUB list read from the plan at origin/main.
- The letter's nine lines as re-checked at 19:51.
- Layer: GitHub state and repo text. This is a proposal: no sizes are claimed (Lead sizes), and no dates are proposed.
- 10-31 additions: Lead's sizes file and PA's MCP ordering memo read at origin/main; #2241 and #2242 read with `gh issue view` after placing.
