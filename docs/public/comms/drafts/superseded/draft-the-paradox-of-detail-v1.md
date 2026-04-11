# The Paradox of Detail

*January 26*

[alt text: Two instruction manuals - one thick and ignored, one thin and dog-eared from use]
Caption: "The short one got followed"

We had a 30-line protocol for session logging. Agents kept forgetting to log. We replaced it with a 6-line reminder. Agents started logging consistently.

More detail didn't produce better compliance. Less detail did.

## The failure

After a context compaction incident on January 22nd, we wrote a comprehensive post-compaction protocol. It covered every scenario: what to do if a log exists, what to do if it doesn't, how to check timestamps, when to create versus continue, edge cases and exceptions.

It was thorough. It was correct. And agents kept failing to follow it.

The pattern repeated for three consecutive days. Detailed protocol in CLAUDE.md. Agent compacts context. Agent doesn't follow the protocol. Work goes unlogged.

## The diagnosis

The Chief Innovation Officer analyzed the pattern and identified what they called "verbosity backfire": detailed instructions can be *less* effective than simple triggers because of cognitive overload.

When an AI agent loads CLAUDE.md, it parses everything. A 30-line protocol takes attention—attention that could go toward the actual work. If the agent is under pressure (complex task, near context limit), detailed protocols may get skimmed or deprioritized.

A 6-line trigger, by contrast, is impossible to miss. "Check your session log. If it doesn't exist, create it. Then proceed." That's it. No edge cases, no exceptions, no scenarios.

[PM PLACEHOLDER: Did you have intuition that this was the problem, or was the CIO's analysis a surprise?]

## The architecture

The solution wasn't to abandon detailed procedures—sometimes you need them. The solution was to separate triggers from procedures.

The trigger lives in CLAUDE.md. It's short, loud, and survives context compaction. "CHECK YOUR SESSION LOG FIRST."

The procedure lives in a skill file. It contains the detailed steps, the edge cases, the error handling. The agent loads it when needed, prompted by the trigger.

It's like the difference between a smoke detector and a fire safety manual. The detector needs to be simple and unmissable—just a loud noise that says "ATTENTION REQUIRED." The manual can be comprehensive because you only consult it when the alarm has already gotten your attention.

## The principle

We've since applied this pattern to other protocols: discovered-work capture, issue closure, audit cascades. Each one has a trigger (inline in CLAUDE.md, under 10 lines) and a skill (detailed procedure, loaded on demand).

The principle: what must survive compaction must be inline, but what's inline must be simple.

Detailed and inline? Gets skimmed.
Simple and external? Gets lost after compaction.
Simple and inline, detailed when loaded? Gets followed.

## The meta-lesson

This isn't just about AI agents. It's about instructions generally.

Think about the onboarding docs that actually get read versus the ones that don't. Think about the coding standards that get followed versus the ones that live in a wiki no one visits. Think about the emergency procedures that work versus the ones that fail under pressure.

The ones that work tend to have a simple trigger ("In case of X, do Y") with detailed backup available if needed. The ones that fail tend to bury the trigger in comprehensive documentation.

When you're writing instructions—for AI or humans—ask yourself: what's the trigger, and what's the procedure? Is the trigger unmissable? Can the procedure be loaded on demand?

If you're combining trigger and procedure into one document, you might be creating something too detailed to follow and too important to skip.

[PM PLACEHOLDER: Any human examples of this pattern from your experience?]

---

*This is part of the Building Piper Morgan series, documenting what we're learning about AI-assisted development—including the frameworks that emerge from doing the work.*

*Have you ever had detailed instructions backfire? What was the simpler version that worked?*
