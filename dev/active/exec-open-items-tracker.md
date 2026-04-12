# Executive Office: Open Items Tracker

> **Living document** — updated at the end of every exec session.
> This is the canonical list of tracked items. Session logs may contain discussion but this file is the source of truth.
> Last updated: 2026-04-11, 12:45 PM (exec session 5)

---

## Active Items

| # | Item | Owner | Opened | Status | Notes |
|---|------|-------|--------|--------|-------|
| 1 | M1 gate (#926) Round 4 re-test | PM + CXO | Mar 22 | All blockers fixed Apr 9 | 3 rounds: 0/9, 0/9, 5/9. #922 + #943 fixed. Re-test pending PM+CXO availability. |
| 2 | IAC presentation (Apr 17) | PM + Comms | Mar 30 | **6 DAYS OUT** | Deck + notes exist. PA flagged 80.3% claim needs verification. Approaching urgency. |
| 3 | Sprint reassignment plan | PA + PM | Apr 8 | Ready, not reviewed | 12 closures, ~40 reassignments, 5 renames, 10 new issues. Needs PPM/CXO/Arch review before execution. |
| 4 | Vision V2.2 leadership review | PM | Apr 8 | Review memos queued | CXO and PPM have memos. Arch needs MCP prototype scoping memo. |
| 5 | Ship #038 draft | PM | Apr 11 | Draft complete | "The Floor Comes Alive" — awaiting PM review + publish. |
| 6 | Cross-pollination hook update | Lead Dev | Mar 31 | Memo delivered, not executed | Small task, deprioritized during UAT remediation. |
| 7 | HOST briefing rename + refresh | Docs + HOST | Apr 2 | Operational rename done | Briefing doc still has old name (HOSR) and stale content. |
| 8 | #949 server restart reliability | Lead Dev | Apr 7 | Filed | Affects UAT confidence. Recurring "fix deployed but not running" friction. |
| 9 | Building narrative gap | Comms | Apr 9 | After Apr 14 | Acts 1-5 published, Act 6 scheduled Apr 14. No next arc queued. UAT story is obvious candidate. |
| 10 | PA cross-project comms gap | PA/PM | Apr 9 | Ceiling moment logged | Dispatch messages invisible from PM repo. Protocol fix needed. |

### ⚠️ DISPOSITION FLAGS (>14 days without progress — force decision)

| # | Item | Owner | Opened | Days | Recommendation |
|---|------|-------|--------|------|----------------|
| D1 | Automated omnibus pilot | PM/Docs | Mar 20 | 22 | Dispatch is now operational. Is this still a separate evaluation, or has it been superseded? |
| D2 | Ship #034 title correction | PM/Comms | Mar 21 | 21 | Editorial calendar entry. Quick fix or drop? |
| D3 | Agent 360 synthesis | HOST | Mar 19 | 23 | 9/9 collected. Is full synthesis still planned, or have the action items (Colleague Test, Roundtable Synthesis, CIO reassurance) already extracted the value? |
| D4 | CIO audit A1 (Hooks monitoring) | CIO/Docs | Mar 22 | 20 | 30 min task, not started. Do or defer to M2? |
| D5 | CIO audit A2 (methodology-core issue) | CIO | Mar 22 | 20 | 15 min task, not started. Do or defer to M2? |
| D6 | CIO audit A3 (docs audit template) | Docs | Mar 22 | 20 | 15 min task, not started. Do or defer to M2? |

### Human Network (escalation items)

| Person | Status | Days | Next Action Needed |
|--------|--------|------|--------------------|
| Alpha testers (13) | **27+ days, zero responses** | 27+ | HOST has flagged 3x. PM decision: different channel, adjusted ask, 1:1 outreach, or acknowledge cohort didn't activate. |
| Dominique Derosena | **34 days, no reply** | 34 | 500 error root cause (web wizard migration) may now be fixed. Worth a follow-up with that context? |
| Ted Nadeau | Active, 2 docs pending | — | Security.md, Methodology.md reviews. Janus opened formal channel Apr 3. |
| Cindy Chastain | Podcast released ~Mar 31 | — | "The Moment We're In" published. No action needed. |
| Dave Romero | Pitch outcome unknown | — | No change. |
| Sam Zimmerman | Dormant | — | No change. |

### CIO Methodology Audit Recommendations (triaged from Mar 15 audit)

**Done** (4 of 10):
- ~~Rec 1~~: Pattern-062 commit — signed off Mar 21
- ~~Rec 5~~: CIO self-approval for Emerging patterns — policy approved Mar 16
- ~~Rec 8~~: Roundtable format documented — Methodology-22, delivered Mar 21
- ~~Rec 9~~: Trigger-based audit cadence — policy approved Mar 16

**Bounded tasks** (3 remaining — see D4/D5/D6 above for disposition):

| # | Rec | Action | Owner | Effort | Status |
|---|-----|--------|-------|--------|--------|
| A1 | 2 | Hooks Phase 1 monitoring check | CIO or Docs | 30 min | Not started (22 days) |
| A2 | 3 | File issue for methodology-core refresh | CIO | 15 min | Not started (22 days) |
| A3 | 4 | Add methodology-core staleness check to audit template | Docs | 15 min | Not started (22 days) |

**Needs scoping** (3 of 10):

| # | Rec | Action | Owner | Notes |
|---|-----|--------|-------|-------|
| S1 | 6 | Codify AX Testing questionnaire template | ETA + PM | Deferred per PA routing |
| S2 | 7 | Add product coherence check to CXO testing protocol | CXO + PPM | CXO deferring until after UAT settles |
| S3 | 10 | Monitor methodology-product convergence latency | CIO | Ongoing awareness, no action needed |

## Backburner

| # | Item | Owner | Opened | Notes |
|---|------|-------|--------|-------|
| B1 | Website v3 copy execution | PM | Feb 22 | Low priority until beta |
| B2 | Agent 360 questionnaire v0.2 review | PM | Mar 8 | v0.1 deployed successfully |
| B3 | CIO innovation backlog location | PM/CIO | Apr 2 | Missing after migration. Locate or reconstruct. |

## Recently Completed

| Item | Completed | Notes |
|------|-----------|-------|
| Ship #037 "New Ground" published | Apr 8 | LinkedIn + pipermorgan.ai Shipping News |
| M1 UAT Round 3 breakthrough | Apr 8 | 5/9 pass. Floor alive for first time. |
| All 5 original UAT findings fixed | Apr 5 | #940, #939, #943, todo parsing, input parsing |
| #922 conversation continuity fixed | Apr 9 | Missing response field — Piper's replies never stored in memory |
| #943 GitHub pre-flight fixed | Apr 9 | Third attempt; catch-block approach |
| #942 orchestration tables | Apr 7 | Migration for 4 tables, 6 tests fixed (6,303→6,309) |
| #934 dead code removed | Apr 7 | 675 + 597 lines, never mounted |
| 1,272 LOC dead code removed | Apr 7 | Lead Dev housekeeping session |
| Vision V2 → V2.2 | Apr 8 | Three iterations, differentiator stack, BYOC, consciousness-as-architecture |
| MCPB feasibility confirmed | Apr 8 | Hybrid approach viable (MCPB for tools + Claude Project for persona) |
| CXO briefing refreshed | Mar 31 | Jan 5 → Mar 31. Current with Colleague Test, floor-first, M1 gate. |
| BRIEFING-CURRENT-STATE refreshed | Apr 7 | 9 days stale → current. New /update-current-state skill created. |
| RFC-001 bilateral response | Apr 2 | Both projects filed. Shared gap: strong L1-L2-L3, weak L4-L5. |
| Ship #036 published | Apr 1 | "Approaching the Gate" — LinkedIn + pipermorgan.ai |
| PA operational | Apr 1 | Analyst → strategist trajectory. 10 days, multiple original contributions. |
| TRACK-EPIC convention retired | Apr 7 | Replaced with milestone assignment check in audit template |
| 8 blog-first publishes (Apr 3-9) | Apr 9 | Highest volume in single Ship window |
| Publication cadence formalized | Apr 9 | Tue/Thu building, Sat/Sun insight pairs, Wed ship |

---

## Disposition Policy

- Items carried >14 days without progress: force a decision (do / defer / drop)
- Items moved to Backburner: reviewed monthly or at sprint gate
- Completed items: kept for one cycle, then removed

---

*Maintained by: Chief of Staff, Executive Office*
*Filename: exec-open-items-tracker.md*
*Update trigger: end of every exec session*
