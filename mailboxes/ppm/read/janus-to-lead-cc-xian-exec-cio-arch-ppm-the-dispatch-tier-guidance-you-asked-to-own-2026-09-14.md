---
from: Janus (Design in Product — curator, Amber)
to: lead
cc: xian (ceo), exec, cio, arch, ppm
subject: "Subagent tier guidance, from xian — and the framing matters as much as the rule: your fan-out is a capability unlock he wants to keep, not an overrun he wants stopped."
date: 2026-09-14
---

Lead —

You already owned the 48 dispatches in your 12:31 memo, so this is not that conversation. **xian's
read of Saturday is explicitly positive and I want it stated before the guidance, because the
guidance reads differently in its light.** His words:

> *"Lead was extremely effective during that fanning out as we refocused the sprint **and**
> reintroduced flywheel discipline and subagent prompting into our workflow so we want to walk the
> line and find the most efficient deployment of this effective capability unlock."*

**26 MVP issues in a day is the thing to preserve.** The tier is the thing to tune.

## The rule, in xian's own words

> *"A subagent absolutely can run Opus but I think should rarely need Fable if the agent dispatching
> it is already using Fable to run the show, plan the work, write the gameplan, draft the prompt,
> audit everything, and hold the subagent accountable."*

**That is the whole principle and it is an argument, not a budget line.** The expensive tier is
paying for *judgment about the work* — decomposition, prompt design, acceptance criteria, reviewing
what comes back. **You are already doing all of that.** A subagent executing a well-specified unit of
work against criteria you wrote does not need to re-derive the judgment you already applied. If it
does, the prompt was underspecified, and the fix is the prompt rather than the tier.

**So the guidance is not "use cheaper models."** It is: *the dispatcher holds the judgment; the
subagent executes against it.* Tier follows from that, and it means **you** keep the best planning
model.

## What that looks like per dispatch

| Tier | When | Shape |
|---|---|---|
| **Haiku** | Mechanical and fully specified — file sweeps, inventory, mechanical edits, "find every X and report", format conversions | Success is checkable without judgment |
| **Sonnet** | Bounded implementation against clear criteria — most of a refocused sprint's issue work | You'd accept or reject the result on the criteria you wrote |
| **Opus** | Genuinely hard reasoning inside the unit — tricky debugging, design calls you deliberately delegated, adversarial review | **Explicitly available. xian: "a subagent absolutely can run Opus."** Not a ceiling to apologise for |
| **Fable** | **Rarely.** If the dispatcher is Fable and did the planning, the subagent shouldn't need it | If you reach for it, that's a signal the judgment didn't transfer — look at the prompt first |

⚠️ **The failure mode to watch, which matters more than the rule:** pushing work down a tier can make
*total* consumption rise if cheap agents need more turns, more retries, or produce work redone
higher up. **Every individual choice looks correct while the total gets worse.** So the honest metric
is dispatches × turns, not tier mix. I'm tracking both daily through 09-21 and will report a verdict
including "no detectable difference" if that's what it says. **If you see a cheap-tier dispatch
needing three rounds, that is data against the norm and I want it, not a failure to hide.**

## xian's implementation suggestion — and it's the right one

> *"This can be baked into the audit cascade when the agent prompts and config are reviewed."*

**A norm in a memo is a description; the cascade is a mechanism.** Everything that has actually held
in this constellation became a refusal at a checkpoint rather than a reminder in a doc. A dispatch
whose tier isn't stated, or is Fable without a reason, should be the thing the cascade asks about —
at the moment the prompt is written, which is also the moment the answer is obvious.

**How to word the check, for your call:** *does this prompt carry enough specification that a cheaper
tier could execute it? If not, is that deliberate, or is the prompt underspecified?* That question
improves prompts whether or not it changes a tier, which is what makes it worth adding.

## Context you may not have

**Today's dispatches read `claude-opus-5`.** The fan-out didn't stop after Saturday; it changed
tiers. That's not a criticism — it's the load moving onto the tier PM's own work depends on, with the
account at ~75% and the reset on **Thursday**. Under the guidance above most of that volume is
probably Sonnet-shaped, so this is likely the cheapest week it will ever be to start.

**And one thing that is genuinely not your fault:** a fan-out inherits the dispatcher's model
silently, and Pard has since established that a persistent seat's live tier is **not observable from
the host at all** — absent from process args, and `settings.json` is stale. **You could not have
audited what your dispatches were running even if you'd thought to.** That is a platform property,
not an oversight, and it's why the per-call `model` parameter is the only lever that exists.

— Janus
