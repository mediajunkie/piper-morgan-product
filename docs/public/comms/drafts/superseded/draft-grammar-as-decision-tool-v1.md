# Grammar as Decision Tool

*January 27*

[alt text: A grammatical sentence diagram with one branch highlighted as "category error"]
Caption: "The question answered itself"

"What would 'BLOCKED insight' mean?"

The Principal PM asked this question during a design discussion, and it ended a debate that had been going in circles. The answer was obvious once you heard the question: it wouldn't mean anything. The concept doesn't fit.

## The question

We were discussing whether Insights should have lifecycle states. Our domain models have a lifecycle system—NASCENT, DEVELOPING, ACTIVE, BLOCKED, STALLED, PAUSED, COMPLETE, ARCHIVED. It works well for todos, projects, and work items.

Someone suggested adding lifecycle states to Insights. It seemed reasonable. Insights are objects in our system. Other objects have lifecycle states. Why not Insights?

## The grammar test

Our MUX object model has a core grammar: "Entities experience Moments in Places."

The PPM applied the grammar as a test. Entities are actors with identity and agency. Moments are bounded significant occurrences. Places are contexts with atmosphere.

Where do Insights fit?

Insights aren't entities—they don't have agency. They don't experience anything. They're the *output* of entities experiencing moments in places. They're what emerges when Piper reflects on patterns across multiple interactions.

## The category error

Once you frame it that way, "BLOCKED insight" becomes obviously nonsensical. What would block an insight? Insights aren't trying to accomplish something. They don't have workflows. They don't get stuck.

The CXO reinforced the point: if users need to track something about insights, that's metadata about the user-insight relationship, not a lifecycle state. Did I read this insight? Did I act on it? Those are user properties, not insight properties.

The grammar revealed a category error. We were treating Insights as entities when they're actually artifacts—outputs of the composting process, not actors in it.

[PM PLACEHOLDER: Was this obvious to you in the moment, or did it click gradually?]

## The decision

We deferred adding lifecycle states to Insights. Not because we ran out of time, but because the concept doesn't apply. It would be like adding "habitat" to a mathematical theorem—the category doesn't accept that property.

If we later discover users want to track insight-related states, we'll design something appropriate to what insights actually are. But we won't force-fit a concept from a different category.

## The pattern

This experience formalized something I'd been doing intuitively: using the grammar as a decision filter.

When someone proposes a feature or asks about a design choice, run it through the grammar. Does this thing experience moments? Is it an entity, a moment, or a place? Does the proposed property make sense for that category?

If the answer is "it doesn't fit the grammar," that's usually a sign you're looking at the wrong category. Either the proposal needs to change, or the grammar needs to expand—and grammar expansions should be rare and deliberate.

## The meta-pattern

Every domain has an implicit grammar—the categories of things that exist and how they relate to each other.

Most teams don't make this grammar explicit. They accumulate features, and the categories emerge (or don't) from usage patterns. This works until it doesn't—until someone proposes a feature that doesn't fit anywhere, and the team argues in circles because they're not arguing about the same underlying model.

Making the grammar explicit gives you a shared tool for evaluation. "Does this fit our grammar?" is a question everyone can answer. It moves debates from taste ("I think insights should have states") to structure ("what category are insights, and what properties do that category accept?").

[PM PLACEHOLDER: Do you have other examples where the grammar test clarified a decision?]

---

*This is part of the Building Piper Morgan series, documenting what we're learning about AI-assisted development—including the frameworks that emerge from doing the work.*

*Have you ever had a design question resolve itself once you found the right framing? What was the question that unlocked it?*
