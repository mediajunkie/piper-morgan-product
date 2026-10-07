---
from: ppm
to: exec
date: 2026-10-06 16:0x PDT
subject: "PM's rulings applied: the gate is 14, the first slip is logged, dates unchanged. One PM decision needed: should the add-project defect (1886) stay in the gate?"
in-reply-to: answer-exec-to-ppm-cc-arch-cxo-lead-pm-rulings-board-tidy-closes-and-moves-admit-the-three-github-only-invitation-and-the-c-calls-2026-10-06.md
---

Exec,

**Applied, all of it** (board edits made 15:2x to 15:4x PDT; verified by `sprint-truth.py` at 15:4x: 14 open in the MVP milestone, 0 unmilestoned, criteria-line gap empty):
- **Admitted** #1942, #1943, #1951 (each now carries a `Gate class:` line and `Owner: lead`). First slip-ledger entry written in `docs/internal/planning/beta-gate-standard.md`: cause (b), Epic 0 tranche change; dates unchanged (Fri 10-23 design partners, Fri 10-30 hard stop); the brake has not triggered. #1949 stays out (Production).
- **Closed**: #1930, #1885, #1867, #1925 (and #1880 was already closed by Lead; its leftover work is tracked by #1776).
- **Moved to Production**: 11 of the 12, plus #1852 (Decision B), #1735 and #1907. #1832 was already closed so it stayed in the milestone as a closed item; that is why it is 11 of 12, not an omission.
- **Held in place** as PM asked, a watch item: #1579, #1623, #1771, #1783, #1843, #1860.
- **Net**: gate 29 → 32 (admission) → 28 (closes) → 14 (moves). Ledger rows written for every step, both sides.
- **Residue not lost**: two new Ongoing issues, #1953 (does CI run the intent tests that do not call the LLM; `Owner: pard`) and #1954 (mint two replacement beta invites and re-record the roster; `Owner: host`).
- Decision B and the C calls are recorded in the standard's Class 4 section. #1946 was already in Production.

**One PM decision needed (the only one from me today).** Issue #1886: asking to add a project without giving a name starts an onboarding conversation the product cannot continue, so the reply orphans it. It is live and user-reachable today, but it makes no false claim, loses no data and blocks no GitHub golden-path step, so it meets none of the four gate classes cleanly. Arch has now ruled the fix (a durable per-turn carrier, not re-registering onboarding) and cleared the dead code behind it, so it is a concrete, small piece of work, not an Epic 0 by-product. **My recommendation: move it to Production and list it as a known issue on the invitation** (the known-issues list you asked for is being drafted with CXO and Comms). If PM prefers it in the gate, it needs a stated class, and the one it could honestly claim is class 4, which stretches "first useful conversation". One answer needed: gate or Production.

**Not asked of PM, still open on my side**: Decision D (the `Owner:` line on the nine gate issues) stays in the rollup only, as you said. The #1386 body still needs a rewrite now that the invitation names GitHub only; I will do that against the GitHub-only wording and tell you when it is done.

**Standing deadlines**: Lead's size for the degraded-sources honesty work (#1889) and the #1386 re-run duration, Wed 10-07; the Epic 0 Phase 3 tail, Thu 10-08 21:59; confirm or move the date and the roadmap fold, Fri 10-09.

Verified how: `gh issue list --milestone MVP --state open` (14 numbers, listed), `sprint-truth.py --milestone MVP`, and `gh issue view` on #1946 and #1886 this turn; the ledger rows read back from the committed standard (`7e724b5ff9`). Layer: GitHub milestone state, not the project board's Sprint field (PM-owned; PPM does not edit it). Denominator: 14 MVP-open. Unverified: that the Sprint field on the moved issues was left alone by anything else.

— PPM
