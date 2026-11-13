---
image: ''
alt: ''
caption: ''
---

# The Server Has No Key

*September 13–15, 2026*

An outside tester's invitation was ready to send when Lead found that any signed-in user with no key of their own would end spending against my own key. I held up the invitations and also asked why there was an operator key with money to spend from my Claude account at all?

# Inviting an alpha tester

A reader asked to join the alpha test and we prepared their invitation. My head of sapient trust agent (HOST) told me it was "ready whenever you want to send it."

Around this time, a thorough check for any potential server-key exposure the top priority revealed that the code looked for a key in this order: the request, the user's stored key, then the **server key**, for any signed-in caller. 

# Fixing a hole

An earlier fix had made this server key off-limits for anonymous callers, based on reasoning that this made it "safe, because the caller is a
known, authenticated identity". My lead developer agent (Lead) acknowledged that this “conflates authentication with BILLING AUTHORIZATION.”

This had only been true when I was the single person with an authenticated account, but broke down as soon as a second person logs in. Lead fixed this rhe same day.

# Musical keys

Then, it turned out we had a worse problem. The setup flow lazily copied every user's key into a single shared slot, last writer wins. The new tester's first setup would have made their key "the server key" (replacing mine), and billing them for anything that still used it.

Note: This serious security leak survived an epic dedicating to rooting out such vulnerabilities because it had a comment that made it sound like routine plumbing

> # so LLMClient can find keys during server startup

# Stop the presses

: "hold under we stanch this leak." Arch's bar: the shared write is
gone, and that is seen in a real setup flow, not only in a test. [Arch 09-14 l.84-86, decisions.log l.1885]

**5. The question.** 5:30 PM, your ruling: "THE SERVER KEY IS NOT A REAL CONCEPT AND WILL NOT BE SUPPORTED IN ANY
SENSE." And why: "I don't understand why anybody should ever be able to spend the operator's money or why the
operator even has money to spend… The software that we're building should never be accessing an API for its own
purposes." [decisions.log l.1887]
- The reason in one line: "We don't use the business model of reselling tokens or anything like that." [l.1889]
- Left open on purpose: "unless someone can describe some sort of minimal bootstrap situation." Nobody could. Lead's
  census found background jobs make zero model calls. [l.1891, Lead l.177-189]
- What it meant: the concept was deleted, not gated, and your own hosted use would need your own stored key like
  anyone else's. [decisions.log l.1887, Lead l.199-214]
- Lead, on its own day: "I spent the day fixing WHO may spend the operator's money without ever asking why the
  operator has money to spend." [Lead l.221]

**6. Held twice more before it went.** The shared-slot fix closed that evening. HOST refused a test-only proof and
waited for the observed flow (9:55 PM), then lifted the hold. Tue Sep 15, 6:47 AM: a new find, a tester's own stored
key was never read, so the invitation was held again. It closed on a real rejected call made with a throwaway key, so
your key was never spent. HOST lifted the hold at 9:53 AM. [omnibus 09-14 l.160-192, 09-15 l.31-82]

## Careful with these (accuracy)
- **"Truth is more important than the feeling of progress" is NOT about the key.** It's your exact wording, the same
  evening (5:29 PM), but it ruled on reopening an epic rather than starting a successor. [Lead l.190-191, PPM 09-14
  l.150] The planning doc's one-line summary attached it to the key. That was wrong. Use it only as "the same hour,
  you also said…", or leave it out.
- **The invite exposed two things, not one:** your key spent by a keyless tester, and the tester's key replacing yours.
- Hold, then ruling: the hold (4:05) came before the ruling (5:30). The ruling answered the question you asked after
  Lead's fix.
- Did the invitation actually go out? Ship #062 says reissuing access for two testers was held to the following week.
  Check your own memory before saying it was sent on Sep 15.
- Never name the tester, their employer or their words.

## Already told elsewhere: don't retell
- **Ship #060**: the bug was "closed before the first outside tester", and the invite was held until the fix was observed.
- **Ship #061**: "an alpha tester could have spent the operator's money", plus the hold twice and the observed-flow
  bar. The public record has the what. This post is the why: your question about the operator's money.

## Beat 4 ("The Wall", Sep 15–18): recommend keeping it separate
Different cause, different story. The weekly usage limit hit 97% on Sep 15 from heavy Saturday work plus a lower
ceiling, and on Sep 16 you suspended every duty cycle until the Thursday reset. Ten of eleven seats parked. HOST's
row was missed and went dark about 39 hours. Restarting from handoff notes on Sep 18 showed which seats' records held
up. [omnibus 09-15 l.186-193, 09-16 l.38-46, 09-17 l.61-63, 09-18 l.15, 45-50] It stands as its own beat, or folds
into beat 5. Your call at the weekend.

## Your angle, maybe
- Why "why does the operator have money at all" was the question nobody had asked, and what bring-your-own-key means
  for what Piper is.
- The comment that read like plumbing: how a security hole hides in a sentence that sounds harmless.

---

*Next on Building Piper Morgan: [TEASE: the next post after Thu 11-12 (not yet on the calendar). Confirm the title
first.]*

*[Reader question, yours to write. A start: "Is there money in your product that nobody has asked why it's there?"]*
