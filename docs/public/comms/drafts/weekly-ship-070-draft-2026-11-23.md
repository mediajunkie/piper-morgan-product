---
image: 'piper-ship.png'
alt: 'A child and a crew of robots checking each other''s work on a boat.'
caption: ''
---

# Weekly Ship #070: No Workarounds

*November 13–19, 2026*

This week the agent team piled up a lot of work that waited for my attention to fully complete or execute. More and more workflows led to manual tasks for me. Eventually, I asked for a review of the state of affairs, writing "We keep changing how provider keys are used, how github is used, how piper morgan is used by our agents and it's become a tangled mess that keeps becoming my problem to manually navigate. this is not an acceptable state of affairs."

This led to an architecture decision record ([ADR-084](https://pmorgan.tech/internal/architecture/adrs/adr-084-seat-resources-are-separate-granted-once-and-bounded)) with an ungainly name, "Seat resources are separate, granted once, and bounded." It gives each agent/role "seat" their own keys, accounts and browser. I accepted it on Nov 16, approving a budget of $10 a run without asking, under a hard cap of $150 a month. Every agent then reviewed their open items for tasks they had assigned to me to run manually that they were now adequately provisioned to run themselves.

# 🚀 Shipped this week

The upshot was that the work done in the first week of this two-week sprint (itself the team's first sprint of this length) didn't get a human review before the second half of the sprint behan.

## ⚙️ Engineering & architecture

The goal of this sprint (Sprint 2 of the Production milestone) is that a new user make it from "onboarding to first valuable experience." The sprint runs from Friday, November 13 to Thursday, November 26 (a U.S. holiday, no newsletter that day, by the way), with 14 specific items, two of which were actually done before the sprint began. We didn't close any in the first week, as noted above, but most of the remaining twelve are already built and on beta, waiting for my to sign-in and review them.

The team also built the tooling to implement ADR-084, with step-by-step instructions ready for me to implement.

The beta was rebuilt 15 times, and Lead Developer wrote an update to the tool that promotes builds to beta so that it walks every parent of a merge (instead of just checking one line of history as it it had done in the past), to address the problem noted in last week's shipping news about the promotion gate missing a tested commit.

Last week I confessed I was astounded to learn that Arch made 160 architectural rulings in supervising the build. I guess I need to get use to that pace because this week they made 175 rulings.

I oversaw one fresh deployment of the MCP build on Nov 15, working with Piper Alpha (it's their project!) to narrow the scope of its GitHub connector to just the repos chosen.

The clock rule (about not guessing the time) went live on Nov 18 per the CIO. A backtest showed it would have refused 7.7% of past commits and revealed a false-positive, enabling CIO to fix it. No false refusals reported yet since.

## 🎯 Product & experience

What a user can do now that they couldn't last week (as far as we can tell, given that I have not tested any of it yet):

- In Claude, limit the Piper Morgan MCP connector's GitHub access to **just the repos you installed it on***.
- **Disconnect** an integration from the Piper Morgan side with clear indications that the connection remains valid and can still be reconnected. 
- Use **Disconnect All** to remove all connections [Exec: please fact-check this?]
- Understand the plain language in the **Integrations** setting page
- Attempt to write to a repository [Exec: does "without the App installed" mean without doing the Github integration, ... the App lingo seems like GitHub App terminology which is not necessarily how the user will understand as "connecting Piper Morgan to Github" - if it means something else, please clarify for me] and get a reminder from Piper says to [install the App first][??]

**▸ Facts: what you can't do yet** (the same shape as #069's list)
- Get an invitation (the hold stands).
- Sign in as a fresh account.
- Reach a first valuable thing in a first session.

Built but not closed yet:
- **Host their own beta** now that a fresh database is built by alembic, not pre-empted by setup. Two copies on one machine no longer share a database: a variable now prefixes every container, network and volume name

We also codified nine conduct rules for Piper's replies:

[Exec: please add succinct list for me to review and edit:]

(These rules sit outside the classifier, so routing is unchanged.)

## 🔬 Methodology & process innovation

I've already devoted enough ink to "don't hand me workarounds (ADR-084) above, and the clock rule.

We also put my machines' keychains off-limits to agents.
- **Keychain follow-through:** on 11-15 a test browser started without the mock-keychain flag, so it may have touched your login keychain. CIO disclosed it 11-16. A hook and an every-fire check now cover it.

The entire team has migrated to the v4 mail system that involves a separate mail repository to avoid overloading traffic on the primary code-and-docs repository. 

## 🌍 External relations & community

I maintained the current hand-written cadence at a barely sustainable pace this week and prepared to move to a new schedule for this phase of the project:


- Sat 11-14, insight: ["Which Agent Did It?"](https://pipermorgan.ai/blog/which-agent-did-it/)
- Sun 11-15, insight: ["No New Skills This Time"](https://pipermorgan.ai/blog/no-new-skills-this-time)
- Tue 11-17, building: ["The Wall"](https://pipermorgan.ai/blog/the-wall/)
- Wed 11-18, Ship #069: ["Off-Limits by Default"](https://pipermorgan.ai/shipping-news/weekly-ship-069-off-limits-by-default)
- Thu 11-19, building: ["Inviting Company In"](https://pipermorgan.ai/blog/inviting-company-in)

[![A nervous host welcomes a smiling guest carrying flowers into a cozy living room, while a translucent AI helper pauses beside a half-painted wall.](https://pipermorgan.ai/assets/blog-images/inviting-company-in.webp)](https://pipermorgan.ai/blog/inviting-company-in)
*"Come in! Mind the unfinished business!"*

The new schedule is as follows:

1. Tuesdays (like today) I will publish the Weekly Ship for the sprint week that ended the previous Thursday. This is moving from Wednesdays. The Ship will continue to appear first in the Shipping News on the Piper Morgan website and then gets crossposted to the Building Piper Morgan newsletter on LinkedIn.
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

- **The second reader caught what the first missed** (a learning-pattern candidate, see below):
  - CIO found three gaps in HOST's first drill read.
  - Lead caught, by running it, that Arch's deploy-step command would have stopped every promotion.
  - Arch caught a CXO sentence about an unknown connection that was untrue for one GitHub path.
  - All three were corrected before merge or serve.
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
