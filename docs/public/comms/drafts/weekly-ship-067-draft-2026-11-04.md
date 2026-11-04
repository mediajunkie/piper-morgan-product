---
image: 'piper-ship.png'
alt: 'A child and a crew of robots checking each other''s work on a boat.'
caption: ''
---

<!--
SCAFFOLD for xian to write (Exec, 2026-11-04). Nothing below is prose to keep. Each section has
the facts it can draw on, with sources, and a [xian: ...] slot. Delete the fact bullets as you
write. Facts come from the nine workstream reviews (10-30), my week review
(https://claude.ai/artifact/4Le3ZyacNXUqo19SQh5GpT), the editorial calendar, and the counts I ran.
Window: Fri 10-23 to Thu 10-29. Publishing Wed 11-04, a week late, so "Coming up next week" can
say what actually happened.
After you write: Exec edits, Comms fact-checks against these bullets and runs the template audit,
and Docs updates the calendar row.
-->

# Weekly Ship #067: What Piper Didn't Check

<!-- Title: xian's pick, 11-04 13:30. -->

*October 23–29, 2026*

[xian: opening, 2–3 paragraphs]

<!-- Facts for the opening:
- Last week had four goals, and three were met. All three must-closes closed Fri 10-23. You sent the three alpha
  invitations Mon 10-26 at 21:00. The GitHub App was installed 10-23. The fourth, the 10-30 MVP target, was
  in reach at week's end: the gate was down to #1386 alone.
- The gate went from 6 open to 2 (10 closed, 7 admitted, 1 moved to known issues; PPM's ledger).
- The product thread was honesty about what Piper actually read. A failed read now says so, instead
  of showing "none". A write goes only where the user said. Your 10-28 word: the confabulations
  "require more than patching".
- Continuity: #066 was "Tested on the Real Thing".
- Optional, since you're writing it a week on: today's advisor beta session (onboarding to first value)
  is the honest next chapter. Keep any outside detail out; the advisor may be named. -->

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

[xian]

<!-- Facts:
- Alpha was updated 24 times (successful promotion dispatches, 10-23 to 10-29 PT); 10 more failed or were
  refused, and alpha was unchanged each time.
- Alpha recovers its own database (#2085, #2146). The restarter passed its tests: down 2 min 6 s with you
  at the keyboard, then healthy 9 min 15 s after a restart nobody touched. No unplanned database outages.
- Deploys now pull the exact image that was tested (#2177, #2181).
- Failed-read surfaces: 156 listed (69 green, 59 red, 28 exempt). The forcing test's known-red list only
  falls: 32 → 14 in the window.
- Arch: 72 rulings, each read from source. Four new rules: a write goes only to a target the user named;
  the user in the current turn, never a stored offer's user; a failed read is stated; catalog order
  comes from a ledger.
- Lead: 34 closed (14 with served evidence). Read-claim inventory for the confabulation class (#2042).
- Main CI was red on 5 of 7 days, fixed the same day each time; the landing gate now runs every test directory CI runs. -->

## 🎯 Product & experience

[xian]

<!-- Facts, as "what a user can do now that they couldn't on 10-22" (all served on alpha):
- Hear "I couldn't check that" instead of a confident wrong answer: GitHub, calendar, preferences
  and documents (#2140). A failed preferences read no longer shows defaults, and Save no longer writes
  defaults over real settings (#2154).
- Trust what Piper says is connected: Calendar only when its box was ticked (#2148); GitHub
  Disconnect sticks (#2172); a dead GitHub connection can be repaired from Settings (#2018).
- Ask about documents and get document answers: analyze, compare two named uploads, summarize past
  the 20-upload window (#2132, #2138, #2139).
- GitHub lists that say what they cover: true counts (#2171), a milestone list that no longer says
  "across all your repositories" (#2194), undated milestones flagged and asked about (#2199, #2200),
  renamed issues shown by their new title in the recap (#2201).
- "Yes" to a delete removes the to-do the prompt named (#2169).
- A standup that shows your own work, not everyone's in a shared repo (#2173), and that names a failed source (#2182).
- Not yet: the two-step milestone ask (#2184) passed 10-28 and failed 10-29. It's a known issue, named in
  the partner note and the beta letter.
- CXO ruled and closed 15 issues, none on a unit test alone, and wrote the words for each honest-failure line. -->

## 🔬 Methodology & process innovation

[xian]

<!-- Facts:
- The confabulation method after your 10-28 word: Arch diagnosed the cause (the floor prompt asks for an
  aside on every reply), Lead inventoried every read claim, and each router change is screened
  against the full corpus before it lands. Rule 7 said no twice on 10-29, which means the screen was working.
- CIO: the staleness re-run measured 11 of 11 seats, and all fixed their lines the same day.
  `briefing-pointer-check.sh` took gaps from 58 to 42.
- Guessed clock times kept turning up across seats; the send scripts now write the time themselves.
- My own miss: my cron died in the 10-28 restart, and when I rebuilt it from memory I dropped the
  Ship kickoff. The fix is a skill step plus a LaunchAgent, and every seat now re-arms from a stored prompt. -->

## 🌍 External relations & community

[xian: a line or two, then the list]

<!-- Published in the window (editorial calendar, 5, all distributed; Comms' review agrees):
- Sat 10-24, insight: "Mistaking the Inset for the Map" https://pipermorgan.ai/blog/mistaking-the-inset-for-the-map
- Sun 10-25, insight: "A Clean Result Needs a Version Number" https://pipermorgan.ai/blog/a-clean-result-needs-a-version-number
- Tue 10-27, building: "The Caveat That Kept Disappearing" https://pipermorgan.ai/blog/the-caveat-that-kept-disappearing
- Wed 10-28, Ship #066: "Tested on the Real Thing" https://pipermorgan.ai/shipping-news/weekly-ship-066-tested-on-the-real-thing/
- Thu 10-29, building: "Citation via Hearsay" https://pipermorgan.ai/blog/citation-via-hearsay
Also: three alpha invitations sent 10-26. pipermorgan.ai: Lighthouse Accessibility 100 on all 11
static pages (Web, 10-27); the Terms page live 10-25; the sitemap lists the blog (433 URLs). -->

[![Three scholars proudly display papers citing “M-45,” while a fourth discovers that the actual source warns against mistaking shared citations for independent evidence.](https://pipermorgan.ai/assets/blog-images/citation-via-hearsay.webp)](https://pipermorgan.ai/blog/citation-via-hearsay)
*"Has anyone actually read this?"*

<!-- Hero: the Thursday building post. Image URL checked live (200) 13:2x 11-04; alt text and caption
from the calendar row. -->

## 📊 Governance & operations

[xian]

<!-- Facts (metrics as bullets, never a table):
- Issues: 75 opened, 62 closed (gh-week-counts.py, Pacific week).
- Gate: 6 → 2 open.
- Alpha updates: 24.
- Spend: 55.1M tokens in, 1.1M out (from your Console screenshots). Almost all of it was two screening days: 10-23 at 42.4M
  and 10-29 at 10.9M. 10-24 to 10-28 together came to 0.69M. The Console shows tokens, not dollars.
- Holds and dispatch: from 10-28, auto mode refused Lead's promotion command, so you dispatched five. Since
  then, your 11-03 allow line lets Lead promote under the grant, which has happened four times since 11-03.
- A premise relayed without checking it (10-29): five seats wrote that alpha's key was capped. It was
  the test workspace's cap. All were withdrawn within the hour. -->

# 🎯 Coming up next week

[xian]

<!-- What actually happened 10-30 to 11-05 (you're writing after it):
- MVP closed: v0.9.0.0 tagged; the public site no longer invites people to alpha; the waiting list is
  the one way in. The first Production sprint is set (22 issues, about 30% held back for partner reports).
- The first beta session (today, the advisor) moved the focus to onboarding: getting a new person to one
  valuable thing in their first session. You said this should shape the planning talk.
- The sprint-cadence question (two-week sprints, or plan two weeks out and revisit weekly) is open. -->

# 🚧 Blockers & asks

[xian]

<!-- Candidates: none public-facing that need naming; or an ask for beta testers via the waiting list
(/try/beta/). -->

# 🔎 This week's learning pattern

## [xian: noun-phrase pattern name]

<!-- Candidate from the week: "Check the premise before you relay it". The 10-29 cap relay repeats
10-20, and fits Thursday's "Citation via Hearsay". Or "Say what you didn't read", the honesty thread. -->

**Discovery**: [xian]

**Example from this week**: [xian]

**Why it matters**: [xian]

**Application beyond this week**: [xian]

**Related patterns**: Last week's "A safeguard you've only read is a guess"; [xian]

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #067. Previous: [#066 "Tested on the Real Thing"](https://pipermorgan.ai/shipping-news/weekly-ship-066-tested-on-the-real-thing/).

*P.S. [xian]*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of October 23–29, 2026 | Phase: [xian: e.g. MVP closure into private beta]**
