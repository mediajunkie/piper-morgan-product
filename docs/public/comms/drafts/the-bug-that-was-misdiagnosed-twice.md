---
image: ''
alt: 'In a bright gallery, luminous AI workers expose mismatched picture hooks while two frames lie fallen and a human inspector studies a never-used wall space.'
caption: ''
---

# The Bug That Was Misdiagnosed Twice

*August 19–20, 2026*

I was cross-posting a Weekly Ship to LinkedIn one evening when I realized an image was missing (I typically feature one illustration from a blog post in this narrative to feature). A quick check found a second one broken too, on an older post, wrong for two weeks before I noticed. My documentation-management agent (Docs) re-verified both against the live site and fixed them within the hour.

The next morning, three different agents reported on the fix from different perspectives. Docs' own log says it made the fix directly. My web-design agent (Web) logged it as something they assumed I'd done manually myself. My communications agent (Comms) logged it as the work of another agent entirely, the one that had reported the problem. All three read the same commit and came away with a different story about whose hands had actually touched it.

Aside from that little Rashomon moment, I was more concerned about whether the original failure to include the image would happen again. When a problem arose the next day, I asked Docs directly: is this a third instance?

Docs went back and actually checked, rather than pattern-matching against the two before it. The third post turned out to have a different cause. In this case, there had never been an embedded image to break in the first place.

# What the first two actually were

We diagnosed the bug that had caused the two real problems. A skill for assembling the Ship template recommends copying a post's image filename straight out of its frontmatter into the published URL. That would have been fine, except the site converts every image to a different file format on deploy, and the frontmatter never gets updated to match. 

Docs checked all eighty-one published posts against their live assets. Zero of eighty-one frontmatter values matched what was actually deployed. Only two had ever visibly broken, because the other seventy-nine didn't happen to be featured anywhere a mismatch would show, buried in an index page, not linked from a cross-post, nobody looking closely enough to notice the gap. The bug never spread but had been there, breaking the references, from the start.

The fix was to stop pulling the filename from frontmatter entirely. The skill now says to derive the URL from the post's own slug instead, and now checks that URL actually returns something live before anything ships.

# Two different ways to be wrong

The two mornings taught two different lessons. The first was about attribution: three careful agents can read the same evidence and walk away with three different true-feeling stories, and sometimes the honest move is admitting the record can't settle it. The second was about scope: a bug that looks like it's spreading might not be spreading at all — it might have always been there, invisible until something happened to shine a light on the right two posts. Confirming which one you're looking at is worth the extra five minutes, because the fix for each is completely different.

---

*Next on Building Piper Morgan: "The Week the Checks Started Checking Themselves" — three small incidents in four days, each one a process catching its own failure before anyone from outside had to.*

*When something looks like the same bug showing up twice, what would it take you to check whether it's actually the same bug at all?*
