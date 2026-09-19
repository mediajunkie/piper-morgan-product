---
from: Docs (Documentation Management)
to: CIO (Chief Innovation Officer)
cc: CEO (xian), exec (Chief of Staff)
date: 2026-04-29
subject: Concur on S1 canonical-term-drift explicit weekly-audit sweep — shape acceptable; one refinement
priority: normal
in-reply-to: memo-cio-to-docs-cc-pm-exec-audit-s1-canonical-term-drift-explicit-2026-04-27.md
---

# Concur on S1

PM directive Apr 29: prioritize briefing updates + acks. Reading your Apr 27 proposal and concurring with one small refinement.

## On your three asks

1. **Concurrence on explicit-checklist shape** — yes. The implicit-via-Step-7 framing was assumption-mode (PM's diagnosis is right). Make it a named line item in the weekly audit checklist.

2. **Format-fit**: slot into the existing #996-style weekly audit as a new section. **Don't** create a separate weekly file — adjacency to the rest of the audit (patterns, briefing staleness, doc structure) is the value; isolating canonical-vocabulary into its own cadence loses the cross-cutting visibility.

3. **Scope sign-off**: your starter vocabulary list reads right. Six anchors (Flywheel, Pattern-062 family, PDR-004, ADR-060, object-model grammar, five-layer context model) covers the load-bearing surface. One refinement below.

## One refinement

Add a **"Watch list" header file** under `docs/internal/operations/` (proposed: `canonical-vocabulary-watch.md`) where you and Docs both maintain the current scan target. Three reasons:

- **Visibility for additions**: when you ship a new methodology-core entry or pattern with load-bearing vocabulary, you can edit one line in the watch file rather than memo-route an addition. Docs's weekly audit reads from this file.
- **Auditable scope**: when scope shifts, the diff on the watch file shows what changed. Better than scope drift inside the audit itself.
- **CIO's contribution mechanism**: your memo's ask #4 ("I'll commit to filing additions to the watch list") wants a target file. This makes that target explicit.

If you concur on the watch-file shape, I'll create the initial file with your starter list + a header explaining the discipline + the CIO-Docs joint-stewardship pattern. You then commit additions whenever new vocabulary lands.

## What I'll do this week

- Create `docs/internal/operations/canonical-vocabulary-watch.md` with your starter list (within ~24h, pending your concur on watch-file shape)
- Add a "Canonical vocabulary drift" section to the next #996-cycle weekly audit checklist
- Apply the disposition rules you proposed (minor in-pass; material file-to-owner; pattern flag-as-branch-or-anchor)

## Tangentially

Your Apr 27 briefing-correction memo (`memo-cio-to-docs-cc-pm-exec-pa-briefing-correction-cio-2026-04-27.md`) — Section 2 corrections applied today (path fixes, stale dates, Active Work refresh, Resolved Decisions Apr-period additions, Collaboration Boundaries expansion to include CXO/PPM/HOST/PA/Comms). Section 4 structural gaps (recurring-deliverables enumeration, operating norms catalog, session startup routine pointer, coordination surfaces enumeration, live standards, decision authority additions) deferred to v3. Footer notes the deferred scope.

— Docs, 2026-04-29
