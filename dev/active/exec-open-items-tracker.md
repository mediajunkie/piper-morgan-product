# Executive Office: Open Items Tracker

> **Living document** — updated at the end of every exec session.
> This is the canonical list of tracked items. Session logs may contain discussion but this file is the source of truth.
>
> **Disposition policy is operational, not aspirational** (per HOST 360 synthesis pull, Apr 27): at every reconciliation, every item is checked against the >14-day-zero-movement threshold and force-decided here (do / defer-with-explicit-reason / drop). Items don't get parked. If an item recurs at the threshold across reconciliations without movement, the role-holder owes an explicit reason or it drops on the next pass.
>
> Last updated: 2026-04-30, ~8:30 AM PT (exec Code session 5 — Day 5 morning, disposition-policy-as-permanent-convention codified per HOST 360 commitment #2)

---

## Context Note

Reconciliation following the Apr 27 #1004 SHIP day. Major closures: #1002, #1003, Phase E gate aftermath, Rubric C-axis discipline, OpenLaws Bet 1 bundle. Major opens: Phase F flag-flip authorization decision (now sits with PM/PA), ADR-061 in flight from Architect (Phase F prerequisite per Lead Dev recommendation), Ship #041 prep window (Apr 24–30 closes Thursday).

Disposition policy applied (>14 days without progress). All items below have either had progress in the last cycle or are flagged for force-decision next pass.

---

## Active Items

| # | Item | Owner | Opened | Status | Notes |
|---|------|-------|--------|--------|-------|
| 1 | **#992 Phase F flag-flip authorization** | PM/PA (decision) + Architect (ADR-061 prerequisite) | Apr 26 | All PPM v4 conditions met (Architect scoping ✓, #1002+#1003 close ✓, flag-matters diagnostic ✓, probe set + two calibration rounds ✓). Lead Dev recommendation: defer pending ADR-061. **Decision sits with PM/PA per Lead Dev memo `2322907a`** (Apr 27). |
| 2 | **ADR-061** (Floor-as-de-facto-ethics-layer + BoundaryEnforcer-as-literal-trigger-fast-path) | Architect | Apr 26 | Drafting; expected for Lead Dev today (Apr 28 per PM Apr 28 morning). | Phase F flag-flip prerequisite per Lead Dev recommendation. Codifies the architectural delta from #1004 ship. |
| 3 | **Ship #040 publication** | exec (draft done) → PM (voice pass) → Docs (publish) | Apr 26 (draft) | Draft at `dev/active/weekly-ship-040-draft-2026-04-26.md`; 4 feedback edits folded Apr 27. PM voice pass tomorrow (Apr 29) AM; Docs publish + LinkedIn syndication after. |
| 4 | **Ship #041 workstream review (Apr 24–30 window)** | exec (solicit + synthesize) | Apr 28 (window) | Solicitation memo to leadership cohort due Wednesday EOD. Window closes Thursday Apr 30. Substantial week material: #1004 ship, Phase F decision arc, migration arc completion, Methodology-24/25 filings, Pattern-063 ratification, Klatch MCP live, 360 round 2 cohort confer. |
| 5 | **Migration checklist v1.1** | HOST (lead) + exec (review) | Apr 22 | HOST drafting; status check pending | Phase 3 first-week findings to roll up. CXO Finding A (outputs-pending-commit-before-retirement), PPM Finding A (worktree-vs-main path discipline), captain-last sequencing, three-artifact package shape, Section 6 thematic-convergence framing. |
| 6 | **Codification of handoff review pattern** | exec | Apr 26 | Methodology debt named in predecessor handoff §6; first-month task | Pattern exists across six review memos but not as referenceable artifact. ~half-day work. Compounding value: future role transitions inherit documented practice. |
| 7 | **Branch-discipline aggregation → formal policy** | PA (aggregator) → PPM (synthesis) | Apr 26 | PA scoping ask to Lead Dev re `merge-keeper-sweep.sh` + `deliver-mail (b)` filed Apr 27. PPM hosting synthesis-into-formal-policy step pending aggregation. | Mailbox-discipline norm (mail-to-main-only + check-branch.sh) landed unilaterally Apr 26 ahead of broader 5-rule synthesis. Pattern-063 PM concurrence landed Apr 27 (PA memo `6d1c7062`). |
| 8 | **Cross-project comms gap escalation** | exec → Architect | Apr 28 (filed) | Filed to Architect today CC PA, PM. Asks Architect read on (a) architectural-protocol scope vs. (b) operational-convention scope vs. (c) already-solved-by-recent-work. PA may follow up with one-page framing per their Apr 27 offer. |
| 9 | **Briefing-freshness hook diagnosis** | exec → Docs (CC PM) | Apr 28 (filed) | Filed today. Diagnosis: hook threshold (>7 days) too lenient vs. skill's "more than a few days"; mechanism uses file mtime, not STATUS BANNER content-date. PM + Docs to discuss fix. | Briefing refreshed today (commit `670ef9c9`) per the standing protocol PM intends to make operational. |
| 10 | **Agent 360 Round 2 — synthesis cohort confer** | HOST (lead) + cohort | Apr 22 | HOST acking syntheses from PPM/CXO/Comms/CIO Apr 27. CIO migration-experience confer resurrected. Active. | All seven leadership 360 v0.2 responses delivered. Section 6 thematic-convergence finding flagged for separate look in post-migration synthesis. |
| 11 | **Briefing correction memos → Docs** | Docs (act) + CXO + PPM + CIO + exec (filed) | Apr 25–28 | All four filed; Docs working through. | All flag M1 staleness, Code-era references, structural gaps. CIO filed Apr 27. Within 2 weeks per author suggested priority. |
| 12 | **Alpha tester phase closure** | PM + HOST | Mar 14 | 45+ days, decision pending; PA noted in Apr 27 omnibus that PM's Apr 25 "phase effectively ended" framing landed in cohort signal but no formal closure message yet | Decision needed: formal closure message + separate Ted/Dominique tracking. |
| 13 | **PDR-004 corrections on Medium/LinkedIn** | PM + Docs | Apr 16 | 12 days, status unknown | "Patience over performance" paraphrase. Canonical-term verification now in omnibus Step 7. Posts still need correction. Verify with Docs. |
| 14 | **team-structure.md staleness** | Docs + HOST | Apr 16 (re-flagged) | 119+ days stale; highest doc-fix priority per HOST | Doesn't list PA, PPM, CXO, ETA, Mobile. Adjacent to CLAUDE.md role table omissions in #11. |
| 15 | **`known_pathological` corpus tagging** | Lead Dev | Apr 16 | Memo delivered Apr 16; status unknown | PA flagged unknown-status in Apr 27 coordination check. Worth a Lead Dev signal soon. May be subsumed by #1004 probe-set work. |
| 16 | **Cross-pollination hook update** | Lead Dev | Mar 31 | 28 days; PM 04-26 "better safe than sorry" — kept tracked | Periodic nudge cadence. Could surface in Lead Dev coordination today. |
| 17 | **PA tracker reconciliation partial-delegation** | PA (data-gathering) + exec (judgment) | Apr 26 | Pattern proposed in coordination-check exchange; awaiting first PA `tracker-prep:` pass | PA does periodic sweep (new/closed/aging items) before exec reconciliation; exec applies disposition judgment. Cleaner separation. Cadence target: weekly. |

### ⚠️ DISPOSITION FLAGS — None this cycle

All items above had progress in the last cycle or have a named owner with a current ETA. No items >14 days with zero movement.

### Human Network (escalation items)

| Person | Status | Days | Next Action Needed |
|--------|--------|------|--------------------|
| Alpha testers (13) | **45+ days, zero responses** | 45+ | Decision needed: formal closure message + separate Ted/Dominique tracking. (Item 12 above.) |
| Dominique Derosena | **46+ days, no reply** | 46+ | 500 error may now be fixed. 1:1 follow-up with that context. Different from group re-engagement. |
| Ted Nadeau | Active advisor | — | Security.md, Methodology.md reviews pending. Janus formal channel Apr 3. Track separately from alpha cohort. |
| Cindy Chastain | Podcast released ~Mar 31 | — | "The Moment We're In" published. No action needed. |
| Dave Romero | Pitch outcome unknown | — | No change. |
| Sam Zimmerman | Dormant advisor | — | Acknowledge formally as dormant with completed contributions. |

## Backburner

| # | Item | Owner | Opened | Notes |
|---|------|-------|--------|-------|
| B1 | Website v3 copy execution | PM | Feb 22 | Low priority until beta |
| B2 | CIO innovation backlog location | PM/CIO | Apr 2 | Missing after kindsys→designinproduct migration. |
| B3 | Colleague Test v2 monitoring integration | HOST | Apr 19 | CT v2.3 (with Branch-or-Anchor embed) committed Apr 27. HOST to incorporate into next health check cycle. |
| B4 | Context-age monitoring for Chat sessions | HOST | Apr 16 | Less relevant post-migration. Defer until we understand Code session patterns. |
| B5 | `workstream-review` skill draft | exec | Apr 22 | Deferred until post-Ship #040 publication. Codify four specs + verifiable-claims discipline. Methodology-25 (Workstream Review Cadence, filed Apr 27 by CIO) overlaps; coordinate before duplicating. |
| B6 | V3 mystery `decline_inappropriate_request` path investigation | Architect | Apr 26 | Resolved per Architect Apr 26 followup memo: not a separate mechanism — LLM classifier free-form action label. Subsumed by Fix B+C1 (#1004 SHIPPED Apr 27). **Move to Recently Completed.** |

## Recently Completed

### Apr 27–28
| Item | Completed | Notes |
|------|-----------|-------|
| **#1004 SHIP** (B+C1 semantic detector + Telemetry Phase 1 + literal-trigger backstop + audit-marker) | Apr 27 | Steps 8 + 9 in single Lead Dev session. 112/112 PASS across full ethics enforcement suite. Probe set + two calibration rounds (run-1 11/20 PASS → CXO prompt v0.2 → run-2 18/20 PASS). |
| **#1002** (pre-classifier shadows ethics floor) | Apr 27 | Closed with full evidence per close-issue-properly skill. |
| **#1003** (harassment vector classified GUIDANCE; BoundaryEnforcer not engaged) | Apr 27 | Closed with full evidence; AC#1 met decisively, AC#2-#3 met via #1004 ship. |
| **Rubric C-axis discipline reconciliation** | Apr 27 | Methodology-24 (Branch-or-Anchor) filed by CIO. CT v2.3 embeds Branch-or-Anchor rule directly in rubric. PPM filed C-axis closure memo. |
| **Methodology-24 (Branch-or-Anchor) filed** | Apr 27 | CIO. Durable safeguard parallel to PDR-004 Step 7. |
| **Methodology-25 (Workstream Review Cadence) filed** | Apr 27 | CIO. Codifies Fri-Thu most-recent-closed window + verifiable-claims + source discipline. |
| **Pattern-063 (Parallel-Authoring Drift) PM concurrence** | Apr 27 | PA memo `6d1c7062`. Sub-pattern of Pattern-062 with distinct mechanism from predecessor's "Extension Without Integration" candidate. |
| **OpenLaws Bet 1 reply bundle** | Apr 26–27 | PA filed Q1+Q2 + Q3 + Q4 to DinP relay surface. exec filed Q5 + Q2 (CoS-vantage independent answer) Apr 27. Q6 = PM call. Bundle complete. |
| **Janus PO advice relay** | Apr 26 | exec filed reply Apr 26; relayed via PM session walk on DinP side. |
| **Janus cross-project relay-reply convention** | Apr 26 | Janus filed convention memo. Filing into DinP working tree IS the signal; PM walks tree at next session. |
| **B6 V3 mystery decline path** | Apr 26 | Resolved via Architect followup: LLM classifier free-form action label, not a separate mechanism. Subsumed by Fix B+C1. |
| **Audit S3 Klatch AAXT scaffolded probing** | Apr 27 | CIO filed memo to Lead Dev. |
| **Audit S1 canonical-term-drift explicit** | Apr 27 | CIO filed memo to Docs. |
| **Audit-A3 disposition: retire** | Apr 27 | Lead Dev memo to CIO. |

### Apr 22–26 (migration period)
| Item | Completed | Notes |
|------|-----------|-------|
| All seven leadership migrations | Apr 22–26 | HOST, CIO, Comms, CXO, PPM, Architect, exec. Captain-last principle held. |
| HOST migration handoff memo | Apr 22 | 6-section structure validated across all seven. |
| Migration checklist v1.0 | Apr 22 | HOST-authored; v1.1 in flight. |
| Workstream memo naming standard | Apr 19 | `workstream-{ship#}-{role}-{date}.md`. Effective Ship #040. |
| Verifiable-claims memo | Apr 19 | Standing norm. |
| Six handoff reviews delivered | Apr 22–25 | HOST 5+1, CIO 4, Comms 3+1, CXO 2, PPM 1+2, Arch 0+1. Decreasing volume = pattern stabilization. |
| Per-memo commit-and-push norm | Apr 26 | CXO-established. CLAUDE.md-codified Apr 26 by Docs. |
| Mailbox-discipline norm (mail-to-main-only) | Apr 26 | Docs unilateral landing; check-branch.sh hook enforces. |
| Phase E gate closure | Apr 26 | All three scenarios PASS R/C/T. |

### M1 + M2 sprint (Apr 10-16)
(See archived tracker `dev/2026/04/22/exec-open-items-tracker.md` for full prior-period record.)

---

## Disposition Policy

- Items carried >14 days without progress: force a decision (do / defer / drop)
- Items moved to Backburner: reviewed monthly or at sprint gate
- Completed items: kept for one cycle, then removed
- **Cadence target**: weekly reconciliation. PA partial-delegation pattern (data-gathering pre-pass) in trial as of Apr 26 (item 17).

---

*Maintained by: Chief of Staff, Executive Office (exec-opus, Code instance)*
*Filename: exec-open-items-tracker.md*
*Update trigger: end of every exec session + during PM-directed reconciliations*
