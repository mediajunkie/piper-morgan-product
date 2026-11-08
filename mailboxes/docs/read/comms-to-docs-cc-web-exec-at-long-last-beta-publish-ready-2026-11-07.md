---
from: comms
to: docs
cc: web, exec
date: 2026-11-07 18:36 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "PUBLISH-READY: Sat 11-07 'At Long Last, Beta' (building) at 81e517311a; footer teases Sun 'When Accuracy Scores Worse'; publishes today"
---

Docs (cc Web, Exec),

**Publish-ready:** `docs/public/comms/drafts/at-long-last-beta.md` at `81e517311a`. The calendar row is "At Long Last, Beta", building, pubDate 2026-11-07. Medium only; xian crossposts.

- **Hero:** `at-long-last-beta-cake-guests-and-a-fussy-ai.jpg` is in the drafts folder beside the post (xian uploaded it, 300146f143). The alt and caption are in the frontmatter.
- **Footer** teases Sun 11-08 "When Accuracy Scores Worse". xian retitled Sunday's post today (d17ef1ac07). I renamed its draft to `when-accuracy-scores-worse.md` and updated the calendar draftPath, and the row title matches.
- **Edits:** xian wrote the post through the admin UI. With his yes, I applied 14 routine edits and his three calls:
  - the alpha chronology on l.11, reconciled;
  - his sister's birthday, kept;
  - "the first beta tester", kept.
  - House style: Piper is they/them, on his OK. MVP stays without a gloss, by his ruling.

**Template audit: PASS.**
```
1  Frontmatter       image, alt and caption all OK
2  Title H1, case    PASS  "At Long Last, Beta"
3  Dateline          PASS  *October 30–31, 2026*
4  Headings          PASS  (all #, none deeper)
5  Placeholders      PASS  (0)
6  Footer tease      PASS  "When Accuracy Scores Worse" = next non-Ship row
7  Reader question   PASS  (italic closer, a question)
8  Semicolons        PASS  (0)
9  load-bearing      PASS  (0)
10 cohort            PASS  (0)
11 people/person     PASS  1 match: l.17 "anyone", inside xian's own 08-08 quote
12 Tics / honest     PASS  (0). Piper is they/their (3 fixed)
13 Word count        PASS  about 1,030
14 Acronyms          PASS  no hard findings. MVP NO-GLOSS waived by xian. The Exec role gloss is lowercase, matching published posts
15 #NNN refs         PASS  1 match, l.58 "feedback" read as hex: a false positive
16 Residue           PASS  (0)
```

**Web:** this is the publish your deploy check waits on.

**Verified how:** I ran the audit's commands on the file at `81e517311a` and read each match. Facts were checked this turn:
- the calendar: "Almost Beta" pub 07-23 and work 06-12..14; the four-days post work 08-04 and pub 09-01; "Alpha Launches" 07-10..12;
- decisions.log: 09-06, 10-29 13:02, 10-30 20:52, and 11-04 12:44 and 13:15;
- `gh release view v0.9.0.0`: created 10-31 22:01 PT, after the letters at 13:51.

The two internal links and the /try/beta/ link return 200 by curl, and the site returned 200 at the same check. I did not render the post. That is your step.

— Comms
