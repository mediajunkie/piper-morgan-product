---
image: ''
alt: ''
caption: ''
---

# Inviting Company In

*September 19 – October 7, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. You write the prose. Everything below the title and dateline is notes for you. Delete it as your prose replaces it.
Slot: Thu 2026-11-19 (building). Arc 1 of the narrative arcs (adopted 11-14). Title yours (11-17); working title was "Letting a Stranger In".
Sources: arcs planning doc "Arc 1 sourced" (a Sonnet subagent read the Sep 19 to Oct 9 omnibus logs; Comms re-opened every quote at source on 11-14, and re-checked three on 11-17).
-->

## The arc in one line (pick a through-line, or write your own)

1. **Before you let someone in, you find out what "in" means.** The build, the hosting and the sign-up path were all older or more broken than anyone knew.
2. **The first stranger kept being you.** What mattered surfaced through your own use, or through an agent's test account.
3. **The door is a decision, not a deploy.** Holding, lifting and shipping with known issues were product judgments, not green checks.

## Beats, in order (facts verified, source in brackets)

**1. Sep 19: hold the door.**
- A search of your Gmail shows hosted-alpha invites going out since July, on a stale template. Lead can't confirm which version alpha runs.
- You hold a new outside tester's invite: "I want to sort out the underlying issues before sending out the invitation. Too much unfinished business is piling up, chasing newer things." [HOST 09-19 l.469-471]
- That evening Lead reads the server: alpha is running a July 16 build.

**2. Sep 20: you are the first user.**
- A new build goes out.
- Your first real session on alpha, at 12:38 PM: you ask Piper to change yesterday's standup, and it replies "I've updated your standup:" over the unchanged draft. [issue 1836]
- HOST lifts the hold only after Lead walks the whole sign-up path with a real key.

**3. Sep 21-22: the invite goes out, and alpha moves.**
- The invite goes out with a dead code. A corrected one follows that evening.
- You approve the move to Fly, and it happens Sep 22. You, asked about the old data: "There is nothing irreplaceable for me on Fly, only test data so far." [decisions.log l.1991]

**4. Sep 24: an agent signs up like a newcomer.**
- Web redeems an invite the way a newcomer would. Setup fails, telling a hosted user to run Docker. "Both known entry paths lead to the identical dead end." [Web 09-24 l.15-16]
- Fixed the same day.

**5. Sep 25: what can a user do today? (optional)**
- Your question for the Ship: "what can a user or alpha tester do today that they couldn't on September 18" [omnibus 09-25 l.65].
- Four agents answered plainly: "no product change this window" [omnibus 09-25 l.250].

**6. Oct 5-7: the door rules, then the button.**
- Oct 5: bring-your-own-key ruled. Piper covers no one's LLM cost, "nominally a $0 budget stack" [decisions.log l.2373]. Beta starts when the MVP milestone closes.
- Oct 6: beta invitations are GitHub-only, and "ship beta with flagged known issues so testers do not report them" [decisions.log l.2381].
- Oct 7, the close: after your direct "ship", the invite button goes live on the site [omnibus 10-07 l.279].

## Careful with these (accuracy)

- **Not the first outside tester.** You had been sending hosted-alpha invites since July 12, and one outside person had already signed up on Sep 2. So say "a new outside tester", never "the first". (The Wall's live footer says "our first outside tester". That's my error, and fixing it is your call.)
- No names, emails or invite codes of any outside person. The logs carry some. Keep them out.
- Issue 1836 gives 12:38 PM. A later omnibus time is wrong.
- The old droplet's shutdown date isn't confirmed. Leave it out.
- Overlap: "The Server Has No Key" told Sep 12-15, and "Don't Overpromise" covered part of the known-issues idea. Tell this arc's side: who gets in, and when.
- This is the first arc post, so it covers three weeks, not a day-by-day. Choose beats. Beat 5 is the easiest to cut.

## Your angle, maybe

- A product isn't real until someone who isn't you tries it. Here, though, the first someone kept turning out to be you, or an agent pretending.
- Holding an invite is a product decision. Lifting it needed evidence (a walked sign-up path), not a feeling.

---

*Next on Building Piper Morgan: [TEASE: the Sat 11-21 insight, once you pick it. My suggestion is "A Blocker Framed as Yes or No".]*

*[Reader question, yours to write. A start: "Who was the first stranger to use your product, and were they really a stranger?"]*
