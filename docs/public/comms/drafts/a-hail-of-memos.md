---
image: ai-hailstorm.png
alt: Figure at center of a radial storm of incoming message-slips, struggling to catch them while working.
caption: "Let me get back to you on that!"
---

# A Hail of Memos

*April 16, 2026*

By the end of the day on Thursday, the project had moved twenty-eight commits and at least thirty-seven inter-agent memos across nine sessions spanning ten roles.

But those are just numbers. Plus, why?

# What kind of day it was

The morning opened at 6:38am with the Lead Developer delegating a linter audit to a subagent. Back when we had almost no guardrails, hooks that cleaned up the code formatting were state of art, but over time they became both a friction point and something of a scofflaw.

Twenty minutes later, the subagent reported back: the recurring culprit wasn't actually the pre-commit hooks themselves, but a combination of format-on-save plus auto-import silently reverting intentional cleanups, causing endless loops.

The recommendation: collapse black, isort, and flake8 into a single ruff hook. By 7:05 AM the consolidation had shipped, seventy-four files reformatted, lint passing on 1,368 files. Issue closed before breakfast.

Lint for breakfast, yum.

# Meanwhile, in the design realm...

The CXO opened their own session at 6:49 AM and walked into two memos already waiting. The first was Lead Dev's #950 direction check — the floor prompt rewrite needed CXO sign-off on Five Pillars, Grammar, and a half-dozen sub-questions before implementation could begin. The second was Piper Alpha's cross-pollination routing memo. CXO answered #950 inside an hour: *Five Pillars are canonical (Identity, Time, Space, Agency, Prediction). Grammar is "Entities experience Moments in Places." Approach is EVOLVE, not rewrite. And — separately — there's a paraphrase of [PDR-004](https://pmorgan.tech/internal/product/pdr/PDR-004-experience-philosophy) in last month's omnibus log that needs correcting; please ask Docs to issue the correction.*

That last item is its own story, threaded through the whole day. The CXO had spotted, while reading prior context to answer the #950 questions, that the omnibus log for Mar 22 had paraphrased one of PDR-004's principles in a way that flattened the original meaning. Docs picked up the correction within fifteen minutes, traced the propagation (seven affected files, two of which were live published blog posts), wrote a five-item process-safeguarding plan back to CXO, and sent a separate memo to Comms with the rewrite spec. Comms returned narrative rewrites for all three affected passages by late afternoon.

*Meta-observation: The same morning Docs fixed the artifacts, they also added a mandatory canonical-verification step to the create-omnibus skill so the same paraphrase drift can't slip past synthesis again. The fix and the methodology change were one motion.*

# Meanwhile, over in product land...

While the PDR-004 chain was unspooling, Piper Alpha was reading four days of cross-pollination briefs and routing the actionable insights to Architect, Lead Dev, and PPM. PA caught a vocabulary import error mid-routing: a phrase imported from the Klatch project ("passed through") had been about to be reframed onto the PM BYOC narrative, and the mechanisms underneath the two phrases were not actually the same. PA retracted the reframe before sending. The remaining insight — a methodology pattern about explicit `known_pathological` tagging in test corpora — survived as genuinely portable. PPM endorsed it later that afternoon.

Documentation Management ("Docs"), in parallel, ran the Excellence Flywheel archaeology subagent to its conclusion: eight distinct formulations of the same idea across three structural families, dating back to July 2025. The archaeology landed at CIO's door before five o'clock; the CIO read it inside an hour, made five structural decisions about the reformulation, and combined the audit with the methodology audit it had been blocking. Three workstreams collapsed into one deliverable.

Lead Developer, meanwhile, kept shipping. By 11:49 AM #951 had wired calendar and deadline context into the floor. By 11:52 AM #950 iteration one was committed. By 12:10 PM Gemini was wired as a real primary/fallback provider. By 2:30 PM #950 iteration two had landed with quality at 72.1% on the canonical retest, up from the iteration-one baseline. By 3:36 PM the M2b and M2c gates had closed.

Comms — in another session, in another window — was at the same time filling an eleven-day gap in the building narrative arc, adding two new bridging pieces and two new insights that connected pieces already drafted but not yet published.

HOST (Head of Sapient Trust) checked in at 4:56 PM (after a six-day gap since the previous health check) and assessed twelve roles, finding `team-structure.md` 103 days stale as the worst finding of the audit.

The Architect responded to PA's cross-pollination memo at 4:15 PM: *adopt the AAXT [automated agent-experience testing] failure-mode vocabulary, build five-to-ten fabrication probes across the absence categories, sparkline test holds for M5.* CXO, having delivered #950 approval, the PDR-004 correction trigger, and the ethics-denial voice guidance memo, closed the day at five o'clock with nine deliverables behind it — the most productive CXO day on record.

The PPM closed at 5:10 PM with one memo to Lead Dev and one acknowledgment.

The CIO closed somewhere around 6:45 PM with a Flywheel reformulation queued and an audit scope set.

Docs did the last mail sweep at 6:48 PM, three follow-up issues filed.

# What went on in all that mail

This sounds like a productive day, and it was. But it's also worth noticing what the volume *had to do* to happen.

Almost all of those thirty-seven-plus memos crossed me.

Some of the agents were running in Claude Chat, others in Claude Code. Chat agents write to a project-knowledge surface that Code agents can't see; Code agents write to a filesystem that Chat agents can't read. Between them, *I* was the postal service. Every CXO memo to Docs got copied across by hand. Every PA routing memo to Architect got carried over by hand. Every Lead Dev question for CXO went out manually; every CXO answer came back manually. The Excellence Flywheel archaeology had to be ferried twice (the first delivery was the wrong file).

It feels strange to know I am doing critical work while being the dumbest bottleneck of them all.

The thing about a hand-carried mail system is that it works fine until it doesn't. A morning where the carrier is also at a conference, also taking phone calls, also writing the Apr 22 Ship draft — the carrier becomes the bottleneck. Twenty-eight commits get through. Thirty-seven memos get through. The day gets done.

But it gets done by routing every coordination through one node, and that node is *also* trying to be the product manager. Which means the coordination cost is invisible until you start noticing how much of your day is the carrying.

# What was about to change

Thursdays like this one don't happen every week. This thirty-seven-memo day occurred at the junction of a sprint-gate closing, a methodology audit kicking off, a blog post to manage, a paraphrase correction propagating across two months of artifacts, and a cross-pollination cycle catching its first vocabulary error all at once. Most weeks have one of these. This week had several, and they all surfaced on the same day.

I am wondering now *which kinds of coordination scale through hand-routing, and which ones need a different shape.* I've been thinking about that question for a while. I just hadn't been ready to act on it.

That's a story for another post.

---

*Next on Building Piper Morgan: Audit and Talk — what happened the day after, when an industry talk and a methodology audit converged on the same Friday afternoon.*

*What's the largest coordination day your team has ever pulled off? When did you notice the bottleneck was you?*
