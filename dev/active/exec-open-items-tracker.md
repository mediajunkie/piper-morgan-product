# Executive Office: Open Items Tracker

> **Living document** — updated at the end of every exec session.
> This is the canonical list of tracked items. Session logs may contain discussion but this file is the source of truth.
>
> **Disposition policy is operational, not aspirational** (per HOST 360 synthesis pull, Apr 27): at every reconciliation, every item is checked against the >14-day-zero-movement threshold and force-decided here (do / defer-with-explicit-reason / drop). Items don't get parked. If an item recurs at the threshold across reconciliations without movement, the role-holder owes an explicit reason or it drops on the next pass.
>
> Last updated: 2026-05-10, ~4:45 PM PT (exec Code session 6 — Day 6 post-6-day-gap refresh; Phase F + ADR-061 + Ship #040 + Ship #041 all closed since last update; new BYOC + M2d + Review-Gates threads opened)

---

## Context Note

Reconciliation following the May 4–9 stretch I was off the project for. Phase F flag-flip + ADR-061 + Ship #040 + Ship #041 all closed during the gap. M2c-tail closed; M2d gate criteria converged; M2a-e DONE per May 8 briefing; M2f opened with A+B shipped May 9. BYOC PDR-005 discovery thread opened. Pattern Sweep 2.0 produced 1 TRUE EMERGENCE + 6 new anti-pattern candidates. Ship #042 kickoff distributed today; window May 1–7 closes; filing window EOD Tue May 12.

Disposition policy applied. No items below at >14-day-zero-movement.

---

## Active Items

| # | Item | Owner | Opened | Status | Notes |
|---|------|-------|--------|--------|-------|
| 1 | **Ship #042 workstream review (May 1–7)** | exec (solicit + synthesize) | May 10 (kickoff filed) | Kickoff distributed today; ~48hr filing window; synthesis Wed May 13 | Third Code-era cycle. Density note folded into kickoff per CEO concern (Ship running long + jargon-y). |
| 2 | **BYOC PDR-005 discovery thread** | PPM (lead) + Architect + CXO + PA | May 4 (PPM opens) | Architect feasibility-check ack May 4 ("folding into next architectural session"); CXO + PA inputs pending | Trigger fired Apr 27 per PM; rate-limited to post-Ship #040 publication; opened post-publication. Paired-document approach (PDR-005 + ADR-061 cross-reference per PDR-001/ADR-060 precedent). |
| 3 | **PPM Review Gates proposal** | PPM (proposed) + HOST/CEO (ratify) + CXO/Architect (refinement) | May 4 (filed) | Architect concur on review-surface shape + Class D refinement (May 4); HOST + CEO ratification pending | HOST 360 §9.2 pull close. 5-class review surface (PDR-adjacent / sub-epic gate / quality-threshold-affecting / integration-pattern-shifting / user-facing-CXO-implication). Fail-soft default; review-surface not gate. |
| 4 | **M2d gate completion criteria operationalization** | PPM (lead) + Lead Dev + Architect + CXO | May 4–5 (converged) | Quality-threshold mapping + verification protocol + conceptual-integrity checklist; PPM → Arch concur → Lead Dev concur converged | M2d issue restructure executed May 2 (#1030/#1031/#1032/#1033 new; #707/#714/#703 reframed; #869 → M2e). Now applies to actual M2d gate-close decisions. |
| 5 | **Architect's Lead-Dev architectural soundness review — 5 cleanup items** | Architect (filed) + PM ratification of cleanup-ticket disposition | May 4 (filed) | 5 items surfaced: (1) alive scaffolding in `services/knowledge/knowledge_graph_service.py` (canonical Pattern-064 wild instance); (2) legacy `boundary_enforcer.py` parallel coexistence; (3) commented-out adaptive-learn TODO; (4) one no-test commit on contract path; (5) ADR-051 RequestContext partial migration (#1015) | None are soundness blockers; all tracking-ticket material. Item #1 is easiest fix + the Pattern-064 textbook-fix instance. PM ratification of cleanup-ticket disposition pending. |
| 6 | **Cross-pollination brief delivery as session-start hook (scoping)** | Lead Dev (scope) + CIO (requestor) + HOST (monitor) | May 8 (CIO scoping ask) | Lead Dev scoping pending; non-urgent | HOST 360 pull #1 (CIO §9.2 wheelhouse). Code-era automation candidate. Lead Dev decides feasibility / shape; no commitment to build. |
| 7 | **Bash-tool cwd-drift hook/automation** | Docs or PA (CEO preference) + Lead Dev (excluded — ops-task distraction concern) | May 4 (CEO May 4 direction) | Open; not yet scoped | HOST observed 3 careful-agent-cwd-drift incidents in 4 days (Apr 26 Lead Dev / Docs subshell / Apr 29 PA). CEO May 4: "want to work on hook/automation; not via Lead Dev." Pair with Docs or PA when bandwidth allows. |
| 8 | **Migration checklist v1.1** | HOST (lead) + exec (review) | Apr 22 | HOST drafting; status check pending | Phase 3 first-week findings + captain-last sequencing + three-artifact package shape + Section 6 thematic-convergence framing. |
| 9 | **Codification of handoff review pattern** | exec | Apr 26 | First-month task per startup prompt §8; target end of May | ~half-day work. Six review memos as source material. Coordinate with Methodology-25 (CIO Apr 27) before duplicating. |
| 10 | **Agent 360 Round 2 — synthesis cohort confer + v0.3 design** | HOST (lead) + cohort | Apr 22 | HOST cohort cover memo distributed Apr 27 with per-role asks; HOST 360 commitments threads landing across cohort; v0.3 design conversation pending | Section 6 thematic-convergence finding (PP-002 ratified Apr 27). Re-benchmark target Jun 8. |
| 11 | **Briefing correction memos → Docs** | Docs (act) + CXO + PPM + CIO + exec (filed) | Apr 25–28 | CIO briefing v3 applied May 3 (Docs); CXO/PPM/Architect/HOST briefing absorption in flight per CIO B6 Flywheel-reference sweep | Docs working through. |
| 12 | **PPM Phase F v5 audit-trail completion** | PPM (filed) | May 4 | Documentation-update only; audit-trail closure; not gating anything | v4 conditions satisfied differently than specified (catch-22 reframe + simulation-first calibration). Future-readers clarity. No response needed. |
| 13 | **Roadmap.md staleness** | PPM (refresh) + Docs (cadence proposal) | May 4 (Docs flag) | 23 days stale at flag; PPM to refresh + propose recurring mechanism | Surfaced via #1049 weekly docs audit. |
| 14 | **Test files in services/ — testing-rigor convention call** | Lead Dev + Architect (call) | May 4 (Docs flag → Lead Dev assessment May 5) | Lead Dev assessment filed to Docs ("fold into testing-rigor ADR"); pending Architect's call on whether convention is intentional or worth tightening | 5 test files co-located in services/. Surfaced via #1049 weekly docs audit. |
| 15 | **Pattern Sweep 2.0 follow-ups** | CIO (lead) | May 9 (results filed) | 6 new anti-pattern candidates added to index (A-12 Alive Scaffolding, P-12 Broad git-add multi-agent sweep, P-13 Commit-attribution drift, P-14 Silent rubric extension, P-15 Branch-collision, T-05 Activation-flag theater); 1 TRUE EMERGENCE Pattern-066 (Stacked Silent Failures) Emerging; 063/064/065 promote-to-Proven recommended (CIO May 8 analysis); 9 stale patterns flagged for next-cycle triage | Pattern-066 to Proven after trial-application; pattern catalog 65 → 66. |
| 16 | **Alpha tester phase closure** | PM + HOST | Mar 14 | 57+ days; PM Apr 25 framing of "phase effectively ended"; CEO May 10: comfortable with stretches without externalities; beta within a month begins new external engagement | Decision needed: formal closure message + separate Ted/Dominique tracking. CEO May 10 context softens urgency; carrying. |
| 17 | **PDR-004 corrections on Medium/LinkedIn** | PM + Docs | Apr 16 | 24 days, status unknown | "Patience over performance" paraphrase. Posts still need correction. Verify with Docs. |
| 18 | **team-structure.md staleness** | Docs + HOST | Apr 16 (re-flagged) | 129+ days stale; highest doc-fix priority per HOST | Doesn't list PA, PPM, CXO, ETA, Mobile. |
| 19 | **`known_pathological` corpus tagging** | Lead Dev | Apr 16 | Likely subsumed by #1004 probe-set work; verify | May be closeable; needs Lead Dev signal. |
| 20 | **Cross-pollination hook update** | Lead Dev | Mar 31 | 40 days; CIO May 8 scoping ask = active progress (see item 6 — same thread) | Folding into item 6. |
| 21 | **PA tracker reconciliation partial-delegation** | PA (data-gathering) + exec (judgment) | Apr 26 | Pattern proposed; awaiting first PA `tracker-prep:` pass | Cadence target: weekly. |
| 22 | **Two stale unowned branches** | Docs (merge-keeper escalation) + PM (disposition) | recurring | Branches: `fix-docker-migration-setup`, `new-docs-log-1XXym`. Recurring across merge-keeper sweep runs. | Disposition: archive / delete / claim. HOST flagged in workstream-041. |
| 23 | **Apr 27 omnibus reframing memo supersession** | Docs (update or supersede) | May 4 (clarification) | May 4 two-senses-of-primary clarification stands as operative; Apr 27 memo reads opposite; not yet formally superseded | Worth Docs's attention. Not urgent. |

### ⚠️ DISPOSITION FLAGS — None this cycle

All items above had progress in the last cycle or have a named owner with a current ETA. No items >14 days with zero movement (item 17 PDR-004 is the closest watch).

### Human Network (escalation items)

| Person | Status | Days | Next Action Needed |
|--------|--------|------|--------------------|
| Alpha testers (13) | **57+ days, zero responses** | 57+ | CEO May 10: comfortable with stretches; beta within a month begins new engagement. Carrying with reduced urgency. |
| Dominique Derosena | **58+ days, no reply** | 58+ | 500 error may be fixed. 1:1 follow-up. |
| Ted Nadeau | Active advisor | — | CEO met with Ted in the May 4–10 window (lightly P-M-related). Security.md, Methodology.md reviews still pending. |
| Cindy Chastain | Podcast released ~Mar 31 | — | No action needed. |
| Dave Romero | Pitch outcome unknown | — | No change. |
| Sam Zimmerman | Dormant advisor | — | Acknowledge formally as dormant with completed contributions. |

## Backburner

| # | Item | Owner | Opened | Notes |
|---|------|-------|--------|-------|
| B1 | Website v3 copy execution | PM | Feb 22 | Low priority until beta |
| B2 | CIO innovation backlog | CIO | Apr 2 | Reconstructed Apr 27 (`a8ea7d48`); standing CIO watch list now in active maintenance |
| B3 | Colleague Test v2 monitoring integration | HOST | Apr 19 | CT v2.3 committed Apr 27. HOST to incorporate into next health check cycle. |
| B4 | Context-age monitoring for Chat sessions | HOST | Apr 16 | Less relevant post-migration. Defer until we understand Code session patterns. |
| B5 | `workstream-review` skill draft | exec | Apr 22 | Coordinate with Methodology-25 (CIO Apr 27) before duplicating. Likely subsumed; verify before drafting. |

## Recently Completed

### Apr 30 – May 10
| Item | Completed | Notes |
|------|-----------|-------|
| **Phase F flag-flip MERGED** (`deecc816`) | Apr 30 | `ENABLE_ETHICS_ENFORCEMENT=true` live. #992 ETHICS-ACTIVATE closed (8/8 ACs marked). Alpha catch-22 reframe (CEO-named) + three-phase calibration plan (simulation → beta → stable) folded into ADR-061 v1.0. |
| **ADR-061 v1.0 RATIFIED** | May 4 | CEO verbal approval. Architect committed v1.0 Apr 30 with all 6 Lead Dev review findings folded. ADR count 63 → 64. |
| **Ship #040 published** ("The Methodology Audits Itself") | Apr 29 | CEO voice pass + Docs publish + LinkedIn syndication. |
| **Ship #041 published** ("The Methodology Closes Its Own Loops") | May 6 (per briefing) | Theme converged on same-cycle methodology closure. CEO post-publication feedback: getting long + jargon-y; folded into #042 kickoff guidance. |
| **#1018 Phase 2 SHIPPED** (`fc79de31`) | May 2 | audit_transparency durability; PostgreSQL-backed `ethics_audit_log`; cluster regressions #1006/#1007/#1008 closed together. |
| **M2d issue restructure** | May 2 | 4 new issues filed (#1030/#1031/#1032/#1033); 3 reframed (#707/#714/#703); #869 relocated to M2e. Conceptual-integrity gate added to M2d completion. |
| **HOST 360 commitment #2: disposition policy as permanent tracker convention** | Apr 30 | Codified in tracker header. |
| **Cross-project comms gap (Architect response)** | Apr 30 | Architect response: weak (a) leaning (b) for now; specific shape proposal in flight. Tracker escalation closed; Architect work continues separately. |
| **Briefing-freshness hook fix** (`75de5213`) | Apr 29 | Docs incorporated my Apr 28 diagnosis. Hook output names response action; CLAUDE.md MANDATORY cross-role subsection. |
| **Branch-discipline synthesis v1.0 final** (`594991db`) | Apr 29 | PA published at canonical path. Rule 5 designation preserved; Docs as merge-keeper PM-confirmed Apr 27. |
| **Methodology-26 (Indoor Plumbing Scope Filter)** | Apr 27 | CIO filed (`6b8bdcb7`). M1 Audit B3 close. |
| **Pattern-065 (Continuity Memo Before the Seam)** | Apr 27 | CIO filed. Six-section structure operationally validated across 7 cohort migrations. |
| **CIO Innovation Backlog reconstructed** | Apr 27 | `dev/active/cio-innovation-backlog.md` (`a8ea7d48`). |
| **M1 audit closure (12 recommendations dispositioned)** | Apr 27 EOD | A1/A2/A3 + B1–B6 + S1/S2/S3 all dispositioned. 10 days from audit delivery. |
| **`canonical-vocabulary-watch.md` v1 shipped** | May 4 | Docs (joint-stewardship with CIO). |
| **CIO briefing v3 applied** | May 3 | Docs absorbed Section 4 structural gaps. |
| **OpenLaws Bet 1 reply bundle** | Apr 26–27 | PA Q1+Q2+Q3+Q4; exec Q5+Q2 (CoS-vantage); Q6 PM call. |
| **B6 V3 mystery decline path** | Apr 26 | Resolved per Architect: LLM classifier free-form action label, not a separate mechanism. Subsumed by #1004. |
| **Audit S1 canonical-term-drift explicit** | Apr 27 / May 4 | CIO filed memo to Docs Apr 27; concur ack May 4; `canonical-vocabulary-watch.md` v1 shipped May 4. |
| **Audit S3 Klatch AAXT scaffolded probing** | Apr 27 | CIO trigger-bound heads-up filed to Lead Dev. |
| **Audit-A3 disposition: retire** | Apr 27 | Lead Dev memo to CIO. |
| **All seven leadership migrations** | Apr 22–26 | Captain-last principle held. |
| **Per-memo commit-and-push norm + Mailbox-discipline norm + Sign-off discipline norm** | Apr 26 → Apr 28 | All three trunk-resident; check-branch.sh hook + sign-off CLAUDE.md section. |
| **merge-keeper-sweep.py + regenerate-mailbox-manifests.py** | Apr 28 | Lead Dev shipped 773 lines combined. Docs runs sweep daily. |

### Archived prior periods
- Apr 22–26 migration period → see archived tracker `dev/2026/04/{28,30}/exec-open-items-tracker.md`
- M1 + M2 sprint (Apr 10–16) → archived

---

## Disposition Policy

- Items carried >14 days without progress: force a decision at the reconciliation surfacing the gap (do / defer-with-explicit-reason / drop)
- Items moved to Backburner: reviewed monthly or at sprint gate
- Completed items: kept for one cycle, then removed
- **Discipline note**: HOST 360 commitment #2 (Apr 27) made this header convention permanent; applied at every reconciliation, not at session-end emergency.

---

*Maintained by: Chief of Staff, Executive Office (exec-opus, Code instance)*
*Filename: exec-open-items-tracker.md*
*Update trigger: end of every exec session + during PM-directed reconciliations + post-multi-day-gap resume*
