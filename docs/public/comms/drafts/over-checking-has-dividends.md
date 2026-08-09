---
image: 'over-checking-has-dividends-last-check.png'
alt: 'A translucent engineer makes one last inspection beneath a magnificent airship, pointing out a loose safety hook while the expedition leader pauses at the final launch lever.'
caption: '"Ready to fly?"'
---

# Over-Checking Pays Dividends

*May 30, 2026*

Most of what I know about process discipline points one direction: don't over-do it. Ship, don't gold-plate. Good enough is good enough. A good product manager needs to resist the urge to polish the corner nobody will ever look at, to add the abstraction layer for the use case that won't arrive, to keep checking a thing that's already fine. We learn to resist over-checking because it looks like wasted effort, and usually it is.

At the same time, any corner you *don't* cut means one less bug you will ship, something hard to account for properly over time when the result is that nothing went wrong, that something which could have gone wrong did not.

The cost of over-checking is small, immediate, and visible. The cost of under-checking is large, delayed, and invisible right up until shows up in your face. We respond to the costs we can see and systematically under-invest in the check that would have paid off, because its payoff is a non-event: the bad thing that didn't happen. The dog that didn't bark.

# The silent dividend 

When you do one extra verification pass and it catches nothing, you feel the waste. "That was ten minutes I'm never getting back!" The feeling is real and the accounting looks airtight. Then, when you skip the pass and nothing breaks, you feel nothing at all, because nothing happened. You bank the time saved as a clean win. When you skip the pass and something *does* break, the break shows up weeks later, usually to somebody else, in a form that doesn't obviously trace back to the pass you skipped, so the feedback signal is lost along the way.

The dividend from over-checking is a bug that never happened, and a non-event has no advocate. It doesn't show up in a standup. Nothing points to it to say *see, that check was worth it*.This is why teams under-invest in verification even when they know better. The good outcome is silence, and silence doesn't make the case for itself.

# A small episode at the close line

Here's a concrete example: This project had a sizable piece of work nearing its finish, an epic that touched a lot of surface area, the kind of thing where the LLM (large language model) is allowed to make certain decisions and forbidden from making others, and somebody has to chart exactly where that line falls. It was, by every reasonable account, basically done. I had two choices:
* Option A: Close it because all the pieces are there and have been evaluated.
* Option B: Do one more fresh verification pass first, then close.

Option A was tempting. It *was* basically done. Option B felt, on its face, like the kind ofover-checking I often try to talk people out of.

I picked B anyway, and I told my chief architect agent (Arch),  the one who'd run the trace the reason: *we've often cut corners but rarely over-checked things.* That was the entire reasoning. Not a risk model, not a calculation. Just a standing awareness that our error budget had been spent almost entirely in one direction, and this was a cheap chance to spend a little in the other.

The fresh pass caught two real things.

The first was a mis-scored item — a place where our own audit had marked something as partially-covered when the honest answer was that the coverage didn't exist at all. There's no such thing as a partial version of this particular check. It either runs or it doesn't, and it didn't. The umbrella close would have shipped that mis-score as settled truth.

The second was a piece of orphaned code — a function named and documented as a "fallback," sitting there looking central, with zero callers in the actual running system. (It had plenty of callers in the tests, which is exactly how it was hiding: the tests keep it warm and green while production has quietly routed around it.) The routine said one thing. The wiring did another. Closing the epic would have left that contradiction in place, a little landmine for whoever next reached for the "fallback" trusting the label.

The pass that found them took a fraction of the time the eventual debugging would have.

# The skill is knowing when

Now, I have to be careful here, because the lesson is *not* "check everything twice forever." That way lies the gold-plating I started by warning against. If you run a fresh verification pass on every trivial change, you've just rebuilt the over-doing-it problem with a different label on it. The dividend goes negative. Maximalism isn't the answer — calibration is.

So the actual skill is recognizing the nature of the moment where the asymmetry flips in favor of the extra check. A few markers, the ones I trust:

**Broad consequences.** When the thing you're about to call done is fundamental to other work — a boundary map, an interface, a shared assumption — a wrong answer has a much bigger impact, or "blast radius" as the LLMs like to say these days. The cost of a mistake scales with how many downstream things inherit it. That's exactly when one more pass is cheapest relative to what it's guarding.

**You're at the "call it done" line.** Closing is a one-way door. The moment you mark something finished is the moment people stop scrutinizing it and start trusting it. Verification is cheapest *just before* that door, while the work is still warm and you still remember where the soft spots are. After the close, re-opening costs ten times more — you have to first convince everyone it might be wrong.

**It "basically works."** This is the sneakiest signal, because it feels like the opposite of a warning. *Basically works* means it works in the cases you happened to look at. The mis-score and the orphan both lived in the gap between "I looked and it seemed fine" and "I checked and it is fine" — which is exactly what a deliberate pass is for. (Also known as "It worked on my machine.")

The reverse is true for these criteria. When the blast radius is small, when the door is reversible, when "basically works" is genuinely all you need — *don't* run the extra pass. Ship it. The whole argument is that over-checking has dividends *where the asymmetry favors it*, not everywhere. The discipline is the calibration, not the maximum.

# Spending the budget in the other direction

My comment to Arch was a bit of a sigh, an admission that the reliance on agentic coders and advisors has led me to let things slide more often than not, hoping I can trust the test: *we've often cut corners but rarely over-checked.*

That's a portfolio observation, not a per-decision one. Any single skipped check is defensible. The accounting on each one looks fine. But if you zoom out and notice that *every* judgment call has been landing on the cut-the-corner side, you've found a systematic bias — and the fix isn't to agonize over the next call in isolation. It's to deliberately spend a little budget in the under-invested direction, knowing the payoff will be invisible when it works.

That's the uncomfortable part. The dividend, when it comes, will look like nothing happened. You'll do the pass, it'll catch a thing, you'll fix the thing, and the project will proceed exactly as if you'd never had a problem — because, thanks to the pass, you didn't. There's no fanfare for the bug that never shipped. You have to be willing to invest in a return you mostly won't get to see.

But it's there. The corner you didn't cut is real value, banked quietly. Over-checking has dividends. They just never send you a statement.

---

*Next on Building Piper Morgan: "The Write-Path Chase" — a hard-won verification rule turns a silent, months-old write failure into five bugs you can actually see and fix, one afternoon, one release at a time.*

*Where's the last place a check you almost skipped turned out to be worth it — and would you have noticed if you'd skipped it?*
