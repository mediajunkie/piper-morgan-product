# From Protocol to Infrastructure

For months, we had a rule: after context compaction, check your mailbox.

Context compaction is what happens when a conversation with Claude gets too long. The system summarizes earlier content to make room for new work. It's necessary, but it has a cost — details get lost. Things that were discussed earlier might not survive the summary.

The mailbox rule existed because of this cost. Important information that arrived during a session might vanish during compaction. If you don't check the mailbox after compaction, you might miss something critical that was sent to you earlier.

It was a good rule. We agreed it was important. And my agents kept forgetting to follow it.

## The compliance problem

Rules that depend on memory have a structural weakness: memory fails. Humans forget. AI agents lose context to compaction. The mechanism differs but the outcome is the same — a rule you agreed to follow doesn't fire.

It's not about discipline or caring. My Lead Developer agent cared deeply about checking the mailbox. But after a long implementation session, context compacts, and the agent is picking up where it left off with fresh context — the mailbox check just... doesn't happen. The rule exists. The intention exists. The behavior doesn't.

We tried reminders. We added it to the session protocols. We documented it prominently. Compliance improved, but it never reached reliability.

The rule was right. The enforcement mechanism was wrong.

## The hook that changed everything

We built a small shell script — the session-start hook — that runs automatically before every agent session begins. Four checks, executed without anyone having to remember:

1. **Session log continuity** — find today's log if one exists, so the agent can resume rather than restart
2. **Mailbox check** — count unread messages across all role inboxes
3. **Briefing freshness** — warn if the project's current-state briefing is more than seven days stale
4. **Role identity** — remind the agent which role they're playing in this session

The checks that kept getting forgotten now happen automatically. Not because anyone remembers to do them — because they're infrastructure.

The mailbox rule didn't change. What changed was its enforcement layer. It moved from protocol (something you're supposed to do) to infrastructure (something that happens).

## Protocol vs infrastructure

This distinction matters more than it might seem.

**Protocols** are agreements about behavior. They're documented, discussed, agreed upon. They depend on people remembering and choosing to follow them. They fail when attention lapses, when context shifts, when the pressure of immediate work crowds out the discipline of process.

**Infrastructure** is environment that shapes behavior. It doesn't ask for compliance — it creates conditions where the right thing happens automatically. You don't decide to check the mailbox; the system surfaces unread items before you can proceed.

Protocols require ongoing effort. Infrastructure requires upfront investment but then runs on its own.

## The graduation pattern

Looking back at how Piper Morgan's methodology evolved, I see a pattern:

**Stage 1: Discovery.** We notice a problem. Context gets lost after compaction. Important memos get missed. Something keeps going wrong.

**Stage 2: Protocol.** We create a rule to address it. "Always check mailbox after compaction." The rule works when followed.

**Stage 3: Failure.** The rule isn't followed reliably. Not because people disagree with it, but because protocol compliance is inherently fragile.

**Stage 4: Infrastructure.** We encode the rule into the environment. The check happens automatically. Compliance becomes structural rather than behavioral.

This is methodology graduating to infrastructure. The insight stays the same — checking the mailbox matters. The enforcement mechanism matures from "remember to do this" to "this happens."

## What else could graduate?

Once you see this pattern, you start noticing other protocols waiting for infrastructure:

**"Always run tests before committing"** — This is a protocol for most teams. For teams with pre-commit hooks, it's infrastructure. The graduation is a shell script.

**"Document architectural decisions"** — Protocol: remember to write Architectural Decision Records (ADRs). Infrastructure: templates that prompt for decisions, continuous integration (CI) checks that flag undocumented changes.

**"Review code before merging"** — Protocol: ask someone to review. Infrastructure: branch protection rules that require approval.

**"Check for breaking changes"** — Protocol: think carefully about compatibility. Infrastructure: automated compatibility testing in CI.

Each of these starts as something people agree to do. Each can become something the environment ensures happens.

## The cost of graduation

Infrastructure isn't free. The session-start hook took time to implement. It requires maintenance. It adds complexity to the development environment.

Not every protocol should graduate. Some rules are context-dependent in ways that resist automation. Some are too rare to justify the investment. Some need human judgment that can't be encoded.

The question isn't "can this become infrastructure?" — almost anything can, with enough effort. The question is "should this become infrastructure?" The answer depends on:

- How often does the protocol need to be followed?
- How reliably do people follow it without enforcement?
- How severe are the consequences of non-compliance?
- How complex would the infrastructure be to build and maintain?

For the mailbox check: frequently needed, unreliably followed, consequences were missed information and duplicated work, infrastructure was a simple shell script. Easy graduation.

For something like "make good architectural decisions" — frequently needed, but what would infrastructure even look like? Some things remain protocols because they require judgment that can't be automated.

## The methodology implication

Building Piper Morgan has taught me to think about methodology in two layers:

**The insight layer**: What practices make development better? What should we do?

**The enforcement layer**: How do we ensure the practices actually happen? Protocol or infrastructure?

Early in a project, everything is protocol. You're discovering what works, documenting agreements, building shared understanding. Protocols are fast to create and easy to change.

As practices stabilize, the best ones graduate. The things that matter most, that need to happen reliably, that keep getting forgotten — those become infrastructure. The insight stays the same. The enforcement matures.

The session-start hook isn't a big feature. But it represents something important: methodology that doesn't depend on memory. Rules that enforce themselves. A system that does the right thing automatically, not because anyone decided to do it, but because the environment makes it happen.

That's the graduation worth pursuing.

*Next on Building Piper Morgan: The Log That Fact-Checked Itself.*

*What protocol on your team is waiting to become infrastructure?*
