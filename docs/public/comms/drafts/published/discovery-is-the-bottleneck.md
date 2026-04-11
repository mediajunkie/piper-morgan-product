# Discovery Is the Bottleneck

*December 28, 2025*

We'd spent a week implementing canonical queries. Eight queries in Phase A. Eight more in Phase B. Coverage climbed from 5% to 31% to 47%. Tests passed. Handlers worked. The infrastructure was solid.

Then the Lead Developer reviewed the roadmap and wrote a single line that reframed everything:

> "19 canonical queries work but users can't discover them."

Nineteen queries. Working. Tested. Deployed. And users couldn't find them.

The missing link? Something I think of as "conversational glue": the ability to converse and extracting meaning. Greet, make small talk, and pick up on requests all in the same flow.

## The implementation trap

It's easy to measure implementation. Issues closed, tests written, coverage percentages. These numbers go up. Progress feels real.

But implementation isn't the same as usefulness. A feature that works but can't be found might as well not exist.

We'd fallen into the implementation trap. Every day brought more capability without improving the user experience, just increasing the confusion about what Piper could actually do.

## What discovery means

Discovery isn't documentation. Users don't read docs before asking questions. They ask questions and expect the system to understand.

Discovery isn't a help command. "What can you do?" returns a list. Lists don't teach. They overwhelm.

Discovery is conversational glue—the ability for natural dialogue to reveal capabilities at the moment they're relevant. A user says "I'm overwhelmed with tasks" and the system responds in a way that naturally surfaces "I can show you what needs attention" or "Want me to prioritize your todos?"

The 19 working queries were islands. Each one accessible if you knew exactly what to ask. No bridges between them. No paths from confusion to clarity.

## The pivot

This realization changed the roadmap. More query handlers wouldn't help. We needed:

1. **Conversational bridges**: Responses that naturally introduce related capabilities
2. **Context-aware suggestions**: Recognizing user states that indicate unmet needs
3. **Graceful discovery**: Revealing functionality through dialogue, not menus

The technical work wasn't wasted. Those 19 queries were still foundation. But the next phase wasn't Phase C of canonical queries—it was Epic #488, the discovery-oriented architecture.

This wasn't the first time we had discovered a missing layer in our foundation. When this happens I always stop building until I trust the architecture again.

## The universal lesson

Every product team faces this eventually. You build features. You ship features. Usage doesn't match expectations.

The instinct is to build more features. Add capability. Expand scope.

Sometimes the answer is: stop building and start revealing. The capabilities exist. The paths to them don't.

This is harder than implementation. Implementation has clear completion criteria. Discovery is fuzzier. How do you know when users can find what they need?

You know when they stop asking "what can you do?" and start asking specific questions.

---

*Next on Building Piper Morgan: "Wiring vs Wizardry" when the gap isn't cutting-edge tech, but just connecting the existing dots.*

*Have you ever discovered that your users couldn't find the features you'd already built?*
