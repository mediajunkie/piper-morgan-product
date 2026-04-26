# Executive Office: Open Items Tracker

> **Living document** — updated at the end of every exec session.
> This is the canonical list of tracked items. Session logs may contain discussion but this file is the source of truth.
> Last updated: 2026-04-26, ~2:00 PM PT (exec Code session 1 — post-migration reconciliation, captain-last complete)

---

## Context Note

This is the first reconciliation in Code. Predecessor (Chat instance) flagged the tracker as 14 days stale at hand-off; reconciled here against omnibus logs Apr 22 → Apr 26 plus today's full Phase E/F traffic. All seven leadership migrations are now complete (HOST Apr 22, CIO Apr 23 morning, Comms Apr 23 evening, CXO Apr 25, PPM Apr 25, Architect Apr 26 morning, exec Apr 26 afternoon). PM stays in Chat per the original migration plan.

The disposition policy (>14 days without progress → do/defer/drop) is applied below, including to two items the predecessor named in handoff Section 6 as discipline failures (items 10 and 12 in the prior tracker).

---

## Active Items

| # | Item | Owner | Opened | Status | Notes |
|---|------|-------|--------|--------|-------|
| 1 | **#992 Phase F flag-flip — held** | PM + PPM + Lead Dev + Architect | Apr 26 | DO NOT AUTHORIZE pending #1002 + #1003 | PM+PA co-signed decision today. Diagnostic confirmed flag is observably inert for naturally-phrased HARASSMENT (4-of-4 vectors no-op); flag matters for PROFESSIONAL. Architect reframe: detector brittleness, not routing. Fix shape B+C1 (~5–7 days). Re-evaluation conditional on #1002+#1003 close + additional vectors evidence + CXO independent scoring. |
| 2 | **#1002 — pre-classifier shadows ethics floor** (umbrella) | Architect → Lead Dev | Apr 25 | Scoping landed; awaiting B+C1 sibling issue + implementation | Architect confirmed dispatch order is correct; bypass mechanism is detector brittleness. Lead Dev concurs on B+C1. PM call pending on whether to file sibling P1 issue or scope under #1002. |
| 3 | **#1003 — harassment vector classified GUIDANCE; BoundaryEnforcer not engaged** | Architect → Lead Dev | Apr 26 | AC#1 met (decisive); AC#2-#3 pending Architect scoping + Lead Dev follow-up | Includes V3 mystery `decline_inappropriate_request` path — separate undocumented mechanism worth Architect investigation. |
| 4 | **Rubric C-axis discipline reconciliation** | PPM (lead) + CXO + Lead Dev + CIO | Apr 26 | Convergence pending (today/tomorrow) | Phase E rubric C=Clarity vs CT v2 C=Context. PPM lean: Option 1 (anchor Phase E to CT v2). PM 04-26 framing: catch drift at notice, not at v2.x. Test of the discipline. Verdicts unaffected. |
| 5 | **Branch discipline — 5-rule proposal** | PA (aggregator) + CXO (origin) + HOST/Docs/LD/Exec/PPM | Apr 26 | EOD today — responses converging | Lead Dev replied (Rule 2 SessionStop hook feasible+cheap; Rule 3 per-sender segment files). PPM replied (Rule 1+2 high value, Rule 5 low urgency). Exec response (Rule 5 ownership) due today. HOST + Docs replies pending. |
| 6 | **Migration checklist v1.1** | HOST (lead) + exec (review) | Apr 22 | HOST drafting | Phase 3 first-week findings to roll up: worktree/push lesson, standing-file routine convention, four workstream specifications, plus CXO Finding A (outputs-pending-commit-before-retirement) and PPM Finding A (worktree-vs-main path discipline). HOST committed at Apr 22 ack. |
| 7 | **Codification of handoff review pattern** | exec | Apr 26 | Methodology debt named in handoff §6 | Pattern exists across six review memos but not as referenceable artifact. ~half-day work. Within first month per startup prompt Task 8. Compounding value: future role transitions inherit documented practice rather than reconstructing from memos. |
| 8 | **Ship #040 workstream review (Apr 17–23)** | exec (synthesis) + all six role memos | Apr 23 (window close) | All team in Code; PM has confirmed memos available; review starts this session | First Code-era Ship synthesis. Naming standard from Apr 19 applies. Verifiable-claims discipline applies. C=2 dominance signal (PPM scoring memo) likely a narrative thread. |
| 9 | **Janus → exec (OpenLaws Bet 1, 6 questions)** | exec + PA (PA decides allocation w/ PM input) | Apr 25 | Allocation proposal forwarded to PA Apr 26; awaiting PA's confirmed cut | 5–7 day window (sprint Apr 27 – Jun 7). Lean: PA Q1/Q3/Q4; CoS Q5; either Q2; PM Q6. |
| 10 | **Janus → exec (PO advice relay, 2 questions)** | exec | Apr 25 | Reply drafted + PM-approved Apr 26 ~14:05; queued for relay | Filed at `mailboxes/exec/outbox/memo-exec-to-janus-po-advice-reply-2026-04-26.md`. Awaiting clarification from PM (who is asking Janus) on the cross-project signaling mechanism. |
| 11 | **Agent 360 Round 2 benchmarking** | HOST + PM | Apr 22 | All seven leadership 360 v0.2 responses delivered | Benchmarking ~6 weeks post-migration. HOST owns synthesis. Section 6 thematic-convergence finding worth a separate look (predecessor flagged in handoff §6 + 360 §9.3). |
| 12 | **CXO/PPM briefing correction memos → Docs** | Docs (act) + CXO + PPM (filed) | Apr 25–26 | Filed; awaiting Docs action | Both note CLAUDE.md role table omits CXO/PPM (Architect likely also). Both flag M1 staleness, Code-era tool references, structural gaps. Within 2 weeks per CXO/PPM suggested priority. |
| 13 | **Alpha tester phase closure** | PM + HOST | Mar 14 | 43+ days, decision pending | HOST flagged 5x. PM considers phase effectively ending. Needs: closure message + separate Ted/Dominique tracking. |
| 14 | **PDR-004 corrections on Medium/LinkedIn** | PM + Docs | Apr 16 | 10 days, status unknown | "Presence over performance" vs. "patience over performance" paraphrase. Canonical term verification now in omnibus Step 7. Posts still need correction. Verify with Docs. |
| 15 | **team-structure.md staleness** | Docs + HOST | Apr 16 (re-flagged) | 117+ days stale | Highest-priority doc fix per HOST. Doesn't list PA, PPM, CXO, ETA, Mobile. Adjacent to CLAUDE.md role table omissions in #12. |
| 16 | **`known_pathological` corpus tagging** | Lead Dev | Apr 16 | Memo delivered, status unknown | Predecessor recommendation. PA also surfaced as unknown-status in coordination check today. Worth a Lead Dev signal soon. |

### ⚠️ DISPOSITION FLAGS — Force-Decided This Session

| Prior # | Item | Days | Decision | Disposition |
|---------|------|------|----------|-------------|
| **10** | PA cross-project comms gap (Dispatch invisibility from PM repo) | 17 | **DO — escalate this week** | Per predecessor handoff §2 + §6 candor. Filing as memo to Architect (or Lead Dev if Architect prefers handoff). The protocol fix is technical-architecture scope. Effective with this reconciliation: removed from open-items, replaced by Item 17 below. |
| **12** | Cross-pollination hook update | 26 | **KEEP TRACKED — PM 04-26 "better safe than sorry"** | Returns to active items as #18. Memo to Lead Dev Mar 31 status: delivered, not executed. Periodic nudge cadence; if Lead Dev confirms the ask is no longer load-bearing, then drop. Until then, hold open. |
| **D1** | Ship #034 title correction | 36 | **DROP** | Long past disposition threshold; editorial calendar artifact at this point. Confirm with Comms/PM if any nuance, otherwise drop. |

| 17 | **PA cross-project comms gap → escalation** | exec → Architect | Apr 26 | New, post-disposition | Replaces prior item 10. Memo to Architect this week per predecessor force-decide. |
| 18 | **Cross-pollination hook update** | Lead Dev | Mar 31 | Memo delivered, not executed; PM 04-26 "better safe than sorry" — kept tracked | Returns from prior #12 disposition. Periodic nudge cadence; ping Lead Dev when convenient. |

### Human Network (escalation items)

| Person | Status | Days | Next Action Needed |
|--------|--------|------|--------------------|
| Alpha testers (13) | **43+ days, zero responses** | 43+ | HOST flagged 5x. PM considers phase ending. Decision needed: closure message + separate Ted/Dominique tracking. (Item 13 above.) |
| Dominique Derosena | **44+ days, no reply** | 44+ | 500 error (web wizard migration) may now be fixed. Worth a 1:1 follow-up with that context. Different from group re-engagement. |
| Ted Nadeau | Active advisor | — | Security.md, Methodology.md reviews pending. Janus opened formal channel Apr 3. Track separately from alpha cohort. |
| Cindy Chastain | Podcast released ~Mar 31 | — | "The Moment We're In" published. No action needed. |
| Dave Romero | Pitch outcome unknown | — | No change. |
| Sam Zimmerman | Dormant advisor | — | Acknowledge formally as dormant with completed contributions. |

## Backburner

| # | Item | Owner | Opened | Notes |
|---|------|-------|--------|-------|
| B1 | Website v3 copy execution | PM | Feb 22 | Low priority until beta |
| B2 | CIO innovation backlog location | PM/CIO | Apr 2 | Missing after kindsys→designinproduct migration. CIO now in Code; natural to pick up. |
| B3 | Colleague Test v2 monitoring integration | HOST | Apr 19 | CXO distributed v2 Apr 19. HOST to incorporate into next health check cycle post-migration. |
| B4 | Context-age monitoring for Chat sessions | HOST | Apr 16 | Becomes less relevant post-migration. Defer until we understand Code session patterns. |
| B5 | `workstream-review` skill draft | exec | Apr 22 | Deferred until post-Ship #040 cycle. Should be drafted within ~2 weeks. Codifies four specs (week, scope, naming, format) + verifiable-claims discipline. |
| B6 | V3 mystery `decline_inappropriate_request` path investigation | Architect | Apr 26 | Architect bandwidth-permitting; not Phase F-blocking. Sharpens architectural picture before B+C1 ships. |

## Recently Completed

### Apr 22 – Apr 26 (migration period)
| Item | Completed | Notes |
|------|-----------|-------|
| All seven leadership migrations | Apr 22–26 | HOST, CIO, Comms, CXO, PPM, Architect, exec (this session). Captain-last principle held. |
| HOST migration handoff memo | Apr 22 | 6-section structure validated across all seven. |
| Migration checklist (v1.0) | Apr 22 | HOST-authored, exec-reviewed. v1.1 pending HOST. |
| Workstream memo naming standard | Apr 19 | `workstream-{ship#}-{role}-{date}.md`. Effective Ship #040. |
| Verifiable-claims memo | Apr 19 | Standing norm. |
| Six handoff reviews delivered | Apr 22–25 | HOST 5+1, CIO 4, Comms 3+1, CXO 2, PPM 1+2, Arch 0+1. Decreasing volume = pattern stabilization. |
| Per-memo commit-and-push norm | Apr 26 | CXO-established. Eliminates asymmetric-visibility windows. Memory saved. |
| Phase E gate closure | Apr 26 | All three scenarios PASS R/C/T. CXO 9/9/9, PPM 7/9, 8/9, 8/9. No tiebreak. Closes cleanly, separately from Phase F. |

### M1 + M2 sprint (Apr 10-16) — preserved from prior reconciliation

(See dev/2026/04/22 archive for full prior-period record. Items folded for legibility.)

---

## Disposition Policy

- Items carried >14 days without progress: force a decision (do / defer / drop)
- Items moved to Backburner: reviewed monthly or at sprint gate
- Completed items: kept for one cycle, then removed
- **Discipline note**: predecessor flagged in handoff §6 that this policy fails when not applied. Applied this session; should re-apply at every reconciliation, not at session-end emergency.

---

*Maintained by: Chief of Staff, Executive Office (exec-opus, Code instance)*
*Filename: exec-open-items-tracker.md*
*Update trigger: end of every exec session*
*Reconciliation cadence target: weekly*
