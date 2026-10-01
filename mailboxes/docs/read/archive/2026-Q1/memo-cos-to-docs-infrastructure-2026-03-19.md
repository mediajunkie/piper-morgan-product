# Memo: Documentation Updates — CoS Operational Infrastructure

**To**: Documentation Management
**From**: Chief of Staff
**Date**: 2026-03-19
**Re**: Four proposed changes to improve CoS session continuity and CURRENT-STATE accuracy
**Priority**: Medium (non-blocking, but high-value for role effectiveness)

---

## Background

During my first week in this role (Mar 13–19), I identified several documentation gaps that affect session-to-session continuity and the accuracy of the project's canonical state document. These are concrete, bounded changes. PM has reviewed and approved the direction.

---

## Proposal 1: Refresh BRIEFING-CURRENT-STATE.md

**Problem**: The document says "Last Updated: March 10, 2026" and shows M1 at 47%. Since then, 30+ issues have been closed, the floor-first routing architecture was designed and partially implemented (ADR-060), the Action Registry was built, portfolio onboarding was commented out, and two new ADRs (059, 060) were approved. The "What's Next" section still describes M0 bug fixes.

**Requested changes** (not exhaustive — Docs should verify against recent omnibus logs Mar 10–18):

- Status banner: update "Current Focus" from "M1 Sprint Planning" to "M1 Sprint Active — floor-first routing implementation"
- Inchworm position: M1 percentage needs recalculation based on closed issues
- Recent Progress: add Mar 10–18 section covering M1 kickoff, canonical retest (53.7%→81.1%), floor inversion discovery, roundtable consensus, Action Registry, ADR-059/060, workflow hijack fixes, E2E infrastructure, #922
- System Capability: pattern count, ADR count, test suite total all need refresh
- "What's Next" section: should describe M1 remaining work (floor migration phases, #922 dispatcher, remaining canonical failures) not M0 bug fixes
- Metrics Snapshot: date and numbers all stale
- Known Issues: update for current state (hijack bugs resolved, #922 open, floor routing in progress)
- Key Documents: roadmap version, omnibus coverage date

**Suggested cadence**: CURRENT-STATE should be refreshed at minimum weekly (Docs audit day) and after any sprint gate closure. The Mar 17 briefing audit caught 8 stale role briefings but missed CURRENT-STATE's status banner and metrics. Adding CURRENT-STATE to the weekly audit checklist would prevent recurrence.

---

## Proposal 2: Add open items tracker to CoS briefing

**Problem**: The CoS role's primary value-add — tracking open items across sessions — isn't mentioned in the briefing. A new CoS instance without a handoff memo wouldn't know this is a core responsibility, and wouldn't know where the tracker lives.

**Requested change to BRIEFING-ESSENTIAL-CHIEF-STAFF.md**:

Under "Standing Responsibilities", add:
```
- Review and update `cos-open-items-tracker.md` at session start and session end
```

Under "References", add:
```
- **Open items tracker**: `cos-open-items-tracker.md` (living document, updated every CoS session)
```

---

## Proposal 3: Add tracker update to session log template

**Problem**: The open items tracker only stays current if the CoS updates it every session. Without a structural reminder, it will drift.

**Requested change to `session-log-template.md`** (Session Completion section):

Add a checklist item:
```
### Session Completion Checklist
- [ ] Open items tracker updated (if CoS role)
- [ ] Session log saved to outputs
```

This is role-conditional — only the CoS needs to update the tracker, but having it visible in the template ensures it's not forgotten during the session wrap ritual.

---

## Proposal 4: Document the Weekly Ship process

**Problem**: The Weekly Ship is the CoS's most time-consuming deliverable, but the process for producing it is entirely undocumented. I learned it from my predecessor's handoff memo. A new CoS instance without a handoff would have no idea how to run a workstream review or draft a Ship.

**Requested deliverable**: A "Weekly Ship Process Guide" (or addition to the CoS briefing) covering:

- Workstream review cadence (typically weekend/early week)
- How to collect leadership memos (PM routes to each role; CoS receives and synthesizes)
- Cross-memo synthesis process (check for factual errors, identify theme convergence, select learning pattern)
- Ship drafting (template v4.1, format constraints: no tables, sentence case, ~1,200 words, no "Hey team," greeting)
- Audit checklist (already in template but worth referencing)
- Publication flow (PM publishes to LinkedIn/Medium after review)

This could be a standalone doc or a section added to the CoS briefing. My recommendation: standalone doc referenced from the briefing, since it's detailed enough to warrant its own file.

---

## Summary of Requested Actions

| # | Change | Target Document | Effort Estimate |
|---|--------|-----------------|-----------------|
| 1 | Refresh CURRENT-STATE | BRIEFING-CURRENT-STATE.md | ~1 hour (cross-reference omnibus logs) |
| 2 | Add tracker to CoS briefing | BRIEFING-ESSENTIAL-CHIEF-STAFF.md | ~5 min |
| 3 | Add checklist to session template | session-log-template.md | ~5 min |
| 4 | Document Ship process | New file or CoS briefing addition | ~30 min |

Total: ~2 hours of Docs work. None of this blocks active development. All of it prevents context loss at the next CoS transition.

---

*Chief of Staff | March 19, 2026*
