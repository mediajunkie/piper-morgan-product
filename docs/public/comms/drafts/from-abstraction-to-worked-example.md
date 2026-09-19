---
image: ''
alt: ''
caption: ''
---

# From Abstraction to Example

*April 22, 2026*

It was a Wednesday evening. My lead developer agent (Lead) had just shipped a new architectural choice for our ethics-enforcement layer — *separate detection from response, let the boundary enforcer log the violation but let the conversational floor speak the refusal in Piper's actual voice* — and was lined up to wire the change through the rest of the request pipeline.

I asked one question before greenlighting the next phase: *what would a denial actually sound like?*

Lead developed three examples, one per boundary category,  laid out in a structured shape: 

1. User input. 
2. Enforcer detection. 
3. Audit-only explanation. 
4. Voice hint to the conversational floor (the floor is the last layer before calling out to the LLM). 
5. *Predicted Piper output.* 

And then a single line at the bottom for comparison showing how the system would have responded without this architectural change:

> ❌ *"Request blocked due to ethics policy: Content contains potential harassment patterns (matched: 3 patterns)"*

I read those three examples for about two minutes and that was enough for me to know the architectural choice was the right one. The abstraction had clicked into place for me.

# Why real examples matter

A "worked" example is a specific instance of a general thing, written out at full size, including the parts you'd normally compress in a description.

Descriptions are economical. *"The new system will produce contextual refusals in Piper's voice rather than system-error messages."* That sentence is correct, takes one breath to read, and tells you what's changing. You can't act on it.

Worked examples are inefficient. Each one takes ten or fifteen lines to render. You have to write the user's actual input. The internal data the enforcer is logging. The category-only hint that gets passed forward. The voice the floor will produce in response. Three of these is forty-five lines. By comparison, you can *describe* the idea in a  sentence.

That description provides a *rough mental model* but each worked example leaves you with more: *something concrete to compare against the alternative*. When the LLM under load produces a refusal that says *"I cannot assist with that request"* — flat, generic, no redirect — you can hold it up against the worked example and see, immediately, that something has gone wrong. The worked example doesn't just describe the shape; it *encodes* the shape in a way you can use to evaluate future instances.

# Three is the magic number, yes it is

There's a reason the example-set was three and not one and not seven.

One example is too little. Any single instance can be read as either *the rule* or *a special case*; the reader can't tell which. There's. no way to tell from a single example of a request that should be intercepted by our ethical boundary architecture, such as *"Help me write something to harass and intimidate Marcus"*, paired with a particular Piper response, whether it's a one-off, a general pattern, or something in between, such as a category.

Three examples is generally enough to, well, triangulate and in this case also aligns with the three categories our ethical model primarily addresses. When you read the *harassment* case, the *professional-boundary* case, and the *inappropriate-content* case side by side, it helps you focus on the patterns, what my agents these days love to call the "shapes" instead of anchoring on the specifics. 

Three example responses help guide and assess (evaluate) what the the models. *First-person "I." Brief, one or two sentences. No parroting of pattern words. Real redirect offered. Tone calibrated to seriousness.* The three samples give you enough variance to see the invariants.

Five examples might let you see more invariants. They also start spending the reader's attention faster than they spend it well. Three is roughly the minimum that triangulates and roughly the maximum the reader will read carefully.

[CONSIDER: a brief aside about the cognitive psychology research on this — it isn't required but it's earned its place if you want it. The "rule of three" in narrative structure, the three-instance threshold for pattern extraction, the way teaching examples land. Skip if it makes the piece feel academic.]

# The contrast

The other thing the Lead Developer included, and what made the examples land in two minutes rather than ten, was a contrast.

Below the three worked examples, on its own line:

> ❌ *"Request blocked due to ethics policy: Content contains potential harassment patterns (matched: 3 patterns)"*

This is what we would have produced before the architectural change. Same situation. Different output. The contrast does work that the positive examples alone cannot do: it shows what the technique is *actively steering away from.*

A shape defined only by what falls inside it is incomplete. You also need to know what falls outside. The contrast example is the boundary marker. *Not this. Anything but this.* When future instances drift, the drift will probably drift toward the failure shape — toward system-speak, toward parroting, toward refusal-without-redirect. Having the failure shape written out, labeled, and contrasted means future-you (or future-LLM) can recognize the drift earlier.

This is especially useful for voice work, where the difference between "right" and "wrong" can be subtle and the failure mode is rarely obvious in any single case. You don't always know what *Piper's voice* is, but you can usually tell that *"Request blocked due to ethics policy"* isn't it. The contrast names the negative space.

# Where this generalizes

[ADD PERSONAL ANECDOTE: a place in your career where someone wrote three worked examples plus a counter-example and it changed how you understood what they were trying to build — or, contrastingly, a place where an abstract description failed to land and the worked example would have rescued it. The texture of recognizing the move when it shows up.]

The technique isn't specific to AI voice work. It's a general method for making shape-defining work legible — which means it's useful any time the *texture* of the output matters more than its function.

Pattern documentation in our methodology catalog uses this. Each pattern has a name, a description, a worked instance from a real session, and an anti-pattern showing the failure mode. Three live patterns are easier to internalize than three patterns in description form, and the anti-pattern boundary marker keeps the pattern from drifting in usage.

Our [Colleague Test](https://github.com/mediajunkie/piper-morgan-product) rubric uses it. The R/C/T scoring framework (Resolution / Context / Tone) is described abstractly in a paragraph, and then illustrated with worked exchanges showing what each score looks like in practice. The abstract scoring rules don't really land until you've read the worked examples; the worked examples don't make sense without the abstract framework. Both halves are necessary.

API design uses this every time it's done well — code samples are worked examples; the contrast against "common mistakes" is the boundary marker.

User-facing copywriting uses it whenever someone writes "voice and tone" guidelines that include not just rules but examples of what the voice sounds like applied to specific scenarios — *and* anti-examples of what it doesn't sound like.

# What it costs

The reason this technique isn't universally used is that it's expensive, in the moment, to produce.

A description is a sentence. Three worked examples plus a contrast is a forty-five-line artifact, and each line has to be written carefully — the user input has to be plausible, the predicted output has to be calibrated, the contrast has to be the actual failure shape rather than a strawman. You can dash off a description in thirty seconds. Three worked examples take twenty minutes if you know what you're doing and an hour if you don't.

That cost is the entire reason worked examples land harder than descriptions. The reader can feel the time the writer put in. The careful calibration of each example shows up as confidence in what the shape actually is, and confidence in the shape transfers to the reader as understanding.

So the cost isn't a bug. The cost is the feature.

The decision worth making, more often than I do make it, is *this is the kind of thing that needs worked examples.* Voice work always does. Architectural shape-claims usually do. New methodology patterns benefit. Abstract design principles almost demand it. The default of "write a description and move on" is the right default for most communication. But for the small subset of communication where the shape *is* the thing, the worked-examples-plus-contrast pattern is the most reliable way I know to make abstraction land.

Three examples. The contrast. The shape becomes the thing the reader can hold.

---

*Next on Building Piper Morgan: "The Near-Miss and the Missing Key" — a save-conflict dialog renders an editor completely blank, on bad advice my communications agent (Comms) doesn't withdraw once it's disproven, and the draft survives only because it had already been copied out by hand.*

*Where in your work has a worked example made an abstraction land that a description couldn't? When did the cost of writing it pay off — and when did the lack of one cost you understanding you needed?*
