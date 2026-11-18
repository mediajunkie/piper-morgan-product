---
image: 'the-server-key-is-not-a-real-concept-ef13a6ab-ad10-4ae4-806d-bf09bb466add.jpg'
alt: 'An AI locksmith secures a coin purse attached to a vending machine while a puzzled proprietor gestures toward it and a customer waits with their own coin.'
caption: '"Who gave it a wallet?"'
---

# Weekly Ship #069: Off-Limits by Default

*November 6–12, 2026*

When I found out agents were using the keychain on my home server as an authentication fallback I declared it off limits. Instead of relying on a rule each agent would have to remember each time, we made this constraint the default in code. I've also moved Piper Morgan's GitHub connection onto its own published GitHub App, so a tester now chooses which repositories Piper can see, instead of granting it every repository their account can reach.

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

After three separate fallback reads of the keychain on Amber (my home server), we first fixed each case on its own, till we refactored to move the fix to where each path has to go (the credential store's default). An agent can only use my keychain if `PIPER_CREDENTIAL_STORE=keychain` is set, and the project's CLAUDE.md forbids any agent from setting it directly.

Moving to a GitHub App also narrowed what Piper can reach: a tester chooses the repositories. There is more to do. Issue and PR searches still read every repository the tester's account is assigned in, and some reads can still answer about a public repository the App isn't installed on.

Piper Alpha noticed the MCP app had fallen a week behind but the item was not rising to my attention. Chief Innovation Officer discovered that the gate guarding promotion was refusing a build that had passed its tests. With a merge commit on top, the gate followed only one line of history back and never found the tested commit.

I was also somewhat astonished to learn that Chief Architect made 160 rulings this week, working on multiple ADRs.

## 🎯 Product & experience

What a user can do now they couldn't do a week ago:

- **Pick a todo after getting a list back:** "complete the second one", "delete the first two" and "complete the X todo" act on the lines just shown. When the words fit more than one line, Piper asks which. With no list shown, it asks rather than guessing.
- **Ask about a repo and get a real response:** before, the answer could be "I don't see that document". Now it asks which repo when there are several, and a past-due milestone is called overdue. Feedback from our advisor, Ted Nadeau, brought this scenario to light, and every one of his test questions now gets a real answer.
- **Change or forget a learned preference,** with consent before forgetting.
- **Add a repo to a project without a "yes" loop,** more easily find Integrations in a reorganized Settings, and sign in successfully with a wrong-case email (usually).
- **Stay signed in under load:** past 20 concurrent requests, sign-in no longer refuses everyone.
- **Get invitation mail that passes SPF, DKIM and DMARC** as I finally spruced up the DNS settings for mail domains.

What you can't do yet:
- Complete a todo by pronoun ("mark them done").
- Run Piper, easily, on your own computer.
- Get an invitation to the beta.
- Definitely reach a "first valuable" thing in your first session.

## 🔬 Methodology & process innovation

I got tired of the agents frequently guessing the time instead of checking, or guessing the time and then checking and then proudly telling me they had been wrong but they fixed it. I have advised agents to "always check the clock time before asserting it" but not in any way that had stuck, so we're making it a requirement.

This week Docs, CIO, PA, PPM, Comms, Lead and Exec each reported guessing the time at least once. The after-the-fact "stamp check" was catching it every time, but I was getting weary of the repeated shuffle. Soon they'll check the time as a matter of course, removing a tiny annoyance for me.

Meanwhile, we're almost done migrating all the agents to the new mail repo that is separate from the product repo. 

## 🌍 External relations & community

I kept up the current publishing pace with some effort, several posts going live in the evening. I've also decided to update the publishing schedule starting next week. This week we published the following, and accidentally labeled one of the weekend posts as part of the building narrative instead of an insight piece:

- Sat 11-07, insight: ["At Long Last, Beta"](https://pipermorgan.ai/blog/at-long-last-beta)
- Sun 11-08, insight: ["When Accuracy Scores Worse"](https://pipermorgan.ai/blog/when-accuracy-scores-worse)
- Tue 11-10, building: ["Never Green in a Thousand Runs"](https://pipermorgan.ai/blog/never-green-in-a-thousand-runs/)
- Wed 11-11, Ship #068: ["Whose Connection Is It, Anyway?"](https://pipermorgan.ai/shipping-news/weekly-ship-068-whose-connection-is-it-anyway)
- Thu 11-12, building: ["The Server Has No Key"](https://pipermorgan.ai/blog/the-server-has-no-key)

[![An AI locksmith secures a coin purse attached to a vending machine while a puzzled proprietor gestures toward it and a customer waits with their own coin.](https://pipermorgan.ai/assets/blog-images/the-server-has-no-key.webp)](https://pipermorgan.ai/blog/the-server-has-no-key)
*"Who gave it a wallet?"*

## 📊 Governance & operations

**Operations numbers**

- Updates to beta: 32
- MCP server deploys: 1
- Issues filed / closed: 70 / 26
- Open Production issues: 252 → 297
- Keychain reads: 3, then opt-in
- Main CI: red on at least 3 of 7 days
- Spend: $33.38 (29,317,890 tokens in, 702,410 out)

Note that spend is nominal, coming from a monthly $200 credit we get on the "Ultra" Claude account that expires if not used. We still need to track so we don't go over without meaning to. Almost all of it was spent in testing during the first three days of the week. 

Production's open issue count grew by 45, mostly derived from the beta session's findings as well as the GitHub work.

# 🎯 Coming up next week

For this beta push to production, I have moved the team to two-week sprints. This will give us a little more breathing room in sprint planning and a more typical cadence. I approved these goals for this sprint:

1. Finish the GitHub move: My manual testing of the new repositories card is required for this.
2. Agents can test without requiring my hands-on steps so often. 
3. Close four issues with the Todo feature
4. Close four issues with the setup wizard
5. Make projects work in chat: adding a task to a project, and asking what's in one.
6. Enable convenient self-hosting for beta testers who want to do it that way.
7. Make sure Piper Morgan knows itself, what it can do, how it works, and the product's ethos as well as the team building it does.

# 🚧 Blockers & asks

Beta invitations remain on hold until the per-user isolation epic and the GitHub "classic-scope" issue are done. The search gap for GitHub issues and pull requests is also still open.

Note: We expect to resume inviting beta testers soon. Sign up at pipermorgan.ai/try/beta/ to join the wait list.

# 🔎 This week's learning pattern

## Fix it at the chokepoint

As noted above, we found three places where agents were reading my keychain (a server start, a smoke test and a check script) and initially patched each case where it happened. Then we got wise and changed the default in the one place every path passes through.

We have realized the rules don't always get remembered, and patched scripts don't help the next script we find with the problem. Changing the default where every path goes through covers all cases. If the default is off-limits, we don't have to rely on agents remembering each time. 

To apply this pattern to your own work, once you notice a fix being applied to two different surfaces, look for the common chokepoint before you have to write a third fix.

**Related patterns:** Weekly Ship #068's "Guard against a class of problems" (the same idea, for tenancy).

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #069. Previous: [#068 "Whose Connection Is It, Anyway?"](https://pipermorgan.ai/shipping-news/weekly-ship-068-whose-connection-is-it-anyway).

*P.S. Getting real interest from peers who want to try Piper Morgan in their real work or their own businesses. Exciting and a bit scary!*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of November 6–12, 2026 | Phase: Production, private beta (invitations on hold).**
