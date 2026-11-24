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

The upshot was that the work done in the first week of this two-week sprint (itself the team's first sprint of this length) didn't get a human review before the second half of the sprint began.

## ⚙️ Engineering & architecture

The goal of this sprint (Sprint 2 of the Production milestone) is that a new user make it from "onboarding to first valuable experience." The sprint runs from Friday, November 13 to Thursday, November 26 (a U.S. holiday, no newsletter that day, by the way), with 14 specific items, two of which were actually done before the sprint began. We didn't close any in the first week, as noted above, but most of the remaining twelve are already built and on beta, waiting for me to sign in and review them.

The team also built the tooling to implement ADR-084, with step-by-step instructions ready for me to implement.

The beta was rebuilt 15 times, and Lead Developer wrote an update to the tool that promotes builds to beta so that it walks every parent of a merge (instead of just checking one line of history as it had done in the past), to address the problem noted in last week's shipping news about the promotion gate missing a tested commit.

Last week I confessed I was astounded to learn that Arch made 160 architectural rulings in supervising the build. I guess I need to get used to that pace because this week they made 175 rulings.

I oversaw one fresh deployment of the MCP build on Nov 15, working with Piper Alpha (it's their project!) to narrow the scope of its GitHub connector to just the repos chosen.

The clock rule (about not guessing the time) went live on Nov 18 per the CIO. A backtest showed it would have refused 7.7% of past commits and revealed a false-positive, enabling CIO to fix it. No false refusals reported yet since.

## 🎯 Product & experience

What a user can do now that they couldn't last week (as far as we can tell, given that I have not tested any of it yet):

- In Claude, limit the Piper Morgan MCP connector's GitHub access to **just the repos you installed it on**.
- **Disconnect** an integration from the Piper Morgan side with clear indications that the connection remains valid and can still be reconnected. 
- Use **Disconnect All** and get a closing note naming any service where you still need to remove Piper yourself (GitHub, if you connected it with the app or a token, and Notion).
- Understand the plain language in the **Integrations** setting page
- Ask Piper to change something in a GitHub repository you haven't given it access to, and get a plain answer saying so, with where to add that repository (Settings, under Integrations).

Built but not closed yet:
- **Host their own beta** now that a fresh database is built by alembic, not pre-empted by setup. Two copies on one machine no longer share a database: a variable now prefixes every container, network and volume name.

What you can't do yet:
- Get an invitation (still holding).
- Reach a first valuable thing in a first session.

We also codified nine conduct rules for Piper's replies:

1. Look before you say.
2. Every claim has a source you could name.
3. "Done" means confirmed.
4. Be plain about your limits.
5. Numbers come with what was counted.
6. A correction is a claim too.
7. Ask when it matters, not by reflex.
8. Help the person check important things.
9. Decline without leaking.

(These rules sit outside the classifier, so routing is unchanged.)

## 🔬 Methodology & process innovation

I've already devoted enough ink to "don't hand me workarounds" (ADR-084) above, and the clock rule.

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

1. **Tuesdays** (like today) I will publish the Weekly Ship for the sprint week that ended the previous Thursday. This is moving from Wednesdays. The Ship will continue to appear first in the [Shipping News](https://pipermorgan.ai/shipping-news/) on the Piper Morgan website and then gets crossposted to the [Building Piper Morgan newsletter](https://www.linkedin.com/newsletters/building-piper-morgan-7346158338541305856) on LinkedIn.
2. **Thursdays** I will publish an update on the building narrative, focused on moving from beta to production and less on the day-to-day blow-by-blow minutiae of building with this agent team. This is moving from the current twice-weekly Tue/Thu schedule to just running once a week on Thursday. These posts will also continue to appear first on the [Building in Public](https://pipermorgan.ai/blog/) on the website and crossposted to the [Building Piper Morgan publication](https://medium.com/building-piper-morgan/) on Medium and will also now be crossposted to LinkedIn as well.
3. **Weekends** I will publish a single insight post, instead of the two I have been running for about 16 months. These posts will continue to appear first on the canonical blog on my site and then crossposted to both LinkedIn and Medium.

I hope this pace works better for my readers as I expect it will for me.

- **Cadence:** Ship moves to Tuesday from this one. No Thursday narrative in Thanksgiving week (your 11-17 word).

## 📊 Governance & operations

**Operations numbers**

- Updates to beta: 15 (of 16 attempts)
- Signed-in reads on beta: 0
- MCP server deploys: 1
- Issues filed / closed: 44 / 10
- Open Production issues: 297 → 329
- Main CI: two red windows (the morning of 11-17), green at every read after
- Paid model calls by seats: $0

# 🎯 Coming up next week

We finish sprint two, closing as many of the goals as possible:

1. The agents use their new accounts for real: Web signs in to beta with its own test account, a real key confirms the self-hosting fix, we measure the size of Piper's conduct rules and check that they are cached (so they don't add cost to every reply), and an agent makes its first paid model call under the budget cap.
2. Check what's already built on beta while signed in, and close each item that works. CXO makes the call on each one.
3. Finish moving the agents' GitHub work onto their own GitHub account (the last few setup steps are mine), then the memo that lets us resume inviting hosted beta testers.
4. Keys and deploys off my hands: I create one token so the team can deploy the MCP server without me from now on. I also run the restore drill, a timed practice of restoring the production database from a backup onto a throwaway copy, to prove our backups actually work before we promise anything about them.
5. Hitting the new editorial calendar deadlines.

# 🚧 Blockers & asks

Invitations are still on hold until I complete a few more manual steps.

The [waitlist for beta access](https://pipermorgan.ai/try/beta/) remains open. 

# 🔎 This week's learning pattern


## The second reader catches what the first one missed

Multiple times this week one agent double-checked another agent's work and closed gaps:

  - HOST reviewed the script for our database restore drill and passed it with one change. CIO reviewed it again and found more, including that an interrupted run would skip deleting the temporary copy of the database.
  - Arch approved a new check to run before every update to beta. Before merging it, Lead ran the command exactly as written, in a bare setup like the deploy's, and it crashed. As written, it would have blocked every update.
  - Arch caught a CXO sentence about an unknown connection that was untrue for one GitHub path.
  - All three were corrected before merge or serve.

**Pattern:** a second reader *using a different method* catches what the first missed.
**Why it matters:** all three were caught before a user saw them.
**Application:** when you check someone's work, don't repeat their method. Run the command, click through the page, or test the claim against its source, rather than rereading the same text the same way.
- **Related:** ["Over-Checking Pays Dividends"](https://pipermorgan.ai/blog/over-checking-pays-dividends/) and ["Verify at the User Path"](https://pipermorgan.ai/blog/verify-at-the-user-path/), plus our methodology note "Agreement Is Not Replication" (several reviewers agreeing proves little if they all checked the same way).

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #070. Previous: [#069 "Off-Limits by Default"](https://pipermorgan.ai/shipping-news/weekly-ship-069-off-limits-by-default).

*P.S. {yours}* More beta invitations coming soon, I promise!

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of November 13–19, 2026 | Phase: Production, sprint 2, week 1 of 2 (private beta, invitations on hold).**
