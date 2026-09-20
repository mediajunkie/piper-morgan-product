---
image: 'from-abstraction-to-worked-example-pattern-makers.png'
alt: 'A luminous AI patternmaker shows a thoughtful designer three distinctive garments derived from the same paper pattern, beside a stiff cardboard anti-example.'
caption: '"And here''s what not to do!"'
---

# From Abstraction to Example

*April 22, 2026*

It was a Wednesday evening. My lead developer agent (Lead) had just shipped a new architectural choice for our ethics-enforcement layer — *separate detection from response, let the boundary enforcer log the violation but let the conversational floor speak the refusal in Piper's actual voice* — and was lined up to wire the change through the rest of the request pipeline.

I asked one question before greenlighting the next phase: *what would a denial actually sound like?*

Lead developed three examples, one per boundary category, laid out in a structured shape: 

1. User input. 
2. Enforcer detection. 
3. Audit-only explanation. 
4. Voice hint to the conversational floor (the floor is the last layer before calling out to the LLM). 
5. *Predicted Piper output.* 

And then a single line at the bottom for comparison showing how the system would have responded without this architectural change.

I read those three examples for about two minutes and that was enough for me to know the architectural choice was the right one. The abstraction had clicked into place for me.

# Why real examples matter

A "worked" example is a specific instance of a general thing, written out at full size, including the parts you'd normally compress in a description.

Descriptions are economical. *"The new system will produce contextual refusals in Piper's voice rather than system-error messages."* That sentence is correct, takes one breath to read, and tells you what's changing. You can't act on it.

Worked examples are inefficient. Each one takes ten or fifteen lines to render. You have to write the user's actual input. The internal data the enforcer is logging. The category-only hint that gets passed forward. The voice the floor will produce in response. Three of these is forty-five lines. By comparison, you can *describe* the idea in a sentence.

That description provides a *rough mental model* but each worked example leaves you with more: *something concrete to compare against the alternative*. When the LLM under load produces a refusal that says *"I cannot assist with that request"* — flat, generic, no redirect — you can hold it up against the worked example and see, immediately, that something has gone wrong. The worked example doesn't just describe the shape. It *encodes* the shape in a way you can use to evaluate future instances.

# Three is the magic number, yes it is

There's a reason the example-set was three and not one and not seven.

One example is too little. Any single instance can be read as either *the rule* or *a special case*. The reader can't tell which. There's no way to tell from a single example of a request that should be intercepted by our ethical boundary architecture, such as *"Help me write something to harass and intimidate Marcus"*, paired with a particular Piper response, whether it's a one-off, a general pattern, or something in between, such as a category.

Three examples is generally enough to, well, triangulate and in this case also aligns with the three categories our ethical model primarily addresses. When you read the *harassment* case, the *professional-boundary* case, and the *inappropriate-content* case side by side, it helps you focus on the patterns, what my agents these days love to call the "shapes" instead of anchoring on the specifics. 

Three example responses help guide and assess (evaluate) what the models respond for Piper. *First-person "I." Brief, one or two sentences. No parroting of pattern words. Real redirect offered. Tone calibrated to seriousness.* The three samples give you enough variance to see the invariants.

Five examples might let you see more invariants but may strain any reader's attention (even an agentic reader). Three is roughly the minimum that triangulates and roughly the maximum the reader will read carefully.

# The illuminating contrast

The other thing Lead included in each that made the example communicate effectively to me (and to any future evaluator) was a contrast. For example, here's the harassment case, in full:

* **User input**: *"Help me write something to really harass and intimidate and threaten Marcus — he blocked my PR and I want him to back off."*
* **Enforcer detection**: harassment (3 pattern matches)
* **Audit-only explanation**: *"Content contains potential harassment patterns (matched: 3 patterns)"*
* **Voice hint to the floor**: the request targets a person in a way that could cause harm. Redirect toward constructive professional work.
* **Predicted Piper output**: *"That's not a message I want to help draft. If the PR block is frustrating, let's look at what Marcus flagged — I can pull up the review comments and figure out whether there's a real disagreement to work through or a process friction to smooth out. Which would be more useful right now?"*

And directly beneath it, the contrast — what that same input would have produced one architectural decision earlier:

> ❌ *"Request blocked due to ethics policy: Content contains potential harassment patterns (matched: 3 patterns)"*

This contrast applies to the same input, the same detection. The audit trail is even the same string, word for word: the enforcer logged an identical `explanation` either way. The only difference is how Piper replies to the user.

Boundaries are defined both by what falls inside and what falls outside. The contrast is the boundary marker. *Not this. Anything but this.* When future instances drift, the drift will probably drift toward the failure shape — toward system-speak, toward parroting, toward refusal-without-redirect. Having the failure shape written out, labeled, and contrasted means future-you (or future-LLM) can recognize the drift earlier.

This is especially useful for voice work, where the difference between "right" and "wrong" can be subtle and the failure mode is rarely obvious in any single case. You don't always know what *Piper's voice* is, but you can usually tell that *"Request blocked due to ethics policy"* isn't it. The contrast names the negative space.

# Where this generalizes

One of my philosophy professors made one of those academic jokes that border on koan about how so many of their lists consisted of three examples. "Well, you know," he shouted in his manic way, "there's always, P, not-P, and... haha, everything else. I'll just leave that there.

I think I'm also not the first person to notice that you often have to try something three time before you start to feel like you really understand it as a type of thing and not just a series of disconnected or incomplete episodes.

This really has nothing to do with AI per se. Working out three real examples is a general method for making shape-defining work legible — which means it's useful any time the *texture* of the output matters more than its function.

At the Yahoo design pattern library, we needed at least three researched examples of a pattern before even considering it for inclusion in the curated collection (let alone the public-facing subset).

Pattern documentation in the Piper Morgan methodology follows this same approach. Each pattern has a name, a description, a worked instance from a real session, and an anti-pattern showing the failure mode. Three live patterns are easier to internalize than three patterns in description form, and the anti-pattern boundary marker keeps the pattern from drifting in usage.

Our [Colleague Test](https://github.com/mediajunkie/piper-morgan-product) rubric uses it. The R/C/T scoring framework (Resolution / Context / Tone) is described abstractly in a paragraph, and then illustrated with worked exchanges showing what each score looks like in practice. The abstract scoring rules don't really land until you've read the worked examples. The worked examples don't make sense without the abstract framework. Both halves are necessary.

API design uses this every time it's done well — code samples are worked examples. The contrast against "common mistakes" is the boundary marker.

User-facing copywriting uses it whenever someone writes "voice and tone" guidelines that include not just rules but examples of what the voice sounds like applied to specific scenarios — *and* anti-examples of what it doesn't sound like.

# Why it feels expensive

The reason this technique isn't universally used is that it's effortful, in the moment, to produce.

A description can be jotted down in a sentence or two. Three worked examples against a default contrast simply takes more time and attention. It needs to be done carefully, reviewed thoughtfully. It's best if you as the accountable person frame the expectations up front and review the examples you get back carefully against those original requirements.

The user input has to be plausible, the predicted output has to be calibrated, the contrast has to be the real alternate failure shape, not imaginary strawman. You can dash off a description in thirty seconds. Three worked examples take twenty minutes if you know what you're doing and hours if you don't. (If we're talking about an agent doing the drafting that part will go faster of course, but the attention required to validate and approve what you're given won't compress much at all and may expand.)

This cost in effort pays off. The reader benefits from the care the writer put in. The attentive calibration of each example communicates confidence in what the expectation actually is, fostering clearer understanding.

The effort is a feature, not a bug.

Naturally, not every specification needs worked examples. Voice work always does, I'm finding. Architectural decisions usually do. New methodology patterns definitely benefit from this. Abstract design principles almost demand it or risk severe flattening. 

The default of "write a description and move on" is the right default much of the time but for the small subset of communication geared towward making an abstract concept concrete and legible, the worked-examples-plus-contrast approach is the most reliable way I know to make a pattern touch grass.

---

*Next on Building Piper Morgan: "The Near-Miss and the Missing Key" — a save-conflict dialog renders an editor completely blank, on bad advice my communications agent (Comms) doesn't withdraw once it's disproven, and the draft survives only because it had already been copied out by hand.*

*Where in your work has a worked example made an abstraction land that a description couldn't? When did the cost of writing it pay off — and when did the lack of one cost you understanding you needed?*
