---
image: ''
alt: ''
caption: ''
---

# Fixed and Scores Higher Came Apart

*October 22, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. PM writes
the prose. Everything below the line is notes for PM. Delete it as the prose replaces it.
Slot: Sun 2026-11-08 (insight). xian's pick, 11-04 ("I like the one about raw quality score falling").
Title is a working title, from the 10-22 omnibus's lesson 5. Footer teases Tue 11-10 (Never Green in a Thousand Runs,
working title).
Sources: PA 10-22 log (l.288-299, 331), CXO 10-22 log (l.32, 97, 107), PPM 10-22 log (l.60-61, 106, 149), 10-22 omnibus
(Core Theme 2, lesson 5), 10-23 omnibus (l.403). Comms opened each line quoted below at its source.
-->

---

## Title options (pick one, or your own)
- **Fixed and Scores Higher Came Apart** (working). The omnibus's own words for it.
- **The Score Went Down When the Answers Got True.** Plainest.
- **A Judge That Prefers Confident Answers.** About the measurement, not the fix.
- **Keep the Raw Number Next to the Read.** About PPM's rule, the part that generalizes.

## The principle in one sentence

When you fix an assistant so it stops making things up, an automated quality score can go *down*, because the judge
rewards a full-sounding answer over a short true one, so the number you need is a person reading what a user would
see, with the raw score kept beside it.

## The episode, in order (facts verified, source in brackets)

**1. The test.** #1386 criterion 2 was a 61-question run against alpha with two bars: routing (did Piper pick the
right action) and expected-pass (a model judge rates each reply PASS, MARGINAL or FAIL). [10-22 omnibus, Core Theme 2]

**2. Morning run.** PA's Run 1 scored expected-pass 24 of 42, **57.1% raw**. Both bars missed. CXO read all 20
MARGINAL rows and held five, including Q25 and Q51, because those replies were false. [PA l.48; CXO l.32]

**3. The fixes land during the day.** Lead landed the honest-answer fixes: list reads never answer "none" for a read
that didn't happen, the closed-issues count that was really a failed read, and others. Alpha was promoted three times.
[10-22 omnibus, Core Theme 3]

**4. Evening run.** Run A, on the fixed build, scored expected-pass 19 of 41, **46.3% raw**. In PA's words: "the
honesty fixes moved the false rows to true, while raw quality fell (57.1 → 46.3). The judge rates terse true answers
MARGINAL. So 'fixed' and 'scores higher' came apart, and the human waiver read is what measures what partners would
see." [PA 10-22 l.299]

**5. The human read.** CXO read the 20 MARGINAL rows, waived 18 with a reason each, and held two. Q27 stayed held
because it was wrong, attributing calendar events to the repo, and was filed as a new issue. Final: **38 of 41 (92.7%)
waived, 46.3% raw.** [CXO l.97, l.107; PA l.331]

**6. The rule that keeps it honest.** PPM's conditions: "A MARGINAL row is waived only with CXO's reason, and the raw
figure is always shown beside the waived one." And: "A row that's false about the user's data can't be waived." [PPM
10-22 l.60-61]

**7. Your call.** On 10-23 you judged it "close enough", with the condition that the document fix closed before any
invitation went out. [10-23 omnibus l.403. Ship #066 says the same in your words]

## Careful with these (accuracy)
- **It's two runs, not one controlled before-and-after.** 57.1% is the morning run (42 rows judged), and 46.3% is the
  evening run on a newer build (41 rows judged). Fixes landed between them. "The score fell as the answers became true"
  is accurate. "The fix lowered the score by 10.8 points" claims more than the data shows.
- The waiver isn't a fudge. Every waiver has a written reason, the raw number travels with it, and false-about-your-data
  rows can't be waived. Without that, this reads like grading on a curve.
- Q-numbers and issue numbers are for you, not the post (template rule 15).

## Where it goes beyond this week (the insight)
- Any automated judge has a taste. This one preferred fuller-sounding answers, and an honest "I couldn't check that" is
  short. When a fix changes the *kind* of answer, the old score stops measuring what you care about.
- The answer isn't "throw out the score". Keep the raw number, add a human read of the rows it flags, and write down
  the reason for each override.
- For a PM: the metric you set before a change can punish the change you wanted. Also the familiar trap: engagement
  falls when you stop a dark pattern.

## Already told elsewhere: don't retell
- **Ship #066** covered the run as news: "PA's Thursday re-run of the 61-question test met both bars once Lead fixed some
  mislabeled questions and CXO excused some answers, row by row with reasons." This post is the why behind "excused".
- **Ship #067's lesson, "Say what you didn't read"**, is about the fixes themselves. Stay on the measurement.

## Your angle, maybe
- How did "close enough" feel, signing off on a number whose raw form went *down*?
- Have you seen this shape in your PM work, where a metric moved the wrong way because the product got more honest?

---

*Next on Building Piper Morgan: [TEASE: Tue 11-10, "Never Green in a Thousand Runs" (working title). Confirm the
title first.]*

*[Reader question, yours to write. A start: "Has a number ever told you a change made things worse, when what it
really changed was what the number could see?"]*
