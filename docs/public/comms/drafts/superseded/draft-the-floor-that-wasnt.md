# The Floor That Wasn't

*March 26, 2026*

[alt text: PLACEHOLDER — cartoon TBD]

*March 15–16*

Saturday afternoon. The floor was working. The Lead Developer had built the conversational floor the evening before — the LLM fallback that was supposed to catch every query the handlers couldn't answer. Twenty-three tests passing. I'd seen the screenshot. It worked.

So I tested it.

I typed seven messages into Piper. The kind of thing a normal user would say. "What should I focus on today?" "Tell me about AI agents." Simple, conversational, the exact queries the floor was built to handle.

Six of the seven came back as template boilerplate. Canned responses. Not the LLM engaging thoughtfully with my question — just the same pre-written handler output I'd been staring at for weeks.

The floor worked. Users just never reached it.

[ADD PERSONAL DETAIL: What did it feel like to test this? Was there a sinking moment, or more of a "here we go again" resignation? What specifically did the boilerplate responses look like?]

## The routing was inverted

I told the Lead Developer: "Invert. Investigate the architecture and docbase, write a report."

The report came back and confirmed what the test results implied. The routing architecture was backwards from the design intent. Our own design documents — PDR-002, ADR-039 — described a system where the conversational floor was the default and structured handlers were enhancements. What we'd actually built was the opposite: canonical handlers were the default path, and the floor was a last resort that almost nothing reached.

Every query hit a handler first. Most handlers had something to say — even if what they had to say was a template response that didn't actually engage with the question. The floor existed, it worked, it was tested, and it was unreachable.

Three stubs were literally labeled "implementation pending" — and they were catching real user queries and returning nothing useful instead of letting the floor handle them. The Lead Developer replaced all three with floor routing, removed a wrong todo fallback, and cleaned up a stale debug print. Small fixes, but each one had been silently eating queries.

## Phase 1

The first fix was scoped and shipped the same day. GUIDANCE intents — the broad category covering "help me think about this" queries — now route to the conversational floor with assembled context. A new context assembler gathers calendar events, projects, and priorities as structured facts and passes them to the LLM. Nineteen new tests. Merged to main.

I tested again. "What should I focus on today?" This time it hit the PRIORITY handler — a different category entirely, not GUIDANCE. The routing was more tangled than one category could fix.

The query that did reach the floor — a question about AI agents — came back with Piper parroting its own system prompt. Instead of engaging with my question, the LLM read its own instructions aloud. "I'm here to help you with product management tasks..."

[CHRISTIAN TO POLISH: Is there a good way to describe the absurdity of this? The LLM literally introduced itself instead of answering the question.]

The Lead Developer diagnosed both issues. PRIORITY was a separate classification category — Phase 1 only covered GUIDANCE. And the floor prompt was written in descriptive mode ("I'm a PM assistant that helps with...") instead of directive mode ("Respond directly to what the user said"). The LLM did exactly what descriptive prompts tell it to do: describe itself.

The prompt was rewritten. The parroting stopped.

## "Floor works" ≠ "users experience the floor"

This is the pattern that kept repeating. Mechanical correctness doesn't guarantee user experience. The floor passed every test. The routing worked as coded. The handlers returned responses. Everything was green.

And a real person typing a real question got template boilerplate six times out of seven.

[ADD REFLECTION: This connects to Pattern-045 (Green Tests, Red User) — passing tests don't guarantee real-user experience quality. Is there a personal way to express this frustration? A moment where the gap between "tests pass" and "this actually works for humans" felt especially acute?]

## Monday: the contract gap

Monday brought more testing and a deeper diagnosis. The leadership team converged again — Architect, PPM, CXO — this time on the structural relationship between classification and handling.

The Architect refined the core question: "Does this intent require an operation the LLM cannot perform?" If no — if it's a conversational question, not an action — the floor should handle it. Handlers are for side effects: creating todos, closing issues, checking calendars. The Action Gate criterion was born.

The CXO added a voice rule: "Never say 'I can't.'" If Piper can't perform the specific action requested, it should still engage conversationally with the topic. The floor makes this possible — there's always a response, always an engagement.

The PPM synthesized: the classifier's accuracy matters for *actions*, not for *conversations*. If a query gets misclassified but both categories route to the floor with context, the user doesn't notice. Classifier accuracy only matters when the wrong classification would trigger the wrong side effect.

[CHRISTIAN TO POLISH: The leadership convergence here was fast — did it feel like the team was building on Saturday's roundtable momentum, or was this a separate "aha" moment?]

The Lead Developer ran a Five Whys analysis that afternoon, exposing a systemic contract gap between the classification layer and the handling layer. The classifier was making fine-grained distinctions, but the handlers on the receiving end didn't honor those distinctions — they returned generic responses regardless of the classified intent. Precision in, mush out.

Nine issues closed by end of day. The architecture was starting to face the right direction.

## The lesson

Two days of testing. Two days of discovering that a system that "worked" — by every automated measure — didn't work at all for the person it was built for.

The floor existed. The tests passed. The routing was mechanically correct. But the architecture was inverted from the design intent, the prompts were written in the wrong mode, the handlers were swallowing queries they should have forwarded, and the contract between classifier and handler was broken.

None of this was visible from the test suite. All of it was visible within thirty seconds of typing a question.

[ADD PERSONAL REFLECTION: What did these two days teach you about the gap between building and testing? Is there something about the PM-as-tester role that automated testing can never replace?]

---

_Next on Building Piper Morgan: [TITLE TBD for Act 4] — the infrastructure week that made everything after it possible._

_[QUESTION PLACEHOLDER: When has "it works" not meant what you thought it meant? What did it take to see the gap?]_
