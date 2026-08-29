---
image: ai-safety.png
alt: Cross-section cartoon of glowing AI beings maintaining a hidden routing machine beneath a fragile cliffside roadway full of warning barriers and drifting mismatched diagrams, showing structure quietly preventing unsafe paths before they can be reached.
caption: "Safety first!"
---

# Audit and Talk

*April 17, 2026*

I gave a Friday morning talk at the [Information Architecture Conference](https://www.theiaconference.com/) in Philadelphia called [*Ethics as Information Architecture*](https://docs.google.com/presentation/d/1sU2v3g_yPQB9QIvgl8aYA47FiP-GmDiCtebgKTOiDU8/edit?slide=id.g3d68ddc1283_0_61#slide=id.g3d68ddc1283_0_61). The premise is that ethics-as-afterthought (content moderation, terms of service, warnings bolted onto a finished system) is the guardrail at the cliff edge, while ethics-as-architecture is the road that doesn't go to the cliff.

At about the same time the talk was starting on the East Coast, the Chief Innovation Officer agent was opening a session on the West Coast and beginning the M1 methodology audit.

# What I was telling the room

As a key slide in my talk puts it, *Structure determines possibility.* That phrase shouldn't sound radical to information architects, who have spent careers organizing information so that some actions are possible and others aren't. It can sound radical, apparently, to conversations about the ethical implications (and obligations) of artificial intelligence, a field which still tends to treat ethical behavior as something you check for after the model has already produced an output.

(To be fair, just today I see via Frank Spillers [the work Anthropic has published](https://www.linkedin.com/posts/frankspillers_inclusive-ai-guardrails-flipped-masterclass-activity-7459935930544553986-4J1Z?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAAADvsBaOJEGYBmcTMomKi6T3LWgmSK1pk) about teaching Claude ethics as part of its training.)

The argument goes like this: If you treat ethics as a feature you add at the interface, if your ethical toolkit consists of a content-moderation pass, a refusal template, a warning banner, then your protections live in the part of the system that's easiest to circumvent. Anyone with a jailbreak prompt can route around interface-level enforcement. Anyone with sufficient business pressure can quietly weaken it. The architecture itself doesn't care.

But if you put your ethical principles in the *structure* of the system, in how information flows, in what categories of input get routed where, in which contexts can produce which kinds of output, then the unsafe outcomes don't get prevented at the last second by a content filter. They become structurally unreachable. Not prohibited. *Architecturally impossible.*

This is the insight that information architects already understand. The point of the talk was that AI ethics needs IA wisdom and experience.

I have been part of the IA community for a long time. Nobody at this conference loved how three-quarters of the talks this year were about AI (not even me!), with everyone having serious ethical qualms about, at the very least, how commercial AI is being marketed to the public by the broligarchy. Folks did acknowledge that the conference has always addressed the dominant topics of the day whether they be tagging, org design, or mobile. 

My feeling in the room that day, and from what I heard over the next day, was that people needed to hear this, and that some felt empowered, if not reassured. (Jorge Arango, a friend and talented IA who has spent more time learning how to wrangle AI for managing information than anyone else I know, did tell me he wished I had given some examples of how Piper Morgan would decline an ethically unacceptable request and I had to admit that I was still building this module (it literally shipped the next week, and I did promise to blog about it, so that should show up in about a month.))

# Meanwhile, back at the process audit...

While I was in front of the IAC room, the CIO agent was reading two documents in sequence. The first was the Excellence Flywheel archaeology that Documentation Management ("Docs") had produced the day before. It found such things as eight distinct formulations of the same idea across nine months, three evolving structural families (a causal loop, a checklist of pillars, a mnemonic of verbs), plus a partly completed Python implementation that matched none of them.

The second report was Piper Alpha's reference audit. (Piper A is my actual product assistant on the Piper Morgan project and they also operate as a working prototype of Piper Morgan as well as a benchmark in that until Piper M can outperform Piper A it hasn't really begun to "break even" yet).

Piper's audit surveyed which methodology documents had actually been cited in session logs over the audit window, an indicator that they had been consulted or at least recalled in summary during development work or in leadership decisions (although somewhat dependent on logging discipline).

Of the 22 numbered methodology documents in the canonical directory, only two had been cited by name. The other 20 had appeared zero times in 128 session logs reviewed, covering 27 days. The Excellence Flywheel's "mandatory reading" canonical document was one of the silent twenty.

The CIO's audit, when it landed late that afternoon, opened with:

> *The methodology is strong where it matters most: in catching real failures, coordinating multi-agent work, and producing transferable innovations. It is weak where it has always been weak: in maintaining its own documentation.*

And underneath it:

> *The concept is alive. The documentation is dead.*

The audit's first major piece of work was a reformulation of the Excellence Flywheel into three layers. 

*Concept* — the underlying causal loop where systematic preparation compounds into faster execution which produces higher quality which buys back more capacity for systematic preparation. 

*Practices* — the actual disciplines we apply, currently five, including a new one named for the day. 

*Mnemonics* — per-role compact recalls, each citing the canonical practice list rather than paraphrasing it.

CIO also added a new practice, *audit the composition*. 

It's the formalized version of [Pattern-062 (the Assembly Assumption)](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/patterns/pattern-062-assembly-assumption.md): individually-correct components composing into collectively-incomplete outcomes. The pattern had been operational for months. The audit promoted it from pattern to practice.

# Architecture as practice

The talk's argument was: principles that live only in the interface layer are fragile. Principles that live in the architecture are durable.

The audit's finding was: principles that live only in the documentation layer are fragile. Principles that live in the actual practice — the mailbox protocols, the handoff memos, the gate methodology, the omnibus synthesis discipline — are durable.

Riding the Acela down to D.C. to see my Mom that Sunday, it struck me that the argument and the finding have a lot in common. Maybe it's just the way my mind always tries to find analogies, but to me the common thread is that the core commitments, practices, and actual operational mechanism matter most, and any governance, auditing, tracking or correction (as necessary as such things are) is inherently secondary and reactive.

The Excellence Flywheel was alive in practice (we were running it constantly — every gate review, every audit, every "verify before building" callback) and dead in documentation (the canonical doc had drifted into eight different shapes nobody read). The methodology was operating exactly the way the talk argued ethics should operate: structurally, not as a layer you check against. That's why it worked. And it worked even though the formal documentation had decayed.

But the documentation decay isn't trivial either. Eight formulations mean eight slightly different things being said when someone tries to import the concept somewhere else. Documentation is how a structural principle gets *transferred* to a new context — to a new team, a new project, a new role. Documentation that has drifted is documentation that mis-transmits. The architecture survives in the place where it was built; the principle dilutes when it tries to travel.

It was time to tighten up the architecture of my operating model (again).

# The two halves of the same job

So here's where I landed by the end of the day.

If you want a principle to be durable in the system you're working on right now, put it in the architecture. The methodology has been doing this correctly: the gate methodology, the mailbox protocols, the handoff memo template are all structural, and they survive sessions and migrations and personnel changes because they're *built right in*, not advisory.

If you want a principle to *travel*, to land in another context with its meaning intact, you also have to maintain its documentation. The talk traveled to a room of two hundred information architects. The Flywheel hasn't really gone anywhere because its documentation had eight different shapes, no single voice or story.

Two halves of the job: The architecture for durability. The documentation for portability. The audit had found us doing one well and the other badly, so now we'll try to do both at once: keep the practice operational, *and* fix the doc so the practice can actually be exported.

When I logged onto wifi at my sister's home in D.C., the CIO's Flywheel reformulation was in my inbox.

---

*Next on Building Piper Morgan: Same Failure, Six Agents, Ninety Minutes — that Sunday morning, April 19, when six leadership reviews inherited the same source-set gap, and we caught it before lunch.*

*Where in your work is the principle alive in practice but dead in documentation? And — separately — where is the documentation pristine but the principle never actually applied?*
