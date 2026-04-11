# The Audit Cascade

*January 13*

[alt text: Robot carefully inspecting parts at a workbench while another robot assembles nearby]
Caption: "Checking the checklist"

Here's something we discovered by accident: AI is better at checking work than doing work.

Not "better" as in faster or cheaper. Better as in *more reliable*. When you ask an AI to create something while following a checklist, it will miss items on the checklist. When you ask the same AI to audit existing work against the same checklist, it will catch those misses.

This asymmetry changed how we build everything.

## The discovery

In January 2025, we were struggling with consistency. Our AI agents would produce deliverables that looked good but missed requirements. A document would be well-written but skip a required section. Code would be clean but miss an edge case from the spec. A process would be followed but a step would be skipped.

We tried more detailed prompts. We tried including checklists in the system instructions. We tried breaking work into smaller pieces. Nothing reliably solved it.

Then one of our architects had a thought: What if we stopped asking the AI to follow the checklist during creation, and instead asked it to audit its own work afterward?

We tried it. The difference was immediate.

## The pattern

We now call this the Audit Cascade. It's Pattern-049 in our methodology handbook, and it works like this:

Create first. Ask the AI to produce the deliverable. Don't burden it with extensive checklists during creation. Let it focus on the creative, constructive work.

Audit second. Give the AI the checklist and ask it to review the deliverable against each item. "Here's what you produced. Here's what was required. What's missing?"

Fix what's found. Address whatever the audit caught. This might mean asking the AI to fix it, or it might mean human intervention.

Proceed only when the audit passes. Only move to the next phase when verification succeeds.

The key insight: the same AI that missed items during creation will catch those same items during audit. It's not that the AI doesn't know the requirements. It's that creation and evaluation use different cognitive modes.

## Why this works

Think about how humans work. A writer drafting a document is in creative flow—generating ideas, building arguments, finding words. A different part of the brain activates when that same writer edits—checking structure, catching errors, evaluating against criteria.

Trying to do both simultaneously is hard. That's why "write drunk, edit sober" is advice, even if apocryphal. The modes are different.

AI seems to have something analogous. During generation, the model is predicting what comes next, building coherent output, maintaining style and structure. Requirements become one signal among many, easily deprioritized when other concerns dominate.

During audit, the task is different: compare this artifact against these criteria. It's a matching problem, not a generation problem. The checklist isn't competing with creative concerns—it IS the concern.

## The numbers

Before implementing the Audit Cascade, our agents completed requirements correctly about 70-80% of the time. Not bad, but the 20-30% miss rate compounded across steps. A five-step process with 75% reliability per step yields 24% end-to-end reliability. (0.75^5 = 0.237)

After implementing the Audit Cascade, our completion rate improved to 95%+ per step. The same five-step process now yields 77% end-to-end reliability. (0.95^5 = 0.774)

That's not just a little better. It's the difference between "usually works" and "mostly broken."

## What it looks like in practice

Here's a real example from this week. We asked an AI agent to create an Architecture Decision Record. Our ADR template has twelve required elements.

Without the Audit Cascade, the agent produced a well-written ADR that covered the technical decision beautifully. It missed the "Alternatives Considered" section, had a vague "Consequences" section, and omitted the status field entirely. Three of twelve elements insufficient.

With the Audit Cascade, same agent, same request. First pass produced similar output. Then we said: "Audit this against the ADR template. For each required element, state whether it's present and complete."

The agent immediately identified all three gaps. We asked it to address them. Final document: twelve of twelve elements complete.

Same AI. Same template. Different approach. Different result.

## The word "audit" matters

We experimented with different framings: "Check your work against this list." "Review the document for completeness." "Verify all requirements are met." "Audit the deliverable against these criteria."

"Audit" performed best. We suspect it's because the word carries specific connotations: systematic, thorough, external evaluation. "Check" is casual. "Review" is vague. "Audit" implies rigor.

This might seem like trivial wordsmithing. In practice, word choice shapes AI behavior. The model's training included countless examples of what "audits" look like—thorough, criteria-based, documented. Using that word activates those patterns.

## Institutionalized skepticism

The Audit Cascade isn't just a technique. It's a philosophy: institutionalized skepticism at every handoff.

Every time work passes from one phase to another, it gets audited. Every time an AI agent produces something, another agent (or the same agent in audit mode) reviews it. Every time a human approves something, they've seen an audit report.

This sounds bureaucratic. It sounds slow.

It's actually faster.

Here's why: catching a problem at step 2 costs minutes. Catching the same problem at step 8, after six more steps built on the flawed foundation, costs hours. The audit time is an investment that pays compound returns in reduced rework.

We now complete complex projects faster than before we implemented the Audit Cascade. Not because each step is faster—each step is actually slightly slower. But we almost never have to throw away work and start over. We almost never discover at the end that a foundational assumption was wrong.

The skepticism is built into the process. We don't have to remember to be careful. The workflow requires it.

## Applying this elsewhere

You don't need our specific tooling to use the Audit Cascade. The principle applies anywhere you're using AI for complex work.

Document creation: Generate the document, then ask the AI to audit it against your template before sending.

Code development: Write the feature, then ask the AI to review it against your acceptance criteria before merging.

Email drafting: Compose the message, then ask the AI to audit it. Does it address all the recipient's questions? Is the tone appropriate? Is the call-to-action clear?

Process execution: Complete the steps, then ask the AI to audit the execution. Were all required steps completed? What evidence exists for each?

The key is separating generation from evaluation. Don't ask the AI to create-and-verify simultaneously. Ask it to create, then verify.

## The uncomfortable implication

The Audit Cascade works because AI isn't reliable enough to trust without verification. This is uncomfortable if you were hoping AI would "just work."

But it's actually good news. It means you can get reliable output from unreliable components. You can build trustworthy systems from probabilistic parts. You just have to design for verification rather than assuming correctness.

This is how we build reliable systems everywhere else. Airplanes have multiple redundant systems that check each other. Financial transactions have auditors. Scientific papers have peer review. The Audit Cascade is the same principle applied to AI-assisted work.

## The one-liner

If there's one thing to take from this, it's this:

Don't ask AI to follow the checklist. Ask AI to audit against the checklist.

Same checklist. Same AI. Different results.

---

*Next on Building Piper Morgan: The October Ghost, when a 5:38 AM email from Google revealed a three-month-old security leak hiding in our logs.*

*Have you noticed AI being better at checking than creating? What verification practices have you built into your AI workflows?*
