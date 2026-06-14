# Architect Attention Doc — Items for PM

**Purpose**: things Architect wants PM to see/decide/respond to, per duty cycle v0.7 / Option B ephemeral worktree.

**Convention**: list items in priority order with brief context. Move resolved items to "Resolved this week" with disposition.

**Last refreshed**: 2026-06-13 04:35 PT (Fire 40 START m-41 attention-doc reconciliation; previous refresh 2026-06-09 19:30 PT was 4 days stale — refresh-on-touch discipline applied).

---

## Active (items PM may want to see/decide/respond to)

- **(PM call open from 2026-06-12 Fire 34)** — **User-correction recovery question**. Lead Dev's #1193 audit surfaced 2 user-data-loss traps in production (`web/api/routes/insights.py:126` user free-text corrections + `:171` mark-surfaced silently discarded since at least May 16 #1079 ship date). Architect raised in ack to Lead + cc PM: attempt recovery of lost corrections from intent logs/replays IF possible, else m-41 guard makes next instance impossible-by-construction. Not blocking other work; PM-time-only decision. Source memos in `arch/read/`.
- **(PM call open from 2026-06-12 workstream-047)** — **Ship #047 spine call**. Architect filed two spine candidates: preferred *"naming what we already do — the catalog grows discipline before crisis"*; alt *"composition-not-greenfield as architectural posture."* PM/Exec own the altitude. Lens at `mailboxes/exec/inbox/workstream-047-arch-2026-06-12.md`.
- **(RESOLVED 2026-06-14 Fire 44)** — ~~ADR-066 v0.2 amendment timing~~ — PA relayed PM call 2026-06-14: draft NOW while reasoning sharp. **ADR-066 v0.2 AUTHORED Fire 44** with D7 Configuration Ownership Convention. PA + cohort review at cadence; CIO catalog touch when next pass opens.
- **(NEW Architect-owed work 2026-06-14 Fire 44)** — **MCP connector ADR + topology**. Lead Dev's PM-ratified decision moved connector model to MCP-consumer direction; Arch owns the ADR + substrate topology design before Lead Dev decomposes WS-1..8. Input doc at `docs/internal/architecture/connector-refactor-sprint-scope-2026-06-14.md`. No M3 dependency (M4/M5 milestone). Substantial — auth model + per-connector migration path + MCP-server maturity per connector. Likely ADR-070 candidate. Queued for next fire; will scope after reading input doc.

## Awareness only (informational; no PM action needed)

- **June 12 was a heavy day**: 6 substantive memos + ADR-069 v0.1 ratification + m-41 Proven promotion CONCUR + Workstream-047 review + #1193 disposition+ratification + #1058 ack + #1207 ratification + ADR-069 ratification. All on origin/main; substantive work complete by Fire 38 22:30 PT. Fire 39 22:52 PT STOP did NOT execute (cron died with session at session-dormancy boundary); Fire 40 04:22 PT Step-0 self-heal cleanly restored close-out discipline. Mechanism-functioned-as-designed.
- **F4 reproducibility re-confirmed 2026-06-12 → 2026-06-13 overnight**: cron `d0b83566` durable=true again no-op. Gap-C session-dormancy is the dominant cron-loss mechanism (CIO empirical finding 6/11 holds; cure remains Routines watchdog $70/mo PM-gated).
- **methodology-41 Emerging→Proven promoted 2026-06-12**: CIO authors amendment + INDEX update next CIO fire. Cure-class generalized: "no path of least resistance bypasses the discipline" with producer-altitude (m-31 dual-surface, superseded by single-log) + consumer-altitude (carry-forward register-separation) sub-shapes.
- **methodology-30 cross-author Proven candidacy strengthening**: 5 instances total now (Phase 3 coverage / Phase 4 audit-cascade / #371 event-shape / #1193 session_scope / #1207 conversation-context). All Lead-Dev-applied as authors but with multi-author historical evidence pairs (#1193 3-actor #1079/#1143/insights; #1207 single-author-multi-incident dead-since-shipping). CIO judgment whether multi-author-historical-arc-via-consumer-trace meets cross-author Proven-bar.
- **ADR-069 (Domain Concept Projection Contract) live in catalog** — Lead-authored from #1207 carve; Architect-ratified. Pattern durable for next mixed-responsibility concept (`Intent` likely next; `Artifact` #952 honest-scope-qualified).
- **CLAUDE.md updates 2026-06-12 (carried)**: (1) Option B ephemeral worktree canonical, Model A deprecated; (2) single-log discipline (session log only; cycle log = optional scratch). Architect already on Option B + adopted single-log Fire 37.

## Discipline-edge observations

- **Pre-authorized-disposition-with-explicit-gating → audit-to-ship inside one cycle (~3 hours)** — #1193 from disposition memo to shipped fix in ~3 hours including 133-site audit + Option A + m-41 guard + behavioral verification. Watch for second instance to evaluate as catalog candidate.
- **Goodness-from-constraint pattern** — Cowork sandbox constraint (no host filesystem write) pushed us toward cleaner architecture (server-owned config + "run anywhere" natural property). Worth flagging as a Pattern-070 (External validation refining design) adjacent instance. CIO catalog lane.

## Mutual-assessment exchange commitments — all COMPLETED

- [x] Day-1 / Day-3/4 / Day-7 synthesis — folded into Day-5 findings memo to CIO (filed 2026-06-08 morning)

## Resolved this week (since 2026-06-09 refresh)

- **F4 cron-durability** — RESOLVED 2026-06-11 by CIO Gap-C empirical investigation; reproducibility re-confirmed 2026-06-12/13 overnight; cure remains external watchdog.
- **methodology-42 (Reflexive Verification)** — Filed Emerging 2026-06-11 by CIO from Architect Fire 26 recognition memo + 5-instance articulation.
- **methodology-41 (Mechanism Displaces Unreferenced Discipline)** — Emerging→Proven promoted 2026-06-12 via Architect CONCUR.
- **Workstream-047 Architect lens** — FILED 2026-06-12 paced to source-set state (NOT Tue Jun 16 backstop).
- **#1193 session_scope() silent no-commit trap** — Lead Dev shipped Option A + m-41 guard 2026-06-12; user-data-loss exposed (PM call OPEN above); m-30 instance #4 + 3-actor historical Pattern-073 evidence.
- **#1207 conversation-context unification + ADR-069 (Domain Concept Projection Contract)** — Lead Dev shipped #1207 implementation + ADR-069 v0.1 authored; Architect ratified carve + ADR artifact; #1211 shadowing+broad-except sweep filed; m-30 instance #5.
- **#1058 template hygiene** — HOST shipped trim; Architect concurred close on hygiene AC; #1206 carries deferred deployment-model reframe (Lead+Arch lane) with four-tier framing note.
- **PA Skunkworks BYOC Phase 2** — Architect lens shipped 2026-06-13; green-light + 5 red flags + ADR-066 v0.2 amendment candidate; cohort-wide cc.
- **June 12 retroactive close-out via Step-0 self-heal** — 2026-06-13 Fire 40.
- **HOST BYOC trust-lens ack** — 2026-06-13 Fire 41; m-41 third sub-shape candidate (architecture-boundary altitude); floor-extends-to-handoff concrete gate-run shape. CIO accepted 2026-06-13 with confluence framing.
- **June 13 retroactive close-out via Step-0 self-heal** — 2026-06-14 Fire 44 (second F4 instance in 48h; mechanism functioning).
- **#1206 item-3 four-tier reframe call** — 2026-06-14 Fire 44; YES reframe; Docs ships.
- **HOST decisions.log reinstatement** — 2026-06-14 Fire 44; CLAUDE.md Recording-decisions section added.
- **ADR-066 v0.2 AUTHORED** — 2026-06-14 Fire 44; D7 Configuration Ownership; "run anywhere" structural.

## "Working memory" for PM (open questions only PM can decide)

- **User-correction recovery question** (Fire 34 6/12) — attempt recovery from intent logs IF possible, else m-41 guard makes next instance impossible-by-construction.
- **Ship #047 spine call** (Fire 32 6/12) — preferred "naming what we already do" vs. alt "composition-not-greenfield." PM/Exec own altitude.
- **Routines watchdog $70/mo funding** — known PM-gated decision; not new. Continued reproducibility of F4 Gap-C session-dormancy across two 48h instances strengthens the cure-rationale.
