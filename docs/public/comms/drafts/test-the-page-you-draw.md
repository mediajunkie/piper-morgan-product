---
image: 'test-the-page-you-draw-finding-the-hidden-elevator-button.jpg'
alt: 'A woman searches the blank wall beside closed elevator doors while a translucent attendant points to a small call button just around the corner.'
caption: '"See, there is a button!"'
---

# Mark One Eyeball

*November 15, 2026*

Whenever you delegate work, especially to agents (but really any time), the moment of truth is when you finally inspect the results of the work yourself, using what military slang jokingly calls the "[mark 1 eyeball](https://en.wiktionary.org/wiki/mark_1_eyeball)" instrument (sometimes written "Mark I" and always pronounced "mark one"). The point is, you have to look at it directly yourself.

The agent team tests Piper Morgan code assiduously, but testing the code is not the same as being a person and using the software. When I get overloaded, the number of items I need to inspect, test, and give feedback on directly mounts fast (at least until I can get more testers in, chicken-or-egg problem!), creating large backlogs for me to wade through, a [reverse centaur](https://pluralistic.net/2025/09/11/vulgar-thatcherism/) to my own apparatus (author Cory Doctorow's coinage, warning us about becoming the servants of our machines).

# Read the fine print

To be fair about what follows, very few products offer a first-class preference-settings or configuration-updating experience. You tend to get utilitarian portals with raw-plumbing workflows. I'd like to do better but I have for the most part let my agent team design and build the settings pages and functionality, passively steering by complaining about clutter or inconsistency from time to time.

My lead developer agent (Lead) had worked on an issue that would enable people to give Piper Morgan access to specific GitHub repositories, adding a `GitHub repositories` text link just below the settings page's "card" for managing a GitHub connection (connecting, testing, and disconnecting to and from a specific GitHub account).

In mid-November I made time to do some manual testing so we could close otherwise presumably completed issues and when asked to configure GitHub repositories for a test account I confidently reported that the Settings page provided me no way to add a repository once a first one was installed.

That's when I was shown that there was indeed a tiny text link sitting outside of the information design and visual hierarchy on the page. I told the team "a floating link on that page violates the design and probably at least six other principles of this project or common sense."

# Even admins deserve design

The diagnosis was quotidian: the link had somehow been added to a branch of the page that includes the Slack and Calendar cards, which apparently left it orphaned. 

From a plumbing point of view, the link existed and there was indeed a way to manage repositories, but the failure to design the experience with intent rendered it invisible and hence useless and frustrating, at least for me or anyone in a hurry who is trusting the design to guide their eye. 

My design agent (CXO) specified how to move the entry from a link to a card (with options "Manage repositories" and "Add another repository"), and Lead implemented the fix that evening. 

# Will agents eventually understand "gestalt"?

The team also added a "drawn-card" test in which the page is rendered and examined in its final HTML form vs parsed as pure source text. The new tests catch words and structure, but not layout. Nothing automated looks at the page the way I do, and yet this is still a good thing for them to do. It will likely reduce the number of things that need attention, but this approach, at this rate, will never substitute for my mark one eyeball.

---

*Next on Building Piper Morgan, we resume the building narrative in late October of this year with "Ready or Not" in which I try to anticipate if we are on track to meet the MVP milestone, close the alpha testing period, and launch the beta*.

*Do you ever put off reviewing work that needs your final approval, for fear of what you might find? Do you have to wait until you are in the right frame of mind to really be attentive and notice things vs. wearily sign off on them? How do you manage the balance of delegating while upholding your own standards?*
