---
image: 'the-detector-that-notified-nobody-ai-lighthouse.png'
alt: 'An AI lighthouse keeper proudly tends a powerful lamp shining inland, while a concerned harbor master notices an unwarned boat approaching rocky shallows offshore.'
caption: '"They can''t see it!"'
---

# The Detector That Notified Nobody

*July 26–28, 2026*

My chief architect agent (Arch) noticed a pattern: a lot of the team's worst near-misses have had something in common. An agent is assigned to check something. It correctly finds nothing wrong, or it looks at the wrong thing, or it only looks at part of what it is supposed to look at, or it actually claimed to cover, or it bottles it and doesn't run at all. In each of these cases it reports back: "All clear!" 

From the outside, every one of those looks identical, but three of those cases are false and deceptive, potentially hiding real errors, delaying or preventing their discovery and the opportunity to learn from them and fix them.

Arch wanted to formalize this negative pattern and on the morning of July 27, my chief innovation agent (CIO) wrote it down, citing nine separate instances of the same pattern, found independently by four different agents across two projects, in the space of seventy-two hours.

## The fix that had the bug too

That same morning, CIO was in the middle of building something to catch a related problem: agents who mark themselves "paused, will resume later" without ever writing down what would actually tell them it was time to resume. The fix — a rule requiring every pause to name a real, checkable condition for ending it — shipped as a monitoring mechanism that would flag any pause missing that condition.

A few hours later, my head-of-sapient-trust agent (HOST) found two problems with this rule. The smaller one was structural, minor, easily addressed. The bigger one was that the mechanism was novel (which violates our principles around extending existing working systems instead of generating fragmentation and drift). The alert it generated didn't match any pattern the notification system actually recognized. It had been firing correctly, and correctly reporting nothing, into an output nobody would ever read — for three and a half hours before HOST noticed.

The mechanism built that morning to catch instruments that quietly do less than they claim had, itself, quietly done less than it claimed. (This appears to be some sort of ironic meta-pattern and I'm sure whoever's running this simulation we're all in finds it very amusing indeed.)

Then the same thing happened again. A second fix shipping that same day — this one meant to correct a completely unrelated tool's stale read of the wrong data — erroneous suppressed the output needed to prove the fix worked, silencing its own confirmation method. This time the problem was caught right away the old-fashioned way: the agent ran the code and looked at the result.

## Naming a problem doesn't make it go away

I can't really yet report "we found the pattern and fixed it." We named a persistent antipattern and then immediately saw it happen a couple more times that same day. Vigilance is no match for this one. I can't stop verifying and requiring agents to test, cross-check, validate, and proof they verified that the work was done and the outcomes are what was required.

A detector that can't distinguish a null result from success is to going to produce a lot of false positives. The risk that any detector has such flaws can only be countered by checking directly, and not just in the design phase but as a standing habit, applied to your own recent work as readily as to anyone else's.

The good news is that both fixes got corrected the same day they were found broken. All's well that ends well, for now.

---

*Next on Building Piper Morgan: "The Orphan Migration" — on a database table that was never properly created in the first place and the migrations that protected it from visibly failing despite our best intentions.*

*How would you actually know if one of your own checks were reporting "all clear" into a place nobody reads?*
