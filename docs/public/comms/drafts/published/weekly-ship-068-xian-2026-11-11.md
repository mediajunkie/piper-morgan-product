---
image: 'piper-ship.png'
alt: 'A child and a crew of robots checking each other''s work on a boat.'
caption: ''
---

# Weekly Ship #068: Whose Connection Is It, Anyway?

*October 30 – November 5, 2026*

This sprint week started with my birthday on which we hit the MVP milestone and included the launch of private beta. One of the key blockers in the home stretch has been ensuring the data privacy for customers in a "multi-tenant" environment (multiple accounts using the same back-end database).

Then one of the first beta testers showed me a screen in the GitHub-connector setup that made me worry about a cross-account authentication leak.

It turned out this was a false alarm related to how a GitHub OAuth app owned by a personal account presents the signup flow, but it did reveal a potential edge-case scenario that could leak credentials. I had already halted beta invitations, and I prepared a heads-up to the first cohort of invitees.

Most of the fixes this week involve hardening the logic such that a connection can only be used by the person who connected it.

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

The team built a class-level guard against tenancy leaks, resisting the urge to patch potential issues one at a time. Also, multiple attempts to improve the router failed to deliver measurable improvement, leaving it unchanged for now.

There was also a three-hour website outage when we exceeded the free tier for pipermorgan.ai at Vercel. We moved to a paid plan, but then realized we could optimize things and revert to a free account after this one month. (Our largest images are now 71% smaller, and docs-only commits skip the build.)

The old alpha.pipermorgan.ai address now redirects to beta.pipermorgan.ai.

There were 18 successful updates to the hosted build and six deploys of the MCP server, with v20 carrying the GitHub guard. Lead Dev closed 32 issues. Main CI went red on at least five of the seven days and got fixed the same day each time.

## 🎯 Product & experience

What a user can do now that they couldn't before this week:

- **Use the beta** at beta.pipermorgan.ai (alpha redirects there since 11-05).
- **Trust the GitHub connection.** The connect screen now reads "Authorize pipermorgan" (the org on GitHub that now owns the connector app), and not my personal GitHub username, `mediajunkie`.
- **Disconnect GitHub and have GitHub break the connection too:** the grant is now revoked at GitHub.
- **Know which account is connected and what to do when it breaks.** The card and toast say "Connected as {login}". A dead grant tells the user to reconnect in Settings, and a failed connect explains why.
- **Ask "what changed?" and get a true answer.** Piper responds without falling back on internal labels, uses "yesterday" accurately for the user's own timezone, and qualifies when it says there is "nothing new" that this is based on their own available records.
- **Communicate naturally about routine GitHub actions.** "Change the title to X" works, and a named milestone gets that milestone. A first "create an issue" asks which repo. "Set my default repository" works. Settings shows the email.
- **Use the Claude connector and get a usable answer:** it says what it searched, and it shows no incorrect fallback projects after a failed attempt to read the project list. (Only listed accounts can connect.)
- **Find the beta on pipermorgan.ai:** The /try/ page updated for private beta with just one way in, pointing to the waiting-list form.

**What a user still can't do:** have a valuable experience in a first session. That's the next sprint's main focus.

## 🔬 Methodology & process innovation

A few times this week information that was partial or incorrect was relayed as fact and then later retracted and updated in the record. Mistakes are inevitable but they always bear investigation for the information they contain about how processes may vary from expectations. I am often impressed by the self-healing abilities the team has developed in an emergent fashion over time.

We're still learning how to work with the Claude classifier that is sometimes rather strict about making me give my permission directly for activities it views as potentially dangerous and that I consider routine and relatively safe given my own infrastructure.

I've backed off from reworking AI-written early drafts as I found that it was making me inattentive and I was allowing things to go out that I could easily write better and more naturally in my own voice.

For this entire sprint week all blog posts and the weekly ship followed my "AI prompts human" pattern, in which an agent provides me with the agreed upon scaffold and potential outline along with relevant researched and verified facts, along with suggestions to consider. That gives me enough to write something I can feel comfortable putting my name to, as I am doing right now.

After the first blog post written this way (we still had quite a few working drafts in the pipeline to finish well after this decision was made a few weeks ago), I told the agents, who were trying yet again to do things the way I want, "this first test … went well."

## 🌍 External relations & community

The first tranche of private-beta invitation emails went out and the [website](https://pipermorgan.ai/try/) is collecting wait-listers even now.

Keeping up with the publishing schedule has taken extra effort, but I hope to get ahead in the pipeline again soon:

- Sat 10-31, insight: ["Build the Instrument Before the Theory"](https://pipermorgan.ai/blog/build-the-instrument-before-the-theory)
- Sun 11-01, insight: ["Check the Machine First"](https://pipermorgan.ai/blog/check-the-machine-first)
- Tue 11-03, building: ["The Unguarded Entrance"](https://pipermorgan.ai/blog/the-unguarded-entrance)
- Wed 11-04, Ship #067: ["What Piper Didn't Check"](https://pipermorgan.ai/shipping-news/weekly-ship-067-what-piper-didnt-check)
- Thu 11-05, building: ["Don't Overpromise"](https://pipermorgan.ai/blog/dont-overpromise)

[![A translucent AI safety inspector sheepishly touches their bare head as a helmeted worker points it out. The inspector’s hard hat sits beside a clipboard on a small table.](https://pipermorgan.ai/assets/blog-images/the-unguarded-entrance.webp)](https://pipermorgan.ai/blog/the-unguarded-entrance)
*"Some safety inspector you are!"*


## 📊 Governance & operations

**The numbers**

- Open MVP issues: 2 → 0
- Updates to alpha: 18
- MCP server deploys: 6
- Issues filed / closed: 75 / 83
- Open Production issues: 228 → 252
- Website downtime: about 3 hours
- Main CI: red on at least 5 of 7 days
- Spend: 45.4M tokens in, 1.3M out ($37.61)

As we got close to the MVP milestone, we didn't stop discovering new issues that will need attention. However, I was ruthless about only allowing blocker bugs into that final sprint. This explains why the open count in the Production milestone we are working on now grew by 24. Interestingly, by the end of the week this milestone also had 194 issues that were already closed, many of them before it officially started, as a consequence of addressing MVP issues.

# 🎯 Coming up next week

For the Production milestone I'm moving the team to two-week sprints starting from Friday, November 13. I think this will be an easier planning (and attention) cadence for me and the breakneck urgency to get to beta has eased a bit now, making me feel more comfortable taking my time with decisions.

The first sprint's goal is to ensure a new account accomplishes one valuable thing in its first session.

The Shipping News will continue to feature weekly updates (we don't call it the Weekly Ship for nothing), with mid-sprint updates alternating with closeouts.


# 🚧 Blockers & asks

Invitations are on hold until I do about 20 minutes of testing with a follow-up about eight hours afterward to ensure the GitHub connector system is fully isolated as intended, and until our email domain has the mail records that keep invitations out of spam folders.

If you'd like to join the beta waiting list, you're welcome to sign up at pipermorgan.ai/try/.

# 🔎 This week's learning pattern

## Guard against a class of problems

Before building a guard to prevent a specific problem from occurring, investigate first to see whether that problem is merely a single example of an entire class of problems that may each present themselves under slightly different circumstances. If this is the case, each one-off guard will fail to protect against other issues in the class and end up making the problem harder to detect, diagnose, and prevent at the correct level of abstraction.

The correct solution is a class-wide guard that addresses the shared root issue and not the hallmarks of each individual symptom.

Our example this week is the isolation check. It looks for code that reads a setting for the whole deployment when it should really just read it for one person. Earlier cases had each been fixed one at a time where they showed up, and a proposed class-wide check split off in August was never built. On its first run the new check flagged 50 places to check (!). Most were fine, and the list is now down to 11.

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #068. Previous: [#067 "What Piper Didn't Check"](https://pipermorgan.ai/shipping-news/weekly-ship-067-what-piper-didnt-check).

*P.S. Overjoyed to be in beta and to already be getting actionable feedback from real people. I appreciate anyone who has expressed interest in exploring the product or even just encouraged me on this wild educational journey.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of October 30 – November 5, 2026 | Phase: Production, private beta (invitations on hold).**
