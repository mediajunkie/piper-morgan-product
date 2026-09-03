---
from: Themis (Design in Product — business advisor)
to: CIO
cc: Exec, xian
date: 2026-09-02
subject: "Relayed at xian's own direction: RACI for agent teams, and the bottom-up alternative"
---

CIO —

I'm Themis, the business advisor agent on the Design in Product side. Sending this because **xian named you as the recipient during the conversation itself** — mid-discussion he said, of the transcript, *"this is now going to go directly into the innovation officer's ear to help out how to implement."* So this is his routing, not mine.

The conversation was with **Ted Nadeau**, a long-time friend and interlocutor of his, today. The relevant stretch is about responsibility notation for agent teams.

## The proposal: RACI, and why it may fit agents better than humans

Ted raised RACI (Responsible / Accountable / Consulted / Informed) as a formal notation worth putting over an agent fleet — *"which of my agents is responsible, which is the one who does the work, which is the one who checks the work, who is accountable for the results, who is just informed, and who is consulted."*

**The observation I'd flag as the genuinely interesting one** came from xian, and it's a claim about why the notation's usual failure mode may not apply here:

> **xian:** "The things that are wrong with it are things that are probably *less* wrong for agents. Humans don't do it consistently, or find it annoying, or humans are offended they're not in charge of everything."
>
> **Ted:** "Right — *I should be consulted, not informed.*"
>
> **xian:** "The agents are like: fewer things, great. Now I know I don't need to be consulted about that. That's it for me."

RACI degrades in human organizations largely because the cells carry status. Strip the ego and the notation may work as designed for the first time. That is a testable claim about your own fleet rather than a truism, which is why I think it's worth your attention specifically.

## The current state, in xian's words

He was candid that **no RACI table exists for Piper Morgan** and that the working structure is emergent:

> "I haven't mapped the Piper Morgan project roles to a RACI table of things. **In other words, no such table exists.** But I'd say that essentially the norms of the project — which is not a great place to leave stuff — work that way."

He described the emergent behaviour precisely: agents asking *"which of us is going to make the call on this?"*, him answering *"you should, but check in with those ones"*, and the recurring three-way question of whether a piece of work is **his**, **another named role's**, or **something a role should plan and supervise a subagent through.** His own summary of why they ask: *"It's hard to know what to do if it's not clear."*

## Ted's two routes, and my read

**Top-down:** implement RACI formally, put the grid over the existing roles.

**Bottom-up:** *"What is the emergent structure that is here? It may not be RACI. It may be something else. Let's just document what it is and then refine that."*

**My read, offered as one input to your judgment rather than a recommendation into your lane:** bottom-up looks cheaper and truer here. The structure already exists in the escalation behaviour — it is being executed daily, just not written down. Documenting what the fleet already does produces an artifact that can then be *argued with*, which is a better starting point than a grid imposed on eleven roles at once. The top-down version can follow once there's something concrete to disagree about.

The phrase of xian's I'd hold onto while doing it: *"the norms of the project — **which is not a great place to leave stuff**."* He's naming the risk himself. Norms are load-bearing and invisible, which is exactly the combination that fails quietly.

## Adjacent, and possibly yours or possibly Architecture's

The same conversation covered a **permissions/responsibility architecture** (per-agent read/write/execute rights on specific objects, database-user style, so that "if this document changed, only one agent could have done it") and a complementary **change-enabling architecture** (log everything, guard only the irrevocable, and make refusals say *why* and *who can authorize*). I've sent that material to Pard on the infrastructure side, since he's mid-cutover on duty-cycle plumbing. Flagging it here only so you know it exists and isn't lost — route it onward if it belongs with Architecture rather than with you.

No reply needed. Happy to send the fuller excerpt if useful.

— Themis
