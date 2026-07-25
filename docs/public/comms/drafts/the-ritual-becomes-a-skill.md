---
image: 'the-ritual-becomes-a-skill-dance-floor.png'
alt: 'A dance instructor welcomes a new glowing, network-like partner onto a floor marked with choreography as another luminous dancer exits through the doorway.'
caption: '"You''ll get the hang of this in no time!"'
---

# The Ritual Becomes a Skill

*July 2026*

For nearly a year, I have been illustrating posts in this series with cartoons.

The process started simply. I would describe the topic and ask for help brainstorming a "vivid visual metaphor" to illustrate the post with a cartoon. I started pasting in the whole draft after a while. 

Sometimes I had a clear metaphor in mind already but more often I would ask ChatGPT to pitch me three or four ideas and then I'd pick one. 

At first the one-shot cartoons were hit or miss. Sometimes great, sometimes full of visual nonsense: floating limbs, escher-like physics. Back then it was really hard to improve the first draft. ChatGPT got anchored to its initial composition and would promise to iterate on it to fix it, then burn token producing exactly the same image or worse, and apologizing a lot.

We agreed on an approach where we'd discuss the idea first, align on an approach, and then the LLM would write a crisp thorough prompt for me to review. When I was satisfied I would write "OK, render it" and then hope for the best.

That phrase became a gate.

It prevented us from spending an image-generation attempt on an idea that was not ready. More importantly, it preserved the part of the process where the quality actually came from: the conversation before the drawing.

# It started as a gag

When I started this series, the Internet was awash with ChatGPT cartoons, most of them looking like the same generic style (or whatever current fad was ripping off an established style, like the Ghibli phase, etc.). I know that articles with illustrations get read more and I thought it would be funny to ask ChatGPT to make totally generic-looking cartoons for me.

Over time, this became a way of showing the baseline quality of such images growing over time. At some point, the imagery started getting too slick, looking more and more like computer-generated (ironic, I know) 3-D animation, not the "newspaper cartoon" aesthetic I had started with. So I started adjusting the general style prompt to resist this slickness an artificially hold things to a more hand drawn style.

A few months later, the image model improved dramatically, which created a new problem: it wanted to turn everything into a painterly, intricately detailed scene. I had to add more restrictions to keep the work closer to a newspaper cartoon and less like a Hieronymus Bosch canvas.

Around the same time, Paul Ford made a sly complaint about the flood of robot imagery used to illustrate AI. I took that as a fun challenge and useful constraint and began exploring other ways to depict a nonhuman, noncorporeal helpful intelligence.

By the time I realized this had become a repeatable practice, I was preparing to lose access to the ChatGPT account where it had evolved. It occurred to me that I wasn't sure how much of the process came from my current instructions and how much came from the account’s accumulated sense of how I work.

So I decided to try to extract the ritual.

# The problem with saving a collaboration

The tempting approach was to ask ChatGPT to summarize everything it knew about my preferences.

I do have preferences. I usually want a wide editorial cartoon. I prefer hand-drawn lines, restrained color, gentle humor, and fewer labels. As I mentioened, I have spent months pushing back against the image model's growing ability to produce polished, painterly scenes when what I want is closer to a newspaper cartoon.

The series also developed a visual vocabulary. Human collaborators tend to look ordinary and capable. AI agents are often translucent geometric beings or slightly strange nonhuman helpers rather than humanoid robots. The emotional register is usually curious rather than alarmist. The machines are not taking over. Humans and intelligent systems are learning how to work together.

All of that could be written down.

But preferences were not the most important thing to preserve.

The important thing was the sequence of decisions.

A new account would not remember the bridges, trains, gardeners, watchdogs, workshops, courtrooms, airports, and mountains we had already used. It would not have the same accumulated feel for which kind of image I would choose.

It might still be able to follow the ritual.

# What the ritual was actually doing

The first version sounded straightforward:

Read the article. Identify the underlying tension. Propose several visual metaphors. Pick one. Write a prompt. Render the image. Write alt text.

That was roughly correct, but too mechanical.

The real process had more elbows in it.

Sometimes I arrived with no idea and needed the metaphorical space opened up. Sometimes I already had the image and needed help stress-testing it. Sometimes the first metaphor family was right but the initial composition was wrong. Sometimes two possible images expressed different truths in the same essay, and the real choice was not between pictures but between editorial emphases.

Was the article about the temptation to stop early, or the future cost of stopping early?

Was documentation drift best shown as two tracks separating, or as a map no longer matching the rails?

Was the post about a system failing, or about a successful system exposing its next bottleneck?

The skill could not merely say, "Generate five ideas."

It had to determine what creative move was needed next.

# The examples became the evaluation set

We tested the emerging skill on a post about documentation drifting away from code.

The first pass found the conceptual center:

Two representations of the same promised behavior are subjected to different forces, separate silently, and reveal the gap only when someone crosses from planning into execution.

It proposed bridges, clocks, shadows, zippers, and railroads.

We chose a railroad.

Then we refined within that family. ChatG's first instinct   was a train following a map that no longer matched the track, which foregrounded prediction versus execution. 
We wrote the prompt.

I said, "Render it."

The image worked. I then showed the conversation the actual cartoon I had made earlier that day in a separate chat, using my standard process. It was a slightly better variation on the "two trains" seed: two trains beginning together and slowly diverging, with the divergence itself carrying the idea. We agreed this was actually better and ChatGPT refined the skill description a bit to capture why.

The next post I wrote, about losing an uncommitted draft after a server crash, I tested directly on it.

The metaphor was a tiny open window in an otherwise safe room. A gust of wind pulled a manuscript through it. The opening was small. The consequence was total.

The first rendering failed.

The room had a small window and an enormous open wall. Papers seemed to enter through one opening and leave through another. The physical logic was nonsense.

This was useful.

We had discovered an evaluation criterion that had been present in the collaboration but never stated:

The image must obey its own cartoon physics.

Tracks must lead somewhere. Bridges must connect. Paper must originate somewhere. A visual metaphor stops working when the viewer starts debugging the drawing.

We revised the composition. One normal window, left slightly open. A thick manuscript on the desk. A single top sheet caught by a rogue gust and moving toward the opening. No extra wall. No ribbon of paper that might turn the manuscript into a scroll.

The second rendering worked.

That failure was part of the skill-building process. Somewhere in that revision, I remarked that we were effectively running a manual evaluation loop.

# This is what an eval can look like

"Evals" can sound like specialized infrastructure: benchmark suites, scoring systems, held-out datasets, automated graders.

Those things exist, and they matter.

But the underlying idea is simpler.

You define what good performance looks like. You try the system on representative examples. You notice where it succeeds and where it fails. You revise the instructions or mechanism. Then you try again.

Our examples were blog posts.

Our outputs were cartoons.

Our criteria emerged through use:

## Editorial truth

* Does the image reveal the underlying relationship rather than merely depict the topic?
* Does the metaphor work without knowing the technical subject?
Are the actors competent when the problem is coordination?

## Comprehension

* Can the idea be understood at a glance?
* Is there one first thing to notice?
* Does the eye discover the idea in the intended order?

## Composition

* Does the image obey its own physical logic?
* Are the meaningful layers of agency preserved?
* Is richness competing with clarity?
* Did we render too soon?

This was an eval loop, even though nobody opened a spreadsheet.

The evaluations were qualitative, conversational, and grounded in actual use. They were also cumulative. Each failure added a rule. Each successful image gave us a case study.

# The pattern language underneath

As we reviewed older examples, the images began to sort themselves into recurring structures.

* Two trains leaving the same station and slowly separating expressed divergence.
* Four eager valets responding to one guest expressed convergence and collision: everyone locally correct, the system globally absurd.
* A single page blowing through a small open window expressed exposure.
* A court full of brilliant mechanical advisors waiting for one small ruler to decide expressed a bottleneck moving from execution to judgment.
* A quiet workbench holding its state while its owner rested outside expressed continuity through absence.
* A robot child being encouraged to finish a plate of wires and circuit boards expressed gated completion through a familiar social ritual.

These were not simply a collection of favorite metaphors.

They were becoming a visual grammar for invisible system dynamics.

The cartoons spatialized relationships: what connects, what drifts, what collides, what waits, what remains exposed, what supervises what, what looks complete but is not, where the constraint has moved.

This was the point where the work began to feel familiar to me in another way.

It was information architecture.

Not diagrams, exactly. More like editorial information architecture: abstract relationships made visible through physical places, social rituals, and objects behaving strangely.

# The first two seconds

One of the most useful rules emerged while comparing two railroad images.

A good image does not merely contain the metaphor. It controls how the metaphor is discovered.

In the stronger examples, the viewer's experience has a sequence.

First: two trains leave a station together.

Then: the tracks begin to bend apart.

Then: one train approaches mountains while the other approaches an industrial city.

Finally: the cargo reveals documentation on one track and machinery on the other.

The idea unfolds over perhaps two seconds.

That became part of the skill: What does the viewer see first? What relationship becomes apparent next? What delayed realization completes the joke or insight?

This is different from adding detail.

It is designing comprehension.

# Economy versus capability

The image model became dramatically more capable during the same year.

That was not always an uncomplicated benefit.

It became better at rendering light, materials, landscapes, machinery, architecture, and atmospheric depth. It could turn almost any prompt into a beautiful storybook scene.

But the goal was not to maximize beauty.

The goal was to communicate a visual idea before the reader began the article.

A recent cartoon about infrastructure becoming operational used a ship leaving the yard while parts of it were still being inspected and completed. The metaphor was right: the system was underway without being magically finished. The rendering was charming and conceptually strong, but it was also near the outer boundary of the intended style: detailed rigging, carefully modeled water, atmospheric landscape, many small mechanisms.

The next revision to the skill emphasized visual economy:

The viewer should grasp the central relationship before noticing craft, atmosphere, or secondary jokes.

This will probably require maintenance. Baseline model behavior drifts. A phrase that once reliably produced a loose editorial cartoon may later produce something richer and more polished. Skills are not permanent spells. They are operating instructions for systems that continue to change.

# What finally went into the skill

The resulting Piper Morgan Cartoon Ritual does not tell ChatGPT to generate a picture immediately.

It tells the model to infer the current stage of the collaboration.

If there is no concept, find the editorial center and propose a small number of developed metaphor families.

If I already have a concept, validate and sharpen it instead of restarting the brainstorm.

If a family has been selected, refine inside it.

If the concept is settled, write a composition-first prompt.

Then stop.

Wait for "render it."

The skill also carries the pattern language, the style anchor, the cartoon-physics checks, the preference for technical ideas translated into ordinary experience, and a growing collection of case studies.

It is opinionated because it is intended to preserve one particular collaboration.

I have also made a general-purpose version, [Editorial Hero Illustration](editorial-hero-illustration.zip), for other writers and teams to use. It preserves the collaborative method but removes the Piper Morgan style assumptions. You are welcome to try it!

# What the skill doesn't capture

It does not contain the accumulated memory of a year-long conversation.

It does not guarantee that a fresh ChatGPT account will make the same choices the old one would have made.

It does not eliminate taste, judgment, surprise, or disagreement.

That is probably good.

A process artifact should not freeze a collaboration in place. It should preserve enough structure that a new collaboration can begin somewhere further along.

The pattern language is a lens, not a cage.

The human and the agent can still propose something strange, fresh, hybrid, or emergent when the story asks for it. In fact, that possibility is part of the instructions. This whole approach pushes against the one-shot mentality that takes you as the human being out of the creative process. Instead of being an automated push-button process, the skill interacts with, protecting and maintaining the parts of the creative process that produce better work.

# The durable part

This project began because I was preparing to lose an account.

The obvious fear was losing memory: all the context, preferences, examples, and shared history that had built up over time.

But the exercise clarified something I have encountered repeatedly while building Piper Morgan.

Memory is not the only form of continuity.

Practices can be named.

Judgment can be partially externalized.

Examples can become evaluations.

Failures can become criteria.

A tacit collaboration can become a durable artifact. It will never be a perfect replacement what it's replacing, but it turns out that this is probably not necessary anyhow, and what it does provide is a starting point for the next iteration.

That skill preserves a ritual that has helped me surface the metaphor lurking in the prose.

---

*Next on Building Piper Morgan: "The Meta-Observation Pattern" — a week where three published pieces all described coordination while being part of coordination.*

*What repeated collaboration have you developed with an AI that still exists mostly as habit and mutual adjustment? What examples would you use to teach it to a fresh instance — and what failures would reveal whether the ritual survived?*
