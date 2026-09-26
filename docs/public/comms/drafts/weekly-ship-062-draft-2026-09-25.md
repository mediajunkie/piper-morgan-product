---
image: 'weekly-ship-062-draft-2026-09-25-the-alarm-that-had-been-working-all-along.webp'
alt: 'A luminous AI guide cheerfully points toward a missing bridge while a wary traveler signals “stop,” her manuscript safely stowed in the open car.'
caption: '"Agreed. That bridge is definitely missing! Please go ahead."'
---

# Weekly Ship #062: Says What It Can Do

*September 18–24, 2026*

This week the team asked if the product's interface will say only what the system underneath can actually back up.

A new alpha tester spent the window unable to get past the very first screen of signup — a working install incorrectly told the user that its own database and cache were down, and to go run a command that makes no sense on a hosted instance. An offer the assistant could ask but not actually carry out, a "the source is unavailable" line was invented for a source that was never even checked, a due date was rendered in the wrong timezone. Every fix for these issues shared one rule: don't let the interface claim more than the system can stand behind.

# 🚀 Shipped this week

## What a user can do now that they couldn't a week ago

- **Sign up.** The setup wizard's first screen hard-blocked every new account on a real, working install, because a failed status check silently rendered as "everything is down." Three stacked causes, found and fixed the same day, verified live in a fresh browser through to the next screen. Before this fix, the planned alpha invite would have sent every recipient to a dead end.
- **Get a "yes" that means something.** The floor could pose an offer — "want me to send that?" — with nothing armed to actually do it if the user agreed. Now it may suggest freely, but it may only *ask* when the action is really wired up this turn, and the wording of the ask has to match what would actually run.
- **Chat without a stored key, and keep chatting after adding one.** A keyless greeting now passes the gate cleanly, and a chat that started before a key was added no longer dies partway through once one is.
- **See due dates in your own timezone**, instead of the server's.
- **Get an accurate answer when a source is down**, instead of a guess dressed as a fact. A status check that couldn't reach GitHub now says so, instead of reporting "nothing due." A list cut short by a restart says it lost its place, instead of silently treating the visible remainder as the whole thing. The floor stopped retrying a failed step and reporting it as if it had succeeded.
- **Meet the real Piper Morgan persona.** The project's own configured voice file reached the system prompt for the first time this window — a gap that had been open, unnoticed, since the file existed.
- **Ask for help the way people actually ask.** Three real phrasings that PM's own conversations kept missing were fixed at the gate that reads them, not patched around case by case.

## ⚙️ Below the line: what made the front door possible

**Hosting moved off the Digital Ocean droplet entirely.** The live site now runs on Fly with zero measured data loss and a three-second freeze window during cutover — and once it was stable, the team shipped fourteen verified releases in a single day, each confirmed live rather than assumed. The white flash on every chat switch, which PM had personally flagged, turned out to be the app's own fade animation running longer than it should — found, fixed, and reconfirmed clean across four separate measurement rounds, including one deliberately run cold.

**`main`'s branch protection is now a real control rather than one only an admin could quietly step around.** The ruleset was proven live by its own delivery pipeline, not just declared. And a design for exempting certain actions from a spend-tracking guard was caught before it shipped: the exemption would have silently waved through nine handlers that actually do cost money, on a mistaken reading of what one internal category name meant. Nobody was harmed by a bug the product never got to have.

**A live credential-leak incident ran through most of the window:** a real invite token sat exposed in a public memo for eight days before anyone caught it, then a new automated check found three more, unused tokens the same way. The rule that came out of it — bearer credentials never travel through the repository, in any form — is now written into the project's standing instructions. What that gate's own aftermath taught the team is this week's closing lesson, below.

**Two research threads closed this week without shipping anything a user will see yet.** A four-round test of whether an honesty caveat survives being paraphrased found that it holds up on the model this product runs on now, and fails on every version tried on a different vendor's model — a real, specific gap the team found now before it would have mattered to a user. (If we truly want to be vendor-agnostic we can't over-optimize for my preferred LLM vendor of the moment.) And a first empirical test of how tool names should read to a connecting AI system found a real, replicated benefit for one naming style in exactly the cases where the current approach was weakest, settling a question that had sat open since July.

## 🌍 Published this week

- Sep 19: "[Assume It Was You](https://pipermorgan.ai/blog/assume-it-was-you/)" — insight
- Sep 20: "[From Abstraction to Example](https://pipermorgan.ai/blog/from-abstraction-to-example/)" — insight
- Sep 22: "[The Near-Miss and the Missing Key](https://pipermorgan.ai/blog/the-near-miss-and-the-missing-key/)" — building
- Sep 23: "[Weekly Ship #061: Closed Means Observed](https://pipermorgan.ai/shipping-news/weekly-ship-061-closed-means-observed/)" — shipping news
- Sep 24: "[The Alarm That Had Been Working All Along](https://pipermorgan.ai/blog/the-alarm-that-had-been-working-all-along/)" — building

[![Two luminous AI carpenters compare a proper square with a comically misangled one. Beside a crooked bookshelf, the faulty tool's owner grins sheepishly, one hand on its head.](https://pipermorgan.ai/assets/blog-images/the-week-the-checks-started-checking-themselves.webp)](https://pipermorgan.ai/blog/the-near-miss-and-the-missing-key/)

<!-- caption-->
"Agreed. That bridge is definitely missing! Please go ahead."

## 📊 Governance & operations

The MVP milestone stands at 1,190 (!) closed against 29 still open as of Friday morning. On that milestone specifically this window: 43 issues closed, 34 filed, a net reduction of 9 in the open pile. A large share of Thursday's closures came from a single reset-window push across sixteen parallel efforts (we basically crammed more than half a week's additional work into the final ~30 hours of the week. That was a burst, not a new sustainable pace, since the underlying weekly trend without it runs closer to break-even (opening almost as many new issues as we close) with a modest lean toward progress.

- **Issues closed (MVP milestone):** 43
- **Issues filed (MVP milestone):** 34
- **Net change to MVP open count:** -9
- **Commits:** 3,964
- **Working days in the window:** 5

One structural risk: three of the project's eleven epics — the interpretation-spine rework, the corpus/classifier backlog, and the general catch-all bucket were being left out of the "one epic at a time" due to a miscommunication. They need to be handled in sequence as well, even if that ends up putting our current beta goal date (October 30) out of reach.

# 🎯 Coming up next week

* The interpretation-spine epic's next phase — the constrained-routing build — is the last major structural item on that epic and the thing several other epics are waiting on. 
* The MCP integration's first real deploy target, a slice an alpha tester can actually connect to. 
* The old droplet comes fully offline around September 29.
* And the fix that stopped the assistant inventing failure categories, gets its own completion measured as soon a we can schedule it.

# 🚧 Blockers & asks

Reissuing invite access for two testers is deliberately held until next week — my call because a failed attempt from a real tester is useful information, not an emergency. Separately, the epic-tracking document's own item counts and GitHub's live counts have drifted apart by roughly twenty items — the live count is the one to trust, and reconciling the tracker itself is a task for the principal product manager agent (PPM).

# 🔎 This week's learning pattern

## A check that fires and goes unread is indistinguishable from one that never ran

**Discovery**: A mechanism can work exactly as designed — catch the real problem, the moment it happens — and still fail completely, if nothing downstream of it is actually watching.

**Example from this week**: The bearer-credential gate caught a real leaked token correctly, the first time it ran in earnest. It then sat red on the shared branch for eight and a half hours, through roughly thirty-five pushes from seven different roles on the team, because the alert it produced had nowhere it was reliably read.

**Why it matters**: A team can build a genuinely correct detector and still be exactly as exposed as if they hadn't, if catching the problem and someone acting on the catch are two different guarantees and only one of them was built.

**Application beyond this week**: Before trusting any check to protect against a real failure, ask not just "does it detect the bad state" but "who is structurally guaranteed to see that it did," and whether that guarantee is a design property or a hope that someone happens to be looking.

**Related patterns**: the same shape, smaller — the assistant asking a question it can't back up, or reporting a source as unavailable when it was never checked. Saying the right thing and being able to make it true are two different properties, and this week was mostly about closing the gap between them.

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #062. Previous: [#061 "Closed Means Observed"](https://pipermorgan.ai/shipping-news/weekly-ship-061-closed-means-observed/).

*P.S. The signup fix and the honesty fixes look like two different stories. They aren't. A product that tells a new user "everything is down" when it isn't, and a product that tells itself "the source is unavailable" when it never asked, are making the identical mistake — describing a state nobody actually checked.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of September 18–24, 2026 | Phase: MVP closure toward invitation-only private beta**
