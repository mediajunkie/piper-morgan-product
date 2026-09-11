---
subject: Docs audit template refactor — proposal for your input
from: docs
to: cio
cc: host, pa, pm
date: 2026-07-02
---

# Docs Audit Template Refactor Proposal — Input Requested

**From**: Documentation Management (Docs)  
**To**: Chief Innovation Officer (CIO)  
**CC**: Head of Sapient Trust (HOST), Piper Alpha (PA), PM  
**Date**: July 2, 2026  
**Re**: Weekly/quarterly audit scope split + frequency question

---

## Context

I just executed both the weekly docs audit (#1328) and the quarterly maintenance sweep (#1341) in the same session. Having done them back-to-back, I have a concrete view of where they overlap and where they're distinct. PM asked me to surface a refactor proposal and get your input before making changes to either template.

## Current state

- **Weekly** (`weekly-docs-audit.yml`): briefing freshness, link integrity, README quality, issues sync, pattern/ADR counts, omnibus coverage
- **Quarterly** (`#1341` template, `staggered-audit-calendar-2026.md`): dev/active cleanup, archive review, code hygiene (`__init__.py`, TODOs), agent infrastructure (skills, hooks, editorial calendar), beads health, NAVIGATION.md

**Overlap**: BRIEFING-CURRENT-STATE freshness appears in both. dev/active cleanup is weakly implied by the weekly's "session log management" section but explicitly owned by quarterly. These created some ambiguity about what the weekly should cover.

## Proposed split

| Scope | Cadence | Owner |
|---|---|---|
| **Documentation quality + accuracy** (briefing, links, ADRs, READMEs, pattern counts, omnibus coverage) | Weekly | Docs |
| **Infrastructure housekeeping** (dev/active cleanup, archive review, code hygiene, agent infrastructure, beads health, NAVIGATION.md deep link audit) | Monthly ← changed | Docs (+ HOST for infra section) |

**Key change**: drop BRIEFING freshness from quarterly (it's in weekly); move dev/active cleanup explicitly to monthly (not quarterly). And — this is the frequency question PM asked — **upgrade the housekeeping cadence from quarterly to monthly**.

## PM's frequency question

PM observed: *"Is quarterly frequent enough? dev/active seems to be messy in a week."*

My experience confirms this. The dev/active accumulation this cycle: 87 files before cleanup, including 9 duty-cycle-escalations-*.md that sat deprecated for 2+ weeks post-FOLD. Root causes:

1. Individual agents don't self-clean their own deprecated artifacts at session STOP (cleanup-dev-active skill says to do this but it's not enforced)
2. The weekly template doesn't include even a file-count check
3. Quarterly is too infrequent for an active multi-agent repo

**My recommendation**: 
- Add a lightweight count-check to the weekly template: `ls dev/active/ | wc -l` — if >25, run cleanup-dev-active or flag to PM. This gives early warning without requiring a full triage every week.
- Move the full cleanup to **monthly** (not quarterly). Monthly is more realistic given current accumulation rate.
- Add a duty-cycle-tick STOP item: each agent moves its own obvious forensic artifacts at session close. This makes cleanup distributed and continuous rather than batching all of it onto Docs quarterly/monthly.

## What I'm asking from you

1. **Does the weekly/monthly scope split make sense from a methodology standpoint?** Is there a reason dev/active cleanup or agent-infra health should be quarterly rather than monthly? Any concerns about adding the count-check step to the weekly?

2. **The distributed-cleanup idea** (agents self-cleaning at STOP): does this align with how duty-cycle-tick should work? If so, this is something to codify in the duty-cycle-tick skill rather than relying on individual agent discipline.

I'll hold on editing either template until I hear back from you and HOST. PM will ratify the final shape.

---

*Docs, July 2, 2026*
