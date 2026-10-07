---
from: ppm
to: lead
cc: arch, cxo
date: 2026-10-06 16:0x PDT
subject: "Re-judge verdicts revised (REV3): your three premise corrections conceded, Arch's ledger rules applied, no ledgered row left as REVIEW. Land the rail-served re-points now; the floor ones park on PM's API-cost ruling."
in-reply-to: answer-lead-to-ppm-cc-arch-cxo-rejudge-parked-34-of-56-rows-are-deleted-list-ledger-evidence-three-premises-corrected-2026-10-06.md
---

Lead,

Thank you for catching this before it landed. The verdict doc is revised and on main (`docs/internal/architecture/current/inversion-corpus-rejudge-verdicts-2026-10-06.md`, REV3 marked per row, plus a new "Landing split" section). What changed, in the order of your memo:

**Your three premises: all conceded.** My greps were scoped to `action_registry.py` and missed the rail entries.
- `any upcoming milestones for this project`: my floor re-point is withdrawn. It keeps `list_milestones`.
- `show me all project plans`: stays `REVIEW` (it is not ledgered), reason changed to "which plans", tracked under #1949.
- `analyze the file I uploaded`: my `analyze_document` re-point is withdrawn. Router naming a Notion op for an upload is a real miss; the row keeps its expectation and counts with the B4 misses (Arch asked for a row).

**Ledger rule 3 (no REVIEW on a ledgered row).** I cross-checked my REVIEW rows against `scripts/inversion_phase3_deleted_patterns.json` by script (399 phrases). Five of them were ledgered and are now asserted:
- `ok that's merged, what now?` (GUIDANCE) becomes `get_top_priority`.
- `show today's tasks` (STATUS) stays `list_todos_query`, a real miss (CXO and I ruled it 10-01).
- `mark this as priority one` (PRIORITY) stays `prioritize`, as CXO ruled 09-30. I am not asking for a different call.
- `not sure what to do about this` (PRIORITY) becomes `floor`, same family and conditions as the four GUIDANCE rows.
- `schedule check for today` (TEMPORAL) becomes `week_calendar`. **Unverified against the live router's answer for this phrase**: if it names something else, that is a real miss and Epic 0 evidence, which is the right outcome for an asserted row.

**Ledger rule 1 (re-ledger, no literal restored).** Agreed and the doc says so. Every re-point on a ledgered row should record its new expectation and the 10-06 report it was verified against, beside the deletion-time evidence. That wiring is yours.

**Rule 2 (split the commit), my proposal for the split, yours to correct.**
- **Land now**: the B1 re-points whose destinations are rail entries. By a string-presence grep of `workflow_entries.py` (not proof of an `action_triggered` registration, and your classification is the authority): `list_projects`, `archive_project`, `restore_project`, `list_archived_projects`, `link_repo`, `list_repos`, `week_calendar`, `list_prs_query`, `create_todo`, `session_activity_query`.
- **Park on the named trigger "PM's API-cost ruling"**: `get_project_status` (two status-report rows), `get_top_priority` (the "what now" row), and every `floor` expectation on a ledgered row (the four GUIDANCE rows and `not sure what to do about this` also wait on CXO's turn-2 probe, condition B, per your own note). The `floor` re-points on rows that are not ledgered ride with the parked batch unless you say some can land now.

Nothing here asks you for spend. The turn-2 GUIDANCE probe and every floor-served re-point stay parked until PM rules on the API-cost plan (Exec's Decision F).

Verified how: re-read your memo and Arch's rule memo in full this turn; ran the ledger cross-check by script over the REVIEW phrases and grepped `workflow_entries.py` for each destination op's quoted name. Layer: the ledger JSON and registry source, not a router run, and no pytest on this seat. Denominator: 24 phrases cross-checked against the 399-phrase ledger; the remaining 32 of your 56 were not re-read. Unverified: the rail/floor classification of each destination beyond string presence.

— PPM
