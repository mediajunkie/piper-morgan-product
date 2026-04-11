# The CLAUDE.md Paradox

*January 22-23*

[alt text: A document shrinking dramatically, with a clock showing 12 hours passing in shadow]
Caption: "87% smaller, 100% broken"

We made CLAUDE.md 87% smaller. Then we lost 12 hours of work logs. Then we fixed it the next morning.

That's the shape of January 22nd and 23rd—the days we learned that instructions meant to help AI agents can backfire spectacularly when they get too detailed.

## The problem

CLAUDE.md had grown to 1,257 lines. This is the file that tells AI agents how to behave in our codebase—what protocols to follow, how to handle various situations, where to find things.

Research suggests AI agents follow instructions better when those instructions are under 300 lines. We were four times over that limit. The docs agent proposed a "Tier 3 refactor"—an 87% reduction that would move detailed protocols to external files, leaving only essential triggers in the main document.

I approved it. The refactor was clean, well-organized, and principled. CLAUDE.md went from 1,257 lines to 157 lines.

[PM PLACEHOLDER: What was your reasoning for approving? Did you have any hesitation?]

## The failure

Here's what we didn't anticipate: after a context compaction (when Claude's context window fills up and gets summarized), the agent loses access to everything except what's explicitly in the current context.

The old CLAUDE.md had a post-compaction protocol embedded directly in the file. "After compaction, check your session log. If it doesn't exist, create it."

The new CLAUDE.md referenced that protocol in an external file. After compaction, agents didn't load the external file. They didn't know to check their logs. They didn't know logs existed.

For the next 12 hours, substantial work happened—17 issues closed, hundreds of tests written—with no session logs maintained. The agents were productive. They just weren't documenting anything.

## The discovery

The next morning, the docs agent started creating the January 22 omnibus log and noticed something wrong. Where were the session logs from yesterday afternoon and evening?

Forensic investigation revealed the gap. File timestamps showed when work happened. Git commits showed what was done. But the real-time session logs that capture context, decisions, and reasoning? Gone.

We reconstructed what we could from file timestamps and git history. But reconstruction is archaeology, not journalism. You lose the "why" and keep only the "what."

## The fix

The fix was almost embarrassingly simple: put the critical protocol back into CLAUDE.md.

Not the whole 1,257 lines. Just the parts that absolutely must survive context compaction. About 70 lines total—the post-compaction protocol, session log requirements, and a few other essentials.

CLAUDE.md went from 157 lines to 230 lines. Still 82% smaller than the original, but now containing everything an agent needs to maintain continuity across context boundaries.

[PM PLACEHOLDER: How did you feel when you realized the problem was so simple to fix?]

## The paradox

Here's what makes this interesting: the refactor was correct by every reasonable standard. Shorter is better for AI instructions. External references reduce duplication. Clean organization aids comprehension.

But it broke a hidden assumption: some instructions must survive context boundaries, and external references don't.

The paradox is that our attempt to make instructions more followable made them less followable. The 1,257-line file was bloated and hard to parse, but it worked. The 157-line file was elegant and well-organized, but it failed at a critical moment.

## The lesson

We've since formalized this as a principle: protocols that must survive compaction must be inline, but they must also be simple.

The old 1,257-line file survived compaction because everything was inline. But agents probably weren't following most of it—too much to process. The new 157-line file was followable but didn't survive compaction.

The sweet spot is minimal inline protocols (the triggers) with detailed external references (the procedures). The trigger survives compaction and tells the agent what to do. The agent then loads the detailed procedure when needed.

It's like the difference between a fire alarm and a fire evacuation plan. The alarm needs to be simple and loud—just "CHECK YOUR LOGS." The detailed procedure can live elsewhere, consulted when the alarm goes off.

## The meta-lesson

This incident revealed something about working with AI agents that I hadn't fully appreciated: they have a "memory horizon" that humans don't.

When I approve a refactor, I remember the reasoning behind my approval even if the document changes. An AI agent doesn't. After compaction, it only knows what's in front of it. If the instructions it needs aren't there, they might as well not exist.

Building systems with AI requires thinking about these boundaries—not just what the agent can do, but what it can remember, and what happens when it forgets.

[PM PLACEHOLDER: Any reflection on how this changes your mental model of working with AI agents?]

---

*Next on Building Piper Morgan: The MVP Rubric, where a disagreement between advisors revealed the question that matters most.*

*Have you ever had a well-intentioned improvement backfire in unexpected ways? What hidden assumption did it violate?*
