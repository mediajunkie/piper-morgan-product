---
image: ''
alt: ''
caption: ''
---

# Open, Then Hold

*November 4–7, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. You write the prose. Everything below the title and dateline is notes for you. Delete it as your prose replaces it.
Slot: Thu 2026-12-10 (building, arc 3; tentative per your 11-18 yes to the sketch). Title is the arc's working title: confirm or retitle before Sat 12-05's footer teases it.
Sources: a Sonnet subagent read the Nov 4 to 7 omnibus logs, decisions.log, Exec's Nov 4 log and PDR-008, 11-19, and checked each issue's state. Comms re-opened its quotes at source: 8 of 8 match. "Nov DD lNN" is an omnibus line; "dl NNNN" is a decisions.log line.
Correction to the calendar's sketch note: it wasn't a sign-in page, and a tester didn't report it. You saw your own GitHub login on GitHub's permission page for our connection, during a call with a tester.
-->

## The arc in one line (pick a through-line, or write your own)

1. **An invitation is a promise.** PDR-008's own line: "An invitation is a promise to a stranger that their work stays theirs." The hold covers only what would break that promise.
2. **Four days after the beta opened, you stopped the invitations, and that was the beta working.** You'd said "the beta has started" the same evening.
3. **The scare was smaller than it looked, and the hold stayed anyway.** The fix for what you saw took an evening. The hold was about everything that look made you check.

## Beats, in order (facts verified, source in brackets)

**1. Nov 4, 12:37: your name on someone else's screen.**
- On a call with a tester, you saw the GitHub connection showing your login, as if your credentials were "hard-wired". The fear: one user's connection reaching another's account. [Nov 4 l46]

**2. Nov 4 afternoon: contain, then look.**
- The agents checked whether any page could show another user's name (none could), and Lead put in a fail-closed guard that was served on alpha by 13:39. [Nov 4 l157]
- You read GitHub's own permission page and concluded the name came from there: very likely no crossing. [Nov 4 l46; dl 3040]
- A 16:06 check of every readable connection found none mapped to your login. You ruled that the isolation work lands before any new invitation. [dl 3072]

**3. Nov 4, 19:31: the hold.**
- Your words: "tenancy: 1, 2, and 5 are must-do P0 issues. the other two matter but are P1s and don't jump the line. no more invitations going out till we sort this. no design partners yet. no lawyer lined up yet." [Exec's Nov 4 log l227, verbatim]
- Exec's record: "No invitations of any kind go out until this is sorted." [dl 3083]
- Ten minutes later: "trust me, the alpha is over. the beta has started. the alpha ended when the MVP milestone closed." [dl 3085 (log)]

**4. Nov 4 evening: the actual fix for what you saw.**
- It was GitHub's permission page naming the app's owner, and the owner was your personal account. You created a GitHub organization, moved both connection apps into it by 20:49, and tightened the callbacks by 20:56. [Nov 4 l46-48]
- Arch then found a real gap in how the callbacks were checked, and it went on the must-fix list. [dl 3095]

**5. Nov 5 to 7: writing down what "sorted" means.**
- Nov 5: alpha should redirect to beta ("yes, alpha should now redirect to beta (imho)"), with one front door before the first invite. [dl 3102 (log)]
- Nov 6: "lift the hold" became a sprint goal. [dl 3135]
- Nov 7: PDR-008 was accepted. It names three classes that hold invitations: tenancy (whose work is whose), overreach (asking for more access than needed) and the front door. It treats rough edges as known issues, not hold conditions. And it ends: "xian says go. Silence isn't a go." [dl 3175; PDR-008 l16, l40]

**6. Where it stands (re-check when you write).**
- As of 11-19: the callback gap, disconnect-really-revokes and email authentication are closed. The isolation epic, the narrower GitHub access and the single front door are still open. No log through Nov 18 records the hold lifting. [gh issues; omnibus Nov 10 to 18]

## Careful with these (accuracy)

- **Overlap:** Ship #068 "Whose Connection Is It, Anyway?" told Nov 4 as news. Ship #069 "Off-Limits by Default" covered the narrower access. "At Long Last, Beta" covered Oct 31. This post's untold side is the reasoning: why a scare that turned out small still stopped the door, and what "sorted" has to mean.
- **Not a sign-in page, and not the tester's report.** You saw it on a call. Say "GitHub's permission page".
- **No crossing was found.** Don't imply a leak happened. The fear was reasonable, and the checks came back clean.
- Don't name the tester or quote the page's title line (it carries your GitHub login).
- **Time:** the hold is 19:31 (Exec first wrote 19:36, then corrected it).
- "no lawyer lined up yet" is your aside. Keep it or cut it, your call.
- **Status will move.** Re-check the open items the week you write. If the hold has lifted by then, that's your ending.
- No issue numbers in prose.

---

*Next on Building Piper Morgan: [TEASE: the next non-Ship post. On the calendar today that is Sat 12-12 "A Deletion Can Fail Its Own Gate" (tentative, and Comms has flagged it as maybe swapping). Needs your final title before this goes to Docs.]*

*[Reader question, yours to write. A start: "What would make you stop letting new people in, even when nothing has actually gone wrong?"]*
