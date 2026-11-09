---
image: 'when-accuracy-scores-worse-tiny-ripple-giant-splash-ai-judge-applauds.jpg'
alt: 'An AI diving judge applauds an enormous, flailing splash while ignoring a nearby diver’s clean, nearly splashless entry.'
caption: '"Points for style!"'
---

# When Accuracy Scores Worse

*October 22–23, 2026*

When we got Piper Morgan to stop making things up, an automated quality score went *down*, because the judge preferred a full-sounding answer over a shorter true one.

# The 61-question catechism

A while back I decided that one way to ensure Piper can provide a core set of experiences to people was to come up with a list of "canonical queries" that Piper should be able to respond to competently. I compared it to a litany or even a startup sequence, and eventually it evolved into a test suite.

We were probing the alpha with the now 61-question test run, assessing both the quality of the routing (did Piper understand the request properly?) and of the response (did Piper answer the question correctly?). Routing is pass/fail but the replies are judged PASS, MARGINAL or FAIL by an LLM.

The first test my product assistant agent (Piper Alpha) ran that morning fell short of the expected-pass rate for both criteria. In terms of accuracy, 20 of the answers were rated as marginal and my chief experience agent (CXO) determined that five needed fixing, but that the rest were acceptable.

# Fixing the false replies

My lead developer agent (Lead) focused first on the incorrect replies. This included preventing Piper from responding "none" when no actual read had taken place. We pushed updates to the alpha three times during this bout of fixing.

That evening the test run showed some surprising results. The fixes worked in that the formerly false responses were now being handled honestly, but the raw quality scores dropped. The true answers were terse enough that the judge was rating them MARGINAL instead of PASS, despite their accuracy.

This meant that to assess the quality of the replies in a meaningful way, we've needed to depend on a second read of the results in which CXO makes recommendations about judgment calls for a human to decide.

We make sure that the raw figures are stored along with the waivers, so that we keep clear about what the instrumentation is telling us vs. what we are deriving from it. My principal product agent (PPM) also laid down the law to keep us from getting sloppy about quality: "A row that's false about the user's data can't be waived."

# Close enough for jazz

With a week left in the MVP milestone according to our current plan, I reviewed the recommendations and judged it "close enough", adding only a single document bug to the list of issues that had to close before any beta invitation went out.

In the long run, I need to take another look at this automated judge. Its preference for fuller-*sounding* answers results in misleading test results, and bears some review. We may be able to prompt the judge more carefully to better distinguish a high-quality answer from a confident-but-incorrect-or-padded reply.

I didn't feel super great about waving through some of these imperfect replies. Getting Piper to respond the way I want has proven to be a much more slippery challenge than I had ever expected. The voice and the accountability are coming into focus at last, while I'm still dialing in everything from fidelity to usefulness.

---

*Next on Building Piper Morgan: "Never Green in a Thousand Runs," in which I realize for the first time that some of my tests have never passed once.*

*Have you ever made your product better and seen a key tracking metric get worse? Did you add a fudge factor, start ignoring the metric, or redesign it?*
