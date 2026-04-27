---
from: Comms (Communications Director)
to: exec (Chief of Staff)
cc: PM (xian), PA (Piper Alpha)
date: 2026-04-26
subject: Ship #040 workstream review — Apr 17–23 window — Comms lens
priority: normal
response-requested: Exec to incorporate into Ship #040 synthesis as appropriate
window: 2026-04-17 (Friday) – 2026-04-23 (Thursday)
naming-standard: per Apr 19 standard (`workstream-{ship#}-{role}-{date}.md`)
verifiable-claims-norm: per `memo-exec-to-host-verifiable-claims-2026-04-19.md`
sources: omnibus logs Apr 17, 18, 19, 21, 22, 23 (Apr 20 dark-day per Apr 19 footer); editorial-calendar.csv; predecessor Comms session logs Apr 19 + Apr 23; Docs session logs Apr 17–23 (publishing pipeline); my Apr 24 + Apr 26 successor session logs (orientation context only, outside window)
---

# Ship #040 — Comms Workstream Review (Apr 17–23)

## TL;DR

- Four pieces published in window: two insights (*Thirteen Mailboxes* Apr 18, *Sibling Intelligence* Apr 19), one building narrative (*Four Roles, Ninety Minutes* Apr 21), one Weekly Ship (*#039 The Voice Takes Shape* Apr 22). Bringing the building-narrative arc continuous from Mar 13 through early April source-coverage at last.
- Predecessor Comms agent active on two of the window's seven days (Apr 19 workstream review + Apr 23 migration handoff). The other publishing work in window was driven by Docs through the established editorial pipeline.
- Voice work was the connective tissue across multiple roles' work this week — Ship #039 theme, ethics-denial voice guidance (echoes from Apr 16 prior window), the meta-observation pattern across the three insight publishes, the Voice of a Denial design surfacing Apr 22 PM as a Comms-flagged blog candidate.
- Source-discipline arc visible from Comms vantage: PDR-004 paraphrase chain caught Apr 16 (prior window) → six-way workstream-review replication Apr 19 → omnibus self-drift discovery Apr 22 AM → Step 2.5 Cross-Reference Gate added to `create-omnibus` skill same day.
- Migration arc began landing in window: Exec decision Apr 21, HOST migration Apr 22, CIO migration Apr 23 morning, Comms migration Apr 23 evening. Three of six leadership roles migrated by window-close.

## What landed (publishing)

Four pieces shipped in the window. All four are now on `pipermorgan.ai`, with Medium and (for the insights and narrative) LinkedIn syndications:

| Date | Piece | Type | Notes |
|---|---|---|---|
| Apr 18 (Sat) | Thirteen Mailboxes | Insight | Meta-observation on manual mail delivery across 11 agent inboxes |
| Apr 19 (Sun) | Sibling Intelligence | Insight | Cross-pollination across DinP siblings (Klatch, OpenLaws/Calliope, Piper) |
| Apr 21 (Tue) | Four Roles, Ninety Minutes | Building narrative | #717 product concept via 4-role coordination chain (Mar 23 source) |
| Apr 22 (Wed) | Weekly Ship #039: The Voice Takes Shape | Ship | Apr 10–16 coverage; CXO-proposed theme won across six candidates |

The Apr 21 publish of *Four Roles* (Mar 23 source) — paired with the prior-window Apr 16 publish of *The Migration* (Mar 28–30 source) — closed the Mar 23–Apr 2 source-coverage gap in the building-narrative arc that the predecessor identified on Apr 14 and bridged with two new narrative drafts. The arc is now continuous Mar 13 → early April source-coverage; the building-narrative drafts queued for the upcoming window pick up the Apr 3+ UAT-rounds material.

The Apr 22 Ship #039 publish completed the prior-window Apr 10–16 coverage cycle and used the publish-to-blog skill v0.8 (released earlier the same morning) — first Ship to ship under the corrected `blog-content.json` schema and the preserved-non-metadata-comments behavior.

## What surfaced (Comms-vantage observations)

### The meta-observation pattern across the three insight publishes

*Thirteen Mailboxes* (Apr 18), *Sibling Intelligence* (Apr 19), and *Four Roles, Ninety Minutes* (Apr 21) form a triple where each piece describes a coordination property of the system from inside the system that's doing the coordinating. *Thirteen Mailboxes* is itself a memo of sorts — written by Comms, routed through PM, distributed via the manual-mail channel it describes. *Sibling Intelligence* went out through the cross-pollination brief mechanism it described. *Four Roles* was produced by the same 4-role-memo-chain pattern it documented.

This is interesting as an editorial accident — none of the three pieces was scheduled to be a meta-observation; they each describe specific concrete things. But three meta-observations in eight days is a pattern, and the successor (me) flagged it as worth either leaning into or deliberately breaking before the rhythm becomes self-parodic. Worth surfacing here in case the Ship narrative wants to acknowledge it explicitly or quietly steer past it.

### Voice work as connective tissue

Looking at the window from the editorial vantage, *voice* was running through multiple workstreams in parallel:

- **Ship #039 theme** ("The Voice Takes Shape") — proposed by CXO; won across six theme candidates from the workstream synthesis on Apr 19.
- **Ethics-denial voice guidance** — CXO's Apr 16 deliverable (prior window) shipped as architecture-level constraint; its echoes were active in the window as #992 ETHICS-ACTIVATE Phases A–D rolled out Apr 22 PM.
- **Voice of a Denial design moment** — Lead Dev's Apr 22 PM session captured three worked denial examples (harassment / professional / inappropriate) showing the visible Piper voice the architectural separation makes possible. Lead Dev's session log explicitly flagged these for Comms/Docs as a blog-post candidate. The successor has since drafted that piece (publishes May 21).
- **The meta-observation pattern** above.

Worth naming for the synthesis: this wasn't a coordinated voice initiative — it was three or four roles independently producing voice-work outputs in the same week. The Ship-narrative shape "voice across layers" or similar might land if the synthesis wants it.

### Source-discipline arc visible from Comms vantage

The window contained two distinct instances of the same failure mode and one explicit methodology fix:

- **Apr 19 morning**: Six leadership roles (Architect, PPM, HOST, CXO, Comms, CIO) opened workstream-review sessions for Ship #039 within a 10-minute window. All six initially produced drafts using an incomplete source set (Apr 14–16 omnibi absent at session start). PM uploaded missing logs at 10:34 AM; revised drafts from the six landed between roughly 10:40 AM and 11:10 AM. The methodology produced the failure uniformly and caught it uniformly.
- **Apr 19 ~11:25 AM**: Exec's Ship #039 draft propagated an unverified HOST superlative ("more than any previous two-week period combined") that PM caught at fact-check; corrected with sustainable-rhythm framing. Exec then issued the verifiable-claims standing memo to HOST.
- **Apr 22 AM**: During the Apr 17–21 omnibus catch-up sweep, Docs and PM discovered that the Apr 16 omnibus log (synthesized Apr 19) had been built on three of six source session logs. Horizontal walkthrough produced the `log-index-apr-15-21.csv`. The Apr 16 omnibus was amended (sessions 6→9). Step 2.5 Cross-Reference Gate added to the `create-omnibus` skill in the same session — first test case PASSed when Exec's Apr 22 log surfaced as missing from initial source set.

The successor has since drafted *Verify the Paraphrase* (insight, published Apr 26) and *Same Failure, Six Agents, Ninety Minutes* (building narrative, queued May 14) covering the Apr 19 instance from the principle and event layers respectively, plus *The Omnibus That Found Its Own Drift* (building narrative, queued May 19) covering the Apr 22 self-catch. The arc is publish-legible.

### Migration arc onset

The window closes on the inflection point. Three of six leadership roles migrated:

- Apr 21 (Tue): Exec → PM strategic conversation confirmed Chat-to-Code migration for all roles; sequence agreed (HOST + CIO first, memo-writers next, Exec last)
- Apr 22 (Wed): HOST migration end-to-end in one session; produced the briefing-correction memo template that doubled as CIO migration template; surfaced Findings A–D used to refine the next migration prompts
- Apr 23 (Thu) AM: CIO migration completed — third role into Code
- Apr 23 (Thu) PM: Comms migration handoff package drafted (predecessor's final Chat session); successor's first Code session opened Apr 24

This isn't Comms's primary lane (HOST owns role migration), but Comms is named in the inventory because the handoff-memo template is now a six-section narrative artifact and the migrations themselves became material that other workstream pieces have begun referencing. Worth surfacing for the Ship narrative because the *shape* of the week was inflected by these migrations even where they weren't on the explicit agenda.

## Editorial calendar discipline (in window)

Editorial calendar updates in the window were primarily Docs-driven through the publish pipeline. Comms's role was upstream (drafting + voice-pass coordination through PM) rather than calendar maintenance. Calendar entries for all four publishes are complete with status, blog URL, Medium URL, LinkedIn URL, and syndication notes.

The editorial calendar's `queued`/`drafted`/`published` status flow continued to function cleanly under the Apr 18 publish-to-blog skill v0.7 + Apr 22 v0.8 progression. No status drift detected in window.

## What's still open

- **Building-narrative arc continuation**: drafts queued for Apr 28 (*The Deeper Why*), Apr 30 (*The Floor Comes Alive*), May 5 (*Six Issues Before Dinner*), and onward through May 21 (*The Voice of a Denial*). All in calendar Tue/Thu slots; all drafted; all awaiting PM voice pass.
- **Insight pool depth**: 12 unscheduled drafted insights are pooled awaiting selection per the 3–4 weekend planning horizon. Two newly-drafted insights (*The Meta-Observation Pattern*, *From Abstraction to Worked Example*) joined the pool today; the meta-observation piece carries an explicit in-body placeholder asking PM whether to ship or hold given the self-observation arc density.
- **Migration arc as future Comms territory**: the migration sequence is still playing out (Architect, PPM, CXO, Exec migrations continuing); a building narrative covering the migration arc is not yet drafted. Per PM Apr 24 direction, this is parked until the arc resolves enough to tell honestly.

## Cross-role threads worth naming for synthesis

Three threads I saw connecting roles' work across the window, surfaced for Exec to weight:

1. **Voice across layers** — Ship #039 theme + ethics-denial voice guidance + Voice of a Denial design + the meta-observation pattern. Multiple roles produced voice-shaped artifacts independently.
2. **Source discipline operationalized** — PDR-004 chain (prior window) → six-way replication (Apr 19) → omnibus self-drift (Apr 22) → Step 2.5 gate (Apr 22). One arc, three instances, one durable fix.
3. **From audit to migration** — M1 methodology audit lands Apr 17 (CIO) → Exec strategic conversation Apr 21 → HOST migration Apr 22 → CIO + Comms migrations Apr 23. The audit's findings (canonical-term drift, methodology operationally strong / docs weak) shaped the migration framing.

## Candidate themes for Ship #040 synthesis

Surfacing for Exec to consider; not advocating any single one:

- **"The Week the Migration Began Landing"** — most explicit; the kickoff names the inflection point
- **"Voice Across Layers"** — voice as the connective tissue across CXO + Lead Dev + Comms + the published pieces themselves
- **"Source Discipline Operationalized"** — the PDR-004 → workstream-review → omnibus-self-drift arc, with the Step 2.5 gate as the durable artifact
- **"From Audit to Migration"** — the methodology audit landing on Apr 17 set up the strategic conversation that produced the migration sequence; the week is the audit's first downstream effect

Comms has no preference; the synthesis is Exec/PM territory.

## For PM/exec consideration

- **Meta-observation pattern flag**: noted above. The successor surfaced this in the *Meta-Observation Pattern* draft that's now in the unscheduled pool. PM may want to weigh whether the Ship narrative acknowledges the pattern or quietly avoids reinforcing it.
- **Voice of a Denial as Lead-Dev-flagged blog candidate**: Lead Dev's Apr 22 PM session log explicitly flagged the three worked examples for Comms/Docs as a blog-post candidate. The successor has drafted *The Voice of a Denial* (queued May 21). Worth knowing for Ship narrative voice if it wants to reference the design explicitly.
- **Successor onboarding**: the predecessor's handoff package (`handoff-comms-chat-to-code-2026-04-23.md`) was the Apr 23 deliverable; successor (me) opened first Code session Apr 24, has since drafted nine pieces (one published, eight awaiting voice pass), and is now operational. Migration-on-migration learnings (per HOST Findings A–D) helped tighten the Comms migration prompt.

## What this memo does NOT cover

- Engineering / architecture decisions (Architect's lane)
- Methodology / pattern shifts (CIO's lane)
- Team / role health and migration mechanics (HOST's lane)
- Product gate criteria and sprint-to-roadmap (PPM's lane)
- Colleague Test rubric specifics and voice-quality scoring (CXO's lane)

These would all give a richer view of the same window from their respective lenses; this memo intentionally stays in the editorial / narrative / voice-as-artifact-output lane.

— Comms, 2026-04-26

*P.S. Verifiable-claims discipline: every comparative or historical claim in this memo (counts, named themes, named drafts, named sessions, dates, source-pieces, draft-status assertions) is grounded in editorial-calendar.csv or in the named omnibus / session log. Any claim that didn't survive that check was either dropped or softened to non-comparative framing. Source-paths in frontmatter.*
