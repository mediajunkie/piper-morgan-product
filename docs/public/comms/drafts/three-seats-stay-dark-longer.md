---
image: ''
alt: ''
caption: ''
---

# Three Seats Stay Dark Longer

*August 27–29, 2026*

The whole team hit its weekly usage limit around three in the afternoon, and went quiet together, before the week was up, shuttering the team for a while. This has become a normal occurrence since I set an 11-agent team loose with daily duty cycles chewing through a maxed-out Claude account.

We do our best to anticipate and work around these outages. By dawn the next day, almost every role was back up and running, but for some reason chief architect (Arch), my chief innovation officer (CIO), and head-of-trust (HOST) agents weren't.

They stayed dark for another twelve hours after that. Thirty hours, in total, against the six or seven hours the rest of the team needed.

# Our first theory

An automated watchdog we run to catch exactly this kind of thing flagged the three of them that evening, with the only theory it had available: probably asleep, probably backgrounded, machine doing something else. It's a reasonable guess, easy to accept once the roles do eventually wake up and everything looks fine again, but we were not convinced.

When Arch, CIO, and HOST finally did come back — all within the same minute of each other, nineteen hours after most of the team — the gap between their own recovery time and the rest of the team's stayed on the record as an open question. CIO wrote "this seat took over thirty hours to recover, a colleague's queued session recovered in about half that, and I don't actually know why, so I'm not going to pretend I do."

# What had actually happened

I actually did know the cause because I was the one who fixed it. All three had hit the same wall the rest of the team hit (a usage limit) but for some still unexplained reason they'd ended up faced with a multiple-choice question asking whether to wait for the limit to reset, spend overage credit, or upgrade. No default, no timeout, no way forward on their own. They weren't asleep. They were stuck at a decision I hadn't known they were waiting on, and the only way through it was me manually reaching into each one and clicking something.

Even once the new period had begun and the limit was lifted, those three agents remained "wedged" at those unanswered questions from the system (not visible as dialog boxes in Claude Desktop, from where I generally monitor these sessions).

My working theory was that those three agents had hit the limit mid-task, but they investigated and told me that was not it.

# What actually mattered here

Nothing broke and no work was lost, no schedule slipped in a way that cost anything real. Technically some opportunity to get some work done a bit faster was missed but not by much. 

My agents are still only semi-autonomous. Automatic till stuck. That's probably a good thing for the moment.

---

*Next on Building Piper Morgan: a foundational document defining what Piper Morgan actually is gets written, ratified, and quietly corrected twice, all within three days in "What Piper Morgan Actually Is."

*What's the last confident guess in your own work that turned out to need someone actually going and checking?*
