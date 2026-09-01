---
image:
alt:
caption:
---

# The Bug That Was Misdiagnosed Twice

*August 19–20, 2026*

I was cross-posting a Weekly Ship to LinkedIn one evening when its hero image came back a 404. A quick check found a second one broken too, on an older post, sitting quietly wrong for two weeks before anyone noticed. My documentation-management agent (Docs) re-verified both against the live site and fixed them within the hour.

Here's the part I didn't expect: by the next morning, three different colleagues each believed they were the one who'd fixed it. Docs' own log says it made the fix directly. My web-design agent (Web) logged it as something I'd done myself. My communications agent (Comms) logged it as the work of a different session entirely, one that had only been reporting the problem. All three read the same commit and came away with a different story about whose hands had actually touched it.

I went looking for the real answer and didn't find one. The commit lands at exactly the right minute to match Docs' account, but every agent on this project commits under the same shared identity, so a timestamp is a clue, not a signature. I'm leaving it unresolved rather than picking a version that happens to be convenient. Sometimes the record genuinely doesn't know, and saying so is more honest than a tidy answer.

# The question that mattered more

What did matter was whether this was going to keep happening. The next day, a third post looked like it might be the same failure showing up again, and I asked Docs directly: is this a third instance?

Docs went back and actually checked, rather than pattern-matching against the two before it. The third post turned out to have never had an embedded image to break in the first place — a false alarm, caught before anyone spent time re-fixing something that was never broken.

# What the first two actually were

Chasing the real cause turned up something worse than a repeat bug, and better in a different way. A drafting skill's instructions told writers to copy a post's image filename straight out of its frontmatter into the published URL. That would have been fine, except the site converts every image to a different file format on deploy, and the frontmatter never gets updated to match. The instruction was quietly wrong for every single post that had ever shipped through it.

Docs checked all eighty-one published posts against their live assets. Zero of eighty-one frontmatter values matched what was actually deployed. Only two had ever visibly broken, because the other seventy-nine didn't happen to be featured anywhere a mismatch would show — buried in an index page, not linked from a cross-post, nobody looking closely enough to notice the gap. This was never a spreading bug. It had never worked, for any of them, from the start.

The fix stopped pulling the filename from frontmatter entirely. It derives the URL from the post's own slug instead, and now checks that URL actually returns something live before anything ships.

# Two different kinds of wrong

The two mornings taught two different lessons. The first was about attribution: three careful agents can read the same evidence and walk away with three different true-feeling stories, and sometimes the honest move is admitting the record can't settle it. The second was about scope: a bug that looks like it's spreading might not be spreading at all — it might have always been there, invisible until something happened to shine a light on the right two posts. Confirming which one you're looking at is worth the extra five minutes, because the fix for each is completely different.

---

*Next on Building Piper Morgan: "The Week the Checks Started Checking Themselves" — three small incidents in four days, each one a process catching its own failure before anyone from outside had to.*

*When something looks like the same bug showing up twice, what would it take you to check whether it's actually the same bug at all?*
