---
image: 'inviting-company-in-welcome-despite-the-unfinished-wall.jpg'
alt: 'A nervous host welcomes a smiling guest carrying flowers into a cozy living room, while a translucent AI helper pauses beside a half-painted wall.'
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

Because the product runs on a "bring your own key" model" and does not resell tokens (a dying business anyhow, what with Claude's new "[linked billing](https://support.claude.com/en/articles/18467148-use-your-claude-platform-account-in-a-third-party-app)" feature), I had to make it 100% clear that Piper has no token budget of their own. I am not paying to subsidize anyone's use of a remote LLM. I also reminded the team that this project started out with the concept of a "$0 stack" although that has become sort of a nominal concept as I've shelled out for subscriptions, hosting, and so on.

I also had to remind the team again that completing the MVP milestone was the trigger for starting the beta (and the Production milestone). I told the team that even when we go to beta the software will still be buggy and that we must flag any known issues so testers are prepared and don't waste their time or ours reporting them.

# Open for business

Once we sorted this all out I approved sending the invitation and we also add a button to the site where people could ask to try the alpha or to join the waitlist for the beta.

Once again, I braced myself for incoming feedback. It's amazing how valuable it is and how I still cringe about putting something that isn't "ready" in front of people I want to respect me. Then again, if I was afraid of criticism, I'd never ship anything at all.


---

*Next on Building Piper Morgan "A Blocker Framed as Yes or No," in which I have to give my agent team some straight talk about how much work they've been assigning me.

*Do you feel that same mixture of thrill and dread when asking people to review your work?*
