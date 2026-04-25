# Executive Office: Open Items Tracker

> **Living document** — updated at the end of every exec session.
> This is the canonical list of tracked items. Session logs may contain discussion but this file is the source of truth.
> Last updated: 2026-04-22, ~6:30 PM (exec session 8 — pre-migration reconciliation)

---

## Context Note

This is the pre-migration state snapshot. HOST migration to Code is in progress today; CIO is next. By the time I (CoS) migrate, this tracker will itself be handed off to my Code successor. Items here have been reconciled against omnibus logs through Apr 16 and Ship #039 workstream memos covering Apr 17-21.

Several migration-era items have been added to the tracker itself, since migration coordination is now a standing concern until all Chat roles are moved.

---

## Active Items

| # | Item | Owner | Opened | Status | Notes |
|---|------|-------|--------|--------|-------|
| 1 | Role migration: Chat → Code/Cowork | PM + exec | Apr 21 | HOST in progress | HOST handoff finalized Apr 22. CIO next. Remaining: CXO, PPM, Architect, Comms. Exec last. PM stays in Chat. |
| 2 | Migration checklist adoption | HOST + exec | Apr 22 | Proposed, pending PM approval | 4-phase checklist drafted by HOST. Exec reviewed and approved with minor notes. Ready for use starting with CIO. |
| 3 | Agent 360 Round 2 deployment | HOST + PM | Apr 22 | In progress | v0.2 questionnaire. Deployed during migration-prep conversations with each role. HOST completed first. Benchmarking round ~6 weeks post-migration. |
| 4 | Ship #039 "The Voice Takes Shape" | PM | Apr 19 | Draft complete | ~2,200 words, corrected after fact-check. Awaiting PM review + publish. |
| 5 | Alpha tester phase closure | PM + HOST | Mar 14 | HOST concurs, decision pending | 39+ days silent, 13 testers, zero responses. HOST flagged 5x. PM considers phase effectively ending. Needs: closure message + separate Ted/Dominique tracking. |
| 6 | team-structure.md staleness | Docs + HOST | Apr 16 | 113+ days stale, highest priority doc fix | Doesn't list PA, PPM, CXO, ETA, Mobile. Still says "HOSR not yet created." HOST flagged as highest priority. |
| 7 | HOST briefing rename + refresh | Docs | Apr 2 | Operational rename done | Briefing doc still `BRIEFING-ESSENTIAL-HOSR.md` with Mar 17 content. Part of Phase 4 of HOST migration (post-Code landing). |
| 8 | BoundaryEnforcer activation (#964) | CXO + Lead Dev | Apr 16 | Voice guidance delivered, activation pending | Pending false-positive rate validation against canonical corpus. Currently disabled in production. |
| 9 | PDR-004 corrections on Medium/LinkedIn | PM + Docs | Apr 16 | Pending | "Presence over performance" vs. "patience over performance" paraphrase propagated to two published posts. Canonical term verification now in omnibus skill. Still need to correct posts. |
| 10 | PA cross-project comms gap | PA + PM | Apr 9 | Ceiling moment logged | Dispatch messages invisible from PM repo. Protocol fix needed. |
| 11 | PM mail delivery bottleneck | PM | Apr 16 | Structural question | Apr 16: 37+ memos manually shuttled. Scaling constraint on high-coordination days. Migration to Code should substantially address this; deferred until measurable post-migration. |
| 12 | Cross-pollination hook update | Lead Dev | Mar 31 | Memo delivered, not executed | Small task, deprioritized during UAT and M2 sprint. Check if still relevant post-migration. |

### ⚠️ DISPOSITION FLAGS (>14 days without progress)

| # | Item | Owner | Opened | Days | Recommendation |
|---|------|-------|--------|------|----------------|
| D1 | Ship #034 title correction | PM/Comms | Mar 21 | 32 | Editorial calendar entry. Quick fix or drop? Long past disposition threshold. |

*Previously flagged items now resolved or naturally folding into migration:*
- ~~D1 (Automated omnibus pilot)~~ — **SUPERSEDED.** Dispatch operational and in active use. Evaluation complete by practice.
- ~~D3 (Agent 360 synthesis)~~ — **SUPERSEDED.** Action items from Round 1 already extracted (Colleague Test, Roundtable Synthesis, CIO reassurance). Round 2 now in progress.
- ~~D4/D5/D6 (CIO audit A1/A2/A3)~~ — **DEFERRED to CIO migration.** Three bounded tasks (30/15/15 min). Natural to pick up in Code environment with direct filesystem access. Revisit with CIO post-migration.

### Human Network (escalation items)

| Person | Status | Days | Next Action Needed |
|--------|--------|------|--------------------|
| Alpha testers (13) | **39+ days, zero responses** | 39+ | HOST flagged 5x. PM considers phase ending. Decision needed: closure message + separate Ted/Dominique tracking. |
| Dominique Derosena | **40+ days, no reply** | 40+ | 500 error (web wizard migration) may now be fixed. Worth a 1:1 follow-up with that context. Different from group re-engagement. |
| Ted Nadeau | Active advisor | — | Security.md, Methodology.md reviews pending. Janus opened formal channel Apr 3. Track separately from alpha cohort. |
| Cindy Chastain | Podcast released ~Mar 31 | — | "The Moment We're In" published. No action needed. |
| Dave Romero | Pitch outcome unknown | — | No change. |
| Sam Zimmerman | Dormant advisor | — | Acknowledge formally as dormant with completed contributions. |

## Backburner

| # | Item | Owner | Opened | Notes |
|---|------|-------|--------|-------|
| B1 | Website v3 copy execution | PM | Feb 22 | Low priority until beta |
| B2 | CIO innovation backlog location | PM/CIO | Apr 2 | Missing after kindsys→designinproduct migration. Locate or reconstruct. Natural task for CIO-in-Code. |
| B3 | Colleague Test v2 monitoring integration | HOST | Apr 19 | CXO distributed v2 Apr 19. HOST to incorporate into next health check cycle post-migration. |
| B4 | Context-age monitoring for Chat sessions | HOST | Apr 16 | Recommendation from HOST health check. Becomes less relevant post-migration (Code sessions work differently). Defer until we understand Code session patterns. |

## Recently Completed

### Migration coordination (Apr 21-22)
| Item | Completed | Notes |
|------|-----------|-------|
| Migration decision confirmed | Apr 21 | All Chat roles → Code/Cowork. Sequencing: HOST+CIO first, exec last, PM stays. |
| HOST migration handoff memo | Apr 22 | 6-section structure. Finalized after single review pass. Pattern for subsequent migrations. |
| Migration checklist drafted | Apr 22 | HOST-authored, exec-reviewed. 4 phases: Pre / During / First Code Session / Follow-Up. |
| Agent 360 v0.2 questionnaire | Apr 22 | Pre-migration baseline version. Deployed during migration-prep conversations. HOST completed first. |
| Workstream memo naming standard | Apr 19 | `workstream-{ship#}-{role}-{date}.md`. Effective Ship #040 onward. |
| HOST verifiable-claims memo | Apr 19 | Guidance to flag unverified comparative claims, ask PA/Docs for statistics. Standing norm. |

### M1 + M2 sprint (Apr 10-16)
| Item | Completed | Notes |
|------|-----------|-------|
| M1 gate CLOSED | Apr 11 | 4 UAT rounds: 0/9, 0/9, 5/9, 7/9. 33 days total. Gate methodology validated. |
| M2a (Foundation Cleanup) | Apr 12 | 10/10 issues. 7 in one day Apr 12. Quality 59%→65.6%, routing 41%→95.1%. |
| M2b (Testing Infrastructure) | Apr 14-15 | Full 3-tier CI: E2E + canonical + AAXT. Built in one afternoon. |
| M2c (Floor Prompt & Voice) | Apr 16 | #950 Five Pillars + Grammar. Quality 65.6%→72.1%. Ethics voice guidance. |
| Floor inversion trilogy | Apr 13 | #925 STATUS + PRIORITY. ADR-060 fully realized. |
| Vision V2.3 adopted | Apr 11 | Three iterations. Differentiator stack. Four leadership reviews endorsed. |
| Roadmap v15.0 published | Apr 11 | Restructured around differentiator stack. |
| Sprint reassignment executed | Apr 11-12 | 10 new issues, 12 closures, ~40 reassignments. |
| Ship #038 "The Floor Comes Alive" | Apr 15 | LinkedIn + pipermorgan.ai |
| Haiku 3 retirement (#979) | Apr 15 | 4 days before deprecation deadline. |
| Ruff migration (#981) | Apr 16 | black/isort/flake8 consolidated. 74 files reformatted. |
| PDR-004 correction chain | Apr 16 | 4-agent chain. Canonical term verification added to omnibus skill. |
| CIO methodology audit | Apr 17 | M1 audit, 12 recommendations. Excellence Flywheel reconciliation decided. |
| IAC talk delivered | Apr 17 | "Ethics as Information Architecture" — Philadelphia |
| Six-act inversion arc complete | Apr 14 | "The Closing Sprint" closed 6-week narrative arc. |
| Stacked Silent Failures formalized | Apr 16 | CIO named the M1 diagnostic pattern. |

### Previously tracked items now closed
| Item | Completed | Notes |
|------|-----------|-------|
| IAC presentation prep | Apr 17 | Delivered in Philadelphia. |
| Sprint reassignment plan | Apr 12 | Executed. |
| Vision V2.2 leadership review | Apr 11 | All four leadership reviews returned, V2.3 adopted. |
| #922 conversation continuity | Apr 9 | Missing response field — memory fix. |
| #943 GitHub pre-flight | Apr 9 | Third attempt, catch-block approach. |
| #949 server restart reliability | Apr 12 | Closed in M2a sprint. |
| Building narrative gap | Apr 14 | Six-act arc closed, pipeline refilled (7 new drafts). |
| Ship #037 "New Ground" | Apr 8 | LinkedIn + pipermorgan.ai |

---

## Disposition Policy

- Items carried >14 days without progress: force a decision (do / defer / drop)
- Items moved to Backburner: reviewed monthly or at sprint gate
- Completed items: kept for one cycle, then removed

---

*Maintained by: Chief of Staff, Executive Office*
*Filename: exec-open-items-tracker.md*
*Update trigger: end of every exec session*
*Next major revision: post-migration (Code successor)*
