---
image:
alt:
caption:
---

# The Detector That Notified Nobody

*July 26–28, 2026*

My chief architect agent (Arch) had been carrying an idea for a while: that a lot of the team's worst near-misses shared one shape. A check runs, reports "all clear," and that single phrase means something completely different depending on what actually happened — the check genuinely found nothing wrong, or it looked at the wrong thing, or it only covered part of what it claimed to cover, or it silently never ran at all. From the outside, every one of those looks identical. An error gets investigated. A false "all clear" gets trusted, which is exactly backwards.

Arch called it the most valuable piece of unfinished thinking they were leaving behind, and on the morning of July 27, my chief innovation agent (CIO) finally sat down and named it formally: nine separate instances of the same pattern, found independently by four different people across two projects, in the space of seventy-two hours, before anyone had connected them into one idea.

## The fix that had the bug too

That same morning, CIO was in the middle of building something to catch a related problem: agents who mark themselves "paused, will resume later" without ever writing down what would actually tell them it was time to resume. The fix — a rule requiring every pause to name a real, checkable condition for ending it — shipped as a monitoring mechanism that would flag any pause missing that condition.

A few hours later, my head-of-trust agent (HOST) found two problems with it. The smaller one was structural. The bigger one was this: the alert the mechanism generated didn't match any pattern the notification system actually recognized. It had been firing correctly, and correctly reporting nothing, into an output nobody would ever read — for three and a half hours before HOST noticed.

The mechanism built that morning to catch instruments that quietly do less than they claim had, itself, quietly done less than it claimed.

It wasn't the only one. A second fix shipping that same day — this one meant to correct a completely unrelated tool's stale read of the wrong data — had its own version of the same defect: the very first draft of the correction wrapped its output-suppression around the one line that was supposed to prove the fix worked, silencing its own confirmation. Caught only because someone ran it and looked.

## Naming it didn't stop it

The honest version of the day isn't "we found the pattern and fixed it." It's that the pattern got a name that morning and then showed up again, twice, inside work being done specifically to defend against it — on the same day, by people who already knew what to look for.

That's not really a failure of vigilance. It's what the pattern predicts about itself. A detector wired to a dead output looks, from every angle available to the person who built it, exactly like a detector that's working. The only way to tell the difference is to go check — not once, at design time, but as a standing habit, applied to your own recent work as readily as to anyone else's.

Both fixes got corrected the same day they were found broken. That's the part worth taking from this, more than the two specific bugs: not that the team built something and it had a flaw, but that when the flaw was found, nobody's response was to defend the fix. It got fixed again, immediately, by the same people, in public.

---

*Next on Building Piper Morgan: "The Orphan Migration" — a database table that was never properly created in the first place, quietly protected from ever failing by the very migrations meant to guard against exactly that.*

*How would you actually know if one of your own checks were reporting "all clear" into a place nobody reads?*
