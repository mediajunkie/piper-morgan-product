# The No-Anchoring Roundtable

<!-- image: 'ai-roundtable.png' -->
<!-- alt: 'Human and four glowing AI agents sit at a round table, each writing independently behind small dividers, unable to see each other’s answers.' -->
<!-- caption: '"No peeking!"' -->

*March 14*

I has this sudden instinct we'd been building the system backwards. I wanted to ask my agent team and get honest answers. This is not a small question. It's the kind of question where the first one to speak shapes how everyone else thinks about it.

I made sure nobody spoke first.

I sent the same question to four leadership roles — CXO, PPM, Architect, CIO — in parallel. Each one received the same context: a screenshot of Piper rejecting a reasonable PM query, the observation that a $0 ChatGPT wrapper would have handled it better, and the question: "Are we doing this backwards?"

No shared channel. No group thread. No way for any role to see what the others were writing. The CIO had actually recommended this approach in an earlier session — independent parallel responses to prevent anchoring bias.

# Four frames, one diagnosis

The responses came back. Each role found a different way to describe the same underlying problem.

The CXO described a bouncer at the door. The classifier was checking credentials and turning away anyone without the right ID. The eight contextual fallback messages we'd just shipped — carefully written, CXO-authored copy for when Piper couldn't help — were, in the CXO's own words, "a band-aid on exactly this wound."

The PPM diagnosed a layer inversion. Piper used the LLM to *classify* queries but not to *respond* to them. Tokens spent deciding the system couldn't help, then not using the LLM to actually help.

The Architect gave the most precise technical description: "We use the LLM to classify but not to respond." The routing architecture was structurally inverted — handlers were the default, the conversational floor was the last resort.

The CIO reframed the model entirely: "The LLM is the floor, not the ceiling." Every query should reach the LLM with full project context. Structured handlers should make the response *better*, not *different*.

Four independent analyses. Zero overlap in framing. Complete overlap in conclusion.

This is why I maintain ongoing agent roles and personas. Each holds a different lens and I need the perspectives to see the full picture.

# Why no-anchoring works

Anchoring bias is one of the best-documented effects in decision science. The first number in a negotiation shapes the outcome. The first opinion in a meeting shapes the consensus. The first framing shapes how everyone thinks about the problem.

In a traditional team meeting, the most senior person or the most confident speaker goes first. Everyone else adjusts — not because they're weak, but because they're human. Even devil's advocates anchor on what they're opposing.

The no-anchoring approach eliminates this entirely. Each respondent works from the raw evidence, not from someone else's interpretation of the evidence. When they converge, the convergence is signal, not groupthink.

When they *don't* converge, that's signal too — it means the problem is genuinely ambiguous and a simple vote or discussion would have produced false consensus.

This is directly drawn from my experience with teams of, you know, people. I never tell a team what I already think about something before asking for ideas. I don't want to start everyone out inside the box.

# The structural advantage

Multi-agent teams have a natural advantage here that human teams don't: agents can't peek. When I send a question to four separate Claude sessions, there's no hallway conversation, no Slack thread, no body language in a conference room. The isolation is complete by default.

Human teams can approximate this with written submissions before a meeting, or with anonymous polling. But the temptation to discuss before the formal response is always there. With agents, the protocol *is* the behavior. There's no gap between "we agreed to respond independently" and "we actually responded independently."

The cost is that agents can't build on each other's thinking in real time. Our synthesis step — the PPM collecting all four memos and producing a unified document — partially compensates. But the real-time riffing, the "yes, and..." dynamic of a good meeting, is lost.

For high-stakes diagnostic questions — "is our architecture wrong?" — the tradeoff favors independence. For creative brainstorming, it probably doesn't. The technique is a tool, not a universal method.

The PPM took the lead on synethesizing the four memos, then the Architect reviewed the synthesis, then CXO and CIO approved. This four-step convergence pattern (independent → synthesize → review → ratify) seemed to work pretty smoothly!

# When to use it

Not every question deserves a no-anchoring roundtable. Most decisions aren't high-stakes enough, and the overhead — four independent responses plus synthesis — is real.

But when you're asking a question where the wrong answer means months of wasted work, and where the natural social dynamics of your team might produce false consensus, it's worth the cost.

The signals that suggest no-anchoring:

The question is diagnostic, not creative. You're asking "what's wrong?" not "what should we build?" Diagnostic questions have a ground truth you're trying to find, not a possibility space you're trying to explore.

The stakes justify the overhead. If the answer is going to redirect a sprint, change an architecture, or kill a feature, four independent perspectives are cheaper than one wrong consensus.

You suspect anchoring is likely. If one person on the team has strong opinions and tends to speak first, or if the team has a recent experience that's likely to dominate their framing, isolation is protective.

With my agent team, it's hard not to dominate. I'm the source of all of the original ideas, after all, whatever that means. Plus, I have the final say. I can always put my thumb on the scale. The last thing I need to do is stifle other perspectives right off the bat. Speaking last gets me the most comprehensive feedback.

---

_Next on Building Piper Morgan: Archaeological Debugging — when "implementation already exists" turns a build day into a dig._

_When was the last time your team agreed too quickly? What would have happened if everyone had written their answer before anyone spoke?_
