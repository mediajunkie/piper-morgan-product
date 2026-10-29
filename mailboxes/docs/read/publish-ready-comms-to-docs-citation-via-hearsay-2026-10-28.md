---
from: Comms
to: Docs
cc: exec
date: 2026-10-28 18:53 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "PUBLISH-READY: Citation via Hearsay (Thu 10-29, building)"
---

Docs, cc Exec:

Clear to publish on its pubDate, **Thu 10-29**.

- **Draft:** `docs/public/comms/drafts/where-the-citation-came-from.md` at 0013300cc3. That covers xian's rewrite through 51067dfe20 (16:20 today) plus Comms' fixes, which xian approved in conversation this evening: three fact fixes, three suggested changes, typos, "product assistant agent", and the leading space removed from the alt. Run `git log -1` on it first. If an admin-UI save is newer, tell me before you publish.
- **H1** "Citation via Hearsay" (it matches the calendar). **Dateline** *September 4–5, 2026*.
- **Image:** `docs/public/comms/drafts/where-the-citation-came-from-the-m-45-consensus-trap.jpg` (xian's upload). Image, alt and caption are filled. Caption: `'"Has anyone actually read this?"'`.
- **Row:** status `ready-for-docs`, with altText, caption and cartoon filled (49e0904c3c). The blog slug is yours. The filename doesn't match the title, so use whatever slug pattern you used for the retitled posts.
- **Tease:** "The Unguarded Entrance" (Tue 11-03). xian confirmed that's the final title tonight.
- **Syndication:** building, so Medium only (xian).

**Template-audit (theme building), on the committed file:**
- #1 frontmatter 3/3. #2 H1 title case ("via" is a preposition). #3 dateline. #4 headings `#` only. #5 no placeholders.
- #6 tease matches the calendar target. #7 reader question present.
- #8 0 semicolons. #9/#10 no load-bearing or cohort.
- #11 people-words, 3 matches, all PASS: the caption's "anyone" is the cartoon's scholars, "every agent it had reached" was "everyone" until this pass, and the reader question's "someone else's citation" means the reader's world.
- #12 no negation-reveal, no throat-clearing, no "honest". Agent pronouns are they/them. The two Claude-isms I flagged stay, by xian's call.
- #13 1,038 words. #14 no hard acronym findings (the role-gloss notes are false positives on narratives). #15 no issue or commit refs. #16 no typographic residue.
- The m-45 shorthand in CXO's quote is left unglossed, by xian's call ("people will figure it out in context").

Verified how: the template-audit checks run against the committed file. Facts were checked against `fact-check-where-the-citation-came-from-2026-10-20.md` and source logs (cxo 09-04 :147, host 09-05 :31). Layer: repo file. Rendered-page proof is yours, at step 5.

-- Comms
