# Entities Experience Moments in Places

*January 19*

[alt text: A sketch showing three interconnected concepts—Entities, Moments, and Places—with arrows indicating how entities move through moments within places]
Caption: "The grammar that shapes everything else."

After eight months of building an AI assistant, we finally wrote down what it actually thinks about.

Not the data model. Not the schema. The *grammar*—the fundamental sentence structure that describes how Piper Morgan understands the world.

It's seven words: **Entities experience Moments in Places.**

## Why grammar, not schema

A database schema tells you what fields exist. A data model tells you how tables relate. But neither tells you what the system *cares about*.

Grammar is different. Grammar describes how meaning gets constructed. Subject-verb-object isn't just syntax—it's a claim about how the world works: there are actors, there are actions, there are things acted upon.

Our grammar makes a similar claim:

**Entities** are actors with identity and agency. Not just data objects. Not just records in a database. Things that can perceive, remember, and anticipate.

**Experience** is the verb—perception plus memory plus anticipation. Not "have" or "contain" or "reference." Experience implies awareness, not storage.

**Moments** are bounded significant occurrences. Not timestamps. Not events. Moments have dramatic unities—a beginning, a middle, an end. They have weight. Some moments matter more than others.

**Places** are contexts with atmosphere. Not containers. Not folders. Places have character. A standup meeting feels different from a strategy session, even if they're both "meetings."

## What this changes

The grammar isn't just philosophy. It shapes implementation decisions.

**Without the grammar**, you might build:
- A task list (entities as rows, attributes as columns)
- An event log (moments as timestamps, places as tags)
- A folder structure (places as containers, entities as files)

**With the grammar**, you build differently:
- Entities that perceive their environment through lenses
- Moments that have dramatic structure, not just start/end times
- Places that carry atmosphere and influence how entities behave within them

The difference is subtle in code but significant in experience. A task list doesn't notice when you're overwhelmed. A system that understands "experience" might.

## The eight lenses

How do entities perceive their world? Through lenses—distinct ways of making sense of the same information.

| Lens | What it sees | Example question |
|------|--------------|------------------|
| Temporal | When things happen | "What's coming up?" |
| Hierarchy | How things nest | "What's this part of?" |
| Priority | What matters most | "What should I focus on?" |
| Collaborative | Who's involved | "Who's working on this?" |
| Flow | What state things are in | "What's blocked?" |
| Quantitative | Measurable aspects | "How many are done?" |
| Causal | What affects what | "Why did this happen?" |
| Contextual | Surrounding circumstances | "What's the situation?" |

The same project looks different through each lens. Through Temporal, it's a timeline. Through Hierarchy, it's a tree. Through Flow, it's a kanban board. Through Causal, it's a dependency graph.

An AI assistant that only has one lens gives one kind of answer. An assistant that can shift lenses gives the answer that matches how you're thinking.

## The implementation test

On January 19th, we turned this grammar into code. The test wasn't whether we could write the classes—of course we could. The test was whether the implementation preserved the philosophy.

Three questions guided verification:

**1. Can entities perceive, or do they just store?**

If an entity is just a data container, we've flattened the model. The implementation needs perception methods—ways for entities to sense their environment, not just hold data.

**2. Do moments have weight, or just timestamps?**

If moments are just events with start/end times, we've lost the dramatic structure. The implementation needs significance markers—ways to distinguish moments that matter from moments that don't.

**3. Do places have atmosphere, or are they just containers?**

If places are just folders or categories, we've lost context. The implementation needs atmosphere properties—characteristics that influence how entities behave within them.

These aren't tests you write in pytest. They're design reviews. Does the code preserve the grammar, or does it flatten the grammar into something simpler but less meaningful?

## The risk of flattening

Every implementation decision carries flattening risk. It's always easier to build a simpler model: entities as database rows, moments as timestamps, places as string tags, experience as CRUD operations.

The flattened version works. It passes tests. It ships faster.

But it doesn't *feel* different from every other PM tool. The grammar is what makes Piper Morgan distinct. Flatten the grammar and you have a sophisticated to-do list. Preserve the grammar and you have something that understands how work actually feels.

## Why it took eight months

We didn't write this grammar in month one. We discovered it gradually: months 1-2 were building features with no coherent model; months 3-4 were noticing patterns and starting to name things; months 5-6 brought "fat markers" sketching sessions and visual thinking; months 7-8 saw the grammar crystallize and implementation begin.

[PM PLACEHOLDER: The fat markers session—any memory of when this sentence first crystallized? Was there a specific sketch?]

The delay wasn't wasted time. We couldn't have written this grammar in January. We didn't know enough yet. The grammar emerged from building, not from planning.

This is the paradox of conceptual work: you need to build to understand, but you need to understand to build well. The grammar came late because it could only come late. Now that we have it, everything else builds on it.

## The sentence as compass

"Entities experience Moments in Places" is now our design compass. When we're unsure about a feature, we ask: does this fit the grammar?

- "Should we add a calendar view?" → Does it help entities perceive moments?
- "Should we add team collaboration?" → Does it enrich how entities experience places together?
- "Should we add analytics?" → Does it give entities new lenses for perception?

Features that fit the grammar belong. Features that require a different grammar probably don't.

It's not a rigid rule. Grammars evolve. But having an explicit grammar means we can notice when we're changing it, rather than drifting unconsciously.

[PM PLACEHOLDER: Should we include one of the actual sketches? The Perceptual Lenses diagram or the Entities/Moments/Places flowchart?]

---

*Next on Building Piper Morgan: The Calendar That Wasn't Mine, where alpha testing revealed that our multi-tenancy wasn't as complete as we thought.*

*Have you ever discovered that naming something changed how you built it? What grammar—explicit or implicit—shapes your work?*
