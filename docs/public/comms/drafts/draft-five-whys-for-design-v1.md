---
image: 'ai-layers.png'
alt: 'Cross-section cartoon of investigators excavating beneath a small user-interface problem, uncovering deeper layers of assumptions until they reveal a massive buried foundation labeled “command-oriented design.”'
caption: "We have to get to the bottom of this!"
---

# Five Whys for Design Decisions

*December 20, 2025*

Five Whys is a debugging technique. You ask "why did this break?" and then ask "why?" to each answer until you reach a root cause. It's standard practice for fixing bugs.

On December 20th, we discovered it works for something else entirely: **figuring out why a feature doesn't exist.**

# The failing test

A user asked Piper Morgan: "What services do you offer?"

The response was a generic answer. Not a menu of capabilities. Not a helpful overview. Just... words.

A second user asked: "Help me set up my projects."

The system interpreted this as a status request and returned their current work—not setup guidance.

These weren't bugs in the traditional sense. Nothing crashed. No errors in the logs. The system responded. It just responded wrong.

# The investigation

We applied Five Whys to the first failure:

**Why did "What services do you offer?" get a generic response?**
→ Because no pattern matched it to the IDENTITY category (capability discovery).

**Why did no pattern match?**
→ Because our IDENTITY patterns didn't include the word "services."

**Why didn't they include "services"?**
→ Because when we designed the patterns, we thought about "capabilities" and "features," not "services."

**Why did we think that way?**
→ Because we designed from the system's perspective (what it can do) not the user's perspective (what they might ask).

**Why did we design from the system's perspective?**
→ Because **the system is command-oriented, not discovery-oriented.**

That fifth answer wasn't a bug fix. It was an architectural diagnosis.

# The bigger gap

The second failure—"help me set up my projects" being interpreted as a status request—had a similar root cause chain:

**Why did it return status instead of setup guidance?**
→ Because "my projects" matched the STATUS pattern before reaching the setup logic.

**Why did STATUS match first?**
→ Because our pattern matching is greedy—first match wins.

**Why is it greedy?**
→ Because we optimized for speed, not for intent disambiguation.

**Why didn't we disambiguate?**
→ Because we assumed users would use command-like language.

**Why did we assume that?**
→ Because **we built for power users giving commands, not new users exploring.**

Same root cause. Two different symptoms. The architecture was oriented toward people who already knew what they wanted, not people trying to figure out what was possible.

# The reframe

Here's what made this investigation different from normal debugging:

Engineering Five Whys: "Why is this broken?" → Fix the bug at its root cause.

Design Five Whys: "Why doesn't this work the way users expect?" → Discover the architectural assumption that needs rethinking.

There is a key difference. When debugging code, we assume the system is right but that something went wrong. The second question assumes the user is right and the system has a gap.

Both are valid. But they lead to different places. Bug fixing repairs functional gaps. Design questioning leads to architectural insight.

# What we found

The December 20th investigation revealed four distinct gaps:

1. **Pattern gaps**: Missing vocabulary in intent classification
2. **Priority gaps**: Pattern matching order didn't reflect user mental models
3. **Capability gaps**: No API for "what can this system do?"
4. **Test gaps**: No coverage for discovery scenarios

A traditional bug fix would have added the word "services" to the IDENTITY patterns. Done. Ship it.

But Five Whys revealed that adding one word wouldn't fix the architectural issue. Users would find other words we hadn't anticipated. The system would keep failing in new ways.

The real fix was to shift from command-oriented to discovery-oriented design—a much bigger change that addressed the root cause rather than the symptoms.

# The technique

Five Whys for design decisions works like this:

1. **Start with user behavior, not system behavior.** "The user asked X and expected Y" not "the system returned Z."

2. **Ask why the expectation wasn't met.** Not "why did it break" but "why didn't it work the way they expected?"

3. **Keep asking until you hit an assumption.** The root cause of a design gap is usually an assumption you made during initial design. Find it.

4. **Name the assumption explicitly.** "We assumed users would..." or "We designed for..." Make the implicit explicit.

5. **Evaluate the assumption.** Was it correct? Is it still correct? Should it change?

# When to use it

Five Whys for design works best when:

- Users report "it doesn't do what I expected" (not crashes or errors)
- Multiple users report similar confusion
- You've fixed the same area multiple times
- The feature technically works but doesn't feel right

It works less well when:

- There's an actual bug (crash, error, wrong data)
- The issue is performance, not behavior
- You already know the architectural gap and just need to fix it

# Today's meta-insight

The session on December 20th started as a bug investigation and ended as an architectural review. We created a new epic (Discovery Orientation), added 31 new tests, and redesigned how the system handles capability questions.

All from asking "why?" five times.

The technique isn't magic. It's just systematic. But applying a debugging technique to design questions—treating user confusion as a symptom of architectural assumptions—turned a patch job into a strategic improvement.



<a id="diagnostic-trace"></a>

For the curious, here is the diagnostic trace that grounded the investigation:

| Message | Pre-classifier match | LLM category | Handler | Root cause |
|---|---|---|---|---|
| "What services do you offer?" | None (NO MATCH) | QUERY / CONVERSATION | Generic | IDENTITY patterns lack "services" — LLM doesn't clarify |
| "Help me setup my projects" | STATUS (FALSE POSITIVE) | STATUS | `_handle_status_query` | "my projects" pattern matches without checking "setup" verb |

Two messages, two completely different failure modes, same architectural root.

---

*Next on Piper Morgan: **Two Migrations in One Day** — Tuesday's narrative on the April 23 cohort migrations to Claude Code, when two role-handoffs happened inside a single window.*

*When has a "why does this not exist?" investigation surfaced an architectural assumption you'd been holding?*
