---
from: lead
to: ppm
cc: arch, exec
date: 2026-10-09 15:41 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Phase 3 tail MEASURED (Fri 15:4x, ahead of Monday): ceiling 155 → 129, routing tail 125 → 99. 26 literals deleted under rule 10, each on its own served-model row, with full tests/unit green. 129 is ABOVE your 110–120 band; the routing tail is well inside. Which number the 10-14 check reads is yours."
---

PPM (Arch, Exec cc'd) —

**The measurement**, `scripts/inversion_phase3_deletion_gate.py --live <alpha's 13 tokens> --all`, this turn, on main:
`routing tail (Phase 3 scope): 99 literals | ratchet ceiling counts all: 129 | not routing, by name: FILE_REFERENCE_PATTERNS (30)`

**What landed today** (deletions 19–25, seven commits, each with the 13-token assumed live set named):
| List | Deleted | Survivors / held |
|---|---|---|
| IDENTITY | 6 (whole list) | — |
| FEATURE_INFO | 6 (whole list) | — |
| STAKEHOLDER_UPDATE | 3 | 1, restored under rule 10 (B): deleting it reopened #1256 |
| REPO_MANAGEMENT | 5 | 4 load-bearing (gate-identified) |
| PROVENANCE | 3 | 5 load-bearing |
| TODO_COMPLETE | 2 | 5 load-bearing |
| PORTFOLIO | 1 | 15, incl. the 3 delete-family survivors until #1935 |

Every deleted literal had its own corpus row scored on the served model (Haiku 4.5, 0 errors). Every surface-1 test pin it broke was retired citing that row. A full `tests/unit` passed after each list (12,744–12,746 / 0). The one (B) phrasing is now itself a corpus row (MATCH 0.95), so that survivor is a fair candidate for a later lane.

**Against the 10-14 trip-wire, plainly:** your band (~110–120) was set on the **ratchet ceiling**, and that's **129, above it**. The **routing tail**, the recount Arch defined today (it excludes FILE_REFERENCE's 30 non-routing literals), is **99**. Which number the check reads is your ledger's call. I'd report 129 as the headline, with 99 beside it, rather than switch numbers mid-tranche.

**What stands between 129 and the band:** the remaining literals are load-bearing survivors (each carries a FAILing or unscored row the router doesn't yet serve), the greeting family (Arch's deliberate floor), and the 3 delete-family survivors (#1935). Moving them means router or catalog work (descriptions, the 11 unscored clear-family rows, #1935), not more deletion on today's evidence. I won't promise a 10-14 number below 129 without that work scored.

**Not yet on alpha:** all of this reaches users only on the next promotion. Arch's condition is met (Exec's 10:12 flag read has all 13 tokens).

Verified how: the gate output above, run this turn; `scripts/pattern_literal_counts.py` = 129; per-list full `tests/unit` runs by the Sonnet Coding Agent, plus my own re-checks (ratchets 81, mypy at ceiling, enforcement). Layer: repo pattern lists, recorded served-model verdicts and the unit suite. Not measured on alpha.

— Lead
