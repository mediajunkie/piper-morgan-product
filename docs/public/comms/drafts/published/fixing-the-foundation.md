# Fixing the Foundation

<!-- image: 'ai-set.png' -->
<!-- alt: 'A presenter stands ready under a spotlight while small AI helpers hurriedly clean up messy, mislabeled props and backdrops behind the scenes.' -->
<!-- caption: '"The show must go on!"' -->

*March 17–18*

After two days of discovering our architecture was inverted, I did the last thing you'd expect. I stopped building features and started cleaning house.

Eight of my twelve agent briefing documents were stale. One was so corrupted it needed a complete rewrite. Three still referenced a sprint from 143 days ago. The editorial calendar existed in four overlapping spreadsheet tabs. Eighty files had accumulated in a staging directory that nobody was sorting. And 97 blog posts were still pointing at Medium instead of our own site.

In theory none of this was urgent, but at moments where I have had to stop and change direction, I find I don't want to do that with a messy desk, so to speak.

# The briefing rot

One issue was a long-standing sloppiness in the architecture of our briefing docs. We'd been embedding time-sensitive information — sprint names, issue counts, current focus areas — directly into role briefing documents. Every time the project moved forward, every briefing got a little more wrong.

The CXO briefing still said we were in B1. The LLM Support briefing was corrupted to the point of being unreadable. The CIO, PPM, and HOSR briefings all had hardcoded pattern counts and category numbers from months ago. My own briefing — the Comms one — was still talking about GREAT-3B plugin architecture. Four months stale.

The fix wasn't just correcting the facts. It was changing the pattern. Stable role context — what the role does, how it works, what it owns — stays in the briefing. Time-sensitive information — current sprint, active issues, recent progress — lives in BRIEFING-CURRENT-STATE, which gets updated weekly. Briefings now *reference* the current state instead of *embedding* it.

Eight files fixed. The root cause addressed, not just the symptoms.

This is a "rock in the shoe" type of problem. In and of itself it only causes a little friction, but after you've walked ten miles it starts to matter.

# The first real publish

Tuesday was the first time we used the new publish-to-blog skill my Docs agent worked out for  me. "[Four Voices, One Spec](https://medium.com/building-piper-morgan/four-voices-one-spec-168e71571f6b)" — a narrative about the spec pipeline pattern — was the guinea pig.

Five things broke.

The image converter couldn't write WebP format (we needed `cwebp` instead of `sips`). The script generated a random hash instead of looking up the existing Medium hash. The CSV append missed a newline. The blog index linked to Medium instead of the local copy. And a completely different post — The Planning Caucus — turned out to have an edit URL instead of its canonical URL.

All fixed within an hour. The skill got updated to v0.2 with pre-flight checks, safe CSV handling, and deployment verification steps. First real use of any tool reveals problems that design review cannot — and now those problems are prevented for every future use.

Most of this was frictionless for me. At this point Claude Code is often self-correcting and if I notice something they don't, then they fix that too. Small issues that had been bothering me about the [website's blog](https://pipermorgan.ai/) design got fixed when it swept through and cleaned up the nav for me. 

There are still layout issues but it gets better with each pass, and also this not really Docs' job! I have a web agent in a different repo but again I am lazy.

# The repatriation

Meanwhile, 97 blog posts were still hosted on Medium with no local copies. The bottleneck turned out to be a stale file path in one script — `parse-blog-content.js` was pointed at an old export directory. One line fix, 117 new content entries processed. By end of day: 268 out of 268 posts with local URLs. Zero posts pointing at Medium.

The next day, the Documentation agent tackled blog image matching. Cross-referencing the editorial calendar, a Medium Posts CSV, and an older CSV with different naming conventions, 134 out of 168 unmatched posts got their images in a single session. The remaining 34 — pre-August posts with gaps in editorial tracking — needed manual matching.

Repatration is a fancy way of saying this blog series lives canonically on my website. Sure, it gets syndicated to Medium except for the Weekly Ships, and the insight pieces and shipping news goes to the LinkedIn newsletter, but it all lives on my site natively now, first, and my publishing flow now starts there and then reposts instead of starting in Medium and coming home afterward.

# The sorting

Eighty-plus files had piled up in my working directory, dev/active/ — a staging area that had become a junk drawer. Three drafts that belonged in the comms folder. Thirty-five files that belonged in archives by date. Five blog images for the website repo. Eight duplicates. Twenty-one memos that had never been delivered to their recipients.

The Documentation agent sorted all of it in one session. Seven post-March-13 memos delivered to the correct inboxes. The CIO's Agent 360 questionnaire distributed to all eight agent mailboxes. Dev/active/ went from 80 files to 12.

And the editorial calendar — previously four overlapping spreadsheet tabs — became a single unified CSV. 304 rows, 16 columns, deduplicated. One source of truth for the entire content pipeline.

# Why this matters

None of this addressed the urgent floor inversion fix. None of it closed M1 issues. None of it moved the sprint forward in any measurable way.

But when all nine agent roles came online two days later — for the first time in project history — they could actually find their briefings. The briefings were accurate. The memos were in the right inboxes. The editorial calendar was trustworthy. The blog pipeline was complete.

Infrastructure work doesn't show up in velocity metrics. It shows up in the absence of friction the next time everything needs to move fast.

---

_Next on Building Piper Morgan: Nine voices — when all nine agent roles convene to write the shipping news._

_When was the last time you stopped building to clean up? What did it cost you in the moment, and what did it save you later?_
