# First two-week Production sprint (11-13 to 11-26): the named set

**Status: ratified by xian, Mon 11-09** ("PM sprint plan approved", to Janus, relayed 08:48). The Friday 11-13 review is shortened, not dropped (Exec, decisions.log 08:56): no ratification there, only a one-line re-check of the State column, which PPM refreshes that morning. The Sprint field isn't touched: this set lives here and on the map.
**Author:** PPM, 2026-11-06, under xian's 10:33 ruling (two-week sprints from Fri 11-13; Exec's memo 10:34).
**Layout (11-09, on xian's note that some bullets were run-on):** one short line per table cell. Each item's history is in "History" at the bottom, unchanged.

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

| # | Item | Owner | Blocker | State, 11-13 06:34 (PPM, `gh issue view`) |
|---|---|---|---|---|
| 1 | #2261: narrow GitHub's `repo` scope, built on D3 (#2342) | Lead | xian registering the published GitHub App, Lead's #2342 build, xian's yes to one promotion (given 11-12 11:44; beta serves it 11:52), then xian's one sitting: App values set and the cutover script run, through #2343's one command (Arch 11-12 06:51 and 08:28; Lead 08:46) | Open. Cutover applied 11-12 19:06 (xian: 10 of 10 classic tokens revoked, 0 left); #2343 closed 11-12 19:17. #2342 row 1 PASS (PA read, CXO ruled). Left: xian reconnects without installing (PA row 2), installs (PA row 3), the refresh row; then #2261 closes |
| 2 | #2282: one canonical host, `beta.pipermorgan.ai` | Web | xian's word for Web's sign-in check | Open, no change since 11-09 (xian's word) |
| 3 | #2292: SPF, DKIM and DMARC | xian | none | **Closed 11-12 13:27** (records at 8.8.8.8 3 of 3, `p=none`; one Workspace message passes SPF, DKIM and DMARC at Gmail). Buttondown's check split to #2344 (Q, not an invite blocker) |
| 4 | #2266's last box: a run as a second GitHub account | Web or PA | xian's second GitHub account | Open, no change since 11-09 |
| 5 | #2219, #2295, #2294, #2328: todo replies (ordinal complete and delete; "them") | Lead, then CXO | none | #2318, #2321 closed 11-08. #2328's follow-up served on alpha 11-10 18:58 (Lead), open. #2219, #2295, #2294 open, no change since 11-09 |
| 6 | #2267: email sign-in after a username is set | Lead | none | Open, no change since 11-09 (username row) |
| 7 | #2268, #2274: the wizard's connect handoff and API-key line | Lead, Web | none | Both open, no change since 11-09 |
| 8 | #2269 3a: "link repo" corpus rows | Lead | none | Open, no change since 11-09 |
| 9 | #2271: the "yes" loop on adding a repo | Lead, Web | none | **Done** (closed 11-06) |
| 10 | CXO's wizard flow: #2273, #2275, #2272's page half, #2286 | Lead, Web, then CXO | Lead names the first ask; prompt 3 needs a fresh connected account | #2273, #2272 closed; #2275, #2286 open, no change since 11-09 |
| 11 | Paths A and B served on fresh accounts | PA, CXO | the invite hold lifting | Not started (the hold stands) |
| 12 | Path B's build: #2297 and #2301 | Lead | Lead's size; Arch on attachment | Both open, no change since 11-09 |
| 13 | #2304: consent asks say what they'd do, not an op name | Lead | none | Open, no change since 11-09 |

#2293 (the priority sort) passed on 11-06 and closes when CXO judges it, so it isn't named.

**Served-check rows (CXO, 10:37):** every build in items 4–10 gets its served quote from PA or Web right after the promotion that carries it, scheduled beside the build. CXO judges only from a quote, so the judgment should never be the one unscheduled step. In #070's progress Ship, a build counts as served only once it has been quoted.

## The second lane: plugin and MCP, with no Lead build time

- **PA's served reads:** #2175's no-account walk is done (11-06), and CXO's three calls are on the issue. #1282's skill and page re-checks are next.
- **xian's two #2242 steps:** the held-token `mcp_allow.py remove`, and his decision on who may connect in the beta. The listing follows that decision.
- **Builds (#1911, and #2175's `next` through `/setup`)** go in the next sprint where Lead isn't fully on onboarding.
- **Docs: #2355's manifest (PPM, 11-13 06:50).** Docs owns it from today: the row shape, then the row list, with the known-limits list as Arch ruled (`docs/ALPHA_KNOWN_ISSUES.md`, a fixed limit deleted). Second lane, no Lead day. Lead's deploy check isn't in this sprint.

## The health lane: the known-failing backlog (PPM, 11-09 10:23)

- **#1452 (section Q), not a named item.** The backlog sat flat at 55 since 11-02: fixture 34, flaky 19, regression 2 (CIO's week count, Exec 10:18).
- **Why a lane, not the set:** the set already runs about a day over, and the score is onboarding. Adding it would push out Path B's build, and that's the one item the score can't lose.
- **The bar:** the 34 fixture entries go down in the sprint, and #070 and #071 each report the count. Lead's size (asked 10:18) sets the target. If a Sonnet subagent can do most of it from a brief, Lead reviews it without spending onboarding days.
- If Lead's size says it can't move without taking named-set days, it comes back to PPM, and then to Exec if the set's scope would change.
- **Met before the sprint (11-09 11:23).** Lead took the fixture entries 34 to 0 this morning, about two Lead-hours, off CIO's 10:10 count. The backlog is 21: flaky 18, regression 3 (CI confirms on the gating push).
- **The 18 flaky stay out of this sprint.** Lead's size is about one Lead-day with a subagent, the same day the set already runs over. #070 and #071 report the count by kind from CI's `backlog size:` line, and the 11-26 review can take them up.
- Burn-down finds, placed 11-09: #2333 (C, spatial, Arch sequences), #2334 (Q, built), #2335 (D, built; xian checks the live log line, on Exec's rollup).
- **11-12, xian via Exec:** #2333 is a **go** (13:59). In this sprint. Arch sequenced it (14:07): Lead builds now, and it rides the first beta promotion after #2342's served rows close, so nothing changes under those rows. #2327 (Piper's analysis reply offers to "close the obvious clutter" in bulk, which it can't do; the issue's audit of floored action names) gets **"yes, Friday"** (14:00): PPM places it at the 11-13 review.
- **11-13 06:35, #2327 placed (PPM, on xian's "yes, Friday"):** in this sprint's health lane, beside #2333, not a named item. It has no user-visible change, so it isn't in the score. Not yet sized: Lead sizes it, and it takes no named-set day while the set runs over. CXO's 11-08 find (the analysis reply offers a bulk "close the obvious clutter" Piper can't do) rides it, so that reply's words come out of the audit. #2320 and #2319 stay candidates, not placed: neither has a go, and the set has no free slot.

## Candidate for xian (sent to him on Exec's rollup 11-09; he books his own hour)

- **One #2157 restore-drill run** early in the sprint, using the 11-04 16:38 safe form, without the full write-up. Arch recommends it (11-06, via Exec 11:01): about an hour, and it retires the larger of the two P1 risks. It needs xian's terminal, because the drill password stays with him. That's a fifth xian step, separate from the other four, so the blocker rule holds. #2157 stays P1, not a hold item. #2158 stays unnamed, since the erase script already serves a request by hand.

## Not named, and why

- **#2157 and #2158 (P1, the restore drill and the purge):** they keep their place, but aren't hold conditions (xian, 11-04).
- **#2164 (the waitlist):** waits on HOST confirming the waves.
- **#2247 (Slack as a source):** 4.5–5.5 Lead-days, plus #1514's review.
- **#2226 (local embeddings):** xian's "when".
- **#2149 and the router items it holds (#2195, #2184, #2209):** the catalog's shape is an open design question. Naming them again would repeat the first sprint's bunching.

## Fit

Estimates, not measurements (Lead's sizes, 11-06).
- About 8 Lead-days of named work against about 7 available, so it draws one day on the reserve.
- Trimmed out on 11-06: #2272's chat half, #2299, #2300 and #2269 3b.
- They come back in this order if a slot frees up: #2312, #2314, #2309, #2269 3b, #2305, #2299.
- The working behind these numbers is under "History".

**Reserve:** 30% of Lead-days for beta-session and partner reports (Lead's 10-31 rule).

Verified how (11-09 08:52 layout pass): `gh issue view` on the 43 issues in the table and the lists above it, for the "State, 11-09" column. Layer: GitHub state. No sizes changed.

## History (moved from the table 11-09, unchanged)

The table's earlier cells, as they stood on 11-08:

| # | Item | Owner | Blocker at the start |
|---|---|---|---|
| 1 | #2261: narrow GitHub's `repo` scope, built on D3 (#2342; the `public_repo` fallback is not taken, #2174 passed 11-11) | Lead | xian registering the published GitHub App, Lead's #2342 build, xian's yes to one promotion (given 11-12 11:44; beta serves it 11:52), then xian's one sitting: App values set and the cutover script run, through #2343's one command (Arch 11-12 06:51 and 08:28; Lead 08:46) |
| 2 | #2282: one canonical host, `beta.pipermorgan.ai` (step 4) | Web | xian's word for Web's sign-in check |
| 3 | #2292: SPF, DKIM and DMARC for pipermorgan.ai (P1, before the next invite) | xian | xian's 15 minutes in Google Admin and Hover |
| 4 | #2266's last box: one run as a second account, its own GitHub identity on every GitHub path | Web or PA (0.25 Lead-day review) | a second GitHub account (xian's) and a Web window |
| 5 | #2219 with #2295 and #2294: the todo replies on the skip landing. List, next and completed served and passed (CXO, 11-06). Ordinal complete and delete are left. | Lead, then CXO (2 days) | **xian said GO on ADR-083 D5 by 11-07 08:03 (Exec relay 08:04). `claude/lead-adr083` lands through the normal gate and promotion, Arch marks D5 accepted, and PA's served checks follow.** **Served on `49a5778df4` (PA, 11-07 09:07–09:11):** 'delete the second one', 'delete the third one' and 'remove the last one' each confirm the shown line, so those pass. Two rows fail and are filed as #2318 in V. First, 'complete the second one' routes to `conversation/complete_todo`, not CLARIFY, so D5's second call never runs. Second, the 'delete the first two' follow-up question is unarmed (#2310's symptom). Those two rows are item 5's last work. Whether D5 covers the complete route is Arch's call with Lead. **Later 11-07:**
- Row 4 ("delete the first two") PASSES on `00da3cb9be`, by number, by name and declined.
- Row 5 ("complete the second one") binds 5 of 5 only at the 5.0 s measurement ceiling (`8633405573`). Complete's second call is 3.2–4.1 s served against 1.1 s direct, and Arch (12:27) puts the extra time inside the app.
- The shipped ceiling must stay at or under xian's approved 2.5 s unless he says otherwise (PPM to Exec, 12:34). Above that, the whole-list pick stays, which is CXO's accepted fallback. **13:42 (Arch, Exec 13:41):** D5 ships at 2.5 s while #2320 is open, and the 3.0 s question to xian is withdrawn. Slow calls are #2320 (about 4 in 10 LLM calls of any kind take about 2.2 s more inside `LLMClient.complete()`), not D5's cost. Whether that fallback rate is acceptable is CXO's call. **18:20 (PA, beta `4d5fbfae7d`, D5 at 1.5 s):** row 5 ("complete the second one") binds 10 of 10 with 0 fallbacks, which meets CXO's bar of at most 1 in 10. Rows 4 and 5 now both pass on the live site. #2318's close is CXO's judgment, and #2321 and #2322 stay open. **New candidates for the 11-13 review (PPM, 15:34):**
- #2320: the slow mode, felt on every turn;
- #2319: an absolute-date reminder saved for tomorrow, a silent wrong date;
- #2321: no-list ordinals skip the armed reply, and one invents a guess. **Closed 11-08 07:18 by CXO: every row has a served quote, including the no-list cap line.** #2324 ("runway", overdue and tomorrow) closed 11-08 08:10. #2318 closed 11-08 12:49 (CXO, on PA's served rows), so item 5's D5 rows are all closed; #2219 stays open for its other rows. #2328 (`them` says not-found, V) **joined item 5 on xian's word, 11-10 17:31 ("Work on 2328 in this sprint", Lead's relay 17:34). Lead builds to the existing armed-pick wording (CXO 17:36); CXO judges the served quotes for both phrasings.** Before that it was a possible rider, V. #2315 and #2316 closed 11-07, served on `641ef2eb56`. Before that: D5 passed its screen (Arch, 11-06 18:24), a second router call only on CLARIFY with a list in scope. Before that, ADR-083's first screen failed its bar (Lead, 11-06 17:24). The ordinals pass 6 of 6, but the slot moves 38 unrelated rows. So ADR-083 stays proposed, xian's veto is moot for now, and ordinal complete and delete keep the interim: a pick over the shown lines, which is honest and served. Item 5 doesn't wait on a second slot shape (Arch's to choose, Exec's to price). Earlier: xian's ADR-083 veto window. Arch accepted the seam at 11-06 10:48, on one condition: a write under a floor category asks first and never writes that turn. CXO's floor words are ready if there's no seam. Arch (11:38) accepted the seam's entry-identity `elif` until #2304's commit deletes it, and (11:49) the census (0 corpus rows move) clears the landing. Served check: PA's rows 3 and 5 after the promotion. |
| 6 | #2267: email sign-in fails once a username is set | Lead (0.5–1 day) | none. PA reproduced it 11-06 10:57: sign-in is case-sensitive (a capitalized first letter gets a 401), not username-related, and the 401 says "session may have expired". CXO words the bad-credentials line. |
| 7 | #2268 and #2274: the wizard's connect handoff and the API-key line. CXO's words exist for both. | Lead, Web (1.25 days) | none |
| 8 | #2269 and #2270: "link repo" and the repo-as-document miss | Lead (2.5 days) | #2270's phrasing arrived 11-07 16:50 (Exec, verbatim from xian's call transcript): "look at this project/repository. Give me quick feedback and then help me to move forward." Lead adds it as a corpus row, Arch rules on the expected route, and PA runs the served check. Condition 2's #2270 trigger is spent. **Turn 1's fix is #2270's own, in the sprint (PPM 20:07):** Settled 20:14 (Arch and CXO): Lead's handler, a router-hidden (`router_visible=False`) `analyze_repository` entry. It resolves through the armed #1641 question in CXO's 20:02 words, reads that one repo, records the read, then composes on the floor over that read only. The gather-side record stays retired. CXO's pass line: the advisor's words ×6 with no document reply; gap B binds or says the project has no repo; at least 3 of 6 replies give feedback with a next step (PA quotes them). A counts-only reply fails. **20:47 (Lead):** handler built, gating z21, out in the 11-08 first window. A failed, unlisted `word/word` always asks (Arch 20:38; CXO's opener: `I couldn't find "{pair}" among your repositories.`). Turn 1 isn't claimed until CXO's list-form ask is built, which is Lead's next unit. No new issue. Gap C's armed read offer is #2326 (V, low, not in the sprint). **11-08 13:44 (CXO): #2270 closed.** Both acceptance rows and every pass-line row have served quotes, and a 6 s re-ask on the near-miss is accepted (faster than an uncached plain ask, about 10 s; Arch 13:32). Left to the #2327 audit: the floor's "in one pass" close offers and the doubled repo name. The not-connected turn 1 (no GitHub connected) stays on PPM's Q8 fresh-account list as a quote to collect, not a reopen condition; CXO's close doesn't depend on it. |
| 9 | #2271: the "yes" loop on adding a repo | Lead (1.5 days), with Web on the project page's edit control | none. PA reproduced it 11-06 10:43: the loop is 2 of 2, and a second fault is an invented `link_repository` op. Web's page half (10:50): the list's Edit button is a "coming soon" placeholder. CXO ruled 11-06 11:02: remove it until it works. The `link_repository` aliases wait on Arch's instrument change (ruled yes 11:49, its own commit first). |
| 10 | **CXO's designed flow:** the wizard ends at the first ask. It covers #2273 (finding Integrations), #2275 (the sign-in screen's line and its first-value prompts), #2272's page half (attach a repo to a project) #2286 (step 3's connect card line, built 11-06 at `6c98bb765b`). The sign-in prompts are now `Add a todo: review the deployment plan` and `Show my todos` (CXO, 11-06). Prompt 1 is off the sign-in screen, so #2302 (it counts 7 tasks but names 3) stays in V, outside this item. | Lead (2 days); Web builds the pages (#2273's Settings groups, and attach and detach on `/projects/<id>` for #2272); then CXO judges | CXO's words after Lead's 11-06 10:57 answers. Attaching a repo is a record only: issue reads don't use it, since #1315 retired project-scoped reads. Detaching changes only Piper's records. Also Lead naming the first ask (step 4). Prompt 3 ("Show my open GitHub issues") waits on a fresh connected account. |
| 12 | **Path B's build:** #2297 (a task added to a named project attaches to it), #2301 ("what's in my project?" reads it instead of looping), #2299 (making a project: the name and the "Call it X" misroute) and #2300 (a todo add asks on one turn and acts on the next). From PA's Path B preview, 11-06 10:58. | Lead | Lead's size. Arch decides whether attachment is an argument the router declares. Path B can't score without this item. |
| 13 | **#2304: consent asks say what they'd do, never an op name.** Every "Quick check" ask gets a summary built from the declared args, or CXO's statement with nothing armed. It's the same root as #2219's seam write asks (Lead, 11-06). CXO's twelve confirms (11:28) are its body, and its commit deletes the seam's `elif` (Arch, 11:38). | Lead (S to M) | none. CXO's words exist. Pulled in 11-06 on CXO's case: it puts an untrue sentence in front of a person today. |
| 11 | **Paths A and B served:** PA's quotes on fresh test accounts, and CXO's judgment | PA, CXO | the invite hold lifting (items 1–3), then HOST mints fresh accounts with xian present. Path B can be previewed sooner on PA's existing account, labelled not first-session, and never counted. |

### Fit and served reads, 11-06 to 11-08 (moved 11-09, unchanged)

**Fit (Lead's sizes, 11-06 10:40; estimates, not measurements)**

Items 4–10 come to about 9–10 Lead-days. Two weeks with 30% held back leaves about 7. PPM's trims:
1. **Taken: one batched rule-7 screen, as one run with separate arms, each with its own preregistered bar (Arch, 10:48),** covering #2269 3a, #2270, #2271's offered wording and ADR-083's screen. That saves about a day. Lead prices it to Exec first.
2. **Conditional:** #2270 leaves the sprint if its phrasing hasn't arrived by #070 (mid-sprint). #2272's chat half leaves if item 10's design isn't agreed by day 5. The page half stays with Web. With both triggers unspent, the set runs about 1 day over and draws on the reserve.
3. **#2175's `next` through `/setup` (about 1 day): next sprint**, as the plugin lane's first Lead build with #1911. Today the allowlist (#2242) keeps people with no account from connecting at all, so the build waits for xian's who-may-connect decision.

**Item 12 changes the fit.** PA's 10:58 preview showed Path B can't be reached on today's build: tasks never attach to a project. Item 12 is unsized until Lead sizes it. Path B is half the score, so if the set no longer fits, other items leave and item 12 stays. First out are #2270, then #2272's chat half (already conditional), then anything in item 12 that isn't #2297 or #2301. #2271's Edit button is removed, not built (CXO's ruling), which is small.

**Fit after item 12 (Lead, 11-06 11:12; PPM's trims applied at 11:13).** Item 12 is about 4 Lead-days: #2297 1–1.5, #2301 1, #2299 1, #2300 0.5. The arithmetic, all estimates:
- Items 4–10 come to 9–10. Built this week, before the sprint starts: #2267 (`ee1f6f8c70`), #2286 (`6c98bb765b`) and #2271's alias (`0fe02547cb`), about 1.5 off. The batched screen saves about 1. That leaves about 7.
- Adding item 12 makes about 11 against about 7.
- **Trims applied now, not left conditional:**
  - #2270 leaves (part of item 8);
  - #2272's chat half leaves (part of item 10; Web's page half stays);
  - #2299 and #2300 leave item 12.
- That's about 3 days out, leaving about 8, which draws one day on the reserve.
- **#2304 pulled in as item 13** (CXO, 11-06: it puts an untrue sentence in front of a person today, and honesty outranks features). To hold the fit, **item 8 narrows to #2269 3a** (corpus rows and pins). 3b (finding the floor-written connect offer, the #2040 class) leaves. That's about 1 day out, by PPM's split of Lead's 2.5, and Lead confirms it.
- **They come back in this order** if a slot frees up (#2312 and #2314 added 11-06 18:34): #2312 (the direct "add a repo to my X" asks with nothing armed, on Path A's turn), then #2314 ("add project" refused as a duplicate of a different name, Path B's first step), then #2309 (a corpus row: "which repos are on my X project?" says a real project doesn't exist), then #2269 3b, then #2305, then #2299, then #2270. #2305 (filed 11-06, placed in V at 12:34) is an untrue "trouble processing" line on a multi-intent turn with a held write sibling. It's honesty work, but neither path reaches it, so it isn't named.
- **#2302** (the silent cap of 3) is a small fix, so Lead takes it this week, before the sprint starts (PPM, 11-06 11:26). That way prompt 1's family is honest whether or not it's offered.
- **Built on main before the sprint (Web, 11:20, `21a8977ea9`; the non-admin "Advanced" heading at 12:21, `a1fd1f0ea2`):** #2273's Settings groups, #2272's page half (attach and detach words) and the removal of #2271's Edit button. Each waits on a promotion and a served read. These lighten items 9 and 10 for the review.
- **#2300 doesn't come back as sized.** Arch (11:13) declined the word-list fix. Its fix is now a router-declared framing unit with its own screen, for a later sprint, and "Also add" keeps asking (the safe side).
- **#2303** (make `archive_project` live, on xian's secret: #2271 gate option 2) is filed in V for a later sprint.
- The set is re-checked at the 11-13 review against what lands before then.

**Served on alpha and beta at `765a2bc4f1` (11-06 13:09; PA's and Web's reads, CXO's judgments 13:15–13:17):**
- **Closed:** #2273 (item 10's Settings groups) and #2302 (the silent cap).
- **Passed but still open:**
  - #2294's ordinals and rows 3 and 5 of #2219's seam (item 5).
  - #2267's wrong-password words (item 6). It still needs a sign-in by email from an account that has set a username.
  - #2271's Edit removal (item 9). The add-repo loop and the hide alias aren't served yet. Arch ruled (b) for the alias at 12:51: an exact match archives, and a fuzzy one is offered. The hide-literal deletion is GO (14:09), and so is the "new project" literal in its own commit (14:29).
  - #2272's attach half (item 10). It still needs the Unlink press and PA's chat quote for a project with no repo.
  - #2286's words (item 10). They're in the served HTML but unseen on a page, which needs an unconnected account or a Disconnect window from xian.
- **Failed:** #2301 (item 12). A served model reply improvised an offer after CXO's line. Arch withdrew the fixed reply too, since it would be untrue for 25 status asks. The interim is pulled (`bf5235c1d4`), and #2301 stays FAIL until its real read lands.
- **#2304 (item 13)** is built on Lead's branch and held for rulings. Arch accepted reusing the existing resolvers and the "not sure" interim (13:23), and CXO worded the "not sure" replies. Five ops always say "not sure" for now. Getting their held yes back is #2308, filed and placed in V. #2307 (the trust-mode outward line still prints an op name) is in V too. Neither is named.

**Served on beta at `7ffd460640` (11-06 15:43; PA's reads, CXO's judgment 15:58):**
- **Passed:** #2271's hide and hide-again rows, and the near-match hide offer (16:10).
- **Failed on words:**
  - link_repo's example;
  - #2272's chat line, which teaches a link phrasing that was declined today. CXO's interim is "You can link one on its project page."
  - the floor's narrated delete ask. "Deleting X and Y — want me to go ahead?" is served with nothing armed; that's #2310, whose fix is ADR-083.

**Served on beta at `06c71d53e2` (11-06 18:11; CXO's judgment):** **#2271 closed.** Every row passed: the add-repo loop is gone, link_repo's held ask names the repo, the decline is honest, and the page shows the link. That completes item 9, including the link_repo slice pulled in from #2308. #2313 ("delete A and B" says "couldn't find" for real todos) is placed in V and not named.

**Later 11-06:** #2272 closed (CXO 19:22, on `771eb4f9bd`), so item 10's page half is done. #2314's fix is on main (`a859041d4a`, Arch validated it at 18:45) and waits on a served read. #2315 and #2316 (todo picks, #2219's family) are placed in V and not named; the 11-13 review re-checks them against item 5.

**PPM's two calls (11-06 16:23):**
- **#2311 is built now, before the sprint,** like #2302. It widens the #1855 seam's lead (Arch 16:10, in principle), so the dash form of the narrated ask is rewritten at the output. Lead's census of 5,379 questions found 0 false positives. It waits on CXO's rewrite words. It's honesty work and small, and it closes the worst served finding of the day without waiting on ADR-083.
- **link_repo's held ask: option (b), pulled into item 9 from #2308.** link_repo's resolve-only step reads only its own resolver, binds what it shows, writes nothing before "yes", and CXO words the ask. It's on Path A's add-repo turn, and PA's phrasing is a real served one. It's small, so it draws on the reserve. #2308's other four ops stay out.
- **CXO's words for link_repo's held ask are final (16:33).** The repo-missing ask must be armed. Lead (16:39) corrected the batched screen: #2269 3a, #2270 and #2271's wording are corpus rows, not prompt changes, so arm B is empty and the batch is A plus C, about $2.60. **PPM (16:41): the batch runs without #2270's row,** which follows in the next screen once its phrasing arrives. #2270 is already out of the set.

**#2301's interim words (pulled 11-06 13:56, see above):** Lead (11:12) found that nothing failed. The project-status answer has project names and counts only. So "I couldn't read it" would be untrue. CXO words the honest interim ("I can see your projects' names, not what's in them yet"). The real fix is #2301's read.

**Path B: build, don't narrow (PPM, 11-06).** Path B stays "a project with tasks in it", and item 12 builds the attach. CXO agrees (11-06): don't score "a project with tasks" on replies that don't deliver it. Until it's built, #2297 carries CXO's honest interim words (`Todos aren't grouped by project yet.`).

**Item 10, settled at 10:49:** CXO delivered the #2273, #2272 and #2275 design into the design doc. The day-5 trigger for #2272's chat half now turns on Lead's three confirmations, not on design.


Verified how:
- `gh issue view` this turn on all 26 issues named here: states, labels, and the latest comment on 13 of them.
- #2219's and #2294's 11-06 comments: CXO's served judgment and Lead's served sha `0d4938cf23`.
- decisions.log at 11-06 10:22 and 10:33, and Exec's two 10:34 memos.

Layer: GitHub and repo text. No sizes are claimed (Lead sizes before the review), and no dates beyond the ruling's.

