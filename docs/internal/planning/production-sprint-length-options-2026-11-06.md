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

- **The weekly Ship stays weekly.** A two-week sprint spans two Ships. The second one's workstream reviews are the sprint review.
- **Weekly goals stay weekly** (xian ratifies them from the Ship reviews; 10-18 ruling).
  - Week 1's goals are the sprint's midpoint check.
  - Week 2's goals are its close.
  - The next sprint's named set is ratified in the same window, so there's no extra meeting.
- **Name a sprint's issues only after checking their blockers.** No more than one named item behind any single unanswered design question or decision. Each named item has its blocker written next to it at the start. This is the fix for what actually went wrong, and it holds at any sprint length.
- **The board's Sprint field stays as it is.** Its options are lanes (PUB, PROD-TECHDEBT, PROD-INFRA, …), not time boxes.
  - The two-week set is named in the plan doc and marked on the map, so the option list isn't touched.
  - Adding an option is a web-UI step only you can do, and any per-item change goes through `assign-sprint-safely`.
- **Where the lanes sit:**
  - **The onboarding sprint, the main focus:** first the invite-hold P0s, then the onboarding path rows (#2219, #2293, #2294, #2295, #2267, #2268, #2273, #2274, #2269), then CXO's designed flow, then served checks on PA's and Web's accounts.
  - **Plugin and MCP lane (R7, #1282):** a second lane in the same sprint, as a smaller slice, not after it. Its first unit is #2242's allowlist, about 1–1.5 Lead-days. The public listing waits for that allowlist anyway (PA, 11-06), and it closes a beta exposure on its own. #1911, #1918 and #2175 follow in the sprint after.

**Capacity facts:** Lead's 10-31 unit still holds:
- a Lead-day covers the build, the landing gate, Arch's validation and the served check;
- two lanes run at once;
- about one Lead-day per partner report;
- hold 30% in reserve.

Lead's fresh numbers (a quiet week's closes, a review-and-promote cycle's cost) and PA's earliest plugin-lane start will be added here when they land.

## 4. Recommendation and the one question

**Recommendation:** two-week sprints for Production, starting at the first Ship boundary after you answer. The first is the onboarding sprint, with #2242's allowlist as its second lane. Keep the Ship and the weekly goals weekly, and check named items for shared blockers before naming them.

**The one question for you:** two-week sprints from the next Ship boundary after you answer, with onboarding as the main focus and the plugin lane's #2242 beside it? Yes, or stay weekly?

Verified how:
- Read the Ship #068 review's sprint row and bottom line, the 11-06 weekly diff's closed counts, and decisions.log for 10-18 (goals), 10-31 21:17 (second track) and 11-06 07:31 (Arch's fourth failed catalog addition).
- Read Lead's 10-31 sizes file.
- Ran `gh issue view` on the six named issues and on #2242, #2238, #2235, #2186, #2149, #2021 and #2165 this turn.

Layer: repo text and GitHub. The "would a second week have closed it" column is my judgment from each issue's blocker, not a measurement.
