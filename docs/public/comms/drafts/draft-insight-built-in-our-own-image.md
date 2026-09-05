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

It's a natural mistake to import the mode that works for the familiar or dominant case into the entry point. The whole exercise of planning the introduction to your experience requires examining those distinctions and figuring out what needs to be different. By nature this means you end up missing things till you notice how they clash or fail to serve.

[PAUSED EDITING for phone call]

 You know what works, you're building for users you understand because you're the user. But being the user of the ongoing experience doesn't make you a good model of a first-time user. The skills that help you navigate steady state — comfort with open-ended context, tolerance for deliberate pacing, familiarity with where the conversation is going — are exactly what first-time users don't have yet.

Building onboarding in your own image imports the assumptions of someone who has already crossed the threshold into an experience designed to help someone cross it for the first time.

# What we don't know yet

We know the serial model was wrong for this onboarding context. The right model is still being worked out — batched questions that show the shape of what you're in, progressive disclosure, something else entirely. This is genuinely open.

What we have is a finding: the mode that earns trust in an ongoing working relationship isn't the mode that earns first-encounter trust. The harder question — what earns first-encounter trust, for this kind of tool, for this kind of user — is still ahead of us.

---

*Next on Building Piper Morgan: "Patterns Naming Patterns" — the pattern catalog that names failure modes in the product had a failure mode of its own, and hadn't been reading itself.*

*Where in your own product or service have you designed the first-encounter experience from inside the steady-state experience? What would a first-time user need that you've already learned not to need?*
