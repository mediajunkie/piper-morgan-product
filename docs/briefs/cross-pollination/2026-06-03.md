# Cross-Pollination Brief — June 3, 2026

Ship #045 "The Substrate Pivoted" draft landed overnight with all six workstream memos absorbed and a clear spine: PM's duty cycle scaled to eight agents on shared `main`, collected enough clash evidence that correct discipline couldn't prevent, and the team overturned its own recent architectural default in a 15-minute ratification window rather than adding a fourth enforcement layer. Also overnight: PM's CIO filed a cross-project methodology handoff to Klatch's Calliope distilling the cohort's hard-won duty-cycle migration lessons — most importantly that cadence should match each agent's work-shape, not be a universal fixed interval. And PM's M2 sprint close-gate is down to one remaining item after last night's trust-layer UI fix.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. "The Substrate Pivoted" — Ship #045 draft complete, ready for PM voice-pass today

**From:** Exec cycle log June 2, Fires 24–26; commit `0694ef3` (draft filed `docs/public/comms/drafts/weekly-ship-045-draft-2026-06-03.md`); all 6 workstream memos (PPM v2, CXO, Architect, Comms, CIO, HOST)
**Relevant to:** designinproduct (publication milestone); Klatch (structural-fix-over-discipline lesson)

The May 22–28 Ship draft is written and waiting for PM voice-pass and publication today. The draft title, "The Substrate Pivoted," continues Ship #044's substrate thread one altitude up: the operating substrate produced enough evidence to invalidate one of its own architectural defaults.

The spine (CIO + HOST memos jointly named it): the duty cycle scaled from 1 agent to 8 on shared `main`, collected 29 commits in 8 hours from simultaneous agents, and experienced 4 independent clash incidents — including one that happened *after* a correct count-check, because the race occurred inside the compound command, after the check. Rather than adding a fourth discipline layer, the team ratified worktree isolation as the structural fix in a 15-minute window on May 28. The cohort self-validated the new spec the same night.

Supporting beats from the five other workstream lanes:
- **Architect**: Anthropic's May 6 Dreams API spec externally validated all 4 of Pattern-070's operational invariants — the "platform laps you, climb the value chain" reframe as a concrete instance
- **CXO**: #683 done-criteria split into Layer A (engineering-DoD) + Layer B (experience-DoD) in one session, with each layer routed to its right owner same-day ("decomposition-with-ownership unblocks faster than escalation")
- **Comms**: five publications shipped the same week ~8,260 words of future inventory were drafted — cadence and capacity decoupled
- **PPM**: standing-items tracker reframed as the Task Loop source with no new tooling (cheap-adoption primitive); Day-1 strand failure → structural fix is the cohort's standard remediation shape
- **HOST**: "correct discipline that still clashes is a trust signal, not a discipline gap" — PP-004 instance #4 candidate; the failure belongs to system design, not agent carelessness

Learning pattern (HOST framing): structural fix beats discipline fix. When correct behavior still produces failure, the right response is to change the system, not tighten the rules.

Per CIO recommendation, the v0.7.0 adoption package, cohort-migration arc, and cron-shape-experiments content are folded out to Ship #046, keeping #045 clean to its window.

**Suggested action:** Klatch — the worktree-isolation lesson applies before it's discovered the hard way. The compound-command race (correct check, then race *inside* the command) is a specific failure mode worth naming in Klatch's multi-agent coordination.

---

### 2. Cadence should match work-shape — PM's CIO hands Klatch 8 migration lessons

**From:** Klatch `docs/mail/cio-piper-to-calliope-shepherding-agents-onto-duty-cycle-2026-06-02.md`; PM directive June 2 (cron-shape experimentation authorized)
**Relevant to:** Klatch (directly addressed); designinproduct (Janus's parallel CCR→local-cron pivot)

PM's CIO filed an 8-principle cross-project handoff to Klatch's Calliope last night, distilling what the full PM cohort (~10 agents) learned over its migration week. The load-bearing principle (§4): "cadence must match work-shape, not be one fixed interval." Three work-shape types emerged in practice: continuous-mail lanes (coordination, docs, publishing) suit hourly cycles; bursty lanes (an architect or implementer whose backlog drains between bursts) work better at longer intervals once drained; intermittent lanes (manual testers, UX agents) need low-frequency awareness, not constant cycling. Recommendation: stand up a `cron-shape-experiments.md` registry early so agents can self-report shapes before defaults get locked in.

Other load-bearing lessons: worktree isolation is determined by the *launch surface* (Desktop "New session" auto-creates ephemeral worktrees; terminal launch at repo root does not — pick one standard and stick to it); the "normalization trap" — standardizing agent prompts to a shared template can silently drop the nuanced heuristics that made earlier bespoke versions perform well (restore them). Also: a "wait-default re-arm heuristic" (re-arm cron only on positive absence signals, not on any silence) outperformed all alternatives for returning to autonomous IDLE after human conversation ends.

PM also authorized cron-shape experimentation across the cohort on June 2 evening: hourly is the default, not a mandate. Agents can experiment with their interval and report results to a shared registry.

Janus (DinP) is solving the parallel problem — transitioning from CCR fresh-spawn triggers to local-cron-against-a-continuing-session. Duty-cycle v0.1 was approved June 1; CIO explicitly cross-referenced Janus and Calliope as solving the same problem in different substrates.

**Suggested action:** Klatch Calliope — classify each agent's work-shape (Daedalus = bursty-implementation; Calliope = continuous-coordination; Theseus = intermittent-manual-testing; Argus = bursty-quality) before picking cadence. Set up the cron-shape experiments registry before standardizing.

---

### 3. PM's M2 close-gate narrows to one smoke test; trust-layer UI fix ships

**From:** Commit `ef58ae7` (`fix(#1132): trust_stage in insights_ui`); lead dev cycle log June 3 Fires 1–5; PM sign-off June 2 ~22:10
**Relevant to:** PM internal; Klatch (PM's trust + context assembly layers are the integration target for future BYOC/MCP work)

Lead Dev shipped #1132 last night: the trust score display in PM's insights UI now reads live from `TrustComputationService` rather than a hardcoded value. The fix is architecturally in the same family as R4 source-declarative provenance (June 2 brief) — "show what you computed, not what you assumed" applied at the display layer. PM signed off at 22:10. M2's close-gate is now down to a single pending smoke test (#1047), which Lead Dev resumes this morning.

When M2 closes, PM's context assembly layer (18 gather paths, structured provenance per R4) and trust layer (TrustComputationService flowing through to the UI) are jointly stabilized — the technical foundation for BYOC/MCP delivery.

**Suggested action:** Watch today's #1047 smoke result. M2 completion is the sprint boundary that clears PM for integration-phase work.

---

## Sources Read

- **piper-morgan-product**: Exec cycle log `dev/active/cycle-log-exec-2026-06-02.md` (full — Fires 15–26, synthesis arc); PPM workstream memo v2 (full); lead dev cycle log June 3 Fires 1–5; commit `ef58ae7` (#1132); git log 48h (~25 commits reviewed)
- **klatch**: `docs/mail/cio-piper-to-calliope-shepherding-agents-onto-duty-cycle-2026-06-02.md` (full); git log 48h (5 commits — brief delivery + mail)
- **designinproduct** (hub): `docs/agents/janus/duty-cycle-v0.1-proposal.md` (header); sweep-log; letters excerpt confirmed current

**Not re-reported (covered in prior briefs):** R4 source-declarative provenance (#1030+#1032, June 2); BYOC post publication (June 2); Ship #045 kickoff distribution (June 2); PPM + CXO cohort onboarding imminent (June 2); INSIGHT-PULL/PUSH (June 1); Opus 4.8 (June 1); Claude Code 2.1.157 auto-loading (June 1); v0.7 worktree-as-cycle-default ratified (May 29).

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*