# Teachable practice: Proven methodology entries in user terms (#2355, part 2(c))

*Draft by CIO, 2026-11-13, for CXO's voice pass against `docs/internal/design/tier1-voice-specification-2026-11-13.md` (draft 1). Not approved wording. Next: CXO passes or returns each row, then xian approves the wording, then Docs lists the passed rows in the corpus manifest (CIO owns these rows there).*

## What this is

The Tier 1 corpus's teachable-practice rows that come from `methodology-core`. A Proven entry is written for the team, with roles, issue numbers and incidents, so none is usable as written (design record, CIO's area 5). Each row below rewrites one entry's practice for a person asking Piper "how should I…?". Piper retrieves a row on a matching turn and answers from it in its own words. The row is not a script to recite.

Source: the Status and Summary lines from 9p (2026-11-12). 19 entries are Proven. 15 of them are covered by the 14 rows below (two rows draw on two entries), and 4 are left out with the reason given.

## How each row was written

Against the spec:
- **Rule 2 (no sources):** no entry numbers, names or incidents in the text. The reviewer column holds the source, and it does not ship.
- **Rule 3 (leak list):** no "the team", roles, issues or internal terms.
- **Rule 9 (user's terms):** a person's project, tickets and documents, not agents, gates or logs.
- **Rule 10 (short):** two to four sentences each.
- **Advice register:** it's addressed to the person ("you"), because these answer "how should I". Rule 1's first person applies when Piper talks about itself, which these rows don't.
- **No claim about Piper's own behaviour:** what Piper does is the conduct layer's job (#2354), so rule 6 has nothing to trace here.

---

## The rows (candidate corpus text)

**Check where you'd actually see it.** *(07, 30)*
Before you rely on something being done, look at it where the result shows up: open the page, run the real step, read what came back. Something being set up the right way doesn't prove it's used. Then say what you checked.

**Read it before you rely on it.** *(52)*
A title, a summary or a search result tells you what a document is about, not what it says. Before you quote it, act on it or pass it along, open it and read the part that matters.

**Look at what already exists first.** *(07)*
Before you start something new, check what's already there and whether your assumptions still hold. It saves building a second copy of something that works, or breaking it.

**Write "done" as something you can check.** *(01)*
Before work starts, write each requirement as a check you could run or watch, such as "a new user can sign in and see their project". Then "done" is something you can see pass, not something to argue about.

**Don't call it done early.** *(03)*
The habits that most often hurt quality: skipping the check, building before you know what passing looks like, working alone on something risky, assuming instead of looking, and calling it done before anyone has seen it work. Each one has a fix, and it's usually the step that felt skippable.

**Get a second look at what matters.** *(17)*
For a claim with real stakes, have someone else check it with the evidence in front of them, not your summary of it. A second reader catches what the first one stopped seeing.

**Hear everyone before you merge views.** *(22)*
When a decision crosses several areas, collect each person's view on their own first, then bring them together. If everyone hears the first opinion before forming theirs, you get that opinion back several times.

**A count isn't the thing you care about.** *(48)*
An easy number can stand in for a hard question without answering it. Twelve tickets closed tells you twelve were closed, not that the problem is solved. Say what was counted and out of how many, and ask whether that's the question you meant.

**A correction needs checking too.** *(47)*
Before you correct something, yours or someone else's, go back to the original and confirm what it said and whether it still stands. Then say plainly what was wrong and what's right.

**If a step keeps getting missed, change the process.** *(36, 53)*
Asking people to be more careful rarely fixes a step that keeps slipping. Attach it to something that can't be skipped, like a field that must be filled before a ticket closes, or produce the list from the source data instead of keeping it by hand.

**When you add automation, look at what it replaces.** *(41)*
A new tool often quietly takes over a habit nobody wrote down. Check what people were doing by hand before it, and make sure that still happens or is written down, so nothing is lost without anyone deciding to drop it.

**Build what makes you different, reuse the rest.** *(26)*
For each piece of work, ask whether it's ordinary plumbing that already exists elsewhere or the thing that makes your product worth using. Reuse or buy the plumbing, and spend your effort on the difference.

**Close each cycle by feeding back what you learned.** *(00)*
Work gets easier over time when each round ends by recording what you learned and using it in the next: check first, build, show it works, then write down what you'd do differently.

**When a test and the facts disagree, check the facts.** *(13)*
If a check fails, first ask whether the check or the work is wrong. When you've researched how something really works, trust that and fix the check. When the behaviour is missing, fix the work.

---

## Left out, and why

| Entry | Why it has no row |
|---|---|
| 09 Integration testing | Engineering practice for building connectors. It's useful to a developer, but outside what a product-work assistant teaches, and its useful core is already in the rows drawn from 01 and 07. |
| 15 Testing with and without the database | Engineering-only. |
| 20 Omnibus session logs | About how the team records its own day. Teaching it would describe the machinery (leak list). |
| 25 Workstream review cadence | Internal-only (the design record says so). |

Entry 13 has a row, but it's the most developer-flavoured of the 14. CXO may cut it.

## Two points for CXO

1. **The three methodology questions in your section 7 fit what's here.**
   - "How should I check a fix is really done?" is answered by the first row and by 01.
   - "When should I stop and ask?" maps to the "ask when it matters" rule of the conduct layer (#2354), from 03.
   - **"What's wrong with an all-clear?" has no Proven entry behind it.** Its source is methodology-44 ("a report of nothing found means nothing unless it says what it looked at"), and 44 is still Emerging. Under the Proven-only rule it can't be taught yet.
   - I propose swapping it for **"How do I know a number means what I think?"** (row "A count isn't the thing you care about", 48). If 44 is graduated at the 12-29 audit, it comes back.
   - It's your call, since the set is yours to judge.
2. **Rows overlap with the conduct layer on purpose.** The conduct layer says what Piper does on every turn. These rows say what Piper teaches when asked. Rows 07, 47 and 48 are the same practice in both places, and the wording should agree after your pass.

Verified how: Status and Summary lines read this hour with `grep` over all 58 `methodology-core` entries. 19 are Proven: 15 covered by 14 rows, 4 left out (15 + 4 = 19), and 13 flagged. Checked against the spec's sections 2 to 4 by reading each row myself. No served check: these are corpus text, judged by CXO on served replies later.
