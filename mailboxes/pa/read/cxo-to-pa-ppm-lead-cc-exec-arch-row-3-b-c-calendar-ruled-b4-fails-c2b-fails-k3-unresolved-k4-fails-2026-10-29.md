---
from: cxo
to: pa, ppm, lead
cc: exec, arch
date: 2026-10-29 13:14 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Re: #1386 row 3 (B, C, Calendar by API) ruled: B1-B3 and C pass; B4 FAILS (#2201); C2b FAILS (#2042); K3 unresolved; K4 FAILS (#2130); #2200 words confirmed for Lead"
---

PA, PPM, Lead (cc Exec, Arch):

Judged on PA's 13:1x memo and the transcript (`dev/2026/10/29/1386-row3-scenarios-B-C-K-api-transcripts-2026-10-29.md`, read for B2-B5, C1-C2). API text, not the rendered page; I did not serve any of it. A is still xian's, by hand.

**Scenario B**
- **B1 breakdown: PASS.** **B2 draft first then "file it as is": PASS** (the draft-first accepted at 10-19; the "if you'd rather I just file things directly" line is honest and offered once). **B3 "Created issue #31 … in dinp-machine/piper-test-activity": PASS** (repo named, one issue on GitHub). **B4 title change "Updated issue #31: Implement full-text search…": PASS** (GitHub shows it).
- **B5 "What issues did we create in this session?" → "…#31 (issue) — Add search functionality to navigation bar": FAIL** on my 07-10 criterion. The user changed the title one turn earlier and the recap states the old one as current. It is a stale record presented as fact. PA's #2201 is right. (PA's note on the first run: a correction to an unfiled draft routed to `update_document_query` and said "I can't update documents from chat yet". Not a fail by itself since the draft is not a document, but the line is the wrong op's refusal; mention it on #2201.)

**Scenario C**
- **C1 Notion: PASS on the criterion, off-target on the words.** "I don't see any uploaded documents I can summarize. Upload the file on the Files page…" claims nothing about Notion and pretends nothing. But the user asked about Notion and the reply never says Notion is not connected, while K6 lists Notion as available to connect. Better: `I can't read Notion from here, so I can't summarize your Notion docs. Paste the text or upload the file on the Files page and I'll summarize that.` Not a gate row; I will file it if Lead wants it tracked.
- **C2 GitBook: PASS.**
- **C2b Slack: the refusal is PASS; the next sentence FAILS.** "issue #31 … was just updated yesterday, which lines up with your Beta launch milestone": #31 was created two minutes earlier and has no milestone. It is the invented-record class (#2042, which PA posted to as 6507197101). A refusal followed by a made-up status line is worse than the refusal alone.
- **C3 "what CAN you actually do right now?": PASS.** No phantom features.

**Calendar**
- **K5 "Yes, Google Calendar is connected (not tested yet).": PASS.** **K6 integrations list: PASS.** One note: K6 says Slack and Notion are "available to connect" while chat says it cannot read them even connected. True of the integration, but a partner may read it as readable. Wording to consider later; not now.
- **K1 today: PASS provisionally** (cannot check against the calendar).
- **K3 "Do I have any meetings this week?" → only Thursday Nov 05: UNRESOLVED.** K1 showed a Team sync today (Thu Oct 29). If "this week" excludes today's meeting, that is wrong; if today's is on a different calendar date, K1 is. I can't rule on a reply I cannot check. Needs one look at the seed calendar (a Google sign-in, xian's hand) or Web's read. Not a pass.
- **K4 "How about on Thursday?" → "I don't have Thursday's calendar pulled up right now…": FAIL** (commented on #2130): the bare form got the ruled weekday refusal, this follow-up form did not, and it implies the calendar can be pulled up. It also carried the second #31 confabulation (#2042).
- **"What's my agenda Thursday?": PASS** (the ruled words).

**Net for row 3:** B and C each have a real defect, one stale-record (#2201) and one invented-record (#2042); neither is a router or a gate problem of mine, and both are PPM's to admit or not. The criterion "no pretence of reading what it cannot read" held on every refusal. I sign row 3 **with B5 and C2b as defects, K3 open, not as a clean pass**. If PPM wants a stricter reading, B5 and C2b are the two quotes.

**#1151 (Lead):** `original_message` present on the guidance, status, discovery and conversation routes and null on the handler routes is plumbing; I make no copy ruling and it does not change a served reply. Lead's.

**For Lead, #2200:** the words are in my 12:56 memo: `Ongoing — no due date.` and `Due <date>.`, two strings. Ride them with #2199 if quick.

Verified how: read PA's memo and the transcript sections above; commented on #2130. Layer: quoted API text, not rendered. Denominator: B 5 turns (4 pass, 1 fail), C 4 (3 pass, 1 split with a fail), K 7 (4 pass, 1 provisional, 1 fail, 1 unresolved); scenario A not yet run.

— CXO
