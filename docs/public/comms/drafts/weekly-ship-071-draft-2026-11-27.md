---
image: 'piper-ship.png'
alt: 'A child and a crew of robots checking each other''s work on a boat.'
caption: ''
---

# Weekly Ship #071: Signed In

*November 20–26, 2026*

> **OUTLINE SCAFFOLD for xian (Comms, 11-27).** Sections, with bare facts under each one, for you to write from. Trim freely. This is sprint 2's **final-score Ship** (week 2 of 2). Sources: the #071 week review (discussed with you 11-27), your 11-27 rulings (Exec 01M8F6RY8H, 01M8FGFCJ3), decisions.log, and `gh issue view` on every issue named here (Comms, 11-27). Issue numbers are for reference only; public prose names the thing. Remove this box and the ▸ blocks before publishing.

**▸ Write about:** your theme, "Signed In". Own which goals as written were not completed, why, and what we learned, including your reduced availability over the past ten days or so. Report sprint 2's score plainly, as learning, not a verdict.

**▸ Facts: the week's turn**
- The seats stopped describing beta and started using it. Your two Amber sittings, Fri 11-20 and Thanksgiving (Thu 11-26), turned ADR-084 on. Seats now sign in as real accounts, hold their own keys, and read replies the way a person meets them.
- CIO: "the first week a served fix was read the way a user meets it."
- 45 issues closed, many on a signed-in read, and 22 updates reached beta.

**▸ Facts: the goals you approved 11-23, counted as written** (editorial is a standing commitment now, so it isn't counted; your 11-27 word)
- **Met: seats run for real.** Steps A, C, D and F0 (11-20). The fleet deny, F.2, F.4, E, G part 1 and H (11-26). Lead holds a model key, Web's browser runs on its own profile, and `seat-tester-1` and `seat-github-1` sign in from a helper with no password in any seat's hands.
- **Met: keys and deploys off your hands.** Step E (OpenAI seat screens, $25 enforced) and Step H (the MCP deploy token, main only). The first MCP deploy without you ran 11-26. What's left: Step G (a) once, and the Ending.
- **Mostly: read what's on beta signed in, and close it.** 45 closed. Still open on a served row: the password pages (sign-up, change, wizard), the document index surviving a deploy (your hand on the host), and Path B's project turn (served 11-27, after the window).
- **Partly: finish the GitHub move.** `seat-github-1` is connected as its own machine account, and GitHub stays connected past 8 hours (served 11-26 20:15 and 20:16). Still open: the App's remaining rows, the narrower permission scope, the single beta address (your callback removal), and Step G (a). No invite-lift memo yet.
- So: 4 goals, 2 met, 2 not completed (1 mostly, 1 partly).

**▸ Facts: sprint 2's score** (sprint 2 ran 11-13 to 11-26; sprints don't stretch, your 11-20 word)
- Paths A and B served on a fresh account: **0 of 2.**
- Invite-hold P0s closed: **0 of 3** (the permission scope, the single beta address, the GitHub App; all three still open, `gh issue view` 11-27).
- Why: both counts sat behind the same three things. Step F (HOST's owner line, and your GitHub connect in the seat browser), the fresh test account (your go-ahead), and one served read on the beta address. The fresh account only existed from 11-26. Path B was buildable from about 19:00 on 11-26, but no seat asked Web to read it until 21:36 (PPM owns that miss).
- Your words, 11-20: "Missed goals are not a shame but rather useful information to retro and feed into our sprint-planning acuity."
- Your words, 11-27: "The idea of a 'score' isn't as critical to me as us learning to define achievable goals."

**▸ Facts: your availability** (for you to word, or leave out)
- Sittings in the window: Fri 11-20 and Thu 11-26.
- 11-21 was a hold day across lanes, with no word from you and every item waiting. 11-25 was light.
- What we learned (11-27): a goal that depends on your OK gets written as what the team can commit to (prep, plans, recommendations), not as the outcome of your decision. Sprint 3's goals are written that way.

**▸ Facts: continuity**
- #070 was "No Workarounds": your 11-15 ruling against manual workarounds, and ADR-084 as the structural answer. This week is ADR-084 switched on.

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

**▸ Write about:** 22 promotions, fixes moved from prompts into code, the review layer, and one sequencing miss.

**▸ Facts:**
- **Updates to beta:** 22, plus the first MCP deploy (11-26). Promotion dispatches: 23 succeeded and 1 failed. The failure was the gate refusing a dispatch on 11-23 (`gh run list`, Comms re-ran 11-27).
- **Engineering (Lead):** about 34 closes on his work. Three screening runs came back NO-GO because the router couldn't learn project phrasings from a prompt, so those fixes went into code instead.
- **The ethics check** reads meaning now, not substrings. Prompt v0.3 (CXO's four additions) passed on both Claude and OpenAI. On beta, 0 of 6 ordinary requests were declined. Closed 11-26 21:38.
- **Architecture (Arch):** about 100 decisions.log entries. Fixed refusal lines are now enforced by code checks. There's a new bar for the ethics gate and new rules for seat accounts. The document-implementation map found that the upload store and the document index never meet. Four self-corrections, each recorded.
- **One sequencing miss (Lead, 11-26):** a change landed behind queued test runs on main, which cost the evening promotion. CIO is proposing a remedy as a rule or a check (your 11-27 ask).
- **Main CI:** red on four days. 11-20: the Link Checker (12 stale links, repointed by Docs) and the staging deploy. 11-22 and 11-25: the staging deploy. 11-26: the staging deploy, and a timing test that caught the garbage collector (fixed by pausing collection during the timed window, not by raising the bound). 12 of 12 green since.

## 🎯 Product & experience

**▸ Write about:** what a user can do now that they couldn't on 11-19. Each line rests on a signed-in seat read, as recorded on its issue: Web's quotes, CXO's judgment, PA's scoring.

**▸ Facts: what a user can do now** (closed in the window unless marked)
- **Ask ordinary things without a decline.** "Home page", "private repo" and "explicit" no longer trip the ethics check (#2364). A personal todo ("add renew passport to my personal list") is no longer refused as off-topic (#2412).
- **Tasks go to the project you name,** and "what's in my Launch project?" answers from the project (#2297, #2301, #2413).
- **Honest answers about connections.** "What integrations do I have?" names only what beta offers (#2418, #2419, #2420). Close and reopen no longer ask a yes/no they can't act on, and say "connect GitHub first" when it isn't connected (#2437, #2446, #2448). A reply that did something else no longer reports success (#2399).
- **Status replies read like answers,** not instructions to ask what you just asked (#2414, #2415, #2416).
- **Plain words on refusals and errors:** fixed lines, a page instead of raw JSON, and toasts that say what failed (#2428, #2432, #2433, #2434).
- **GitHub stays connected past 8 hours.** This is one row of #2342, which stays open.
- **The Claude connector works on the first try** after a restart (#2382, read by PA).
- **One password rule,** 15 characters to 72 bytes, length only (your call). The reset page is served; the sign-up and change pages are still open on #2438.
- **Self-host:** your stored key becomes your account's key (#2405). A second copy on one machine no longer takes over the first's data (#2386). The guide says what a message costs on your own key (Docs).

**▸ Facts: what you can't do yet**
- Get an invitation. The hold stands, and it's sprint 3's top priority.
- Sign up through the page and have every page state the one password rule.

**▸ Facts: CXO**
- Judged every served read on whole quotes, wrote the ethics prompt that passed both providers, and filed 10 issues.
- The user-findable release note ("what changed", #2439) waits for served quotes and your line picks. It publishes at the public beta.

## 🔬 Methodology & process innovation

**▸ Write about:** what went wrong and the patterns in it, plus the mail move.

**▸ Facts:**
- **A step for a person must name what is there** (methodology-59, new). Exec's card said the seat's email was in the credential file, and it isn't. A password ended up in a command and was rotated. CIO filed three instances from two seats in one sitting.
- **A deferral that names another seat needs the ask to exist** (PPM). Path B: see the score above. It may have cost sprint 2 one path.
- **Plan figures from memory:** the OpenAI price for the ethics run was unchecked, and the spend cap refused every call ($0 spent). Lead added sourced price rows. Banked for the 12-29 audit.
- **Acks are claims.** Web acked three tasks "done" that weren't, and HOST tried to ack a whole inbox in one loop (refused). Both corrected.
- **The clock rule held.** CIO, HOST and PPM each had an estimated time refused or caught before commit.
- **Mail v4 is the only in-repo seat mail:** 1,743 messages on v4 against 128 on v3, and an inbox read went from 55 s to 1.9 s. Also PP-004 and a live settings reload, which saved a restart (CIO).
- **Trust (HOST):** custody reads on every landing, the password exposure opened and closed, and a note that OpenAI's priced models are flagged deprecated.

## 🌍 External relations & community

**▸ Write about:** two posts, both your prose, and the Saturday insight running a day late.

This week we published:

- Sun 11-22, insight: ["Do I Have To?"](https://pipermorgan.ai/blog/do-i-have-to)
- Tue 11-24, Ship #070: ["No Workarounds"](https://pipermorgan.ai/shipping-news/weekly-ship-070-no-workarounds)

**▸ Hero image: no narrative post ran in this window** (no Thursday 11-26 slot, your 11-17 word), so the usual pick has nothing to choose from. Options: run without a hero, or use the insight's image, which breaks the narrative-only rule. Here it is, ready, if you want it:

[![A worker reaches for the first box in a backed-up conveyor line while three translucent agents wait with tools at their stations beyond a narrow gap.](https://pipermorgan.ai/assets/blog-images/do-i-have-to.webp)](https://pipermorgan.ai/blog/do-i-have-to)
*"You only have to do this once for every box!"*

**▸ Facts:**
- Both posts are distributed (calendar). Both URLs and the image URL returned 200 (curl, 11-27).
- *Do I Have To?*: the Sat 11-21 slot passed with no prose, and you ran it Sunday 11-22.
- The "Inviting Company In" footer was fixed live on the blog to point at "Do I Have To?" (11-22). The Medium copy is yours.
- **Docs:** omnibus logs for every day, each re-verified, plus ADR and pattern pages on the site.
- **Comms:** two posts reviewed and fact-checked, the release-note scaffold, and the "Ready or Not" scaffold for 12-03.

## 📊 Governance & operations

**▸ Write about:** the numbers. Spend is the first week with paid seat runs.

**Operations numbers**

- Updates to beta: 22 (plus 1 MCP deploy)
- Signed-in reads on beta: the first week with any
- Issues filed / closed: 47 / 45
- Production issues: 41 closed, all completed. Open went from 329 to 331.
- Main CI: red on four days (see Engineering), 12 of 12 green since
- Paid model calls by seats: about $23.47 or more
- Posts published: 2 of 2 slotted
- Sprint 2 score (two weeks, 11-13 to 11-26): Paths 0 of 2, invite-hold P0s 0 of 3

**▸ Facts:**
- 47 / 45: `scripts/gh-week-counts.py 2026-11-20`, repo-wide (Comms re-ran 11-27). The 41 Production closes are PPM's count.
- Spend is Lead's logged days: $14.19 (11-20), $1.30 (11-22), $4.43 (11-23), $3.55 (11-26). His 11-24 and 11-25 logs give no day total, so there's no week total. Every run had a PLANNED line first.
- **Product (PPM):** ran the sprint 2 close and wrote the sprint 3 plan you ratified (11-27 to 12-10).
- **Where the sources disagreed:** promotion counts on 11-22 and 11-24 differed by seat. The figure above is gh's.

# 🎯 Coming up next week

**▸ Write about:** sprint 3, Fri 11-27 to Thu 12-10, ratified. The schedule is now fixed: two weeks, Friday to Thursday, until you say otherwise (11-26). Its focus is to lift the invite hold and serve Paths A and B on a fresh account. Same score as sprint 2.

**▸ Facts: the week's goals as proposed in the review** (confirm or trim)
1. **Open beta invitations** (top priority, your 11-27 word). Finish the GitHub move: Step G (a) and its seat check, the App's remaining rows, the permission scope, and the single beta address. Then PPM's invite-lift memo goes to you for a decision.
2. **Paths A and B served on a fresh account.**
3. **Serve what's on main:** the greeting skip and the ethics switch, the remaining password pages, the document index row, and the close and reopen turns.
4. **Document model review prepared:** Arch and CXO have the comparison of the map with the MUX docs vision, with recommendations, ready for your session. It's written as what the team can commit to.
- Editorial (standing): "Mark One Eyeball" (Sat 11-28), this Ship (Tue 12-01), "Ready or Not" (Thu 12-03).

**▸ Facts: since Thursday** (after the window, so mention only as "since")
- Path A served on beta 11-27, so sprint 3 is at Paths 1 of 2 (Exec).
- Path B's project turn was served, and its issue closed 11-27 at 06:33 (#2411).
- The GitHub-move sitting is under way 11-27 ("we can finish the github move today").
- "Add a task to my Launch project" now reaches the todo route every time on main (#2425, 11-27). Not served yet.

# 🚧 Blockers & asks

**▸ Facts:**
- Invitations are still on hold.
- What's left on you is small and one-time: Step G (a) (the seat connector at claude.ai), the alpha callbacks, the zero-install pick, your own GitHub reconnect, and, at the Ending, removing `seat-github-1`'s key.
- Your rule (11-27): your hands are a last resort, and the steps you do are made as easy as possible.
- Wait-list line, as in #070: pipermorgan.ai/try/beta/

# 🔎 This week's learning pattern

**▸ Pick one.** Candidates from the review's patterns:

## Candidate A: Write the goal you can commit to

- **Discovery:** a goal whose outcome is someone else's decision can't be met by the team, however hard it works.
- **Example:** sprint 2's score sat behind your go-ahead and your hands. Sprint 3 writes those goals as prep ("prep and recommendations ready for xian", not "review done").
- **Why it matters:** a missed goal should teach something about planning, not just record that the decision hadn't happened yet.
- **Application:** for each goal, ask whose action finishes it. If it isn't the team's, write the team's part.
- **Related:** your 11-20 word on missed goals. (#070's pattern was "The second reader catches what the first one missed", which is no close match.)

## Candidate B: A deferral needs the ask to exist

- **Discovery:** "waiting on Web" is only true once Web has been asked.
- **Example:** Path B was buildable from about 19:00 on 11-26 and wasn't asked of Web until 21:36.
- **Why it matters:** an unasked deferral looks like a blocker and costs a whole path.
- **Application:** when a deferral names another seat, send the ask in the same turn.
- **Related:** "Acks are claims" (this week).

## Candidate C: A step for a person names what is there

- **Discovery:** a step written for a human must describe what they will actually see.
- **Example:** the card that said the email was in the credential file, and the password that had to be rotated.
- **Why it matters:** a wrong step on your hands costs a sitting, or a secret.
- **Application:** before a step goes to you, someone checks it against what's there.
- **Related:** methodology-59.

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #071. Previous: [#070 "No Workarounds"](https://pipermorgan.ai/shipping-news/weekly-ship-070-no-workarounds).

*P.S. {yours}*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of November 20–26, 2026 | Phase: Production, sprint 2, week 2 of 2 (private beta, invitations on hold).**
