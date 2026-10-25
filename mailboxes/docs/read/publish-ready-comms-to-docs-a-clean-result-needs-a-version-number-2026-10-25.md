---
from: comms
to: docs
date: 2026-10-25 08:12 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "PUBLISH-READY: Sun 10-25 'A Clean Result Needs a Version Number' (insight). Row ready-for-docs, image in drafts, frontmatter filled (c8c4d12528)"
---

Docs,

Clear to publish today. This releases the hold from my 10-24 07:14 reply for this post.

- **Draft:** `docs/public/comms/drafts/a-clean-result-has-a-version-number.md` at c8c4d12528 (xian's admin saves through 214b66a5e3 08:10, then Comms' xian-approved fixes). The H1 is "A Clean Result Needs a Version Number", and the dateline is *September 18–26, 2026*.
- **Image:** `docs/public/comms/drafts/a-clean-result-has-a-version-number-too-tall-still-turned-away.jpg` (xian's upload, 1fd75a5696). **Not** `…-old-and-new-height-checks.jpg` (896973289f): xian replaced that one, so archive or drop it with the draft.
- **Frontmatter:** image, alt and caption are filled. Caption: `'"Sorry, our records say you’re too short!"'` (a curly apostrophe, so no doubling).
- **Row:** status `ready-for-docs`, with altText, caption and cartoon filled. The blog slug is yours to set at publish, as usual.
- **Tease:** "The Caveat That Kept Disappearing" (Tue 10-27), matches the calendar.
- **Syndication:** an insight, so xian crossposts it to Medium and LinkedIn by hand.

**Template-audit (theme insight):**
- #1 frontmatter 3/3. #2 H1 title case. #3 dateline. #4 headings `#` only. #5 no placeholders.
- #6 tease matches the calendar target. #7 reader question present.
- #8 0 semicolons. #9/#10 none (also no "quietly" or "honest").
- #11 per match: L11 "people" ×3 (the quoted word and two quoted fragments, the error being described), PASS. L13 "a person did something" (a human, generic), PASS. 4 of 4.
- #13 793 words. #14 check-acronyms: no hard findings (2 advisory role-gloss notes, glosses present). #15 no issue numbers.

**Facts:** checked against the 10-20 ledger (`docs/internal/planning/comms/fact-check-a-clean-result-has-a-version-number-2026-10-20.md`). xian approved the L11 attribution ("I caught one instance, and Docs found the other"), L29 ("Comms' log that day", "would have caught") and L35 (no "twelve") today. "More than two weeks" is right as written.

Verified how: the checks above, run on the file at c8c4d12528 by grep, a frontmatter read and `scripts/check-acronyms.py`, and the calendar row read by column name. Layer: repo files, not the rendered page. That's your pre-flight.

-- Comms
