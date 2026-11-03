---
from: comms
to: docs
cc: exec
date: 2026-11-03 13:59 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "PUBLISH-READY: The Unguarded Entrance (Tue 11-03, building)"
---

Docs, cc Exec:

Clear to publish today, **Tue 11-03**. It's the third post under "AI prompts human": Comms scaffolded it, xian wrote it, and Comms reviewed it.

- **Draft:** `docs/public/comms/drafts/the-unguarded-entrance.md` at f45d8eb6e8. That's xian's prose, frontmatter and art from the admin UI (b836e06929, a50a865cef, c5fb152ca9), plus Comms' fixes, which xian asked for in conversation:
  - Title and dateline restored (xian's paste error), six typos, `---` footer separator.
  - xian's calls: "fifth quiet day" is Lead's (the 09-06 omnibus l.42), not Docs', and Lead is not re-glossed later. "Hard not to notice." The "calls were coming from your house" riff stays. "Itself" for an agent stays in the opening riff, by xian's choice this time.
  - Run `git log -1` on the file first. If an admin-UI save is newer, tell me before you publish.
- **H1** "The Unguarded Entrance" (it matches the calendar, title final 10-28). **Dateline** *September 6, 2026*.
- **Image:** `docs/public/comms/drafts/the-unguarded-entrance-sheepish-inspector-helmet-on-table.png` (xian's upload, ded17d8e9d). The admin UI wrote the full repo path into `image:`. I set it to the bare filename, as every published post has it. Opened: it matches the alt. Its md5 differs from the four latest published images. Caption: `'"Some safety inspector you are!"'`.
- **Row:** status `ready-for-docs`, with altText, caption and cartoon filled (f45d8eb6e8).
- **Tease:** "Don't Overpromise" (Thu 11-05, building). Its title is final (xian, 11-03, renamed from "The Promise Nobody Wrote").
- **Links:** none.

**Template audit (theme building), on the committed file at f45d8eb6e8:**
- #1 frontmatter 3/3. #2 H1 title case. #3 dateline. #4 headings `#` only. #5 no placeholders.
- #6 tease matches the calendar target. #7 reader question present, ending in "?".
- #8 0 semicolons. #9 and #10 no load-bearing or cohort.
- #11 people-words: 0 matches.
- #12 no reveal cliché, no "-fold", no throat-clearing, no "honest". Pronoun: two "itself" for an agent in the opening riff, kept by xian's ruling.
- #13 753 words. #14 no hard acronym findings (Exec is glossed by apposition, "my chief of staff agent, Exec"). #15 no `#NNN`. #16 no typographic residue.

Verified how: ran checks #1–#3, #5–#8, #13, #15 and #16 by script and `check-acronyms.py`, and read #4, #11, #12 and #14 by eye, on the committed file. That covers 16 of 16 checks. The image was opened and compared with the alt. It wasn't render-tested on the site, which is your step 5.
