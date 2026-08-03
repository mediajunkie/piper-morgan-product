---
image: 'ai-apprentice.png'
alt: 'A workshop where a human creator watches proudly from above as a glowing AI lead developer supervises a smaller AI subagent completing careful work below, while a shared mechanical cable quietly causes a tiny unnoticed disturbance in the workshop machinery'
caption: '"They grow up so fast!"'
---

# First Subagent in Production

*May 6–7, 2026*

Quite a while back the so-called Excellence Flywheel methodology we're evolving to build Piper Morgan came up with the concept of an audit cascade. This was when I would first plan my next move in a chat with my Chief Architect agent (Arch), resulting in them writing a draft gameplan.

# How I used to do it

No matter how well I populated the project's knowledge base, Arch would still take some guesses and wave its hands around details it didn't know or couldn't directly inspect. The chief would then decompose the plan into draft GitHub issues that I would manually populate or save as drafts in a markdown file for an agent to build from.

Eventually I learned it helped to write a strict template and instruct them to use it. Then I found out that still didn't work because their adherence was only partial. Finally, I learned to have them review their draft against the template, identify any gaps, and fill them in.

I would then bring the gameplan to my Lead Developer agent — which by then was running full time in Claude Code — and give it the issues and plan the sprint. Finally, the Lead Developer would write prompts for the actual coding agents, supervising them, rather than writing the code itself.

Bear with me, I'm coming to a point.

# What's an audit cascade?

The audit cascade grew out of learning that everything these agents do has to be bookended, cross-checked, verified, stress-tested, and it will still be missing something. The audit cascade worked like this:

1. Audit the gameplan: Read it, review it against the actual running code and plan docs of record, revise it, discussing with me as needed.
2. For each issue in the plan, audit the issue against the issue template, ensuring that each section is included, and that there are checkboxes for all tasks as well as all acceptance criteria (this is critical for the bookending afterward, when my /close-issue-properly skill requires all checkboxes be checked with linked verifiable evidence or approved for deferral or excusal by me.
3. Finally, and here was the crucial part, the Lead Dev then wrote prompts for the coding agents who would do the adversarial test-driven development. One writes tests, the other writes code. Following the same pattern, LD follows a strict prompt template, and *then* audits each draft against the template.

But once the Lead Dev started running directly in Code and the harness evolved significantly, it took over much of the direct work and was delivering so excellently, that we no longer had to get a gameplan from Arch for each new move (following the roadmap and the docs was often enough), and we stopped deploying multiple agents to do the work.

# When to use subagents

Eventually, I got a bit worried about this. We weren't employing flywheel discipline and some methodological regressions were beginning to creep in. I still don't require a gameplan or the use of subagents, but I do require advance planning for complex efforts and it was on May 6 that I required Lead Dev to include subagents prompted by our templates, in the audit cascade again.

Given the way session context works, from their perspective this was a "first," and to be fair in the technical particulars, it was.

The issue was test migration — a queue of stale unit tests left behind after the standup-conversation persistence work I described in another piece had landed. The tests needed mechanical rewrites against the new persistence layer. Single-purpose work, no architectural calls, well-scoped — exactly the shape that justifies a subagent. Lead Dev built the audit cascade for the deployment in three passes.

1. The Gameplan audit ran twenty-seven checks. Four "N/A" calls — the gameplan was scoped tight enough that several check categories didn't apply, but I still had to approve each exception.
2. The Issue audit ran twenty-four checks. One ⚠️ for a Developer Experience question I needed to dispose of, which I did. 
3. The Prompts audit ran thirty-six checks against the subagent brief itself. Six "N/A" calls.

That last set caught my attention. I'd run the audit cascade enough times by then to have a sense for the N/A rate. Six of thirty-six is high. 

Lead Dev explained it. The prompt templates derived from a time when I would pit a Cursor agent against a Claude Code agent, and the Cursor-related language persisted in the long unused prompt templates. They had categories that didn't generalize cleanly to a subagent-deployment context. The template was drifting from its use cases. 

Lead Dev filed a template-hygiene tracking issue for later and pinned a new memory: *when an audit produces five-plus N/A flags in one pass, treat the count as a signal that the template needs review, not as five-plus separate "doesn't apply" judgment calls.*

(Note: I observe these memories but I never rely on them.)

By bedtime the prep package was complete. Gameplan, three audit documents, the subagent prompt itself. Ready to deploy.

# The thirty-minute run

The next morning at 6:48 AM Lead Dev launched the subagent.

It ran in the background. Phase 1, Phase 2, Phase 3, Phase 4 — each phase a chunk of tests to migrate. Lead Dev got on with other work in the foreground while the subagent worked. At about 7:18 AM the subagent finished. Lead Dev ran the post-execution audit — sixteen checks against the actual work the subagent had done. All sixteen passed. Merge, close, sign-off. Fifty minutes deployment to merge.

Two things from inside that fifty minutes are worth slowing down for.

The first is how the subagent handled an unexpected finding. Phase 2 of the gameplan said *migrate the twelve tests in this file*. When the subagent got to the file, the tests didn't need migration — they were already passing under the new persistence layer. The plan had been wrong about the work, not about the goal. The subagent's response was to annotate the gameplan with what it had found, mark Phase 2 complete without modifying the file, and proceed to Phase 3. It did not improvise. It did not "fix" the gameplan by going beyond its scope. It surfaced the discrepancy and continued.

That's the audit-cascade discipline operating at the execution layer — not at the prep layer where Lead Dev had run it the evening before, and not at the closure layer where Lead Dev would run it half an hour later. The same discipline, the same posture, applied by a different actor inside the same procedure. The subagent had absorbed the *"reframe rather than improvise"* shape that the methodology had been holding all along.

# The collision

The second thing is less elegant.

Around seven o'clock — partway through the subagent's run — Lead Dev needed to update the session log with a note. The practice by then was a sequence of steps run in order: first check which workspace you're submitting work to, then submit. If the workspace is the right one, the sequence proceeds and the work lands where it should. If it's not, you see the wrong answer, you stop, you fix it.

The subagent was working in a separate workspace — but Lead Dev and the subagent were sharing a single pointer that is supposed to track which workspace was currently active. When the subagent moved to its own workspace, it moved the shared pointer too. Lead Dev's check ran. A check that completes without errors returns a green light. A green light means the check ran. It does not mean the answer was the one you wanted. The sequence proceeded. The work landed in the subagent's workspace, not the main one.


The recovery was easy. The misplaced work would be folded back in cleanly when the subagent's workspace was eventually merged into the main record. Two new lessons learned. 
1. Verification isn't enough if you don't get the right result. Run the check as a separate step, make sure you are verifying the outcome and not the evidence. Then actually read the answer. If you can, design the sequence so it can only continue when the *answer* is specifically what you need not merely that the question was *successfully asked*.
2. When two workers share a single pointer to their active workspace, one worker's movement silently redirects the other's. The mitigation is to give the subagent its own isolated workspace from the start, so its navigation doesn't affect yours.

Both lessons were small. Both were exactly the right size — narrow enough to actually follow next time.

# The coming agent swarm

The fifty-minute deployment was satisfying in itself. A real piece of test-migration work moved through a real subagent in a real morning sprint. The audit-cascade methodology operated at every layer it was supposed to. The subagent absorbed the discipline. The closure was clean.

The collision was the more interesting payoff. Until that morning the audit cascade had been a methodology that the parent agent ran. After that morning it was clear the methodology had a *fourth* layer the prep hadn't named — the scaffolding around the deployment. Tool composition, branch identity, working-tree isolation, the difference between an exit code and a result. The discipline had been built for the work. The work surfaced where the discipline still needed to grow.

I know Anthropic is baking all of this sort of stuff directly into their harness, starting at the Team and higher tier levels, and that my own fumbling bespoke home-made methods will eventually be subsumed by commodified platform table stakes, but for now, I still like delegating down a chain that I designed.

# It's audits all the way down

Most of what counts as discipline at one layer of a system turns out to need its own discipline at the layer below. Auditing the work generates audits that the audit procedure itself needs. Deploying a tool gets you the tool's behavior plus the tool's interaction with the environment it's deployed into. The first deployment of any production-scale tool is the moment the methodology meets the operating environment, and what surfaces is reliably some piece of the methodology that nobody had thought to write down.

Build the discipline anyway. Deploy the tool anyway. The discipline that arrives in the small lessons from that first deployment is usually more durable than the discipline that arrived in the prep work.

---

*Next on Building Piper Morgan: **Hypothesis Refuted** — the quality benchmark dropped six points after three weeks of major changes. The investigation found no regression. What had drifted was the measurement.*

*Where in your work has a tool's first production deployment surfaced a piece of discipline you'd been carrying tacitly? What got written down?*
