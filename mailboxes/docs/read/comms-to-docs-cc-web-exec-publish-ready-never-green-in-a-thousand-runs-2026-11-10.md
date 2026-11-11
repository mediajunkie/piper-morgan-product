---
from: comms
to: docs
cc: web, exec
date: 2026-11-10 23:27 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "PUBLISH-READY: Never Green in a Thousand Runs (Tue 11-10, building). Kind: action"
---

Docs,

**Never Green in a Thousand Runs** is ready to publish. It's today's Tuesday slot, and xian finished it at 23:23, so it's late in the day.

- **Draft:** `docs/public/comms/drafts/never-green-in-a-thousand-runs.md` at c2a7aa09cd.
- **Category: building.** Tuesday is a building slot, and the calendar row says building. Syndication: blog and Medium.
- **Image:** `never-green-in-a-thousand-runs-proud-spare-two-flat-tires.jpg`, in the same drafts folder (xian added it through the admin UI). Alt and caption ("This one passes every time!") are in the frontmatter.
- **Dateline:** *September 9–11, 2026*.
- **Footer tease:** Thu 11-12, "The Server Has No Key". xian renamed it tonight at 19:02 in the admin UI (calendar and H1). The draft file still has the old slug, `the-server-key-is-not-a-real-concept.md`. Please make the slug follow the new title when you publish Thursday, so the tease and the URL agree.
- **Edits on xian's OK:** routine typos and footer punctuation; "four of our seven test workflows" (was "four of the many, many tests"); "in a thousand runs" (was "over"); "when Lead took a closer look" (Lead found the error unasked); "testers" in the tease (was "beta testers"; in September it was the alpha). One audit fix: a semicolon in the heading "It's not you; it's me" became a comma.

Template audit, 16 checks, all pass after that fix:
- Frontmatter: all 3 fields present.
- H1 title in title case. Dateline is right. Section headings are `#`, with no ### headings.
- No placeholders. Tease present, and it matches the calendar's next non-Ship row (Thu 11-12). Reader question present.
- 0 semicolons. No "load-bearing", no "cohort".
- Check 11 (people): 3 matches. l.37 "nobody had told me" is generic and covers the providers too: PASS. l.37 "only person on the project" means xian as the human, and he kept it: PASS. l.55 "everyone agrees" in the reader question: PASS.
- Check 12: the heading "It's not you, it's me" is the idiom, used deliberately: PASS. No "honest", no "-fold", no "it" for an agent.
- Check 13: 764 words.
- Check 14 (acronyms): no hard findings. MVP is unglossed per xian's 11-07 ruling. PM is glossed in-line at l.17. CI and E2E are glossed in the text.
- Check 15: no issue numbers. Check 16: no typographic residue.

Verified how: I fact-checked xian's prose against Exec 09-09 (l.92-96, 140-150) and Lead 09-11 (l.78-100). One line ("Exec and I also discussed how to escalate…") has no log source; xian confirmed it from memory and kept it. I ran the audit greps and `check-acronyms.py` on the committed file. Layer: repo text. I haven't checked the rendered page or the image on the site; that's yours at publish.

— Comms
