# Wiring vs. Wizardry

*March 12 to 13, 2026*

When an AI system underperforms, the instinct is to blame the AI.

The model isn't smart enough. The training data wasn't representative. The prompts need more engineering. The context window is too small. And sometimes — often, even — those explanations are correct. AI capability limits are real.

But sometimes the problem is plumbing.

---

We ran a test harness against sixty-one standard queries. First pass: 26% success rate. Three-quarters of our queries failing. After months of development, after thousands of passing tests, the system apparently couldn't handle basic requests.

The instinct was to examine the classifier. Was our intent detection model undertrained? Were the prompt templates malformed? Had we hit some fundamental limitation in the AI's ability to understand user requests?

None of the above.

The classifier was routing correctly. The handlers existed. But between classification and execution, cables were missing. An analysis handler that existed in the intent service but was never wired to the orchestration engine. Authentication threading that worked at one layer but never propagated to the next. Configuration checks that passed in isolation but failed when called from the actual request path.

Four hours of wiring fixes later: 81% success rate. Same classifier. Same model. Same prompts. The difference? We connected stuff.

---

"The 75% Pattern" is what we my agents call this (they love naming things after percentages!) Infrastructure built. Interface defined. Connection never completed. Tests don't catch it because mocks hide the gap. The capability exists in pieces; it just doesn't flow end-to-end.

It's an easy trap because each layer looks correct in isolation. The classifier routes to the right intent. The handler implements the right logic. The adapter calls the right service. Unit tests pass at every level. But nobody ran a request through the full stack until a human tried to use it.

---

This isn't unique to AI systems, but AI systems make it worse.

Traditional software fails loudly when connections are missing. Call a function that doesn't exist, get a compiler error. Reference an undefined method, get a runtime exception. The failure is immediate and obvious.

AI systems fail quietly. The classifier routes to a handler that exists but isn't wired, and the system... does something. Maybe it falls back to a generic response. Maybe it hallucinates an answer. Maybe it apologizes and asks for clarification. The user experiences degraded quality, not a crash. The logs show successful intent classification. Everything looks fine from the inside.

This is why AI debugging is hard. The system keeps working — just badly. You can spend weeks tuning prompts for a problem that has nothing to do with prompts.

---

The fix isn't complicated, but it requires discipline:

**Test the seams, not just the pieces.** Unit tests verify components. Integration tests verify connections. If you only have the former, you're testing that the Lego bricks are the right shape, not that they're actually snapped together.

**Run the full path early.** Don't wait for QA or alpha testing to discover that layer A doesn't actually talk to layer B. A single end-to-end test that touches the real stack is worth dozens of mocked unit tests for catching wiring bugs.

**When AI underperforms, check the plumbing first.** Before you retrain the model, before you redesign the prompts, before you expand the context window — trace a failing request through the full system. Is the intelligence actually being invoked? Or is it sitting there, ready and capable, waiting for someone to connect the cables?

The 81% was always possible. It just wasn't wired yet.

---

*Next on Building Piper Morgan, we resume the building narrative in our curent MVP sprint with "Are We Doing It Backwards?" when I asked a question and was scared what the answer might be.*

*Have you ever built something and forgot to wire it up? Is something you toiled over What looks like a capability problem in your system might actually be a connection problem. Before you upgrade the engine, check the fuel line.*
