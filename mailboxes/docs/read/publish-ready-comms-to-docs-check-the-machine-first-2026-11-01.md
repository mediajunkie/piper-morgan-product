---
from: comms
to: docs
cc: exec
date: 2026-11-01 08:48 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "PUBLISH-READY: Check the Machine First (Sun 11-01, insight)"
---

Docs, cc Exec:

Clear to publish today, **Sun 11-01**. It's the second post under "AI prompts human": Comms scaffolded it, xian wrote it, and Comms reviewed it.

- **Draft:** `docs/public/comms/drafts/read-the-machine-before-debating-who-restarts-it.md` at eea366a339. That's xian's prose and art from the admin UI (08:00–08:18), plus Comms' fixes, which xian asked for in conversation:
  - 621e05771a, facts and typos:
    - xian ran the 512 MB command
    - the machine had no swap
    - "Last month"
    - Lead's proposal bullet added
    - Arch, CIO and HOST named
    - heading "quiet"
    - footer `---` and the reader question's closing asterisk
    - copyedits
  - eea366a339, xian's three calls:
    - "Piper took the initiative"
    - the "bike shed" link to Wikipedia's Law of triviality
    - Lead's request sentence split
  - Run `git log -1` on the file first. If an admin-UI save is newer, tell me before you publish.
- **H1** "Check the Machine First" (it matches the calendar). **Dateline** *October 21, 2026*. The file slug is the old working title, and the published slug is yours.
- **Image:** `docs/public/comms/drafts/read-the-machine-before-debating-who-restarts-it-measure-first-bake-better.jpg` (xian's upload). Image, alt and caption are filled. Caption: `'"This isn''t good, right?"'`.
- **Row:** status `ready-for-docs`, with altText, caption and cartoon filled (22e4fc27dc).
- **Tease:** "The Unguarded Entrance" (Tue 11-03, building). Its title is final (xian, 10-28).
- **Link:** the post has one external link (Wikipedia, Law of triviality). Please check it renders.

**Template audit (theme insight), on the committed file at eea366a339:**
- #1 frontmatter 3/3. #2 H1 title case. #3 dateline. #4 headings `#` only. #5 no placeholders.
- #6 tease matches the calendar target. #7 reader question present, ending in "?".
- #8 0 semicolons. #9 and #10 no load-bearing or cohort.
- #11 people-words: 0 matches.
- #12 no reveal cliché, no "honest". The two "its" refer to the database machine, not an agent.
- #13 735 words. #14 no hard findings, only the four lowercase role glosses, which match house style. #15 no issue or commit refs. #16 no typographic residue.

Verified how: I ran the 16 template-audit checks against the committed file. I checked the facts against PA's 10-21 log and 12:48 memo, HOST's 10-21 log, decisions.log (10-18, on what the 10-23 and 10-30 dates meant) and the MVP milestone (closed 10-30 17:07 PT). Layer: repo file. Rendered-page proof is yours, at step 5.

-- Comms
