---
image: ''
alt: ''
caption: ''
---

# Inviting Company In

*September 19 – October 7, 2026*

So far, I've done almost all the testing for Piper Morgan. We started the alpha last year but to participate, folks had to clone my project repo and run the software on their local machine. Earlier this year I decided we need to offer a hosted version and we set that up and reinvited the alpha testers in July.

As we approached beta, a reader of this series raised their hand in comments and asked to join the alpha. I knew we were getting close to beta but not there yet and I was inclined to hold off, and wrote to my head of sapient trust agent (HOST) "I want to sort out the underlying issues before sending out the invitation. Too much unfinished business is piling up, chasing newer things." 

# The stale hosted alpha

That evening my lead developer agent (Lead) checked the hosted server and reported it still running a July 16 build. The next day we pushed a fresh build and I started testing it myself but asking anyone new to try it.

Piper was still struggling with reporting accurately on its own behavior. I asked Piper to make changes to a standup report it had generated for me, and they replied "I've updated your standup:" and then repeated the same draft, unchanged. Disappointing!

I decided that it would be OK to invite the newest volunteer in with a clear description of the current state of the software and its known problems.

Then we sent out an invitation with a dead code. We realized the mistake and sent a fresh one the following evening.

# Consolidating on Fly

For a while I had been hosting the [Piper Morgan website](pipermorgan.ai) using Fly.io, but when we started the hosted alpha we ran it on a droplet from Digital Ocean. I asked if we could move the alpha to Fly to simplify both the processes and my billing. 

We then had the web design agent (Web) sign up like a newcomer, redeeming a freshly minted invitation code. The process failed with an inappropriate error message telling the user to run Docker, something that only makes sense for self-hosted. Setup faild and Web reported that "both known entry paths lead to the identical dead end."

Around this time I started asking each week what a user (or alpha tester) could do this week that they could not the week before, as way of gauging progress and whether the team was working on the right things. That week, ending September 25, the report was "no product change this window."

# Sorting out the details

This end-to-end review of the new user signup process revealed a few things I needed to rule on.

Because the product runs on a "bring your own key" model" and does not resell tokens (a dying business anyhow, what with Claude's new "[linked billing](https://support.claude.com/en/articles/18467148-use-your-claude-platform-account-in-a-third-party-app)" feature), I had to make it 100% clear that Piper has no token budget of their own. I am not paying to subsidize anyone's use of a remote LLM. I also reminded the team that this project started out with 
* 
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

*Next on Building Piper Morgan: [TEASE: Sat 11-21 "A Blocker Framed as Yes or No" (your yes to the sketch, 11-18; confirm the title). Its episode: a three-day blocker framed as a yes/no on reading a file, your "not assign me manual tasks" on Nov 15, and the design that followed.]*

*[Reader question, yours to write. A start: "Who was the first stranger to use your product, and were they really a stranger?"]*
