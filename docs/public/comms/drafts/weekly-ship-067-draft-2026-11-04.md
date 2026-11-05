---
image: 'piper-ship.png'
alt: 'A child and a crew of robots checking each other''s work on a boat.'
caption: ''
---

# Weekly Ship #067: What Piper Didn't Check

*October 23–29, 2026*

Until this week, Piper couldn't tell the difference between a blank answer and a failure to read the data. The MVP gate went from 6 open issues to 2 with one day left to the latest milestone goal date. The last set of alpha invitations also went out. The next invitations to go out should be for the beta. Along the way, I ruled that we couldn't just patch confabulations and this led to a methodology update.

The team met three of the four goals for this week's sprint:

- The three must-closes closed Friday, 10/23.
- The alpha invitations went out Monday, 10/26.
- The GitHub app that lets the agents work in the repository was installed 10/23.

The fourth goal, to close the MVP milestone, would have to happen on Friday, the first day of the following sprint. Along the way the alpha build was updated 24 times.

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

The Alpha now runs itself more safely. It restarts its own database, and deploys from the correct tested build. We listed every place in the code that a failed read could be misreported as a "nothing" response and set up a test to keep that list shrinking.

Arch wrote some new rules: Piper may only write where the user indicated and must report a failed read. Lead Developer closed 34 issues. Main CI went red on five of the seven days of the week, but was fixed the same day each time. Lead's gate now runs every test directory CI runs.

## 🎯 Product & experience

What a user can do on alpha now that they couldn't a week ago:

- **Hear "I couldn't check that" instead of a confident wrong answer.** When a GitHub, calendar, preferences or document read fails, Piper now says so, where they used to report "no issues," "no activity" or an empty day. "What changed since yesterday?" now says what it actually checked. A failed preferences read no longer shows the defaults, and pressing Save no longer writes those defaults over your real settings.
- **Trust what Piper says is connected.** Calendar shows as connected only when you ticked its box. GitHub's Disconnect sticks. A dead GitHub connection can be repaired from Settings without our help.
- **Ask about documents and get answers about documents.** Analyze an upload, compare two uploads by name, or summarize past the 20 most recent.
- **Read GitHub lists that say what they cover.** Counts are true. A milestone's list no longer claims to cover all your repositories. Milestones without a date are flagged, Piper asks which one you mean, and the next turn reads the one you named. A renamed issue shows its new title in the session recap.
- **See your own work in your standup,** not everyone's in a shared repo. If a source fails, the standup names it instead of showing a free day.
- **Delete safely.** Saying "yes" to a delete removes the to-do the prompt named, not the one before it.

Not yet: asking for a milestone's issues in two steps passed on Wednesday and failed on Thursday. It's a known issue, and the beta letter names it. And the first time you ask to create an issue, Piper now asks which repository. That was live by Thursday evening but passed its check on Friday, so it belongs to next week.

Also, CXO made a rule that we only close an issue when a person can see the fix, not based on a unit test alone.

## 🔬 Methodology & process innovation

When I challenged the team to stop trying to solve confabulation problems by patching, we adopted this approach:

- Find the cause. In this case it was the way the base prompt asked for an aside with each reply, and those asides were adding unchecked noise.
- List every claim Piper makes.
- Screen each change against the whole test set before accepting it.

The screen already refused a change twice on 10/29, working as intended.

The team learned another tough lesson about checking an assumption before passing it along. On 10/29, five agents relayed that alpha's API key had hit its cap and chat was down for everyone. It was the test workspace's cap, and Piper has no key of their own. All five corrections came within about fifteen minutes. This kind of mistake, and our commitment to getting past it, keeps recurring at different levels of the project.

One small fix that removes an entire class of errors: the send scripts now write their own clock times.

We also recognized a weakness in the process that drives Exec's weekly review with the whole team, which feeds into our planning and these Shipping News updates, and fixed it, so that Exec no longer needs to "remember" to send out the reminder memos to the team.

## 🌍 External relations & community

I maintained the established publishing cadence and sent out the last set of alpha invitations, including one going to a reader who raised their hand a few weeks back. We also added a Terms page to the website and are maintaining a high accessibility score.

- Sat 10-24, insight: ["Mistaking the Inset for the Map"](https://pipermorgan.ai/blog/mistaking-the-inset-for-the-map)
- Sun 10-25, insight: ["A Clean Result Needs a Version Number"](https://pipermorgan.ai/blog/a-clean-result-needs-a-version-number)
- Tue 10-27, building: ["The Caveat That Kept Disappearing"](https://pipermorgan.ai/blog/the-caveat-that-kept-disappearing)
- Wed 10-28, Ship #066: ["Tested on the Real Thing"](https://pipermorgan.ai/shipping-news/weekly-ship-066-tested-on-the-real-thing/)
- Thu 10-29, building: ["Citation via Hearsay"](https://pipermorgan.ai/blog/citation-via-hearsay)

[![Three scholars proudly display papers citing “M-45,” while a fourth discovers that the actual source warns against mistaking shared citations for independent evidence.](https://pipermorgan.ai/assets/blog-images/citation-via-hearsay.webp)](https://pipermorgan.ai/blog/citation-via-hearsay)
*"Has anyone actually read this?"*

## 📊 Governance & operations

**The numbers**

- Open MVP issues: 6 → 2
- Updates to alpha: 24
- Unplanned database outages: 0
- Main CI: Red on 5 of 7 days
- Spend: 55.1M tokens in, 1.1M out

Almost all of the spend came from two days of screening runs.

# 🎯 Coming up next week

Since Thursday, the MVP closed on Friday, which ended the alpha, and the private beta began with Saturday's invitations. I am considering moving to more conventional two-week sprints for the Production milestone, to make planning easier.

The first Production sprint is set: 22 issues, with about 30% held back for partner reports.

# 🚧 Blockers & asks

No blockers right now. The public site no longer invites people to alpha, but there is a path now to [sign up for the beta waiting list](https://pipermorgan.ai/try/beta/).

# 🔎 This week's learning pattern

## Say what you didn't read

**Discovery**: Don't report a failed read as a deliberate "None"-type reply. Nobody is going to trust an assistant who reports something as missing or absent just because they failed to look for it properly.

**Example from this week**: Until this week, if Piper failed while trying to look up your GitHub issues, they would tell you that you had "no issues" with no awareness that this was false. Now Piper knows to tell you "I couldn't check."

**Application beyond this week**: Any check that can fail needs a failure answer of its own, separate from the empty one. The same goes for people. "I didn't look" and "there's nothing there" are different reports, and a team that blurs them builds on gaps it can't see.

**Related patterns**: Last week's "A safeguard you've only read is a guess," and this week's posts "Mistaking the Inset for the Map" and "Citation via Hearsay."

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #067. Previous: [#066 "Tested on the Real Thing"](https://pipermorgan.ai/shipping-news/weekly-ship-066-tested-on-the-real-thing/).

*P.S. There are times I never thought I'd get this close to a real beta release. I am infinitely grateful to the people who have followed along and encouraged on the way throughout this wild rollercoaster ride.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of October 23–29, 2026 | Phase: MVP closure on the cusp of private beta.**
