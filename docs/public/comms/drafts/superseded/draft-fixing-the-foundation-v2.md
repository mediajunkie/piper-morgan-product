# Fixing the Foundation

*March 26, 2026*

[alt text: PLACEHOLDER — cartoon TBD]

*March 17–18*

After two days of discovering our architecture was inverted, I did the last thing you'd expect. I stopped building features and started cleaning house.

Eight of my twelve agent briefing documents were stale. One was so corrupted it needed a complete rewrite. Three still referenced a sprint from 143 days ago. The editorial calendar existed in four overlapping spreadsheet tabs. Eighty files had accumulated in a staging directory that nobody was sorting. And 97 blog posts were still pointing at Medium instead of our own site.

None of this was urgent. All of it was compounding.

[ADD PERSONAL ANECDOTE: What made you decide to do this now instead of pushing forward on the floor inversion fix? Was it a deliberate decision or did you just look around and realize the mess?]

## The briefing rot

The root cause was architectural, not laziness. We'd been embedding time-sensitive information — sprint names, issue counts, current focus areas — directly into role briefing documents. Every time the project moved forward, every briefing got a little more wrong.

The CXO briefing still said we were in B1. The LLM Support briefing was corrupted to the point of being unreadable. The CIO, PPM, and HOSR briefings all had hardcoded pattern counts and category numbers from months ago. My own briefing — the Comms one — was still talking about GREAT-3B plugin architecture. Four months stale.

The fix wasn't just correcting the facts. It was changing the pattern. Stable role context — what the role does, how it works, what it owns — stays in the briefing. Time-sensitive information — current sprint, active issues, recent progress — lives in BRIEFING-CURRENT-STATE, which gets updated weekly. Briefings now *reference* the current state instead of *embedding* it.

Eight files fixed. The root cause addressed, not just the symptoms.

[CHRISTIAN TO POLISH: Did any of the stale briefings actually cause a problem, or was this preventive? The Comms briefing was definitely stale when I onboarded — was that a known issue or did it surprise you?]

## The first real publish

Tuesday was the first time we used the publish-to-blog skill for real. "Four Voices, One Spec" — a narrative about the spec pipeline pattern — was the guinea pig.

Five things broke.

The image converter couldn't write WebP format (we needed `cwebp` instead of `sips`). The script generated a random hash instead of looking up the existing Medium hash. The CSV append missed a newline. The blog index linked to Medium instead of the local copy. And a completely different post — The Planning Caucus — turned out to have an edit URL instead of its canonical URL.

All fixed within an hour. The skill got updated to v0.2 with pre-flight checks, safe CSV handling, and deployment verification steps. First real use of any tool reveals problems that design review cannot — and now those problems are prevented for every future use.

[ADD PERSONAL DETAIL: Was this frustrating or satisfying? Five things breaking sounds bad, but all fixed in an hour sounds like the system is resilient. Which was it?]

## The repatriation

Meanwhile, 97 blog posts were still hosted on Medium with no local copies. The bottleneck turned out to be a stale file path in one script — `parse-blog-content.js` was pointed at an old export directory. One line fix, 117 new content entries processed. By end of day: 268 out of 268 posts with local URLs. Zero posts pointing at Medium.

The next day, the Documentation agent tackled blog image matching. Cross-referencing the editorial calendar, a Medium Posts CSV, and an older CSV with different naming conventions, 134 out of 168 unmatched posts got their images in a single session. The remaining 34 — pre-August posts with gaps in editorial tracking — needed manual matching.

[CHRISTIAN TO POLISH: Is there a good way to characterize the blog repatriation? It sounds dry but it represents full ownership of your content — no more dependency on Medium for hosting. Is that meaningful to you?]

## The sorting

Eighty-plus files in dev/active/ — a staging area that had become a junk drawer. Three drafts that belonged in the comms folder. Thirty-five files that belonged in dated archives. Five blog images for the website repo. Eight duplicates. Twenty-one memos that had never been delivered to their recipients.

The Documentation agent sorted all of it in one session. Seven post-March-13 memos delivered to the correct inboxes. The CIO's Agent 360 questionnaire distributed to all eight agent mailboxes. Dev/active/ went from 80 files to 12.

And the editorial calendar — previously four overlapping spreadsheet tabs — became a single unified CSV. 304 rows, 16 columns, deduplicated. One source of truth for the entire content pipeline.

## Why this matters

None of this was the floor inversion fix. None of it closed M1 issues. None of it moved the sprint forward in any measurable way.

But when all nine agent roles came online two days later — for the first time in project history — they could actually find their briefings. The briefings were accurate. The memos were in the right inboxes. The editorial calendar was trustworthy. The blog pipeline was complete.

Infrastructure work doesn't show up in velocity metrics. It shows up in the absence of friction the next time everything needs to move fast.

[ADD PERSONAL REFLECTION: Is there a broader lesson about the relationship between cleaning up and speeding up? Cathedral building philosophy meets housekeeping?]

---

_Next on Building Piper Morgan: [TITLE TBD for Act 5] — when all nine agent roles come online for the first time._

_[QUESTION PLACEHOLDER: When was the last time you stopped building to clean up? What did it cost you in the moment, and what did it save you later?]_
