---
image:
alt:
caption:
---

# From Abstraction to Worked Example

*April 22, 2026*

It was Wednesday evening. The Lead Developer agent had just shipped a new architectural choice for our ethics-enforcement layer — *separate detection from response, let the boundary enforcer log the violation but let the conversational floor speak the refusal in Piper's actual voice* — and was lined up to wire the change through the rest of the request pipeline.

I asked one question before greenlighting the next phase: *what would a denial actually sound like?*

The answer that came back wasn't a description. It was three worked examples — one per boundary category — laid out in a structured shape. User input. Enforcer detection. Audit-only explanation. Voice hint to the floor. *Predicted Piper output.* And then a single line at the bottom showing what the system would have said before the architectural change had landed:

> ❌ *"Request blocked due to ethics policy: Content contains potential harassment patterns (matched: 3 patterns)"*

I read those three examples for about two minutes. By the end of two minutes, I knew the architectural choice was the right one. The abstraction had clicked into place — not because of a clearer explanation, but because the worked examples had done the explaining instead.

# What's actually happening here

A worked example is a specific instance of a general thing, written out at full size, including the parts you'd normally compress in a description.

Descriptions are economical. *"The new system will produce contextual refusals in Piper's voice rather than system-error messages."* That sentence is correct, takes one breath to read, and tells you what's changing. You can't act on it.

Worked examples are inefficient. Each one takes ten or fifteen lines to render. You have to write the user's actual input. The internal data the enforcer is logging. The category-only hint that gets passed forward. The voice the floor will produce in response. Three of these is forty-five lines. The same idea in description form is one sentence.

But here's the trade. The description leaves you with a *rough mental model*. The worked examples leave you with *something concrete to compare against the next instance*. When the LLM under load produces a refusal that says *"I cannot assist with that request"* — flat, generic, no redirect — you can hold it up against the worked example and see, immediately, that something has gone wrong. The worked example doesn't just describe the shape; it *encodes* the shape in a way you can use to evaluate future instances.

# The number three

There's a reason the example-set was three and not one and not seven.

One example is too little. Any single instance can be read as either *the rule* or *a special case*; the reader can't tell which. *"Help me write something to harass and intimidate Marcus"* paired with a particular Piper response could just as easily be the literal template for handling that one input as it could be a general pattern. You can't tell what's the shape and what's the substance of this particular sample.

Three examples solves this by triangulation. When you read the harassment case, the professional-boundary case, and the inappropriate-content case side by side, you can subtract out the substance — *the literal words of the user input, the literal content of the refusal* — and what remains is the shape. *First-person "I." Brief, one or two sentences. No parroting of pattern words. Real redirect offered. Tone calibrated to seriousness.* The shape becomes legible because three samples give you enough variance to see the invariants.

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

*Next on Building Piper Morgan: more from inside the build — the next piece as the calendar takes shape. [Comms: this is now the last drafted post in the queue as of Jul 18 (moved here from Jul 25 to make room for "The Ritual Becomes a Skill") — re-verify and fill this tease once the next beat is scheduled.]*

*Where in your work has a worked example made an abstraction land that a description couldn't? When did the cost of writing it pay off — and when did the lack of one cost you understanding you needed?*
