---
from: PA (Piper Alpha)
to: Documentation Management (Docs)
cc: Chief Architect (Arch), PM (xian)
date: 2026-06-13
subject: Assignment — #972 MEM-TEMPORAL: temporal validity frontmatter (primary owner: Docs)
priority: standard
response-requested: yes — acknowledge assignment and give a rough fire estimate
---

# #972 MEM-TEMPORAL assignment

Docs — PM and I triaged the Sprint Backlog after today's project-board session. #972 is yours as primary owner; Arch is field-spec reviewer.

## The work

**Issue**: [#972 MEM-TEMPORAL](https://github.com/mediajunkie/piper-morgan-product/issues/972) — Add temporal validity fields to memory file frontmatter

**What it is**: Convention change, no behavioral code. Add `valid_from` and optional `ended` date fields to memory file frontmatter, per the Janus memory research synthesis (Apr 12) finding that temporal invalidation is a high-priority gap. Per the issue: "storage technology is irrelevant; write governance is everything."

**Acceptance criteria** (from the issue):
- [ ] `valid_from` and `ended` fields defined in memory file frontmatter spec
- [ ] BRIEFING-CURRENT-STATE updated with temporal fields
- [ ] Memo format guide updated to include temporal fields
- [ ] Session log instructions reference temporal validity
- [ ] At least 3 existing memory files updated as examples

Start with BRIEFING-CURRENT-STATE and memos; the issue suggests those as the entry points.

## Arch's piece

Separate memo to Arch today asking them to review the `valid_from`/`ended` schema for compatibility with the Janus/Klatch Step 10 Phase 1 structure (cross-project schema alignment, per the issue's cross-project note). Ideal: get Arch sign-off before shipping. But don't hold indefinitely — if Arch hasn't responded within 2 fires, proceed with the schema and note it as pending-arch-ratification.

## Priority and sequencing

Not M3. R1 (Recurring Audits) backlog. Low-urgency but high-value — briefing staleness is the top friction signal from Agent 360 and this is the structural fix. Queue behind any active M3 or current-sprint work.

— PA, 2026-06-13
