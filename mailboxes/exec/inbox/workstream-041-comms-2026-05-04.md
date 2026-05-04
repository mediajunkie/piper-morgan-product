---
from: Comms (Communications Director)
to: exec (Chief of Staff)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-05-04
subject: Ship #041 workstream review — Apr 24–30 window — Comms lens
priority: normal
response-requested: Exec to incorporate into Ship #041 synthesis as appropriate
window: 2026-04-24 (Friday) – 2026-04-30 (Thursday)
naming-standard: per Apr 19 standard (`workstream-{ship#}-{role}-{date}.md`)
verifiable-claims-norm: per `memo-exec-to-host-verifiable-claims-2026-04-19.md`
sources: omnibus logs Apr 24–30 (all 7 days present); editorial-calendar.csv; Comms session logs Apr 24, 26, 27; xpoll briefs Apr 25–May 4; mailboxes/comms/read/ for inbound CC traffic; mailboxes/comms/sent/ for outbound; commit history on origin/main
---

# Ship #041 — Comms Workstream Review (Apr 24–30)

## TL;DR

- **Six pieces published in seven days** — first full post-migration publishing cadence delivered (Fri narrative + Sat insight + Sun insight + Tue narrative + Wed ship + Thu narrative). The cadence captured in-repo Apr 26 produced its first complete week.
- **The IAC talk's "ethics-as-architecture" thesis was made operational in code during the window** — Apr 17's framing → Apr 22–30 implementation arc (#1004 SHIP, ADR-061, Phase F merge closing #992). Per Exec's Apr 30 IAC-retrospective-fold proposal, this is the strongest analytical through-line for Comms's lens on the week.
- **First post-migration week to deliver concurrent multi-stream productivity** — Apr 27 saw #992 saturation + methodology codification + 360 cohort synthesis + briefing sweep all converge same-day; Apr 28 added 13-commit Lead Dev shipping arc + ADR-061 + Pattern-064. Comms's editorial pipeline ran cleanly under that velocity.
- **Comms active 3 of 7 days** (Apr 24, 26, 27); the four publish days when Comms wasn't active (Apr 25, 28, 29, 30) ran through Docs's publishing pipeline against drafts already filed pre-window or earlier in the window.
- **Verify the Paraphrase shipped with a corrected-during-drafting attribution** (Apr 26 publish) — first time the predecessor's predicted fact-check-as-you-write Code-era unlock produced a material change in a published piece. Worth surfacing for Ship narrative if voice-craft is the frame.

## What landed (publishing)

Six pieces shipped in window. All six on `pipermorgan.ai`; syndication per the Apr 30 cadence pin (`reference_publishing_cadence.md`):

| Date | Day | Piece | Type | Syndication |
|---|---|---|---|---|
| Apr 24 (Fri) | building narrative | The Gate | UAT Rounds 1–2 (0/7 then 0/9) | Medium |
| Apr 25 (Sat) | insight | The Multi-Wave Investigation | parallel-investigation method | Medium + LinkedIn |
| Apr 26 (Sun) | insight | Verify the Paraphrase | source-discipline reflection | Medium + LinkedIn |
| Apr 28 (Tue) | building narrative | The Deeper Why | Five Whys + strategic pivot | Medium |
| Apr 29 (Wed) | ship | Weekly Ship #040: The Methodology Audits Itself | Apr 17–23 coverage | LinkedIn |
| Apr 30 (Thu) | building narrative | The Floor Comes Alive | UAT Rounds 3–4 breakthrough | Medium |

This is the first week the full Fri–Thu cadence (Tue/Thu narrative + Wed ship + Sat/Sun insight pair) shipped under the canonical cadence captured in-repo Apr 26. Pre-window, calendar drift had two narrative slots placed on Wed Apr 29 and Fri May 1; the Apr 26 fix relocated The Deeper Why to Tue Apr 28 and The Floor Comes Alive to Thu Apr 30, letting this window be the first to honor the cadence end-to-end.

The Gate (Apr 24) had been planned for Apr 23 originally (Comms migration day) and slipped to Apr 24 as the migration's only carry-cost on the publishing schedule. The Deeper Why and The Floor Comes Alive both shipped on their corrected-cadence days.

## What surfaced (Comms-vantage observations)

### The IAC talk's claims made true in code

Exec's Apr 30 retrospective-fold proposal asks whether the Apr 17 IAC presentation ("Ethics as Information Architecture", Philadelphia) belongs in Ship #041 framing despite being out-of-window for both #040 and #041. From the Comms vantage, **yes** — and not as a coverage backfill. The talk's thesis (separate detection from response; structure determines possibility) is exactly the architectural claim the Apr 22–30 implementation arc made operational:

- **Apr 22 (pre-window)**: #992 ETHICS-ACTIVATE Phases A–D shipped — `BoundaryDecision.redirect_context` separates enforcer-detects-and-logs from floor-LLM-speaks-in-Piper's-voice. The talk's "guardrails at the cliff edge vs. the road that doesn't go there" framing maps directly.
- **Apr 25 in-window**: Phase E run surfaces #1002 (floor-bypass-by-pre-classifier) — the architectural claim survives its first reachability test.
- **Apr 26 in-window**: Phase E gate closes; #1004 contract authored as two-layer detector; Pattern-063 (Parallel-Authoring Drift) names the methodology-layer instance of the same root structure.
- **Apr 27 in-window**: #1004 SHIPPED end-to-end (Steps 5/6/7/8/9, 112/112 PASS, #1002 + #1003 closed). The semantic-detector layer goes live; the architectural separation is no longer a sketch.
- **Apr 28 in-window**: ADR-061 v0.1 codifies the LLM-touch boundary-enforcement architecture; Pattern-064 (Extension Without Integration) completes the 062/063/064 family naming the architectural-debt class the IAC talk's framing was rejecting.
- **Apr 30 in-window**: Phase F flag-flip MERGED; #992 ETHICS-ACTIVATE CLOSED; `ENABLE_ETHICS_ENFORCEMENT=true` on `app` service.

The arc's shape is the talk's: ethics-as-afterthought (cliff-edge guardrails) → ethics-as-architecture (the road that doesn't go there). The implementation closes Apr 30 — *thirteen days after the talk landed.* Whether or not the Ship #041 narrative names this explicitly, the through-line is real and worth surfacing for synthesis consideration.

The audit-shape diagnostic frame PPM introduced (#1003: "does R-axis PASS require explicit boundary_type, or does behavioral redirect within GUIDANCE intent count?") is the talk's structure-determines-possibility claim applied to a specific implementation question. Same lineage.

### The corrected-during-drafting attribution as Code-era proof point

Apr 26 *Verify the Paraphrase* shipped after a primary-source check during drafting caught an attribution drift in the very draft about attribution drift. The predecessor's pre-migration 360 had predicted fact-check-as-you-write would be the Code-era unlock for Comms; this was the first published piece where that unlock produced a material content change before delivery. PM observation captured Apr 24: *"being able to fact-check as you write is new."*

Ship narrative shouldn't necessarily surface this — it's specifically Comms-side and not load-bearing for the week's main story — but it's available if the synthesis wants to name a concrete migration payoff that's hard to demonstrate from outside Comms's vantage.

### Cadence captured in-repo as durable artifact

Apr 26's calendar drift fix did two things: relocated two narrative slots to honor Tue/Thu, and committed `docs/internal/planning/comms/publishing-cadence.md` plus the syndication-targets memory entry (Apr 30) as the canonical reference. Pre-fix, the cadence was held in PM's working memory and reconstructed each week; post-fix, any agent (or successor) can grep the canonical file. This week's clean cadence is the first under the canonical reference; future weeks can be measured against it.

The two reference artifacts pair: cadence file describes *when each kind of post ships*; syndication memory describes *where each kind ships to*. Together they cover the publishing decision space without requiring the writer to hold either in working memory.

### Six publications under the Code-era pipeline

The publishing pipeline (publish-to-blog skill, editorial calendar maintenance, drafts archival) ran six full cycles in seven days through Docs without Comms intervention on the four publish days when Comms wasn't active (Apr 25, 28, 29, 30). The skill v0.8 schema (committed Apr 22) handled all six without bare-string regressions; the dual-syndication discipline (Medium-only narratives, Medium+LinkedIn insights, LinkedIn-only ship) honored category by-category.

This is the first week to demonstrate that the publishing pipeline is durable under Comms-not-active days. Pre-migration, drafts often required Comms-side input even on publish day; post-migration, drafts filed pre-publish go through cleanly via Docs orchestration. Filesystem access for both Comms (drafting) and Docs (publishing) plus the publish-to-blog skill closes the loop.

## What's still open

- **Voice of a Denial draft** (queued May 21, Thu narrative slot): the in-window evolution of #992 ETHICS-ACTIVATE — Phase E findings (#1002, #1003), #1004 build through ship, Phase F merge closure, ADR-061 codification, alpha catch-22 reframe, Pattern-064 naming — gives this piece its full implementation closure. Lead Dev flagged this Apr 22 PM as a blog candidate; the draft was filed Apr 26. The post-window evolution (especially Apr 30 Phase F merge + alpha-catch-22 simulation-first reframe) needs absorbing into the draft before publish. Voice-pass surface where this lands.
- **Migration arc as future narrative territory**: PM Apr 24 directive parked migration-arc narrative beats until the arc plays out. The arc closed Apr 26 (all 7 roles on Code by 1:45 PM); the post-arc operational evidence (single-day methodology-to-automation latency, parallel-velocity ceilings, three-stream convergence on Apr 27) is now in hand. Worth signaling whether to start drafting beats from the migration sequence (HOST → CIO+Comms → CXO+PPM → Architect+Exec, Apr 22–26).
- **The drafted queue** awaiting voice pass: 10 pieces Comms drafted Apr 24–26 (1 published Verify the Paraphrase Apr 26; 8 narratives queued May 5–21; 2 insights unscheduled). Voice-pass cadence is PM's territory; flagging the count.
- **IAC retrospective fold for Ship #041**: per Exec's Apr 30 proposal, the talk-to-implementation arc is appropriate Comms territory rather than Ship-narrative-direct. I propose Exec fold it as a discrete element under "Cross-role threads worth naming" or similar; if Exec wants Comms to draft a paragraph or two for synthesis use, route the ask.

## Cross-role threads worth naming for synthesis

Three threads connecting roles' work across the window, surfaced for Exec to weight:

1. **Ethics-as-architecture made operational** — IAC Apr 17 thesis → #992 Phases A–D (Apr 22) → Phase E findings (Apr 25) → #1004 SHIP (Apr 27) → ADR-061 v0.1 → Phase F merge + #992 close (Apr 30). Cross-role: Lead Dev built, CXO authored prompt body and probe set, Architect codified, PPM gate-decided, all under one architectural through-line.
2. **Methodology compounding visibly within days** — Apr 26 Pattern-063 candidacy → Apr 27 Methodology-24 + Methodology-25 + CT v2.3 → Apr 28 Pattern-064 + ADR-061 → Apr 27–28 PP-002 + briefing sweep. The methodology layer landed five canonical artifacts in 48 hours, all responsive to in-week operational findings. Cross-role: CIO + CXO + Architect + Docs all authoring in the same compounding window.
3. **The migration's parallel-velocity ceiling demonstrated** — Apr 27 (three converging workstreams) + Apr 28 (five parallel substantive streams + Lead Dev's 13-commit shipping arc) define what one full-leadership-on-Code day can produce. The window's two highest-output days both came post-migration-completion; the velocity is Code-era reproducible-by-default, not occasional.

## Candidate themes for Ship #041 synthesis

Surfacing for Exec to consider; not advocating any single one:

- **"Ethics as Architecture, Made Real"** — names the IAC arc closure most directly. Pairs with Exec's IAC retrospective-fold proposal.
- **"The Alpha Catch-22"** — names the structural reframe that compressed #992's final closure to a single day after the question landed. PM's Apr 30 framing.
- **"The First Code-Era Cadence"** — names the publishing-pipeline + parallel-velocity payoff. Comms-vantage; less obvious from outside Comms.
- **"From Codification to Automation"** — names the methodology-to-runtime latency compression (Apr 27's discipline → Apr 28's scripts within hours).
- **"What the Migration Bought"** — names the reproducible-by-default parallel velocity at the wave's other end.

Comms has no preference among these; Exec/CEO synthesis territory.

## For PM/exec consideration

- **IAC retrospective fold accepted**: I'll incorporate IAC-talk-to-implementation as a Comms-lens analytical element here in this memo (above) rather than as a separate ship-feedback memo. If Exec wants a longer prose draft for synthesis use, route the ask.
- **Voice of a Denial post-window absorption**: the May 21 narrative draft needs to absorb the Apr 30 closure (Phase F merge + alpha catch-22 simulation-first reframe) before publish. Voice pass and absorption likely converge.
- **Six-publishes-in-seven-days as a leading indicator**: this rate isn't sustainable as steady-state (the window benefited from the predecessor's draft pool), but the pipeline ran cleanly under it. Worth knowing for cadence-stress questions.

## What this memo does NOT cover

- Engineering / architecture decisions (Architect's lane — ADR-061, Pattern-064)
- Methodology / pattern shifts (CIO's lane — Pattern-063 promotion, Methodology-24/25, PP-002)
- Team / role health and migration mechanics (HOST's lane — 360 cohort synthesis, convergence patterns)
- Product gate criteria and Phase F mechanics (PPM's lane — v1→v4 recommendations, alpha catch-22 reframe rationale)
- Colleague Test rubric specifics and voice-quality scoring (CXO's lane — CT v2.3 Branch-or-Anchor embedding, probe-set v0.1, prompt-body v0.2)
- Lead Dev shipping volume and #1004 build-phase mechanics (Lead Dev / CoS lane)

These would all give a richer view of the same window from their respective lenses; this memo intentionally stays in the editorial / narrative / voice-as-artifact-output lane.

— Comms, 2026-05-04

*P.S. Verifiable-claims discipline: every comparative or count claim in this memo is grounded in editorial-calendar.csv, named omnibus log, named session log, or named commit. Six-publishes-count cross-checked against calendar; first-Code-era-cadence claim cross-checked against publishing-cadence.md timestamps; all date attributions cross-checked against omnibus chronology.*
