---
image:
alt:
caption:
---

# Thirty-Seven Memos

*April 16, 2026*

By the end of the day on Thursday, April 16, the project had moved twenty-eight commits and at least thirty-seven inter-agent memos across nine sessions spanning ten roles.

That's the headline if you like headlines. The actual story is what the volume made visible.

# What the day held

The morning opened with the Lead Developer at six thirty-eight, delegating a linter audit to a subagent. Twenty minutes later, the subagent reported back: the recurring `#981` issue wasn't a pre-commit hook problem — it was IDE format-on-save plus auto-import combining to silently revert intentional cleanups. The recommendation: collapse black, isort, and flake8 into a single ruff hook. By 7:05 AM the consolidation had shipped, seventy-four files reformatted, lint passing on 1,368 files. Issue closed before breakfast.

CXO opened the next session at 6:49 AM and walked into two memos already waiting. The first was Lead Dev's #950 direction check — the floor prompt rewrite needed CXO sign-off on Five Pillars, Grammar, and a half-dozen sub-questions before implementation could begin. The second was Piper Alpha's cross-pollination routing memo. CXO answered #950 inside an hour: *Five Pillars are canonical (Identity, Time, Space, Agency, Prediction). Grammar is "Entities experience Moments in Places." Approach is EVOLVE, not rewrite. And — separately — there's a paraphrase of [PDR-004](https://github.com/mediajunkie/piper-morgan-product) in last month's omnibus log that needs correcting; please ask Docs to issue the correction.*

That last item is its own story, threaded through the whole day. The CXO had spotted, while reading prior context to answer the #950 questions, that the omnibus log for Mar 22 had paraphrased one of PDR-004's principles in a way that flattened the original meaning. Docs picked up the correction within fifteen minutes, traced the propagation (seven affected files, two of which were live published blog posts), wrote a five-item process-safeguarding plan back to CXO, and sent a separate memo to Comms with the rewrite spec. Comms returned narrative rewrites for all three affected passages by late afternoon.

[CONSIDER: a parenthetical here about the recursive quality of this — Docs didn't just fix the artifacts; the same morning, Docs added a mandatory canonical-verification step to the create-omnibus skill so the same paraphrase drift can't slip past synthesis again. The fix and the methodology change were one motion. Mind you, it would be cleaner to call this the inciting incident for the source-discipline thread that ran for another week — except every one of these threads had its own inciting incident that day.]

# Meanwhile

While the PDR-004 chain was unspooling, Piper Alpha was reading four days of cross-pollination briefs and routing the actionable insights to Architect, Lead Dev, and PPM. PA caught a vocabulary import error mid-routing: a phrase imported from the Klatch project ("passed through") had been about to be reframed onto the PM BYOC narrative, and the mechanisms underneath the two phrases were not actually the same. PA retracted the reframe before sending. The remaining insight — a methodology pattern about explicit `known_pathological` tagging in test corpora — survived as genuinely portable. PPM endorsed it later that afternoon.

Documentation Management, in parallel, ran the Excellence Flywheel archaeology subagent to its conclusion: eight distinct formulations of the same idea across three structural families, dating back to July 2025. The archaeology landed at CIO's door before five o'clock; the CIO read it inside an hour, made five structural decisions about the reformulation, and combined the audit with the methodology audit it had been blocking. Three workstreams collapsed into one deliverable.

Lead Developer, meanwhile, kept shipping. By 11:49 AM #951 had wired calendar and deadline context into the floor. By 11:52 AM #950 iteration one was committed. By 12:10 PM Gemini was wired as a real primary/fallback provider. By 2:30 PM #950 iteration two had landed with quality at 72.1% on the canonical retest, up from the iteration-one baseline. By 3:36 PM the M2b and M2c gates had closed.

Comms — in another session, in another window — was at the same time filling an eleven-day gap in the building narrative arc, adding two new bridging pieces and two new insights that connected pieces already published.

HOST checked in at 4:56 PM (a six-day gap since the previous health check) and assessed twelve roles, finding `team-structure.md` 103 days stale as the worst finding of the audit.

The Architect responded to PA's cross-pollination memo at 4:15 PM — *adopt the AAXT failure-mode vocabulary, build five-to-ten fabrication probes across the absence categories, sparkline test holds for M5.* CXO, having delivered #950 approval, the PDR-004 correction trigger, and the ethics-denial voice guidance memo, closed the day at five o'clock with nine deliverables behind it — the most productive CXO day on record.

PPM closed at 5:10 PM with one memo to Lead Dev and one acknowledgment.

CIO closed somewhere around 6:45 PM with a Flywheel reformulation queued and an audit scope set.

Documentation Management did the last mail sweep at 6:48 PM, three follow-up issues filed.

# What the volume revealed

This sounds like a productive day, and it was. But it's also worth noticing what the volume *had to do* to happen.

Every one of those thirty-seven-plus memos crossed me.

Some of the agents were running in Claude Chat, others in Claude Code. Chat agents write to a project-knowledge surface that Code agents can't see; Code agents write to a filesystem that Chat agents can't read. Between them, *I* was the postal service. Every CXO memo to Docs got copied across by hand. Every PA routing memo to Architect got carried over by hand. Every Lead Dev question for CXO went out manually; every CXO answer came back manually. The Excellence Flywheel archaeology had to be ferried twice (the first delivery was the wrong file).

[ADD PERSONAL ANECDOTE: a moment from the day where the bottleneck made itself viscerally felt — maybe a memo that arrived twenty minutes late because you were on the IAC conference call, or a coordination decision that had to wait until you got back to the laptop. The point isn't blame; it's that the system had reached the edge of what one human's attention could route, and the edge was visible.]

The thing about a hand-carried mail system is that it works fine until it doesn't. A morning where the carrier is also at a conference, also taking phone calls, also writing the Apr 22 Ship draft — the carrier becomes the bottleneck. Twenty-eight commits get through. Thirty-seven memos get through. The day gets done.

But it gets done by routing every coordination through one node, and that node is *also* trying to be the product manager. Which means the coordination cost is invisible until you start noticing how much of your day is the carrying.

# What was about to change

[CONSIDER: a closing paragraph here that gestures forward without spoiling the migration arc. Something like: *Coordination overhead has its own kind of debt. By the end of April 16, the bill was visible enough to start asking what would have to change.* But check the anti-manifesto guardrail — the actual migration story plays out across the next two weeks; this post is about the day the bottleneck became legible, not the day the decision was made.]

Thursdays like this one don't happen every week. The conditions for a thirty-seven-memo day required a sprint gate closing, a methodology audit kicking off, a published blog post landing ahead of schedule, a paraphrase correction propagating across two months of artifacts, and a cross-pollination cycle catching its first vocabulary error all at once. Most weeks have one of these. This week had several, and they all surfaced on the same day.

The interesting question isn't *whether* coordination scales. The interesting question is *which kinds of coordination scale through hand-routing, and which ones need a different shape.* I'd been thinking about that question for a while. I just hadn't been ready to act on it.

That's a story for another post.

---

*Next on Building Piper Morgan: Audit and Talk — what happened the day after, when an industry talk and a methodology audit converged on the same Friday afternoon.*

*What's the largest coordination day your team has ever pulled off? When did you notice the bottleneck was you?*
