---
image: 'piper-ship.png'
alt: 'A child and a crew of robots checking each other''s work on a boat.'
caption: ''
---

# Weekly Ship #070: No Workarounds

*November 13–19, 2026*

This week the agent team piled up a lot of work that waited for my attention to fully complete or execute. More and more workflows led to manual tasks for me. Eventually, I asked for a review of the state of affairs, writing "We keep changing how provider keys are used, how github is used, how piper morgan is used by our agents and it's become a tangled mess that keeps becoming my problem to manually navigate. this is not an acceptable state of affairs."

This led to 
- What led up to it: a stored testing key couldn't be decrypted, the classifier refused the workaround, and the seats drifted toward "xian runs it".
- The structural answer: ADR-084, which gives the seats their own keys, accounts and browser (a paraphrase. Its title is "Seat resources: what agents use to run and test Piper is separate from xian's, granted once, and bounded where a seat can't pass"). You accepted it 11-16 at 06:20 with a budget of $10 a run without asking, under a hard cap of $150 a month. Every seat rewrote its open items so that none ends in "xian runs it".
- The cost: a whole week of work that was built and put on beta but not read by a signed-in person. All of it converged on one sitting at Amber (Fri 11-20).
- Sprint 2 is "onboarding to first value", 11-13 to 11-26, and it has 14 named items. 2 were done before the sprint began. 0 closed in week one, and 12 are open. Most of the 12 are built and on beta, waiting for a signed-in read.
- Continuity: #069 was "Off-Limits by Default" (the keychain). This one is the same instinct applied to your own hands.

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

**▸ Write about:** the seat tools built for ADR-084, the promotions to beta, and the review layer catching mistakes before they reached a user.

**▸ Facts:**
- **ADR-084's tools, built and read by 11-18:** seat keys, seat sign-in, seat accounts, the seat browser, a dollar cap per run, and a scan for credential shapes. Real runs that week: 0. Your sitting on 11-20 did Steps A, C, D, F0 and F.1.
- **Updates to beta:** 15 of 16 promotion dispatches succeeded. The gate refused one (11-15 20:00). Lead counts 14, and GitHub and the omnibus count 15.
- **The promotion gate now walks every parent** of a merge, not just one line of history (Lead, landed 11-13. #2363 itself is still open, so don't say closed). This follows on #069's story of the gate missing the tested commit.
- **The second reader caught what the first missed** (a learning-pattern candidate, see below):
  - CIO found three gaps in HOST's first drill read.
  - Lead caught, by running it, that Arch's deploy-step command would have stopped every promotion.
  - Arch caught a CXO sentence about an unknown connection that was untrue for one GitHub path.
  - All three were corrected before merge or serve.
- **Arch:** 175 ruling lines this week, with at least five self-corrections. (Last week's Ship said 160. Your "somewhat astonished" line could continue.)
- **Main CI** had two red windows on the morning of 11-17 (5 failed Tests runs, 08:11 to 09:50, from Lead's pushes) and was 12 of 12 green at every read after (Lead's and PPM's reads).
- **MCP deploys:** 1, yours on 11-15 in PA's session. It kept the connector's GitHub reads inside the repositories you chose (see Product).
- **Clock rule:** live 11-18 (CIO), the follow-through on #069's time-guessing story. Backtest: it would have refused 138 of 1,781 past commits (7.7%). The backtest found one false positive, which CIO fixed, and no seat has reported a false refusal since it went live.

## 🎯 Product & experience

**▸ Write about:** what a user can do now that they couldn't on 11-12, and the caveat that almost none of it has been read by a signed-in person.

**▸ Facts: read on the live service by a person (1 item)**
- In Claude, the connector's GitHub issue reads stay inside the repositories you installed the App on. Before: 366 issues, mostly from public repositories nobody chose. After: 1, the one issue in the chosen test repository. PA read it through the connector on your account on 11-15, and CXO passed it. (#2374)

**▸ Facts: on beta, not yet read signed in**
- **Disconnect** says what stays behind at the provider: the App stays installed, and a token or Notion key stays valid. The wording is cautious when Piper can't tell how GitHub was connected. Disconnect All lists what's left to do.
- **The Integrations cards** read in plain sentences: no code words or exception text, and one sentence about a stale connection per connector, on the card and in chat. Before a write to a repository without the App installed, Piper says to install the App first. (#2379, #2401, #2402)
- **Piper's replies follow the nine conduct rules** you approved (#2354). They sit outside the classifier, so routing is unchanged.
- **Self-hosters:** a fresh database is built by alembic, not pre-empted by setup (#2372, closed 11-15). The key saved at setup becomes the account's key (#2405, closed 11-20, after the window, so say "since" or move it to next week). Two copies on one machine no longer share a database: a variable now prefixes every container, network and volume name (`433a8c6b33`, 11-16). Setup's self-hoster lines now name the three data services the docker compose step starts, in CXO's words (`6a27a0a47d`, 11-16). Both are under #2386, which is still open, so call them built, not closed. (Exec 11-23: sources for the two lines Comms flagged.)
- **Smaller fixes:**
  - Piper stops blaming GitHub when it never touched it (#2407).
  - An unreachable Redis no longer costs 2 seconds a call (#2370).
  - The Anthropic subscription sentence (#2274).
  - The archive pick shows its date (#2271).

**▸ Facts: what you can't do yet** (the same shape as #069's list)
- Get an invitation (the hold stands).
- Sign in as a fresh account.
- Reach a first valuable thing in a first session.

## 🔬 Methodology & process innovation

**▸ Write about:** turning "don't hand me workarounds" into structure, and one or two of the week's process rules.

**▸ Facts:**
- **ADR-084 as method:** the fix for "xian keeps becoming the manual step" is to give each seat its own key, account and browser, with a budget, rather than a rule to remember. Same shape as #069's chokepoint lesson.
- **The D6 check** (from the ADR-084 sitting): any step that lands on you is checked for whether standing access would remove it, and who would actually do it.
- **"The check and the claim go in separate calls"** (CIO, 11-15), after CIO caught itself reporting a result before reading it six times in two days (11-14 and 11-15, seven by that night). The same shape recurred in Comms (11-17: reporting "The Wall" unchanged after you'd edited it in the admin UI). This is the same family as #069's time guessing.
- **The clock rule** went live 11-18 (see Engineering), the end of #069's "weary of the repeated shuffle".
- **Keychain follow-through:** on 11-15 a test browser started without the mock-keychain flag, so it may have touched your login keychain. CIO disclosed it 11-16. A hook and an every-fire check now cover it.
- **Mail move:** v4 (the separate mail repository) is now the only path between seats. The old path ended 11-23, which is after the window, so mention it only as "since".

## 🌍 External relations & community

**▸ Write about:** the five posts, all your prose, plus the new cadence starting this week: Ship on Tuesday, a narrative on Thursday and an insight on the weekend.

This week we published:

- Sat 11-14, insight: ["Which Agent Did It?"](https://pipermorgan.ai/blog/which-agent-did-it/)
- Sun 11-15, insight: ["No New Skills This Time"](https://pipermorgan.ai/blog/no-new-skills-this-time)
- Tue 11-17, building: ["The Wall"](https://pipermorgan.ai/blog/the-wall/)
- Wed 11-18, Ship #069: ["Off-Limits by Default"](https://pipermorgan.ai/shipping-news/weekly-ship-069-off-limits-by-default)
- Thu 11-19, building: ["Inviting Company In"](https://pipermorgan.ai/blog/inviting-company-in)

[![A nervous host welcomes a smiling guest carrying flowers into a cozy living room, while a translucent AI helper pauses beside a half-painted wall.](https://pipermorgan.ai/assets/blog-images/inviting-company-in.webp)](https://pipermorgan.ai/blog/inviting-company-in)
*"Come in! Mind the unfinished business!"*

**▸ Facts:**
- All five are distributed (calendar). Each one is your prose, which Comms checked against sources, with fixes made only on your OK.
- **One-line content notes**, from each post's opening:
  - *Which Agent Did It?*: every agent acted on GitHub as your account, so work couldn't be traced to a seat.
  - *No New Skills This Time*: the monthly skills sweep found nothing new to build, and that was the right result.
  - *The Wall*: the September week the team hit the weekly usage limit.
  - *Inviting Company In*: the first arc post, about the stale hosted alpha, moving onto Fly, and inviting a reader in.
- **Hero alternative:** "The Wall" (`the-wall.webp`, caption *"I thought you said it ran itself?"*). Both image URLs returned 200. I picked "Inviting Company In" because "unfinished business" fits a week of work that was built but not yet seen. Your call.
- **Cadence:** Ship moves to Tuesday from this one. No Thursday narrative in Thanksgiving week (your 11-17 word).

## 📊 Governance & operations

**▸ Write about:** the numbers, and the spend line (seats spent $0, since every paid run waited on Step A).

**Operations numbers**

- Updates to beta: 15 (of 16 dispatches)
- Signed-in reads on beta: 0
- MCP server deploys: 1
- Issues filed / closed: 44 / 10
- Open Production issues: 297 → 329
- Main CI: two red windows (the morning of 11-17), green at every read after
- Paid model calls by seats: $0
- Posts published: 5

**▸ Facts:**
- Closes: 10 repo-wide (gh), 8 in Production (PPM). Both are right, about different sets.
- Your 11-17 spend reads: the test key at $16.19 of $40, and the org at $49.29 of $250. #069 printed a week's spend and tokens. I don't have this week's token totals from the same source, so leave that line out or ask me for it.

# 🎯 Coming up next week

**▸ Write about:** sprint 2's last week. #071 reports the final score as it stands, since sprints don't stretch (your 11-20 word).

**▸ Facts:** the five goals you approved for 11-20 to 11-26:
1. Seats run for real: Web's sign-in, the real-key run for the self-host fix, the conduct-rules count and cache run, and the first paid call under the cap.
2. Read what's on beta, signed in, and close it. CXO judges.
3. Finish the GitHub move: the open rows on the seat's GitHub account, then the lift-readiness memo.
4. Keys and deploys off your hands: the MCP deploy job and its one token from you, and the restore drill on your day.
5. Editorial: Sat 11-21, this Ship, and Sat 11-28. (Sat 11-21's insight ran Sun 11-22 as "Do I Have To?", at your request.)

Since the window closed: your 11-20 sitting did Steps A, C, D, F0 and F.1, and "Do I Have To?" published Sun 11-22.

# 🚧 Blockers & asks

**▸ Facts:**
- Invitations are still on hold.
- The signed-in reads wait on the remaining sitting steps: F.2 onward, and the seat-tester account.
- The step that puts an OpenAI key in the seats' hands is the one thing between the provider-key work and merge.
- Wait-list line, as in #069: pipermorgan.ai/try/beta/

# 🔎 This week's learning pattern

**▸ Pick one.** Candidates from the review:

## Candidate A: Fix the system, not the person

- **Discovery:** when a fix keeps landing on one person's hands, the system is missing a resource, not a rule.
- **Example:** your 11-15 ruling led to ADR-084's seat keys, accounts and browser.
- **Why it matters:** a manual step done once becomes a manual step forever.
- **Application:** when an item's next step reads "X runs it", ask what standing access would remove the step.
- **Related:** #069 "Fix it at the chokepoint".

## Candidate B: The second reader

- **Discovery:** a second reader using a different method catches what the first missed.
- **Example:** the three catches listed under Engineering.
- **Why it matters:** all three were caught before a user saw them.
- **Application:** have the second reader run it, not just reread it.
- **Related:** {yours. I found no close match in recent Ships}

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #070. Previous: [#069 "Off-Limits by Default"](https://pipermorgan.ai/shipping-news/weekly-ship-069-off-limits-by-default).

*P.S. {yours}*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of November 13–19, 2026 | Phase: Production, sprint 2, week 1 of 2 (private beta, invitations on hold).**
