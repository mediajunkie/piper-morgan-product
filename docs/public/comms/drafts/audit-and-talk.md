---
image:
alt:
caption:
---

# Audit and Talk

*April 17, 2026*

I gave a talk Friday afternoon at the Information Architecture Conference in Philadelphia. The title was *Ethics as Information Architecture*. The premise was that ethics-as-afterthought — content moderation, terms of service, warnings bolted onto a finished system — is the guardrail at the cliff edge, while ethics-as-architecture is the road that doesn't go to the cliff.

At about the same time the talk was starting on the East Coast, the Chief Innovation Officer agent was opening a session on the West Coast and beginning the M1 methodology audit.

I didn't plan for those two things to overlap. They overlapped anyway, and the overlap turned out to be the day's lesson.

# What I was telling the room

The talk had one load-bearing slide. *Structure determines possibility.* That phrase doesn't sound radical to information architects, who have spent careers organizing information so that some actions are possible and others aren't. It does sound radical, apparently, to AI ethics — which still tends to treat ethical behavior as something you check for after the model has already produced an output.

The argument went like this. If you treat ethics as a feature you add at the interface — a content-moderation pass, a refusal template, a warning banner — your protections live in the part of the system that's easiest to circumvent. Anyone with a jailbreak prompt can route around interface-level enforcement. Anyone with sufficient business pressure can quietly weaken it. The architecture itself doesn't care.

But if you put your ethical principles in the *structure* of the system — in how information flows, in what categories of input get routed where, in which contexts can produce which kinds of output — then the unsafe outcomes don't get prevented at the last second by a content filter. They become structurally unreachable. Not prohibited. *Architecturally impossible.*

This is the insight that information architects already understand. The point of the talk was that AI ethics needs to import it.

[CONSIDER: a beat here about how the talk landed in the room — a question, a hand, a moment that suggested the room was meeting the argument rather than just listening to it. Skip if no specific moment is worth lingering on.]

# What the audit was finding

While I was in front of the IAC room, the CIO agent was reading two documents in sequence. The first was the Excellence Flywheel archaeology that Documentation Management had produced the day before — eight distinct formulations of the same idea across nine months, three structural families (a causal loop, an N-pillar checklist, an N-verb mnemonic), plus a Python implementation that matched none of them.

The second was Piper Alpha's reference audit — a survey of which methodology documents had actually been cited in session logs over the audit window. The headline number: of the twenty-two numbered methodology documents in the canonical directory, two had been cited. The other twenty had appeared zero times in 128 session logs across 27 days. The Excellence Flywheel's "mandatory reading" canonical document was one of the silent twenty.

The CIO's audit, when it landed late that afternoon, opened with a sentence that I keep coming back to:

> *The methodology is strong where it matters most: in catching real failures, coordinating multi-agent work, and producing transferable innovations. It is weak where it has always been weak: in maintaining its own documentation.*

And underneath it:

> *The concept is alive. The documentation is dead.*

The audit's first major piece of work was a reformulation of the Excellence Flywheel into three layers. *Concept* — the underlying causal loop where systematic preparation compounds into faster execution which produces higher quality which buys back more capacity for systematic preparation. *Practices* — the actual disciplines we apply, currently five, including a new one named for the day. *Mnemonics* — per-role compact recalls, each citing the canonical practice list rather than paraphrasing it.

The fifth practice — the new one — is *audit the composition*. It's the formalized version of [Pattern-062 (the Assembly Assumption)](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/current/patterns/pattern-062-assembly-assumption.md): individually-correct components composing into collectively-incomplete outcomes. The pattern had been operational for months. The audit promoted it from pattern to practice.

# What I noticed when both things had happened

The talk's argument was: principles that live only in the interface layer are fragile. Principles that live in the architecture are durable.

The audit's finding was: principles that live only in the documentation layer are fragile. Principles that live in the actual practice — the mailbox protocols, the handoff memos, the gate methodology, the omnibus synthesis discipline — are durable.

[ADD PERSONAL ANECDOTE: a moment where the resonance hit you — maybe reading the audit on the train back from Philadelphia, or the next morning, or in the conversation with CIO that followed. The beat where you noticed the talk and the audit were arguing the same point at different layers.]

That's the same argument. I just hadn't expected to see it twice in one day, once aimed outward at a conference room and once aimed inward at our own methodology.

The Excellence Flywheel was alive in practice (we were running it constantly — every gate review, every audit, every "verify before building" callback) and dead in documentation (the canonical doc had drifted into eight different shapes nobody read). The methodology was operating exactly the way the talk argued ethics should operate: structurally, not as a layer you check against. That's why it worked. And it worked even though the formal documentation had decayed.

But the documentation decay isn't trivial either. Eight formulations means eight slightly different things being said when someone tries to import the concept somewhere else. Documentation is how a structural principle gets *transferred* to a new context — to a new team, a new project, a new role. Documentation that has drifted is documentation that mis-transmits. The architecture survives in the place where it was built; the principle dilutes when it tries to travel.

# The two halves of the same job

So here's where I landed by the end of the day.

If you want a principle to be durable in the system you're working on right now, put it in the architecture. The methodology has been doing this correctly: the gate methodology, the mailbox protocols, the handoff memo template are all structural, and they survive sessions and migrations and personnel changes because they're *load-bearing*, not advisory.

If you want a principle to *travel* — to land in another context with its meaning intact — you also have to maintain its documentation. The talk traveled to a room of two hundred information architects. The Flywheel had been failing to travel because its documentation had eight different shapes.

Both halves of the job. The architecture for durability. The documentation for portability. The audit had found us doing one well and the other badly, and the reformulation that came out of it was an attempt to do both at once: keep the practice operational, *and* fix the doc so the practice could actually be exported.

[CONSIDER: a closing reflection here about how the IAC talk and the methodology audit landing on the same Friday wasn't coincidence so much as it was both responding to the same underlying question — what makes a principle durable across change? — from different angles. Mind the anti-manifesto guardrail; this is an observation, not a thesis.]

I caught the train back to DC that evening. The Flywheel reformulation was in my inbox before I'd unpacked.

---

*Next on Building Piper Morgan: Same Failure, Six Agents, Ninety Minutes — what happened the Sunday after, when six leadership agents made the same source-discipline mistake within a ten-minute window.*

*Where in your work is the principle alive in practice but dead in documentation? And — separately — where is the documentation pristine but the principle never actually applied?*
