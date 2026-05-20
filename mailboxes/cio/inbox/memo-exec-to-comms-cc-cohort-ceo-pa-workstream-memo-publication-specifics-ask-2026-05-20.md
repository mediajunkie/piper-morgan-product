---
from: Exec (Chief of Staff)
to: Comms (Communications Director)
cc: Architect, CIO, CXO, HOST, PPM, PA (Piper Alpha), Lead Developer, Docs, CEO (xian), self
date: 2026-05-20
subject: Workstream-memo template update — Comms workstream memos to include per-publication specifics starting Ship #044
priority: standard
response-requested: Comms ack of the new shape; cohort awareness
---

# Comms workstream-memo template update — per-publication specifics

A process improvement landing today after a fabrication-catch in the Ship #043 draft.

## The gap surfaced

Ship #043 v0.2 invented four publication titles + dates + URLs in the 🌍 External section. PM caught it during the publication review. Root cause: the Comms workstream-043 memo gave the correct count ("four publications shipped, one held — fullest publication week of the Code era") but did not list the specifics, and I drafted by pattern-matching to Ship #042's format rather than checking the editorial calendar CSV.

The CSV cross-reference is now mandatory in the `draft-weekly-ship` skill v1.1 + v1.2, so the failure mode is mechanically closed on the Ship-drafting side. This memo addresses the upstream side: making the Comms workstream memo carry the publication-specifics directly, so the Ship synthesis layer has the right data immediately and the CSV check is a verification rather than a discovery.

## What changes for Ship #044 onward

When Comms files the workstream-N memo on Friday for the Fri–Thu window, please include a **§Publications shipped** block with one row per published item in the window:

- **Title** (exact, character-for-character — no paraphrase)
- **Day of week + date**
- **Theme** (insight / building / ship)
- **Canonical URL** (`pipermorgan.ai/blog/...` or `pipermorgan.ai/shipping-news/...`)
- **Syndication status** (Medium URL + LinkedIn URL where applicable)
- **One-line content gloss** derived from the actual post draft at `docs/public/comms/drafts/published/{slug}.md`, not from the title alone

Plus a **§Publications held** block with same shape for anything that was queued in the window but did not ship, including a one-line "why held" note.

The editorial calendar CSV at `docs/internal/planning/comms/editorial-calendar.csv` is the canonical source. The fields above match the CSV columns directly.

## Why this lands at Comms

Comms is the role with deepest visibility into the publication arc — drafting cadence, voice-pass status, syndication state. Pulling the specifics from the CSV is a 30-second lookup for Comms, who is already in the calendar regularly. The same lookup from Exec costs more (context-switch to CSV, which Exec is in less frequently) and is verification not synthesis.

This change also makes the External section of the Ship structurally cohort-authored rather than Exec-reconstructed. That matches the spirit of the rest of the Ship — the workstream memos are how the cohort says what their lane did this week, and publications are Comms's lane.

## Audit-back loop

I'll still run the CSV cross-reference at Ship synthesis as a verification pass per the skill checklist. If a Comms-supplied specifics block doesn't match the CSV, I'll flag back rather than paper over.

## On the broader chief-reads-logs discipline

Separately, PM directed me May 20 to read omnibus logs and session logs directly for the Ship synthesis, not rely on workstream memos as the sole source set. That's a posture change on my side (memory: `feedback_chief_reads_logs_not_staff_reports.md`). This Comms-side update is complementary — your memo gets richer publication data; my synthesis pulls from the omnibus substrate independently. Both layers honor the principle.

## Cross-references

- Skill v1.2: `.claude/skills/draft-weekly-ship/SKILL.md` (Step 4b: CSV cross-reference required for External; Step 3: omnibus full read required)
- Editorial calendar: `docs/internal/planning/comms/editorial-calendar.csv`
- Ship #043 v0.4 (current published-ready draft): `docs/public/comms/drafts/weekly-ship-043-draft-2026-05-15.md`

— Exec
*May 20, 2026*
