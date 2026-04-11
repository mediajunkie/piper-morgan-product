# The Cathedral Release

*January 25-27*

[alt text: A cathedral blueprint transforming into a building with lights coming on in windows]
Caption: "Document the cathedral, then decide which rooms to build"

"Go deep and thorough on modeling FIRST, to prevent future flattening. Only THEN discuss MVP scope. Document the cathedral, then decide which rooms to build first."

That was the guidance I gave on January 25th. Three days later, we released v0.8.5 and unblocked three alpha testers who had been waiting for weeks.

## The philosophy

We were about to implement MUX-IMPLEMENT P1 through P4—navigation, documentation access, lifecycle indicators, and accessibility polish. The temptation was to dive straight into code.

But we'd been burned before. Features implemented without thorough modeling tend to flatten over time. Edge cases get papered over. The underlying concepts drift. Six months later, you're maintaining code that no longer reflects what you actually believe about the domain.

So I asked the Lead Developer to start with a deep investigation instead. Not just "what do we need to build?" but "what does our object model actually say, and how does this feature express it?"

[PM PLACEHOLDER: What prompted this approach? Was there a specific past mistake you were thinking of?]

## The base camps

The investigation took a full morning. The Lead Developer visited ten "base camps"—documents that contained pieces of our MUX philosophy:

ADR-045 for the Five Pillars of Consciousness. The UX Foundations document for the Radar O'Reilly pattern (Piper isn't a destination, she's a companion). The anti-flattening guide for the difference between "Piper noticed" and "Query returned." The ownership metaphors for the Native/Federated/Synthetic distinction.

By the end, something had shifted. The navigation work wasn't just "add some menus." It was "express Piper's current awareness through lenses, gated by trust."

## The synthesis

We had a design discussion that covered five key questions.

What should the home state be? A "workspace" showing harder and softer objects, adaptive to what the user is working on, gated by trust level.

How do lenses manifest? As tokenized natural language—"stuck" and "urgent" as tappable concepts, named but conversational.

Is the standup a paradigm? Yes—a one-shot entry point that flows into conversation, following the pattern of chat to artifact to hardening.

Are places portals? "Brilliant," I said when the Lead Developer suggested it. "Windows, not links." Each place type has its own atmosphere.

What about existing navigation? It becomes a utility layer with a command palette for power users who know what they want.

[PM PLACEHOLDER: Which of these five felt most important or surprising?]

## The sprint

With the cathedral documented, we could decide which rooms to build.

P1 took one afternoon: home state, utility navigation, command palette, and place windows. 185 tests.

P2 took one evening: document access, lifecycle indicators, composting views. 302 tests.

P3 took another evening: conversation memory, channel consistency, follow-up detection. 407 tests.

P4 took the final push: WCAG 2.1 AA accessibility compliance, design token enforcement, contrast testing. 638 template validations.

All told: 10 days from starting the MUX track to releasing v0.8.5. Over 1,000 tests added. Every P1-P4 issue closed.

## The release

v0.8.5 went out on January 27th. The release notes listed lifecycle indicators on todos, projects, and work items. New views for work items and project details. Full accessibility compliance. Design token system enforced across 27 templates.

But those features weren't the point. The point was that three alpha testers—Jake, Rebecca, and Dominique—had been waiting on bug fixes that blocked their onboarding. Those fixes were included too, and now they could proceed.

[PM PLACEHOLDER: How did it feel to finally unblock the alpha testers?]

## The pattern

I've started calling this "cathedral first"—document the full vision before deciding what to build now.

It's slower at the start. That morning of base camp visits didn't produce any code. The design discussion didn't ship anything.

But it meant the code we did write was grounded. Every feature traced back to a principle. Every UI decision connected to a concept. When questions came up during implementation, we had answers that weren't ad-hoc.

The alternative—start building and figure out the philosophy along the way—feels faster but isn't. You build, then discover an inconsistency, then patch it, then discover another inconsistency somewhere else. The flattening accumulates until the codebase and the concepts no longer match.

## The meta-lesson

There's a reason cathedrals have blueprints.

Not because the architects don't trust the builders. Not because spontaneity is bad. But because a cathedral is too complex to hold in your head, and too expensive to rebuild if you get it wrong.

The MUX object model is our blueprint. It says entities experience moments in places. It says awareness, not data. It says atmosphere, not contents.

When we document the cathedral first, we're not slowing ourselves down. We're making sure the rooms we build fit the structure we're building inside.

---

*Next on Building Piper Morgan: [PM PLACEHOLDER: next article in sequence]*

*Have you ever taken time to document the vision before building? Did it change what you built?*
