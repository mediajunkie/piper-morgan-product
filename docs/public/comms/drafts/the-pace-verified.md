---
image:
alt:
caption:
---

# The Pace Verified

*May 2–5, 2026*

The previous Sunday had ended with a milestone closed. The ethics-floor build, the upstream-detector reframe, the simulation-first calibration — all of that had shipped on the prior Wednesday. Friday had been catch-up. The weekend was supposed to be quiet.

On Saturday, Lead Dev opened a single commit that closed four issues at once.

The commit landed the persistent backing for an ethics audit log — the durable storage for what the now-active ethics floor was deciding. Three smaller cluster issues that had been queued as regression targets — a timezone-offset crash, a missing redaction path, a mock-as-list type error — folded into the same atomic commit. Four issues closed, one commit, fifty-eight hours from design ratification to ship.

That was Saturday's headline. The quieter Saturday news was that the audit cascade — a procedural check we'd been running before implementation gameplans — had caught conceptual drift in three of four issues queued for the next major milestone. Decisions from the source documents hadn't been folded back into the issue bodies. The audit pass restructured the queue: a parent epic broken into three children, a sibling pulled out, a relocation to the next sub-epic, a rewrite of one body to fold a decision-doc finding. The next milestone's gameplan gained a conceptual-integrity gate. Catch-and-fold became catch-and-prevent.

That sequence — the cluster-commit, the audit catch, the restructure — was the rehearsal for what Sunday turned out to be.

# The record day

Sunday morning Lead Dev started early and shipped eight implementation issues end-to-end before the day was over.

Each issue followed the same arc — Phase 0 design pass through the audit cascade, walkthrough with me to dispose of any open questions, implementation in a feature branch, tests written alongside, merge to main. Eight times. Two hundred twenty-one new tests added, zero regressions across the seven merges that closed before bed. The eighth shipped late-night against a branch staged for an early Monday merge. The overall test count crossed twelve hundred forty-nine.

Mid-flight the architectural calls came up. One issue's design touched the InsightJournal — the place where the system stored what it learned from each session. Lead Dev surfaced a question about whether to bolt a switchable storage layer onto the existing journal, or rewrite the journal to store things the durable way from the start. The bolt-on was less to migrate. The rewrite matched a design principle the project had been holding — each service does one thing cleanly, rather than hiding a mode-switch inside it. I called the rewrite. Twenty-one test sites moved to a new stand-in, and the journal got rewritten in place.

A second issue surfaced a question about eligibility for one of the new modes — should the eligibility check be channel-aware (in-chat for now, with provisions for other channels later) or channel-agnostic (one decision rule, channel renderers consume the output)? Channel-agnostic. The eligibility check became one decision any channel could read, with each channel responsible only for how it displays the result. Future push channels reuse the same decision and add their own display.

A third issue surfaced a question about whether to filter learnings at compost time (before storage), at surface time (before retrieval), or both. Both — same `safe_surface()` function called at both layers, single source of truth, no surveillance-shape phrasing slipping through either way.

By Sunday night the next major milestone's implementation scope was closed. Three architectural decisions had been made mid-flight that turned out to matter later. One discipline incident — a feature branch's commits landed on local main by accident — got recovered via cherry-pick. The discipline lesson got pinned: verify the branch name after every checkout, not just after the next commit fails.

# The verdict

Monday brought a different kind of verification.

Architect had been working on the project's first sustained workstream review — a multi-day pass across roughly seven hundred commits Lead Dev had landed over the prior three weeks. Independent review, no prior conversation about what to expect, scoped specifically to the question I had been holding privately: was this work as good as it looked?

The answer Architect filed Monday afternoon was yes.

The verdict: structurally sound. Mature domain-modeling discipline. Clean, consistent handling at every point where the AI touches a decision. Test coverage in the high seventies on the code that changed. Five cleanup items surfaced. Five non-blocking. The standout-positive examples named in the review were two pieces Lead Dev had shipped during the prior weeks without any architecture-side hand-holding: a pure-decision-function for a calendar-offer policy ("gold standard" framing in the review), and a transaction-boundary semantic in the audit-log persistence work that Lead Dev had gotten right on the first try without Architect flagging it during build.

The instinct verified by independent review. The right division of labor showed up cleanly. I get to keep the instinct at my seat. The architect contributes the load only the architect can carry. Neither of us has to be in every conversation the other is in.

# Why the pace held

Monday's other story — quieter, but the one that explained the pace — was that the multi-phase shipping pattern showed up first.

Two of Lead Dev's Monday issues were filed as multi-phase from the start. One was a UI restructure with components, partials, and template work that would obviously need to land in stages. The other was the persistence work for a conversation-state object — schema migration in Phase 1, manager rewrite plus call-site rewiring in Phase 2. Phase 1 of each shipped Monday. Phase 2s were queued for Tuesday.

Tuesday told the rest of the story. The conversation-state object's Phase 2 shipped clean — twenty-six call-sites rewired across four files, fully moved over to the durable storage. Then a downstream issue that had been gameplanned at fourteen hours of work shipped in two. The downstream issue had been waiting on the conversation-state object. With the persistence work landed and the call-sites rewired, the downstream issue's implementation was mechanical. The fourteen-hour estimate had been for the version of the issue that included the persistence prep. With the prep done, the issue itself was small.

That's the pattern the multi-phase shipping unlocks. The hard work is the prep — the schema, the persistence, the state machine. Once those land, the downstream issues that depended on them ship at a fraction of their estimate. Eight issues on Sunday, five plus two multi-phase Phase 1s on Monday, three more on Tuesday: a sixteen-issue end-to-end run over three days, with the velocity coming from the prep work that had landed beforehand and unblocked the rest.

# What's portable

It's tempting to read sustained shipping like this as heroic effort, and the rate does sound heroic. It isn't.

The pace came from three things stacked. The audit cascade caught conceptual drift before gameplan, so the gameplans didn't waste hours on issues that needed restructuring. The multi-phase pattern landed the prep work in Phase 1, so downstream issues shipped against work that was already done. And the independent soundness review gave the cohort a defensible answer to "is this work as good as it looks" — letting me stop holding the question privately and the engineering side keep shipping without re-litigating quality at every issue.

None of the three was new that weekend. The audit cascade had landed as a methodology weeks earlier, the multi-phase pattern during the ethics-floor build, the workstream-review cadence over the prior month. What was new was that all three came due at once.

That's the shape worth carrying. Sustained pace isn't a function of effort. It's a function of which preparatory pieces are already in place and ready to pay off together.

---

*Next on Building Piper Morgan: which parts of a role are the irreplaceable ones, and which are the commodity work anyone could do. "Critical vs Commodity Work in a Role," this Saturday.*

*Where in your work has a long-term discipline payoff arrived at the same time as a short-term opportunity to use it? What did it look like when they landed together?*

[FACT-CHECK NOTE for PM: Sources verified against May 2, 3, 4, 5 omnibus logs. Key facts: May 2 — #1018 Phase 2 + 3-issue cluster (#1006/#1007/#1008) closed atomically in single commit `fc79de31`, ~58 hours design-to-ship; m2-structure.md gains conceptual-integrity gate. May 3 — Lead Dev shipped 8 M2d implementation issues end-to-end (#704/#714/#1030/#1031/#1032/#1033/#1034/#1035 — #1032 awaited final merge by EOD), 221 new tests, 0 regressions, 1249/1249 overall pass. PM mid-flight consultations: DDD strict-rewrite for InsightJournal (#1035), channel-agnostic eligibility for Push (#1032), two-layer guardrail for COMPOSTED (#1033). ADR-061 PM verbal ratification recorded. Lead Dev branch-drift incident on #1030 recovered. May 4 — Architect soundness review verdict structurally sound, 5 cleanup items non-blocking; standout examples #790 calendar-offer policy ("gold-standard pure-decision-function") + #1018 transaction-boundary semantic (Lead Dev "got subtle right without Architect flagging during build"); Lead Dev second-day shipping (5 issues end-to-end + multi-phase Phase 1 on #869 + #1052); 12 stale-state M2d retro close. May 5 — Lead Dev third-day shipping (3 issues end-to-end: #1052 Phase 2 + #900 + #869 Phases 2-5+Z); #900 actual ~2h vs ~14h estimate per Apr 30 omnibus Impact #2.]

[SOURCE NEEDED for PM: "the question I had been holding privately: was this work as good as it looked?" — May 4 omnibus says Architect's soundness review answered "the PM-instinct verified" question but doesn't quote the actual question you'd been holding. If your actual phrasing was different, happy to swap. Same applies to the "gold standard" attribution — May 4 omnibus says #790 was named as a "gold-standard pure-decision-function for new policy work" in Architect's review; I'm rendering this as a phrase that could appear in quotes in the post but it's the omnibus's summary of Architect's framing, not the verbatim review text.]
