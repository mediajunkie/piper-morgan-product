# Two-week sprints for Production: whether, when, how

**Author:** PPM, 2026-11-06, at Exec's ask (10:09, xian's words: "whether and when and how, if so, to move to 2-week sprints for this milestone"). **For:** xian's sprint-cadence talk, one card on the rollup. It also answers the onboarding proposal's question 1 (a sprint or a lane). Dates are xian's; this page names triggers, not dates.

## 1. Whether

**What the first Production sprint showed (10-31 to 11-06):** it named six issues: #2195, #2042, #2197, #2209, #2184 and #2164. One closed (#2197). Across the whole milestone, though, 30 Production issues were served that week (weekly diff, 11-06).

**Why the other five didn't close:**

| Issue | What held it | Would a second week have closed it? |
|---|---|---|
| #2195, #2184, #2209 | The router catalog. Every catalog addition since 10-29 has failed its screen; today's #2219 split was the fourth (Arch, 07:31). #2195 went NO-GO twice, and the other two wait for router rules. | No. They wait on a design answer (#2149's shape), not on time. |
| #2042 | Its relations pass served. Its aside waits on served traffic and CXO's words. | Maybe. |
| #2164 | The waiting-list mechanism, a decision and HOST's list. The form itself is live. | No. It waits on a decision. |

**So it was mostly neither length nor interruption. It was the blockers being bunched together.** Three of the six named items sat behind one constraint.

- The 11-04 GitHub-connect incident and the invite hold that followed (#2266, #1551, #2261, #2178, #2281–#2283) did take the second half of the week.
- But the lanes still served 30 issues, so capacity wasn't the binding limit.
- How I know: the Ship #068 review's sprint row, the weekly diff's closed counts, and Arch's 11-06 07:31 ruling (decisions.log).

**Weekly and two-week side by side, for the first sprint:**

| | Weekly | Two-week |
|---|---|---|
| The named six | 1 of 6, as it happened | Still about 1 or 2 of 6. The router items wait on #2149 either way. |
| Lead's 10-31 arithmetic for the suggested first set | That set was 14–25 Lead-days, 2–3 weeks at two lanes, before the 30% reserve. A week can't hold a set that size, so each week restarts mid-set. | Fits one sprint if #2021's migration and #2226's large option are left out (Lead's own two levers). |
| Cost to xian | One sprint talk a week, in short windows | One every two weeks. Weekly goals still run. |
| Absorbing an interruption | A half-week incident is half the sprint. | A half-week incident is a quarter of the sprint. |

**The case for two weeks rests on the work's shape, not on the first sprint's miss.** The next sprint's main focus is onboarding to first value (xian, 11-04). That work goes design, then build, then a served check of Paths A and B on test accounts, then a judgment by CXO. It can't show its result inside one week.

## 2. When

**Trigger: the first Ship boundary (a Friday) after xian answers this page.** Exec's example was Fri 11-13, the Ship #069 boundary. Whether that's the start is xian's.

- I wouldn't tie the start to #2261 clearing. The invite-hold P0s (#2261, #2282, #2292) are in flight and belong inside the onboarding sprint as its first rows. Waiting for them would just stretch the current sprint.
- The current sprint runs on, weekly, until that Friday.

## 3. How

**xian's framing (11-06 10:22, via Exec; not yet his yes or no on two weeks):**
- **The weekly Ship continues whatever the sprint length.** In a two-week sprint, the mid-sprint Ship reports progress, and the closing Ship reports the final score.
- **xian and Exec hold a weekly review every week, and the sprint cadence sits inside it.** In a closing week it also plans the next sprint and holds a retro on the last one. Most of the preparation is delegated through the team.

**Who prepares what for that review:**

| | Mid-sprint week (progress) | Closing week (final score) |
|---|---|---|
| Each lane's workstream review | progress on its named items, and any blocker that showed up | the result for each named item (served or not, and why), plus two or three retro lines: what slowed it, what to keep |
| PPM | the named items' state on the map | the next sprint's named set, with each item's blocker checked and written beside it, plus the plan Total and the map |
| Exec | the weekly goals, as now | the synthesis: the final score, the retro lines across lanes, and PPM's proposed set, as one card |
| xian | ratifies the week's goals | ratifies the goals and the next sprint's set, all in the same review, so there's no extra meeting |

- **Comms:** the Ship template gets two forms, progress and final score, if xian says yes.
- **HOST:** may want a say in the retro's shape.
- **Weekly goals stay weekly** (10-18 ruling). They come from the reviews, as now.
- **Name a sprint's issues only after checking their blockers.** No more than one named item behind any single unanswered design question or decision. Each named item has its blocker written next to it at the start. This is the fix for what actually went wrong, and it holds at any sprint length.
- **The board's Sprint field stays as it is.** Its options are lanes (PUB, PROD-TECHDEBT, PROD-INFRA, …), not time boxes.
  - The two-week set is named in the plan doc and marked on the map, so the option list isn't touched.
  - Adding an option is a web-UI step only you can do, and any per-item change goes through `assign-sprint-safely`.
- **Where the lanes sit:**
  - **The onboarding sprint, the main focus:** first the invite-hold P0s, then the onboarding path rows (#2219, #2293, #2294, #2295, #2267, #2268, #2273, #2274, #2269), then CXO's designed flow, then served checks on PA's and Web's accounts.
  - **Plugin and MCP lane (R7, #1282):** beside onboarding as a smaller second lane, with no Lead build time in it. It has three parts, each with its own trigger (PA, 11-06 10:16):
    - **PA's served reads start now.** #2175's no-account walk was done at 10:18: a first-timer gets "Welcome back!", there's no waitlist link, and sign-up loses the connect. CXO words the path next. Then come #1282's skill and page re-checks. #1918's with-a-row check needs an allowlisted account.
    - **Builds wait for a Lead slot.** #1911 (consent branding) is one. #2175 may add `next` carried through `/setup`. They go in the first sprint where Lead isn't fully on onboarding.
    - **The listing waits for xian.** #2242's allowlist is already built and served (PA, 11-03, MCP v19). What's left is xian's held-token step (`mcp_allow.py remove`) and his decision on who may connect in the beta. The listing follows that decision, because a public listing before it sends most visitors to a 403.
    - *Corrected 10:23: the first version of this page called #2242 a 1–1.5 Lead-day build. That was Lead's 10-31 size, before it was built.*

**Capacity facts:** Lead's 10-31 unit still holds:
- a Lead-day covers the build, the landing gate, Arch's validation and the served check;
- two lanes run at once;
- about one Lead-day per partner report;
- hold 30% in reserve.

PA's plugin-lane timing is in the plugin lane's entry above. Lead's fresh numbers (a quiet week's closes, a review-and-promote cycle's cost) will be added here when they land.

## 4. Recommendation and the one question

**Recommendation:** two-week sprints for Production, starting at the first Ship boundary after you answer.
- The first is the onboarding sprint. The plugin lane runs beside it as PA's reads plus your two #2242 steps, with no Lead build time.
- The Ship stays weekly (progress, then final score). Your weekly review takes the planning and the retro, prepared as in the table above.
- Check named items for shared blockers before naming them.

**The one question for you:** two-week sprints from the next Ship boundary after you answer, with onboarding as the main focus and the plugin lane's reads beside it? Yes, or stay weekly?

Verified how:
- Read the Ship #068 review's sprint row and bottom line, the 11-06 weekly diff's closed counts, and decisions.log for 10-18 (goals), 10-31 21:17 (second track) and 11-06 07:31 (Arch's fourth failed catalog addition).
- Read Lead's 10-31 sizes file.
- Ran `gh issue view` on the six named issues and on #2242, #2238, #2235, #2186, #2149, #2021 and #2165 this turn.

Layer: repo text and GitHub. The "would a second week have closed it" column is my judgment from each issue's blocker, not a measurement.
