---
image: ''
alt: ''
caption: ''
---

# We Built Onboarding in Our Own Image

*May 19–31, 2026*

My personal working preference for conversations is serial. One thing at a time. I've worked out over time that this keeps me from feeling overwhelmed by too much at once. 

While building an Claude plugin for a client I deconstructed some of the plugins Anthropic was releasing at the time and liked the idea of what they called a cold-start interview" skill, for gathering preferences and background about the user to inform later interactions with the remote API (via MCP, *M-O-U-S-E*). This is maps more or less to what product people call onboarding and or what UX folks call first-time user experience (or "ftux").

So I made one for Piper Morgan, an onboarding skill that helps a new user describe how they work so Piper Morgan can adapt to them before the first real session. This was all part of a "skunkworks" project on the side that I assigned to my product assistant *on* the Piper Morgan project, Piper Alpha (or PA for short). Piper drafted the skill and seamlessly incorporated *my* personal preference into its design: The interview would proceed conversationally, one turn at a time, one question at a time. The same deliberate cadence that makes ongoing collaboration feel careful and considered *for me*.

As usual, I was the first tester.

Boy did the experience drag! It stretched out. It was hard to follow. At several points I had no sense of where I was in the interview or how much was left, which made me anxious. If this were not my own software I might easily have bailed out of impatience partway through. What was intended as deliberate and careful, calibrated for an established ongoing dialogue, registered differently as a first impression. For a beginner the result is you don't know how long this will take, you can't see the shape of what you're in, and there's no map.

# Trust is earned in context

Ongoing use can earn trust by maintaining careful context, by not overwhelming, by letting each thing land. Those are real properties of the serial conversational mode.

Onboarding earns trust by orienting, by giving someone a sense of what they're getting into, how much is asked, what the shape of the thing is. Those are different goals. They don't necessarily benefit from the same interaction model, even for people whose preferences are similar to mine.

It's a natural mistake to reuse the mode that works for the familiar or dominant case into the entry point. You know what works, you're the prototypical user. Problem is you've got the whole mental model already in your brain's cache. You're not a good model of a first-time user. 

The whole exercise of planning the introduction to your experience requires examining those distinctions and figuring out what needs to be different. By nature this means you end up missing some things till you notice how they clash or fail to serve.

# What I don't know yet

I know the serial model felt wrong for this onboarding context. I'm still thinking about what might be the right model. (I've heard now of more than one AI product where the onboarding flow *reduced* activation.) Maybe batched questions that show the shape of what you're in, maybe progressive disclosure where you start shallow and wait for them to ask for more detail, maybe the sort of widget-y modular form interactions LLMs can conjure up these days, or something else entirely. You tell me!

---

*Next on Building Piper Morgan: "Patterns Naming Patterns" — the pattern catalog that names failure modes in the product had a failure mode of its own, and hadn't been reading itself.*

*What's your approach to onboarding new users into conversational or generative environments? I need more examples!*
