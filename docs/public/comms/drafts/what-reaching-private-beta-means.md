---
image: ''
alt: ''
caption: ''
---

# What Reaching Private Beta Means

*October 30–31, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. PM writes
the prose. Everything below the line is notes for PM. Delete it as the prose replaces it.
Slot: Sat 2026-11-07 (building, milestone piece, outside the Sep-front order like "Almost Beta" and "Alpha Launches").
xian said yes 11-04. TITLE NEEDED BEFORE THURSDAY: Thu 11-05's footer teases this post.
Footer teases Sun 11-08 "Fixed and Scores Higher Came Apart" (working title).
Sources: decisions.log 2026-08-08 (via 09-06), 09-06 ~07:0x and ~16:1x, 10-29 13:02, 10-30 14:52, 10-30 20:52, 10-31 13:51,
11-04 19:31 and 19:41; #1386's last two comments (PPM 10-30 17:37 and 19:51); GitHub milestone "MVP" (closed
2026-10-31T00:07:54Z = Fri 10-30 17:07 PT); the Ship #067 week review; published posts "Almost Beta" (07-23),
"A Sender-Impersonation Bug, Four Days Before Beta" (09-01), Ship #067. Comms opened each line quoted below at source.
No recipient is named anywhere (rule 8). Keep it that way.
-->

---

## Title options (pick one, or your own. Thursday's footer needs it)
- **What Reaching Private Beta Means** (working, Docs' row).
- **Beta, With Nine Known Issues.** The letter said what doesn't work yet, by name.
- **Eight Weeks Late, on the Day We Set.** Beta slipped from early September, then landed on the reset date.
- **The Alpha Is Over.** Your words, 11-04.
- **Almost Beta, Then Beta.** Calls back to the July post.

## The story in one sentence

Beta was "four days away" on Sep 1. On Sep 6 you reset the date to Oct 30 and admitted the gate's evidence would go
stale. On Oct 30 the MVP milestone closed on that date, and the next day you sent the private-beta letters, each one
saying in plain words what Piper still gets wrong.

## Beats, in order (facts verified, source in brackets)

**1. The near miss.** The blog already told readers beta was close: "Almost Beta" (Jul 23) and "A Sender-Impersonation
Bug, Four Days Before Beta" (Sep 1). On Aug 8 you had already moved beta back a month, without a new date: "we clearly
have a lot more work still to do than anyone ever reported to me." [decisions.log 09-06 ~07:0x, quoting 08-08]

**2. The reset.** Sep 6, early morning: MVP moves to **Oct 30**, then Production Feb 2, and so on. [decisions.log
09-06 ~07:0x] That afternoon you ruled the last gate line ("PM go/no-go") fires at MVP close, not then, because the
gate's evidence was point-in-time: "beta moved eight weeks out from under them." [decisions.log 09-06 ~16:1x]
- This is also the subject of Tue 11-03's "The Unguarded Entrance" (Sep 6). Point back to it lightly, or don't.

**3. Eight weeks of making Piper say what it doesn't know.** Don't retell these, just name the arc. The building
posts and Ships #060–#067 carry it: failed reads that said "none", promises the code didn't keep, a router that wasn't
live. Your 10-28 ruling that the confabulations "require more than patching" is the turn. [Ship #067 week review]

**4. Calling one a known issue.** 10-29: the two-step milestone question passed one day and failed the next. You:
"we can admit this one is trickier than it looks and call it out as a known issue." It went off the gate and into the
letter. [decisions.log 10-29 13:02]

**5. The day.** Fri 10-30: you chose the beta build and the re-checks before any invitation. [decisions.log 10-30
14:52] The MVP milestone closed at about 5:07 PM, on its due date. [GitHub milestone MVP, closed_at] That evening:
"We can all catch our breath and then discuss priorities in the first sprint of the journey to our next big
milestone, the Production release." [decisions.log 10-30 20:52]

**6. The letter.** It carried **nine** known-issue lines, each checked against an open issue at send time ("9 of 9
hold"). [#1386, PPM 10-30 19:51] Among them: Piper can misread what you ask, an answer about your own data can be wrong,
it can state a detail it didn't look up, and there's no undo for a deleted to-do. [#1386, PPM 10-30 17:37] You sent
them Sat 10-31. [decisions.log 10-31 13:51]

**7. What beta means, per you.** "trust me, the alpha is over. the beta has started. the alpha ended when the MVP
milestone closed." [decisions.log 11-04 19:41]

**8. Optional coda, your call whether it's public.** On 11-04 you held all further invitations until three security
items are done: "No invitations of any kind go out until this is sorted." [decisions.log 11-04 19:31] It fits the
post's theme (beta is a door you can close again), but it's very fresh. Leave it out if you'd rather it surface in
Ship #069.

## Careful with these (accuracy)
- **Private** beta: invitation only, sent personally, in waves. The public site offers a waiting list
  (pipermorgan.ai/try/beta/), not sign-up. Don't imply anyone can join now.
- Don't count recipients or name anyone. The letters' recipients and codes are held privately on purpose.
- "On the day we set" is true for the milestone (due Oct 30, closed Oct 30). The letters went the next day.
- The known-issues quotes are paraphrases from PPM's table, not the letter's exact copy. If you quote the letter, take
  the words from `beta-invitation-letter-draft-2026-10-30.md`.

## Already told elsewhere: don't retell
- **Ship #067** (11-04) ends: "Since Thursday, the MVP closed on Friday, which ended the alpha, and the private beta
  began with Saturday's invitations." This post is the meaning, not the news.
- **Ship #068** (Wed 11-11) will cover Oct 30–Nov 5 as news. Leave the sprint details for it.

## Your angle, maybe
- What it felt like on Oct 30, against Ship #067's P.S. ("There are times I never thought I'd get this close").
- Why a letter that lists what's broken is the right way to invite people.
- What "beta" means to you as a PM, compared with how products usually use the word.

---

*Next on Building Piper Morgan: [TEASE: Sun 11-08, "Fixed and Scores Higher Came Apart" (working title). Confirm the
title first.]*

*[Reader question, yours to write. A start: "When you launch something, what do you tell people it can't do yet?"]*
