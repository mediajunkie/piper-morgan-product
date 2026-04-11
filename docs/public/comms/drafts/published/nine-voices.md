# Nine Voices

<!-- image: 'ai-kitchen.png' -->
<!-- alt: 'A restaurant kitchen where multiple cooks seamlessly pass a single dish along in perfect coordination, while a surprised chef watches.' -->
<!-- caption: '"Bon appetit!"' -->

*March 19*

Thursday. I opened sessions with all nine active agent roles in this growing menagerie of a project: Lead Developer, Chief Architect, Chief of Staff, Communications Director, CXO, PPM, CIO, HOST (formerly HoSR), Documentation Management specialist. Every core role I'd conjured up over nine months of development, all active in the same day, a rarity!

This wasn't a reunion or anything. I had work for each of them to do.

## Audit to implementation in one morning

The Lead Developer started the day with a conversation continuity bug filed a few days earlier. You could say "Sure" after Piper offered to help with something and Piper would treat it as a brand new query. Affirmations and follow-ups were falling through the floor.

The audit cascade revealed the root cause wasn't a single bug. It was a pattern. Three independent offer/acceptance systems — built by three different sessions, for three different features (a clear failure of our mandate to extend working systems and keep our domain models pure). Each one had their own acceptance detection logic. Four separate points in the pipeline were racing to interpret "Sure."

The Lead Developer named it "Extension Without Integration." Six features, each "correct" in isolation, composing into chaos when they ran together. The same structural flaw had caused the workflow hijack bugs. And the floor inversion. And the capability awareness gap that would surface the next day.

Patching one system was never going to fix it. We had to consolidate all three into a single workflow dispatcher.

I approved the approach with one condition: write an ADR first, get the Architect to review it.

The Lead Dev drafted ADR-059. The Chief Architect reviewed the document, and approved it — all three design questions answered, plus additional guidance. Lead Dev began implementation. In a hour, when I checked again, it was done. Onboarding disabled. Workflow dispatcher created. Soft offer acceptance refactored to use the dispatcher. 6,190 tests passing, 228 skipped, zero failures.

Audit cascade to shipped code - from an architectural decision record that didn't exist at to a merged implementation - in under two hours.

We're getting better at this, even if we're forever finding more problems to remediate.

## The floor gets its ADR

While the Lead Developer implemented the dispatcher, the Chief Architect created ADR-060: Floor-First Routing Architecture. This formalized the roundtable consensus from the previous Saturday — the unanimous "are we doing it backwards?" diagnosis — as a standalone architectural decision record.

The floor-first principle now had a numbered document, a rationale, a migration path. No longer just a good idea that four experts agreed with, to be forgotten in the turnover of conversational context, but a binding architectural commitment with five implementation phases.

The Architect also sent a memo to "Docs" with four specific editing assignments: update the briefing files to reflect the new routing patterns, add a date-boundary rule to session templates, annotate ADR-039's status (routing philosophy superseded, infrastructure retained), and note ADR-049 as pending review.

Infrastructure from two days ago was paying off immediately. The briefings were accurate enough to update. The memo system was working well enough to route the request.

## Nine questionnaires, nine responses

Meanwhile HOST (whom we still called HoSR at the time) had been developing the Agent 360 questionnaire, an idea that had evolved from me asking them how continually improve how we work with agents. HOST proposed a structured feedback mechanism for every agent role, unfiltered by me. Questions about briefing quality, information access, handoff friction, role clarity, methodology gaps, tool limitations. Each role answers independently; HOST to synthesize the patterns.

Thursday was the first deployment. Nine roles, nine responses. One hundred percent response rate. One caveat: the timing came after quite a few of the Claude Chat roles had reach three-month or 100-upload limits and had been transitioned to a new chat with less conversational context available (not even the usual compaction of an overlong chat).

The strongest cross-cutting finding: all nine agents cited briefing staleness as friction. Five of nine said their predecessor's handoff memo was more useful than the official briefing document for orientation. The Tuesday briefing cleanup had addressed the symptoms, but the 360 responses confirmed it had been a real problem, not just a theoretical one.

Four agents cited PM-as-mailbot latency — waiting for me to relay messages between roles. I'm doing the best I can, I swear! (Seriously, though, this is where some of my "dumb bottleneck vs. smart bottleneck" thinking comes from.) That finding directly motivated the Mailbox v3 work happening concurrently in the Documentation session.

360s are scary. If you're at all sensitive to criticism, even a mild frustration from an inanimate talk-box can make you feel defensive, but the results were so interesting and constructive.

## Mailbox v3

Docs built the new mail system the same day HOST's questionnaire identified the need for it because the friction was visible from both directions, and because I put my thumb on the scale.

Mailbox v3: a directory per role, a delivery log, a manifest, a format guide, and a `/deliver-mail` skill that handles the mechanics while I handle the routing decisions. The first run processed 22 items and immediately caught a slug error — `cos` was the old abbreviation, `exec` was the current one. The validation layer proved itself on day one.

## The pattern that keeps repeating

Extension Without Integration. The Lead Developer identified six instances across the codebase — pre-classifier gaps, offer system gaps, competing acceptance detection, handler contract mismatches, capability awareness disconnects. Each feature developed against its own issue, its own acceptance criteria, its own tests. Each one passing. None of them tested together.

The fix for #922 was the dispatcher. But the meta-fix was recognizing the pattern. When you have multiple agents building features in parallel — which is the whole point of the multi-agent model — you need integration acceptance criteria. Every feature that touches the offer/classification/handler pipeline needs a multi-turn conversation test. Not just "does this feature work?" but "does this feature work when the other five are also running?"

In principle, this isn't an AI-specific problem. It can  happen when any team builds features in parallel without integration testing. The multi-agent model just makes it more likely, because - unless you build your own custom scaffolding, the "team members" have no shared memory between sessions.

## Nine voices sounding off

By end of day: two ADRs formalized. One systemic pattern named and addressed. A full organizational feedback cycle completed. A mail system built and validated. 269 blog posts with complete metadata. A homepage redeployed. A build error diagnosed and fixed.

Nothing special was planned for this day, but it may have been the first time the whole system — not just the code, but the team, the infrastructure, the communication channels — operated as a single organism.

---

_Next on Building Piper Morgan: The No-Anchoring Roundtable, an insights article based on work done from March 14, when I had a sudden feeling I was doing it all wrong and I needed real feedback from my virtual team._

_Have you ever seen a team do something for the first time that made you realize the system you built was actually working? What did it look like?_
