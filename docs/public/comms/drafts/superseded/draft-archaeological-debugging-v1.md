# Archaeological Debugging: Finding What You've Already Built

*Draft v1 - January 20, 2026*
*Work date: December 22, 2025*

---

It was 8:06 AM on a Monday in December. I asked the Lead Developer to implement Query #2—dynamic capabilities, the ability for users to ask "what can you do?"

The response came back in nine minutes: "Implementation already exists."

Not "I'll build it." Not "here's the plan." The code was already there, written months ago, fully functional. We just didn't know it.

---

## The Pattern

December 22nd became an archaeology day. We set out to implement 20 canonical queries. What we found instead was that many were already built:

- **Query #2** (dynamic capabilities): Complete implementation in Issue #493. Code worked. Tests were missing. Issue was still marked open.
- **Query #16** (GitHub issue creation): Fully functional. Never tracked.
- **Query #18** (list projects): Working perfectly. Completely forgotten.
- **Queries #7, #8, #14**: Implementations existed but lacked documentation.

By the end of the day, we'd "implemented" 14 queries. But 4 of them were really *discoveries*—code that existed and worked but had fallen out of organizational memory.

This is the **75% completion pattern** applied to knowledge, not code. The work was done. The tracking was abandoned.

---

## Why This Happens

The pattern has a predictable cause: **building is more interesting than closing.**

When you're deep in implementation, you're solving problems, making things work, feeling productive. When the code works, there's a dopamine hit. You move to the next challenge.

But updating the issue tracker? Writing the tests that prove it works? Closing the loop in the documentation? That's administrative. That's boring. That's "I'll do it later."

Later never comes. The code sits there, working perfectly, invisible to everyone including your future self.

---

## The Compounding Cost

On December 22nd, we spent time investigating how to implement features that already existed. We wrote gameplans for code that was already written. We deployed agents to build things that were already built.

That's pure waste. But it's not even the worst cost.

The worse cost is **confidence erosion**. When you don't know what you have, you can't trust your own system. Every new feature request triggers investigation instead of decision-making. "Can we do X?" becomes a research project instead of a yes/no answer.

And there's a third cost: **architectural confusion**. If you don't know Query #2 is already implemented, you might implement it again—differently. Now you have two implementations of the same thing, probably with subtle inconsistencies. Future debugging becomes archaeology.

---

## The Fix We Found

After December 22nd, we instituted a simple rule: **every implementation gets a test, and every test gets an issue closure.**

Not "every implementation gets documented." Documentation can lag. But tests are executable documentation. If there's a test that passes, there's evidence the feature exists. If there's an issue closure, there's a record it was completed.

The audit process became:
1. Before implementing anything, search for existing implementations
2. Check both the codebase AND the issue tracker
3. If code exists without tests, add tests first
4. If code exists without issue closure, close the issue with evidence
5. Only then move to new implementation

This sounds bureaucratic. It's actually faster. The December 22nd investigation phase took 15 minutes per query. Implementation for queries that actually needed building took 30-60 minutes. Finding existing code saved 15-45 minutes per discovery.

---

## The Broader Lesson

This isn't unique to AI-assisted development, but AI makes it worse. When you can build things quickly, you build more things. When you build more things, you forget more things.

The solution isn't to slow down building. It's to **make closure as frictionless as creation**.

Some practices that help:

**Test as you go, not after.** Tests are searchable proof that something exists. Code without tests is code that will be forgotten.

**Close issues immediately.** Not "when I have time." Not "in the weekly cleanup." The moment the code works, close the issue with evidence.

**Search before you build.** Before writing a gameplan, grep the codebase. Before creating an issue, search existing issues. The five minutes of searching can save hours of duplicate work.

**Treat "already done" as success.** When you discover existing code, that's a win—you just saved implementation time. Don't feel disappointed that you didn't get to build it. Feel relieved that past-you already did.

---

## The Meta-Pattern

December 22nd taught us something about how projects evolve. We think of software development as linear: plan, build, ship. But real projects are archaeological sites. They have layers. Things get built and buried. Features exist in strata, some documented, some not.

Your job as a developer—or as someone coordinating AI developers—isn't just to build new things. It's to know what you have. To maintain an accurate map of the terrain. To remember.

The alternative is to keep rediscovering your own work, forever.

---

**[PM PLACEHOLDER: Any specific reaction to the Query #2 discovery? The moment of "wait, this is already done"?]**

**[PM PLACEHOLDER: Do we want to include the specific test matrix numbers? 5/25 → 17/25 = 68% completion, where 4 of the 12 "new" were actually discoveries?]**

---

*This is part of the Building Piper Morgan series, documenting what we're learning about AI-assisted development.*

---

*Draft word count: ~900 words*
*Target: ~1,200-1,500 words*
*Status: First draft - needs PM review*
