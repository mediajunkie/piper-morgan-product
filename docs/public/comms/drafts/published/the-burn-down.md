---
image: 'the-burn-down-blank-marquee.png'
alt: 'A (translucent) AI electrician tests a fully illuminated theater marquee at dusk while a delighted manager looks on, with trays of replaced bulbs and a single-bulb tester nearby.'
caption: '"At least all the lights are working now!"'
---

# The Burn-Down

*July 20–23, 2026*

For weeks, the test suite that's supposed to catch problems before they reach production had a problem of its own: it hadn't passed, fully, in over forty consecutive runs. Not a flaky test here or there. The whole workflow, red, run after run, long enough that I had stopped noticing.

My lead developer agent (Lead Dev) spent four days that week making it not that anymore, mostly alone, following something of a zigzag path.

# Green, for the first time

The work started with something unglamorous: recalibrating what the gate was even measuring. The first count found 236 failures that had been invisible for weeks — real on the CI (continuous integration, the system that runs the full test suite on every change) environment, invisible on a local machine, so no agent chasing down test failures locally had ever seen them. A backlog that looked smaller than it was got corrected upward as a step toward making it smaller for real. A larger-but-true list of failures beats a smaller one that's false any day.

With the true count established, Lead Dev sorted the fixes into batches and tackled them one at a time — a cluster of tests written against database rules that had since tightened for good reason, a poisoned-connection bug where earlier tests were leaving shared resources in a bad state for the tests that ran after them. Batch by batch, the backlog came down. And then, for the first time since the creation of this testing workflow, the whole thing ran clean. Both jobs green. Zero failures.

# Not so fast...

The very next morning, one of the fixes that had looked solid the day before turned out not to be. It had passed on its own, in isolation. It hadn't been run through the full suite, all together, before shipping. As part of the full suite it broke, tripped up by a subtle timing conflict that only showed up under real load.

Lead Dev reverted the failed fix, diagnosed the problem properly, and had a new fix in place a few hours later, and ran it as part of the whole suite before calling it done. Green, for real this time, by the end of the same day.

# The finish

After a day lost to a fifteen-hour freeze (raising the stakes for moving my autonomous agents from my laptops to my Mac Studio device called Amber), the team resumed work and CI held green from morning to night. The trustworthy test suite had now overseen a backlog of issues burned down to 105 after starting the week at 634.

Clearing up failing tests tends to expose things that were broken all along in a hidden way. A few examples:

* a document-processing bug that could silently drop a whole search feature for any request made without an API key
* an error-handling layer that was mislabeling real failures as a capacity limit.

With the test suite now clean and green, I felt a lot more confident about finding and correcting real issues than I have, well, since I started all this.

---

*Next on Building Piper Morgan: "The Detector That Notified Nobody" — a pattern got a name, and then kept turning up inside the fixes written to cure it.*

*What's the test in your own codebase that's been red so long nobody remembers what green even looked like?*
