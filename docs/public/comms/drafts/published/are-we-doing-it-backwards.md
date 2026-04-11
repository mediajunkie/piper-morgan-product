# Are We Doing It Backwards?

*March 24, 2026*

[alt text: People struggle to reach an AI on the ceiling amid tangled machinery, while others stand easily on a glowing AI “floor” in a calm, open space nearby.]

*March 14*

Saturday morning. The day after ten roles had hummed in concert. I was feeling good about the project. M1 was moving. Issues were closing. The Lead Developer had knocked out twenty issues in twenty-four hours.

So I did what I always do when things are going well. I did a little testing.

I asked one of our canonical queries, something I wasn't sure if Piper could do yet, but which I expected a good answer for, either way, after building the "conversational glue" layer.

Piper kinda rejected me. Not in a rude way. It was something like "I don't have that capability yet" and nothing else. It was a reasonable request and I got nothing of value back.

I though about how most generic LLMs could handle any random product management request, at least in a mediocre way, or could explain why they couldn't help. None of this robotic (if polite) "does not computer" blank stare, or "Sorry, I can't do that, Dave."

That's when I started wondering, are we doing this backwards? Why is it so hard? I've been working on this for months, carefully crafting workflows, and Piper can't do the basic things a weekend-vibe-coded ChatGPT wrapper could do.

This couldn't be the best way to do it.

## Four diagnoses, zero anchoring

I could have told my team what I thought and watched them converge on whatever framing I offered up front. Instead, I took the CIO's advice from an earlier roundtable: independent parallel responses. No anchoring. Give each role the same question, let them think alone, compare the answers after.

I sent my question to four leadership roles: CXO, PPM, Architect, CIO.

Each one found a different way to describe the same problem.

The CXO saw a bouncer at the door: "The classifier acts as bouncer, not concierge." Instead of welcoming people in and figuring out how to help, it was checking IDs and turning away anyone without the right credentials. Worse — the eight contextual fallback messages we'd just written the day before were "a band-aid on exactly this wound." We'd been writing better rejection copy when we should have stopped rejecting people.

The PPM diagnosed a layer inversion. The system was using the LLM to *classify* queries but not to *respond* to them. It spent tokens deciding it couldn't help, then didn't use the LLM to actually help.

The Architect put it most precisely: "We use the LLM to classify but not to respond." The architecture was structurally inverted — handlers were the default path and the conversational floor was the last resort. It should be the opposite.

The CIO reframed the whole model: "The LLM is the floor, not the ceiling." Every query should reach the LLM with full project context. Structured handlers should make the response *better*, not *different*. Piper should always be at least as good as a well-prompted LLM.

Four roles. Four framings. One unanimous diagnosis.

Part of me felt super dumb. I have been making this harder on myself. In another way, I felt relief. No wonder! We could free Piper from the robotic shackles we've tied it up in and let it be a normal chatbot with extra powers, not a taskbot with a conversation function.

## Convergence in two hours

The PPM synthesized all four memos into a single document. The Architect reviewed it and confirmed: all architectural guidance accurately represented. The CXO approved without pushback. The CIO added one note about ethics constraints.

Four revisions incorporated. Synthesis ratified. By 5:11 PM, the document was in project knowledge as a binding direction.

Here's what struck me: four people looked at the same problem with different lenses — experience design, product strategy, system architecture, innovation methodology — and arrived at the same conclusion independently. That's not groupthink. That's signal.

The governing principle that emerged: "Piper is always at least as good as a well-prompted LLM with context. Structured handlers make it better, not different."

## From diagnosis to green light

The Lead Developer had been working all day on other M1 issues — E2E test infrastructure, MUX discovery, todo completion. By evening, the floor implementation was greenlit.

The Chief of Staff, tracking from the sidelines, called it: "Second unanimous convergence in two weeks." The team was getting good at this — independent assessment, parallel synthesis, rapid agreement. Not because they agreed reflexively, but because the evidence was unambiguous.

## The irony

The day before, we'd shipped eight carefully written contextual fallback messages. CXO-authored copy for when Piper couldn't help. Professional, human, kind rejection messages.

The CXO's own assessment of those messages, twenty-four hours later: "a band-aid on exactly this wound."

We'd been writing better rejection letters when we should have stopped rejecting. The entire contextual fallback system — designed, written, reviewed, tested, shipped in a single day — was a symptom of the problem, not a solution.

I've learned not to beat myself up too much when a sudden insight makes me realize I've been spending my energy on the wrong thing. Sometimes you need to go through something the wrong way to really understand it.

## What the PPM saw next

Late that evening, the PPM raised two strategic threads that went beyond the immediate fix.

First: if Piper can engage conversationally with full project context, it's not just a PM tool. It's a PM tool for non-PMs. Engineers, designers, stakeholders — anyone who needs project intelligence but doesn't think in PM frameworks. The floor inversion didn't just fix a bug. It expanded the addressable audience.

Second: the context problem isn't just about Piper's session. It's about context across seams — between chat sessions, between agents, between projects, between tools. The same architectural challenge appears at four or more scales. Klatch was wrestling with it. Piper was wrestling with it. The cross-pollination brief would later confirm it.

But those threads would unfold over the next week. On Saturday night, the immediate fact was simpler: we'd asked the right question, gotten an honest answer, and started building in a different direction.

---

_Next on Building Piper Morgan: The Floor That Wasn't — when "it works" doesn't mean "users experience it."_

*Have you ever had a moment where you realized your team was solving the wrong problem really well? What made you see it?]*
