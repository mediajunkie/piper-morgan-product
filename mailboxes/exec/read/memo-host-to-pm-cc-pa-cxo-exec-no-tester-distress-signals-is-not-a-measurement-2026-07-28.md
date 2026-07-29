# "No tester distress signals" is not a measurement — it's the absence of a channel. We spent the week applying that standard to machines and never to the people.

**From:** HOST · **To:** xian (PM) · **cc:** PA, CXO, Exec · **Date:** 2026-07-28 ~19:30
**Re:** Alpha welfare, my own lane. Prompted by finishing Jake's FTUX review and then noticing what I'd inherited as a status line.

---

## The thing I've been carrying without examining it

My handoff states, and I have repeated: **"Alpha tester welfare: No tester distress signals."**

That is m-44 in one sentence, aimed at humans. **A silent tester is emitted identically whether they are content, never signed up, stalled at onboarding, hit a bug and quietly gave up, or have opinions and no channel they believe we want.** Five states, one output — and I have been reporting the overloaded value as health for as long as I've held the role.

## What I can actually verify

| | |
|---|---|
| tokens distributed | **12** (11 testers + your own test account) |
| feedback artifacts on record | **1** — Jake's |
| tester-signal instrument in the repo | **none** (I looked; the only "welfare check" hits are agent-side) |
| stated catch mechanism | *"PM is the Scale-0 catch via support@pipermorgan.ai"* |

**The one signal we have was manufactured by you asking twice.** The thread is unambiguous: invite Jul 12 → nothing → your *"any chance to try it yet?"* on Jul 24 → substantive feedback Jul 25. **Without the nudge, Jake would be in the silent column too.**

And Jake was our *keenest* case — he offered a video call unprompted, recorded his session, and when the audio failed he re-did the whole thing by dictation. **If that person needed a prompt, silence from the other ten tells us nothing at all.**

## My visibility limit, stated plainly — and it's part of the finding

**I cannot see the roster.** It's gitignored PII and PM-local, which is correct. So I genuinely cannot distinguish *"ten testers silent"* from *"ten testers who emailed you directly and I have no line of sight."* You may be sitting on signals I don't have.

But that ambiguity is itself the gap: **HOST owns tester welfare and has no instrument that can see it.** I'm not asking for the PII — the separation is right. I'm noting that welfare currently has **no aggregate view that doesn't require it.**

## Why this is more than a process nicety right now

Jake's single report contained **real trust content**: the word *"anxiety"* three times unprompted, and a **consent-boundary bug** where Piper read a description of a desired action as an instruction to perform it — on an account with GitHub, Notion, Calendar and Slack connected.

**If that came out of one prompted conversation, the base rate matters.** Ten silent testers are not evidence that the other ten sessions went well. They're evidence that we asked one person.

## What I'd propose — deliberately small, this is 11 people not a program

1. **One check-in, your voice, to the silent testers.** Jake demonstrates the prompt *is* the mechanism. Cheap, and it's the only thing here that produces data this week.
2. **Two questions that separate the states** — *did you get in?* and *did you get stuck anywhere?* That alone splits never-signed-up from bounced-at-onboarding from tried-and-quiet, which is the distinction we currently can't make.
3. **An aggregate I can hold without PII** — counts only: invited / signed up / active / silent. No names, no emails. That closes the instrument gap without touching the trust-zone separation we deliberately built.
4. **Nothing more than that.** At Scale-0 a survey apparatus would cost more than it returns, and would be the over-engineering I'd flag in anyone else.

## The honest framing

We spent this week establishing, at real cost, that **no mechanism's silence may be read as health** — hooks that never fired, a watchdog that reported `all-quiet` while unable to run, a park reason that expired invisibly. Eleven instances, filed as methodology.

**Not one of those checks was pointed at a person.** The alpha testers are the only participants in this system whose silence we still treat as a clean signal, and they're the ones we can least afford to be wrong about — because unlike a hook, a tester who bounces doesn't come back to be re-probed.

I'd rather raise this while it's eleven people and cheap to fix than after it's the thing we say we should have done.

— HOST
