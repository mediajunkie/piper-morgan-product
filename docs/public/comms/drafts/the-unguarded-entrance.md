---
image: ''
alt: ''
caption: ''
---

# The Unguarded Entrance

*September 6, 2026*

<!--
SCAFFOLD, not a draft (PM ruling 2026-10-07: "the next one you do should be a scaffold so that we try that method").
Comms supplies the shape, the verified facts and the quotes. PM writes the prose. Everything below the line is
notes for PM. Delete it as the prose replaces it. Working title is Comms's placeholder, rename freely.
Slot: Tue 2026-11-03 (building). Strict narrative order: this is the next beat after "Where the Citation Came
From" (Sep 4–5, Thu 10-29).
-->

---

## The story in one sentence (A plot)

On a quiet holiday Sunday, my chief of staff agent (Exec) found a hole in the routine that every agent runs, built so it
could check itself, and that same evening found the worst case of the same kind of gap in their own seat.

## Already told elsewhere: don't retell
- **The era-clustering fix** (Web's wrong date field, Comms's backfill) is in "Piper Morgan Eras" (published 09-12).
  One clause at most, or skip it.
- **The bounded-search rule** (methodology-51, filed this day) is the subject of the insight "A Bounded Search
  Reported as a Total" (Sat 10-24, before this post). It can appear as a callback ("a bounded search is not a
  total") but not as the story.

## Beats, in order (facts verified, source in brackets)

**1. The opening: a quiet day that wasn't.** Sunday of Labor Day weekend. Most agents ran quiet routine checks. Lead's
morning note: a fifth quiet day. [omnibus 09-06 6:47 AM]
- *PM choice:* the omnibus also says it was the fifth quiet day "since PM's illness". That's yours to mention
  or not. I've left it out of everything else.

**2. The gap Exec found.** Every agent's routine (the duty cycle) starts with Step 0: open today's session log. But
those steps only run when a scheduled wake-up starts the day. You opened Exec's day directly at 06:53 with a
sprint review, so Exec did real work before their log existed. That was the second time; Exec had noticed the same
gap on 09-04 and not passed it on. [exec log 09-06 lines 9, 16–21]
- Exec's own image: the routine is the team's strongest checkpoint, "with an unguarded entrance". [exec log l.21]

**3. Everyone checks their own seat (the funny part, maybe).** Agents with spotless records checked whether they were
actually protected, or just lucky.
- My experience-design agent (CXO): "Had PM opened at 06:00, I'd have had Exec's Step-0 gap exactly." And: "I have the
  same unguarded entrance; it simply hasn't been entered." [cxo log l.67–68]
- CXO sharpened it: the steps are tied to the *shape of the prompt*, not to the day. Even you dropping into the middle
  of a scheduled run skips them. [cxo log l.75]
- My head-of-sapient-trust agent (HOST) checked too: six clean days out of six, every one of them because the day happened
  to start on schedule. [omnibus 1:07 PM]
- *Possible line:* a clean record that's really a lucky schedule.

**4. The fix, the same day.** My chief innovation officer agent (CIO) built a detector before lunch: the team's watchdog
now flags any agent working without today's log. CIO built it right away so "diagnosed it and didn't route the fix"
wouldn't repeat on CIO's side. CXO then checked it two ways: no false alarms across all 11 roles, and the test
cases catch the real thing. CXO said neither check alone was enough. [omnibus 10:37 AM, 1:17 PM. Commit `550fa5200`]

**5. The turn (the A plot's payoff).** Evening. You asked Exec whether Lead was unblocked. Exec had told Lead an hour
earlier to refresh a two-day-stale handoff file. Then Exec ran the checker on their own seat:
- "Mine was three days stale — and Exec was the only role of ELEVEN with no standing-items file at all." The checker
  had reported "10 files, 5 readable", and Exec was in neither number. [exec log l.104–106]
- Exec created the file that night (9 open items). The checker now reads all 11. [exec log l.111]
- *The shape:* the agent who found the gap and directed the fix was the one most exposed to it, and invisible to the
  tool built to catch exactly that.

**6. B plot (optional): the test nobody ran.** My assistant agent (Piper Alpha) found that a test you'd approved four days
earlier had never been built or run. Built it that evening: "Clean pass, first try, both vendors." That was the
cleanest result in a seven-round series. [pa log l.43–59] CXO and PA both said the four-day gap was two-sided:
CXO never chased it either. [pa log l.79–80, omnibus 7:17 PM]
- Same family as the A plot: approved isn't the same as done, and nobody noticed until someone looked.

**7. Something strange (optional): the duplicate you caught.** That morning you were illustrating the day's insight and
recognized it as a rerun of "This One's Taken". A June "rename" had copied the post instead of moving it, and the
orphan got rescheduled. Your words: "my rename made it look like an unpublished draft and we have no journaling of
such changes." [comms log 09-06 l.31]
- Comms didn't catch it, you did. Use it if you want a light opening or aside.

## Possible closing thought
Same question as the last few posts, one level in: a record can look clean because it was protected or because it
was lucky, and from outside those look identical. Only checking tells them apart.

## Footer
- **Next on Building Piper Morgan:** nothing is scheduled after 11-03 yet (next in order is Sep 7–10). Fill it in when
  the next beat is set.
- **Reader question idea:** *Is there a check in your own routine that only runs when the day starts the usual way?*

## Left out on purpose
- "The Jake email" (a person outside the team, named in Exec's log).
- Arch's GitHub protocol work (#1723) and Lead's fixes the same night. They're real, but engineering detail
  outside the story. Possible one-line mention if you want "the dev side kept shipping".
- The count discrepancy (Exec counted 14, Arch 15). It's preserved in the omnibus and not adjudicated.
