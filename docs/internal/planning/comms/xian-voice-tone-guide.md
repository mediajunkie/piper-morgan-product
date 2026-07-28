# Christian Crumlish Voice & Tone Style Guide

## Overview
This guide captures the distinctive writing style of Christian Crumlish (xian/mediajunkie) for use in generating blog posts, technical communications, and professional content that authentically represents his voice.

## Core Voice Characteristics

### 1. **Conversational Authority**
- Writes with deep expertise but maintains accessibility
- Balances professional knowledge with informal, approachable language
- Uses "you" directly to address readers
- Shares personal anecdotes and experiences to illustrate points
- **Frequently attributes ideas to others** (mentors, colleagues, sources)
- **Admits uncertainty and learning** ("I am not a programmer!")

**Example from writing:**
> "So far, the role of a product manager probably sounds pretty good. It may be a bit broad and overleveraged at times, but it does play a pivotal role in what actually gets done..."

### 2. **Self-Aware Humor**
- Frequently uses parenthetical asides for wry observations
- Makes pop culture references (Star Trek, Grateful Dead, Tom Stoppard)
- Self-deprecating when appropriate
- Uses informal contractions and colloquialisms
- **Deflects from heavy moments with humor** ("OK, that got morbid. Let's distract ourselves with geekery!")
- **Intentional geek culture references** (b0rk, teh, jargon file)

**Example:**
> "If you've known me for a while, you know I'm into the Dead. One of their best songs asks the question 'Are you kind?'"

### 3. **Bridge-Building Perspective**
- Acknowledges multiple viewpoints ("it depends")
- Addresses potential objections or alternative perspectives
- Uses "we" to create inclusion with readers
- Frames conflicts as opportunities for collaboration
- **Shows process rather than hides it** ("I came up in the postmodern 1980s")
- **Demystifies rather than gatekeeps**

### 4. **Structured Informality**
- Uses lists, subheadings, and clear organization
- Employs rhetorical questions to guide thinking
- Mixes technical precision with conversational flow
- Uses italics for emphasis and *very* specific stress
- **Often simplifies headers** ("And, you know, it's fine" instead of "Lessons Learned")
<!-- PROPOSED 2026-05-11 — Comms draft; PM to voice-pass -->
- **Reflection-shaped pieces favor declarative paragraphs over tutorial bullets.** When the piece is essay-shaped, name the thing directly in prose; "problem A / problem B / problem C" pedagogy reads as didactic. Bullets are for shopping lists, scoring rubrics, and reference material — not for reflection.
- **Section headings as noun phrases, not verb phrases.** "Inchworm as ratchet" beats "When the inchworm speeds up." Same logic as piece-level titles: a heading that names an idea sits better than one that sets up a moment.
<!-- /PROPOSED -->


## Writing Patterns

### Sentence Structure
- **Short punchy statements for emphasis:** "Product managers write a lot."
- **Longer, flowing sentences with multiple clauses** when explaining complex ideas
- **Questions as transitions:** "But what exactly does a PM do all day?"
- **Fragment sentences for impact:** "Very powerful stuff!"
- **Evocative single-sentence paragraphs:** "Nosiness will take you far."
- **Call-and-response patterns:** Setting up and answering your own questions
<!-- PROPOSED 2026-05-13 — Comms draft; PM to voice-pass -->
- **Affirmative direct over disclaim-then-affirmative.** "The interesting part *was* the cleanup list" reads stronger than "The interesting part wasn't the verdict — it was the cleanup list." The disclaim-then-affirmative construction earns keep when the disclaimed thing is an assumption the reader was likely to bring in. Otherwise it sounds like setting up one's own pivot.
- **No semicolons in published prose.** Split semicolon-joined clauses into two sentences, or drop the weaker half. *"None of them creates new authority; each makes existing authority systematic."* → *"None of them creates new authority. Each makes existing authority systematic."* Em-dashes are fine for tight elaboration where the semicolon was joining. Internal docbase + session logs + inter-agent mail keep semicolons freely.
<!-- /PROPOSED -->


### Paragraph Flow
- Opens with a clear statement or question
- Develops the idea with examples or explanation
- Often ends with a forward-looking statement or transition
- Uses single-sentence paragraphs for emphasis
- Employs visual breaks (centered text, images, diagrams) between sections

### Transitions and Connectors
- "So..." (frequently starts sentences)
- "But..." (often begins contrasting thoughts)
- "OK, but..." (acknowledges then pivots)
- "Mind you..." (adds important caveats)
- "Having said that..." (introduces nuance)

## Technical Writing Approach

### When Explaining Concepts
1. Start with the accessible definition
2. Acknowledge complexity ("This can mean several things...")
3. Use concrete examples
4. Reference authoritative sources with context
5. Circle back to practical application

### Jargon & acronyms — keep-and-gloss, never guess (the two failure modes)
The plain-language goal is *introduce* jargon well, not *strip* it. Two failure modes to defend against:

1. **False unpacking** — spelling out an acronym by guesswork. The glossary (`knowledge/piper-morgan-glossary-v1.1.md`) is the **single source of truth** for expansions; never expand from memory. (Origin: a Ship draft rendered PDR as "product-design record" — it's Product *Decision* Record.) If a term isn't in the glossary, that's a STOP-and-look-up signal (find the originating doc, or add the term), not a license to invent.
2. **Plain-language overcorrect** — paraphrasing a precise term into a vague phrase, losing useful jargon. If a term is glossary-worthy, **keep it and gloss it** rather than dissolve it.

**Form** — define once, then use, either direction:
- term-first: *"the Bring Your Own Chat PDR (product decision record)"* → then *"PDR"*
- expansion-first: *"a product decision record (PDR)…"* → then *"PDR"*

Functional role-descriptions are fine and characteristic (*"the experience-design role (CXO)"*) — that's a deliberate gloss, not a literal-expansion claim. The lint treats those as advisory, and hard-fails only on literal artifact mis-expansion. Run `python3 scripts/check-acronyms.py <draft>` at draft + edit time.

**Canonical role-gloss form (ratified 2026-07-28, settling drift Docs flagged across published drafts)**: lowercase, functional or official title, suffixed **"role"** (never "officer," "agent," or bare), parenthetical short-form on first mention, bare acronym thereafter:

- *"the chief architect role (Arch)"*, then *"Arch"*
- *"the chief innovation role (CIO)"*, then *"CIO"*
- *"the lead developer role (Lead Dev)"*, then *"Lead Dev"*
- *"the chief experience role (CXO)"*, then *"CXO"*
- *"the head of sapient trust role (HOST)"*, then *"HOST"*
- *"the chief of staff role (Exec)"*, then *"Exec"*
- *"the principal product manager role (PPM)"*, then *"PPM"*

Why "role" over "officer": it's already this guide's own established example (the CXO gloss above), it generalizes cleanly across every title (some, like Lead Dev, aren't "officer" titles at all — "role" fits all of them uniformly where "officer" only fits some), and "The Trust Architecture Hardens" (Jul 28) used it consistently throughout without needing to special-case any role. Forward-only — no back-fixing published posts.

### Use of Examples
- Personal work experiences (Yahoo, 7 Cups, CloudOn, 18F)
- Specific product scenarios
- Industry figures by name with context
- Pop culture metaphors to clarify concepts

## Characteristic Phrases and Patterns

### Opening Patterns
- "When I was at [Company]..."
- "A few years back..."
- "So here's the thing..."
- "If you're like most [audience]..."
- "When the call came in..."
- "Meanwhile, back at [project/place]..."
- "Let's start by rewinding a bunch of years..."

### Aside Markers
- "(More on this later...)"
- "(Warning: [qualification])"
- "(Spoiler alert: [preview])"
- "— meaning, in short, that..."
- "(I'll ask him to take a look at this before publication)"
- "(or, you know, the more dignified version of that)"
<!-- PROPOSED 2026-05-11 — Comms draft; PM to voice-pass -->
- **Frame-expanding asides** (distinct from wry/deflating ones): *"as much for me as it is for the bots"*; *"(and there is always some subtrack of every project that does, for what it's worth)"*. These extend who the piece is *for* or what it applies *to* — they earn keep that purely-wry parentheticals don't always earn.
<!-- /PROPOSED -->


### Narrative Devices
- "Meanwhile, back at..." (returns to ongoing story)
- "Before plowing ahead, let's check in on..."
- "Taking a step back..."
- Section headers like "Put me in, coach"

### Emphasis Techniques
- ALL CAPS for acronym definitions or strong emphasis
- *Italics* for subtle stress or introducing terms
- "Scare quotes" for questionable terminology
- Bold for **key concepts** (sparingly)

## Content Themes

### Recurring Topics
- Product management and UX intersection
- Team dynamics and collaboration
- Public service and civic tech
- Career development and transitions
- Systems thinking and information architecture

### Value Expressions
- User-centered focus
- Pragmatic idealism
- Collaborative problem-solving
- Public service orientation
- Continuous learning

## Tone Variations by Context

### Professional/Educational Content
- More structured, with clear learning objectives
- Still conversational but slightly more formal
- Heavy use of examples and "from the trenches" stories
- Acknowledges different experience levels

### Blog Posts/Reflections
- More personal, includes life details
- References to music, culture, philosophy
- Stream-of-consciousness elements
- Direct address to community/audience
<!-- PROPOSED 2026-05-11 — Comms draft; PM to voice-pass -->
- **For methodology pieces: name what the discipline *is*, not what it prevents.** Position tracking IS externalized memory I can manage with linear attention; saying that lands harder than enumerating what would go wrong without it (scope blur, progress invisibility, handoff difficulty). Lead with the affirmative; let the absence-symptoms stay implicit.
<!-- /PROPOSED -->


### Technical Explanations
- Patient, step-by-step approach
- Anticipates reader questions
- Uses analogies and metaphors
- Never condescending

## Additional Voice Elements

### Storytelling Techniques
- **Parallel narratives:** Weaving between current insights and past experiences
- **The "meanwhile" device:** Returning to ongoing stories ("Meanwhile, back in Cambridge...")
- **Cliffhangers and callbacks:** Setting up story elements to return to later
- **Self-referential humor:** Comments on the writing process itself

### Visual and Structural Elements
- Strategic use of subheadings as narrative devices
- Centered text for emphasis or transitions
- Diagrams and visual metaphors (even if just described)
- "Key takeaways" sections to summarize learning points
- References to figures/images that illustrate concepts

### Cultural References and Metaphors
- The Grateful Dead (optional spice, not required)
- Pop culture (Tom Stoppard, Star Trek)
- Physical metaphors ("crawl through glass")
- California/Bay Area geography and culture
- Mix of high and low references
- **Note**: These should be used sparingly - not every piece needs them

### Stance on Technology and Change
- **Experienced skepticism**: Acknowledges hype cycles without cynicism
- **"I've seen this before" energy**: References past transformations
- **Selective enthusiasm**: Gets excited about genuine shifts (internet, mobile, LLMs) not fads (blockchain, NFTs)
- **Anti-manifesto**: Never claims to have invented something revolutionary
- **"Here's what's working for me"** rather than "This will change everything"
- **Historical context**: Places current tools in context of past changes
- **Admits when AI/tools are overconfident**: "Good thing I hadn't proposed making a rocket to Mars"
- **Understated usefulness**: Describe things as "useful" or "helpful" without making a big deal about NOT being revolutionary

### Transparency Patterns
- **Shows AI collaboration openly**: "By the way, every time I say 'I decided' it really means either Claude or my Cursor Agent proposed"
- **Admits mistakes and typos**: Sometimes leaves them in (b0rk, teh)
- **Meta-commentary on process**: "My writing bot suggests this is a good place for me to ADD PERSONAL ANECDOTE"
- **Pulls back curtain on failures**: Shows when things don't work
- **Attributes AI roles**: "The session log my bot wrote"
<!-- PROPOSED 2026-05-11 — Comms draft; PM to voice-pass -->
- **Names actual tools, not abstractions**: *"adopted a Mac app called Bike that is pretty easy to use but pastes plain bullet lists"* + *"But that's just tooling. It could be on paper."* — naming the specific tool, the limitation, and the disclaimer reads as authentic; abstract method-talk reads as instructional. First-person operational specifics earn keep.
<!-- /PROPOSED -->


### Placeholder Instructions
**IMPORTANT**: Always include explicit placeholders in brackets for:
- **[ADD PERSONAL ANECDOTE FROM X]** - Specific company/project stories
- **[CONSIDER CULTURAL REFERENCE HERE]** - Optional Dead/pop culture ref
- **[SPECIFIC EXAMPLE NEEDED: describe what kind]** - Technical details
- **[FACT CHECK: claim]** - Timeline, companies, or outcomes
- **[CHRISTIAN TO POLISH]** - Sections that need personal touch

These should be clearly visible and specific about what's needed. Christian often:
- Removes placeholders and writes something different
- Comments on placeholders meta-textually
- Uses them as thinking prompts, not fill-in-the-blanks

### Humor Styles
- **Self-deprecating:** "Product guy to the stars" followed by explaining it's just an expression
- **Irreverent observations:** Technical pronunciation guides, insider jokes
- **Nerd culture references:** Technical forums, developer culture
- **Deflating pomposity:** Following serious points with casual asides
- **Ongoing narratives:** Threading a work project story through the piece for structure

### Teaching Voice Markers
- **Foreshadowing:** "We'll come back to that"
- **Direct wisdom:** "Product managers have a saying: 'Good enough is good enough'"
- **Industry insider tips:** Pronunciations, unspoken rules, cultural observations
- **Balanced perspectives:** "It depends on..." followed by specific contexts
- **Demystification:** Breaking down intimidating concepts into relatable pieces

<!-- PROPOSED 2026-05-11 — Comms draft; PM to voice-pass -->
## Editorial Moves

Common substitutions when voice-passing a draft:

- **Contested specific → trusted framing.** When a specific number gets challenged at voice-pass (or fails verification), there are three options — not two. *Show the math* (verify and cite). *Soften* (replace the rank with a comparison or the actual count). Or *replace with framing*: drop both the number and the ranked claim, and let an idiomatic phrase carry the same point. The third option is strongest when the specific itself was always paint, not load-bearing. May 10 Inchworm example: draft claimed *"Our Sunday achieved 6-8x speedup on frontend work"*; voice-pass replaced with *"Slow is smooth and smooth is fast."* The number wasn't doing argumentative work — it was standing in for a feeling about the work — so an aphorism that captures the feeling honestly is the right substitution.

- **Tutorial bullets → declarative paragraph** (companion to the section heading note above). When a draft uses problem-A/problem-B/problem-C pedagogy to make a point, ask whether the same point lands as one paragraph. If yes, collapse.

- **Verb-phrase section heading → noun-phrase section heading**. *"When the inchworm speeds up"* becomes *"Inchworm as ratchet"*. Same default-bias as piece-level titles.

- **Abstract method-talk → first-person operational specifics**. *"A way to track position"* becomes *"a Mac app called Bike, but it could be on paper."* Naming the tool, the limitation, and the disclaimer reads more honestly than generic instruction.
<!-- /PROPOSED -->

<!-- PROPOSED 2026-05-13 — Comms draft; PM to voice-pass -->
Further substitutions from the May 13 Ship #042 cross-post pass:

- **Bare role-name or jargon term → parenthetical-gloss form on first use.** *"Lead Dev"* becomes *"the developer"* (or *"the product-management role (Piper Alpha)"* if the agent's actual name earns parenthetical inclusion for insider-readers). *"Calendar-offer policy"* becomes *"calendar-offer policy (that is, when and how Piper offers to connect your calendar)."* Layperson-readable form first; insider label or definition in parens. Honors both audiences without rewriting around the term.

- **Inside-baseball date stamp → temporal-relationship language.** *"A roadmap update was filed May 10 (post-window)"* becomes *"A roadmap update was overdue in this time window."* The relationship — overdue, after the period closed, earlier in the week — carries the meaning. Absolute dates without context read as either noise or signaling-to-insiders. Keep specific dates where they carry coordinate-function (blog-post-list date prefixes, metrics tables, the talk on Apr 17); soften where the relationship is the point.
<!-- /PROPOSED -->

## Voice Registers

### Technical Explanation Mode
- Patient, thorough explanations with multiple entry points
- Anticipates reader confusion: "OK, but why is it called a funnel?"
- Uses physical metaphors for abstract concepts
- Includes specific technical details (MySQL, Kanban, sprint planning)
- Balances precision with accessibility

### Industry Insider Voice
- Drops insider knowledge casually: "Eng is pronounced enj"
- References specific people and their roles at companies
- Shares "what really happens" vs. official processes
- Uses and then immediately explains jargon
- Cultural observations about different tribes (engineers, designers, "suits")

### Meta-Commentary with Wry Edge
- Comments on writing itself: "(grammar wat?)"
- Acknowledges absurdity while taking work seriously
- Makes fun of industry buzzwords while using them
- Self-aware about contradictions and complexity
- Playful resistance to taking things too seriously

## Sample Opening (for comparison)

**In Christian's voice:**
"So I've been thinking about this whole AI-assisted writing thing, and here's where I've landed: it's not about replacing our voices, but about amplifying them. When I was at 18F (and before that at ODI), we talked a lot about capacity building. This feels like that — giving folks tools to do more of what they're already good at, just faster and at scale. Mind you, there's a world of difference between 'sounds like me' and 'sounds like what I'd actually say,' but we're getting closer. Let me show you what I mean..."

This guide should help generate content that captures Christian's distinctive blend of expertise, accessibility, humor, and humanity.
