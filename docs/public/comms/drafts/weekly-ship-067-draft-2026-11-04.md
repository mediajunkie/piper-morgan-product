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

**▸ Write about**
- Frame it as what a tester can do now that they couldn't on 10-22. The list is below; pick the ones that matter most to a reader.
- The honest-failure lines: Piper says "I couldn't check that" instead of a confident wrong answer.
- The one that isn't fixed: the two-step milestone ask (#2184), named openly as a known issue in the beta letter.
- Optionally, what CXO's rule meant this week: an issue closes only when the person can see the fix, not on a unit test alone.

**▸ Facts** (all served on alpha unless marked)
- **"I couldn't check that"** instead of a confident wrong answer. This covers GitHub, calendar, preferences and documents. "What changed since yesterday?" now says what it checked (#2140). A failed preferences read no longer shows defaults, and Save no longer writes them over real settings (#2154).
- **Trust what Piper says is connected:**
  - Calendar shows as connected only when its box was ticked (#2148).
  - GitHub Disconnect sticks (#2172).
  - A dead GitHub connection can be repaired from Settings (#2018).
- **Document questions get document answers:** analyze one, compare two named uploads, summarize past the 20-upload window (#2132, #2138, #2139).
- **GitHub lists say what they cover:**
  - true counts (#2171);
  - a milestone list no longer says "across all your repositories" (#2194);
  - undated milestones are flagged and asked about (#2199, #2200);
  - a renamed issue shows its new title in the recap (#2201).
- **Deleting is safe:** "Yes" removes the to-do the prompt named, not the previous one (#2169).
- **Standup shows your own work,** not everyone's in a shared repo (#2173), and it names a source that failed instead of showing a free day (#2182).
- **Not yet:** the two-step milestone ask passed on 10-28 and failed on 10-29 (#2184). It's a known issue, and the partner note and the beta letter both name it.
- **CXO** ruled and closed 15 issues, none on a unit test alone, and wrote the words for every honest-failure line.

## 🔬 Methodology & process innovation

**▸ Write about**
- How "more than patching" works in practice: find the cause, list every claim Piper makes, and screen each change against the whole test set before it lands.
- The week's process lesson: a premise passed along without checking it. Five seats repeated "alpha's key is capped", and it was the test workspace's cap. This ties to Thursday's post, "Citation via Hearsay".
- Small fixes that remove a class of error: the send scripts now write their own clock times.
- Optional, candidly: my own miss. My scheduled run died in a restart, I rebuilt it from memory, and dropped the Ship kickoff.

**▸ Facts**
- **Confabulation method** (after your 10-28 word):
  - Arch found the cause: the base prompt asks for an aside on every reply.
  - Lead listed every read claim.
  - Every routing change is now screened on the full test set before it lands. The screen refused a change twice on 10-29, which is it working.
  - The Haiku 5.5 screen ran on 10-30 (about $1.65 across 2,100 requests). Arch ruled it NO-GO as a drop-in: it routed worse than 4.5 (473 vs 488 rows, 75% vs 87% above the consult floor). Piper stays on 4.5 and re-baselines under #2227.
- **The premise relay (10-29):** five seats wrote that alpha's own key was capped and chat was down. It was the test workspace's cap, and Piper has no Anthropic key of its own. It repeats a 10-20 mistake, and all were withdrawn within the hour.
- **CIO:** the staleness re-run measured 11 of 11 seats, and all fixed their lines the same day. `briefing-pointer-check.sh` took gaps from 58 to 42.
- **Guessed clock times** turned up in most seats. Since Thursday, the send scripts stamp the time themselves.
- **Exec's miss:** my cron died in the 10-28 restart, and four runs didn't happen. I rebuilt it from memory and dropped the Ship kickoff. The fix is a skill step plus a LaunchAgent, and every seat now re-arms from a stored prompt.

## 🌍 External relations & community

**▸ Write about**
- A line or two introducing the week's posts, then the list.
- The alpha invitations going out (Mon 10-26).
- Optionally, the site: accessibility at 100, and the Terms page.

**▸ Facts: published in the window** (editorial calendar; all five distributed, matching Comms' review)
- Sat 10-24, insight: ["Mistaking the Inset for the Map"](https://pipermorgan.ai/blog/mistaking-the-inset-for-the-map)
- Sun 10-25, insight: ["A Clean Result Needs a Version Number"](https://pipermorgan.ai/blog/a-clean-result-needs-a-version-number)
- Tue 10-27, building: ["The Caveat That Kept Disappearing"](https://pipermorgan.ai/blog/the-caveat-that-kept-disappearing)
- Wed 10-28, Ship #066: ["Tested on the Real Thing"](https://pipermorgan.ai/shipping-news/weekly-ship-066-tested-on-the-real-thing/)
- Thu 10-29, building: ["Citation via Hearsay"](https://pipermorgan.ai/blog/citation-via-hearsay)

**▸ Facts: other**
- Three alpha invitations sent Mon 10-26, 21:00.
- pipermorgan.ai:
  - Lighthouse Accessibility 100 on all 11 static pages (Web, 10-27);
  - the Terms page live 10-25;
  - the sitemap now lists the blog (433 URLs, all served).

Hero image (Thursday's building post; image link checked live). Keep it as is:

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
