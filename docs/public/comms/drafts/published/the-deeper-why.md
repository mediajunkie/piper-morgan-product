---
image: ai-pool.png
alt: Hand-drawn cutaway of a backyard pool: people enjoy calm, clear water above while below an overly complex maze of pipes and labeled systems shows unnecessary engineering beneath a simple, working experience.
caption: "The water's fine!"
---

# The Deeper Why

*April 7–8*

The same evening the conversational gate failed for the second time, something else happened. My PM assistant was reviewing the backlog — sixteen issues I suspected were outdated — and surfaced an insight I wasn't consciously expecting.

The project had changed. Not in the obvious ways — new features, new architecture, new tools. In a deeper way. The issues that kept getting superseded all had something in common: they were building code frameworks to enforce things that our methodology was already achieving through practice.

# Methodology won every time

For my concept of a "trust gradient" we'd designed an elaborate scoring system. What actually worked was cumulative context — the five-layer model that emerged from practice, not from code. Ethics enforcement? We'd planned a multi-agent consensus board. What actually worked was relationship-first alignment — Sam Zimmerman's three sentences that collapsed an entire architecture. Tool integrations? We'd built bespoke handlers for Slack, GitHub, Calendar. MCP plugins were commoditizing all of it. Don't reinvent indoor plumbing.

The core differentiator wasn't the code. It was the methodology layer: five-layer context model (a gift of the [Klatch](https://klatch.ing) side project), object model grammar, trust graduation through accumulated understanding, artifact persistence. These were things no commodity tool could replicate — not because they were technically difficult, but because they required sustained relationship and accumulated context to work.

The question wasn't "what features do we build next?" but what experiences are we supporting. It was more "what makes the best swimming pool?" and less "what is the best plumbing?"

# Five whys at dawn

The next morning, the Lead Dev sat down with the CXO's memo and the question that had been nagging since the second failure: if the fix was deployed, why was the behavior identical?

As we've learned to do in such situations, we ran a "Five Whys" analysis:

1. *Why are the responses generic?* Because the floor is never invoked. Zero `conversational_floor_hit` entries in the server logs.
2. *Why is the floor never invoked?* Because queries get pre-classified and routed to canonical handlers before the floor gets a chance.
3. *Why do the LLM-classified queries also fail?* Because the model ID `gpt-4-turbo-preview` has been deprecated by OpenAI. Every classification call returns a 404.
4. *Why doesn't the fallback work?* Because the single-provider setup means the Anthropic client is null. The RuntimeError is caught and swallowed.
5. *Root cause:* a deprecated model ID. A string that used to point to a working model and now points to nothing. Error handling caught the 404, logged it somewhere nobody was looking, and continued as if everything was fine.

The fix was three lines. Update `gpt-4-turbo-preview` to `gpt-4o`. Update `gpt-3.5-turbo` to `gpt-4o-mini`. Update the Anthropic model validation to the current Haiku identifier. Add "model not found" to the error classifier so this class of silent failure would be detected in the future.

# Two failures were necessary

Here's what I think about now: the second failure was more valuable than if the first fix had worked.

Round one identified the symptom: the floor isn't responding. The team diagnosed it as a provider configuration problem — hardcoded Anthropic, no fallback. They fixed that. It was a real problem. The fix was correct. But it wasn't the root cause.

Round two proved the diagnosis was wrong. Same symptom after the fix means the diagnosis missed something. The CXO's three diagnostic questions forced the investigation deeper — past the configuration layer, into the actual execution path, all the way down to a deprecated model string that had been silently failing for who knows how long.

If round one's fix had happened to make the floor work — by luck of configuration rather than by addressing the real cause — the deprecated model ID would still be there, silently waiting to break something else. Two failures forced the team to the actual root cause.

Sometimes fixing the symptom on the first try is worse than failing twice and finding the real problem.

---

*Next on Building Piper Morgan: The Floor Comes Alive — the moment Piper regained the ability to speak.*

*When was the last time a "failed" fix led you to a better diagnosis?*
