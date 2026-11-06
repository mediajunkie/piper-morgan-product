# First two-week Production sprint (11-13 to 11-26): proposed named set

**Author:** PPM, 2026-11-06, under xian's 10:33 ruling (two-week sprints from Fri 11-13; Exec's memo 10:34). **For:** the 11-13 weekly review, where xian ratifies it. **Status:** a proposal. Lead sizes the build items before the review. The Sprint field isn't touched: this set lives here and on the map.

- **Main focus:** onboarding to first value (xian, 11-04).
- **Ships:** #070 (11-13 to 11-19) reports progress, and #071 (11-20 to 11-26) reports the final score.

## The goal and its final score

**Goal:** a new account reaches one valuable thing in its first session, without help.
- Path A, a PM with a repo: a useful read of their own GitHub work.
- Path B, no repo: a project with tasks in it.

**The final score at #071** is two counts:
- Paths A and B, each quoted served on a fresh test account by PA and judged by CXO (0, 1 or 2 of 2);
- the invite-hold P0s closed (n of 3).

Beta-user sessions come after the hold lifts. They aren't in this sprint's score.

## The named set, with each item's blocker written beside it

Rule, from the ruling: no more than one named item behind any single unanswered design question or decision.

| # | Item | Owner | Blocker at the start |
|---|---|---|---|
| 1 | #2261: narrow GitHub's `repo` scope (`public_repo` if D3 fails) | Lead | xian's #2174 runs |
| 2 | #2282: one canonical host, `beta.pipermorgan.ai` (step 4) | Web | xian's word for Web's sign-in check |
| 3 | #2292: SPF, DKIM and DMARC for pipermorgan.ai (P1, before the next invite) | xian | xian's 15 minutes in Google Admin and Hover |
| 4 | #2266's last box: one run as a second account, its own GitHub identity on every GitHub path | Web or PA (0.25 Lead-day review) | a second GitHub account (xian's) and a Web window |
| 5 | #2219 with #2295 and #2294: the todo replies on the skip landing. List, next and completed served and passed (CXO, 11-06). Ordinal complete and delete are left. | Lead, then CXO (2 days) | xian's ADR-083 veto window. Arch accepted the seam at 11-06 10:48, on one condition: a write under a floor category asks first and never writes that turn. CXO's floor words are ready if there's no seam. |
| 6 | #2267: email sign-in fails once a username is set | Lead (0.5–1 day) | PA's served repro: the code already falls back to email (#1261), so the bug is somewhere else |
| 7 | #2268 and #2274: the wizard's connect handoff and the API-key line. CXO's words exist for both. | Lead, Web (1.25 days) | none |
| 8 | #2269 and #2270: "link repo" and the repo-as-document miss | Lead (2.5 days) | #2270 waits on the session's exact phrasing (PA's repro or xian's notes) |
| 9 | #2271: the "yes" loop on adding a repo | Lead (1.5 days), with Web on the project page's edit control | none. PA reproduced it 11-06 10:43: the loop is 2 of 2, and a second fault is an invented `link_repository` op. |
| 10 | **CXO's designed flow:** the wizard ends at the first ask. It covers #2273 (finding Integrations), #2275 (the sign-in screen's line and its first-value prompts), #2272's page half (attach a repo to a project) and #2286 (step 3's connect card line, which is final and unbuilt). | Lead (2 days; Web builds the pages), then CXO judges | Lead's three confirmations to CXO (what attaching a repo does; that a detach changes only the link; that prompts 1 and 2 work on a fresh account), and naming the first ask (step 4). CXO's design was delivered 11-06 10:49 (design doc, section "Settings, project and repo, and the sign-in prompts"). |
| 11 | **Paths A and B served:** PA's quotes on fresh test accounts, and CXO's judgment | PA, CXO | the invite hold lifting (items 1–3), then HOST mints fresh accounts with xian present. Path B can be previewed sooner on PA's existing account, labelled not first-session, and never counted. |

#2293 (the priority sort) passed on 11-06 and closes when CXO judges it, so it isn't named.

**Served-check rows (CXO, 10:37):** every build in items 4–10 gets its served quote from PA or Web right after the promotion that carries it, scheduled beside the build. CXO judges only from a quote, so the judgment should never be the one unscheduled step. In #070's progress Ship, a build counts as served only once it has been quoted.

## The second lane: plugin and MCP, with no Lead build time

- **PA's served reads:** #2175's no-account walk is done (11-06), and CXO's three calls are on the issue. #1282's skill and page re-checks are next.
- **xian's two #2242 steps:** the held-token `mcp_allow.py remove`, and his decision on who may connect in the beta. The listing follows that decision.
- **Builds (#1911, and #2175's `next` through `/setup`)** go in the next sprint where Lead isn't fully on onboarding.

## Not named, and why

- **#2157 and #2158 (P1, the restore drill and the purge):** they keep their place, but aren't hold conditions (xian, 11-04).
- **#2164 (the waitlist):** waits on HOST confirming the waves.
- **#2247 (Slack as a source):** 4.5–5.5 Lead-days, plus #1514's review.
- **#2226 (local embeddings):** xian's "when".
- **#2149 and the router items it holds (#2195, #2184, #2209):** the catalog's shape is an open design question. Naming them again would repeat the first sprint's bunching.

## Fit (Lead's sizes, 11-06 10:40; estimates, not measurements)

Items 4–10 come to about 9–10 Lead-days. Two weeks with 30% held back leaves about 7. PPM's trims:
1. **Taken: one batched rule-7 screen, as one run with separate arms, each with its own preregistered bar (Arch, 10:48),** covering #2269 3a, #2270, #2271's offered wording and ADR-083's screen. That saves about a day. Lead prices it to Exec first.
2. **Conditional:** #2270 leaves the sprint if its phrasing hasn't arrived by #070 (mid-sprint). #2272's chat half leaves if item 10's design isn't agreed by day 5. The page half stays with Web. With both triggers unspent, the set runs about 1 day over and draws on the reserve.
3. **#2175's `next` through `/setup` (about 1 day): next sprint**, as the plugin lane's first Lead build with #1911. Today the allowlist (#2242) keeps people with no account from connecting at all, so the build waits for xian's who-may-connect decision.

**Item 10, settled at 10:49:** CXO delivered the #2273, #2272 and #2275 design into the design doc. The day-5 trigger for #2272's chat half now turns on Lead's three confirmations, not on design.

**Reserve:** 30% of Lead-days for beta-session and partner reports (Lead's 10-31 rule).

Verified how:
- `gh issue view` this turn on all 26 issues named here: states, labels, and the latest comment on 13 of them.
- #2219's and #2294's 11-06 comments: CXO's served judgment and Lead's served sha `0d4938cf23`.
- decisions.log at 11-06 10:22 and 10:33, and Exec's two 10:34 memos.

Layer: GitHub and repo text. No sizes are claimed (Lead sizes before the review), and no dates beyond the ruling's.
