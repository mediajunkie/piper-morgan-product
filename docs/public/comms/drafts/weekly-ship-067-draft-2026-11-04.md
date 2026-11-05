---
image: 'piper-ship.png'
alt: 'A child and a crew of robots checking each other''s work on a boat.'
caption: ''
---

# Weekly Ship #067: What Piper Didn't Check

*October 23–29, 2026*

Until this week, Piper couldn't tell the difference between a blank and answer and a failure to read the data. The MVP gate went from 6 open issues to 2 with one day left to the latest milestone goal date. The last set of alpha invitations also went out. The next invitations to go out should be for the beta. Along the way, I ruled that we couldn't just patch confabulations and this led to a methodology update.

The team met three of the four goals for this week's sprint:

- The three must-closes closed Friday, 10/23.
- The alpha invitations went out Monday, 10/26.
- The GitHub app (for integration) was installed 10/23.

The fourth goal, to close the MVP milestone, would have to happen on Friday, the first day of the following sprint. Along the way the alpha build was updated 24 times.

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

The Alpha now runs itself more safely. It restarts its own database, and deploys from the correct tested build. We listed every place in the code that a failed read could be misreported as a "nothing" response and set up a test to keep that list shrinking.

Arch wrote some new rules: Piper may only write where the user indicated and must report a failed read. Lead Developer closed 34 issues. Main CI went red on five of the seven days of the week, but was fixed the same day each time. Lead's gate now runs every test directory CI runs.

## 🎯 Product & experience

What a user can do on alpha now that they couldn't a week ago:

- **Hear "I couldn't check that" instead of a confident wrong answer.** When a GitHub, calendar, preferences or document read fails, Piper now says so, where it used to report "no issues," "no activity" or an empty day. "What changed since yesterday?" now says what it actually checked. A failed preferences read no longer shows the defaults, and pressing Save no longer writes those defaults over your real settings.
- **Trust what Piper says is connected.** Calendar shows as connected only when you ticked its box. GitHub's Disconnect sticks. A dead GitHub connection can be repaired from Settings without our help.
- **Ask about documents and get answers about documents.** Analyze an upload, compare two uploads by name, or summarize past the 20 most recent.
- **Read GitHub lists that say what they cover.** Counts are true. A milestone's list no longer claims to cover all your repositories. Milestones without a date are flagged, Piper asks which one you mean, and the next turn reads the one you named. A renamed issue shows its new title in the session recap.
- **See your own work in your standup,** not everyone's in a shared repo. If a source fails, the standup names it instead of showing a free day.
- **Delete safely.** Saying "yes" to a delete removes the to-do the prompt named, not the one before it.

Not yet: asking for a milestone's issues in two steps passed on Wednesday and failed on Thursday. It's a known issue, and the beta letter names it. And the first time you ask to create an issue, Piper now asks which repository. That was live by Thursday evening but passed its check on Friday, so it belongs to next week.

Also, CXO made a rule that we only close an issue when a person can see the fix, not based on a unit test alone.



## 🔬 Methodology & process innovation

When I challenged the team to stop trying to solve confabulation problems by patching, we adopted this approach:

- Find the cause. In this case it was the way the base prompt asked for an aside with each reply, and those asides were adding unchecked noise
- List every claim Piper makes
- Screen each change against the whole test set before accepting it

The screen already refused a change twice on 10/29, working as intended.

The team learned another tough lesson in verifying assumptions before passing the along. This type of issue and the commitment to transcend it continues to recur at various level of abstraction throughout the project. 

One small fix that removes an entire class of errors: the send scripts now write their own clock times.

We also recognized a weakness in the process that drives Exec's weekly review process with the whole team that feeds into our planning and these Shipping News updates, and fixed it, so that Exec no longer needs to "remember" to send out the reminder memos to the team.


## 🌍 External relations & community

I maintained the established publishing cadence and sent out the last set of alpha invitations, including one going to reader who raised their hand a few weeks back. We also added a Terms page to the website and are maintaining a high accessibility score.

- Sat 10-24, insight: ["Mistaking the Inset for the Map"](https://pipermorgan.ai/blog/mistaking-the-inset-for-the-map)
- Sun 10-25, insight: ["A Clean Result Needs a Version Number"](https://pipermorgan.ai/blog/a-clean-result-needs-a-version-number)
- Tue 10-27, building: ["The Caveat That Kept Disappearing"](https://pipermorgan.ai/blog/the-caveat-that-kept-disappearing)
- Wed 10-28, Ship #066: ["Tested on the Real Thing"](https://pipermorgan.ai/shipping-news/weekly-ship-066-tested-on-the-real-thing/)
- Thu 10-29, building: ["Citation via Hearsay"](https://pipermorgan.ai/blog/citation-via-hearsay)

[![Three scholars proudly display papers citing “M-45,” while a fourth discovers that the actual source warns against mistaking shared citations for independent evidence.](https://pipermorgan.ai/assets/blog-images/citation-via-hearsay.webp)](https://pipermorgan.ai/blog/citation-via-hearsay)
*"Has anyone actually read this?"*

## 📊 Governance & operations

**▸ Write about**
- The numbers, as a bullet list (never a table).
- Spend: almost all of it came from two days of screening runs.
- Releasing without bottlenecks: you were dispatching every promotion by hand, and now Lead can, under your grant.

**▸ Facts**
- **Issues:** 75 opened, 62 closed (gh-week-counts.py, Pacific week).
- **MVP gate:** 6 → 2 open.
- **Alpha updates:** 24.
- **Spend:** 55.1M tokens in, 1.1M out (your Console screenshots; the Console shows tokens, not dollars).
  - 10-23: 42.4M, router screens.
  - 10-29: 10.9M, rule-7 screens.
  - 10-24 to 10-28 together: 0.69M.
- **Promotions:** from 10-28, auto mode refused Lead's promotion command, so you dispatched five yourself. Since your 11-03 allow line, Lead has promoted six times without you (after this window).
- **Database outages:** 0 unplanned.

# 🎯 Coming up next week

**▸ Write about** (the week of 10-30 to 11-05, already mostly lived)
- MVP closed, and alpha became private beta.
- The first beta session, and what it taught: onboarding to a first valuable moment comes before more plumbing.
- The planning question you're weighing: two-week sprints, or plan two weeks out and revisit weekly.

**▸ Facts**
- **v0.9.0.0 tagged.** The public site no longer invites people to alpha; the waiting list (/try/beta/) is the one way in.
- **The first Production sprint is set:** 22 issues, with about 30% held back for partner reports.
- **The first beta session (11-04, with your advisor):**
  - 12 findings filed (#2267–#2278).
  - The theme: getting a new person to one valuable thing in their first session.
  - PPM has an onboarding-to-first-value proposal for the planning talk.
- **The GitHub approval screen** looked like Piper was connecting the tester as you. Investigating and fixing it the same day is a good example of the week's theme. Status:
  - Lead's guard is live (#2266).
  - Piper's link to GitHub names no account.
  - The census so far shows no crossing.
  - The app moves to an organization so the screen names the org.
  - Include this only if you want it public. It's still being confirmed.

# 🚧 Blockers & asks

**▸ Write about**
- Probably none that are public-facing. Or an ask: people interested in the private beta can join the waiting list at https://pipermorgan.ai/try/beta/.

# 🔎 This week's learning pattern

## [Pattern name, a noun phrase]

**▸ Candidates**
- **"Check the premise before you relay it."** The 10-29 key-cap relay repeated 10-20, and it echoes Thursday's "Citation via Hearsay".
- **"Say what you didn't read."** The honesty thread; it fits the title most closely.

**▸ Facts for the example**
- 10-29: five seats relayed that alpha's key was capped. It was the test workspace's cap, and all were withdrawn within the hour.
- Or: a failed GitHub read used to come back as "no issues"; now it says "I couldn't check" (#2140).

**Discovery**: [one sentence]

**Example from this week**: [a specific instance]

**Why it matters**: [its impact, and what it addresses]

**Application beyond this week**: [how to apply it elsewhere]

**Related patterns**: Last week's "A safeguard you've only read is a guess"; [others]

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #067. Previous: [#066 "Tested on the Real Thing"](https://pipermorgan.ai/shipping-news/weekly-ship-066-tested-on-the-real-thing/).

*P.S. [A key takeaway or a personal note]*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of October 23–29, 2026 | Phase: [e.g. MVP closure into private beta]**
